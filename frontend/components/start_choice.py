"""Get started — bottom CTA band on landing page."""

from __future__ import annotations

import streamlit as st

from frontend.utils.html_ui import render_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual


def render_start_choice() -> None:
    render_html(
        """
        <section class="fc-cta-band">
          <div class="fc-cta-band-inner">
            <h2 class="fc-cta-band-title">Ready to see your credit insight?</h2>
            <p class="fc-cta-band-sub">
              Explore a demo farmer profile in seconds, or enter your own farm and loan details
              for a personalized assessment.
            </p>
          </div>
        </section>
        """
    )
    st.markdown('<div class="fc-cta-actions">', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if st.button(
            "Explore Demo Profiles →",
            key="start_demo",
            type="primary",
            use_container_width=True,
        ):
            go_farmer_demo()
            st.rerun()
    with c2:
        if st.button(
            "Enter Your Details →",
            key="start_custom",
            use_container_width=True,
        ):
            go_farmer_manual()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
