"""Advisory generation with demo-cache, template, or live LLM fallbacks."""

from __future__ import annotations

import time
from typing import Any

from backend.app.core.config import Settings
from backend.app.llm.prompts import template_advisory
from backend.app.models.schemas import AdvisoryResponse, FarmerFeatures, RiskFactor
from backend.app.services.demo_service import DemoService


class AdvisoryService:
    def __init__(
        self,
        settings: Settings,
        demo_service: DemoService,
        llm_client: Any | None = None,
    ) -> None:
        self.settings = settings
        self.demo_service = demo_service
        self.llm_client = llm_client

    def advise(
        self,
        *,
        features: FarmerFeatures | None = None,
        farmer_id: str | None = None,
        risk_score: float | None = None,
        risk_level: str | None = None,
        top_factors: list[RiskFactor] | None = None,
        question: str | None = None,
        use_demo_cache: bool = True,
        use_live_llm: bool = False,
        display_name: str | None = None,
    ) -> AdvisoryResponse:
        top_factors = top_factors or []

        if farmer_id and use_demo_cache and not use_live_llm:
            cache = self.demo_service.get_cache(farmer_id, required=False)
            if cache and cache.get("advisory_text"):
                return AdvisoryResponse(
                    advisory_text=cache["advisory_text"],
                    model_id="demo_cache",
                    latency_ms=0,
                    cached=True,
                    degraded=False,
                )

        if features is None and farmer_id:
            features = self.demo_service.get_farmer_features(farmer_id)

        if features is None:
            from backend.app.core.exceptions import AppError

            raise AppError(
                "features or farmer_id is required for advisory",
                code="validation_error",
                status_code=422,
            )

        factor_dicts = [f.model_dump() if isinstance(f, RiskFactor) else f for f in top_factors]

        if use_live_llm and self.settings.llm_enabled and self.llm_client is not None:
            try:
                if not getattr(self.llm_client, "is_loaded", False):
                    self.llm_client.load()
                text, latency = self.llm_client.generate_advisory(
                    features.model_dump(),
                    float(risk_score or 0.0),
                    str(risk_level or "Medium"),
                    factor_dicts,
                    question,
                )
                return AdvisoryResponse(
                    advisory_text=text,
                    model_id=getattr(self.llm_client, "model_id", self.settings.hf_model_id),
                    latency_ms=latency,
                    cached=False,
                    degraded=False,
                )
            except Exception as exc:  # noqa: BLE001
                text = template_advisory(
                    str(risk_level or "Medium"),
                    factor_dicts,
                    display_name=display_name,
                )
                return AdvisoryResponse(
                    advisory_text=f"{text}\n\n(Live model unavailable: {exc})",
                    model_id="template_fallback",
                    latency_ms=0,
                    cached=False,
                    degraded=True,
                )

        start = time.perf_counter()
        text = template_advisory(
            str(risk_level or "Medium"),
            factor_dicts,
            display_name=display_name,
        )
        latency_ms = int((time.perf_counter() - start) * 1000)
        return AdvisoryResponse(
            advisory_text=text,
            model_id="template",
            latency_ms=latency_ms,
            cached=False,
            degraded=not self.settings.llm_enabled,
        )
