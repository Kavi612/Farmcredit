"""Load and score the FarmCredit XGBoost risk model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_DIR = REPO_ROOT / "ml" / "artifacts" / "model"

DISPLAY_LABELS = {
    "state": "State",
    "district": "District",
    "crop_type": "Crop",
    "season": "Season",
    "land_size_ha": "Land size (ha)",
    "soil_type": "Soil type",
    "rainfall_mm": "Rainfall (mm)",
    "irrigation_type": "Irrigation",
    "loan_amount_inr": "Loan amount",
    "prior_loan_count": "Prior loans",
    "prior_default_flag": "Prior default",
    "repayment_score": "Repayment history",
    "annual_income_inr": "Annual farm income",
    "existing_debt_inr": "Existing debt",
}


class RiskModel:
    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = Path(model_dir) if model_dir else DEFAULT_MODEL_DIR
        bundle = joblib.load(self.model_dir / "model.joblib")
        self.model = bundle["model"]
        self.feature_columns: list[str] = bundle["feature_columns"]
        self.categorical_columns: list[str] = bundle["categorical_columns"]
        with (self.model_dir / "feature_schema.json").open(encoding="utf-8") as f:
            self.schema = json.load(f)
        self.risk_bands = self.schema["risk_bands"]

    def band(self, score: float) -> str:
        if score < self.risk_bands["Low"]:
            return "Low"
        if score < self.risk_bands["Medium"]:
            return "Medium"
        if score < self.risk_bands["High"]:
            return "High"
        return "Critical"

    def frame_from_features(self, features: dict[str, Any]) -> pd.DataFrame:
        data = {c: [features[c]] for c in self.feature_columns}
        df = pd.DataFrame(data)
        for col in self.categorical_columns:
            cats = self.schema["categories"][col]
            val = str(df.at[0, col])
            if val not in cats:
                raise ValueError(f"Invalid value for {col}: {val}. Allowed: {cats}")
            df[col] = pd.Categorical([val], categories=cats)
        return df

    def predict_score(self, features: dict[str, Any]) -> float:
        X = self.frame_from_features(features)
        score = float(np.clip(self.model.predict(X)[0], 0.0, 1.0))
        return score

    def predict(self, features: dict[str, Any]) -> dict[str, Any]:
        score = self.predict_score(features)
        return {
            "risk_score": round(score, 4),
            "risk_level": self.band(score),
        }
