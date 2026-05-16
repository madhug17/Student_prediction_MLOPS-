import requests

url = "http://localhost:8000/predict-easy"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc3NjY4NTI2MX0.s2sFVxu20TAPqXTFxOGCnteU6CDu5hBUkJVWk1waVb8"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# The chef wants 'higher' to be a string, not a number!
data = {
    "G1": 15,
    "G2": 14,
    "absences": 2,
    "higher": "yes"  # Changed from 1 to "yes"
}

response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Prediction Result: {response.json()}")