"""System status — hidden in expander for admins."""

from __future__ import annotations

import streamlit as st

from frontend.utils import api
from frontend.utils.api import ApiError


def render_system_status() -> None:
    with st.expander("System Status (technical)", expanded=False):
        try:
            health = api.health()
            st.markdown(
                f"- **API:** `{api.get_base_url()}`\n"
                f"- **Model:** {'ready' if health.get('xgb_loaded') else 'not loaded'}\n"
                f"- **LLM:** {'on' if health.get('llm_enabled') else 'off (demo/template advice)'}"
            )
        except ApiError as exc:
            st.error(exc.message)
