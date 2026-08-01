"""Farmer assessment result section (shown inline on farmer view)."""

from __future__ import annotations

import html

import streamlit as st

from frontend.components.advisory_card import render_advisory_card
from frontend.components.risk_badge import render_risk_badge
from frontend.components.shap_panel import render_shap_panel
from frontend.utils.constants import STATE_NAMES
from frontend.utils.badges import risk_badge_html
from frontend.utils.theme import section_close, section_heading


def _recommendations_from_advisory(text: str | None, top_factors: list[dict]) -> list[str]:
    if text:
        lines = [ln.strip("•- ").strip() for ln in text.split("\n") if ln.strip()]
        if len(lines) >= 2:
            return lines[:4]
    recs = []
    for f in top_factors[:4]:
        hint = f.get("plain_hint")
        if hint:
            recs.append(str(hint))
    if not recs:
        recs = [
            "Review your repayment schedule and keep instalments on time.",
            "Compare loan size against expected crop income before borrowing more.",
            "Explore government crop insurance or subsidy schemes in your state.",
        ]
    return recs[:4]


def render_farmer_result(result: dict, *, inline: bool = True) -> None:
    section_heading(
        "Your credit risk assessment",
        "Risk score, key factors, advisory text, and downloadable report.",
    )

    name = result.get("display_name") or st.session_state.get("wizard_meta", {}).get(
        "farmer_name"
    ) or "Your profile"
    feats = result.get("features") or {}
    state = STATE_NAMES.get(feats.get("state", ""), feats.get("state", ""))
    crop = feats.get("crop_type", "")
    level = result.get("risk_level") or "Medium"
    score = float(result.get("risk_score") or 0.0)
    top = result.get("top_factors") or []

    st.markdown(
        f"""
        <div class="fc-result-hero">
          <div class="fc-result-left">
            <div class="fc-profile-name">{html.escape(str(name))}</div>
            <div class="fc-profile-meta">{html.escape(str(state))} · {html.escape(str(crop))}</div>
            <div style="margin-top:0.5rem;">{risk_badge_html(level)}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_risk_badge(level, score)
    render_shap_panel(top, result.get("protective_factors"))

    section_heading(
        "What should you consider next?",
        "Recommended next steps based on this profile.",
    )
    advisory = result.get("advisory") or {}
    advisory_text = advisory.get("advisory_text") or result.get("advisory_text")
    for rec in _recommendations_from_advisory(advisory_text, top):
        st.markdown(f"- :material/check_circle: {rec}")

    render_advisory_card(
        advisory_text,
        model_id=advisory.get("model_id"),
        cached=advisory.get("cached", result.get("cached")),
        latency_ms=advisory.get("latency_ms"),
        report=result.get("report"),
        farmer_label=result.get("farmer_id") or "custom",
        farmer_id=result.get("farmer_id"),
        features=feats if feats else None,
        use_demo_cache=bool(result.get("cached")),
    )
    section_close()
