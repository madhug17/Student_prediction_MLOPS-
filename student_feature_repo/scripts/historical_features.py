import pandas as pd
from feast import FeatureStore

store = FeatureStore(
    repo_path="feature_repo"
)

# LOAD TRAINING DATA
entity_df = pd.read_csv(
    "feature_repo/data/training_data.csv"
)

# CLEAN COLUMNS
entity_df.columns = entity_df.columns.str.strip()

# FIX DATATYPES
entity_df["student_id"] = entity_df["student_id"].astype("int64")

# CONVERT TIMESTAMP
entity_df["event_timestamp"] = pd.to_datetime(
    entity_df["event_timestamp"]
)

print("🔥 ENTITY DATAFRAME:")
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

print("\n🔥 TRAINING FEATURES:")
print(training_df)