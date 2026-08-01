"""Multi-step custom farm details wizard."""

from __future__ import annotations

import streamlit as st

from frontend.utils.constants import (
    CROPS,
    DEFAULT_FEATURES,
    DISTRICTS_BY_STATE,
    IRRIGATION,
    SEASONS,
    SOILS,
    STATE_NAMES,
    STATES,
)
from frontend.utils.theme import section_heading

STEPS = [
    ("Farmer Information", "badge"),
    ("Farm Information", "agriculture"),
    ("Financial Information", "payments"),
    ("Additional Information", "shield"),
]


def render_wizard_form() -> dict | None:
    step = st.session_state.get("form_step", 0)
    wizard = st.session_state.setdefault("wizard", dict(DEFAULT_FEATURES))
    meta = st.session_state.setdefault("wizard_meta", {"farmer_name": "", "age": 30})

    prog = " · ".join(
        f"{'**' + s[0] + '**' if i == step else s[0]}" for i, s in enumerate(STEPS)
    )
    st.markdown(prog)

    with st.form("wizard_form", clear_on_submit=False):
        if step == 0:
            meta["farmer_name"] = st.text_input(
                "Full name (optional, for display)",
                value=meta.get("farmer_name", ""),
            )
            meta["age"] = st.number_input(
                "Age (optional)",
                min_value=18,
                max_value=90,
                value=int(meta.get("age", 30)),
            )
            state_labels = [f"{s} — {STATE_NAMES.get(s, s)}" for s in STATES]
            idx = STATES.index(wizard["state"]) if wizard["state"] in STATES else 0
            state_choice = st.selectbox("State", state_labels, index=idx)
            wizard["state"] = state_choice.split(" — ")[0]
            districts = DISTRICTS_BY_STATE.get(wizard["state"], [])
            d_idx = (
                districts.index(wizard["district"])
                if wizard["district"] in districts
                else 0
            )
            wizard["district"] = st.selectbox("District / zone", districts, index=d_idx)

        elif step == 1:
            wizard["crop_type"] = st.selectbox(
                "Crop",
                CROPS,
                index=CROPS.index(wizard["crop_type"])
                if wizard["crop_type"] in CROPS
                else 0,
            )
            wizard["land_size_ha"] = st.number_input(
                "Land size (hectares)",
                min_value=0.2,
                max_value=10.0,
                value=float(wizard["land_size_ha"]),
                step=0.1,
            )
            wizard["irrigation_type"] = st.selectbox(
                "Irrigation",
                IRRIGATION,
                index=IRRIGATION.index(wizard["irrigation_type"])
                if wizard["irrigation_type"] in IRRIGATION
                else 0,
            )
            wizard["season"] = st.selectbox(
                "Season",
                SEASONS,
                index=SEASONS.index(wizard["season"])
                if wizard["season"] in SEASONS
                else 0,
            )
            wizard["soil_type"] = st.selectbox(
                "Soil type",
                SOILS,
                index=SOILS.index(wizard["soil_type"])
                if wizard["soil_type"] in SOILS
                else 0,
            )

        elif step == 2:
            wizard["annual_income_inr"] = st.number_input(
                "Annual farm income (₹)",
                min_value=40000,
                max_value=700000,
                value=int(wizard["annual_income_inr"]),
                step=5000,
            )
            wizard["loan_amount_inr"] = st.number_input(
                "Loan amount requested (₹)",
                min_value=25000,
                max_value=800000,
                value=int(wizard["loan_amount_inr"]),
                step=5000,
            )
            wizard["existing_debt_inr"] = st.number_input(
                "Existing debt (₹)",
                min_value=0,
                max_value=400000,
                value=int(wizard["existing_debt_inr"]),
                step=5000,
            )
            wizard["prior_loan_count"] = st.number_input(
                "Prior loan count",
                min_value=0,
                max_value=8,
                value=int(wizard["prior_loan_count"]),
            )
            wizard["repayment_score"] = st.slider(
                "Repayment history score",
                min_value=0.0,
                max_value=100.0,
                value=float(wizard["repayment_score"]),
            )

        else:
            wizard["rainfall_mm"] = st.number_input(
                "Annual rainfall in your area (mm)",
                min_value=0.0,
                max_value=4000.0,
                value=float(wizard["rainfall_mm"]),
                step=10.0,
            )
            wizard["prior_default_flag"] = (
                1
                if st.checkbox(
                    "Had a prior loan default",
                    value=bool(wizard.get("prior_default_flag", 0)),
                )
                else 0
            )
            st.caption(
                "Weather and repayment history help the model estimate crop and credit stress."
            )

        c1, c2, c3 = st.columns(3)
        with c1:
            back = st.form_submit_button("← Back", use_container_width=True, disabled=step == 0)
        with c2:
            nxt = st.form_submit_button(
                "Continue →" if step < len(STEPS) - 1 else "Analyze My Credit Risk →",
                use_container_width=True,
                type="primary",
            )
        with c3:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

    st.session_state.wizard = wizard
    st.session_state.wizard_meta = meta

    if cancel:
        from frontend.utils.state import go_welcome

        go_welcome()
        st.rerun()
    if back and step > 0:
        st.session_state.form_step = step - 1
        st.rerun()
    if nxt:
        if step < len(STEPS) - 1:
            st.session_state.form_step = step + 1
            st.rerun()
        return {
            "state": wizard["state"],
            "district": wizard["district"],
            "crop_type": wizard["crop_type"],
            "season": wizard["season"],
            "land_size_ha": float(wizard["land_size_ha"]),
            "soil_type": wizard["soil_type"],
            "rainfall_mm": float(wizard["rainfall_mm"]),
            "irrigation_type": wizard["irrigation_type"],
            "loan_amount_inr": int(wizard["loan_amount_inr"]),
            "prior_loan_count": int(wizard["prior_loan_count"]),
            "prior_default_flag": int(wizard["prior_default_flag"]),
            "repayment_score": float(wizard["repayment_score"]),
            "annual_income_inr": int(wizard["annual_income_inr"]),
            "existing_debt_inr": int(wizard["existing_debt_inr"]),
        }
    return None
