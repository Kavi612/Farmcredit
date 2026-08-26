"""Viewport width detection for responsive layout (render one nav, not two)."""

from __future__ import annotations

import streamlit as st

MOBILE_BREAKPOINT_PX = 768


def is_mobile_viewport() -> bool:
    """True when viewport looks mobile. Avoids hard crash if JS helper is missing."""
    try:
        from streamlit_javascript import st_javascript

        width = st_javascript("window.innerWidth")
        if width is None:
            return bool(st.session_state.get("_fc_is_mobile", False))
        mobile = int(width) <= MOBILE_BREAKPOINT_PX
        st.session_state._fc_is_mobile = mobile
        return mobile
    except Exception:  # noqa: BLE001
        return bool(st.session_state.get("_fc_is_mobile", False))
