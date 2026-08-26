"""About page — clean project overview."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading


def render_about_view() -> None:
    section_heading(
        "About FarmCredit AI",
        "A portfolio demonstration of explainable agri-credit risk scoring.",
    )
    st.markdown(
        """
FarmCredit AI helps farmers and rural bank officers understand crop-loan default risk
before a lending conversation gets locked in. It combines an XGBoost risk model,
SHAP explanations, and practical advisory text — using **synthetic** demonstration data only.
"""
    )
    items = "".join(
        f"""
        <div class="fc-capability">
          <div class="fc-capability-num">{num}</div>
          <div>
            <div class="fc-capability-title">{html.escape(title)}</div>
            <div class="fc-capability-text">{html.escape(text)}</div>
          </div>
        </div>
        """
        for num, title, text in [
            ("01", "For farmers", "See your risk level, what drives it, and practical next steps."),
            ("02", "For bank officers", "Review demo applications with filters, charts, and approve/flag decisions."),
            ("03", "How AI helps", "XGBoost scores risk, SHAP explains factors, and advisory text turns results into guidance."),
        ]
    )
    render_html(f'<div class="fc-capability-grid">{items}</div>')
    st.caption("Demo only — synthetic data. Not for real lending decisions.")


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
