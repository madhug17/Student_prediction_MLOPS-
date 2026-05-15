import pandas as pd
from datetime import datetime, timezone
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Added timezone.utc to make the timestamps tz-aware
entity_df = pd.DataFrame.from_dict({
    "student_id": [1, 2],  
    "event_timestamp": [
        datetime(2026, 5, 8, 9, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 5, 8, 11, 0, 0, tzinfo=timezone.utc)
    ]
})

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_features:absences",
        "student_features:studytime",
        "student_features:G2"
    ]
).to_df()

print("\n--- PHASE 3: HISTORICAL DATASET ---")
print(training_df)
