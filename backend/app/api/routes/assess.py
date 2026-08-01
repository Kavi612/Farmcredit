"""Orchestrated assess route (predict + explain + advisory)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.deps import get_report_service
from backend.app.models.schemas import AssessRequest, AssessResponse
from backend.app.services.report_service import ReportService

router = APIRouter(tags=["assess"])


@router.post("/assess", response_model=AssessResponse)
def assess(
    body: AssessRequest,
    report_service: ReportService = Depends(get_report_service),
) -> AssessResponse:
    return report_service.assess(
        features=body.features,
        farmer_id=body.farmer_id,
        use_live_llm=body.use_live_llm,
        use_demo_cache=body.use_demo_cache,
        include_advisory=body.include_advisory,
    )
