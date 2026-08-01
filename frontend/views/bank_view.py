"""Bank officer dashboard — demo farmers, filters, decisions, district risk."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.components.officer_filters import render_officer_filters
from frontend.components.officer_table import render_officer_table
from frontend.components.risk_by_state_chart import render_risk_by_state_chart
from frontend.utils import api
from frontend.utils.api import ApiError
from frontend.utils.constants import STATE_NAMES
from frontend.utils.officer_portfolio import portfolio_to_dataframe_rows
from frontend.utils.state import go_farmer
from frontend.utils.theme import section_heading


def _ensure_state() -> None:
    st.session_state.setdefault("officer_decisions", {})
    st.session_state.setdefault("officer_portfolio", None)


@st.cache_data(ttl=300, show_spinner=False)
def _load_demo_portfolio() -> list[dict]:
    """Build officer queue from the 5 API demo farmers only."""
    rows: list[dict] = []
    demos = api.list_demo_farmers()
    for demo in demos:
        bundle = api.get_demo_farmer(demo["id"])
        features = bundle["features"]
        prediction = bundle.get("prediction") or {}
        explanation = bundle.get("explanation") or {}
        rows.append(
            {
                "application_id": demo["id"],
                "display_name": bundle.get("display_name") or demo["id"],
                "is_demo": True,
                "narrative": bundle.get("narrative"),
                "state": features["state"],
                "state_name": STATE_NAMES.get(features["state"], features["state"]),
                "district": features["district"],
                "crop_type": features["crop_type"],
                "season": features.get("season"),
                "loan_amount_inr": features["loan_amount_inr"],
                "land_size_ha": features.get("land_size_ha"),
                "risk_score": prediction.get("risk_score"),
                "risk_level": prediction.get("risk_level"),
                "top_factors": explanation.get("top_factors")
                or prediction.get("top_factors")
                or [],
                "features": features,
            }
        )
    rows.sort(key=lambda r: float(r["risk_score"] or 0), reverse=True)
    return rows


def render_bank_view() -> None:
    _ensure_state()

    section_heading(
        "Bank Officer Dashboard",
        "Review demo loan applications, filter by risk, and record approve / reject / flag decisions.",
    )

    try:
        api.health()
    except ApiError as exc:
        st.error(exc.message)
        st.stop()

    if st.session_state.officer_portfolio is None:
        try:
            st.session_state.officer_portfolio = _load_demo_portfolio()
        except ApiError as exc:
            st.error(exc.message)
            st.stop()

    apps: list[dict] = st.session_state.officer_portfolio
    states = sorted({a["state"] for a in apps})

    filters = render_officer_filters(states)
    table_rows = portfolio_to_dataframe_rows(apps, st.session_state.officer_decisions)
    df = pd.DataFrame(table_rows)

    mask = (
        df["risk_level"].isin(filters["risk_levels"])
        & df["state"].isin(filters["states"])
        & df["decision"].isin(filters["decisions"])
    )
    if filters["search"]:
        q = filters["search"].lower()
        mask &= (
            df["application_id"].str.lower().str.contains(q)
            | df["display_name"].str.lower().str.contains(q)
        )
    filtered = df.loc[mask].sort_values("risk_score", ascending=False)

    section_heading("Portfolio overview", "Summary counts for the filtered queue.")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Applications", len(filtered))
    m2.metric("Pending", int((filtered["decision"] == "Pending").sum()))
    m3.metric("Approved", int((filtered["decision"] == "Approved").sum()))
    m4.metric("Rejected", int((filtered["decision"] == "Rejected").sum()))
    m5.metric("Flagged", int((filtered["decision"] == "Flagged").sum()))

    section_heading("District / state risk view", "Risk distribution across states in the queue.")
    render_risk_by_state_chart(filtered)

    apps_by_id = {a["application_id"]: a for a in apps}
    render_officer_table(filtered, apps_by_id)

    st.markdown("---")
    if st.button(
        "← Switch to Farmer View",
        key="bank_to_farmer",
        use_container_width=True,
        icon=":material/agriculture:",
    ):
        go_farmer()
        st.rerun()
