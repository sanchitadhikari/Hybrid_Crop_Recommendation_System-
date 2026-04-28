from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier


def build_stacking_model(num_classes: int) -> StackingClassifier:
    estimators = [
        (
            "xgb",
            XGBClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                objective="multi:softprob",
                num_class=num_classes,
                eval_metric="mlogloss",
                random_state=42,
                verbosity=0,
            ),
        ),
        (
            "lgbm",
            LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                objective="multiclass",
                random_state=42,
                verbose=-1,
            ),
        ),
        (
            "cat",
            CatBoostClassifier(
                iterations=200,
                depth=6,
                learning_rate=0.1,
                random_seed=42,
                verbose=0,
            ),
        ),
        ("svm", SVC(kernel="rbf", C=10, probability=True, random_state=42)),
    ]

    meta = LogisticRegression(
        C=1.0,
        max_iter=1000,
        multi_class="multinomial",
        solver="lbfgs",
        random_state=42,
    )

    return StackingClassifier(
        estimators=estimators,
        final_estimator=meta,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        stack_method="predict_proba",
        n_jobs=-1,
    )


def build_rf_explainer_model() -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
