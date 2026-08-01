"""Welcome page — landing mockup layout."""

from __future__ import annotations

from frontend.components.feature_cards import render_feature_cards
from frontend.components.how_it_works import render_how_it_works
from frontend.components.landing_hero import render_landing_hero
from frontend.components.start_choice import render_start_choice


def render_welcome_page() -> None:
    render_landing_hero()
    render_feature_cards()
    render_how_it_works()
    render_start_choice()
