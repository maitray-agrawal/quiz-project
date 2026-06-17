import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import pickle
import os

def train_model():
    """
    Train an XGBoost classifier on student performance data.
    In production, load from MongoDB. Here we generate synthetic data.
    """
    np.random.seed(42)
    n = 1000

    data = pd.DataFrame({
        "attendance_pct": np.random.uniform(50, 100, n),
        "avg_score": np.random.uniform(30, 100, n),
        "assignments_submitted": np.random.randint(0, 20, n),
        "quiz_avg": np.random.uniform(20, 100, n),
        "study_hours_week": np.random.uniform(0, 40, n),
    })

    # Label: pass (1) if avg_score >= 50 and attendance >= 65
    data["label"] = ((data["avg_score"] >= 50) & (data["attendance_pct"] >= 65)).astype(int)

    X = data.drop("label", axis=1)
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        "max_depth": [3, 5],
        "n_estimators": [100, 200],
        "learning_rate": [0.05, 0.1],
    }

    base_model = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
    grid_search = GridSearchCV(base_model, param_grid, cv=3, scoring="f1", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Best params:", grid_search.best_params_)
    print(classification_report(y_test, best_model.predict(X_test)))

    os.makedirs("app/ml", exist_ok=True)
    with open("app/ml/model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    print("Model saved to app/ml/model.pkl")
    return best_model

if __name__ == "__main__":
    train_model()