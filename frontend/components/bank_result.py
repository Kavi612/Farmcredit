"""Bank officer — single farmer review result."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.assessment import load_demo_result, portfolio_row_to_result
from frontend.utils.constants import STATE_NAMES
from frontend.utils.formatting import format_inr, risk_points
from frontend.utils.officer_portfolio import load_portfolio
from frontend.utils.state import go_bank
from frontend.utils.badges import risk_badge_html
from frontend.utils.theme import section_heading


def _lending_notes(level: str, top_factors: list[dict]) -> list[tuple[str, str]]:
    notes: list[tuple[str, str]] = []
    if level in ("High", "Critical"):
        notes.append(
            (
                "Potential concern",
                "Consider reviewing repayment capacity and existing debt burden closely.",
            )
        )
    elif level == "Medium":
        notes.append(
            (
                "Consider reviewing",
                "Profile shows mixed signals — additional income verification may be useful.",
            )
        )
    else:
        notes.append(
            (
                "Favourable indicators",
                "Strong profile overall — standard documentation may suffice.",
            )
        )
    for f in top_factors[:2]:
        pts = int(f.get("points", 0))
        label = str(f.get("display_label") or f.get("feature"))
        if pts >= 8:
            notes.append(
                (
                    "Additional verification may be useful",
                    f"Elevated impact from {label}. {f.get('plain_hint', '')}",
                )
            )
    return notes[:4]


def _resolve_bank_result(farmer_id: str) -> dict | None:
    if farmer_id.startswith("DEMO-"):
        try:
            return load_demo_result(farmer_id)
        except Exception:
            pass
    try:
        _, apps = load_portfolio()
        for app in apps:
            if app["application_id"] == farmer_id:
                result = portfolio_row_to_result(app)
                if app.get("is_demo"):
                    try:
                        full = load_demo_result(farmer_id)
                        result["advisory"] = full.get("advisory", {})
                        result["advisory_text"] = full.get("advisory_text")
                        result["protective_factors"] = full.get("protective_factors", [])
                    except Exception:
                        pass
                return result
    except Exception:
        return None
    return None


def render_bank_result(farmer_id: str, *, inline: bool = False) -> None:
    result = _resolve_bank_result(farmer_id)
    if not result:
        st.error("Could not load this farmer profile.")
        if st.button("Back to farmer list"):
            go_bank()
            st.rerun()
        return

    section_heading("Farmer Profile Review", "Detailed credit-risk overview for lending review.")

    feats = result.get("features") or {}
    state = STATE_NAMES.get(feats.get("state", ""), feats.get("state", ""))
    level = result.get("risk_level") or "Medium"
    score = float(result.get("risk_score") or 0.0)
    name = html.escape(str(result.get("display_name") or farmer_id))

    st.markdown(
        f"""
        <div class="fc-result-hero">
          <div class="fc-profile-name">{name}</div>
          <div class="fc-profile-meta">
            {html.escape(str(state))} · {html.escape(str(feats.get('crop_type', '')))}
            · {feats.get('land_size_ha', '—')} ha · Loan {format_inr(feats.get('loan_amount_inr', 0))}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("Credit Risk Overview", "")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(risk_badge_html(level), unsafe_allow_html=True)
        st.metric("Risk score", f"{risk_points(score)} / 100")
    with c2:
        st.metric("Annual income", format_inr(feats.get("annual_income_inr", 0)))
        st.metric("Existing debt", format_inr(feats.get("existing_debt_inr", 0)))

    section_heading("Risk Factors", "Model-identified drivers for this profile.")
    top = result.get("top_factors") or []
    if top:
        cols = st.columns(min(len(top), 3))
        factor_icons = {
            "repayment": "payments",
            "income": "account_balance_wallet",
            "debt": "credit_card",
            "loan": "payments",
            "rain": "cloud",
            "crop": "agriculture",
        }
        for i, f in enumerate(top[:3]):
            with cols[i]:
                feat_key = str(f.get("feature", "")).lower()
                icon = "analytics"
                for k, ic in factor_icons.items():
                    if k in feat_key:
                        icon = ic
                        break
                label = html.escape(str(f.get("display_label") or f.get("feature")))
                hint = html.escape(str(f.get("plain_hint") or ""))
                st.markdown(f":material/{icon}:")
                st.markdown(
                    f'<div class="fc-card"><div class="fc-card-title">{label}</div>'
                    f'<div class="fc-card-text">{hint}</div></div>',
                    unsafe_allow_html=True,
                )

    section_heading("Recommended Lending Considerations", "")
    for tag, text in _lending_notes(level, top):
        st.markdown(f"**:material/info: {tag}** — {text}")

    if result.get("narrative"):
        st.caption(result["narrative"])

    st.markdown("---")
    if not inline:
        if st.button("← Choose another farmer", key="bank_back_list", use_container_width=True):
            go_bank()
            st.rerun()
