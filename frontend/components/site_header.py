"""Site header — mockup top bar + full-width pill nav."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from frontend.utils.html_ui import render_html
from frontend.utils.state import go_about, go_bank, go_farmer, go_welcome
from frontend.utils.theme import brand_html
from frontend.utils.viewport import is_mobile_viewport

NavLink = tuple[str, str, Callable[[], None]]


def _run(handler: Callable[[], None]) -> None:
    handler()
    st.rerun()


def _render_nav(
    *,
    links: list[NavLink],
    primary: tuple[str, str, Callable[[], None], bool],
    highlight_first: bool = False,
) -> None:
    st.markdown('<div class="fc-nav-row-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    if highlight_first:
        st.markdown('<div class="fc-nav-active-marker" aria-hidden="true"></div>', unsafe_allow_html=True)

    plabel, pkey, phandler, pprimary = primary
    mobile = is_mobile_viewport()

    if mobile:
        menu_col, bank_col = st.columns([0.55, 3.35], gap="small")
        with menu_col:
            with st.popover("☰", use_container_width=True):
                for label, key, handler in links:
                    if st.button(label, key=key, use_container_width=True):
                        _run(handler)
        with bank_col:
            if st.button(
                plabel,
                key=pkey,
                type="primary" if pprimary else "secondary",
                use_container_width=True,
                icon=":material/account_balance:",
            ):
                _run(phandler)
        return

    if not links:
        if st.button(
            plabel,
            key=pkey,
            type="primary" if pprimary else "secondary",
            use_container_width=True,
        ):
            _run(phandler)
        return

    weights = [1.0] * len(links) + [1.2]
    cols = st.columns(weights, gap="medium")
    icons = {
        "Home": ":material/home:",
        "About": ":material/info:",
        "Farmer": ":material/agriculture:",
    }
    for idx, (label, key, handler) in enumerate(links):
        with cols[idx]:
            if st.button(
                label,
                key=key,
                use_container_width=True,
                icon=icons.get(label),
            ):
                _run(handler)
    with cols[-1]:
        if st.button(
            plabel,
            key=pkey,
            type="primary" if pprimary else "secondary",
            use_container_width=True,
            icon=":material/account_balance:" if "Bank" in plabel else ":material/agriculture:",
        ):
            _run(phandler)


def render_site_header() -> None:
    view = st.session_state.get("current_view", "welcome")
    subtitles = {
        "welcome": "Credit Guidance for Farmers",
        "about": "About this project",
        "bank": "Bank Officer Dashboard",
        "farmer": "Farmer Assessment",
    }
    subtitle = subtitles.get(view, "Credit Guidance for Farmers")

    render_html(brand_html(subtitle=subtitle, shell=True), height=84)

    if view == "welcome":
        _render_nav(
            links=[
                ("Home", "nav_home", go_welcome),
                ("About", "nav_about", go_about),
            ],
            primary=("Bank Officer", "nav_bank", go_bank, True),
            highlight_first=True,
        )
    elif view == "about":
        _render_nav(
            links=[("Home", "nav_about_home", go_welcome)],
            primary=("Bank Officer", "nav_about_bank", go_bank, True),
        )
    elif view == "bank":
        _render_nav(
            links=[
                ("Home", "nav_bank_menu_home", go_welcome),
                ("About", "nav_bank_menu_about", go_about),
                ("Farmer", "nav_bank_menu_farmer", go_farmer),
            ],
            primary=("Farmer View", "nav_bank_farmer", go_farmer, False),
        )
    else:
        _render_nav(
            links=[
                ("Home", "nav_farmer_home", go_welcome),
                ("About", "nav_farmer_about", go_about),
            ],
            primary=("Bank Officer", "nav_farmer_bank", go_bank, True),
        )
