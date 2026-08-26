"""Feature section — three clear capabilities, no clutter."""

from __future__ import annotations

import html

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading

FEATURES = [
    (
        "01",
        "Know your risk level",
        "Get a clear Low to Critical assessment from farm and loan details — without banking jargon.",
    ),
    (
        "02",
        "See what drives the score",
        "Understand which factors raised or lowered risk: rainfall, crop, debt, repayment history, and more.",
    ),
    (
        "03",
        "Act on practical guidance",
        "Receive plain-language advice and download a PDF brief you can review with a bank officer.",
    ),
]


def render_feature_cards() -> None:
    section_heading(
        "What you get",
        "One assessment. Clear risk. Explainable factors. Actionable guidance.",
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
        for num, title, text in FEATURES
    )
    render_html(f'<div class="fc-capability-grid">{items}</div>')
