import pandas as pd
from feast import FeatureStore

print("🚀 Starting Batch Scoring Pipeline...")

store = FeatureStore(
    repo_path="feature_repo"
)

# ENTITY DATA
entity_df = pd.DataFrame({
    "student_id": [1001, 1002, 1003],
    "event_timestamp": pd.to_datetime([
        "2026-05-07 14:43:00",
        "2026-05-07 14:43:00",
        "2026-05-07 14:43:00"
    ])
})

print("\n🔥 ENTITY DATA:")
print(entity_df)

# GET HISTORICAL FEATURES
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_features:absences",
        "student_features:studytime",
        "student_features:G2",
    ]
).to_df()

print("\n🔥 FEATURES FROM FEAST:")
print(training_df)

# FAKE MODEL PREDICTION
training_df["prediction"] = (
    training_df["G2"] * 0.5
    + training_df["studytime"] * 2
    - training_df["absences"] * 0.3
)

print("\n🔥 BATCH PREDICTIONS:")
print(training_df)

# SAVE PREDICTIONS
training_df.to_csv(
    "batch_predictions.csv",
    index=False
)

print("\n✅ Predictions saved to batch_predictions.csv")