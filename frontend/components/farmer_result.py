"""Farmer assessment result — card layout matching project theme."""

from __future__ import annotations

import html

import streamlit as st

from frontend.components.advisory_card import render_advisory_card
from frontend.components.risk_badge import risk_score_block_html
from frontend.components.shap_panel import render_shap_panel
from frontend.utils.assessment import advisory_source_label
from frontend.utils.constants import STATE_NAMES
from frontend.utils.formatting import format_inr
from frontend.utils.html_ui import render_html
from frontend.utils.theme import status_pill_html


_FEATURE_CHIP_ORDER = [
    ("state", "State"),
    ("district", "District"),
    ("crop_type", "Crop"),
    ("season", "Season"),
    ("land_size_ha", "Land (ha)"),
    ("soil_type", "Soil"),
    ("rainfall_mm", "Rainfall"),
    ("irrigation_type", "Irrigation"),
    ("loan_amount_inr", "Loan"),
    ("annual_income_inr", "Income"),
    ("existing_debt_inr", "Debt"),
    ("prior_loan_count", "Prior loans"),
    ("prior_default_flag", "Prior default"),
    ("repayment_score", "Repayment"),
]


def _chip_value(key: str, value) -> str:
    if key == "state":
        return STATE_NAMES.get(str(value), str(value))
    if key in {"loan_amount_inr", "annual_income_inr", "existing_debt_inr"}:
        return format_inr(value)
    if key == "prior_default_flag":
        return "Yes" if int(value or 0) == 1 else "No"
    if key == "rainfall_mm":
        return f"{float(value):.0f} mm"
    if key == "land_size_ha":
        return f"{float(value):.1f}"
    if key == "repayment_score":
        return f"{float(value):.0f}"
    return str(value)


def _affordability_html(features: dict) -> str:
    loan = float(features.get("loan_amount_inr") or 0)
    income = float(features.get("annual_income_inr") or 0)
    debt = float(features.get("existing_debt_inr") or 0)
    land = float(features.get("land_size_ha") or 0)

    loan_income = (loan / income) if income > 0 else None
    debt_income = (debt / income) if income > 0 else None
    loan_land = (loan / land) if land > 0 else None

    def fmt_ratio(v: float | None) -> str:
        return "—" if v is None else f"{v:.2f}×"

    def fmt_per_ha(v: float | None) -> str:
        return "—" if v is None else format_inr(v)

    return (
        '<div class="fc-metric-grid">'
        '<div class="fc-metric-card">'
        '<p class="fc-metric-label">Loan / income</p>'
        f'<p class="fc-metric-value">{fmt_ratio(loan_income)}</p>'
        '<p class="fc-metric-hint">Requested loan vs annual farm income</p>'
        "</div>"
        '<div class="fc-metric-card">'
        '<p class="fc-metric-label">Debt / income</p>'
        f'<p class="fc-metric-value">{fmt_ratio(debt_income)}</p>'
        '<p class="fc-metric-hint">Existing debt vs annual farm income</p>'
        "</div>"
        '<div class="fc-metric-card">'
        '<p class="fc-metric-label">Loan / land</p>'
        f'<p class="fc-metric-value">{fmt_per_ha(loan_land)}</p>'
        '<p class="fc-metric-hint">Loan amount per hectare</p>'
        "</div>"
        "</div>"
    )


def render_farmer_result(result: dict, *, inline: bool = True) -> None:
    name = (
        result.get("display_name")
        or st.session_state.get("wizard_meta", {}).get("farmer_name")
        or "Your profile"
    )
    feats = result.get("features") or {}
    if hasattr(feats, "model_dump"):
        feats = feats.model_dump()
    state = STATE_NAMES.get(feats.get("state", ""), feats.get("state", ""))
    crop = feats.get("crop_type", "")
    level = result.get("risk_level") or "Medium"
    score = float(result.get("risk_score") or 0.0)
    advisory = result.get("advisory") or {}
    source = advisory_source_label(advisory, cached=bool(result.get("cached")))

    initials = "".join(part[0] for part in str(name).split()[:2]).upper() or "FC"

    render_html(
        f'<div class="fc-result-header">'
        f'<div class="fc-result-identity">'
        f'<div class="fc-avatar">{html.escape(initials)}</div>'
        f"<div>"
        f'<p class="fc-result-name">{html.escape(str(name))}</p>'
        f'<p class="fc-result-meta">{html.escape(str(state))} · {html.escape(str(crop))}</p>'
        f"</div></div>"
        f"{risk_score_block_html(level, score)}"
        f"</div>",
        height=100,
    )

    pills = status_pill_html(str(level), kind=f"risk-{level}") + status_pill_html(
        source, kind="source"
    )
    render_html(f'<div class="fc-pill-row">{pills}</div>', height=48)

    chips = []
    for key, label in _FEATURE_CHIP_ORDER:
        if key not in feats:
            continue
        val = _chip_value(key, feats.get(key))
        chips.append(
            f'<span class="fc-chip"><strong>{html.escape(label)}:</strong>'
            f"{html.escape(val)}</span>"
        )
    if chips:
        render_html(
            f'<div class="fc-card"><div class="fc-card-title">Submitted inputs</div>'
            f'<div class="fc-chip-row">{"".join(chips)}</div></div>',
            height=120,
        )

    if feats:
        render_html(
            '<div class="fc-card"><div class="fc-card-title">Affordability</div>'
            + _affordability_html(feats)
            + "</div>",
            height=160,
        )

    render_shap_panel(
        result.get("top_factors") or [],
        result.get("protective_factors"),
        all_factors=result.get("all_factors"),
        baseline=result.get("baseline"),
    )

    render_advisory_card(
        advisory.get("advisory_text") or result.get("advisory_text"),
        model_id=advisory.get("model_id"),
        cached=advisory.get("cached", result.get("cached")),
        latency_ms=advisory.get("latency_ms"),
        report=result.get("report"),
        farmer_label=result.get("farmer_id") or "custom",
        farmer_id=result.get("farmer_id"),
        features=feats if feats else None,
        use_demo_cache=bool(result.get("cached")),
    )
