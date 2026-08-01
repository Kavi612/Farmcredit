"""Feature loading and schema helpers for FarmCredit XGBoost training."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def load_train_config(path: Path | None = None) -> dict:
    cfg_path = path or (REPO_ROOT / "ml" / "configs" / "train_config.yaml")
    with cfg_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def risk_band(score: float, bands: dict[str, float]) -> str:
    if score < bands["Low"]:
        return "Low"
    if score < bands["Medium"]:
        return "Medium"
    if score < bands["High"]:
        return "High"
    return "Critical"


def prepare_frame(df: pd.DataFrame, categorical_columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in categorical_columns:
        if col in out.columns:
            out[col] = out[col].astype("category")
    return out


def load_xy(
    csv_path: Path,
    feature_columns: list[str],
    categorical_columns: list[str],
    target_column: str,
) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(csv_path)
    X = prepare_frame(df[feature_columns], categorical_columns)
    y = df[target_column].astype(float)
    return X, y


def build_feature_schema(
    X_train: pd.DataFrame,
    feature_columns: list[str],
    categorical_columns: list[str],
    risk_bands: dict[str, float],
) -> dict[str, Any]:
    categories: dict[str, list[Any]] = {}
    for col in categorical_columns:
        cats = list(X_train[col].cat.categories)
        categories[col] = [str(c) for c in cats]

    dtypes = {}
    for col in feature_columns:
        if col in categorical_columns:
            dtypes[col] = "category"
        elif col in {"prior_loan_count", "prior_default_flag", "loan_amount_inr", "annual_income_inr", "existing_debt_inr"}:
            dtypes[col] = "int"
        else:
            dtypes[col] = "float"

    return {
        "feature_columns": feature_columns,
        "categorical_columns": categorical_columns,
        "target_column": "default_risk",
        "dtypes": dtypes,
        "categories": categories,
        "risk_bands": {
            "Low": risk_bands["Low"],
            "Medium": risk_bands["Medium"],
            "High": risk_bands["High"],
            "Critical": 1.0,
        },
        "band_rules": {
            "Low": f"< {risk_bands['Low']}",
            "Medium": f">= {risk_bands['Low']} and < {risk_bands['Medium']}",
            "High": f">= {risk_bands['Medium']} and < {risk_bands['High']}",
            "Critical": f">= {risk_bands['High']}",
        },
    }


def save_feature_schema(schema: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)


def features_from_dict(
    row: dict[str, Any],
    schema: dict[str, Any],
) -> pd.DataFrame:
    """Build a single-row model frame from a FarmerFeatures-like dict."""
    feature_columns = schema["feature_columns"]
    categorical_columns = schema["categorical_columns"]
    data = {c: [row[c]] for c in feature_columns}
    df = pd.DataFrame(data)
    for col in categorical_columns:
        allowed = schema["categories"][col]
        val = str(df.at[0, col])
        if val not in allowed:
            # keep unseen as NaN-like category for xgboost; still raise for API layer
            cats = allowed + [val]
        else:
            cats = allowed
        df[col] = pd.Categorical(df[col].astype(str), categories=cats)
    return df
