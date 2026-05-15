from feast import FeatureStore
import pandas as pd

store = FeatureStore(
    repo_path="./student_feature_repo/feature_repo"
)

print("🚀 TESTING REQUEST-TIME FEATURES...\n")

features = store.get_online_features(
    features=[
        "student_request_metrics:live_performance_score",
    ],

    entity_rows=[
        {
            "student_id": 1001,

            # LIVE REQUEST DATA
            "hours_slept": 10,
            "extra_study_hours": 4,
        }
    ]
).to_dict()

print("🔥 REQUEST FEATURE OUTPUT:\n")
print(pd.DataFrame.from_dict(features))