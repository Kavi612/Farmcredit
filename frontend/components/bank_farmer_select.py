"""Bank officer — farmer profile list with filters."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.constants import RISK_COLORS, STATE_NAMES
from frontend.utils.officer_portfolio import load_portfolio
from frontend.utils.badges import risk_badge_html
from frontend.utils.state import go_bank
from frontend.utils.theme import section_heading


def render_bank_farmer_list(*, demo_only: bool = False) -> str | None:
    title = (
        "Explore Demo Farmer Profiles"
        if demo_only
        else "Select a Farmer to Review"
    )
    subtitle = (
        "Choose one sample profile to review in the bank officer view."
        if demo_only
        else "Search and filter the portfolio, then review one farmer at a time."
    )
    section_heading(title, subtitle)

    try:
        _, apps = load_portfolio()
    except Exception as exc:
        st.error(str(exc))
        return None

    if demo_only:
        apps = [a for a in apps if a.get("is_demo")]

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        search = st.text_input("Search farmer", placeholder="Name or ID", key="bank_search").strip()
    with f2:
        risk_filter = st.multiselect(
            "Risk level",
            ["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"],
            key="bank_risk_f",
        )
    with f3:
        states = sorted({a["state"] for a in apps})
        state_filter = st.multiselect("State", states, default=states, key="bank_state_f")
    with f4:
        crops = sorted({a["crop_type"] for a in apps})
        crop_filter = st.multiselect("Crop", crops, default=crops, key="bank_crop_f")

    filtered = []
    for app in apps:
        if app["risk_level"] not in risk_filter:
            continue
        if app["state"] not in state_filter:
            continue
        if app["crop_type"] not in crop_filter:
            continue
        if search:
            q = search.lower()
            if q not in app["application_id"].lower() and q not in app["display_name"].lower():
                continue
        filtered.append(app)

    if not filtered:
        st.warning("No farmers match your filters.")
        return None

    selected_id = st.session_state.get("bank_selected_id")
    clicked: str | None = None
    cols = st.columns(3, gap="medium")
    for i, app in enumerate(filtered[:30]):
        with cols[i % 3]:
            state = STATE_NAMES.get(app["state"], app["state"])
            name = html.escape(app["display_name"])
            crop = html.escape(app["crop_type"])
            level = app["risk_level"]
            color = RISK_COLORS.get(level, "#546e7a")
            selected = app["application_id"] == selected_id
            card_style = (
                f"border:2px solid {color};box-shadow:0 2px 10px {color}33;"
                if selected
                else ""
            )
            app_id = app["application_id"]
            st.markdown(
                f'<div class="fc-profile-card" style="{card_style}">'
                f'<div class="fc-profile-name">{name}</div>'
                f'<div class="fc-profile-meta">{html.escape(state)} · {crop}</div>'
                f"{risk_badge_html(level)}"
                f'<div class="fc-profile-desc">{html.escape(str(app.get("narrative") or ""))}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Load {app_id}",
                key=f"bank_load_{app_id}",
                use_container_width=True,
                type="primary" if selected else "secondary",
                icon=":material/arrow_forward:",
            ):
                clicked = app_id
    return clicked


def render_bank_back_nav() -> None:
    if st.button("← Back to Bank Officer Home", key="bank_list_back"):
        go_bank()
        st.rerun()
