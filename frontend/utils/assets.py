"""Static asset helpers for Streamlit UI."""

from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
HERO_BG_PATH = ASSETS_DIR / "hero-bg.png"


@lru_cache(maxsize=4)
def image_data_uri(path: str | Path, *, mime: str = "image/png") -> str:
    file_path = Path(path)
    if not file_path.is_file():
        return ""
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def hero_bg_data_uri() -> str:
    return image_data_uri(HERO_BG_PATH)
