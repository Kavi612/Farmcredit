"""Welcome hero — full-bleed mockup layout."""

from __future__ import annotations

import streamlit as st

from frontend.utils.assets import hero_bg_data_uri
from frontend.utils.html_ui import render_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual


def render_landing_hero() -> None:
    bg = hero_bg_data_uri()
    media = (
        f'<img class="fc-hero-img" src="{bg}" alt="" />'
        if bg
        else '<div class="fc-hero-fallback" aria-hidden="true"></div>'
    )

    render_html(
        f"""
        <section class="fc-hero" aria-label="FarmCredit AI">
          <div class="fc-hero-media">{media}</div>
          <div class="fc-hero-veil" aria-hidden="true"></div>
          <div class="fc-hero-body">
            <span class="fc-hero-badge">Empowering Farmers</span>
            <h1 class="fc-hero-brand">FarmCredit AI</h1>
            <p class="fc-hero-sub">
              Crop-loan risk scores with plain-language explanations for Indian farmers
              and rural bank officers.
            </p>
            <div class="fc-hero-features">
              <span class="fc-hero-feat"><span class="dot"></span>Fair Assessment</span>
              <span class="fc-hero-feat"><span class="dot"></span>Better Decisions</span>
              <span class="fc-hero-feat"><span class="dot"></span>Stronger Rural Economy</span>
            </div>
          </div>
        </section>
        """,
        height=420,
    )

    st.markdown('<div class="fc-hero-actions-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if st.button(
            "Try Demo Data",
            key="hero_try_demo",
            type="primary",
            use_container_width=True,
            icon=":material/bar_chart:",
        ):
            go_farmer_demo()
            st.rerun()
    with c2:
        if st.button(
            "Enter Your Own Details",
            key="hero_enter_own",
            use_container_width=True,
            icon=":material/person:",
        ):
            go_farmer_manual()
            st.rerun()

    render_html(
        """
        <div class="fc-process-row">
          <div class="fc-process-step step-1">
            <div class="fc-process-badge">1</div>
            <div class="fc-process-body">
              <div class="fc-process-title">Share details</div>
              <div class="fc-process-text">Provide farmer and loan information.</div>
            </div>
            <div class="fc-process-chevron">›</div>
          </div>
          <div class="fc-process-step step-2">
            <div class="fc-process-badge">2</div>
            <div class="fc-process-body">
              <div class="fc-process-title">Get assessed</div>
              <div class="fc-process-text">AI analyzes risk and calculates score.</div>
            </div>
            <div class="fc-process-chevron">›</div>
          </div>
          <div class="fc-process-step step-3">
            <div class="fc-process-badge">3</div>
            <div class="fc-process-body">
              <div class="fc-process-title">Act on guidance</div>
              <div class="fc-process-text">View simple explanations &amp; next steps.</div>
            </div>
            <div class="fc-process-chevron">›</div>
          </div>
        </div>
        """,
        height=120,
    )
