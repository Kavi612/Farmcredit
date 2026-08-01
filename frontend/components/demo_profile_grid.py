"""Demo profile cards."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.constants import RISK_COLORS, STATE_NAMES
from frontend.utils.badges import risk_badge_html
from frontend.utils.formatting import shorten
from frontend.utils.html_ui import render_html
from frontend.utils.theme import crop_emoji, section_heading


def render_demo_profile_grid(demos: list[dict]) -> str | None:
    section_heading(
        "Choose a demo farmer",
        "Pick a profile to pre-fill the form with that farmer's actual data.",
    )
    if not demos:
        st.warning("No demo profiles available right now.")
        return None

    selected_id = st.session_state.get("selected_demo_id")
    cards_html = []
    for demo in demos[:5]:
        level = demo.get("risk_level") or "Medium"
        color = RISK_COLORS.get(level, "#546e7a")
        selected = demo.get("id") == selected_id
        extra = f"border-color:{color};box-shadow:0 6px 20px {color}28;" if selected else ""
        state = STATE_NAMES.get(demo.get("state", ""), demo.get("state", ""))
        crop = demo.get("crop_type", "")
        demo_id = demo.get("id", "")
        name = html.escape(str(demo.get("display_name", "")))
        narrative = html.escape(shorten(str(demo.get("narrative", "")), 90))
        cards_html.append(
            f'<div class="fc-profile-card" style="{extra}">'
            f'<div class="fc-profile-crop">{crop_emoji(crop)}</div>'
            f'<div class="fc-profile-name">{name}</div>'
            f'<div class="fc-profile-meta">{html.escape(state)} · {html.escape(crop)}</div>'
            f"{risk_badge_html(level)}"
            f'<div class="fc-profile-desc">{narrative}</div>'
            f"</div>"
        )

    render_html(f'<div class="fc-card-grid fc-card-grid-5">{"".join(cards_html)}</div>')

    clicked: str | None = None
    cols = st.columns(min(len(demos), 5), gap="small")
    for i, demo in enumerate(demos[:5]):
        demo_id = demo.get("id", "")
        selected = demo_id == selected_id
        with cols[i]:
            if st.button(
                f"Use {demo_id} →",
                key=f"use_{demo_id}",
                use_container_width=True,
                type="primary" if selected else "secondary",
            ):
                clicked = demo_id
    return clicked
