"""Risk badge HTML helpers."""

from __future__ import annotations

import html

RISK_STYLES = {
    "Low": ("#2e7d32", "#e8f5e9"),
    "Medium": ("#b8860b", "#fff8e1"),
    "High": ("#e65100", "#fff3e0"),
    "Critical": ("#c62828", "#ffebee"),
}


def risk_badge_html(level: str) -> str:
    fg, bg = RISK_STYLES.get(level, ("#546e7a", "#eceff1"))
    return (
        f'<span class="fc-risk-badge" style="color:{fg};background:{bg};">'
        f"{html.escape(level.upper())}</span>"
    )
