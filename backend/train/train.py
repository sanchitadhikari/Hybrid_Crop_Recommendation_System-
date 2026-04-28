import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import shap
from sklearn.metrics import accuracy_score

from .config import (
    FEATURES,
    FEATURES_PATH,
    LABEL_ENCODER_PATH,
    MODEL_PATH,
    MODELS_DIR,
    RF_EXPLAINER_MODEL_PATH,
    SCALER_PATH,
    SHAP_GLOBAL_PATH,
)
from .modeling import build_rf_explainer_model, build_stacking_model
from .preprocessing import load_data, preprocess


def compute_shap_global(rf_model, x_sample: np.ndarray) -> list[dict]:
    explainer = shap.TreeExplainer(rf_model)
    shap_values = explainer.shap_values(x_sample)

    if isinstance(shap_values, list):
        shap_arr = np.array(shap_values)
        mean_abs = np.mean(np.abs(shap_arr), axis=(0, 1))
    else:
        mean_abs = np.mean(np.abs(shap_values), axis=(0, 2))

    items = [
        {"feature": feat, "importance": float(val)}
        for feat, val in zip(FEATURES, mean_abs)
    ]
    items.sort(key=lambda x: x["importance"], reverse=True)
    return items


def main(data_path: str) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data(data_path)
    x_train, x_test, y_train, y_test, scaler, label_encoder = preprocess(df)

    num_classes = len(label_encoder.classes_)
    stacking_model = build_stacking_model(num_classes=num_classes)
    stacking_model.fit(x_train, y_train)

    y_pred = stacking_model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)

    rf_explainer_model = build_rf_explainer_model()
    rf_explainer_model.fit(x_train, y_train)

    x_sample = x_test[: min(300, len(x_test))]
    shap_global = compute_shap_global(rf_explainer_model, x_sample)

    joblib.dump(stacking_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)
    joblib.dump(rf_explainer_model, RF_EXPLAINER_MODEL_PATH)

    with open(FEATURES_PATH, "w", encoding="utf-8") as f:
        json.dump(FEATURES, f, indent=2)

    with open(SHAP_GLOBAL_PATH, "w", encoding="utf-8") as f:
        json.dump(shap_global, f, indent=2)

    print("Training complete")
    print(f"Test accuracy: {acc * 100:.2f}%")
    print(f"Saved model: {Path(MODEL_PATH)}")
    print(f"Saved SHAP global: {Path(SHAP_GLOBAL_PATH)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train hybrid crop model")
    parser.add_argument("--data", required=True, help="Path to Crop_recommendation.csv")
    args = parser.parse_args()
    main(args.data)
