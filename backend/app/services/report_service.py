"""Report + full assess orchestration."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.app.core.config import Settings
from backend.app.models.schemas import (
    AssessResponse,
    AdvisoryResponse,
    ExplainRiskResponse,
    FarmerFeatures,
    ReportResponse,
    RiskFactor,
)
from backend.app.services.advisory_service import AdvisoryService
from backend.app.services.demo_service import DemoService
from backend.app.services.risk_service import RiskService


class ReportService:
    def __init__(
        self,
        settings: Settings,
        risk_service: RiskService,
        advisory_service: AdvisoryService,
        demo_service: DemoService,
    ) -> None:
        self.settings = settings
        self.risk_service = risk_service
        self.advisory_service = advisory_service
        self.demo_service = demo_service

    def generate_report(
        self,
        *,
        features: FarmerFeatures | None = None,
        farmer_id: str | None = None,
        include_advisory: bool = True,
        use_demo_cache: bool = True,
        use_live_llm: bool = False,
    ) -> ReportResponse:
        if farmer_id and use_demo_cache and not use_live_llm:
            cache = self.demo_service.get_cache(farmer_id, required=False)
            if cache and cache.get("report"):
                report = cache["report"]
                return ReportResponse(
                    title=report.get("title", f"FarmCredit risk brief — {farmer_id}"),
                    farmer_summary={
                        "farmer_id": cache.get("id"),
                        "display_name": cache.get("display_name"),
                        "features": cache.get("features"),
                    },
                    risk_score=report["risk_score"],
                    risk_level=report["risk_level"],
                    top_factors=[RiskFactor(**f) for f in report.get("top_factors", [])],
                    advisory_text=report.get("advisory_text") if include_advisory else None,
                    generated_at=report.get("generated_at", datetime.now(timezone.utc).isoformat()),
                    cached=True,
                )

        if features is None and farmer_id:
            features = self.demo_service.get_farmer_features(farmer_id)
        if features is None:
            from backend.app.core.exceptions import AppError

            raise AppError(
                "features or farmer_id is required",
                code="validation_error",
                status_code=422,
            )

        prediction = self.risk_service.predict(features, include_shap=True)
        advisory_text = None
        if include_advisory:
            advisory = self.advisory_service.advise(
                features=features,
                farmer_id=farmer_id,
                risk_score=prediction.risk_score,
                risk_level=prediction.risk_level,
                top_factors=prediction.top_factors,
                use_demo_cache=False,
                use_live_llm=use_live_llm,
            )
            advisory_text = advisory.advisory_text

        return ReportResponse(
            title="FarmCredit risk brief",
            farmer_summary={"features": features.model_dump(), "farmer_id": farmer_id},
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            top_factors=prediction.top_factors,
            advisory_text=advisory_text,
            generated_at=datetime.now(timezone.utc).isoformat(),
            cached=False,
        )

    def generate_report_pdf(
        self,
        *,
        features: FarmerFeatures | None = None,
        farmer_id: str | None = None,
        include_advisory: bool = True,
        use_demo_cache: bool = True,
        use_live_llm: bool = False,
    ) -> tuple[bytes, str]:
        from backend.app.reports.pdf_generator import build_pdf

        report = self.generate_report(
            features=features,
            farmer_id=farmer_id,
            include_advisory=include_advisory,
            use_demo_cache=use_demo_cache,
            use_live_llm=use_live_llm,
        )
        payload = report.model_dump()
        pdf_bytes = build_pdf(payload)
        label = farmer_id or "custom"
        summary = payload.get("farmer_summary") or {}
        if summary.get("display_name"):
            label = str(summary["display_name"]).replace(" ", "_").lower()
        elif summary.get("farmer_id"):
            label = str(summary["farmer_id"]).lower()
        filename = f"farmcredit_report_{label}.pdf"
        return pdf_bytes, filename

    def assess(
        self,
        *,
        features: FarmerFeatures | None = None,
        farmer_id: str | None = None,
        use_live_llm: bool = False,
        use_demo_cache: bool | None = None,
        include_advisory: bool = True,
    ) -> AssessResponse:
        if use_demo_cache is None:
            use_demo_cache = self.settings.demo_use_cache_by_default

        if farmer_id and use_demo_cache and not use_live_llm:
            bundle = self.demo_service.get_bundle(farmer_id)
            pred = bundle.prediction
            expl = bundle.explanation
            assert pred is not None and expl is not None
            advisory = None
            if include_advisory:
                advisory = AdvisoryResponse(
                    advisory_text=bundle.advisory_text or "",
                    model_id="demo_cache",
                    latency_ms=0,
                    cached=True,
                )
            report = None
            if bundle.report:
                report = ReportResponse(
                    title=bundle.report.get("title", "FarmCredit risk brief"),
                    farmer_summary={
                        "farmer_id": bundle.id,
                        "display_name": bundle.display_name,
                        "features": bundle.features.model_dump(),
                    },
                    risk_score=bundle.report["risk_score"],
                    risk_level=bundle.report["risk_level"],
                    top_factors=[RiskFactor(**f) for f in bundle.report.get("top_factors", [])],
                    advisory_text=bundle.report.get("advisory_text"),
                    generated_at=bundle.report.get("generated_at"),
                    cached=True,
                )
            return AssessResponse(
                features=bundle.features,
                risk_score=pred.risk_score,
                risk_level=pred.risk_level,
                top_factors=pred.top_factors or expl.top_factors,
                explanation=expl,
                advisory=advisory,
                report=report,
                cached=True,
                farmer_id=bundle.id,
            )

        if features is None and farmer_id:
            features = self.demo_service.get_farmer_features(farmer_id)
        if features is None:
            from backend.app.core.exceptions import AppError

            raise AppError(
                "features or farmer_id is required",
                code="validation_error",
                status_code=422,
            )

        prediction = self.risk_service.predict(features, include_shap=True)
        explanation_raw = self.risk_service.explain(features, top_k=5)
        explanation = ExplainRiskResponse(**explanation_raw)

        advisory = None
        if include_advisory:
            advisory = self.advisory_service.advise(
                features=features,
                farmer_id=farmer_id,
                risk_score=prediction.risk_score,
                risk_level=prediction.risk_level,
                top_factors=prediction.top_factors,
                use_demo_cache=False,
                use_live_llm=use_live_llm,
            )

        report = self.generate_report(
            features=features,
            farmer_id=farmer_id,
            include_advisory=include_advisory,
            use_demo_cache=False,
            use_live_llm=use_live_llm,
        )

        return AssessResponse(
            features=features,
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            top_factors=prediction.top_factors,
            explanation=explanation,
            advisory=advisory,
            report=report,
            cached=False,
            farmer_id=farmer_id,
        )
