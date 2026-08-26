"""Welcome page — focused, professional landing flow."""

from __future__ import annotations

from frontend.components.feature_cards import render_feature_cards
from frontend.components.how_it_works import render_how_it_works
from frontend.components.landing_hero import render_landing_hero


def render_welcome_page() -> None:
    render_landing_hero()
    render_how_it_works()
    render_feature_cards()
