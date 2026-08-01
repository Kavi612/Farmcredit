"""FarmCredit AI — single app, three top-level views."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from frontend.components.site_footer import render_site_footer
from frontend.components.site_header import render_site_header
from frontend.utils.state import init_app_state
from frontend.utils.theme import apply_theme
from frontend.views.about_view import render_about_view
from frontend.views.bank_view import render_bank_view
from frontend.views.farmer_view import render_farmer_view
from frontend.views.welcome_view import render_welcome_page

st.set_page_config(
    page_title="FarmCredit AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
init_app_state()


def main() -> None:
    render_site_header()

    view = st.session_state.get("current_view", "welcome")
    if view == "farmer":
        render_farmer_view()
    elif view == "bank":
        render_bank_view()
    elif view == "about":
        render_about_view()
    else:
        render_welcome_page()

    render_site_footer()


if __name__ == "__main__":
    main()
