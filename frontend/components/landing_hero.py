"""Welcome hero — clean brand-first composition."""

from __future__ import annotations

import streamlit as st

from frontend.utils.assets import hero_bg_data_uri
from frontend.utils.html_ui import render_html, render_inline_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual


def render_landing_hero() -> None:
    bg = hero_bg_data_uri()
    media = (
        f'<img class="fc-hero-img" src="{bg}" alt="" />'
        if bg
        else '<div class="fc-hero-fallback" aria-hidden="true"></div>'
    )

    render_inline_html(
        f"""
        <section class="fc-hero" aria-label="FarmCredit AI">
          <div class="fc-hero-media">{media}</div>
          <div class="fc-hero-veil" aria-hidden="true"></div>
          <div class="fc-hero-body">
            <h1 class="fc-hero-brand">FarmCredit AI</h1>
            <p class="fc-hero-sub">
              Crop-loan risk scores with plain-language explanations for Indian farmers
              and rural bank officers.
            </p>
          </div>
        </section>
        """
    )

    st.markdown('<div class="fc-hero-actions">', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("Try Demo Data", key="hero_try_demo", type="primary", use_container_width=True):
            go_farmer_demo()
            st.rerun()
    with c2:
        if st.button("Enter Your Own Details", key="hero_enter_own", use_container_width=True):
            go_farmer_manual()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    render_html(
        """
        <div class="fc-process-row">
          <div class="fc-process-step">
            <div class="fc-process-num">1</div>
            <div class="fc-process-title">Share details</div>
            <div class="fc-process-text">Use a demo farmer or enter farm and loan information.</div>
          </div>
          <div class="fc-process-step">
            <div class="fc-process-num">2</div>
            <div class="fc-process-title">Get assessed</div>
            <div class="fc-process-text">See the risk level and the factors that drove the score.</div>
          </div>
          <div class="fc-process-step">
            <div class="fc-process-num">3</div>
            <div class="fc-process-title">Act on guidance</div>
            <div class="fc-process-text">Read advice and download a PDF brief to review.</div>
          </div>
        </div>
        """
    )
