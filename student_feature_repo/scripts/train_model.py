import pandas as pd
from feast import FeatureStore
from sklearn.linear_model import LinearRegression
import joblib

print("?? TRAINING PIPELINE STARTED")

store = FeatureStore(repo_path="feature_repo")

# <-- FIXED: Reading from the exact same file Feast looks at!
source_data = pd.read_parquet("feature_repo/data/student_data.parquet")
entity_df = source_data[["student_id", "event_timestamp"]]

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_features:absences",
        "student_features:studytime",
        "student_features:G2",
    ]
).to_df()

print("\n?? TRAINING DATA:")
print(training_df)

if training_df.empty:
    print("? ERROR: Data is still empty!")
    exit()

training_df["final_score"] = (
    training_df["G2"] * 2
    + training_df["studytime"] * 3
    - training_df["absences"]
)

X = training_df[["absences", "studytime", "G2"]]
y = training_df["final_score"]

model = LinearRegression()
model.fit(X, y)

print("\n? MODEL TRAINED")

joblib.dump(model, "student_model.pkl")
print("\n? MODEL SAVED")
