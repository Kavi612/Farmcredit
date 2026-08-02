"""Welcome hero — full-bleed landscape background, brand-first composition."""

from __future__ import annotations

import streamlit as st

from frontend.utils.assets import hero_bg_data_uri
from frontend.utils.html_ui import render_inline_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual


def render_landing_hero() -> None:
    bg = hero_bg_data_uri()
    if bg:
        st.markdown(
            f"<style>.fc-hero-bleed-bg{{background-image:url('{bg}');}}</style>",
            unsafe_allow_html=True,
        )

    render_inline_html(
        """
        <section class="fc-hero-bleed" aria-label="FarmCredit AI welcome">
          <div class="fc-hero-bleed-bg"></div>
          <div class="fc-hero-bleed-veil" aria-hidden="true"></div>
          <div class="fc-hero-bleed-content">
            <h1 class="fc-hero-brand">FarmCredit AI</h1>
            <p class="fc-hero-title">Understand crop loan risk before you apply</p>
            <p class="fc-hero-sub">
              Clear risk scores, plain-language explanations, and practical guidance
              for farmers and rural bank officers.
            </p>
          </div>
        </section>
        """
    )

    st.markdown('<div class="fc-hero-cta-bar"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button(
            "Try Demo Data →",
            key="hero_try_demo",
            type="primary",
            use_container_width=True,
        ):
            go_farmer_demo()
            st.rerun()
    with c2:
        if st.button(
            "Enter Your Own Details",
            key="hero_enter_own",
            use_container_width=True,
        ):
            go_farmer_manual()
            st.rerun()
