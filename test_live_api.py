import requests
import json

BASE_URL = "https://student-prediction-mlops.onrender.com"

# 1. Authenticate to get Bearer Token
print("🔐 Logging into live API...")
token_response = requests.post(
    f"{BASE_URL}/token", 
    data={"username": "admin", "password": "1234"}
)

if token_response.status_code != 200:
    print(f"❌ Login Failed: {token_response.text}")
    exit()

token = token_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ Token acquired successfully!\n")

# 2. Define Student Payload
student_payload = {
    "G1": 15,
    "G2": 16,
    "absences": 1,
    "failures": 0,
    "studytime": 4,
    "higher": "yes"
}

# 3. Trigger Prediction Task
print("🚀 Sending student data for async prediction...")
predict_response = requests.post(
    f"{BASE_URL}/predict-easy", 
    headers=headers, 
    json=student_payload
)

if predict_response.status_code == 200:
    res_data = predict_response.json()
    task_id = res_data["task_id"]
    print(f"🎯 Task successfully queued! ID: {task_id}")
    
    # 4. Check results endpoint
    print("🔄 Checking processing status...")
    result_response = requests.get(f"{BASE_URL}/result/{task_id}", headers=headers)
    print("📊 Current Live State:")
    print(json.dumps(result_response.json(), indent=2))
else:
    print(f"❌ Prediction Error: {predict_response.status_code} - {predict_response.text}")