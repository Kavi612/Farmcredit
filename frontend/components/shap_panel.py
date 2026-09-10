"""SHAP factor breakdown — diverging bars, risk vs protective lists."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading


def _merge_factors(
    all_factors: list[dict] | None,
    top_factors: list[dict] | None,
    protective_factors: list[dict] | None,
) -> list[dict]:
    by_feat: dict[str, dict] = {}
    for group in (all_factors or [], top_factors or [], protective_factors or []):
        for f in group:
            key = str(f.get("feature") or f.get("display_label") or "")
            if key and key not in by_feat:
                by_feat[key] = f
    return sorted(
        by_feat.values(),
        key=lambda x: abs(float(x.get("shap_value") or x.get("points") or 0)),
        reverse=True,
    )


def _bar_html(factor: dict, max_abs: float) -> str:
    pts = int(factor.get("points") or round(float(factor.get("shap_value") or 0) * 100))
    direction = factor.get("direction") or (
        "increases_risk" if pts >= 0 else "decreases_risk"
    )
    label = html.escape(str(factor.get("display_label") or factor.get("feature") or "Factor"))
    mag = abs(pts)
    # Half-track width (0–50%), bars grow from center
    width_pct = min(50.0, (mag / max_abs) * 50.0) if max_abs > 0 else 0.0
    is_up = direction == "increases_risk"
    color = "#b91c1c" if is_up else "#15803d"
    if is_up:
        # Center → right (risk-increasing)
        bar_style = f"left:50%;width:{width_pct:.1f}%;background:{color};"
    else:
        # Center → left (risk-reducing)
        left = 50.0 - width_pct
        bar_style = f"left:{left:.1f}%;width:{width_pct:.1f}%;background:{color};"
    sign = "+" if pts > 0 else ""
    return (
        f'<div class="fc-factor-row">'
        f'<div class="fc-factor-label">{label}</div>'
        f'<div class="fc-factor-track">'
        f'<div class="fc-factor-mid"></div>'
        f'<div class="fc-factor-bar" style="{bar_style}"></div>'
        f"</div>"
        f'<div class="fc-factor-pts" style="color:{color};">{sign}{pts}</div>'
        f"</div>"
    )


def render_shap_panel(
    top_factors: list[dict],
    protective_factors: list[dict] | None = None,
    *,
    all_factors: list[dict] | None = None,
    baseline: float | None = None,
) -> None:
    section_heading(
        "What is influencing this assessment?",
        "Factor contributions relative to the model baseline."
        + (f" Baseline {baseline:.2f}." if baseline is not None else ""),
    )

    factors = _merge_factors(all_factors, top_factors, protective_factors)
    if not factors:
        st.info("No explanation factors available for this result.")
        return

    max_abs = max(
        abs(int(f.get("points") or round(float(f.get("shap_value") or 0) * 100)))
        for f in factors
    )
    max_abs = max(max_abs, 1)

    default_n = 5
    show_all = st.checkbox(
        f"View all factors ({len(factors)})",
        value=False,
        key="fc_view_all_factors",
    )
    visible = factors if show_all else factors[:default_n]
    rows = "".join(_bar_html(f, max_abs) for f in visible)
    legend = (
        '<div class="fc-factor-legend">'
        '<span><span class="swatch down"></span> Lowers risk</span>'
        '<span><span class="swatch up"></span> Raises risk</span>'
        "</div>"
    )
    render_html(
        f'<div class="fc-card">'
        f'<div class="fc-card-title">Factor breakdown</div>'
        f"{legend}{rows}</div>",
        height=72 + len(visible) * 36,
    )

    risk_factors = [f for f in factors if f.get("direction") == "increases_risk"][:5]
    protect = protective_factors or [
        f for f in factors if f.get("direction") == "decreases_risk"
    ][:3]

    def _list_items(items: list[dict]) -> str:
        if not items:
            return '<li class="hint">None highlighted for this profile.</li>'
        out = []
        for f in items:
            label = html.escape(str(f.get("display_label") or f.get("feature")))
            hint = html.escape(str(f.get("plain_hint") or ""))
            out.append(
                f"<li><strong>{label}</strong><span class='hint'>{hint}</span></li>"
            )
        return "".join(out)

    render_html(
        f'<div class="fc-two-col">'
        f'<div class="fc-card" style="margin:0;">'
        f'<div class="fc-card-title">Risk-increasing factors</div>'
        f'<ul class="fc-factor-list">{_list_items(risk_factors)}</ul></div>'
        f'<div class="fc-card" style="margin:0;">'
        f'<div class="fc-card-title">Protective factors</div>'
        f'<ul class="fc-factor-list">{_list_items(protect)}</ul></div>'
        f"</div>",
        height=220,
    )
