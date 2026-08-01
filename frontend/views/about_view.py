"""About and privacy pages."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.theme import section_heading


def render_about_view() -> None:
    section_heading(
        "About FarmCredit AI",
        "AI-powered credit guidance for farmers and financial institutions.",
    )
    st.markdown(
        """
FarmCredit AI was created to make agricultural credit-risk information **easier to
understand** — for farmers planning their next loan and for institutions reviewing profiles.

It combines machine-learning risk scoring with clear explanations and practical guidance.
"""
    )
    cols = st.columns(3, gap="medium")
    cards = [
        ("person", "For Farmers",
         "Understand your risk level, what drives it, and practical steps you can take."),
        ("account_balance", "For Banks",
         "Review one farmer at a time with structured risk factors and lending considerations."),
        ("psychology", "How AI Helps",
         "XGBoost estimates risk, SHAP explains factors, and optional AI generates guidance."),
    ]
    for col, (icon, title, text) in zip(cols, cards):
        with col:
            st.markdown(f":material/{icon}: **{title}**")
            st.markdown(
                f'<div class="fc-card"><div class="fc-card-text">{html.escape(text)}</div></div>',
                unsafe_allow_html=True,
            )
    st.caption(
        "Demo only — synthetic data. Not for real lending decisions."
    )


def render_privacy_view() -> None:
    section_heading("Privacy Policy", "How this demo handles your information.")
    st.markdown(
        """
- Data stays on your **local** backend unless you deploy elsewhere.
- Demo profiles use synthetic sample data.
- Bank review sessions are stored in your browser only.

This is a demonstration notice — not a production legal document.
"""
    )
