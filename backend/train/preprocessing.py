import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from .config import FEATURES, TARGET


def load_data(data_path: str) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")
    return df


def preprocess(df: pd.DataFrame):
    x = df[FEATURES].values
    y_raw = df[TARGET].values

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    return x_train, x_test, y_train, y_test, scaler, label_encoder
