import joblib
import numpy as np


class StudentPerformanceModel:

    def __init__(self):
        print("Loading model...")

        self.model = joblib.load("student_model.pkl")

        print("Model loaded successfully!")

    def predict(self, X, features_names=None, meta=None):

        try:
            X = np.array(X)

            prediction = self.model.predict(X)

            return prediction.tolist()

        except Exception as e:
            return {"error": str(e)}