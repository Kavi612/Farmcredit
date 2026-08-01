"""Color-coded risk score display."""

from __future__ import annotations

import streamlit as st

from frontend.utils.constants import RISK_BG, RISK_COLORS
from frontend.utils.formatting import risk_points


def render_risk_badge(risk_level: str, risk_score: float) -> None:
    color = RISK_COLORS.get(risk_level, "#455a64")
    bg = RISK_BG.get(risk_level, "#eceff1")
    points = risk_points(risk_score)

    st.markdown(
        f"""
        <div style="background:{bg};border:1px solid {color}44;border-left:5px solid {color};
            border-radius:18px;padding:1.25rem 1.4rem;margin:0.75rem 0 1.25rem 0;
            box-shadow:0 2px 12px rgba(15,23,42,0.05);">
          <div style="font-size:0.72rem;font-weight:800;color:#64748b;
              letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">
            Credit risk level
          </div>
          <div style="display:flex;align-items:baseline;gap:0.85rem;flex-wrap:wrap;">
            <span style="font-size:2.1rem;font-weight:800;color:{color};letter-spacing:-0.02em;">{risk_level}</span>
            <span style="font-size:1.2rem;font-weight:700;color:#0f172a;">{points} / 100</span>
            <span style="font-size:0.88rem;color:#94a3b8;">score {risk_score:.2f}</span>
          </div>
          <div style="margin-top:1rem;height:12px;background:#e2e8f0;border-radius:999px;overflow:hidden;">
            <div style="width:{min(points, 100)}%;height:100%;background:linear-gradient(90deg,{color},{color}cc);border-radius:999px;"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
