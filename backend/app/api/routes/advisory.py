"""Advisory endpoint (cache / template / live LLM)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.deps import (
    AppState,
    get_advisory_service,
    get_app_state,
    get_risk_service,
)
from backend.app.core.exceptions import AppError
from backend.app.models.schemas import AdvisoryRequest, AdvisoryResponse, FarmerFeatures
from backend.app.services.advisory_service import AdvisoryService
from backend.app.services.demo_service import DemoService
from backend.app.services.risk_service import RiskService

router = APIRouter(tags=["advisory"])


def get_demo_service(state: AppState = Depends(get_app_state)) -> DemoService:
    return DemoService(state.settings.demo_farmers_file, state.settings.demo_cache_path)


@router.post("/advisory", response_model=AdvisoryResponse)
def advisory(
    body: AdvisoryRequest,
    advisory_service: AdvisoryService = Depends(get_advisory_service),
    risk_service: RiskService = Depends(get_risk_service),
    demo_service: DemoService = Depends(get_demo_service),
) -> AdvisoryResponse:
    features = body.features
    if features is None and body.farmer_id:
        features = demo_service.get_farmer_features(body.farmer_id)

    risk_score = body.risk_score
    risk_level = body.risk_level
    top_factors = body.top_factors

    if features is not None and (risk_score is None or risk_level is None or not top_factors):
        prediction = risk_service.predict(features, include_shap=True)
        risk_score = risk_score if risk_score is not None else prediction.risk_score
        risk_level = risk_level or prediction.risk_level
        top_factors = top_factors or prediction.top_factors

    if features is None and not body.farmer_id:
        raise AppError(
            "Provide features or farmer_id",
            code="validation_error",
            status_code=422,
        )

    return advisory_service.advise(
        features=features,
        farmer_id=body.farmer_id,
        risk_score=risk_score,
        risk_level=risk_level,
        top_factors=top_factors,
        question=body.question,
        use_demo_cache=body.use_demo_cache,
        use_live_llm=body.use_live_llm,
    )
