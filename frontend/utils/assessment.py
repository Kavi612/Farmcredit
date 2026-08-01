"""Assessment helpers — demo load and custom assess."""

from __future__ import annotations

import streamlit as st

from frontend.utils import api


def load_demo_prefill(farmer_id: str) -> tuple[dict, str]:
    """Return (features, display_name) for form pre-fill."""
    bundle = api.get_demo_farmer(farmer_id)
    features = dict(bundle.get("features") or {})
    display_name = str(bundle.get("display_name") or farmer_id)
    return features, display_name


def load_demo_result(farmer_id: str) -> dict:
    bundle = api.get_demo_farmer(farmer_id)
    prediction = bundle.get("prediction") or {}
    explanation = bundle.get("explanation") or {}
    advisory = {
        "advisory_text": bundle.get("advisory_text"),
        "model_id": "demo_cache",
        "cached": True,
        "latency_ms": 0,
    }
    return {
        "farmer_id": bundle.get("id"),
        "display_name": bundle.get("display_name"),
        "features": bundle.get("features"),
        "risk_score": prediction.get("risk_score"),
        "risk_level": prediction.get("risk_level"),
        "top_factors": explanation.get("top_factors")
        or prediction.get("top_factors")
        or [],
        "protective_factors": explanation.get("protective_factors") or [],
        "advisory": advisory,
        "advisory_text": bundle.get("advisory_text"),
        "report": bundle.get("report"),
        "cached": True,
        "narrative": bundle.get("narrative"),
    }


def run_custom_assess(features: dict) -> dict:
    payload = api.assess(
        features=features,
        use_demo_cache=False,
        use_live_llm=False,
        include_advisory=True,
    )
    explanation = payload.get("explanation") or {}
    advisory = payload.get("advisory") or {}
    meta = st.session_state.get("wizard_meta", {})
    name = meta.get("farmer_name") or None
    return {
        "farmer_id": payload.get("farmer_id"),
        "display_name": name,
        "features": payload.get("features") or features,
        "risk_score": payload.get("risk_score"),
        "risk_level": payload.get("risk_level"),
        "top_factors": payload.get("top_factors")
        or explanation.get("top_factors")
        or [],
        "protective_factors": explanation.get("protective_factors") or [],
        "advisory": advisory,
        "advisory_text": advisory.get("advisory_text"),
        "report": payload.get("report"),
        "cached": bool(payload.get("cached")),
    }


def portfolio_row_to_result(app: dict) -> dict:
    return {
        "farmer_id": app.get("application_id"),
        "display_name": app.get("display_name"),
        "features": app.get("features"),
        "risk_score": app.get("risk_score"),
        "risk_level": app.get("risk_level"),
        "top_factors": app.get("top_factors") or [],
        "protective_factors": [],
        "advisory": {},
        "advisory_text": None,
        "report": None,
        "cached": True,
        "narrative": app.get("narrative"),
    }
