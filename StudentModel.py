import joblib
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class StudentModel:
    def __init__(self):
        """
        Seldon calls this once when the container starts.
        This replaces your global 'model load' in tasks.
        """
        self.model = joblib.load("student_model.pkl")
        logger.info("✅ Seldon Wrapper: Model loaded and ready for inference.")
    def predict(self,x,features_names=None):
        """
        Seldon calls this every time a user hits the API.
        X: The input data sent by the user (Seldon passes this as a Numpy array).
        """
        logger.info(f"🚀 Seldon received request data: {x}")
        prediction = self.model.predict(x)
        return prediction.tolist()