"""SHAP factor bars and plain-language hints."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from frontend.utils.theme import section_heading


def render_shap_panel(
    top_factors: list[dict],
    protective_factors: list[dict] | None = None,
) -> None:
    section_heading(
        "What's influencing this assessment?",
        "Key factors identified by the credit-risk model.",
    )
    if not top_factors:
        st.info("No explanation factors available for this result.")
        return

    rows = []
    for f in top_factors:
        rows.append(
            {
                "Factor": f.get("display_label") or f.get("feature"),
                "Points": int(f.get("points", 0)),
            }
        )
    df = pd.DataFrame(rows).set_index("Factor")
    try:
        st.bar_chart(df, horizontal=True, color="#2e7d32")
    except TypeError:
        st.bar_chart(df)

    st.markdown("##### :material/chat: In simple words")
    for f in top_factors:
        pts = int(f.get("points", 0))
        sign = "+" if pts > 0 else ""
        label = html.escape(str(f.get("display_label") or f.get("feature")))
        hint = html.escape(str(f.get("plain_hint") or ""))
        color = "#c62828" if pts > 0 else "#2e7d32"
        st.markdown(
            f"- **{label}** "
            f"<span style='color:{color}'>({sign}{pts})</span>: {hint}",
            unsafe_allow_html=True,
        )

    if protective_factors:
        with st.expander(":material/shield: Protective factors", expanded=False):
            for f in protective_factors:
                label = f.get("display_label") or f.get("feature")
                st.markdown(f"- **{label}**: {f.get('plain_hint', '')}")
