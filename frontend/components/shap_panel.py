"""SHAP factor breakdown — diverging bars, risk vs protective lists."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.html_ui import render_inline_html
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
    return sorted(by_feat.values(), key=lambda x: abs(float(x.get("shap_value") or x.get("points") or 0)), reverse=True)


def _bar_html(factor: dict, max_abs: float) -> str:
    pts = int(factor.get("points") or round(float(factor.get("shap_value") or 0) * 100))
    direction = factor.get("direction") or ("increases_risk" if pts >= 0 else "decreases_risk")
    label = html.escape(str(factor.get("display_label") or factor.get("feature") or "Factor"))
    mag = abs(pts)
    width_pct = min(50.0, (mag / max_abs) * 50.0) if max_abs > 0 else 0.0
    cls = "up" if direction == "increases_risk" else "down"
    color = "#b91c1c" if cls == "up" else "#15803d"
    if cls == "up":
        bar = (
            f'<div class="fc-factor-bar {cls}" '
            f'style="left:50%;width:{width_pct:.1f}%;background:{color};"></div>'
        )
    else:
        bar = (
            f'<div class="fc-factor-bar {cls}" '
            f'style="right:50%;width:{width_pct:.1f}%;background:{color};"></div>'
        )
    sign = "+" if pts > 0 else ""
    return f"""
    <div class="fc-factor-row">
      <div class="fc-factor-label">{label}</div>
      <div class="fc-factor-track">
        <div class="fc-factor-mid"></div>
        {bar}
      </div>
      <div class="fc-factor-pts" style="color:{color};">{sign}{pts}</div>
    </div>
    """


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

    max_abs = max(abs(int(f.get("points") or round(float(f.get("shap_value") or 0) * 100))) for f in factors)
    max_abs = max(max_abs, 1)

    default_n = 5
    visible = factors[:default_n]
    rest = factors[default_n:]

    rows = "".join(_bar_html(f, max_abs) for f in visible)
    render_inline_html(f'<div class="fc-card"><div class="fc-card-title">Factor breakdown</div>{rows}</div>')

    if rest:
        with st.expander(f"View all factors ({len(factors)})", expanded=False):
            more = "".join(_bar_html(f, max_abs) for f in rest)
            render_inline_html(f'<div class="fc-card" style="margin:0;">{more}</div>')

    risk_factors = [f for f in factors if f.get("direction") == "increases_risk"][:5]
    protect = protective_factors or [f for f in factors if f.get("direction") == "decreases_risk"][:3]

    def _list_items(items: list[dict]) -> str:
        if not items:
            return '<li class="hint">None highlighted for this profile.</li>'
        out = []
        for f in items:
            label = html.escape(str(f.get("display_label") or f.get("feature")))
            hint = html.escape(str(f.get("plain_hint") or ""))
            out.append(f"<li><strong>{label}</strong><span class='hint'>{hint}</span></li>")
        return "".join(out)

    render_inline_html(
        f"""
        <div class="fc-two-col">
          <div class="fc-card" style="margin:0;">
            <div class="fc-card-title">Risk-increasing factors</div>
            <ul class="fc-factor-list">{_list_items(risk_factors)}</ul>
          </div>
          <div class="fc-card" style="margin:0;">
            <div class="fc-card-title">Protective factors</div>
            <ul class="fc-factor-list">{_list_items(protect)}</ul>
          </div>
        </div>
        """
    )
