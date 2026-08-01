"""Demo farmer catalog and precomputed cache loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.app.core.exceptions import NotFoundError
from backend.app.models.schemas import (
    DemoFarmerBundle,
    DemoFarmerSummary,
    FarmerFeatures,
)


class DemoService:
    def __init__(self, farmers_path: Path, cache_dir: Path) -> None:
        self.farmers_path = farmers_path
        self.cache_dir = cache_dir
        self._farmers: list[dict[str, Any]] | None = None

    def _load_farmers(self) -> list[dict[str, Any]]:
        if self._farmers is None:
            self._farmers = json.loads(self.farmers_path.read_text(encoding="utf-8"))
        return self._farmers

    def list_summaries(self) -> list[DemoFarmerSummary]:
        summaries: list[DemoFarmerSummary] = []
        for farmer in self._load_farmers():
            cache = self.get_cache(farmer["id"], required=False)
            risk_level = None
            if cache and cache.get("prediction"):
                risk_level = cache["prediction"].get("risk_level")
            elif farmer.get("expected_risk_level"):
                risk_level = farmer["expected_risk_level"]
            summaries.append(
                DemoFarmerSummary(
                    id=farmer["id"],
                    display_name=farmer["display_name"],
                    state=farmer["features"]["state"],
                    crop_type=farmer["features"]["crop_type"],
                    risk_level=risk_level,
                    narrative=farmer["narrative"],
                )
            )
        return summaries

    def get_farmer_features(self, farmer_id: str) -> FarmerFeatures:
        fid = farmer_id.strip().upper()
        for farmer in self._load_farmers():
            if farmer["id"].upper() == fid:
                return FarmerFeatures(**farmer["features"])
        raise NotFoundError(f"Unknown demo farmer_id: {farmer_id}")

    def get_cache(self, farmer_id: str, required: bool = True) -> dict[str, Any] | None:
        fid = farmer_id.strip().upper()
        path = self.cache_dir / f"{fid}.json"
        if not path.exists():
            if required:
                raise NotFoundError(f"No demo cache for farmer_id: {farmer_id}")
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def get_bundle(self, farmer_id: str) -> DemoFarmerBundle:
        cache = self.get_cache(farmer_id, required=True)
        assert cache is not None
        # Ensure prediction has top_factors key for schema compatibility
        prediction = cache.get("prediction") or {}
        if "top_factors" not in prediction:
            prediction = {
                **prediction,
                "top_factors": (cache.get("explanation") or {}).get("top_factors", []),
            }
            cache = {**cache, "prediction": prediction}
        return DemoFarmerBundle(**cache)
