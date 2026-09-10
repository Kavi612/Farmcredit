"""Welcome page."""

from __future__ import annotations

from frontend.components.landing_hero import render_landing_hero


def render_welcome_page() -> None:
    render_landing_hero()
