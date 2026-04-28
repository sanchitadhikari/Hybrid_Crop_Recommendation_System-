import json
from pathlib import Path

import joblib
import numpy as np
import shap

from . import config


class ModelService:
    def __init__(self) -> None:
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.rf_explainer_model = None
        self.features = config.FEATURES
        self.shap_global = []

    def load(self) -> None:
        required = [
            config.MODEL_PATH,
            config.SCALER_PATH,
            config.LABEL_ENCODER_PATH,
            config.RF_EXPLAINER_MODEL_PATH,
            config.FEATURES_PATH,
        ]
        missing = [str(p) for p in required if not Path(p).exists()]
        if missing:
            raise FileNotFoundError(
                "Missing model artifacts. Run training first. Missing: " + ", ".join(missing)
            )

        self.model = joblib.load(config.MODEL_PATH)
        self.scaler = joblib.load(config.SCALER_PATH)
        self.label_encoder = joblib.load(config.LABEL_ENCODER_PATH)
        self.rf_explainer_model = joblib.load(config.RF_EXPLAINER_MODEL_PATH)

        with open(config.FEATURES_PATH, "r", encoding="utf-8") as f:
            self.features = json.load(f)

        if Path(config.SHAP_GLOBAL_PATH).exists():
            with open(config.SHAP_GLOBAL_PATH, "r", encoding="utf-8") as f:
                self.shap_global = json.load(f)

    def _to_array(self, payload: dict) -> np.ndarray:
        return np.array([[payload[f] for f in self.features]], dtype=float)

    @staticmethod
    def _entropy_uncertainty(probs: np.ndarray) -> tuple[float, float]:
        eps = 1e-12
        probs = np.clip(probs, eps, 1.0)
        entropy = float(-(probs * np.log(probs)).sum())
        max_entropy = float(np.log(len(probs)))
        uncertainty = entropy / max_entropy if max_entropy > 0 else 0.0
        confidence = max(0.0, min(100.0, (1.0 - uncertainty) * 100.0))
        return uncertainty, confidence

    def predict(self, payload: dict) -> dict:
        x_raw = self._to_array(payload)
        x_scaled = self.scaler.transform(x_raw)

        pred_idx = int(self.model.predict(x_scaled)[0])
        pred_crop = str(self.label_encoder.inverse_transform([pred_idx])[0])
        probs = self.model.predict_proba(x_scaled)[0]
        uncertainty, confidence = self._entropy_uncertainty(probs)

        hint = "Input looks valid."
        if payload["ph"] < 4.5 or payload["ph"] > 8.5:
            hint = "Soil pH is outside common crop comfort range (4.5-8.5)."
        elif payload["humidity"] < 20:
            hint = "Humidity is low; prediction confidence may drop in dry conditions." 

        return {
            "crop": pred_crop,
            "confidence": round(confidence, 2),
            "uncertainty": round(uncertainty, 4),
            "validation_hint": hint,
        }

    def get_shap_global(self) -> list[dict]:
        if self.shap_global:
            return self.shap_global
        return [{"feature": f, "importance": 0.0} for f in self.features]

    def get_shap_local(self, payload: dict) -> dict:
        x_raw = self._to_array(payload)
        x_scaled = self.scaler.transform(x_raw)

        pred_idx = int(self.model.predict(x_scaled)[0])
        pred_crop = str(self.label_encoder.inverse_transform([pred_idx])[0])

        explainer = shap.TreeExplainer(self.rf_explainer_model)
        shap_values = explainer.shap_values(x_scaled)

        if isinstance(shap_values, list):
            vals = shap_values[pred_idx][0]
        else:
            vals = shap_values[0, :, pred_idx]

        items = [
            {"feature": feat, "contribution": float(val)}
            for feat, val in zip(self.features, vals)
        ]
        items.sort(key=lambda x: abs(x["contribution"]), reverse=True)

        return {"predicted_crop": pred_crop, "items": items}


model_service = ModelService()
