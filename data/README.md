# FarmCredit AI — Datasets

## Important: synthetic data only

All tabular farmer/loan records in this folder are **synthetically generated** for a resume/portfolio demo.

They are designed to **mirror the structure, value ranges, and risk correlations** of Indian agricultural credit contexts (state–soil–rainfall patterns, common crops, KCC-like loan sizes). They are **not** scraped or downloaded from NABARD, IMD, ICAR, or any government portal, and must not be presented as official statistics.

The instruction-tuning / LLM corpus (if present under `llm/data/`) is likewise synthetic or template-generated for demo fine-tuning.

---

## Layout

```text
data/
├── README.md                 # this file
├── reference/                # priors used by the generator (not raw gov dumps)
│   ├── state_priors.json
│   └── crop_water.json
├── raw/
│   └── farmcredit_synthetic.csv
└── processed/
    ├── train.csv             # ~70%
    ├── val.csv               # ~15%
    └── test.csv              # ~15%
```

Demo farmer profiles and precomputed API caches live under the backend (not here):

- `backend/app/data/demo_farmers.json`
- `backend/app/data/demo_cache/{DEMO-0x}.json`

---

## Tabular schema (FarmerFeatures + target)

Row count: **10,000** total, stratified split **70 / 15 / 15** by risk band.  
Random seed: **42** (set in `ml/configs/generate_config.yaml`).

| Column | Type | Allowed values / range | In model input? |
|---|---|---|---|
| `farmer_id` | string | `FC-000001` … | No (dropped before train) |
| `state` | category | MH, UP, MP, RJ, KA, AP, TG, PB, HR, GJ, TN, BR | Yes |
| `district` | category | Synthetic agro-zone per state (e.g. `MH-Vidarbha`) | Yes |
| `crop_type` | category | Rice, Wheat, Cotton, Sugarcane, Soybean, Maize, Pulses, Groundnut, Mustard, Millet | Yes |
| `season` | category | Kharif, Rabi, Zaid | Yes |
| `land_size_ha` | float | 0.2 – 10.0 | Yes |
| `soil_type` | category | Alluvial, Black, Red, Laterite, Sandy, ClayLoam | Yes |
| `rainfall_mm` | float | ~300 – 3200 (state-conditioned) | Yes |
| `irrigation_type` | category | Rainfed, Canal, Tubewell, Drip | Yes |
| `loan_amount_inr` | int | 25,000 – 800,000 | Yes |
| `prior_loan_count` | int | 0 – 8 | Yes |
| `prior_default_flag` | int | 0 or 1 | Yes |
| `repayment_score` | float | 0 – 100 (higher = better) | Yes |
| `annual_income_inr` | int | 40,000 – 700,000 | Yes |
| `existing_debt_inr` | int | 0 – 400,000 | Yes |
| `default_risk` | float | **0.0 – 1.0** (training target) | Target only |

This column set matches the Phase 7 FastAPI `FarmerFeatures` contract (plus `default_risk` for supervised training).

---

## Risk bands (locked)

Mapped from predicted / true `default_risk` for UI, metrics, and demo labels:

| Band | Score |
|---|---|
| Low | `< 0.25` |
| Medium | `>= 0.25` and `< 0.50` |
| High | `>= 0.50` and `< 0.75` |
| Critical | `>= 0.75` |

Thresholds are also persisted in `ml/artifacts/model/feature_schema.json` so the backend does not drift from training.

---

## How labels are created (correlation signal)

Rows are **not** independent random noise. Generation follows a causal-ish order:

1. Sample `state` → condition soil mix and rainfall baseline  
2. Sample `crop_type` / `season` with state-aware priors  
3. Sample `irrigation_type` influenced by rainfall  
4. Derive income from land × crop productivity proxies ± climate stress  
5. Sample loan / debt / repayment history with mild leverage correlation  
6. Compute a latent risk score from stress factors + noise  
7. Map through a sigmoid to `default_risk` ∈ [0, 1]

**Higher risk** tends to follow: low rainfall + water-intensive crop + rainfed irrigation; high debt-to-income; small land with large loan; prior default / weak repayment.  
**Lower risk** tends to follow: canal/drip, adequate rain, climate-fit crops (e.g. millet in dry zones), strong repayment history.

That structure gives XGBoost real interactions to learn; SHAP explanations should then align with agricultural intuition on the five demo farmers.

---

## Regeneration

From the repo root (after `ml` deps are installed):

```bash
python -m ml.src.generate_synthetic
```

Do not hand-edit processed CSVs for demos — change the generator or demo JSON instead.
