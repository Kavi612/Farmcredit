"""What is FarmCredit AI — brief intro on welcome page."""

from __future__ import annotations

import streamlit as st

from frontend.utils.theme import section_heading


def render_intro_section() -> None:
    section_heading(
        "What is FarmCredit AI?",
        "An AI-powered tool that turns farm and financial information into clear credit insights.",
    )
    st.markdown(
        """
FarmCredit AI is designed for **farmers** and **financial institutions** who need
credit-risk information explained in plain language — not spreadsheets or jargon.

Whether you explore sample profiles or enter your own details, you get a structured
view of risk level, influencing factors, and practical next steps.
"""
    )
