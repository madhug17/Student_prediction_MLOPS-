import requests
import concurrent.futures
import time
from collections import Counter

# 1. YOUR TOKEN
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc3Njc1NjA3Nn0.uqvUg0aIrQdWSO5I4LI-TuggV0B8cACXmyiqSagEuJc"

URL = "http://localhost/predict-easy"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
DATA = {"G1": 15, "G2": 14, "absences": 2, "higher": "yes"}

def send_request(request_id):
    try:
        start = time.time()
        # Reduced timeout to 2s so we catch "choking" faster
        response = requests.post(URL, json=DATA, headers=HEADERS, timeout=2)
        latency = (time.time() - start) * 1000
        return response.status_code
    except Exception:
        return "FAILED"

# STRESS SETTINGS: 100 workers, 5000 requests
MAX_WORKERS = 100
TOTAL_REQUESTS = 5000

print(f"--- RELEASING THE HAMMER: {TOTAL_REQUESTS} requests @ {MAX_WORKERS} workers ---")
start_hammer = time.time()

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    results = list(executor.map(send_request, range(TOTAL_REQUESTS)))

duration = time.time() - start_hammer
counts = Counter(results)

print("\n--- STRESS TEST RESULTS ---")
print(f"Total Time: {duration:.2f} seconds")
print(f"Requests Per Second: {TOTAL_REQUESTS/duration:.2f}")
for status, count in counts.items():
    print(f"Status {status}: {count}")
print("---------------------------")