"""FarmCredit AI design system — clean neutral UI, risk colors only for risk."""

from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

# ── Palette ───────────────────────────────────────────────────────────────────
PAGE_BG = "#f3f4f6"
SURFACE = "#ffffff"
BORDER = "#e5e7eb"
TEXT = "#111827"
TEXT_MUTED = "#6b7280"
ACCENT = "#2563eb"
ACCENT_HOVER = "#1d4ed8"

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
  border-radius:12px;
  padding:18px;
  margin-bottom:16px;
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
.fc-process-step {{ background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px; padding:16px; }}
.fc-process-num {{ font-size:13px; font-weight:500; color:{ACCENT}; margin-bottom:6px; }}
.fc-process-title {{ font-size:14px; font-weight:500; color:{TEXT}; margin-bottom:4px; }}
.fc-process-text {{ font-size:13px; color:{TEXT_MUTED}; line-height:1.45; }}
.fc-capability-grid {{ display:grid; gap:0; }}
.fc-capability {{
  display:grid; grid-template-columns:2.5rem 1fr; gap:12px;
  padding:14px 0; border-bottom:1px solid {BORDER};
}}
.fc-capability:last-child {{ border-bottom:none; }}
.fc-capability-num {{ font-size:13px; font-weight:500; color:{ACCENT}; }}
.fc-capability-title {{ font-size:14px; font-weight:500; color:{TEXT}; margin-bottom:4px; }}
.fc-capability-text {{ font-size:13px; color:{TEXT_MUTED}; line-height:1.45; }}

@media (max-width:768px) {{
  .fc-card-grid-2, .fc-card-grid-3, .fc-process-row {{ grid-template-columns:1fr !important; }}
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
.stApp {{ background:{PAGE_BG} !important; }}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] {{
  display:none !important;
}}

.stAppViewContainer .main .block-container,
.block-container {{
  padding-top:12px;
  padding-bottom:40px;
  max-width:1040px;
}}

{_SHARED}

/* Header shell */
.fc-header-shell {{
  background:{SURFACE};
  border:1px solid {BORDER};
  border-bottom:none;
  border-radius:12px 12px 0 0;
  padding:14px 16px 0;
}}
.fc-header-shell .fc-brand {{
  padding-bottom:12px;
  border-bottom:1px solid {BORDER};
}}
div[data-testid="stMarkdownContainer"]:has(.fc-header-shell) {{ margin-bottom:0 !important; }}
.fc-nav-row-marker {{ display:none !important; height:0 !important; margin:0 !important; }}

div.element-container:has(.fc-nav-row-marker) + div.element-container div[data-testid="stHorizontalBlock"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
  background:{SURFACE};
  border:1px solid {BORDER};
  border-top:none;
  border-radius:0 0 12px 12px;
  padding:8px 12px 10px;
  margin-top:-6px;
  margin-bottom:24px;
  align-items:center !important;
  gap:8px !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="secondary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] {{
  background:transparent !important;
  border-color:transparent !important;
  box-shadow:none !important;
  color:{TEXT} !important;
  font-weight:500 !important;
}}
div.element-container:has(.fc-nav-row-marker) + div.element-container .stButton > button[kind="primary"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.fc-nav-row-marker) + [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="primary"] {{
  background:{ACCENT} !important;
  border-color:{ACCENT} !important;
}}

/* Hero */
.fc-hero {{
  position:relative; overflow:hidden; border-radius:12px;
  min-height:min(42vh, 360px); margin:0 0 16px 0;
  display:flex; align-items:flex-end; isolation:isolate;
  border:1px solid {BORDER};
}}
.fc-hero-media, .fc-hero-fallback {{ position:absolute; inset:0; background:#1f2937; z-index:0; }}
.fc-hero-img {{ width:100%; height:100%; object-fit:cover; object-position:center 40%; display:block; }}
.fc-hero-veil {{
  position:absolute; inset:0; z-index:1;
  background:linear-gradient(105deg, rgba(17,24,39,0.82) 0%, rgba(17,24,39,0.45) 55%, rgba(17,24,39,0.15) 100%);
}}
.fc-hero-body {{ position:relative; z-index:2; padding:24px 20px; max-width:34rem; }}
.fc-hero-brand {{
  font-size:22px; font-weight:500; color:#fff; margin:0 0 8px 0; line-height:1.2;
}}
.fc-hero-sub {{ margin:0; color:rgba(255,255,255,0.88); font-size:15px; line-height:1.5; font-weight:400; }}
.fc-hero-actions {{ margin:0 0 24px; max-width:28rem; }}

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

.fc-factor-row {{
  display:grid; grid-template-columns:140px 1fr 48px; gap:10px;
  align-items:center; margin-bottom:10px;
}}
.fc-factor-label {{ font-size:13px; color:{TEXT}; font-weight:400; }}
.fc-factor-track {{
  position:relative; height:10px; background:#f3f4f6; border-radius:6px; overflow:hidden;
  border:1px solid {BORDER};
}}
.fc-factor-mid {{
  position:absolute; left:50%; top:0; bottom:0; width:1px; background:#d1d5db;
}}
.fc-factor-bar {{
  position:absolute; top:1px; bottom:1px; border-radius:4px; height:calc(100% - 2px);
}}
.fc-factor-bar.up {{ background:#b91c1c; }}
.fc-factor-bar.down {{ background:#15803d; }}
.fc-factor-pts {{ font-size:12px; font-weight:500; text-align:right; }}

.fc-two-col {{
  display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;
}}
.fc-factor-list {{ margin:0; padding:0; list-style:none; }}
.fc-factor-list li {{
  font-size:13px; color:{TEXT}; line-height:1.45;
  padding:8px 0; border-bottom:1px solid {BORDER};
}}
.fc-factor-list li:last-child {{ border-bottom:none; }}
.fc-factor-list .hint {{ color:{TEXT_MUTED}; display:block; margin-top:2px; font-size:12px; }}

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
  border-radius:8px !important;
  font-family:'IBM Plex Sans', sans-serif !important;
  font-weight:500 !important;
  font-size:14px !important;
  padding:8px 14px !important;
  border:1px solid {BORDER} !important;
  box-shadow:none !important;
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
  .fc-metric-grid, .fc-two-col {{ grid-template-columns:1fr !important; }}
  .fc-factor-row {{ grid-template-columns:1fr !important; gap:4px !important; }}
  .fc-result-score-block {{ text-align:left !important; }}
  .fc-hero {{ min-height:min(36vh, 280px) !important; }}
}}
"""

HTML_IFRAME_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap');
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:'IBM Plex Sans', sans-serif; color:{TEXT}; font-weight:400; }}
{_SHARED}
.fc-result-header {{
  display:flex; justify-content:space-between; align-items:flex-start;
  gap:16px; flex-wrap:wrap; background:{SURFACE}; border:1px solid {BORDER};
  border-radius:12px; padding:18px; margin-bottom:12px;
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
.fc-pill-row {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 16px; }}
.fc-metric-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:16px; }}
.fc-metric-card {{ background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px; padding:16px; }}
.fc-metric-label {{ font-size:12px; color:{TEXT_MUTED}; margin:0 0 6px; }}
.fc-metric-value {{ font-size:20px; font-weight:500; color:{TEXT}; margin:0; }}
.fc-metric-hint {{ font-size:12px; color:{TEXT_MUTED}; margin:6px 0 0; }}
.fc-factor-row {{
  display:grid; grid-template-columns:140px 1fr 48px; gap:10px;
  align-items:center; margin-bottom:10px;
}}
.fc-factor-label {{ font-size:13px; color:{TEXT}; }}
.fc-factor-track {{
  position:relative; height:10px; background:#f3f4f6; border-radius:6px;
  overflow:hidden; border:1px solid {BORDER};
}}
.fc-factor-mid {{ position:absolute; left:50%; top:0; bottom:0; width:1px; background:#d1d5db; }}
.fc-factor-bar {{ position:absolute; top:1px; bottom:1px; border-radius:4px; }}
.fc-factor-pts {{ font-size:12px; font-weight:500; text-align:right; }}
.fc-two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px; }}
.fc-factor-list {{ margin:0; padding:0; list-style:none; }}
.fc-factor-list li {{
  font-size:13px; color:{TEXT}; line-height:1.45;
  padding:8px 0; border-bottom:1px solid {BORDER};
}}
.fc-factor-list li:last-child {{ border-bottom:none; }}
.fc-factor-list .hint {{ color:{TEXT_MUTED}; display:block; margin-top:2px; font-size:12px; }}
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
