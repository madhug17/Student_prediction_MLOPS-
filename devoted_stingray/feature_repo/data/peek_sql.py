import sqlite3
import pandas as pd

con = sqlite3.connect("data/online_store.db")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
print("--- TABLES IN SQLITE ---")
print(tables)
print("\n--- DATA INSIDE THE FEATURE TABLE ---")
df = pd.read_sql_query("SELECT * FROM student_feature_repo_student_features", con)
print(df)
con.close()