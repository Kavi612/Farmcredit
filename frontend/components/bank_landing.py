"""Bank Officer landing — choose demo or full profile list."""

from __future__ import annotations

import streamlit as st

from frontend.utils.state import go_bank_demo, go_bank_profiles, go_welcome
from frontend.utils.theme import section_heading


def render_bank_landing() -> None:
    section_heading(
        "FarmCredit AI — Bank Officer",
        "Review farmer credit-risk profiles and support informed lending decisions.",
    )
    st.markdown(
        "Use FarmCredit AI to explore farmer credit-risk profiles, understand the "
        "factors behind assessments, and support informed lending decisions."
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(":material/play_circle:")
        st.markdown(
            """
            <div class="fc-choice-card">
              <div class="fc-card-title">Explore Demo Profiles</div>
              <div class="fc-card-text">
                Use sample farmer data to understand how the bank officer view works.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Use Demo Data",
            key="bank_land_demo",
            type="primary",
            use_container_width=True,
            icon=":material/arrow_forward:",
        ):
            go_bank_demo()
            st.rerun()
    with c2:
        st.markdown(":material/groups:")
        st.markdown(
            """
            <div class="fc-choice-card">
              <div class="fc-card-title">Review Farmer Profiles</div>
              <div class="fc-card-text">
                Select a farmer and review their available credit-risk information.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "View Farmer Profiles",
            key="bank_land_profiles",
            use_container_width=True,
            icon=":material/arrow_forward:",
        ):
            go_bank_profiles()
            st.rerun()

    if st.button("← Back to Farmer View", key="bank_land_back"):
        go_welcome()
        st.rerun()
