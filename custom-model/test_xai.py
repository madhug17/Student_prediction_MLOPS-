import shap
import joblib
import numpy as np

# Load model
model = joblib.load('student_model.pkl')

# MUST match training feature count
X_sample = np.array([[1,2]])

# SHAP explainer
explainer = shap.Explainer(model.predict, X_sample)

# Calculate SHAP values
shap_values = explainer(X_sample)

print("\n--- XAI Analysis for Student 2 ---")

feature_names = ["Absences", "Study Hours"]

student2 = shap_values.values[0]

for i in range(len(feature_names)):
    print(f"{feature_names[i]} Impact: {student2[i]:.3f}")