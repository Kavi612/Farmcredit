"""Generate synthetic FarmCredit tabular dataset with correlated default_risk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
FEATURE_COLUMNS = [
    "farmer_id",
    "state",
    "district",
    "crop_type",
    "season",
    "land_size_ha",
    "soil_type",
    "rainfall_mm",
    "irrigation_type",
    "loan_amount_inr",
    "prior_loan_count",
    "prior_default_flag",
    "repayment_score",
    "annual_income_inr",
    "existing_debt_inr",
    "default_risk",
]


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _weighted_choice(rng: np.random.Generator, weights: dict[str, float]) -> str:
    keys = list(weights.keys())
    vals = np.array([max(float(weights[k]), 0.0) for k in keys], dtype=float)
    if vals.sum() <= 0:
        vals = np.ones(len(keys), dtype=float)
    vals = vals / vals.sum()
    return str(rng.choice(keys, p=vals))


def _risk_band(score: float, bands: dict) -> str:
    if score < bands["Low"]:
        return "Low"
    if score < bands["Medium"]:
        return "Medium"
    if score < bands["High"]:
        return "High"
    return "Critical"


def generate_dataframe(cfg: dict) -> pd.DataFrame:
    rng = np.random.default_rng(cfg["seed"])
    n = int(cfg["n_rows"])
    noise_std = float(cfg.get("noise_std", 0.35))
    bands = cfg["risk_bands"]

    state_priors = _load_json(REPO_ROOT / cfg["paths"]["state_priors"])["states"]
    crop_water = _load_json(REPO_ROOT / cfg["paths"]["crop_water"])
    crops_meta = crop_water["crops"]
    irr_buffer = crop_water["irrigation_drought_buffer"]
    water_score = crop_water["water_intensity_score"]

    state_keys = list(state_priors.keys())
    state_w = np.array([state_priors[s]["sample_weight"] for s in state_keys], dtype=float)
    state_w = state_w / state_w.sum()

    rows: list[dict] = []
    for i in range(n):
        state = str(rng.choice(state_keys, p=state_w))
        sp = state_priors[state]
        district = str(rng.choice(sp["districts"]))
        soil_type = _weighted_choice(rng, sp["soil_weights"])
        crop_type = _weighted_choice(rng, sp["crop_weights"])
        crop = crops_meta[crop_type]
        season = str(rng.choice(crop["typical_seasons"]))

        rainfall_mm = float(
            np.clip(rng.normal(sp["rainfall_mm_mean"], sp["rainfall_mm_std"]), 250, 3500)
        )
        rain_deficit = (sp["rainfall_mm_mean"] - rainfall_mm) / max(sp["rainfall_mm_mean"], 1.0)

        # Irrigation biased by rainfall stress
        if rainfall_mm < 500:
            irr_weights = {"Rainfed": 0.35, "Tubewell": 0.35, "Canal": 0.15, "Drip": 0.15}
        elif rainfall_mm < 900:
            irr_weights = {"Rainfed": 0.25, "Tubewell": 0.35, "Canal": 0.25, "Drip": 0.15}
        else:
            irr_weights = {"Rainfed": 0.35, "Tubewell": 0.2, "Canal": 0.3, "Drip": 0.15}
        irrigation_type = _weighted_choice(rng, irr_weights)

        # Smallholder-skewed land
        land_size_ha = float(np.clip(rng.lognormal(mean=0.15, sigma=0.75), 0.2, 10.0))

        wi = crop["water_intensity"]
        drought_sens = float(crop["drought_sensitivity"])
        buffer = float(irr_buffer[irrigation_type])
        climate_stress = max(0.0, rain_deficit) * drought_sens * (1.0 - buffer)
        climate_stress += water_score[wi] * max(0.0, rain_deficit) * (0.6 if irrigation_type == "Rainfed" else 0.25)

        soil_bonus = 0.08 if soil_type in crop["preferred_soils"] else -0.06
        yield_mult = float(np.clip(1.0 - 0.55 * climate_stress + soil_bonus + rng.normal(0, 0.08), 0.35, 1.35))
        yield_qtl = float(
            np.clip(
                rng.normal(crop["base_yield_qtl_ha"], crop["yield_std_qtl_ha"]) * yield_mult,
                0.5,
                crop["base_yield_qtl_ha"] * 1.6,
            )
        )
        gross = land_size_ha * yield_qtl * float(crop["price_inr_per_qtl"])
        annual_income_inr = int(np.clip(gross * rng.uniform(0.55, 0.85), 40_000, 700_000))

        # Loan correlated with land + income, with over-borrow noise
        base_loan = 25_000 + land_size_ha * 45_000 + annual_income_inr * 0.25
        loan_amount_inr = int(np.clip(base_loan * rng.uniform(0.7, 1.45), 25_000, 800_000))
        existing_debt_inr = int(np.clip(rng.lognormal(10.2, 1.1), 0, 400_000))
        if rng.random() < 0.18:
            existing_debt_inr = 0

        prior_loan_count = int(np.clip(rng.poisson(2.2), 0, 8))
        # Weak history correlated with climate/leverage stress later
        prior_default_flag = 0
        repayment_score = float(np.clip(rng.normal(72, 14), 5, 100))

        dti = (loan_amount_inr + existing_debt_inr) / max(annual_income_inr, 1)
        loan_to_land = loan_amount_inr / max(land_size_ha, 0.2)

        latent = (
            -1.1
            + 1.6 * climate_stress
            + 0.9 * water_score[wi] * (1.0 if irrigation_type == "Rainfed" else 0.35) * max(0.0, rain_deficit + 0.15)
            + 0.85 * np.clip(dti - 1.0, -0.5, 3.0)
            + 0.55 * np.clip((loan_to_land - 120_000) / 200_000, -0.5, 2.0)
            + 0.7 * (1.0 if prior_default_flag else 0.0)
            - 0.012 * (repayment_score - 60)
            - 0.35 * buffer
            + (0.15 if land_size_ha < 1.0 else 0.0)
            + rng.normal(0.0, noise_std)
        )

        # Assign history with feedback from latent (still causal for learner)
        if latent > 0.8 and rng.random() < 0.45:
            prior_default_flag = 1
            repayment_score = float(np.clip(repayment_score - rng.uniform(15, 35), 5, 100))
            latent += 0.45
        elif latent < -0.2 and rng.random() < 0.5:
            repayment_score = float(np.clip(repayment_score + rng.uniform(5, 15), 5, 100))
            latent -= 0.2

        default_risk = float(1.0 / (1.0 + np.exp(-latent)))
        default_risk = float(np.clip(default_risk, 0.01, 0.99))

        rows.append(
            {
                "farmer_id": f"FC-{i + 1:06d}",
                "state": state,
                "district": district,
                "crop_type": crop_type,
                "season": season,
                "land_size_ha": round(land_size_ha, 2),
                "soil_type": soil_type,
                "rainfall_mm": round(rainfall_mm, 1),
                "irrigation_type": irrigation_type,
                "loan_amount_inr": loan_amount_inr,
                "prior_loan_count": prior_loan_count,
                "prior_default_flag": prior_default_flag,
                "repayment_score": round(repayment_score, 1),
                "annual_income_inr": annual_income_inr,
                "existing_debt_inr": existing_debt_inr,
                "default_risk": round(default_risk, 4),
                "risk_band": _risk_band(default_risk, bands),
            }
        )

    return pd.DataFrame(rows)


def stratified_split(
    df: pd.DataFrame, train_frac: float, val_frac: float, seed: int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    train_parts, val_parts, test_parts = [], [], []
    for _, group in df.groupby("risk_band", sort=False):
        idx = np.arange(len(group))
        rng.shuffle(idx)
        n = len(idx)
        n_train = int(round(n * train_frac))
        n_val = int(round(n * val_frac))
        train_idx = idx[:n_train]
        val_idx = idx[n_train : n_train + n_val]
        test_idx = idx[n_train + n_val :]
        train_parts.append(group.iloc[train_idx])
        val_parts.append(group.iloc[val_idx])
        test_parts.append(group.iloc[test_idx])

    train = pd.concat(train_parts).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    val = pd.concat(val_parts).sample(frac=1.0, random_state=seed + 1).reset_index(drop=True)
    test = pd.concat(test_parts).sample(frac=1.0, random_state=seed + 2).reset_index(drop=True)
    return train, val, test


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FarmCredit synthetic dataset")
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "ml" / "configs" / "generate_config.yaml"),
    )
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    df = generate_dataframe(cfg)
    train, val, test = stratified_split(df, cfg["train_frac"], cfg["val_frac"], cfg["seed"])

    raw_path = REPO_ROOT / cfg["paths"]["raw_csv"]
    train_path = REPO_ROOT / cfg["paths"]["train_csv"]
    val_path = REPO_ROOT / cfg["paths"]["val_csv"]
    test_path = REPO_ROOT / cfg["paths"]["test_csv"]
    for p in [raw_path, train_path, val_path, test_path]:
        p.parent.mkdir(parents=True, exist_ok=True)

    export_cols = FEATURE_COLUMNS  # risk_band used only for split
    df[export_cols].to_csv(raw_path, index=False)
    train[export_cols].to_csv(train_path, index=False)
    val[export_cols].to_csv(val_path, index=False)
    test[export_cols].to_csv(test_path, index=False)

    print(f"Wrote {len(df)} rows -> {raw_path}")
    print(f"train={len(train)} val={len(val)} test={len(test)}")
    print("Risk band distribution (full):")
    print(df["risk_band"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
