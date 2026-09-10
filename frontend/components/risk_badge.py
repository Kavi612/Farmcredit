"""Large risk score display for results header."""

from __future__ import annotations

import html

from frontend.utils.badges import RISK_STYLES
from frontend.utils.formatting import risk_points


def risk_score_block_html(risk_level: str, risk_score: float) -> str:
    """HTML for the large score block (right side of results header)."""
    fg, _bg = RISK_STYLES.get(risk_level, ("#6b7280", "#f3f4f6"))
    points = risk_points(risk_score)
    return f"""
    <div class="fc-result-score-block">
      <p class="fc-result-score-label">Risk score</p>
      <p class="fc-result-score-value" style="color:{fg};">{points}</p>
      <p class="fc-result-score-sub">{html.escape(risk_level)} · {risk_score:.2f}</p>
    </div>
    """


def render_risk_badge(risk_level: str, risk_score: float) -> None:
    """Standalone score block (legacy callers). Prefer risk_score_block_html in header."""
    from frontend.utils.html_ui import render_inline_html

    render_inline_html(risk_score_block_html(risk_level, risk_score))
