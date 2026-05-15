from feast import FeatureStore

print("🚀 Testing Feature Service...")
store = FeatureStore(repo_path="student_feature_repo/feature_repo")

features = store.get_online_features(
    features=store.get_feature_service(
        "student_prediction_service"
    ),
    entity_rows=[
        {"student_id": 1001}
    ]
).to_dict()

print("\n🔥 FEATURE SERVICE OUTPUT:\n")
print(features)