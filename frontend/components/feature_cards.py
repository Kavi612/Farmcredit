"""Feature cards — landing page."""

from __future__ import annotations

import html

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading

# SVG icons (no emoji) — matching mockup energy, FarmCredit accuracy
_ICON_GAUGE = """
<svg class="fc-icon-svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M12 3a9 9 0 1 0 9 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M12 12l5-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <circle cx="12" cy="12" r="1.6" fill="currentColor"/>
</svg>
"""

_ICON_FACTORS = """
<svg class="fc-icon-svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <rect x="4" y="3.5" width="16" height="17" rx="2.2" stroke="currentColor" stroke-width="1.8"/>
  <path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

_ICON_GUIDE = """
<svg class="fc-icon-svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M9 18h6M10 21h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M12 3a6 6 0 0 1 3.6 10.8c-.7.55-1.1 1.2-1.25 2.2H9.65c-.15-1-.55-1.65-1.25-2.2A6 6 0 0 1 12 3z"
        stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
</svg>
"""

_ICON_SHIELD = """
<svg class="fc-icon-svg" viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M12 3l7 3v5.5c0 4.4-2.9 7.5-7 9.5-4.1-2-7-5.1-7-9.5V6l7-3z"
        stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M9.5 12.2l1.8 1.8 3.5-3.8" stroke="currentColor" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

FEATURES = [
    (
        _ICON_GAUGE,
        "Credit Risk Check",
        "See a clear Low to Critical risk level from your farm and loan details — without banking jargon.",
    ),
    (
        _ICON_FACTORS,
        "Understand Factors",
        "Learn which inputs raised or lowered your score — rainfall, crop, debt, repayment history, and more.",
    ),
    (
        _ICON_GUIDE,
        "Personalized Guidance",
        "Get practical next steps and indicative scheme pointers shaped around your assessment result.",
    ),
    (
        _ICON_SHIELD,
        "Better Loan Conversations",
        "Download a PDF brief you can review with a bank officer — transparent, explainable, demo-ready.",
    ),
]


def render_feature_cards() -> None:
    section_heading(
        "What can FarmCredit AI help you with?",
        "Turn farm and financial information into simple, understandable credit insights.",
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
    render_html(
        f'<div class="fc-feature-section"><div class="fc-card-grid fc-card-grid-4">{cards}</div></div>'
    )
