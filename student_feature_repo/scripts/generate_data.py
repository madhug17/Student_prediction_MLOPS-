import pandas as pd
from datetime import datetime, timezone

data = pd.DataFrame.from_dict({
    "student_id": [1001, 1002, 1003, 1004, 1005],
    "absences": [0, 4, 2, 10, 1],
    "studytime": [3, 2, 4, 1, 3],
    "G2": [15, 11, 16, 8, 14],
    "event_timestamp": [datetime.now(timezone.utc)] * 5
})

# <-- FIXED: Forcing the save into the Feast repo folder!
data.to_parquet("feature_repo/data/student_data.parquet")
print("? Expanded dataset created in feature_repo/data!")
