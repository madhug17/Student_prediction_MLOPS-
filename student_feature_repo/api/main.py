from fastapi import FastAPI
from feast import FeatureStore

app = FastAPI()

store = FeatureStore(repo_path="../feature_repo")

# ADD THIS: A dummy endpoint to stop the 404 terminal spam
@app.get("/metrics")
def metrics():
    return{
         "feature_service": "healthy",
        "redis_status": "connected",
        "feature_view": "student_features",
         "monitored_features": [
            "absences",
            "studytime",
            "G2"
        ]
    }

@app.get("/predict/{student_id}")
def predict(student_id: int):
    features = store.get_online_features(
        features=[
            "student_features:absences",
            "student_features:studytime",
            "student_features:G2",
        ],
        entity_rows=[{"student_id": student_id}]
    ).to_dict()
    return features
