from fastapi.testclient import TestClient
from app01 import app, get_current_user
from services.prediction_service import get_model

# 1. Mock the Model
class Fakemodel:
    def predict(self, X):
        return
    def predict_proba(self, X):
        return [[0.2, 0.8]]

# 2. Mock the User (Bypasses the JWT requirement for tests)
def override_get_current_user():
    return {"sub": "test_admin"}

# Apply Overrides
app.dependency_overrides[get_model] = lambda: Fakemodel()
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_predict_success():
    response = client.post('/predict', json={
        "hours_studied": 5,
        "attendance": 80,
        "previous_score": 70
    })
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert 'confidence' in data

def test_predict_invalid_input():
    # Pydantic will catch the negative hours based on our gt=0 rule in the schema
    response = client.post('/predict', json={
        "hours_studied": -5,
        "attendance": 80,
        "previous_score": 70
    })
    assert response.status_code == 422

def test_zero_hours():
    response = client.post('/predict', json={
        "hours_studied": 0,
        "attendance": 80,
        "previous_score": 70
    })
    assert response.status_code == 422