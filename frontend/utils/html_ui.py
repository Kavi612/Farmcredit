"""Safe HTML rendering — prefer iframe HTML so nested cards/bars never leak as text."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from frontend.utils.theme import HTML_IFRAME_CSS


def _estimate_height(content: str) -> int:
    rows = content.count("fc-factor-row")
    cards = content.count("fc-card")
    metrics = content.count("fc-metric-card")
    two_col = content.count("fc-two-col")
    chips = content.count("fc-chip")
    header = 96 if "fc-result-header" in content else 0
    pills = 44 if "fc-pill-row" in content else 0
    title = 36 if "fc-card-title" in content else 0
    base = 24 + header + pills + title
    return max(
        72,
        base
        + rows * 36
        + cards * 12
        + metrics * 88
        + two_col * 160
        + min(chips, 20) * 4,
    )


def render_html(content: str, *, height: int | None = None) -> None:
    """Render multi-element HTML blocks (cards, factor bars, grids)."""
    h = height if height is not None else _estimate_height(content)
    wrapped = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{HTML_IFRAME_CSS}</style></head>"
        f"<body>{content}</body></html>"
    )
    components.html(wrapped, height=h, scrolling=False)


def render_inline_html(content: str) -> None:
    """Simple inline HTML only (brand mark, short pills). Prefer render_html for cards."""
    st.markdown(content, unsafe_allow_html=True)
