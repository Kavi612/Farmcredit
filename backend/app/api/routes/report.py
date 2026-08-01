"""Report generation routes (JSON + PDF)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from backend.app.api.deps import get_report_service
from backend.app.models.schemas import ReportRequest, ReportResponse
from backend.app.services.report_service import ReportService

router = APIRouter(tags=["report"])


@router.post("/generate-report", response_model=ReportResponse)
def generate_report(
    body: ReportRequest,
    report_service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    return report_service.generate_report(
        features=body.features,
        farmer_id=body.farmer_id,
        include_advisory=body.include_advisory,
        use_demo_cache=body.use_demo_cache,
        use_live_llm=body.use_live_llm,
    )


@router.post("/generate-report/pdf")
def generate_report_pdf(
    body: ReportRequest,
    report_service: ReportService = Depends(get_report_service),
) -> Response:
    pdf_bytes, filename = report_service.generate_report_pdf(
        features=body.features,
        farmer_id=body.farmer_id,
        include_advisory=body.include_advisory,
        use_demo_cache=body.use_demo_cache,
        use_live_llm=body.use_live_llm,
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
