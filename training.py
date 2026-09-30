import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# Ensure the file exists in your folder!
try:
    df = pd.read_csv("student-mat.csv", sep=";")
except FileNotFoundError:
    # If semicolon fails, try comma
df = pd.read_csv("student-mat.csv", sep=";")
if "G3" not in df.columns:
    df = pd.read_csv("student-mat.csv", sep=",")

# -------- 2. TARGET FIX --------
df["pass"] = (df["G3"] >= 10).astype(int)

# -------- 3. FEATURE ENGINEERING --------
# I added G1, G2, Medu, Fedu, and higher for better accuracy
features = [
    "G1", "G2", "absences", "failures", "studytime", 
    "Medu", "Fedu", "goout", "health", "higher", "sex", "school"
]

# Ensure all selected features actually exist in the CSV
features = [f for f in features if f in df.columns]

X = df[features]
y = df["pass"]

# -------- 4. PREPROCESSING --------
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),# perpose of OneHotEncoder is to convert words into int (1,0)
    ("num", StandardScaler(), num_cols) # Added scaling for better stability
])

# -------- 5. THE MODEL --------
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestClassifier(
        n_estimators=300, 
        max_depth=12, 
        class_weight="balanced", # Fixes the False Positives issue
        random_state=42
    ))
])

# -------- 6. TRAIN & EVALUATE --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)

# -------- 7. RESULTS --------
y_pred = pipeline.predict(X_test)
print(f"New Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print("\nNew Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

joblib.dump(pipeline, "model.joblib")
print("\nModel saved with improved features!")