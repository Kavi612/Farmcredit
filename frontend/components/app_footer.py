"""Site footer with About and Privacy links."""

from __future__ import annotations

import streamlit as st


def render_app_footer() -> None:
    st.markdown('<hr class="fc-footer-divider">', unsafe_allow_html=True)
    left, right = st.columns([2, 1], vertical_alignment="center")
    with left:
        st.markdown(
            """
            <div class="fc-footer-brand">
              🌱 <strong>FarmCredit AI</strong><br>
              <span class="fc-footer-copy">© 2026 FarmCredit AI. All rights reserved.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("About", key="footer_about", use_container_width=True):
                st.session_state.app_view = "about"
                st.rerun()
        with c2:
            if st.button("Privacy", key="footer_privacy", use_container_width=True):
                st.session_state.app_view = "privacy"
                st.rerun()
