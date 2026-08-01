"""Evaluate trained FarmCredit risk model; write metrics and plots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from ml.src.features import REPO_ROOT, load_train_config, load_xy, risk_band


def evaluate(cfg: dict) -> dict:
    paths = cfg["paths"]
    feature_columns = cfg["feature_columns"]
    categorical_columns = cfg["categorical_columns"]
    target = cfg["target_column"]
    bands = cfg["risk_bands"]
    thr = float(cfg["binary_threshold"])

    bundle = joblib.load(REPO_ROOT / paths["model_dir"] / "model.joblib")
    model = bundle["model"]
    schema = json.loads((REPO_ROOT / paths["model_dir"] / "feature_schema.json").read_text(encoding="utf-8"))

    X_test, y_test = load_xy(
        REPO_ROOT / paths["test_csv"], feature_columns, categorical_columns, target
    )
    for col in categorical_columns:
        cats = schema["categories"][col]
        X_test[col] = X_test[col].astype(str).astype("category")
        X_test[col] = X_test[col].cat.set_categories(cats)

    pred = np.clip(model.predict(X_test), 0.0, 1.0)
    rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
    mae = float(mean_absolute_error(y_test, pred))

    y_true_bin = (y_test >= thr).astype(int)
    y_pred_bin = (pred >= thr).astype(int)

    metrics = {
        "rmse": rmse,
        "mae": mae,
        "binary_threshold": thr,
        "auc_roc": float(roc_auc_score(y_true_bin, pred)) if y_true_bin.nunique() > 1 else None,
        "accuracy": float(accuracy_score(y_true_bin, y_pred_bin)),
        "precision": float(precision_score(y_true_bin, y_pred_bin, zero_division=0)),
        "recall": float(recall_score(y_true_bin, y_pred_bin, zero_division=0)),
        "f1": float(f1_score(y_true_bin, y_pred_bin, zero_division=0)),
        "classification_report": classification_report(
            y_true_bin, y_pred_bin, target_names=["low_risk", "high_risk"], zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_true_bin, y_pred_bin).tolist(),
    }

    # Band distribution check
    true_bands = [risk_band(float(s), bands) for s in y_test]
    pred_bands = [risk_band(float(s), bands) for s in pred]
    metrics["band_accuracy"] = float(np.mean(np.array(true_bands) == np.array(pred_bands)))

    reports_dir = REPO_ROOT / paths["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Confusion matrix plot
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_predictions(
        y_true_bin,
        y_pred_bin,
        display_labels=["low_risk", "high_risk"],
        ax=ax,
        colorbar=False,
    )
    ax.set_title("Default risk (thresholded)")
    fig.tight_layout()
    fig.savefig(reports_dir / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    # ROC
    if metrics["auc_roc"] is not None:
        fpr, tpr, _ = roc_curve(y_true_bin, pred)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(fpr, tpr, label=f"AUC={metrics['auc_roc']:.3f}")
        ax.plot([0, 1], [0, 1], "--", color="gray")
        ax.set_xlabel("FPR")
        ax.set_ylabel("TPR")
        ax.set_title("ROC curve")
        ax.legend()
        fig.tight_layout()
        fig.savefig(reports_dir / "roc_curve.png", dpi=150)
        plt.close(fig)

    # Pred vs actual
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(y_test, pred, alpha=0.25, s=12)
    ax.plot([0, 1], [0, 1], "--", color="gray")
    ax.set_xlabel("Actual default_risk")
    ax.set_ylabel("Predicted default_risk")
    ax.set_title("Predicted vs actual")
    fig.tight_layout()
    fig.savefig(reports_dir / "pred_vs_actual.png", dpi=150)
    plt.close(fig)

    metrics_path = REPO_ROOT / paths["model_dir"] / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump({k: v for k, v in metrics.items() if k != "classification_report"}, f, indent=2)

    report_txt = reports_dir / "classification_report.txt"
    report_txt.write_text(
        f"RMSE={rmse:.4f}\nMAE={mae:.4f}\nAUC={metrics['auc_roc']}\n\n"
        + metrics["classification_report"],
        encoding="utf-8",
    )

    print(f"RMSE={rmse:.4f} MAE={mae:.4f} AUC={metrics['auc_roc']}")
    print(f"P={metrics['precision']:.3f} R={metrics['recall']:.3f} F1={metrics['f1']:.3f}")
    print(f"Wrote metrics -> {metrics_path}")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "ml" / "configs" / "train_config.yaml"),
    )
    args = parser.parse_args()
    cfg = load_train_config(Path(args.config))
    evaluate(cfg)


if __name__ == "__main__":
    main()
