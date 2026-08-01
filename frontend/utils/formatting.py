"""Display helpers for scores and money."""

from __future__ import annotations


def risk_points(score: float) -> int:
    return int(round(float(score) * 100))


def format_inr(value: int | float) -> str:
    return f"₹{int(value):,}"


def shorten(text: str, max_len: int = 140) -> str:
    text = (text or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"
