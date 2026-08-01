"""Advisory text card and PDF/JSON report downloads."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from typing import Any

import streamlit as st

from frontend.utils import api
from frontend.utils.api import ApiError
from frontend.utils.theme import section_heading


def render_advisory_card(
    advisory_text: str | None,
    *,
    model_id: str | None = None,
    cached: bool | None = None,
    latency_ms: int | None = None,
    report: dict | None = None,
    farmer_label: str = "farmer",
    farmer_id: str | None = None,
    features: dict[str, Any] | None = None,
    use_demo_cache: bool = True,
) -> None:
    section_heading("Advice for you", "Plain-language guidance based on your profile.")
    if not advisory_text:
        st.info("No advisory text returned for this assessment.")
        return

    safe = html.escape(advisory_text).replace("\n", "<br>")
    st.markdown(
        f'<div class="fc-advisory-box">{safe}</div>',
        unsafe_allow_html=True,
    )

    meta_bits = []
    if model_id:
        meta_bits.append(f"source: `{model_id}`")
    if cached is not None:
        meta_bits.append("cached demo" if cached else "live result")
    if latency_ms is not None:
        meta_bits.append(f"{latency_ms} ms")
    if meta_bits:
        st.caption(" · ".join(meta_bits))

    st.markdown("##### Download report")
    pdf_key = f"pdf_{farmer_label}"
    if st.button("Prepare PDF report", key=f"btn_{pdf_key}", use_container_width=True):
        with st.spinner("Building PDF…"):
            try:
                pdf_bytes, filename = api.generate_report_pdf(
                    farmer_id=farmer_id,
                    features=features,
                    use_demo_cache=use_demo_cache,
                )
                st.session_state[pdf_key] = (pdf_bytes, filename)
            except ApiError as exc:
                st.error(exc.message)

    if pdf_key in st.session_state:
        pdf_bytes, filename = st.session_state[pdf_key]
        st.download_button(
            label="Download PDF report",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
            key=f"dl_{pdf_key}",
        )

    payload = report or {
        "advisory_text": advisory_text,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    st.download_button(
        label="Download report (JSON)",
        data=json.dumps(payload, indent=2),
        file_name=f"farmcredit_report_{farmer_label}.json",
        mime="application/json",
        use_container_width=True,
        key=f"json_{pdf_key}",
    )
