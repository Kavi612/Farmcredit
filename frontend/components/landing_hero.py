"""Welcome hero — one clear composition: photo, brand, headline, CTAs."""

from __future__ import annotations

import streamlit as st

from frontend.utils.assets import hero_bg_data_uri
from frontend.utils.html_ui import render_inline_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual


def render_landing_hero() -> None:
    bg = hero_bg_data_uri()
    media = (
        f'<img class="fc-hero-bleed-img" src="{bg}" alt="" />'
        if bg
        else '<div class="fc-hero-bleed-fallback" aria-hidden="true"></div>'
    )

    render_inline_html(
        f"""
        <section class="fc-hero-bleed" aria-label="FarmCredit AI welcome">
          <div class="fc-hero-bleed-media">{media}</div>
          <div class="fc-hero-bleed-veil" aria-hidden="true"></div>
          <div class="fc-hero-bleed-content">
            <p class="fc-hero-kicker">Crop loan risk guidance</p>
            <h1 class="fc-hero-brand">FarmCredit AI</h1>
            <p class="fc-hero-sub">
              See your risk score, understand what drives it, and get practical next steps —
              built for Indian farmers and rural bank officers.
            </p>
          </div>
        </section>
        """
    )

    st.markdown('<div class="fc-hero-cta-wrap">', unsafe_allow_html=True)
    c1, c2, _ = st.columns([1.15, 1.15, 0.9], gap="small")
    with c1:
        if st.button(
            "Try Demo Data",
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
    st.markdown("</div>", unsafe_allow_html=True)
