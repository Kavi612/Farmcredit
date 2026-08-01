"""How it works — 3-step explainer."""

from __future__ import annotations

import html

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading

STEPS = [
    ("01", "Provide Details",
     "Use demo data or enter your own farm and financial details."),
    ("02", "AI Analyzes",
     "FarmCredit AI evaluates your profile and identifies important credit-risk factors."),
    ("03", "Understand Result",
     "See your risk level, key factors, and practical next steps."),
]


def render_how_it_works() -> None:
    section_heading("How FarmCredit AI works", "Three simple steps from information to insight.")
    steps = "".join(
        f"""
        <div class="fc-step-card">
          <div class="fc-card-num">{num}</div>
          <div class="fc-card-title">{html.escape(title)}</div>
          <div class="fc-card-text">{html.escape(text)}</div>
        </div>
        """
        for num, title, text in STEPS
    )
    render_html(f'<div class="fc-steps-row">{steps}</div>')
