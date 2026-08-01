"""Train XGBRegressor on synthetic default_risk and persist model + schema."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from ml.src.features import (
    REPO_ROOT,
    build_feature_schema,
    load_train_config,
    load_xy,
    save_feature_schema,
)


def train_model(cfg: dict) -> dict:
    paths = cfg["paths"]
    feature_columns = cfg["feature_columns"]
    categorical_columns = cfg["categorical_columns"]
    target = cfg["target_column"]
    seed = int(cfg["seed"])

    X_train, y_train = load_xy(
        REPO_ROOT / paths["train_csv"], feature_columns, categorical_columns, target
    )
    X_val, y_val = load_xy(
        REPO_ROOT / paths["val_csv"], feature_columns, categorical_columns, target
    )

    # Align categorical levels across splits (union from train)
    schema = build_feature_schema(X_train, feature_columns, categorical_columns, cfg["risk_bands"])
    for col in categorical_columns:
        cats = schema["categories"][col]
        X_train[col] = X_train[col].astype(str).astype("category")
        X_train[col] = X_train[col].cat.set_categories(cats)
        X_val[col] = X_val[col].astype(str).astype("category")
        X_val[col] = X_val[col].cat.set_categories(cats)

    xcfg = cfg["xgb"]
    model = XGBRegressor(
        n_estimators=int(xcfg["n_estimators"]),
        learning_rate=float(xcfg["learning_rate"]),
        max_depth=int(xcfg["max_depth"]),
        min_child_weight=float(xcfg["min_child_weight"]),
        subsample=float(xcfg["subsample"]),
        colsample_bytree=float(xcfg["colsample_bytree"]),
        reg_lambda=float(xcfg["reg_lambda"]),
        reg_alpha=float(xcfg["reg_alpha"]),
        objective=xcfg["objective"],
        random_state=seed,
        n_jobs=-1,
        enable_categorical=True,
        tree_method="hist",
        early_stopping_rounds=int(xcfg["early_stopping_rounds"]),
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )

    val_pred = np.clip(model.predict(X_val), 0.0, 1.0)
    val_rmse = float(np.sqrt(mean_squared_error(y_val, val_pred)))
    val_mae = float(mean_absolute_error(y_val, val_pred))

    model_dir = REPO_ROOT / paths["model_dir"]
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "model.joblib"
    schema_path = model_dir / "feature_schema.json"
    meta_path = model_dir / "train_meta.json"

    bundle = {
        "model": model,
        "feature_columns": feature_columns,
        "categorical_columns": categorical_columns,
        "target_column": target,
    }
    joblib.dump(bundle, model_path)
    save_feature_schema(schema, schema_path)

    meta = {
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "best_iteration": int(getattr(model, "best_iteration", xcfg["n_estimators"]) or 0),
        "val_rmse": val_rmse,
        "val_mae": val_mae,
        "xgb": xcfg,
        "model_path": str(model_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "schema_path": str(schema_path.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved model -> {model_path}")
    print(f"Saved schema -> {schema_path}")
    print(f"val RMSE={val_rmse:.4f} MAE={val_mae:.4f}")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "ml" / "configs" / "train_config.yaml"),
    )
    args = parser.parse_args()
    cfg = load_train_config(Path(args.config))
    train_model(cfg)


if __name__ == "__main__":
    main()
