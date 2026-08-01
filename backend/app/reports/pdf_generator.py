"""Convert FarmCredit report payloads into a downloadable PDF."""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

RISK_COLORS = {
    "Low": colors.HexColor("#2e7d32"),
    "Medium": colors.HexColor("#f9a825"),
    "High": colors.HexColor("#ef6c00"),
    "Critical": colors.HexColor("#c62828"),
}

SCHEME_BULLETS = [
    "PM-KISAN — income support for eligible landholding farmers (verify eligibility locally).",
    "Kisan Credit Card (KCC) — working-capital credit for crop and farm needs.",
    "PMFBY — crop insurance against weather and yield shocks (check crop/season coverage).",
]

DISCLAIMER = (
    "Indicative demo report only. Synthetic portfolio data — not an official bank or "
    "government credit decision. Confirm scheme details and subsidy amounts at your bank or CSC."
)


def _safe(value: Any) -> str:
    if value is None:
        return "—"
    return str(value)


def _wrap(text: str, style: ParagraphStyle) -> Paragraph:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(escaped, style)


def build_pdf(report: dict[str, Any]) -> bytes:
    """Build PDF bytes from a ReportResponse-like dict."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=report.get("title", "FarmCredit Report"),
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#1b5e20"),
        spaceAfter=8,
    )
    h2 = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#33691e"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        leading=11,
    )

    story: list[Any] = []
    story.append(_wrap(report.get("title", "FarmCredit AI — Risk Brief"), title_style))
    generated = report.get("generated_at")
    if generated:
        story.append(_wrap(f"Generated: {generated}", small))
    story.append(_wrap(DISCLAIMER, small))
    story.append(Spacer(1, 0.15 * inch))

    summary = report.get("farmer_summary") or {}
    features = summary.get("features") or {}
    display_name = summary.get("display_name") or summary.get("farmer_id") or "Farmer"

    story.append(_wrap("Farmer summary", h2))
    summary_rows = [
        ["Name / ID", _safe(display_name)],
        ["State", _safe(features.get("state"))],
        ["District", _safe(features.get("district"))],
        ["Crop", _safe(features.get("crop_type"))],
        ["Season", _safe(features.get("season"))],
        ["Land (ha)", _safe(features.get("land_size_ha"))],
        ["Soil", _safe(features.get("soil_type"))],
        ["Rainfall (mm)", _safe(features.get("rainfall_mm"))],
        ["Irrigation", _safe(features.get("irrigation_type"))],
        ["Loan (₹)", _safe(features.get("loan_amount_inr"))],
        ["Annual income (₹)", _safe(features.get("annual_income_inr"))],
        ["Existing debt (₹)", _safe(features.get("existing_debt_inr"))],
    ]
    summary_table = Table(summary_rows, colWidths=[1.6 * inch, 4.6 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f8e9")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 0.12 * inch))

    risk_level = report.get("risk_level", "Medium")
    risk_score = float(report.get("risk_score", 0.0))
    risk_color = RISK_COLORS.get(risk_level, colors.black)
    story.append(_wrap("Risk assessment", h2))
    risk_rows = [
        ["Risk level", risk_level],
        ["Risk score", f"{risk_score:.2f} ({int(round(risk_score * 100))}/100)"],
    ]
    risk_table = Table(risk_rows, colWidths=[1.6 * inch, 4.6 * inch])
    risk_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (1, 0), (1, 0), risk_color),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ]
        )
    )
    story.append(risk_table)
    story.append(Spacer(1, 0.12 * inch))

    factors = report.get("top_factors") or []
    story.append(_wrap("What drove this score (SHAP)", h2))
    if factors:
        factor_rows = [["Factor", "Impact", "Explanation"]]
        for f in factors[:5]:
            pts = int(f.get("points", 0))
            sign = "+" if pts > 0 else ""
            factor_rows.append(
                [
                    _safe(f.get("display_label") or f.get("feature")),
                    f"{sign}{pts} pts",
                    _safe(f.get("plain_hint")),
                ]
            )
        factor_table = Table(factor_rows, colWidths=[1.4 * inch, 0.8 * inch, 4.0 * inch])
        factor_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eceff1")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(factor_table)
    else:
        story.append(_wrap("No factor breakdown available.", body))

    story.append(Spacer(1, 0.12 * inch))
    story.append(_wrap("Advisory", h2))
    advisory = report.get("advisory_text") or "No advisory text included in this report."
    story.append(_wrap(advisory, body))

    story.append(Spacer(1, 0.12 * inch))
    story.append(_wrap("Scheme checks (indicative)", h2))
    for bullet in SCHEME_BULLETS:
        story.append(_wrap(f"• {bullet}", body))

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        _wrap(
            f"FarmCredit AI · portfolio demo · {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            small,
        )
    )

    doc.build(story)
    return buffer.getvalue()
