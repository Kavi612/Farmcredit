"""Welcome page hero — open layout with brand icon, no card wrapper."""

from __future__ import annotations

import streamlit as st

from frontend.utils.html_ui import render_inline_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual
from frontend.utils.theme import brand_icon_html


def render_landing_hero() -> None:
    render_inline_html(
        f"""
        <section class="fc-hero-open">
          <div class="fc-hero-grid">
            <div class="fc-hero-left">
              <span class="fc-hero-badge">AI-POWERED CREDIT GUIDANCE</span>
              <h1 class="fc-hero-title">Welcome to FarmCredit AI</h1>
              <p class="fc-hero-sub">
                Understand your credit risk, discover what affects your financial profile,
                and get practical guidance for your next financial step.
              </p>
              <div class="fc-hero-bullets">
                <span>Simple insights</span>
                <span>Clear explanations</span>
                <span>Better decisions</span>
              </div>
            </div>
            <div class="fc-hero-right fc-hero-icon-col">
              {brand_icon_html(size="hero")}
            </div>
          </div>
        </section>
        """
    )

    st.markdown(
        '<div class="fc-hero-cta-bar"><p class="fc-hero-cta-label">Get started</p></div>',
        unsafe_allow_html=True,
    )
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
