"""SHAP TreeExplainer wrapper returning Phase-7 RiskFactor dicts."""

from __future__ import annotations

from typing import Any

import numpy as np
import shap

from backend.app.ml.risk_model import DISPLAY_LABELS, RiskModel

PLAIN_HINTS = {
    "rainfall_mm": {
        "up": "Rainfall conditions in your area raised repayment risk",
        "down": "Rainfall conditions helped lower repayment risk",
    },
    "crop_type": {
        "up": "Crop choice is water-demanding or poorly matched to conditions",
        "down": "Crop choice fits local conditions better than average",
    },
    "irrigation_type": {
        "up": "Irrigation setup left the farm more exposed to weather stress",
        "down": "Irrigation setup helped protect against weather stress",
    },
    "loan_amount_inr": {
        "up": "Loan size is high relative to what similar farms typically carry",
        "down": "Loan size is manageable compared with similar farms",
    },
    "existing_debt_inr": {
        "up": "Existing debt increased pressure on repayment capacity",
        "down": "Lower existing debt reduced pressure on repayment",
    },
    "annual_income_inr": {
        "up": "Farm income looks thin for the loan burden",
        "down": "Farm income provides a stronger buffer for repayment",
    },
    "land_size_ha": {
        "up": "Smaller landholding raised leverage risk",
        "down": "Land size supported a more comfortable loan profile",
    },
    "prior_default_flag": {
        "up": "A past default signal pushed risk higher",
        "down": "No prior default helped keep risk lower",
    },
    "repayment_score": {
        "up": "Weaker repayment history increased risk",
        "down": "Stronger repayment history lowered risk",
    },
    "prior_loan_count": {
        "up": "More prior borrowing added to credit stress",
        "down": "Limited prior borrowing kept credit stress lower",
    },
    "soil_type": {
        "up": "Soil type is a weaker match for the chosen crop",
        "down": "Soil type supports the chosen crop reasonably well",
    },
    "season": {
        "up": "Season timing added some risk for this crop profile",
        "down": "Season timing is a reasonable fit for this crop",
    },
    "state": {
        "up": "State-level climate/credit patterns raised risk vs baseline",
        "down": "State-level patterns were slightly protective vs baseline",
    },
    "district": {
        "up": "Local district conditions raised risk vs baseline",
        "down": "Local district conditions were slightly protective",
    },
}


def _plain_hint(feature: str, direction: str) -> str:
    key = "up" if direction == "increases_risk" else "down"
    hints = PLAIN_HINTS.get(feature)
    if hints:
        return hints[key]
    label = DISPLAY_LABELS.get(feature, feature)
    if direction == "increases_risk":
        return f"{label} pushed risk above the average farmer"
    return f"{label} pulled risk below the average farmer"


def _to_python(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value


class ShapExplainer:
    def __init__(self, risk_model: RiskModel) -> None:
        self.risk_model = risk_model
        self.explainer = shap.TreeExplainer(risk_model.model)

    def explain(self, features: dict[str, Any], top_k: int = 5) -> dict[str, Any]:
        X = self.risk_model.frame_from_features(features)
        prediction = float(np.clip(self.risk_model.model.predict(X)[0], 0.0, 1.0))

        shap_values = self.explainer.shap_values(X)
        if isinstance(shap_values, list):
            shap_row = np.asarray(shap_values[0]).reshape(-1)
        else:
            shap_row = np.asarray(shap_values).reshape(-1)

        expected = self.explainer.expected_value
        if isinstance(expected, (list, np.ndarray)):
            baseline = float(np.asarray(expected).reshape(-1)[0])
        else:
            baseline = float(expected)

        factors: list[dict[str, Any]] = []
        for i, col in enumerate(self.risk_model.feature_columns):
            sv = float(shap_row[i])
            direction = "increases_risk" if sv >= 0 else "decreases_risk"
            raw_val = _to_python(X.iloc[0][col])
            factors.append(
                {
                    "feature": col,
                    "display_label": DISPLAY_LABELS.get(col, col),
                    "feature_value": raw_val,
                    "shap_value": round(sv, 6),
                    "direction": direction,
                    "points": int(round(sv * 100)),
                    "plain_hint": _plain_hint(col, direction),
                }
            )

        factors_sorted = sorted(factors, key=lambda f: abs(f["shap_value"]), reverse=True)
        top_factors = factors_sorted[:top_k]
        protective = [f for f in factors_sorted if f["direction"] == "decreases_risk"][:3]

        return {
            "baseline": round(baseline, 4),
            "prediction": round(prediction, 4),
            "risk_level": self.risk_model.band(prediction),
            "top_factors": top_factors,
            "protective_factors": protective,
        }
