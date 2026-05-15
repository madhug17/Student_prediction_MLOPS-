import pandas as pd
df = pd.read_parquet("data/student_data.parquet")
print(df.head())
print("Min time:", df["event_timestamp"].min())
print("Max time:", df["event_timestamp"].max())
