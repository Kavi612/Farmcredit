"""Welcome hero + start CTAs — matches the portfolio landing mockup."""

from __future__ import annotations

import streamlit as st

from frontend.utils.assets import hero_bg_data_uri
from frontend.utils.html_ui import render_inline_html
from frontend.utils.state import go_farmer_demo, go_farmer_manual

_ICON_SHIELD = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M12 3l7 3v5.5c0 4.2-2.9 7.3-7 9.2-4.1-1.9-7-5-7-9.2V6l7-3z" '
    'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
    "</svg>"
)
_ICON_CHART = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M4 19V5M4 19h16" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    '<path d="M8 15v-4M12 15V8M16 15v-6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    "</svg>"
)
_ICON_BOOK = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5V5.5z" '
    'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
    '<path d="M8 7h8M8 11h6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    "</svg>"
)
_ICON_LOCK = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.7"/>'
    '<path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    "</svg>"
)
_ICON_ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M7 17L17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
_ICON_USER = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="1.7"/>'
    '<path d="M5 19.5c1.6-3.2 4-4.8 7-4.8s5.4 1.6 7 4.8" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round"/>'
    "</svg>"
)


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
            <div class="fc-hero-trust">
              <span class="fc-hero-trust-dot" aria-hidden="true"></span>
              Trusted · Secure · Farmer First
            </div>
            <p class="fc-hero-kicker">Crop loan risk guidance</p>
            <h1 class="fc-hero-brand">FarmCredit AI</h1>
            <p class="fc-hero-sub">
              See your risk score, understand what drives it, and get practical next steps —
              built for Indian farmers and rural bank officers.
            </p>
            <div class="fc-hero-metrics">
              <div class="fc-hero-metric">
                <div class="fc-hero-metric-icon">{_ICON_SHIELD}</div>
                <div>
                  <div class="fc-hero-metric-title">Risk Assessment</div>
                  <div class="fc-hero-metric-sub">AI-powered scores</div>
                </div>
              </div>
              <div class="fc-hero-metric">
                <div class="fc-hero-metric-icon">{_ICON_CHART}</div>
                <div>
                  <div class="fc-hero-metric-title">Insights</div>
                  <div class="fc-hero-metric-sub">Clear &amp; actionable</div>
                </div>
              </div>
              <div class="fc-hero-metric">
                <div class="fc-hero-metric-icon">{_ICON_BOOK}</div>
                <div>
                  <div class="fc-hero-metric-title">Guidance</div>
                  <div class="fc-hero-metric-sub">Step-by-step</div>
                </div>
              </div>
              <div class="fc-hero-metric">
                <div class="fc-hero-metric-icon">{_ICON_LOCK}</div>
                <div>
                  <div class="fc-hero-metric-title">Secure</div>
                  <div class="fc-hero-metric-sub">Demo-safe design</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        """
    )

    st.markdown(
        '<div class="fc-start-row-marker" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        render_inline_html(
            f"""
            <div class="fc-start-card fc-start-card-primary">
              <div class="fc-start-card-icon">{_ICON_ARROW}</div>
              <div class="fc-start-card-title">Try Demo Data</div>
              <div class="fc-start-card-sub">Explore with sample farmer profiles</div>
            </div>
            """
        )
        if st.button(
            "Open demo →",
            key="hero_try_demo",
            type="primary",
            use_container_width=True,
        ):
            go_farmer_demo()
            st.rerun()
    with c2:
        render_inline_html(
            f"""
            <div class="fc-start-card fc-start-card-secondary">
              <div class="fc-start-card-icon">{_ICON_USER}</div>
              <div class="fc-start-card-title">Enter Your Own Details</div>
              <div class="fc-start-card-sub">Get your personalized risk assessment</div>
            </div>
            """
        )
        if st.button(
            "Start assessment →",
            key="hero_enter_own",
            use_container_width=True,
        ):
            go_farmer_manual()
            st.rerun()
