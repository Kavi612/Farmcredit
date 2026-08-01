"""Illustrative officer portfolio: 5 demos + synthetic applications."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from frontend.utils import api
from frontend.utils.constants import (
    CROPS,
    DISTRICTS_BY_STATE,
    IRRIGATION,
    SEASONS,
    SOILS,
    STATE_NAMES,
    STATES,
)

PORTFOLIO_PATH = Path(__file__).resolve().parents[1] / "data" / "officer_portfolio.json"
FIRST_NAMES = [
    "Asha", "Ravi", "Meena", "Suresh", "Kavita", "Anil", "Pooja", "Vikram",
    "Sunita", "Deepak", "Nisha", "Rahul", "Lata", "Manoj", "Geeta", "Arjun",
    "Priya", "Kiran", "Neha", "Sanjay",
]
LAST_NAMES = [
    "Patil", "Singh", "Devi", "Kumar", "Sharma", "Reddy", "Nair", "Yadav",
    "Ghosh", "Joshi", "Verma", "Das", "Khan", "Pillai", "Choudhary",
]


def _synthetic_features(rng: np.random.Generator, idx: int) -> dict[str, Any]:
    state = str(rng.choice(STATES))
    districts = DISTRICTS_BY_STATE[state]
    district = str(rng.choice(districts))
    crop_type = str(rng.choice(CROPS))
    season = "Rabi" if crop_type in {"Wheat", "Mustard"} else str(rng.choice(SEASONS))
    soil_type = str(rng.choice(SOILS))
    irrigation_type = str(rng.choice(IRRIGATION))
    land_size_ha = float(np.clip(rng.lognormal(0.1, 0.7), 0.2, 10.0))
    rainfall_mm = float(np.clip(rng.normal(850, 280), 280, 3200))
    annual_income_inr = int(np.clip(40_000 + land_size_ha * 55_000 * rng.uniform(0.7, 1.3), 40_000, 700_000))
    loan_amount_inr = int(np.clip(25_000 + land_size_ha * 40_000 + annual_income_inr * 0.2, 25_000, 800_000))
    existing_debt_inr = int(np.clip(rng.integers(0, 250_000), 0, 400_000))
    return {
        "state": state,
        "district": district,
        "crop_type": crop_type,
        "season": season,
        "land_size_ha": round(land_size_ha, 2),
        "soil_type": soil_type,
        "rainfall_mm": round(rainfall_mm, 1),
        "irrigation_type": irrigation_type,
        "loan_amount_inr": loan_amount_inr,
        "prior_loan_count": int(rng.integers(0, 7)),
        "prior_default_flag": int(rng.random() < 0.18),
        "repayment_score": float(np.clip(rng.normal(65, 18), 5, 100)),
        "annual_income_inr": annual_income_inr,
        "existing_debt_inr": existing_debt_inr,
    }


def _row_from_prediction(
    *,
    app_id: str,
    display_name: str,
    features: dict[str, Any],
    prediction: dict[str, Any],
    is_demo: bool,
    narrative: str | None = None,
) -> dict[str, Any]:
    return {
        "application_id": app_id,
        "display_name": display_name,
        "is_demo": is_demo,
        "narrative": narrative,
        "state": features["state"],
        "state_name": STATE_NAMES.get(features["state"], features["state"]),
        "district": features["district"],
        "crop_type": features["crop_type"],
        "season": features["season"],
        "loan_amount_inr": features["loan_amount_inr"],
        "land_size_ha": features["land_size_ha"],
        "risk_score": prediction["risk_score"],
        "risk_level": prediction["risk_level"],
        "top_factors": prediction.get("top_factors") or [],
        "features": features,
    }


def build_portfolio(n_synthetic: int = 40, seed: int = 42, include_shap: bool = False) -> list[dict[str, Any]]:
    """Build portfolio using live API scores (demos + synthetic rows)."""
    rows: list[dict[str, Any]] = []

    demos = api.list_demo_farmers()
    for demo in demos:
        bundle = api.get_demo_farmer(demo["id"])
        features = bundle["features"]
        prediction = bundle.get("prediction") or {}
        if include_shap and not prediction.get("top_factors"):
            prediction = api.predict_risk(features, include_shap=True)
        elif not prediction.get("top_factors"):
            # keep cache score; attach empty factors (detail view can refetch)
            prediction = {
                "risk_score": prediction.get("risk_score"),
                "risk_level": prediction.get("risk_level"),
                "top_factors": (bundle.get("explanation") or {}).get("top_factors", []),
            }
        rows.append(
            _row_from_prediction(
                app_id=demo["id"],
                display_name=bundle.get("display_name") or demo["id"],
                features=features,
                prediction=prediction,
                is_demo=True,
                narrative=bundle.get("narrative"),
            )
        )

    rng = np.random.default_rng(seed)
    for i in range(n_synthetic):
        features = _synthetic_features(rng, i)
        prediction = api.predict_risk(features, include_shap=include_shap)
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        rows.append(
            _row_from_prediction(
                app_id=f"APP-{i + 1:04d}",
                display_name=name,
                features=features,
                prediction=prediction,
                is_demo=False,
            )
        )

    rows.sort(key=lambda r: float(r["risk_score"]), reverse=True)
    return rows


def save_portfolio(rows: list[dict[str, Any]], path: Path | None = None) -> Path:
    out = path or PORTFOLIO_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": "Illustrative portfolio for dashboard demo — not real applicants.",
        "n_rows": len(rows),
        "applications": rows,
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def load_portfolio(path: Path | None = None) -> tuple[str, list[dict[str, Any]]]:
    src = path or PORTFOLIO_PATH
    if not src.exists():
        rows = build_portfolio()
        save_portfolio(rows, src)
        return "Illustrative portfolio for dashboard demo — not real applicants.", rows
    payload = json.loads(src.read_text(encoding="utf-8"))
    return payload.get("label", "Illustrative portfolio"), payload.get("applications", [])


def portfolio_to_dataframe_rows(
    applications: list[dict[str, Any]],
    decisions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    table = []
    for app in applications:
        app_id = app["application_id"]
        decision = decisions.get(app_id, {})
        table.append(
            {
                "application_id": app_id,
                "display_name": app["display_name"],
                "is_demo": app.get("is_demo", False),
                "state": app["state"],
                "state_name": app.get("state_name", app["state"]),
                "district": app["district"],
                "crop_type": app["crop_type"],
                "season": app.get("season"),
                "loan_amount_inr": app["loan_amount_inr"],
                "land_size_ha": app.get("land_size_ha"),
                "risk_score": app["risk_score"],
                "risk_level": app["risk_level"],
                "decision": decision.get("status", "Pending"),
                "decision_note": decision.get("note", ""),
                "decision_updated_at": decision.get("updated_at", ""),
            }
        )
    return table
