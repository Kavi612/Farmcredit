"""End-to-end API test runner for FarmCredit AI."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

BASE = "http://127.0.0.1:8000"
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "ml" / "artifacts" / "reports" / "e2e"


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def ok(msg: str) -> None:
    print(f"  [PASS] {msg}")


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    errors = 0

    section("STEP 1 — /health")
    try:
        r = requests.get(f"{BASE}/health", timeout=10)
        h = r.json()
        print(json.dumps(h, indent=2))
        if h.get("xgb_loaded") and h.get("shap_ready"):
            ok("XGBoost + SHAP loaded")
        else:
            fail("Model not fully loaded")
            errors += 1
        llm_on = h.get("llm_enabled")
        llm_loaded = h.get("llm_loaded")
        print(f"  LLM enabled={llm_on}  loaded={llm_loaded}")
    except Exception as exc:  # noqa: BLE001
        fail(f"Backend not reachable: {exc}")
        return 1

    section("STEP 2 — Demo farmers DEMO-01..05")
    expected = {
        "DEMO-01": "Low",
        "DEMO-02": "Medium",
        "DEMO-03": "High",
        "DEMO-04": "Critical",
        "DEMO-05": "Medium",
    }
    scores = {}
    for fid, exp in expected.items():
        r = requests.get(f"{BASE}/demo-farmers/{fid}", timeout=20)
        if r.status_code != 200:
            fail(f"{fid} HTTP {r.status_code}")
            errors += 1
            continue
        d = r.json()
        pred = d.get("prediction") or {}
        expl = d.get("explanation") or {}
        level = pred.get("risk_level")
        score = pred.get("risk_score")
        scores[fid] = score
        factors = expl.get("top_factors") or pred.get("top_factors") or []
        advisory = d.get("advisory_text") or ""
        print(f"\n  {fid} | expected={exp} actual={level} score={score:.4f}")
        print(f"    SHAP factors: {len(factors)} | advisory chars: {len(advisory)}")
        if factors:
            top = factors[0]
            print(f"    top factor: {top.get('display_label')} ({top.get('points'):+d} pts)")
        if level != exp:
            fail(f"{fid} band mismatch (expected {exp}, got {level})")
            errors += 1
        elif len(factors) < 3 or not advisory:
            fail(f"{fid} missing SHAP or advisory")
            errors += 1
        else:
            ok(f"{fid} consistent")

    if scores.get("DEMO-04", 0) <= scores.get("DEMO-01", 1):
        fail("Score ordering: DEMO-04 should exceed DEMO-01")
        errors += 1
    else:
        ok("Risk score ordering DEMO-04 > DEMO-01")

    section("STEP 3 — Custom farmer live /assess")
    custom = {
        "features": {
            "state": "KA",
            "district": "KA-North",
            "crop_type": "Rice",
            "season": "Kharif",
            "land_size_ha": 2.0,
            "soil_type": "Red",
            "rainfall_mm": 1100,
            "irrigation_type": "Canal",
            "loan_amount_inr": 150000,
            "prior_loan_count": 1,
            "prior_default_flag": 0,
            "repayment_score": 75,
            "annual_income_inr": 280000,
            "existing_debt_inr": 30000,
        },
        "use_demo_cache": False,
        "use_live_llm": False,
        "include_advisory": True,
    }
    t0 = time.perf_counter()
    r = requests.post(f"{BASE}/assess", json=custom, timeout=60)
    elapsed = time.perf_counter() - t0
    if r.status_code != 200:
        fail(f"/assess custom HTTP {r.status_code}: {r.text[:200]}")
        errors += 1
    else:
        a = r.json()
        print(f"  cached={a.get('cached')} level={a.get('risk_level')} score={a.get('risk_score'):.4f} ({elapsed:.2f}s)")
        if a.get("cached"):
            fail("Custom assess should not be cached")
            errors += 1
        else:
            ok("Live XGBoost + SHAP (not cached)")
        for f in (a.get("top_factors") or [])[:3]:
            print(f"    {f.get('display_label')}: {f.get('plain_hint')} ({f.get('points'):+d})")
        custom_features = custom["features"]

    section("STEP 4 — Live LLM (optional)")
    print("  Skipping automatic LLM load unless backend already has llm_enabled=true + HF_TOKEN.")
    print("  (See manual LLM subsection in test report.)")

    section("STEP 5 — PDF generation")
    for label, body in [
        ("demo", {"farmer_id": "DEMO-03", "use_demo_cache": True}),
        ("custom", {"features": custom["features"], "use_demo_cache": False}),
    ]:
        r = requests.post(f"{BASE}/generate-report/pdf", json=body, timeout=60)
        if r.status_code != 200 or r.headers.get("content-type", "").startswith("application/pdf") is False:
            fail(f"PDF {label} HTTP {r.status_code}")
            errors += 1
            continue
        path = OUT / f"report_{label}.pdf"
        path.write_bytes(r.content)
        ok(f"PDF {label} -> {path} ({len(r.content)} bytes)")

    section("STEP 6 — Frontend API paths (Streamlit uses same calls)")
    demos = requests.get(f"{BASE}/demo-farmers", timeout=15).json()
    ok(f"GET /demo-farmers -> {len(demos)} summaries")
    portfolio_path = REPO / "frontend" / "data" / "officer_portfolio.json"
    if portfolio_path.exists():
        n = len(json.loads(portfolio_path.read_text())["applications"])
        ok(f"Officer portfolio JSON present ({n} rows) — dashboard loads locally")
    else:
        warn("officer_portfolio.json missing")

    section("STEP 7 — Error handling")
    bad422 = {
        "features": {
            "state": "MH",
            "district": "MH-Vidarbha",
            "crop_type": "Banana",
            "season": "Kharif",
            "land_size_ha": 1.0,
            "soil_type": "Black",
            "rainfall_mm": 5000,
            "irrigation_type": "Rainfed",
            "loan_amount_inr": 100000,
            "prior_loan_count": 0,
            "prior_default_flag": 0,
            "repayment_score": 50,
            "annual_income_inr": 100000,
            "existing_debt_inr": 0,
        }
    }
    r = requests.post(f"{BASE}/predict-risk", json=bad422["features"], timeout=15)
    if r.status_code == 422:
        ok(f"Invalid crop/rainfall -> 422: {str(r.json())[:120]}...")
    else:
        fail(f"Expected 422, got {r.status_code}")
        errors += 1

    r = requests.get(f"{BASE}/demo-farmers/DOES-NOT-EXIST", timeout=15)
    if r.status_code == 404:
        ok(f"Unknown farmer_id -> 404: {r.json()}")
    else:
        fail(f"Expected 404, got {r.status_code}")
        errors += 1

    print("\n" + "=" * 72)
    if errors:
        print(f"DONE with {errors} failure(s)")
        return 1
    print("ALL AUTOMATED API TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
