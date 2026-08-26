"""Site footer."""

from __future__ import annotations

from frontend.utils.html_ui import render_html


def render_site_footer() -> None:
    render_html(
        """
        <footer class="fc-footer-wrap">
          <div class="fc-footer-brand">FarmCredit AI</div>
          <p class="fc-footer-copy">Portfolio demo · Synthetic data only · Not for real lending decisions</p>
        </footer>
        """
    )
