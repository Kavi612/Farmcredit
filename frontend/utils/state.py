"""Session-state navigation — welcome → farmer | bank, with farmer sub-steps."""

from __future__ import annotations

import streamlit as st

from frontend.utils.constants import DEFAULT_FEATURES

# Top-level: welcome | farmer | bank
# Farmer sub-steps: choose | demo_pick | form | results


def init_app_state() -> None:
    st.session_state.setdefault("current_view", "welcome")
    st.session_state.setdefault("farmer_step", "choose")
    st.session_state.setdefault("farmer_entry_mode", None)
    st.session_state.setdefault("selected_demo_id", None)
    st.session_state.setdefault("form_defaults", dict(DEFAULT_FEATURES))
    st.session_state.setdefault("wizard_meta", {"farmer_name": "", "age": 30})
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("officer_decisions", {})
    st.session_state.setdefault("officer_portfolio", None)
    st.session_state.setdefault("officer_portfolio_label", "")


def _reset_form() -> None:
    st.session_state.form_defaults = dict(DEFAULT_FEATURES)
    st.session_state.wizard_meta = {"farmer_name": "", "age": 30}
    st.session_state.selected_demo_id = None
    st.session_state.result = None


def go_welcome() -> None:
    st.session_state.current_view = "welcome"
    st.session_state.farmer_step = "choose"
    st.session_state.farmer_entry_mode = None
    _reset_form()


def go_farmer() -> None:
    st.session_state.current_view = "farmer"
    st.session_state.farmer_step = "choose"
    st.session_state.farmer_entry_mode = None
    _reset_form()


def go_bank() -> None:
    st.session_state.current_view = "bank"
    st.session_state.farmer_step = "choose"
    st.session_state.farmer_entry_mode = None
    _reset_form()


def go_about() -> None:
    st.session_state.current_view = "about"


def go_farmer_demo() -> None:
    """Welcome hero / start card → demo farmer pick."""
    st.session_state.current_view = "farmer"
    farmer_choose_demo()


def go_farmer_manual() -> None:
    """Welcome hero / start card → empty shared form."""
    st.session_state.current_view = "farmer"
    farmer_choose_manual()


def farmer_choose_demo() -> None:
    st.session_state.farmer_entry_mode = "demo"
    st.session_state.farmer_step = "demo_pick"
    st.session_state.result = None


def farmer_choose_manual() -> None:
    st.session_state.farmer_entry_mode = "manual"
    st.session_state.farmer_step = "form"
    st.session_state.selected_demo_id = None
    st.session_state.form_defaults = dict(DEFAULT_FEATURES)
    st.session_state.wizard_meta = {"farmer_name": "", "age": 30}
    st.session_state.result = None


def farmer_apply_demo_prefill(form_defaults: dict, *, display_name: str, demo_id: str) -> None:
    st.session_state.form_defaults = dict(form_defaults)
    st.session_state.wizard_meta = {"farmer_name": display_name, "age": 30}
    st.session_state.selected_demo_id = demo_id
    st.session_state.farmer_entry_mode = "demo"
    st.session_state.farmer_step = "form"
    st.session_state.result = None


def farmer_show_results(result: dict) -> None:
    st.session_state.result = result
    st.session_state.farmer_step = "results"


def farmer_back_to_choose() -> None:
    st.session_state.farmer_step = "choose"
    st.session_state.farmer_entry_mode = None
    st.session_state.result = None
    st.session_state.selected_demo_id = None


def farmer_back_from_form() -> None:
    if st.session_state.get("farmer_entry_mode") == "demo":
        st.session_state.farmer_step = "demo_pick"
    else:
        st.session_state.farmer_step = "choose"
    st.session_state.result = None


def farmer_new_assessment() -> None:
    st.session_state.farmer_step = "choose"
    st.session_state.farmer_entry_mode = None
    _reset_form()


# Explicit exports (used across views/components)
__all__ = [
    "init_app_state",
    "go_welcome",
    "go_farmer",
    "go_farmer_demo",
    "go_farmer_manual",
    "go_bank",
    "go_about",
    "farmer_choose_demo",
    "farmer_choose_manual",
    "farmer_apply_demo_prefill",
    "farmer_show_results",
    "farmer_back_to_choose",
    "farmer_back_from_form",
    "farmer_new_assessment",
]
