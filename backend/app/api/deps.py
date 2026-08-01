"""FastAPI dependencies and shared application state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from fastapi import Depends, Request

from backend.app.core.config import Settings, get_settings
from backend.app.core.exceptions import ModelNotReadyError
from backend.app.services.advisory_service import AdvisoryService
from backend.app.services.demo_service import DemoService
from backend.app.services.report_service import ReportService
from backend.app.services.risk_service import RiskService

if TYPE_CHECKING:
    from backend.app.ml.risk_model import RiskModel
    from backend.app.ml.shap_explainer import ShapExplainer


@dataclass
class AppState:
    settings: Settings
    risk_model: RiskModel | None = None
    shap_explainer: ShapExplainer | None = None
    llm_client: Any | None = None
    llm_load_error: str | None = None
    xgb_load_error: str | None = None


def get_app_settings() -> Settings:
    return get_settings()


def get_app_state(request: Request) -> AppState:
    return request.app.state.farmcredit


def get_risk_service(state: AppState = Depends(get_app_state)) -> RiskService:
    if state.risk_model is None:
        detail = state.xgb_load_error or "Risk model is not loaded"
        raise ModelNotReadyError(detail)
    return RiskService(state.risk_model, state.shap_explainer)


def get_demo_service(state: AppState = Depends(get_app_state)) -> DemoService:
    return DemoService(state.settings.demo_farmers_file, state.settings.demo_cache_path)


def get_advisory_service(state: AppState = Depends(get_app_state)) -> AdvisoryService:
    return AdvisoryService(
        settings=state.settings,
        demo_service=get_demo_service(state),
        llm_client=state.llm_client,
    )


def get_report_service(state: AppState = Depends(get_app_state)) -> ReportService:
    return ReportService(
        settings=state.settings,
        risk_service=get_risk_service(state),
        advisory_service=get_advisory_service(state),
        demo_service=get_demo_service(state),
    )
