"""FarmCredit AI design system — polished UI tokens & global CSS."""

from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

# ── Palette ───────────────────────────────────────────────────────────────────
GREEN_DARK = "#14532d"
GREEN_MID = "#15803d"
GREEN_BRIGHT = "#22c55e"
GREEN_LIGHT = "#dcfce7"
MINT = "#f0fdf4"
SKY = "#eff6ff"
SKY_DEEP = "#dbeafe"
PAGE_BG = "#f8fafc"
SURFACE = "#ffffff"
TEXT = "#0f172a"
TEXT_MUTED = "#64748b"
BORDER = "#e2e8f0"
BORDER_SOFT = "#f1f5f9"
WHITE = "#ffffff"
SHADOW_SM = "0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04)"
SHADOW_MD = "0 4px 16px rgba(15,23,42,0.08), 0 2px 6px rgba(15,23,42,0.04)"
SHADOW_LG = "0 12px 40px rgba(15,23,42,0.10), 0 4px 12px rgba(15,23,42,0.05)"

RISK_STYLES = {
    "Low": ("#15803d", "#dcfce7"),
    "Medium": ("#a16207", "#fef9c3"),
    "High": ("#c2410c", "#ffedd5"),
    "Critical": ("#b91c1c", "#fee2e2"),
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

HERO_ILLUSTRATION = """
<svg class="fc-farm-svg" viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="heroSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#bfdbfe"/>
      <stop offset="100%" stop-color="#f0fdf4"/>
    </linearGradient>
    <linearGradient id="heroField" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4ade80"/>
      <stop offset="100%" stop-color="#22c55e"/>
    </linearGradient>
  </defs>
  <rect width="400" height="260" rx="20" fill="url(#heroSky)"/>
  <circle cx="330" cy="52" r="32" fill="#fde68a" opacity="0.95"/>
  <ellipse cx="70" cy="58" rx="42" ry="15" fill="#fff" opacity="0.9"/>
  <ellipse cx="105" cy="52" rx="30" ry="11" fill="#fff" opacity="0.75"/>
  <ellipse cx="220" cy="60" rx="36" ry="12" fill="#fff" opacity="0.7"/>
  <path d="M0 175 Q100 155 200 170 T400 175 L400 260 L0 260 Z" fill="url(#heroField)"/>
  <path d="M0 190 Q130 175 240 188 T400 195 L400 260 L0 260 Z" fill="#16a34a" opacity="0.35"/>
  <rect x="268" y="138" width="58" height="42" fill="#a16207" rx="3"/>
  <polygon points="268,138 297,100 326,138" fill="#dc2626"/>
  <rect x="286" y="154" width="16" height="26" fill="#78350f" rx="1"/>
  <rect x="304" y="148" width="12" height="12" fill="#fef3c7" rx="1"/>
  <rect x="310" y="108" width="4" height="34" fill="#78716c"/>
  <polygon points="312,108 312,88 332,108" fill="#e5e7eb" opacity="0.9"/>
  <line x1="312" y1="108" x2="292" y2="128" stroke="#e5e7eb" stroke-width="2"/>
  <line x1="312" y1="108" x2="332" y2="128" stroke="#e5e7eb" stroke-width="2"/>
  <circle cx="312" cy="108" r="3" fill="#78716c"/>
  <circle cx="155" cy="158" r="30" fill="#16a34a"/>
  <circle cx="190" cy="148" r="22" fill="#22c55e"/>
  <rect x="137" y="158" width="6" height="32" fill="#92400e" rx="1"/>
  <rect x="183" y="162" width="5" height="28" fill="#92400e" rx="1"/>
  <circle cx="95" cy="162" r="18" fill="#4ade80"/>
  <rect x="92" y="162" width="4" height="24" fill="#92400e"/>
  <circle cx="230" cy="168" r="14" fill="#86efac"/>
  <rect x="228" y="168" width="3" height="18" fill="#92400e"/>
</svg>
"""

BRAND_LEAF_SVG_RAW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M12 2C8 6 4 8 4 14c0 4 3.5 7 8 8 4.5-1 8-4 8-8 0-6-4-8-8-12z" fill="#15803d"/>
  <path d="M12 22V10" stroke="#dcfce7" stroke-width="1.5" stroke-linecap="round"/>
</svg>
""".strip()

# Kept for any legacy inline SVG usage
BRAND_LEAF_SVG = BRAND_LEAF_SVG_RAW.replace(
    'viewBox="0 0 24 24"', 'width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"'
)
BRAND_LEAF_SVG_HERO = BRAND_LEAF_SVG_RAW.replace(
    'viewBox="0 0 24 24"', 'width="64" height="64" viewBox="0 0 24 24" aria-hidden="true"'
)


def _svg_data_uri(svg: str) -> str:
    return "data:image/svg+xml;charset=utf-8," + quote(svg.strip())


BRAND_LEAF_ICON_URI = _svg_data_uri(BRAND_LEAF_SVG_RAW)

THEME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,800&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {{
  --fc-green: {GREEN_MID};
  --fc-green-dark: {GREEN_DARK};
  --fc-text: {TEXT};
  --fc-muted: {TEXT_MUTED};
  --fc-border: {BORDER};
  --fc-surface: {SURFACE};
  --fc-radius: 18px;
  --fc-radius-lg: 24px;
  --fc-font: 'Outfit', 'Segoe UI', sans-serif;
  --fc-display: 'Fraunces', Georgia, serif;
}}

html, body, [class*="css"] {{
  font-family: var(--fc-font) !important;
  color: {TEXT};
}}
.stApp {{
  background:
    linear-gradient(180deg, #ecfdf5 0%, #f7faf8 38%, #f8fafc 100%) !important;
}}

@keyframes fc-fade-up {{
  from {{ opacity: 0; transform: translateY(18px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fc-soft-zoom {{
  from {{ transform: scale(1.04); }}
  to {{ transform: scale(1); }}
}}
@keyframes fc-fade-in {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
  display: none !important;
  height: 0 !important;
  visibility: hidden !important;
}}

.stAppViewContainer .main .block-container,
.block-container {{
  padding-top: 0.5rem;
  padding-bottom: 2.5rem;
  max-width: 1140px;
}}
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {{
  display: none !important;
}}

/* ── Bottom CTA band ── */
.fc-cta-band {{
  background: linear-gradient(135deg, {GREEN_DARK} 0%, {GREEN_MID} 55%, #166534 100%);
  border-radius: 22px;
  padding: 2rem 2.25rem 3.25rem;
  margin: 3rem 0 0;
  box-shadow: {SHADOW_LG};
  color: white;
  position: relative;
  overflow: hidden;
}}
.fc-cta-band::before {{
  content: "";
  position: absolute;
  width: 280px; height: 280px;
  top: -60%; right: -5%;
  background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.fc-cta-band-inner {{
  position: relative;
  z-index: 1;
}}
.fc-cta-band-title {{
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.45rem 0;
  line-height: 1.2;
}}
.fc-cta-band-sub {{
  font-size: 0.95rem;
  opacity: 0.88;
  line-height: 1.55;
  margin: 0;
  max-width: 560px;
}}
.fc-cta-actions {{
  margin: -2.35rem 0 0.5rem 0;
  padding: 0 1.25rem;
  position: relative;
  z-index: 2;
}}

/* ── Header shell (brand + nav) ── */
.fc-header-shell {{
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226,232,240,0.95);
  border-bottom: none;
  border-radius: 20px 20px 0 0;
  padding: 0.9rem 1.15rem 0;
  margin-bottom: 0;
  box-shadow: none;
}}
.fc-header-shell .fc-brand {{
  padding-bottom: 0.8rem;
  border-bottom: 1px solid {BORDER_SOFT};
  margin-bottom: 0;
}}
div[data-testid="stMarkdownContainer"]:has(.fc-header-shell) {{
  margin-bottom: 0 !important;
}}

/* Nav row card styling */
.fc-nav-row-marker {{
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}}

div.element-container:has(.fc-nav-row-marker) + div.element-container div[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226,232,240,0.95);
  border-top: none;
  border-radius: 0 0 20px 20px;
  padding: 0.55rem 1.15rem 0.7rem;
  margin-top: -0.5rem;
  margin-bottom: 1.35rem;
  box-shadow: 0 8px 28px rgba(15, 70, 40, 0.06);
  align-items: center !important;
  gap: 0.45rem !important;
}}

@media (max-width: 768px) {{
  div.element-container:has(.fc-nav-row-marker) + div.element-container div[data-testid="stHorizontalBlock"],
  [data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
    flex-wrap: nowrap !important;
    gap: 0.5rem !important;
    padding: 0.45rem 0.85rem 0.55rem !important;
    border-radius: 0 0 16px 16px !important;
    margin-bottom: 1rem !important;
  }}
  div.element-container:has(.fc-nav-row-marker) + div.element-container [data-testid="stPopover"] > button,
  [data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPopover"] > button {{
    padding: 0.4rem 0.35rem !important;
    font-size: 1.05rem !important;
    min-height: 2.35rem !important;
    line-height: 1 !important;
  }}
}}

/* ── Full-bleed photo hero ── */
.fc-hero-bleed {{
  position: relative;
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  margin-bottom: 2.25rem;
  min-height: min(72vh, 640px);
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  border-radius: 0;
  isolation: isolate;
  animation: fc-fade-in 0.7s ease both;
}}
.fc-hero-bleed-bg {{
  position: absolute;
  inset: 0;
  background-color: #14532d;
  background-position: center center;
  background-size: cover;
  background-repeat: no-repeat;
  animation: fc-soft-zoom 12s ease-out both;
  z-index: 0;
}}
.fc-hero-bleed-veil {{
  position: absolute;
  inset: 0;
  z-index: 1;
  background:
    linear-gradient(105deg, rgba(10, 36, 22, 0.82) 0%, rgba(15, 61, 36, 0.62) 42%, rgba(15, 61, 36, 0.28) 68%, rgba(15, 61, 36, 0.12) 100%),
    linear-gradient(180deg, rgba(8, 28, 18, 0.15) 0%, rgba(8, 28, 18, 0.55) 100%);
}}
.fc-hero-bleed-content {{
  position: relative;
  z-index: 2;
  width: min(1140px, calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 3.5rem 0 3.25rem;
  animation: fc-fade-up 0.85s 0.12s ease both;
}}
.fc-hero-brand {{
  font-family: var(--fc-display);
  font-size: clamp(2.6rem, 6.2vw, 4.4rem);
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.035em;
  line-height: 0.98;
  margin: 0 0 0.85rem 0;
  text-shadow: 0 2px 24px rgba(0,0,0,0.25);
  max-width: 14ch;
}}
.fc-hero-title {{
  font-family: var(--fc-font);
  font-size: clamp(1.15rem, 2.2vw, 1.45rem);
  font-weight: 600;
  color: rgba(255,255,255,0.94);
  line-height: 1.35;
  letter-spacing: -0.01em;
  margin: 0 0 0.75rem 0;
  max-width: 28ch;
}}
.fc-hero-sub {{
  color: rgba(236, 253, 245, 0.88);
  font-size: 1.02rem;
  line-height: 1.6;
  max-width: 36ch;
  margin: 0;
  font-weight: 400;
}}
.fc-hero-cta-bar {{
  width: min(1140px, 100%);
  margin: -1.1rem auto 2.5rem;
  max-width: 560px;
  padding: 0;
  position: relative;
  z-index: 3;
  animation: fc-fade-up 0.8s 0.28s ease both;
}}
.fc-hero-cta-label {{
  display: none;
}}
.fc-hero-open {{
  display: none;
}}
.fc-feature-section {{
  animation: fc-fade-up 0.75s 0.18s ease both;
}}
.fc-icon-svg {{
  width: 26px;
  height: 26px;
  display: block;
}}

/* ── Card grids ── */
.fc-card-grid {{
  display: grid;
  gap: 1.1rem;
  margin-bottom: 0.5rem;
}}
.fc-card-grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
.fc-card-grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
.fc-card-grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
.fc-card-grid-5 {{ grid-template-columns: repeat(5, 1fr); }}

@media (max-width: 900px) {{
  .fc-card-grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
}}

.fc-steps-row {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.1rem;
  position: relative;
  margin-bottom: 0.5rem;
}}
.fc-step-card {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: var(--fc-radius);
  padding: 1.45rem 1.35rem;
  box-shadow: {SHADOW_SM};
  height: 100%;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}}
.fc-step-card:hover {{
  transform: translateY(-2px);
  box-shadow: {SHADOW_MD};
}}

/* legacy hero panels */
.fc-hero-panel {{
  background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 55%, #f0fdf4 100%);
  border: 1px solid #dbeafe;
  border-radius: 22px;
  padding: 2rem 1.75rem;
  box-shadow: {SHADOW_LG};
  height: 100%;
  box-sizing: border-box;
}}

/* ── Sections ── */
.fc-section-title {{
  font-family: var(--fc-display);
  font-size: 1.85rem;
  font-weight: 700;
  color: {GREEN_DARK};
  letter-spacing: -0.03em;
  margin: 3rem 0 0.45rem 0;
  line-height: 1.15;
}}
.fc-section-title:first-child {{ margin-top: 0.25rem; }}
.fc-section-sub {{
  color: {TEXT_MUTED};
  font-size: 0.98rem;
  line-height: 1.55;
  margin: 0 0 1.45rem 0;
  max-width: 640px;
}}

/* ── Cards ── */
.fc-card {{
  background: {SURFACE};
  border: 1px solid rgba(226,232,240,0.9);
  border-radius: var(--fc-radius);
  padding: 1.55rem 1.35rem 1.45rem;
  box-shadow: 0 10px 30px rgba(15, 70, 40, 0.05);
  height: 100%;
  box-sizing: border-box;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}}
.fc-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 16px 36px rgba(15, 70, 40, 0.09);
  border-color: #bbf7d0;
}}
.fc-card-icon-wrap {{
  width: 52px; height: 52px;
  border-radius: 16px;
  background: linear-gradient(145deg, #ecfdf5, #dcfce7);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.1rem;
  border: 1px solid #bbf7d0;
  color: {GREEN_MID};
}}
.fc-card-num {{
  width: 36px; height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, {GREEN_MID}, {GREEN_BRIGHT});
  color: white;
  font-size: 0.78rem;
  font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 0.85rem;
}}
.fc-card-title {{
  font-weight: 700;
  color: {TEXT};
  font-size: 1.05rem;
  margin-bottom: 0.5rem;
  letter-spacing: -0.015em;
}}
.fc-card-text {{
  color: {TEXT_MUTED};
  font-size: 0.9rem;
  line-height: 1.6;
}}

.fc-choice-card {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: var(--fc-radius-lg);
  padding: 1.65rem 1.5rem 1.25rem;
  box-shadow: {SHADOW_SM};
  height: 100%;
  margin-bottom: 0.85rem;
  transition: box-shadow 0.18s ease, border-color 0.18s ease;
}}
.fc-choice-card:hover {{
  box-shadow: {SHADOW_MD};
  border-color: #cbd5e1;
}}
.fc-choice-icon {{
  width: 52px; height: 52px;
  border-radius: 16px;
  background: linear-gradient(135deg, {SKY}, {GREEN_LIGHT});
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem;
  margin-bottom: 1rem;
  border: 1px solid #dbeafe;
}}

.fc-profile-card {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: var(--fc-radius);
  padding: 1.15rem 1.2rem 1rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  box-shadow: {SHADOW_SM};
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.fc-profile-card:hover {{
  transform: translateY(-1px);
  box-shadow: {SHADOW_MD};
}}
.fc-profile-crop {{
  width: 40px; height: 40px;
  border-radius: 12px;
  background: {MINT};
  border: 1px solid #bbf7d0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
}}
.fc-profile-name {{
  font-weight: 700;
  color: {GREEN_DARK};
  font-size: 0.98rem;
  letter-spacing: -0.01em;
}}
.fc-profile-meta {{
  color: {TEXT_MUTED};
  font-size: 0.8rem;
  margin: 0.2rem 0 0.55rem;
  font-weight: 500;
}}
.fc-profile-desc {{
  color: {TEXT_MUTED};
  font-size: 0.8rem;
  line-height: 1.5;
  flex: 1;
  margin-top: 0.35rem;
}}

.fc-risk-badge {{
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 800;
  padding: 0.22rem 0.65rem;
  border-radius: 999px;
  letter-spacing: 0.04em;
}}

.fc-result-hero {{
  background: linear-gradient(135deg, {SURFACE}, {MINT});
  border: 1px solid #bbf7d0;
  border-radius: var(--fc-radius-lg);
  padding: 1.35rem 1.5rem;
  margin-bottom: 1.25rem;
  box-shadow: {SHADOW_SM};
}}

.fc-footer-wrap {{
  margin-top: 3rem;
  padding: 1.75rem 0 0.25rem;
  border-top: 1px solid {BORDER};
  text-align: center;
}}
.fc-footer-brand {{
  font-weight: 800;
  color: {GREEN_DARK};
  font-size: 0.98rem;
  margin-bottom: 0.2rem;
}}
.fc-footer-tag {{
  font-size: 0.82rem;
  color: {TEXT_MUTED};
  margin-bottom: 0.75rem;
}}
.fc-footer-copy {{
  text-align: center;
  font-size: 0.78rem;
  color: #94a3b8;
  margin: 0.85rem 0 0;
  line-height: 1.5;
}}
.fc-advisory-box {{
  background: linear-gradient(135deg, #f0fdf4, #ffffff);
  border: 1px solid #bbf7d0;
  border-radius: 16px;
  padding: 1.25rem 1.35rem;
  line-height: 1.65;
  color: {GREEN_DARK};
  box-shadow: {SHADOW_SM};
}}
.fc-panel {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: var(--fc-radius-lg);
  padding: 1.35rem 1.4rem;
  box-shadow: {SHADOW_SM};
  margin-bottom: 1rem;
}}

.fc-brand {{
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 0;
}}
.fc-brand-icon {{
  width: 44px; height: 44px;
  border-radius: 50%;
  background: linear-gradient(145deg, #dcfce7, #bbf7d0);
  border: 1px solid #86efac;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}}
.fc-brand-icon svg,
.fc-brand-icon img {{
  width: 22px;
  height: 22px;
  display: block;
}}
.fc-brand-name {{
  font-family: var(--fc-display);
  font-size: 1.2rem;
  font-weight: 700;
  color: {GREEN_DARK};
  letter-spacing: -0.025em;
  line-height: 1.15;
}}
.fc-brand-tag {{
  font-size: 0.78rem;
  color: {TEXT_MUTED};
  font-weight: 500;
  margin-top: 0.12rem;
}}

/* ── Streamlit widgets ── */
[data-testid="stHorizontalBlock"] {{
  gap: 0.65rem !important;
  align-items: stretch !important;
}}
[data-testid="column"] [data-testid="stVerticalBlock"] {{
  gap: 0.35rem !important;
}}

.stButton > button {{
  border-radius: 14px !important;
  font-weight: 650 !important;
  font-family: var(--fc-font) !important;
  padding: 0.7rem 1.2rem !important;
  transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease !important;
  border: 1px solid {BORDER} !important;
  box-shadow: 0 2px 8px rgba(15,70,40,0.05) !important;
}}
.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, #166534, {GREEN_MID}) !important;
  border-color: #166534 !important;
  color: white !important;
  box-shadow: 0 8px 22px rgba(21,128,61,0.28) !important;
}}
.stButton > button[kind="primary"]:hover {{
  background: linear-gradient(135deg, {GREEN_DARK}, #166534) !important;
  border-color: {GREEN_DARK} !important;
  transform: translateY(-1px);
}}
.stButton > button[kind="secondary"] {{
  background: rgba(255,255,255,0.92) !important;
}}
.stButton > button[kind="secondary"]:hover {{
  border-color: #86efac !important;
  background: {MINT} !important;
}}

div[data-testid="stForm"] {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: var(--fc-radius-lg);
  padding: 1.5rem 1.35rem;
  box-shadow: {SHADOW_SM};
}}

[data-testid="stMetric"] {{
  background: {SURFACE};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 0.85rem 1rem;
  box-shadow: {SHADOW_SM};
}}
[data-testid="stMetricLabel"] {{
  font-size: 0.78rem !important;
  color: {TEXT_MUTED} !important;
  font-weight: 600 !important;
}}
[data-testid="stMetricValue"] {{
  font-size: 1.5rem !important;
  font-weight: 800 !important;
  color: {GREEN_DARK} !important;
}}

[data-testid="stDataFrame"] {{
  border: 1px solid {BORDER};
  border-radius: 14px;
  overflow: hidden;
  box-shadow: {SHADOW_SM};
}}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {{
  border-radius: 10px !important;
}}

hr {{
  border: none !important;
  border-top: 1px solid {BORDER} !important;
  margin: 2rem 0 !important;
}}

@media (max-width: 768px) {{
  .stAppViewContainer .main .block-container,
  .block-container {{
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    padding-top: 0.35rem !important;
  }}

  /* Header */
  .fc-header-shell {{
    padding: 0.7rem 0.85rem 0 !important;
    margin-bottom: 0 !important;
    border-radius: 16px 16px 0 0 !important;
  }}
  .fc-header-shell .fc-brand {{
    padding-bottom: 0.65rem !important;
  }}

  /* Stack page content columns — not the nav row */
  section.main .block-container div[data-testid="stHorizontalBlock"]:not(:has([data-testid="stPopover"])) {{
    flex-wrap: wrap !important;
  }}
  section.main .block-container div[data-testid="stHorizontalBlock"]:not(:has([data-testid="stPopover"])) > [data-testid="column"] {{
    flex: 1 1 100% !important;
    min-width: 100% !important;
    width: 100% !important;
  }}

  .fc-hero-bleed {{
    min-height: min(62vh, 520px) !important;
    margin-bottom: 1.5rem !important;
  }}
  .fc-hero-bleed-content {{
    padding: 2.4rem 0 2.1rem !important;
    width: calc(100% - 1.5rem) !important;
  }}
  .fc-hero-brand {{
    font-size: 2.35rem !important;
    max-width: none !important;
  }}
  .fc-hero-title {{
    font-size: 1.08rem !important;
    max-width: none !important;
    margin-bottom: 0.55rem !important;
  }}
  .fc-hero-sub {{
    font-size: 0.92rem !important;
    max-width: none !important;
  }}
  .fc-hero-cta-bar {{
    margin: -0.65rem 0 1.5rem 0 !important;
    max-width: none !important;
  }}

  /* Sections & cards */
  .fc-section-title {{ font-size: 1.4rem !important; margin-top: 1.75rem !important; }}
  .fc-section-sub {{ font-size: 0.88rem !important; margin-bottom: 1rem !important; }}
  .fc-card-grid-3, .fc-card-grid-2, .fc-card-grid-4, .fc-card-grid-5, .fc-steps-row {{
    grid-template-columns: 1fr !important;
  }}

  /* CTA band */
  .fc-cta-band {{
    padding: 1.25rem 1rem 2rem !important;
    border-radius: 16px !important;
    margin-top: 1.75rem !important;
  }}
  .fc-cta-band-title {{ font-size: 1.15rem !important; }}
  .fc-cta-band-sub {{ font-size: 0.86rem !important; }}
  .fc-cta-actions {{
    margin: -1.5rem 0 0.5rem 0 !important;
    padding: 0 !important;
  }}

  /* Brand */
  .fc-brand-name {{ font-size: 0.98rem !important; }}
  .fc-brand-tag {{ font-size: 0.7rem !important; }}

  /* Content buttons (not nav row with popover) */
  section.main .block-container div[data-testid="stHorizontalBlock"]:not(:has([data-testid="stPopover"])) .stButton > button {{
    padding: 0.62rem 0.85rem !important;
    font-size: 0.88rem !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    min-height: 2.75rem !important;
  }}

  /* Metrics & tables */
  [data-testid="stMetric"] {{ margin-bottom: 0.35rem !important; }}
  [data-testid="stMetricValue"] {{ font-size: 1.25rem !important; }}
  [data-testid="stDataFrame"] {{ overflow-x: auto !important; }}

  [data-testid="stHtml"],
  [data-testid="stHtml"] iframe {{
    width: 100% !important;
    max-width: 100% !important;
  }}
}}

@media (max-width: 480px) {{
  .fc-hero-brand {{ font-size: 2.05rem !important; }}
  .fc-hero-title {{ font-size: 1rem !important; }}
}}
"""

# CSS injected into every st.html iframe (global theme CSS does NOT reach iframes)
HTML_IFRAME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,800&family=Outfit:wght@400;500;600;700;800&display=swap');
* {{ box-sizing: border-box; }}
body {{
  font-family: 'Outfit', 'Segoe UI', sans-serif;
  margin: 0;
  color: {TEXT};
}}
.fc-brand {{ display: flex; align-items: center; gap: 0.65rem; }}
.fc-brand-icon {{
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(145deg, #dcfce7, #bbf7d0);
  border: 1px solid #86efac;
  display: flex; align-items: center; justify-content: center;
}}
.fc-brand-icon svg,
.fc-brand-icon img {{ width: 22px; height: 22px; display: block; }}
.fc-brand-name {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.2rem; font-weight: 700; color: {GREEN_DARK}; line-height: 1.15;
}}
.fc-brand-tag {{ font-size: 0.78rem; color: {TEXT_MUTED}; margin-top: 0.12rem; }}
.fc-card-grid {{ display: grid; gap: 1.1rem; }}
.fc-card-grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
.fc-card-grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
.fc-card-grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
.fc-card-grid-5 {{ grid-template-columns: repeat(5, 1fr); }}
.fc-steps-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; }}
.fc-card, .fc-step-card, .fc-choice-card, .fc-profile-card {{
  background: {SURFACE};
  border: 1px solid rgba(226,232,240,0.9);
  border-radius: 18px;
  padding: 1.45rem 1.25rem;
  box-shadow: 0 10px 30px rgba(15, 70, 40, 0.05);
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}}
.fc-card:hover, .fc-step-card:hover, .fc-choice-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 16px 36px rgba(15, 70, 40, 0.09);
  border-color: #bbf7d0;
}}
.fc-choice-card {{ border-radius: 20px; padding: 1.65rem 1.5rem; margin-bottom: 0; }}
.fc-choice-icon {{
  width: 52px; height: 52px; border-radius: 16px;
  background: linear-gradient(135deg, {SKY}, {GREEN_LIGHT});
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; margin-bottom: 1rem; border: 1px solid #dbeafe;
}}
.fc-card-icon-wrap {{
  width: 52px; height: 52px; border-radius: 16px;
  background: linear-gradient(145deg, #ecfdf5, #dcfce7);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.1rem; border: 1px solid #bbf7d0; color: {GREEN_MID};
}}
.fc-icon-svg {{ width: 26px; height: 26px; display: block; }}
.fc-card-num {{
  width: 36px; height: 36px; border-radius: 12px;
  background: linear-gradient(135deg, {GREEN_MID}, {GREEN_BRIGHT});
  color: white; font-size: 0.78rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 0.85rem;
}}
.fc-card-title {{ font-weight: 700; color: {TEXT}; font-size: 1.05rem; margin-bottom: 0.5rem; }}
.fc-card-text {{ color: {TEXT_MUTED}; font-size: 0.9rem; line-height: 1.6; }}
.fc-profile-crop {{
  width: 40px; height: 40px; border-radius: 12px; background: {MINT};
  border: 1px solid #bbf7d0; display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; margin-bottom: 0.75rem;
}}
.fc-profile-name {{ font-weight: 700; color: {GREEN_DARK}; font-size: 0.98rem; }}
.fc-profile-meta {{ color: {TEXT_MUTED}; font-size: 0.8rem; margin: 0.2rem 0 0.55rem; }}
.fc-profile-desc {{ color: {TEXT_MUTED}; font-size: 0.8rem; line-height: 1.5; margin-top: 0.35rem; }}
.fc-risk-badge {{
  display: inline-block; font-size: 0.68rem; font-weight: 800;
  padding: 0.22rem 0.65rem; border-radius: 999px;
}}
.fc-footer-wrap {{ text-align: center; padding: 1.5rem 0 0.25rem; border-top: 1px solid {BORDER}; margin-top: 2rem; }}
.fc-footer-brand {{
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 700; color: {GREEN_DARK}; font-size: 1.05rem;
}}
.fc-footer-tag {{ font-size: 0.82rem; color: {TEXT_MUTED}; margin-top: 0.2rem; }}
.fc-footer-copy {{ font-size: 0.78rem; color: #94a3b8; margin: 0.85rem 0 0; line-height: 1.5; }}
.fc-cta-band {{
  background: linear-gradient(135deg, {GREEN_DARK} 0%, {GREEN_MID} 55%, #166534 100%);
  border-radius: 22px;
  padding: 2rem 2.25rem;
  margin: 0;
  box-shadow: {SHADOW_LG};
  color: white;
  position: relative;
  overflow: hidden;
}}
.fc-cta-band::before {{
  content: "";
  position: absolute;
  width: 280px; height: 280px;
  top: -60%; right: -5%;
  background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.fc-cta-band-inner {{ position: relative; z-index: 1; }}
.fc-cta-band-title {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.55rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 0.45rem 0;
  line-height: 1.2;
}}
.fc-cta-band-sub {{
  font-size: 0.95rem;
  opacity: 0.88;
  line-height: 1.55;
  margin: 0;
}}
@media (max-width: 900px) {{
  .fc-card-grid-4 {{ grid-template-columns: repeat(2, 1fr) !important; }}
}}
@media (max-width: 768px) {{
  .fc-card-grid-3, .fc-card-grid-2, .fc-card-grid-4, .fc-card-grid-5, .fc-steps-row {{
    grid-template-columns: 1fr !important;
  }}
  .fc-card, .fc-step-card, .fc-choice-card, .fc-profile-card {{
    padding: 1.15rem 1.05rem !important;
  }}
  .fc-cta-band {{
    padding: 1.35rem 1.15rem 2.25rem !important;
    border-radius: 18px !important;
  }}
  .fc-cta-band-title {{ font-size: 1.25rem !important; }}
  .fc-cta-band-sub {{ font-size: 0.88rem !important; }}
}}
"""


def apply_theme() -> None:
    st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)


def brand_icon_html(*, size: str = "sm") -> str:
    if size == "hero":
        return (
            f'<div class="fc-hero-icon">'
            f'<img src="{BRAND_LEAF_ICON_URI}" alt="" width="64" height="64" />'
            f"</div>"
        )
    return (
        f'<div class="fc-brand-icon">'
        f'<img src="{BRAND_LEAF_ICON_URI}" alt="" width="22" height="22" />'
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
    """No-op — kept for backward compatibility."""
    return


def section_header(title: str, icon: str = "analytics") -> None:
    st.markdown(f":material/{icon}: **{title}**")


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
