import pandas as pd
from datetime import datetime
from feast import FeatureStore

# 1. Point to the current directory for the config
store = FeatureStore(repo_path=".")

# 2. Fix the dictionary syntax (need colons and commas)
entity_df = pd.DataFrame.from_dict({
    "student_id":[1001,1002], # We need a list of IDs matching the timestamps
    "event_timestamp": [
        datetime(2026, 5, 8, 9, 0, 0),
        datetime(2026, 5, 8, 11, 0, 0),
    ],
})

# 3. The historical fetch (Offline Store)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_features:absences",
        "student_features:studytime",
        "student_features:G2",
    ],
).to_df()

print("\n--- PHASE 3: HISTORICAL DATASET ---")
print(training_df)