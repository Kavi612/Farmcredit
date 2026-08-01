"""Feature cards — landing page."""

from __future__ import annotations

import html

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading

FEATURES = [
    ("📊", "Understand Your Credit Risk",
     "Get a clear view of your credit-risk level without complicated financial terminology."),
    ("📈", "Know What Drives Your Risk",
     "See how income, repayment history, debt, and farming conditions influence your assessment."),
    ("💡", "Get Practical Guidance",
     "Receive useful next steps based on your financial and farming situation."),
]


def render_feature_cards() -> None:
    section_heading(
        "What can FarmCredit AI help you with?",
        "Turn your farm and financial information into simple, understandable credit insights.",
    )
    cards = "".join(
        f"""
        <div class="fc-card fc-feature-card">
          <div class="fc-card-icon-wrap">{icon}</div>
          <div class="fc-card-title">{html.escape(title)}</div>
          <div class="fc-card-text">{html.escape(text)}</div>
        </div>
        """
        for icon, title, text in FEATURES
    )
    render_html(f'<div class="fc-card-grid fc-card-grid-3">{cards}</div>')
