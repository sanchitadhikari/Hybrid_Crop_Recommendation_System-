from pathlib import Path

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET = "label"

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "stacking_model.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.joblib"
RF_EXPLAINER_MODEL_PATH = MODELS_DIR / "rf_explainer_model.joblib"
FEATURES_PATH = MODELS_DIR / "features.json"
SHAP_GLOBAL_PATH = MODELS_DIR / "shap_global.json"
