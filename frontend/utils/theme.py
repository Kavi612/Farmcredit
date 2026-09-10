"""FarmCredit AI design system — one visual language for every screen."""

from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

# ── Palette ───────────────────────────────────────────────────────────────────
GREEN_DARK = "#0f3d24"
GREEN_MID = "#1b5e38"
GREEN_BRIGHT = "#2f9e5c"
GREEN_LIGHT = "#e7f5ec"
MINT = "#f3faf6"
PAGE_BG = "#f4f6f5"
SURFACE = "#ffffff"
TEXT = "#15231b"
TEXT_MUTED = "#5f6f66"
BORDER = "#dde5df"
BORDER_SOFT = "#eef3f0"
WHITE = "#ffffff"

RISK_STYLES = {
    "Low": ("#1b5e38", "#e7f5ec"),
    "Medium": ("#9a6700", "#fff6db"),
    "High": ("#b54708", "#ffedd5"),
    "Critical": ("#b42318", "#fee4e2"),
}

CROP_ICON: dict[str, str] = {
    "Cotton": "filter_vintage",
    "Groundnut": "nutrition",
    "Maize": "grain",
    "Millet": "grass",
    "Mustard": "local_florist",
    "Pulses": "spa",
    "Rice": "rice_bowl",
    "Soybean": "eco",
    "Sugarcane": "forest",
    "Wheat": "agriculture",
}

BRAND_LEAF_SVG_RAW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M12 2C8 6 4 8 4 14c0 4 3.5 7 8 8 4.5-1 8-4 8-8 0-6-4-8-8-12z" fill="#1b5e38"/>
  <path d="M12 22V10" stroke="#e7f5ec" stroke-width="1.5" stroke-linecap="round"/>
</svg>
""".strip()


def _svg_data_uri(svg: str) -> str:
    return "data:image/svg+xml;charset=utf-8," + quote(svg.strip())


BRAND_LEAF_ICON_URI = _svg_data_uri(BRAND_LEAF_SVG_RAW)

# Shared CSS used both in page theme and st.html iframes
_SHARED_COMPONENT_CSS = f"""
.fc-brand {{ display: flex; align-items: center; gap: 0.7rem; min-width: 0; }}
.fc-brand-icon {{
  width: 42px; height: 42px; border-radius: 50%;
  background: {GREEN_LIGHT}; border: 1px solid #c6e7d2;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}}
.fc-brand-icon img {{ width: 20px; height: 20px; display: block; }}
.fc-brand-name {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.15rem; font-weight: 700; color: {GREEN_DARK};
  letter-spacing: -0.02em; line-height: 1.15;
}}
.fc-brand-tag {{ font-size: 0.78rem; color: {TEXT_MUTED}; margin-top: 0.1rem; }}

.fc-section-title {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.55rem; font-weight: 700; color: {GREEN_DARK};
  letter-spacing: -0.025em; margin: 1.75rem 0 0.35rem; line-height: 1.2;
}}
.fc-section-sub {{
  color: {TEXT_MUTED}; font-size: 0.95rem; line-height: 1.55;
  margin: 0 0 1.15rem; max-width: 54ch;
}}

.fc-card-grid {{ display: grid; gap: 0.9rem; margin-bottom: 0.35rem; }}
.fc-card-grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
.fc-card-grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
.fc-card-grid-5 {{ grid-template-columns: repeat(5, 1fr); }}

.fc-choice-card, .fc-profile-card, .fc-card {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 1.15rem 1.1rem;
}}
.fc-choice-icon {{
  width: 36px; height: 36px; border-radius: 10px;
  background: {GREEN_LIGHT}; color: {GREEN_DARK};
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 700; margin-bottom: 0.75rem;
  border: 1px solid #c6e7d2;
}}
.fc-card-title {{ font-weight: 700; color: {TEXT}; font-size: 1rem; margin-bottom: 0.35rem; }}
.fc-card-text {{ color: {TEXT_MUTED}; font-size: 0.9rem; line-height: 1.55; }}

.fc-profile-crop {{
  width: 36px; height: 36px; border-radius: 10px; background: {GREEN_LIGHT};
  border: 1px solid #c6e7d2; display: flex; align-items: center; justify-content: center;
  font-size: 1.05rem; margin-bottom: 0.65rem;
}}
.fc-profile-name {{ font-weight: 700; color: {GREEN_DARK}; font-size: 0.95rem; }}
.fc-profile-meta {{ color: {TEXT_MUTED}; font-size: 0.78rem; margin: 0.2rem 0 0.45rem; }}
.fc-profile-desc {{ color: {TEXT_MUTED}; font-size: 0.78rem; line-height: 1.45; margin-top: 0.4rem; }}

.fc-risk-badge {{
  display: inline-block; font-size: 0.68rem; font-weight: 750;
  padding: 0.2rem 0.55rem; border-radius: 999px; letter-spacing: 0.02em;
}}

.fc-capability-grid {{ display: grid; border-top: 1px solid {BORDER}; }}
.fc-capability {{
  display: grid; grid-template-columns: 2.75rem 1fr; gap: 0.75rem;
  padding: 1.05rem 0; border-bottom: 1px solid {BORDER};
}}
.fc-capability-num {{
  font-family: 'Fraunces', Georgia, serif; font-weight: 700;
  color: {GREEN_MID}; font-size: 1.05rem;
}}
.fc-capability-title {{ font-weight: 700; color: {TEXT}; margin-bottom: 0.25rem; }}
.fc-capability-text {{ color: {TEXT_MUTED}; font-size: 0.9rem; line-height: 1.5; }}

.fc-process-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }}
.fc-process-step {{ border-top: 2px solid {GREEN_MID}; padding-top: 0.85rem; }}
.fc-process-num {{
  font-family: 'Fraunces', Georgia, serif; font-size: 1.2rem; font-weight: 700;
  color: {GREEN_MID}; margin-bottom: 0.35rem;
}}
.fc-process-title {{ font-weight: 700; color: {TEXT}; margin-bottom: 0.3rem; }}
.fc-process-text {{ color: {TEXT_MUTED}; font-size: 0.9rem; line-height: 1.5; }}

.fc-footer-wrap {{
  margin-top: 2.5rem; padding-top: 1.25rem; border-top: 1px solid {BORDER};
}}
.fc-footer-brand {{
  font-family: 'Fraunces', Georgia, serif; font-weight: 700;
  color: {GREEN_DARK}; font-size: 1rem; margin-bottom: 0.25rem;
}}
.fc-footer-copy {{ font-size: 0.78rem; color: #8a9a91; margin: 0; line-height: 1.5; }}

@media (max-width: 768px) {{
  .fc-card-grid-2, .fc-card-grid-3, .fc-card-grid-5, .fc-process-row {{
    grid-template-columns: 1fr !important;
  }}
}}
"""

THEME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Outfit:wght@400;500;600;700&display=swap');

:root {{
  --fc-green: {GREEN_MID};
  --fc-green-dark: {GREEN_DARK};
  --fc-text: {TEXT};
  --fc-muted: {TEXT_MUTED};
  --fc-border: {BORDER};
  --fc-surface: {SURFACE};
  --fc-font: 'Outfit', 'Segoe UI', sans-serif;
  --fc-display: 'Fraunces', Georgia, serif;
}}

html, body, [class*="css"] {{
  font-family: var(--fc-font) !important;
  color: {TEXT};
}}
.stApp {{
  background:
    radial-gradient(ellipse 80% 40% at 10% -10%, rgba(231,245,236,0.9) 0%, transparent 55%),
    {PAGE_BG} !important;
}}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {{
  display: none !important;
}}

.stAppViewContainer .main .block-container,
.block-container {{
  padding-top: 0.75rem;
  padding-bottom: 2.75rem;
  max-width: 1040px;
}}

{_SHARED_COMPONENT_CSS}

/* Header */
.fc-header-shell {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-bottom: none;
  border-radius: 14px 14px 0 0;
  padding: 0.85rem 1rem 0;
}}
.fc-header-shell .fc-brand {{
  padding-bottom: 0.7rem;
  border-bottom: 1px solid {BORDER_SOFT};
}}
div[data-testid="stMarkdownContainer"]:has(.fc-header-shell) {{
  margin-bottom: 0 !important;
}}
.fc-nav-row-marker {{ display: none !important; height: 0 !important; margin: 0 !important; }}

div.element-container:has(.fc-nav-row-marker) + div.element-container div[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-top: none;
  border-radius: 0 0 14px 14px;
  padding: 0.45rem 0.75rem 0.55rem;
  margin-top: -0.45rem;
  margin-bottom: 1.35rem;
  align-items: center !important;
  gap: 0.35rem !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="secondary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] {{
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: {TEXT} !important;
  font-weight: 560 !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="primary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="primary"] {{
  background: {GREEN_DARK} !important;
  border-color: {GREEN_DARK} !important;
}}

/* Welcome hero */
.fc-hero {{
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  min-height: min(48vh, 420px);
  margin: 0 0 1rem 0;
  display: flex;
  align-items: flex-end;
  isolation: isolate;
}}
.fc-hero-media, .fc-hero-fallback {{
  position: absolute; inset: 0; background: {GREEN_DARK}; z-index: 0;
}}
.fc-hero-img {{
  width: 100%; height: 100%; object-fit: cover; object-position: center 40%; display: block;
}}
.fc-hero-veil {{
  position: absolute; inset: 0; z-index: 1;
  background:
    linear-gradient(105deg, rgba(10,32,20,0.88) 0%, rgba(10,32,20,0.62) 42%, rgba(10,32,20,0.22) 100%),
    linear-gradient(180deg, rgba(10,32,20,0.1) 0%, rgba(10,32,20,0.5) 100%);
}}
.fc-hero-body {{
  position: relative; z-index: 2; padding: 2rem 1.5rem 1.75rem; max-width: 36rem;
}}
.fc-hero-brand {{
  font-family: var(--fc-display);
  font-size: clamp(2.3rem, 5vw, 3.4rem);
  font-weight: 700; color: #fff; letter-spacing: -0.03em;
  line-height: 1; margin: 0 0 0.75rem;
}}
.fc-hero-sub {{
  margin: 0; color: rgba(236,253,245,0.9); font-size: 1.02rem; line-height: 1.55;
}}
.fc-hero-actions {{
  margin: 0.85rem 0 2rem; max-width: 34rem;
}}

/* Step progress */
.fc-steps {{
  display: flex; flex-wrap: wrap; gap: 0.45rem; margin: 0 0 1.15rem;
}}
.fc-step-pill {{
  font-size: 0.78rem; font-weight: 600; color: {TEXT_MUTED};
  background: {SURFACE}; border: 1px solid {BORDER};
  border-radius: 999px; padding: 0.28rem 0.7rem;
}}
.fc-step-pill.is-active {{
  color: {GREEN_DARK}; background: {GREEN_LIGHT}; border-color: #c6e7d2;
}}
.fc-step-pill.is-done {{
  color: {GREEN_MID};
}}

/* Result / panels */
.fc-result-hero {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 1.15rem 1.2rem;
  margin-bottom: 1rem;
}}
.fc-panel {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 1.15rem 1.2rem;
  margin-bottom: 0.85rem;
}}
.fc-advisory-box {{
  background: {MINT};
  border: 1px solid #c6e7d2;
  border-radius: 14px;
  padding: 1.1rem 1.15rem;
  color: {GREEN_DARK};
  line-height: 1.6;
}}

/* Widgets */
.stButton > button {{
  border-radius: 10px !important;
  font-family: var(--fc-font) !important;
  font-weight: 600 !important;
  padding: 0.62rem 1rem !important;
  border: 1px solid {BORDER} !important;
  box-shadow: none !important;
}}
.stButton > button[kind="primary"] {{
  background: {GREEN_DARK} !important;
  border-color: {GREEN_DARK} !important;
  color: #fff !important;
}}
.stButton > button[kind="primary"]:hover {{
  background: #0a2f1c !important;
  border-color: #0a2f1c !important;
}}
.stButton > button[kind="secondary"]:hover {{
  background: {GREEN_LIGHT} !important;
  border-color: #c6e7d2 !important;
}}
div[data-testid="stForm"] {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 1.2rem 1.1rem;
}}
[data-testid="stMetric"] {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 12px;
  padding: 0.75rem 0.9rem;
}}
[data-testid="stMetricLabel"] {{
  color: {TEXT_MUTED} !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
}}
[data-testid="stMetricValue"] {{
  color: {GREEN_DARK} !important;
  font-weight: 750 !important;
}}
[data-testid="stDataFrame"] {{
  border: 1px solid {BORDER};
  border-radius: 12px;
  overflow: hidden;
}}
hr {{
  border: none !important;
  border-top: 1px solid {BORDER} !important;
  margin: 1.5rem 0 !important;
}}

@media (max-width: 768px) {{
  .block-container {{
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
  }}
  .fc-hero {{ min-height: min(42vh, 340px) !important; border-radius: 14px !important; }}
  .fc-hero-body {{ padding: 1.4rem 1.05rem 1.25rem !important; }}
  .fc-hero-brand {{ font-size: 2.1rem !important; }}
  .fc-hero-actions {{ max-width: none !important; }}
  .fc-section-title {{ font-size: 1.3rem !important; }}
}}
"""

HTML_IFRAME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Outfit:wght@400;500;600;700&display=swap');
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: 'Outfit', 'Segoe UI', sans-serif;
  color: {TEXT};
}}
{_SHARED_COMPONENT_CSS}
"""


def apply_theme() -> None:
    st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)


def brand_icon_html(*, size: str = "sm") -> str:
    px = "20" if size != "hero" else "48"
    return (
        f'<div class="fc-brand-icon">'
        f'<img src="{BRAND_LEAF_ICON_URI}" alt="" width="{px}" height="{px}" />'
        f"</div>"
    )


def brand_html(*, subtitle: str = "Credit Guidance for Farmers", shell: bool = False) -> str:
    inner = f"""
    <div class="fc-brand">
      {brand_icon_html()}
      <div>
        <div class="fc-brand-name">FarmCredit AI</div>
        <div class="fc-brand-tag">{html.escape(subtitle)}</div>
      </div>
    </div>
    """
    if shell:
        return f'<div class="fc-header-shell">{inner}</div>'
    return inner


def section_heading(title: str, subtitle: str = "") -> None:
    st.markdown(f'<p class="fc-section-title">{html.escape(title)}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f'<p class="fc-section-sub">{html.escape(subtitle)}</p>',
            unsafe_allow_html=True,
        )


def section_close() -> None:
    return


def section_header(title: str, icon: str = "analytics") -> None:
    section_heading(title)


def render_step_progress(current: str) -> None:
    """Farmer flow progress: choose → demo/form → results."""
    order = ["choose", "input", "results"]
    labels = {
        "choose": "1 · Path",
        "input": "2 · Details",
        "results": "3 · Result",
    }
    mapped = {
        "choose": "choose",
        "demo_pick": "input",
        "form": "input",
        "results": "results",
    }.get(current, "choose")
    current_idx = order.index(mapped)
    pills = []
    for i, key in enumerate(order):
        cls = "fc-step-pill"
        if i < current_idx:
            cls += " is-done"
        elif i == current_idx:
            cls += " is-active"
        pills.append(f'<span class="{cls}">{labels[key]}</span>')
    st.markdown(f'<div class="fc-steps">{"".join(pills)}</div>', unsafe_allow_html=True)


from frontend.utils.badges import risk_badge_html as _risk_badge_html


def risk_badge_html(level: str) -> str:
    return _risk_badge_html(level)


def crop_icon_name(crop: str) -> str:
    return CROP_ICON.get(crop, "agriculture")


CROP_EMOJI = {
    "Wheat": "🌾",
    "Rice": "🍚",
    "Cotton": "🌿",
    "Soybean": "🫘",
    "Millet": "🌱",
    "Maize": "🌽",
    "Groundnut": "🥜",
    "Mustard": "🌼",
    "Pulses": "🫛",
    "Sugarcane": "🎋",
}


def crop_emoji(crop: str) -> str:
    return CROP_EMOJI.get(crop, "🌾")
