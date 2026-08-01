"""Score demo farmers with XGBoost + SHAP and write backend demo_cache JSON."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.ml.risk_model import RiskModel
from backend.app.ml.shap_explainer import ShapExplainer

DEMO_PATH = REPO_ROOT / "backend" / "app" / "data" / "demo_farmers.json"
CACHE_DIR = REPO_ROOT / "backend" / "app" / "data" / "demo_cache"


def _template_advisory(name: str, level: str, top_factors: list[dict]) -> str:
    drivers = [
        f["plain_hint"]
        for f in top_factors
        if f["direction"] == "increases_risk"
    ][:3]
    helpers = [
        f["plain_hint"]
        for f in top_factors
        if f["direction"] == "decreases_risk"
    ][:2]
    driver_txt = "; ".join(drivers) if drivers else "Overall credit and climate balance."
    help_txt = "; ".join(helpers) if helpers else "Keep using practices that protect income."
    return (
        f"Namaste {name}. Your FarmCredit risk level is {level}. "
        f"Main pressure points: {driver_txt}. "
        f"What is helping: {help_txt}. "
        f"Next steps: match crop and irrigation to local rainfall, keep loan size "
        f"close to expected income, and ask your bank/CSC about KCC, PM-KISAN, and "
        f"PMFBY eligibility. Figures here are indicative for this demo — confirm locally."
    )


def main() -> None:
    farmers = json.loads(DEMO_PATH.read_text(encoding="utf-8"))
    risk_model = RiskModel()
    explainer = ShapExplainer(risk_model)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    scores = []
    for farmer in farmers:
        features = farmer["features"]
        prediction = risk_model.predict(features)
        explanation = explainer.explain(features, top_k=5)
        advisory = _template_advisory(
            farmer["display_name"],
            prediction["risk_level"],
            explanation["top_factors"],
        )
        bundle = {
            "id": farmer["id"],
            "display_name": farmer["display_name"],
            "narrative": farmer["narrative"],
            "expected_risk_level": farmer["expected_risk_level"],
            "features": features,
            "prediction": prediction,
            "explanation": explanation,
            "advisory_text": advisory,
            "report": {
                "title": f"FarmCredit risk brief — {farmer['display_name']}",
                "risk_score": prediction["risk_score"],
                "risk_level": prediction["risk_level"],
                "top_factors": explanation["top_factors"],
                "advisory_text": advisory,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "cached": True,
            },
            "cached": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        out = CACHE_DIR / f"{farmer['id']}.json"
        out.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
        scores.append((farmer["id"], prediction["risk_score"], prediction["risk_level"]))
        print(f"{farmer['id']}: score={prediction['risk_score']:.3f} band={prediction['risk_level']}")

    # Sanity: Critical should outrank Low
    by_id = {i: s for i, s, _ in scores}
    if by_id["DEMO-04"] <= by_id["DEMO-01"]:
        raise SystemExit(
            f"Demo ordering failed: DEMO-04 ({by_id['DEMO-04']}) should be > DEMO-01 ({by_id['DEMO-01']})"
        )
    print(f"Wrote {len(scores)} cache files -> {CACHE_DIR}")


if __name__ == "__main__":
    main()
