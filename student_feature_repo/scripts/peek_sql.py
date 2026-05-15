import sqlite3
import pandas as pd

# Connect to the Online Store database
# Path relative to this script
conn = sqlite3.connect("data/online_store.db")

print("--- TABLES IN SQLITE ---")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type=\"table\";", conn)
print(tables)

# Feast table names usually follow: project_featureview
print("\n--- DATA INSIDE THE FEATURE TABLE ---")
try:
    df = pd.read_sql_query("SELECT * FROM student_feature_repo_student_features", conn)
    print(df)
except Exception as e:
    print(f"Error: {e}")

conn.close()
