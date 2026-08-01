"""Call-to-action block before the custom farmer form."""

from __future__ import annotations

import streamlit as st


def render_enter_details_cta() -> bool:
    """Render CTA; returns True if user clicked Enter Details."""
    with st.container(border=True):
        icon_col, text_col, btn_col = st.columns(
            [0.4, 3, 1.2], vertical_alignment="center"
        )
        with icon_col:
            st.markdown(
                '<p style="font-size:2rem;margin:0;text-align:center;">📝</p>',
                unsafe_allow_html=True,
            )
        with text_col:
            st.markdown(
                "**Or enter your own farm details**  \n"
                "Get your credit risk score and personalized guidance."
            )
        with btn_col:
            clicked = st.button(
                "Enter Details",
                key="enter_details_btn",
                use_container_width=True,
                type="primary",
                icon=":material/arrow_forward:",
            )
    return clicked
