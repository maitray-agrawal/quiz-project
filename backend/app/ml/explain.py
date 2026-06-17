import shap
import pickle
import pandas as pd
import numpy as np

with open("app/ml/model.pkl", "rb") as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)

FEATURE_NAMES = [
    "attendance_pct",
    "avg_score",
    "assignments_submitted",
    "quiz_avg",
    "study_hours_week",
]

def get_explanation(student_features: dict) -> dict:
    """
    Returns SHAP-based explanation for a single student prediction.
    student_features: dict with keys matching FEATURE_NAMES
    """
    df = pd.DataFrame([student_features])[FEATURE_NAMES]
    
    proba = model.predict_proba(df)[0]
    prediction = int(model.predict(df)[0])
    
    shap_values = explainer.shap_values(df)
    
    # Build a readable explanation
    contributions = []
    for i, feat in enumerate(FEATURE_NAMES):
        contributions.append({
            "feature": feat,
            "value": float(df[feat].iloc[0]),
            "shap_value": float(shap_values[0][i]),
            "direction": "increases_risk" if shap_values[0][i] < 0 else "reduces_risk"
        })
    
    # Sort by absolute impact
    contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    
    return {
        "prediction": "pass" if prediction == 1 else "fail",
        "confidence": float(max(proba)),
        "risk_tier": "low" if proba[1] > 0.7 else ("medium" if proba[1] > 0.4 else "high"),
        "top_factors": contributions[:3],  # top 3 drivers
        "all_factors": contributions,
    }