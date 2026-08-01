"""Risk prediction and SHAP explanation routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.deps import AppState, get_app_state, get_risk_service
from backend.app.core.exceptions import AppError
from backend.app.models.schemas import (
    ExplainRiskRequest,
    ExplainRiskResponse,
    FarmerFeatures,
    PredictRiskRequest,
    PredictRiskResponse,
    RiskFactor,
)
from backend.app.services.demo_service import DemoService
from backend.app.services.risk_service import RiskService

router = APIRouter(tags=["risk"])


def get_demo_service(state: AppState = Depends(get_app_state)) -> DemoService:
    return DemoService(state.settings.demo_farmers_file, state.settings.demo_cache_path)


@router.post("/predict-risk", response_model=PredictRiskResponse)
def predict_risk(
    body: PredictRiskRequest,
    risk_service: RiskService = Depends(get_risk_service),
) -> PredictRiskResponse:
    return risk_service.predict(body, include_shap=body.include_shap)


@router.post("/explain-risk", response_model=ExplainRiskResponse)
def explain_risk(
    body: ExplainRiskRequest,
    risk_service: RiskService = Depends(get_risk_service),
    demo_service: DemoService = Depends(get_demo_service),
) -> ExplainRiskResponse:
    features: FarmerFeatures | None = body.features
    if features is None and body.farmer_id:
        features = demo_service.get_farmer_features(body.farmer_id)
    if features is None:
        raise AppError(
            "Provide features or farmer_id",
            code="validation_error",
            status_code=422,
        )
    raw = risk_service.explain(features, top_k=body.top_k)
    return ExplainRiskResponse(
        baseline=raw["baseline"],
        prediction=raw["prediction"],
        risk_level=raw["risk_level"],
        top_factors=[RiskFactor(**f) for f in raw["top_factors"]],
        protective_factors=[RiskFactor(**f) for f in raw.get("protective_factors", [])],
        waterfall_image_url=None,
    )
