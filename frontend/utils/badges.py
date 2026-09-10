"""Risk badge HTML helpers — risk palette only."""

from __future__ import annotations

import html

RISK_STYLES = {
    "Low": ("#15803d", "#dcfce7"),
    "Medium": ("#a16207", "#fef3c7"),
    "High": ("#c2410c", "#ffedd5"),
    "Critical": ("#b91c1c", "#fee2e2"),
}


def risk_badge_html(level: str) -> str:
    fg, bg = RISK_STYLES.get(level, ("#6b7280", "#f3f4f6"))
    return (
        f'<span class="fc-risk-badge" style="color:{fg};background:{bg};">'
        f"{html.escape(level)}</span>"
    )
