"""Risk scoring orchestration (XGBoost + optional SHAP)."""

from __future__ import annotations

from typing import Any

from backend.app.core.exceptions import AppError, ModelNotReadyError
from backend.app.ml.risk_model import RiskModel
from backend.app.ml.shap_explainer import ShapExplainer
from backend.app.models.schemas import FarmerFeatures, PredictRiskResponse, RiskFactor


class RiskService:
    def __init__(
        self,
        risk_model: RiskModel | None,
        shap_explainer: ShapExplainer | None,
    ) -> None:
        self.risk_model = risk_model
        self.shap_explainer = shap_explainer

    def _require_model(self) -> RiskModel:
        if self.risk_model is None:
            raise ModelNotReadyError()
        return self.risk_model

    def predict(
        self,
        features: FarmerFeatures,
        include_shap: bool = True,
    ) -> PredictRiskResponse:
        model = self._require_model()
        feat = features.model_dump()
        try:
            result = model.predict(feat)
        except ValueError as exc:
            raise AppError(str(exc), code="validation_error", status_code=422) from exc

        top_factors: list[RiskFactor] = []
        if include_shap:
            if self.shap_explainer is None:
                raise ModelNotReadyError("SHAP explainer is not loaded")
            explanation = self.shap_explainer.explain(feat, top_k=5)
            top_factors = [RiskFactor(**f) for f in explanation["top_factors"]]

        return PredictRiskResponse(
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            top_factors=top_factors,
        )

    def explain(self, features: FarmerFeatures, top_k: int = 5) -> dict[str, Any]:
        if self.shap_explainer is None:
            raise ModelNotReadyError("SHAP explainer is not loaded")
        feat = features.model_dump()
        try:
            return self.shap_explainer.explain(feat, top_k=top_k)
        except ValueError as exc:
            raise AppError(str(exc), code="validation_error", status_code=422) from exc
