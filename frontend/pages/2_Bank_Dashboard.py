"""Legacy multipage entry — redirects to main app."""

import streamlit as st

st.session_state.current_view = "bank"
st.switch_page("streamlit_app.py")
