from feast import FeatureStore
import joblib
import pandas as pd
import numpy as np

# 1. Load the "Brain" and the "Store"
model = joblib.load("student_model.pkl")
store = FeatureStore(repo_path=".")

def make_prediction(student_id):
    # 2. Fetch from Online Store
    feature_vector = store.get_online_features(
        features=[
            "student_features:absences",
            "student_features:studytime",
        ],
        entity_rows=[{"student_id": student_id}],
    ).to_dict()

    df = pd.DataFrame.from_dict(feature_vector)
    
    # Check if student exists
    if df["absences"].isnull().values.any():
        return None

    X = df[["absences", "studytime"]]

    # 3. Predict and extract the scalar value
    prediction = model.predict(X)
    
    # <-- FIXED: Scikit-learn returns an array like [14.5]. We grab the first item!
    return float(prediction[0])

# --- TEST IT OUT ---
try:
    sid = int(input("Enter Student ID to predict (1001-1005): "))
    result = make_prediction(sid)
    
    if result is None:
        print(f"\n? Student {sid} not found in Online Store.")
    else:
        print(f"\n? Result for Student {sid}:")
        print(f"Predicted G2 Grade: {result:.2f}/20")
except Exception as e:
    print(f"?? Error: {e}")
