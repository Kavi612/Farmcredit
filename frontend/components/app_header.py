"""Top navigation header — logo and view switcher."""

from __future__ import annotations

import streamlit as st


def render_app_header() -> None:
    view = st.session_state.get("app_view", "farmer")
    left, right = st.columns([4, 1], vertical_alignment="center")

    with left:
        st.markdown(
            """
            <div class="fc-app-logo">
              <span class="fc-app-logo-icon">🌱</span>
              <span class="fc-app-logo-text">FarmCredit AI</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        if view in ("farmer", "bank"):
            label = (
                "Switch to Bank"
                if view == "farmer"
                else "Switch to Farmer"
            )
            if st.button(
                label,
                key="header_view_switch",
                use_container_width=True,
                icon=":material/swap_horiz:",
            ):
                st.session_state.app_view = "bank" if view == "farmer" else "farmer"
                st.rerun()
        else:
            if st.button(
                "Back to Home",
                key="header_back_home",
                use_container_width=True,
                icon=":material/home:",
            ):
                st.session_state.app_view = "farmer"
                st.rerun()

    st.markdown('<hr class="fc-header-divider">', unsafe_allow_html=True)
