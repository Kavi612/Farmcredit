"""Demo profile picker — Streamlit-native cards, no iframe grid."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.badges import risk_badge_html
from frontend.utils.constants import STATE_NAMES
from frontend.utils.formatting import shorten
from frontend.utils.theme import section_heading


def render_demo_profile_grid(demos: list[dict]) -> str | None:
    section_heading(
        "Choose a demo farmer",
        "Select a profile to pre-fill the assessment form.",
    )
    if not demos:
        st.warning("No demo profiles available right now.")
        return None

    clicked: str | None = None
    rows = [demos[i : i + 3] for i in range(0, min(len(demos), 5), 3)]
    for row in rows:
        cols = st.columns(len(row), gap="small")
        for col, demo in zip(cols, row):
            demo_id = str(demo.get("id", ""))
            level = demo.get("risk_level") or "Medium"
            state = html.escape(str(STATE_NAMES.get(demo.get("state", ""), demo.get("state", ""))))
            crop = html.escape(str(demo.get("crop_type", "")))
            name = html.escape(str(demo.get("display_name", "")))
            narrative = html.escape(shorten(str(demo.get("narrative", "")), 90))
            with col:
                st.markdown(
                    f"""
                    <div class="fc-profile-card">
                      <div class="fc-profile-name">{name}</div>
                      <div class="fc-profile-meta">{state} · {crop}</div>
                      {risk_badge_html(level)}
                      <div class="fc-profile-desc">{narrative}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Use {demo_id}", key=f"use_{demo_id}", use_container_width=True):
                    clicked = demo_id
    return clicked
