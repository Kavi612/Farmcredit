"""Viewport width detection for responsive layout (render one nav, not two)."""

from __future__ import annotations

import streamlit as st
from streamlit_javascript import st_javascript

MOBILE_BREAKPOINT_PX = 768


def is_mobile_viewport() -> bool:
    """True when innerWidth <= 768px. Uses JS once per rerun — only one nav layout is rendered."""
    width = st_javascript("window.innerWidth")
    if width is None:
        return bool(st.session_state.get("_fc_is_mobile", False))
    mobile = int(width) <= MOBILE_BREAKPOINT_PX
    st.session_state._fc_is_mobile = mobile
    return mobile
