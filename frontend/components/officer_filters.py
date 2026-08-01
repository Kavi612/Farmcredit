"""Sidebar / main-area filters for the bank officer dashboard."""

from __future__ import annotations

import streamlit as st

from frontend.utils.constants import STATE_NAMES, STATES


def render_officer_filters(available_states: list[str] | None = None) -> dict:
    states = available_states or STATES
    with st.expander(":material/filter_list: Officer filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            risk_levels = st.multiselect(
                "Risk level",
                ["Low", "Medium", "High", "Critical"],
                default=["Low", "Medium", "High", "Critical"],
            )
            state_options = [f"{s} — {STATE_NAMES.get(s, s)}" for s in states]
            selected_state_labels = st.multiselect(
                "State",
                state_options,
                default=state_options,
            )
            selected_states = [s.split(" — ")[0] for s in selected_state_labels]
        with c2:
            decisions = st.multiselect(
                "Decision",
                ["Pending", "Approved", "Rejected", "Flagged"],
                default=["Pending", "Approved", "Rejected", "Flagged"],
            )
            search = st.text_input("Search name or ID", value="").strip()
        with c3:
            st.caption("Decisions are stored in this browser session only.")
            if st.button("Reset all decisions", key="officer_reset_all", use_container_width=True):
                st.session_state.officer_decisions = {}
                st.session_state.officer_decision_notice = "All decisions reset to Pending."
                st.rerun()

    return {
        "risk_levels": risk_levels,
        "states": selected_states,
        "decisions": decisions,
        "search": search,
        "demos_only": False,
    }
