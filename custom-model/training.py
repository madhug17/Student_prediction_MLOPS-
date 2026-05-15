from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import joblib

# Create dummy training data
X, y = make_regression(
    n_samples=100,
    n_features=3,
    noise=0.1,
    random_state=42
)

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "student_model.pkl")

print("Model saved successfully!")