import pandas as pd
import joblib
import os

print("STARTING PREDICTION PIPELINE")

# -----------------------------
# 1. LOAD MODEL (STRICT)
# -----------------------------
MODEL_PATH = "models/model_latest.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ model_latest.pkl not found. Run training.py first")

model = joblib.load(MODEL_PATH)

# -----------------------------
# 2. LOAD DATA
# -----------------------------
data = pd.read_csv("student-mat.csv")

print("Columns:", data.columns.tolist())

# -----------------------------
# 3. SAMPLE DATA
# -----------------------------
new_data = data.sample(10).copy()

# -----------------------------
# 4. FORCE DRIFT (for testing)
# -----------------------------
new_data['studytime'] = 10
new_data['absences'] = 100
new_data['G2'] = 0

# -----------------------------
# 5. RENAME (MATCH TRAINING)
# -----------------------------
df = new_data.rename(columns={
    'Medu': 'Mother_edu',
    'Fedu': 'Father_edu',
    'goout': 'Trip'
})

# -----------------------------
# 6. SELECT EXACT TRAINING FEATURES
# -----------------------------
features = [
    "G1", "G2", "absences", "failures", "studytime",
    "Mother_edu", "Father_edu", "Trip", "health",
    "higher", "sex", "school"
]

X = df[features].copy()

print("Final Features Used:", X.columns.tolist())
print(X.head())

# -----------------------------
# 7. PREDICT (IMPORTANT: NO .values)
# -----------------------------
predictions = model.predict(X)

# -----------------------------
# 8. CLEAN LOGGING (STRICT FORMAT)
# -----------------------------
log_data = pd.DataFrame({
    "attendance": df["absences"],
    "hours_studied": df["studytime"],
    "previous_score": df["G2"],
    "prediction": predictions,
    "prediction_time": pd.Timestamp.now()
})

# -----------------------------
# 9. SAVE LOGS (CONSISTENT SCHEMA)
# -----------------------------
os.makedirs("logs", exist_ok=True)
log_file = "logs/predictions.csv"

log_data.to_csv(
    log_file,
    mode='a',
    header=not os.path.exists(log_file),
    index=False
)

print("✅ SUCCESS: Predictions logged cleanly")