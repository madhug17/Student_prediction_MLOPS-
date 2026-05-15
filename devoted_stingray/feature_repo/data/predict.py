from feast import feature_store
import joblib
import pandas as pd

model = joblib.load("student_model.pkl")
store = feature_store(repo_path=".")

def make_prediction(student_id):
    feature_vector = store.get_online_features(
        features=[
            "student_features:absences",
            "student_features:studytime",
            ],
            entity_rows = [{"student_id":student_id}],

    ).to_dict()
    df = pd.DataFrame.from_dict(feature_vector)
    x = df[['absences',"studytime"]]
    prediction = model.predict(x)
    return prediction
# --- TEST IT OUT ---
sid = int(input("Enter Student ID to predict grade (e.g., 1001): "))
result = make_prediction(sid)
print(f"\n?? Result for Student {sid}:")
print(f"Predicted G2 Grade: {result:.2f}/20")