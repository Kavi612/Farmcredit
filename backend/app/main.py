"""FarmCredit AI FastAPI application entrypoint."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.deps import AppState
from backend.app.api.routes import (
    advisory as advisory_routes,
    assess as assess_routes,
    demo as demo_routes,
    health as health_routes,
    report as report_routes,
    risk as risk_routes,
)
from backend.app.core.config import get_settings
from backend.app.core.exceptions import AppError, app_error_handler
from backend.app.ml.risk_model import RiskModel
from backend.app.ml.shap_explainer import ShapExplainer

logger = logging.getLogger("farmcredit")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    state = AppState(settings=settings)

    try:
        state.risk_model = RiskModel(model_dir=settings.model_dir_path)
        state.shap_explainer = ShapExplainer(state.risk_model)
        logger.info("Loaded XGBoost + SHAP from %s", settings.model_dir_path)
    except Exception as exc:  # noqa: BLE001 — surface in /health for demo hosts
        state.xgb_load_error = str(exc)
        logger.exception("Failed to load risk model artifacts: %s", exc)

    if settings.llm_enabled:
        try:
            from backend.app.llm.mistral_client import MistralClient

            client = MistralClient(settings)
            state.llm_client = client
            if settings.llm_eager_load:
                client.load()
                logger.info("LLM eager-loaded: %s", client.model_id)
            else:
                logger.info("LLM client ready (lazy load on first /advisory)")
        except Exception as exc:  # noqa: BLE001
            state.llm_load_error = str(exc)
            logger.exception("Failed to initialize LLM client: %s", exc)

    app.state.farmcredit = state
    yield
    app.state.farmcredit = None


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Agricultural credit risk scoring, SHAP explanations, and advisory API",
        lifespan=lifespan,
    )
    app.state.farmcredit = AppState(settings=settings)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_routes.router)
    app.include_router(risk_routes.router)
    app.include_router(demo_routes.router)
    app.include_router(advisory_routes.router)
    app.include_router(report_routes.router)
    app.include_router(assess_routes.router)
    return app


app = create_app()
