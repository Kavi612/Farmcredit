"""About page."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading


def render_about_view() -> None:
    section_heading(
        "About FarmCredit AI",
        "A portfolio demo of explainable crop-loan risk scoring.",
    )
    st.markdown(
        """
FarmCredit AI shows how machine learning and clear explanations can support
agri-credit conversations — for farmers reviewing their profile and for bank
officers screening applications.

It uses **synthetic demonstration data only**. It is not a production lending system.
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
            ("01", "For farmers", "See risk level, what drives it, and practical next steps."),
            ("02", "For bank officers", "Review demo applications with filters, charts, and decisions."),
            ("03", "How AI helps", "XGBoost scores risk, SHAP explains factors, advisory text guides action."),
        ]
    )
    render_html(f'<div class="fc-capability-grid">{items}</div>')
    st.caption("Demo only — synthetic data. Not for real lending decisions.")


def render_privacy_view() -> None:
    section_heading("Privacy", "How this demo handles information.")
    st.markdown(
        """
- Data stays on your local/backend host unless you deploy elsewhere.
- Demo profiles use synthetic sample data.
- Bank decisions are stored in the browser session only.
"""
    )
