from feast import FeatureStore
from datetime import datetime
import pandas as pd

store = FeatureStore(
    repo_path="feature_repo"
)
push_off= pd.DataFrame.from_dict({
    "student_id": [1001],
    "absences": [1],
    "studytime": [5],
    "G2": [18],
    "event_timestamp": [datetime.utcnow()]
})
store.push(
    push_source_name="student_push_source",
    df= push_off
)
print("🔥 Features pushed successfully!")