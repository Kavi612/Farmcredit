"""Demo farmer listing and cached bundle routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.deps import AppState, get_app_state
from backend.app.models.schemas import DemoFarmerBundle, DemoFarmerSummary
from backend.app.services.demo_service import DemoService

router = APIRouter(tags=["demo"])


def get_demo_service(state: AppState = Depends(get_app_state)) -> DemoService:
    return DemoService(state.settings.demo_farmers_file, state.settings.demo_cache_path)


@router.get("/demo-farmers", response_model=list[DemoFarmerSummary])
def list_demo_farmers(
    demo_service: DemoService = Depends(get_demo_service),
) -> list[DemoFarmerSummary]:
    return demo_service.list_summaries()


@router.get("/demo-farmers/{farmer_id}", response_model=DemoFarmerBundle)
def get_demo_farmer(
    farmer_id: str,
    demo_service: DemoService = Depends(get_demo_service),
) -> DemoFarmerBundle:
    return demo_service.get_bundle(farmer_id)
