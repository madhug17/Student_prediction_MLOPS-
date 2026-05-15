from feast import FeatureStore
import pandas as pd 
store = FeatureStore(
    repo_path="./student_feature_repo/feature_repo"
)
features = store.get_online_features(
    features=[
        "student_live_metrics:performance_ratio",
        "student_live_metrics:attendance_score",
        "student_live_metrics:final_risk_score",
    ],
    entity_rows=[
        {"student_id": 1001}
    ]
).to_dict()
print("\n🔥 ON-DEMAND FEATURES:\n")
print(pd.DataFrame.from_dict(features))