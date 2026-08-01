"""Shared farmer form — empty or pre-filled from demo selection."""

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


def render_farmer_form(*, title: str | None = None, subtitle: str | None = None) -> dict | None:
    defaults = st.session_state.get("form_defaults") or dict(DEFAULT_FEATURES)
    meta = st.session_state.setdefault("wizard_meta", {"farmer_name": "", "age": 30})
    demo_id = st.session_state.get("selected_demo_id")

    heading = title or "Farm & credit details"
    sub = subtitle or (
        f"Pre-filled from {demo_id} — review the values below, then submit."
        if demo_id
        else "Fill in your farm and financial details to get a credit risk assessment."
    )
    section_heading(heading, sub)

    with st.form("shared_farmer_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            meta["farmer_name"] = st.text_input(
                "Full name (optional, for display)",
                value=meta.get("farmer_name", ""),
            )
            state_labels = [f"{s} — {STATE_NAMES.get(s, s)}" for s in STATES]
            default_state = defaults.get("state", "MH")
            state_idx = STATES.index(default_state) if default_state in STATES else 0
            state_choice = st.selectbox("State", state_labels, index=state_idx)
            state = state_choice.split(" — ")[0]

            districts = DISTRICTS_BY_STATE.get(state, [])
            default_district = defaults.get("district", districts[0] if districts else "")
            district_idx = (
                districts.index(default_district) if default_district in districts else 0
            )
            district = st.selectbox("District / zone", districts, index=district_idx)

            crop_default = defaults.get("crop_type", "Soybean")
            crop_idx = CROPS.index(crop_default) if crop_default in CROPS else 0
            crop_type = st.selectbox("Crop", CROPS, index=crop_idx)

            season_default = defaults.get("season", "Kharif")
            season_idx = SEASONS.index(season_default) if season_default in SEASONS else 0
            season = st.selectbox("Season", SEASONS, index=season_idx)

            soil_default = defaults.get("soil_type", "Black")
            soil_idx = SOILS.index(soil_default) if soil_default in SOILS else 0
            soil_type = st.selectbox("Soil type", SOILS, index=soil_idx)

            irr_default = defaults.get("irrigation_type", "Tubewell")
            irr_idx = IRRIGATION.index(irr_default) if irr_default in IRRIGATION else 0
            irrigation_type = st.selectbox("Irrigation", IRRIGATION, index=irr_idx)

            prior_default = bool(defaults.get("prior_default_flag", 0))
            prior_default_flag = (
                1 if st.checkbox("Had a prior loan default", value=prior_default) else 0
            )

        with c2:
            land_size_ha = st.number_input(
                "Land size (hectares)",
                min_value=0.2,
                max_value=10.0,
                value=float(defaults.get("land_size_ha", 1.2)),
                step=0.1,
            )
            rainfall_mm = st.number_input(
                "Annual rainfall (mm)",
                min_value=0.0,
                max_value=4000.0,
                value=float(defaults.get("rainfall_mm", 780.0)),
                step=10.0,
            )
            loan_amount_inr = st.number_input(
                "Loan amount requested (₹)",
                min_value=25000,
                max_value=800000,
                value=int(defaults.get("loan_amount_inr", 180000)),
                step=5000,
            )
            annual_income_inr = st.number_input(
                "Annual farm income (₹)",
                min_value=40000,
                max_value=700000,
                value=int(defaults.get("annual_income_inr", 165000)),
                step=5000,
            )
            existing_debt_inr = st.number_input(
                "Existing debt (₹)",
                min_value=0,
                max_value=400000,
                value=int(defaults.get("existing_debt_inr", 70000)),
                step=5000,
            )
            prior_loan_count = st.number_input(
                "Prior loan count",
                min_value=0,
                max_value=8,
                value=int(defaults.get("prior_loan_count", 2)),
                step=1,
            )
            repayment_score = st.slider(
                "Repayment history score",
                min_value=0.0,
                max_value=100.0,
                value=float(defaults.get("repayment_score", 62.0)),
                step=1.0,
            )

        submitted = st.form_submit_button(
            "Get my risk assessment",
            use_container_width=True,
            type="primary",
            icon=":material/analytics:",
        )

    st.session_state.wizard_meta = meta

    if not submitted:
        return None

    features = {
        "state": state,
        "district": district,
        "crop_type": crop_type,
        "season": season,
        "land_size_ha": float(land_size_ha),
        "soil_type": soil_type,
        "rainfall_mm": float(rainfall_mm),
        "irrigation_type": irrigation_type,
        "loan_amount_inr": int(loan_amount_inr),
        "prior_loan_count": int(prior_loan_count),
        "prior_default_flag": int(prior_default_flag),
        "repayment_score": float(repayment_score),
        "annual_income_inr": int(annual_income_inr),
        "existing_debt_inr": int(existing_debt_inr),
    }
    st.session_state.form_defaults = features
    return features
