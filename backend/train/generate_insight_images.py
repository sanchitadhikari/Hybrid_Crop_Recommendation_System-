import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from app import config


def generate_shap_global_image() -> Path:
    if not config.SHAP_GLOBAL_PATH.exists():
        raise FileNotFoundError(f"Missing SHAP global artifact: {config.SHAP_GLOBAL_PATH}")

    with open(config.SHAP_GLOBAL_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    if not items:
        raise ValueError("SHAP global artifact is empty.")

    # Keep top features in descending order while plotting bottom-to-top for readability.
    items = sorted(items, key=lambda x: x["importance"], reverse=True)
    features = [i["feature"] for i in items][::-1]
    values = [float(i["importance"]) for i in items][::-1]

    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fcfcfc")

    colors = ["#1c7c54" if v == max(values) else "#ef7d34" for v in values]
    bars = ax.barh(features, values, color=colors, edgecolor="#2a2a2a", linewidth=0.6)

    ax.set_title("Global SHAP Feature Importance", fontsize=18, fontweight="bold", pad=14)
    ax.set_xlabel("Mean |SHAP Value|", fontsize=12)
    ax.set_ylabel("Features", fontsize=12)
    ax.grid(axis="x", linestyle="--", alpha=0.25)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_width() + max(values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.4f}",
            va="center",
            fontsize=10,
            color="#1f2a20",
        )

    fig.tight_layout()
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(config.SHAP_GLOBAL_IMAGE_PATH, bbox_inches="tight")
    plt.close(fig)

    return config.SHAP_GLOBAL_IMAGE_PATH


def _resolve_dataset_path() -> Path:
    candidates = [
        config.BASE_DIR.parent / "Crop_recommendation.csv",
        config.BASE_DIR / "data" / "Crop_recommendation.csv",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("Could not find Crop_recommendation.csv for EDA image generation.")


def generate_correlation_heatmap_image() -> Path:
    data_path = _resolve_dataset_path()
    df = pd.read_csv(data_path)

    corr = df[config.FEATURES].corr().values
    labels = config.FEATURES

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    heat = ax.imshow(corr, cmap="YlGnBu", vmin=-1, vmax=1)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_yticklabels(labels)
    ax.set_title("Feature Correlation Heatmap", fontsize=16, fontweight="bold", pad=12)

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", color="#102018", fontsize=8)

    cbar = fig.colorbar(heat, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Correlation", rotation=270, labelpad=14)

    fig.tight_layout()
    fig.savefig(config.CORRELATION_HEATMAP_IMAGE_PATH, bbox_inches="tight")
    plt.close(fig)
    return config.CORRELATION_HEATMAP_IMAGE_PATH


def generate_crop_distribution_image() -> Path:
    data_path = _resolve_dataset_path()
    df = pd.read_csv(data_path)

    counts = df["label"].value_counts().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fcfcfc")
    bars = ax.barh(counts.index, counts.values, color="#1c7c54", edgecolor="#2a2a2a", linewidth=0.5)

    ax.set_title("Crop Class Distribution", fontsize=16, fontweight="bold", pad=12)
    ax.set_xlabel("Samples")
    ax.set_ylabel("Crop")
    ax.grid(axis="x", linestyle="--", alpha=0.25)

    for bar, val in zip(bars, counts.values):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2, f"{int(val)}", va="center", fontsize=8)

    fig.tight_layout()
    fig.savefig(config.CROP_DISTRIBUTION_IMAGE_PATH, bbox_inches="tight")
    plt.close(fig)
    return config.CROP_DISTRIBUTION_IMAGE_PATH


if __name__ == "__main__":
    shap_path = generate_shap_global_image()
    heatmap_path = generate_correlation_heatmap_image()
    distribution_path = generate_crop_distribution_image()
    print(f"Generated insight image: {shap_path}")
    print(f"Generated insight image: {heatmap_path}")
    print(f"Generated insight image: {distribution_path}")
