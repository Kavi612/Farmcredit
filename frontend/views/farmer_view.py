"""Unified farmer flow — choose → demo pick (optional) → form → results."""

from __future__ import annotations

import streamlit as st

from frontend.components.demo_profile_grid import render_demo_profile_grid
from frontend.components.farmer_form import render_farmer_form
from frontend.components.farmer_result import render_farmer_result
from frontend.utils import api
from frontend.utils.api import ApiError
from frontend.utils.assessment import load_demo_prefill, run_custom_assess
from frontend.utils.state import (
    farmer_apply_demo_prefill,
    farmer_back_from_form,
    farmer_back_to_choose,
    farmer_choose_demo,
    farmer_choose_manual,
    farmer_new_assessment,
    farmer_show_results,
    go_welcome,
)
from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading


@st.cache_data(ttl=60)
def _cached_demos() -> list[dict]:
    return api.list_demo_farmers()


def _render_choose_step() -> None:
    section_heading(
        "How would you like to start?",
        "Try a demo profile or enter your own farm details — both use the same form.",
    )
    render_html(
        """
        <div class="fc-card-grid fc-card-grid-2">
          <div class="fc-choice-card">
            <div class="fc-choice-icon">▶</div>
            <div class="fc-card-title">Try Demo Data</div>
            <div class="fc-card-text">Pick one of 5 sample farmers and see their actual values pre-filled in the form.</div>
          </div>
          <div class="fc-choice-card">
            <div class="fc-choice-icon">📋</div>
            <div class="fc-card-title">Enter Your Own Data</div>
            <div class="fc-card-text">Start with a blank form and fill in your farm and financial details manually.</div>
          </div>
        </div>
        """
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if st.button("Try Demo Data →", key="farmer_try_demo", type="primary", use_container_width=True):
            farmer_choose_demo()
            st.rerun()
    with c2:
        if st.button("Enter Your Own Data →", key="farmer_enter_own", use_container_width=True):
            farmer_choose_manual()
            st.rerun()

    if st.button("← Back to Welcome", key="farmer_choose_back"):
        go_welcome()
        st.rerun()


def _render_demo_pick_step() -> None:
    try:
        demos = _cached_demos()
    except ApiError as exc:
        st.error(exc.message)
        demos = []

    picked = render_demo_profile_grid(demos)
    if picked:
        with st.spinner("Loading farmer data…"):
            try:
                features, display_name = load_demo_prefill(picked)
                farmer_apply_demo_prefill(features, display_name=display_name, demo_id=picked)
                st.rerun()
            except ApiError as exc:
                st.error(exc.message)

    if st.button("← Back", key="farmer_demo_back"):
        farmer_back_to_choose()
        st.rerun()


def _render_form_step() -> None:
    features = render_farmer_form()
    if features:
        with st.spinner("Analyzing your credit risk…"):
            try:
                result = run_custom_assess(features)
                if st.session_state.get("selected_demo_id"):
                    result["farmer_id"] = st.session_state.selected_demo_id
                farmer_show_results(result)
                st.rerun()
            except ApiError as exc:
                st.error(exc.message)

    if st.button("← Back", key="farmer_form_back"):
        farmer_back_from_form()
        st.rerun()


def _render_results_step() -> None:
    result = st.session_state.get("result")
    if not result:
        farmer_back_to_choose()
        st.rerun()
        return

    st.markdown("---")
    render_farmer_result(result, inline=True)

    if st.button(
        "Start a new assessment",
        key="farmer_new_assessment",
        use_container_width=True,
        icon=":material/refresh:",
    ):
        farmer_new_assessment()
        st.rerun()


def render_farmer_view() -> None:
    step = st.session_state.get("farmer_step", "choose")
    if step == "choose":
        _render_choose_step()
    elif step == "demo_pick":
        _render_demo_pick_step()
    elif step == "form":
        _render_form_step()
    elif step == "results":
        _render_results_step()
    else:
        farmer_back_to_choose()
        st.rerun()
