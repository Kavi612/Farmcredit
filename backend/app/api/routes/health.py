"""Health and readiness endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.deps import AppState, get_app_state
from backend.app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(state: AppState = Depends(get_app_state)) -> HealthResponse:
    settings = state.settings
    return HealthResponse(
        status="ok" if state.risk_model is not None else "degraded",
        app_name=settings.app_name,
        app_env=settings.app_env,
        xgb_loaded=state.risk_model is not None,
        shap_ready=state.shap_explainer is not None,
        llm_enabled=settings.llm_enabled,
        llm_loaded=state.llm_client is not None,
        model_dir=str(settings.model_dir_path),
    )
