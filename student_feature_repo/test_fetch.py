from feast import FeatureStore

print("🔍 Starting Feast feature fetch...")

store = FeatureStore(repo_path="student_feature_repo/feature_repo")

# Using the feature service ensures you request the exact registered features
features = store.get_online_features(
    features=store.get_feature_service("student_prediction_service"),
    entity_rows=[{"student_id": 1001}]
).to_dict()

print("\n🔥 FETCHED ONLINE FEATURES:\n")
print(features)