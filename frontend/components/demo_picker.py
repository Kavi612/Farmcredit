"""One-click demo farmer cards."""

from __future__ import annotations

import html

import streamlit as st

from frontend.utils.constants import RISK_COLORS, STATE_NAMES
from frontend.utils.formatting import shorten
from frontend.utils.theme import crop_emoji, section_header


def _demo_card_html(
    *,
    border: str,
    shadow: str,
    crop: str,
    name: str,
    state_label: str,
    level: str,
    color: str,
    narrative: str,
) -> str:
    return (
        f'<div class="fc-demo-card" style="border:{border};{shadow}">'
        f'<div class="fc-demo-crop">{crop_emoji(crop)}</div>'
        f'<div class="fc-demo-name">{name}</div>'
        f'<div class="fc-demo-meta">{state_label} · {html.escape(crop)}</div>'
        f'<span class="fc-risk-pill" style="background:{color}22;color:{color};">'
        f"{html.escape(level)}</span>"
        f'<div class="fc-demo-narrative">{narrative}</div>'
        f"</div>"
    )


def render_demo_picker(demos: list[dict], selected_id: str | None) -> str | None:
    section_header("Try Demo", icon="play_circle")
    st.caption("One click loads a pre-built farmer profile — no form filling needed.")

    if not demos:
        st.warning("No demo farmers available from the API.")
        return None

    clicked: str | None = None
    n = min(len(demos), 5)
    cols = st.columns(n, gap="small", vertical_alignment="bottom")

    for i, demo in enumerate(demos[:n]):
        with cols[i]:
            level = demo.get("risk_level") or "Medium"
            color = RISK_COLORS.get(level, "#546e7a")
            state = demo.get("state", "")
            state_label = html.escape(STATE_NAMES.get(state, state))
            crop = demo.get("crop_type", "")
            selected = demo.get("id") == selected_id
            border = f"2px solid {color}" if selected else "1px solid #e0e0e0"
            shadow = (
                "box-shadow:0 2px 8px rgba(46,125,50,0.12);"
                if selected
                else ""
            )
            name = html.escape(str(demo.get("display_name", "")))
            narrative = html.escape(shorten(demo.get("narrative", ""), 100))

            st.markdown(
                _demo_card_html(
                    border=border,
                    shadow=shadow,
                    crop=crop,
                    name=name,
                    state_label=state_label,
                    level=level,
                    color=color,
                    narrative=narrative,
                ),
                unsafe_allow_html=True,
            )
            if st.button(
                f"Load {demo.get('id')}",
                key=f"demo_btn_{demo.get('id')}",
                use_container_width=True,
                type="primary" if selected else "secondary",
                icon=":material/arrow_forward:",
            ):
                clicked = demo.get("id")

    return clicked
