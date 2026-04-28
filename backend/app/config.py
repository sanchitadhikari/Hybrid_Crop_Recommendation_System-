from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "stacking_model.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.joblib"
RF_EXPLAINER_MODEL_PATH = MODELS_DIR / "rf_explainer_model.joblib"
FEATURES_PATH = MODELS_DIR / "features.json"
SHAP_GLOBAL_PATH = MODELS_DIR / "shap_global.json"
SHAP_GLOBAL_IMAGE_PATH = MODELS_DIR / "shap_global_importance.png"
CORRELATION_HEATMAP_IMAGE_PATH = MODELS_DIR / "feature_correlation_heatmap.png"
CROP_DISTRIBUTION_IMAGE_PATH = MODELS_DIR / "crop_distribution.png"

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
