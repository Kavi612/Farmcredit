"""FarmCredit AI design system — clean neutral UI, risk colors only for risk."""

from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

# ── Palette (mockup: soft blue page, royal accent) ─────────────────────────────
PAGE_BG = "#eef3fb"
SURFACE = "#ffffff"
BORDER = "#e5e7eb"
TEXT = "#0f172a"
TEXT_MUTED = "#64748b"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1d4ed8"
SHADOW = "0 10px 30px rgba(15, 23, 42, 0.08)"
RADIUS = "20px"

# Risk band colors — ONLY for risk UI
RISK_STYLES = {
    "Low": ("#15803d", "#dcfce7"),
    "Medium": ("#a16207", "#fef3c7"),
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

BRAND_LEAF_SVG_RAW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M12 2C8 6 4 8 4 14c0 4 3.5 7 8 8 4.5-1 8-4 8-8 0-6-4-8-8-12z" fill="#2563eb"/>
  <path d="M12 22V10" stroke="#eff6ff" stroke-width="1.5" stroke-linecap="round"/>
</svg>
""".strip()


def _svg_data_uri(svg: str) -> str:
    return "data:image/svg+xml;charset=utf-8," + quote(svg.strip())


BRAND_LEAF_ICON_URI = _svg_data_uri(BRAND_LEAF_SVG_RAW)

_SHARED = f"""
.fc-brand {{ display:flex; align-items:center; gap:0.65rem; }}
.fc-brand-icon {{
  width:40px; height:40px; border-radius:10px; background:#eff6ff;
  border:1px solid #dbeafe; display:flex; align-items:center; justify-content:center;
}}
.fc-brand-icon img {{ width:20px; height:20px; display:block; }}
.fc-brand-name {{ font-size:18px; font-weight:500; color:{TEXT}; line-height:1.2; }}
.fc-brand-tag {{ font-size:12px; color:{TEXT_MUTED}; margin-top:2px; font-weight:400; }}

.fc-section-title {{
  font-size:20px; font-weight:500; color:{TEXT};
  margin:0 0 6px 0; line-height:1.3;
}}
.fc-section-sub {{
  font-size:14px; font-weight:400; color:{TEXT_MUTED};
  margin:0 0 20px 0; line-height:1.5; max-width:60ch;
}}

.fc-card {{
  background:{SURFACE};
  border:1px solid {BORDER};
  border-radius:{RADIUS};
  padding:18px;
  margin-bottom:16px;
  box-shadow:{SHADOW};
}}
.fc-card-title {{
  font-size:16px; font-weight:500; color:{TEXT}; margin:0 0 12px 0;
}}

.fc-pill {{
  display:inline-flex; align-items:center; gap:6px;
  font-size:12px; font-weight:500; line-height:1;
  padding:6px 10px; border-radius:999px; border:1px solid transparent;
}}
.fc-chip {{
  display:inline-flex; align-items:center;
  font-size:12px; font-weight:400; color:{TEXT};
  background:#f9fafb; border:1px solid {BORDER};
  border-radius:6px; padding:5px 8px; margin:0 6px 6px 0;
}}
.fc-chip strong {{ font-weight:500; margin-right:4px; }}
strong {{ font-weight:500 !important; }}
em, i {{ font-style:normal !important; }}
h1, h2, h3, h4, h5, h6 {{ text-transform:none !important; font-style:normal !important; }}

.fc-risk-badge {{
  display:inline-flex; align-items:center;
  font-size:12px; font-weight:500;
  padding:6px 10px; border-radius:999px;
}}

.fc-footer-wrap {{
  margin-top:32px; padding-top:16px; border-top:1px solid {BORDER};
}}
.fc-footer-brand {{ font-size:14px; font-weight:500; color:{TEXT}; margin-bottom:4px; }}
.fc-footer-copy {{ font-size:12px; color:{TEXT_MUTED}; margin:0; line-height:1.5; }}

.fc-choice-card, .fc-profile-card {{
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px; padding:16px;
}}
.fc-choice-icon {{
  width:28px; height:28px; border-radius:6px; background:#f3f4f6; color:{TEXT};
  display:flex; align-items:center; justify-content:center;
  font-size:12px; font-weight:500; margin-bottom:10px; border:1px solid {BORDER};
}}
.fc-card-title {{ font-size:15px; font-weight:500; color:{TEXT}; margin-bottom:6px; }}
.fc-card-text {{ font-size:13px; color:{TEXT_MUTED}; line-height:1.5; }}
.fc-profile-name {{ font-size:14px; font-weight:500; color:{TEXT}; }}
.fc-profile-meta {{ font-size:12px; color:{TEXT_MUTED}; margin:4px 0 8px; }}
.fc-profile-desc {{ font-size:12px; color:{TEXT_MUTED}; line-height:1.45; margin-top:8px; }}
.fc-card-grid {{ display:grid; gap:12px; }}
.fc-card-grid-2 {{ grid-template-columns:repeat(2,1fr); }}
.fc-card-grid-3 {{ grid-template-columns:repeat(3,1fr); }}
.fc-process-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:8px; }}
.fc-process-step {{
  position:relative; background:{SURFACE}; border:1px solid {BORDER};
  border-radius:{RADIUS}; padding:18px 18px 18px 20px;
  box-shadow:{SHADOW}; display:flex; gap:12px; align-items:flex-start;
}}
.fc-process-step::before {{
  content:""; position:absolute; left:0; top:14px; bottom:14px; width:4px;
  border-radius:0 4px 4px 0;
}}
.fc-process-step.step-1::before {{ background:#22c55e; }}
.fc-process-step.step-2::before {{ background:#2563eb; }}
.fc-process-step.step-3::before {{ background:#8b5cf6; }}
.fc-process-badge {{
  width:28px; height:28px; border-radius:999px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-size:13px; font-weight:500; color:#fff;
}}
.fc-process-step.step-1 .fc-process-badge {{ background:#22c55e; }}
.fc-process-step.step-2 .fc-process-badge {{ background:#2563eb; }}
.fc-process-step.step-3 .fc-process-badge {{ background:#8b5cf6; }}
.fc-process-body {{ flex:1; min-width:0; }}
.fc-process-title {{ font-size:15px; font-weight:500; color:{TEXT}; margin-bottom:4px; }}
.fc-process-text {{ font-size:13px; color:{TEXT_MUTED}; line-height:1.45; }}
.fc-process-chevron {{ color:#94a3b8; font-size:18px; margin-left:auto; align-self:center; }}
.fc-process-num {{ display:none; }}
.fc-capability-grid {{ display:grid; gap:0; }}
.fc-capability {{
  display:grid; grid-template-columns:2.5rem 1fr; gap:12px;
  padding:14px 0; border-bottom:1px solid {BORDER};
}}
.fc-capability:last-child {{ border-bottom:none; }}
.fc-capability-num {{ font-size:13px; font-weight:500; color:{ACCENT}; }}
.fc-capability-title {{ font-size:14px; font-weight:500; color:{TEXT}; margin-bottom:4px; }}
.fc-capability-text {{ font-size:13px; color:{TEXT_MUTED}; line-height:1.45; }}

.fc-chip-row {{ display:flex; flex-wrap:wrap; gap:0; }}
.fc-factor-legend {{
  display:flex; gap:16px; margin:0 0 12px 0; font-size:12px; color:{TEXT_MUTED};
}}
.fc-factor-legend span {{ display:inline-flex; align-items:center; gap:6px; }}
.fc-factor-legend .swatch {{
  display:inline-block; width:12px; height:8px; border-radius:3px;
}}
.fc-factor-legend .swatch.up {{ background:#b91c1c; }}
.fc-factor-legend .swatch.down {{ background:#15803d; }}
.fc-factor-row {{
  display:grid; grid-template-columns:150px 1fr 44px; gap:10px;
  align-items:center; margin-bottom:12px;
}}
.fc-factor-label {{ font-size:13px; color:{TEXT}; font-weight:400; }}
.fc-factor-track {{
  position:relative; height:12px; background:#f3f4f6; border-radius:6px;
  overflow:hidden; border:1px solid {BORDER};
}}
.fc-factor-mid {{
  position:absolute; left:50%; top:0; bottom:0; width:1px; background:#d1d5db; z-index:1;
}}
.fc-factor-bar {{
  position:absolute; top:2px; bottom:2px; border-radius:4px; z-index:2;
}}
.fc-factor-pts {{ font-size:12px; font-weight:500; text-align:right; }}
.fc-two-col {{
  display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:8px;
}}
.fc-factor-list {{ margin:0; padding:0; list-style:none; }}
.fc-factor-list li {{
  font-size:13px; color:{TEXT}; line-height:1.45;
  padding:8px 0; border-bottom:1px solid {BORDER};
}}
.fc-factor-list li:last-child {{ border-bottom:none; }}
.fc-factor-list .hint {{ color:{TEXT_MUTED}; display:block; margin-top:2px; font-size:12px; }}

@media (max-width:768px) {{
  .fc-card-grid-2, .fc-card-grid-3, .fc-process-row, .fc-two-col {{ grid-template-columns:1fr !important; }}
  .fc-factor-row {{ grid-template-columns:1fr !important; gap:4px !important; }}
}}
"""

THEME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap');

:root {{
  --fc-page:{PAGE_BG};
  --fc-surface:{SURFACE};
  --fc-border:{BORDER};
  --fc-text:{TEXT};
  --fc-muted:{TEXT_MUTED};
  --fc-accent:{ACCENT};
}}

html, body, [class*="css"] {{
  font-family:'IBM Plex Sans', 'Segoe UI', sans-serif !important;
  color:{TEXT};
  font-weight:400;
}}
.stApp {{
  background:
    radial-gradient(ellipse 40% 30% at 0% 0%, rgba(37,99,235,0.08), transparent 60%),
    radial-gradient(ellipse 35% 28% at 100% 100%, rgba(34,197,94,0.07), transparent 55%),
    linear-gradient(180deg, #eef3fb 0%, #f8fafc 55%, #eef3fb 100%) !important;
}}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {{
  display:none !important;
}}

/* Full-bleed: no side gutters */
.stAppViewContainer .main .block-container,
.block-container {{
  padding-top: 12px !important;
  padding-bottom: 48px !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
  max-width: 100% !important;
}}
section.main > div {{ max-width: 100% !important; }}

{_SHARED}

/* Header shell — mockup top bar */
.fc-topbar {{
  display:flex; justify-content:space-between; align-items:center;
  gap:16px; flex-wrap:wrap;
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:{RADIUS};
  padding:14px 18px; margin-bottom:12px; box-shadow:{SHADOW};
}}
.fc-topbar-right {{ display:flex; align-items:center; gap:10px; }}
.fc-motto-chip {{
  display:inline-flex; align-items:center; gap:8px;
  background:#f8fafc; border:1px solid {BORDER}; border-radius:999px;
  padding:8px 14px; font-size:12px; font-weight:500; color:{TEXT};
}}
.fc-motto-chip .leaf {{ color:#22c55e; font-size:14px; }}
.fc-theme-btn {{
  width:40px; height:40px; border-radius:999px; border:1px solid {BORDER};
  background:{SURFACE}; display:flex; align-items:center; justify-content:center;
  color:#f59e0b; font-size:16px; box-shadow:{SHADOW};
}}

.fc-header-shell {{ display:none; }}
.fc-nav-row-marker {{ display:none !important; height:0 !important; margin:0 !important; }}

/* Welcome nav pills — full width row */
div.element-container:has(.fc-nav-row-marker) + div.element-container div[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
  background:transparent !important;
  border:none !important;
  padding:0 !important;
  margin:0 0 16px 0 !important;
  gap:12px !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {{
  border-radius:999px !important;
  min-height:48px !important;
  font-size:15px !important;
  box-shadow:{SHADOW} !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="secondary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] {{
  background:{SURFACE} !important;
  border:1px solid {BORDER} !important;
  color:{TEXT} !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="primary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="primary"] {{
  background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
  border-color:transparent !important;
  color:#fff !important;
}}
/* Active Home-style nav (data-testid via key not available) — style first secondary as soft blue when welcome */
div.element-container:has(.fc-nav-active-marker) + div.element-container div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {{
  background:#eff6ff !important;
  border-color:#bfdbfe !important;
  color:{ACCENT} !important;
}}
.fc-nav-active-marker {{ display:none !important; height:0 !important; margin:0 !important; }}

/* Hero — mockup banner */
.fc-hero {{
  position:relative; overflow:hidden; border-radius:{RADIUS};
  min-height:min(48vh, 420px); margin:0 0 16px 0;
  display:flex; align-items:stretch; isolation:isolate;
  border:1px solid {BORDER}; box-shadow:{SHADOW};
}}
.fc-hero-media, .fc-hero-fallback {{ position:absolute; inset:0; background:#1e293b; z-index:0; }}
.fc-hero-img {{ width:100%; height:100%; object-fit:cover; object-position:center 40%; display:block; }}
.fc-hero-veil {{
  position:absolute; inset:0; z-index:1;
  background:linear-gradient(100deg, rgba(15,23,42,0.88) 0%, rgba(15,23,42,0.55) 42%, rgba(15,23,42,0.12) 72%, transparent 100%);
}}
.fc-hero-body {{
  position:relative; z-index:2; padding:36px 32px 28px;
  max-width:min(36rem, 92%); display:flex; flex-direction:column; justify-content:flex-end;
}}
.fc-hero-badge {{
  display:inline-flex; align-items:center; gap:6px; align-self:flex-start;
  background:#dcfce7; color:#15803d; border:1px solid #bbf7d0;
  border-radius:999px; padding:6px 12px; font-size:12px; font-weight:500; margin-bottom:14px;
}}
.fc-hero-brand {{
  font-size:clamp(28px, 4vw, 40px); font-weight:500; color:#fff; margin:0 0 10px 0; line-height:1.15;
}}
.fc-hero-sub {{
  margin:0 0 22px; color:rgba(255,255,255,0.9); font-size:15px; line-height:1.55; font-weight:400;
  max-width:34ch;
}}
.fc-hero-features {{
  display:flex; flex-wrap:wrap; gap:18px 22px; margin-top:auto;
}}
.fc-hero-feat {{
  display:inline-flex; align-items:center; gap:8px;
  color:rgba(255,255,255,0.92); font-size:13px; font-weight:500;
}}
.fc-hero-feat .dot {{
  width:8px; height:8px; border-radius:999px; background:#4ade80; flex-shrink:0;
}}
.fc-hero-actions {{ margin:0 0 18px; width:100%; }}
div.element-container:has(.fc-hero-actions-marker) + div.element-container .stButton > button,
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-hero-actions-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {{
  min-height:56px !important;
  border-radius:16px !important;
  font-size:16px !important;
  box-shadow:{SHADOW} !important;
}}
.fc-hero-actions-marker {{ display:none !important; height:0 !important; margin:0 !important; }}

/* Step progress */
.fc-steps {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 16px; }}
.fc-step-pill {{
  font-size:12px; font-weight:500; color:{TEXT_MUTED};
  background:{SURFACE}; border:1px solid {BORDER};
  border-radius:999px; padding:6px 10px;
}}
.fc-step-pill.is-active {{ color:{ACCENT}; border-color:#bfdbfe; background:#eff6ff; }}
.fc-step-pill.is-done {{ color:{TEXT}; }}

/* Results layout */
.fc-result-header {{
  display:flex; justify-content:space-between; align-items:flex-start;
  gap:16px; flex-wrap:wrap;
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
  padding:18px; margin-bottom:12px;
}}
.fc-result-identity {{ display:flex; gap:12px; align-items:center; min-width:0; }}
.fc-avatar {{
  width:44px; height:44px; border-radius:999px; background:#eff6ff; color:{ACCENT};
  display:flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:500; border:1px solid #dbeafe; flex-shrink:0;
}}
.fc-result-name {{ font-size:18px; font-weight:500; color:{TEXT}; margin:0 0 4px; }}
.fc-result-meta {{ font-size:13px; color:{TEXT_MUTED}; margin:0; }}
.fc-result-score-block {{ text-align:right; }}
.fc-result-score-label {{ font-size:12px; color:{TEXT_MUTED}; margin:0 0 4px; }}
.fc-result-score-value {{ font-size:28px; font-weight:500; line-height:1; margin:0; }}
.fc-result-score-sub {{ font-size:12px; color:{TEXT_MUTED}; margin:6px 0 0; }}

.fc-pill-row {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 16px; }}

.fc-metric-grid {{
  display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:16px;
}}
.fc-metric-card {{
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px; padding:16px;
}}
.fc-metric-label {{ font-size:12px; color:{TEXT_MUTED}; margin:0 0 6px; font-weight:400; }}
.fc-metric-value {{ font-size:20px; font-weight:500; color:{TEXT}; margin:0; }}
.fc-metric-hint {{ font-size:12px; color:{TEXT_MUTED}; margin:6px 0 0; }}

.fc-form-section {{
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
  padding:18px; margin-bottom:16px;
}}
.fc-form-section-title {{
  font-size:15px; font-weight:500; color:{TEXT}; margin:0 0 12px 0;
}}

.fc-bank-panel {{
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
  padding:16px; margin-bottom:16px;
}}

/* Match Streamlit bordered containers to card system */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
  background:{SURFACE} !important;
  border:1px solid {BORDER} !important;
  border-radius:12px !important;
  box-shadow:none !important;
}}
div[data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] {{
  margin-bottom:16px !important;
}}
div[data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] > div {{
  padding:16px 18px !important;
}}

/* Widgets */
.stButton > button {{
  border-radius:16px !important;
  font-family:'IBM Plex Sans', sans-serif !important;
  font-weight:500 !important;
  font-size:14px !important;
  padding:10px 16px !important;
  border:1px solid {BORDER} !important;
  box-shadow:{SHADOW} !important;
}}
.stButton > button[kind="primary"] {{
  background:{ACCENT} !important;
  border-color:{ACCENT} !important;
  color:#fff !important;
}}
.stButton > button[kind="primary"]:hover {{
  background:{ACCENT_HOVER} !important;
  border-color:{ACCENT_HOVER} !important;
}}
.stButton > button[kind="secondary"]:hover {{
  background:#f9fafb !important;
  border-color:#d1d5db !important;
}}
div[data-testid="stForm"] {{
  background:transparent; border:none; padding:0;
}}
[data-testid="stMetric"] {{
  background:{SURFACE};
  border:1px solid {BORDER};
  border-radius:12px;
  padding:12px 14px;
}}
[data-testid="stMetricLabel"] {{
  color:{TEXT_MUTED} !important;
  font-weight:400 !important;
  font-size:12px !important;
}}
[data-testid="stMetricValue"] {{
  color:{TEXT} !important;
  font-weight:500 !important;
  font-size:20px !important;
}}
[data-testid="stDataFrame"] {{
  border:1px solid {BORDER};
  border-radius:12px;
  overflow:hidden;
}}
hr {{ display:none !important; }}

@media (max-width:768px) {{
  .fc-metric-grid {{ grid-template-columns:1fr !important; }}
  .fc-result-score-block {{ text-align:left !important; }}
  .fc-hero {{ min-height:min(36vh, 280px) !important; }}
}}
"""

HTML_IFRAME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap');
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:0; font-family:'IBM Plex Sans', sans-serif; color:{TEXT}; font-weight:400; background:transparent; }}
{_SHARED}
.fc-topbar {{
  display:flex; justify-content:space-between; align-items:center;
  gap:16px; flex-wrap:wrap;
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:{RADIUS};
  padding:14px 18px; margin:0; box-shadow:{SHADOW};
}}
.fc-topbar-right {{ display:flex; align-items:center; gap:10px; }}
.fc-motto-chip {{
  display:inline-flex; align-items:center; gap:8px;
  background:#f8fafc; border:1px solid {BORDER}; border-radius:999px;
  padding:8px 14px; font-size:12px; font-weight:500; color:{TEXT};
}}
.fc-motto-chip .leaf {{ color:#22c55e; font-size:14px; }}
.fc-theme-btn {{
  width:40px; height:40px; border-radius:999px; border:1px solid {BORDER};
  background:{SURFACE}; display:flex; align-items:center; justify-content:center;
  color:#f59e0b; font-size:16px; box-shadow:{SHADOW};
}}
.fc-hero {{
  position:relative; overflow:hidden; border-radius:{RADIUS};
  min-height:400px; height:400px; margin:0;
  display:flex; align-items:stretch; isolation:isolate;
  border:1px solid {BORDER}; box-shadow:{SHADOW};
}}
.fc-hero-media, .fc-hero-fallback {{ position:absolute; inset:0; background:#1e293b; z-index:0; }}
.fc-hero-img {{ width:100%; height:100%; object-fit:cover; object-position:center 40%; display:block; }}
.fc-hero-veil {{
  position:absolute; inset:0; z-index:1;
  background:linear-gradient(100deg, rgba(15,23,42,0.88) 0%, rgba(15,23,42,0.55) 42%, rgba(15,23,42,0.12) 72%, transparent 100%);
}}
.fc-hero-body {{
  position:relative; z-index:2; padding:36px 32px 28px;
  max-width:min(36rem, 92%); display:flex; flex-direction:column; justify-content:flex-end;
  height:100%;
}}
.fc-hero-badge {{
  display:inline-flex; align-items:center; gap:6px; align-self:flex-start;
  background:#dcfce7; color:#15803d; border:1px solid #bbf7d0;
  border-radius:999px; padding:6px 12px; font-size:12px; font-weight:500; margin-bottom:14px;
}}
.fc-hero-brand {{
  font-size:clamp(28px, 4vw, 40px); font-weight:500; color:#fff; margin:0 0 10px 0; line-height:1.15;
}}
.fc-hero-sub {{
  margin:0 0 22px; color:rgba(255,255,255,0.9); font-size:15px; line-height:1.55; font-weight:400;
  max-width:34ch;
}}
.fc-hero-features {{ display:flex; flex-wrap:wrap; gap:18px 22px; margin-top:auto; }}
.fc-hero-feat {{
  display:inline-flex; align-items:center; gap:8px;
  color:rgba(255,255,255,0.92); font-size:13px; font-weight:500;
}}
.fc-hero-feat .dot {{
  width:8px; height:8px; border-radius:999px; background:#4ade80; flex-shrink:0;
}}
.fc-result-header {{
  display:flex; justify-content:space-between; align-items:flex-start;
  gap:16px; flex-wrap:wrap; background:{SURFACE}; border:1px solid {BORDER};
  border-radius:{RADIUS}; padding:18px; margin-bottom:0; box-shadow:{SHADOW};
}}
.fc-result-identity {{ display:flex; gap:12px; align-items:center; }}
.fc-avatar {{
  width:44px; height:44px; border-radius:999px; background:#eff6ff; color:{ACCENT};
  display:flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:500; border:1px solid #dbeafe;
}}
.fc-result-name {{ font-size:18px; font-weight:500; color:{TEXT}; margin:0 0 4px; }}
.fc-result-meta {{ font-size:13px; color:{TEXT_MUTED}; margin:0; }}
.fc-result-score-block {{ text-align:right; }}
.fc-result-score-label {{ font-size:12px; color:{TEXT_MUTED}; margin:0 0 4px; }}
.fc-result-score-value {{ font-size:28px; font-weight:500; line-height:1; margin:0; }}
.fc-result-score-sub {{ font-size:12px; color:{TEXT_MUTED}; margin:6px 0 0; }}
.fc-pill-row {{ display:flex; flex-wrap:wrap; gap:8px; margin:0; }}
.fc-metric-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
.fc-metric-card {{ background:#f9fafb; border:1px solid {BORDER}; border-radius:12px; padding:16px; }}
.fc-metric-label {{ font-size:12px; color:{TEXT_MUTED}; margin:0 0 6px; }}
.fc-metric-value {{ font-size:20px; font-weight:500; color:{TEXT}; margin:0; }}
.fc-metric-hint {{ font-size:12px; color:{TEXT_MUTED}; margin:6px 0 0; }}
@media (max-width:768px) {{
  .fc-metric-grid {{ grid-template-columns:1fr !important; }}
  .fc-result-score-block {{ text-align:left !important; }}
  .fc-hero {{ min-height:320px; height:320px; }}
  .fc-hero-body {{ padding:24px 18px; }}
}}
"""


def apply_theme() -> None:
    st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)


def brand_icon_html(*, size: str = "sm") -> str:
    return (
        f'<div class="fc-brand-icon">'
        f'<img src="{BRAND_LEAF_ICON_URI}" alt="" width="20" height="20" />'
        f"</div>"
    )


def brand_html(*, subtitle: str = "Credit Guidance for Farmers", shell: bool = False) -> str:
    """Top brand mark. shell=True includes motto chip (welcome mockup top bar)."""
    brand = f"""
    <div class="fc-brand">
      {brand_icon_html()}
      <div>
        <div class="fc-brand-name">FarmCredit AI</div>
        <div class="fc-brand-tag">{html.escape(subtitle)}</div>
      </div>
    </div>
    """
    if shell:
        return f"""
        <div class="fc-topbar">
          {brand}
          <div class="fc-topbar-right">
            <div class="fc-motto-chip">
              <img src="{BRAND_LEAF_ICON_URI}" alt="" width="14" height="14" style="filter:hue-rotate(90deg);" />
              Stronger Farmers, Brighter Tomorrow
            </div>
            <div class="fc-theme-btn" title="Theme" aria-hidden="true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="12" r="4" fill="#f59e0b"/>
                <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/>
              </svg>
            </div>
          </div>
        </div>
        """
    return brand


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
    order = ["choose", "input", "results"]
    labels = {"choose": "1 · Path", "input": "2 · Details", "results": "3 · Result"}
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


def status_pill_html(label: str, *, kind: str = "neutral") -> str:
    """kind: risk-Low/Medium/High/Critical | source | neutral"""
    if kind.startswith("risk-"):
        level = kind.replace("risk-", "")
        fg, bg = RISK_STYLES.get(level, (TEXT_MUTED, "#f3f4f6"))
        return (
            f'<span class="fc-pill" style="color:{fg};background:{bg};border-color:{fg}33;">'
            f"{html.escape(label)}</span>"
        )
    if kind == "source":
        return (
            f'<span class="fc-pill" style="color:{ACCENT};background:#eff6ff;border-color:#bfdbfe;">'
            f"{html.escape(label)}</span>"
        )
    return (
        f'<span class="fc-pill" style="color:{TEXT_MUTED};background:#f9fafb;border-color:{BORDER};">'
        f"{html.escape(label)}</span>"
    )


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
