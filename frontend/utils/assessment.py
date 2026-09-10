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


def _enrich_explanation(features: dict | None, explanation: dict) -> dict:
    """Prefer full factor list via existing /explain-risk (top_k=14). No API contract change."""
    baseline = explanation.get("baseline")
    all_factors = list(explanation.get("top_factors") or [])
    protective = list(explanation.get("protective_factors") or [])

    if features:
        try:
            full = api.explain_risk(features=features, top_k=14)
            baseline = full.get("baseline", baseline)
            all_factors = list(full.get("top_factors") or all_factors)
            protective = list(full.get("protective_factors") or protective)
        except api.ApiError:
            pass

    return {
        "baseline": baseline,
        "all_factors": all_factors,
        "protective_factors": protective,
        "top_factors": all_factors[:5] if all_factors else [],
    }


def load_demo_result(farmer_id: str) -> dict:
    bundle = api.get_demo_farmer(farmer_id)
    prediction = bundle.get("prediction") or {}
    explanation = bundle.get("explanation") or {}
    features = bundle.get("features") or {}
    enriched = _enrich_explanation(features if isinstance(features, dict) else None, explanation)
    advisory = {
        "advisory_text": bundle.get("advisory_text"),
        "model_id": "demo_cache",
        "cached": True,
        "latency_ms": 0,
        "degraded": False,
    }
    return {
        "farmer_id": bundle.get("id"),
        "display_name": bundle.get("display_name"),
        "features": features,
        "risk_score": prediction.get("risk_score"),
        "risk_level": prediction.get("risk_level"),
        "baseline": enriched["baseline"],
        "top_factors": enriched["top_factors"],
        "all_factors": enriched["all_factors"],
        "protective_factors": enriched["protective_factors"],
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
    feats = payload.get("features") or features
    if hasattr(feats, "model_dump"):
        feats = feats.model_dump()
    enriched = _enrich_explanation(feats if isinstance(feats, dict) else features, explanation)
    meta = st.session_state.get("wizard_meta", {})
    name = meta.get("farmer_name") or None
    return {
        "farmer_id": payload.get("farmer_id"),
        "display_name": name,
        "features": feats,
        "risk_score": payload.get("risk_score"),
        "risk_level": payload.get("risk_level"),
        "baseline": enriched["baseline"],
        "top_factors": enriched["top_factors"],
        "all_factors": enriched["all_factors"],
        "protective_factors": enriched["protective_factors"],
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
        "baseline": None,
        "top_factors": app.get("top_factors") or [],
        "all_factors": app.get("top_factors") or [],
        "protective_factors": [],
        "advisory": {},
        "advisory_text": None,
        "report": None,
        "cached": True,
        "narrative": app.get("narrative"),
    }


def advisory_source_label(advisory: dict | None, *, cached: bool = False) -> str:
    adv = advisory or {}
    model_id = str(adv.get("model_id") or "")
    degraded = bool(adv.get("degraded"))
    is_cached = bool(adv.get("cached", cached))
    if is_cached or model_id == "demo_cache":
        return "Cached demo"
    if degraded or model_id in {"template", "template_fallback"}:
        return "Template advisory"
    if model_id:
        return "Live model"
    return "Template advisory"
