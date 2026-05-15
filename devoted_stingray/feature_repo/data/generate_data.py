import pandas as pd 
from datetime import datetime , timedelta,timezone
data = pd.DataFrame.from_dict({
    "student_id": [1001, 1002, 1003, 1004, 1005],  # <-- Filled with 5 IDs
    "absences": [0, 4, 2, 10, 1],                  # <-- 5 absence records
    "studytime": [3, 2, 4, 1, 3],                  # <-- 5 studytime records
    "G2": [15, 11, 16, 8, 14],                     # <-- 5 grades
    "event_timestamp": [datetime.now(timezone.utc) - timedelta(days=1)] * 5
})
# Save it over our old parquet file
data.to_parquet("data/student_data.parquet")
print("✅ Expanded dataset created with 5 students!")