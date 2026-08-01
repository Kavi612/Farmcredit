"""Site footer."""

from __future__ import annotations

from frontend.utils.html_ui import render_html


def render_site_footer() -> None:
    render_html(
        """
        <footer class="fc-footer-wrap">
          <div class="fc-footer-brand">FarmCredit AI</div>
          <div class="fc-footer-tag">Credit Guidance for Farmers</div>
          <p class="fc-footer-copy">© 2026 FarmCredit AI · Illustrative demo — not real lending decisions.</p>
        </footer>
        """
    )
