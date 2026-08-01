"""Safe HTML rendering — st.html for blocks, markdown for simple/icon HTML."""

from __future__ import annotations

import streamlit as st

from frontend.utils.theme import HTML_IFRAME_CSS


def render_html(content: str) -> None:
    """Render multi-element HTML blocks (cards, grids, steps)."""
    wrapped = f"<style>{HTML_IFRAME_CSS}</style>{content}"
    if hasattr(st, "html"):
        st.html(wrapped)
    else:
        st.markdown(wrapped, unsafe_allow_html=True)


def render_inline_html(content: str) -> None:
    """Render simple HTML in the main page (icons, brand mark)."""
    st.markdown(content, unsafe_allow_html=True)
