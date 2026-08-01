"""Prompt builders for FarmCredit advisory (Mistral chat template)."""

from __future__ import annotations

from typing import Any

SYSTEM_PROMPT = (
    "You are FarmCredit AI, a practical agricultural credit advisor for Indian farmers. "
    "Use simple everyday language. Explain risk clearly, suggest practical next steps, "
    "and mention schemes like PM-KISAN, KCC, or PMFBY only as indicative options to "
    "verify at a local bank/CSC. Do not invent exact subsidy amounts or guarantee approval."
)


def build_advisory_messages(
    features: dict[str, Any],
    risk_score: float,
    risk_level: str,
    top_factors: list[dict[str, Any]],
    question: str | None = None,
) -> list[dict[str, str]]:
    drivers = [
        f"- {f.get('display_label', f.get('feature'))}: {f.get('plain_hint')} "
        f"({f.get('points', 0):+d} pts)"
        for f in top_factors
        if f.get("direction") == "increases_risk"
    ][:5]
    helpers = [
        f"- {f.get('display_label', f.get('feature'))}: {f.get('plain_hint')} "
        f"({f.get('points', 0):+d} pts)"
        for f in top_factors
        if f.get("direction") == "decreases_risk"
    ][:3]

    user_q = question or (
        "Explain my risk in simple words and tell me what I should do next, "
        "including relevant government scheme checks."
    )

    user_content = (
        f"Farmer profile:\n"
        f"- State: {features.get('state')}, District: {features.get('district')}\n"
        f"- Crop: {features.get('crop_type')} ({features.get('season')})\n"
        f"- Soil: {features.get('soil_type')}, Rainfall: {features.get('rainfall_mm')} mm\n"
        f"- Irrigation: {features.get('irrigation_type')}, Land: {features.get('land_size_ha')} ha\n"
        f"- Loan: Rs {features.get('loan_amount_inr')}, Existing debt: Rs {features.get('existing_debt_inr')}\n"
        f"- Annual income: Rs {features.get('annual_income_inr')}\n"
        f"- Repayment score: {features.get('repayment_score')}, "
        f"Prior default: {features.get('prior_default_flag')}\n\n"
        f"Model risk score: {risk_score:.2f} ({risk_level})\n\n"
        f"Top risk drivers:\n"
        + ("\n".join(drivers) if drivers else "- None dominant")
        + "\n\nProtective factors:\n"
        + ("\n".join(helpers) if helpers else "- None dominant")
        + f"\n\nFarmer question: {user_q}\n"
        "Answer in 4-8 short sentences."
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def template_advisory(
    risk_level: str,
    top_factors: list[dict[str, Any]],
    display_name: str | None = None,
) -> str:
    name = display_name or "ji"
    drivers = [
        f["plain_hint"]
        for f in top_factors
        if f.get("direction") == "increases_risk"
    ][:3]
    helpers = [
        f["plain_hint"]
        for f in top_factors
        if f.get("direction") == "decreases_risk"
    ][:2]
    driver_txt = "; ".join(drivers) if drivers else "Overall credit and climate balance."
    help_txt = "; ".join(helpers) if helpers else "Keep practices that protect income."
    return (
        f"Namaste {name}. Your FarmCredit risk level is {risk_level}. "
        f"Main pressure points: {driver_txt}. "
        f"What is helping: {help_txt}. "
        f"Next steps: match crop and irrigation to local rainfall, keep loan size "
        f"close to expected income, and ask your bank/CSC about KCC, PM-KISAN, and "
        f"PMFBY eligibility. Figures here are indicative for this demo — confirm locally."
    )
