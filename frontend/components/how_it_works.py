"""How it works — clean three-step process."""

from __future__ import annotations

import html

from frontend.utils.html_ui import render_html
from frontend.utils.theme import section_heading

STEPS = [
    ("1", "Share details", "Use a demo farmer profile or enter your own farm and loan information."),
    ("2", "Get assessed", "The model scores default risk and explains the main drivers behind it."),
    ("3", "Review & decide", "Read the guidance, download a PDF, or switch to the bank officer view."),
]


def render_how_it_works() -> None:
    section_heading("How it works", "Three steps from information to insight.")
    steps = "".join(
        f"""
        <div class="fc-process-step">
          <div class="fc-process-num">{num}</div>
          <div class="fc-process-title">{html.escape(title)}</div>
          <div class="fc-process-text">{html.escape(text)}</div>
        </div>
        """
        for num, title, text in STEPS
    )
    render_html(f'<div class="fc-process-row">{steps}</div>')
