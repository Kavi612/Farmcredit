"""Advisory card and PDF/JSON downloads."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from typing import Any

import streamlit as st

from frontend.utils import api
from frontend.utils.api import ApiError
from frontend.utils.html_ui import render_html


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
    if not advisory_text:
        render_html(
            '<div class="fc-card"><div class="fc-card-title">What to consider next</div>'
            '<p class="fc-section-sub" style="margin:0;">No advisory text returned for this assessment.</p></div>',
            height=96,
        )
    else:
        safe = html.escape(advisory_text).replace("\n", "<br>")
        meta_bits = []
        if model_id:
            meta_bits.append(f"source: {html.escape(str(model_id))}")
        if cached is not None:
            meta_bits.append("cached demo" if cached else "live result")
        if latency_ms is not None:
            meta_bits.append(f"{int(latency_ms)} ms")
        meta = (
            f'<p class="fc-section-sub" style="margin:12px 0 0;">{ " · ".join(meta_bits)}</p>'
            if meta_bits
            else ""
        )
        approx = 120 + max(1, advisory_text.count("\n") + len(advisory_text) // 90) * 22
        render_html(
            f'<div class="fc-card"><div class="fc-card-title">What to consider next</div>'
            f'<div style="font-size:14px;line-height:1.55;color:#111827;">{safe}</div>'
            f"{meta}</div>",
            height=min(360, approx),
        )

    st.markdown(
        '<p class="fc-section-title" style="font-size:16px;">Downloads</p>',
        unsafe_allow_html=True,
    )
    pdf_key = f"pdf_{farmer_label}"
    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        if st.button(
            "Prepare PDF",
            key=f"btn_{pdf_key}",
            use_container_width=True,
            icon=":material/picture_as_pdf:",
        ):
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
    with c2:
        if pdf_key in st.session_state:
            pdf_bytes, filename = st.session_state[pdf_key]
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                key=f"dl_{pdf_key}",
                icon=":material/download:",
            )
        else:
            st.caption("Prepare PDF first")
    with c3:
        payload = report or {
            "advisory_text": advisory_text,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(payload, indent=2),
            file_name=f"farmcredit_report_{farmer_label}.json",
            mime="application/json",
            use_container_width=True,
            key=f"json_{pdf_key}",
            icon=":material/data_object:",
        )
