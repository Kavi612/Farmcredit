"""State-level risk visualization for the officer dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.utils.theme import section_header


def render_risk_by_state_chart(df: pd.DataFrame) -> None:
    section_header("Risk by state", icon="map")
    st.caption("Average model risk score across the illustrative portfolio (not a geographic map).")

    if df.empty:
        st.info("No rows match the current filters.")
        return

    grouped = (
        df.groupby("state_name", as_index=False)
        .agg(
            avg_risk_score=("risk_score", "mean"),
            applications=("application_id", "count"),
            high_or_critical=("risk_level", lambda s: int(((s == "High") | (s == "Critical")).sum())),
        )
        .sort_values("avg_risk_score", ascending=False)
    )

    chart_df = grouped.set_index("state_name")[["avg_risk_score"]]
    chart_df = chart_df.rename(columns={"avg_risk_score": "Avg risk score"})
    try:
        st.bar_chart(chart_df, horizontal=True, color="#ef6c00")
    except TypeError:
        st.bar_chart(chart_df)

    band_counts = (
        df["risk_level"]
        .value_counts()
        .reindex(["Low", "Medium", "High", "Critical"])
        .fillna(0)
        .astype(int)
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### :material/pie_chart: Applications by risk band")
        st.bar_chart(band_counts)
    with c2:
        st.markdown("##### :material/warning: High / Critical count by state")
        hi = grouped.set_index("state_name")[["high_or_critical"]].rename(
            columns={"high_or_critical": "High+Critical"}
        )
        try:
            st.bar_chart(hi, horizontal=True, color="#c62828")
        except TypeError:
            st.bar_chart(hi)
