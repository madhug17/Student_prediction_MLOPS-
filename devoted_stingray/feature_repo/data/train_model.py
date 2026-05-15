import pandas as pd
from datetime import datetime,timezone,timedelta
from feast import FeatureStore
from sklearn.linear_model import LinearRegression
import joblib 
store = FeatureStore(repo_path=".")
entity_df = pd.DataFrame.from_dict({
    "student_id": [1001, 1002, 1003, 1004, 1005],
    # Ask for data from 23 hours ago so it safely falls inside the TTL window!
    "event_timestamp": [datetime.now(timezone.utc) - timedelta(hours=23)] * 5
})
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_features:absences",
        "student_features:studytime",
        "student_features:G2",
    ],
).to_df()
x= training_df[['absences','studytime']]
y = training_df["G2"]
model = LinearRegression()
model.fit(x,y)
joblib.dump(model, "student_model.pkl")
print("✅ Model trained and saved as student_model.pkl!")
print("\nTraining Data used:\n", training_df[["student_id", "absences", "studytime", "G2"]])