"""HTTP client for the FarmCredit FastAPI backend."""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class ApiError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def get_base_url() -> str:
    """Resolve API URL: Streamlit secrets → env var → local default."""
    # Streamlit Cloud secrets (Settings → Secrets)
    try:
        import streamlit as st

        secret = st.secrets.get("FARMCREDIT_API_URL")
        if secret:
            return str(secret).rstrip("/")
    except Exception:  # noqa: BLE001 — no streamlit / no secrets file locally
        pass

    return os.getenv("FARMCREDIT_API_URL", DEFAULT_BASE_URL).rstrip("/")


def _raise_for_response(response: requests.Response) -> None:
    if response.ok:
        return
    detail: Any
    try:
        payload = response.json()
        detail = payload.get("detail") or payload.get("error") or payload
    except Exception:  # noqa: BLE001
        detail = response.text or response.reason
    raise ApiError(str(detail), status_code=response.status_code)


def _request(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    timeout: float = 60.0,
) -> Any:
    url = f"{get_base_url()}{path}"
    try:
        response = requests.request(method, url, json=json, timeout=timeout)
    except requests.ConnectionError as exc:
        raise ApiError(
            f"Cannot reach the FarmCredit API at {get_base_url()}. "
            "Start the backend with: python -m uvicorn backend.app.main:app --port 8000"
        ) from exc
    except requests.Timeout as exc:
        raise ApiError("The API took too long to respond. Try demo mode or disable live LLM.") from exc
    _raise_for_response(response)
    return response.json()


def health() -> dict[str, Any]:
    return _request("GET", "/health", timeout=10.0)


def list_demo_farmers() -> list[dict[str, Any]]:
    return _request("GET", "/demo-farmers", timeout=15.0)


def get_demo_farmer(farmer_id: str) -> dict[str, Any]:
    return _request("GET", f"/demo-farmers/{farmer_id}", timeout=20.0)


def assess(
    *,
    features: dict[str, Any] | None = None,
    farmer_id: str | None = None,
    use_demo_cache: bool | None = True,
    use_live_llm: bool = False,
    include_advisory: bool = True,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "use_live_llm": use_live_llm,
        "include_advisory": include_advisory,
    }
    if use_demo_cache is not None:
        body["use_demo_cache"] = use_demo_cache
    if farmer_id:
        body["farmer_id"] = farmer_id
    if features:
        body["features"] = features
    timeout = 120.0 if use_live_llm else 60.0
    return _request("POST", "/assess", json=body, timeout=timeout)


def generate_report(
    *,
    features: dict[str, Any] | None = None,
    farmer_id: str | None = None,
    use_demo_cache: bool = True,
    use_live_llm: bool = False,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "use_demo_cache": use_demo_cache,
        "use_live_llm": use_live_llm,
        "include_advisory": True,
    }
    if farmer_id:
        body["farmer_id"] = farmer_id
    if features:
        body["features"] = features
    return _request("POST", "/generate-report", json=body, timeout=60.0)


def predict_risk(features: dict[str, Any], include_shap: bool = False) -> dict[str, Any]:
    body = {**features, "include_shap": include_shap}
    return _request("POST", "/predict-risk", json=body, timeout=30.0)


def generate_report_pdf(
    *,
    features: dict[str, Any] | None = None,
    farmer_id: str | None = None,
    use_demo_cache: bool = True,
    use_live_llm: bool = False,
) -> tuple[bytes, str]:
    body: dict[str, Any] = {
        "use_demo_cache": use_demo_cache,
        "use_live_llm": use_live_llm,
        "include_advisory": True,
    }
    if farmer_id:
        body["farmer_id"] = farmer_id
    if features:
        body["features"] = features
    url = f"{get_base_url()}/generate-report/pdf"
    try:
        response = requests.post(url, json=body, timeout=60.0)
    except requests.ConnectionError as exc:
        raise ApiError(
            f"Cannot reach the FarmCredit API at {get_base_url()}. "
            "Start the backend with: python -m uvicorn backend.app.main:app --port 8000"
        ) from exc
    except requests.Timeout as exc:
        raise ApiError("PDF generation timed out.") from exc
    _raise_for_response(response)
    cd = response.headers.get("Content-Disposition", "")
    filename = "farmcredit_report.pdf"
    if "filename=" in cd:
        filename = cd.split("filename=")[-1].strip('"')
    return response.content, filename
