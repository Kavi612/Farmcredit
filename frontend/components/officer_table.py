"""Officer application table and decision controls."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from frontend.utils.badges import RISK_STYLES, risk_badge_html
from frontend.utils.formatting import format_inr, risk_points
from frontend.utils.theme import section_heading


def _decision_badge(status: str) -> str:
    # Neutral / accent only — risk greens/reds reserved for risk bands.
    styles = {
        "Pending": ("#6b7280", "#f3f4f6"),
        "Approved": ("#2563eb", "#eff6ff"),
        "Rejected": ("#374151", "#f3f4f6"),
        "Flagged": ("#1d4ed8", "#dbeafe"),
    }
    fg, bg = styles.get(status, ("#6b7280", "#f3f4f6"))
    return (
        f'<span class="fc-pill" style="color:{fg};background:{bg};border-color:{fg}33;">'
        f"{status}</span>"
    )


def _set_decision(app_id: str, status: str, note: str) -> None:
    """Assign a new dict so Streamlit detects the session_state change."""
    decisions = dict(st.session_state.get("officer_decisions") or {})
    decisions[app_id] = {
        "status": status,
        "note": note,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    st.session_state.officer_decisions = decisions
    st.session_state.officer_decision_notice = f"{app_id} marked as {status}."


def render_officer_table(
    df: pd.DataFrame,
    applications_by_id: dict[str, dict],
) -> None:
    section_heading("Application queue", "Demo applications in the current filter set.")

    if df.empty:
        st.info("No applications match the current filters.")
        return

    view = df.copy()
    view["risk_points"] = view["risk_score"].map(risk_points)
    view["loan_display"] = view["loan_amount_inr"].map(format_inr)
    view["demo"] = view["is_demo"].map(lambda x: "Yes" if x else "")

    display_cols = [
        "application_id",
        "display_name",
        "state_name",
        "crop_type",
        "loan_display",
        "risk_points",
        "risk_level",
        "decision",
        "demo",
    ]
    st.dataframe(
        view[display_cols].rename(
            columns={
                "application_id": "ID",
                "display_name": "Farmer",
                "state_name": "State",
                "crop_type": "Crop",
                "loan_display": "Loan",
                "risk_points": "Risk pts",
                "risk_level": "Risk level",
                "decision": "Decision",
                "demo": "Demo",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    section_heading("Review & decide", "Select an application and record a session decision.")
    options = [
        f"{r.application_id} — {r.display_name} ({r.risk_level})"
        for r in view.itertuples()
    ]
    selected = st.selectbox("Select application", options, key="officer_app_select")
    app_id = selected.split(" — ")[0]
    app = applications_by_id[app_id]
    decisions = st.session_state.get("officer_decisions") or {}
    decision = decisions.get(app_id, {"status": "Pending", "note": ""})
    current_status = decision.get("status", "Pending")

    notice = st.session_state.pop("officer_decision_notice", None)
    if notice:
        st.success(notice)

    level = app.get("risk_level") or "Medium"
    fg, _bg = RISK_STYLES.get(level, ("#6b7280", "#f3f4f6"))
    st.markdown(
        f"**{app['display_name']}** · {risk_badge_html(level)} "
        f"<span style='color:{fg};font-weight:500'>({risk_points(app['risk_score'])}/100)</span> · "
        f"{format_inr(app['loan_amount_inr'])} · {_decision_badge(current_status)}",
        unsafe_allow_html=True,
    )
    if app.get("narrative"):
        st.caption(app["narrative"])

    factors = app.get("top_factors") or []
    if factors:
        st.markdown("**:material/trending_up: Top drivers:**")
        for f in factors[:3]:
            pts = int(f.get("points", 0))
            sign = "+" if pts > 0 else ""
            st.markdown(
                f"- **{f.get('display_label', f.get('feature'))}** ({sign}{pts}): "
                f"{f.get('plain_hint', '')}"
            )

    note = st.text_input(
        "Officer note (optional)",
        value=decision.get("note", ""),
        key=f"note_{app_id}",
    )
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button(
            "Approve",
            key=f"officer_approve_{app_id}",
            icon=":material/check_circle:",
            type="primary",
            use_container_width=True,
        ):
            _set_decision(app_id, "Approved", note)
            st.rerun()
    with b2:
        if st.button(
            "Reject",
            key=f"officer_reject_{app_id}",
            icon=":material/cancel:",
            use_container_width=True,
        ):
            _set_decision(app_id, "Rejected", note)
            st.rerun()
    with b3:
        if st.button(
            "Flag",
            key=f"officer_flag_{app_id}",
            icon=":material/flag:",
            use_container_width=True,
        ):
            _set_decision(app_id, "Flagged", note)
            st.rerun()
    with b4:
        if st.button(
            "Reset to Pending",
            key=f"officer_reset_{app_id}",
            use_container_width=True,
        ):
            _set_decision(app_id, "Pending", note)
            st.rerun()
