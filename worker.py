import os
import time
import json
import redis
import joblib
import numpy as np

# Use 127.0.0.1 for local Windows stability
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print("Connecting to Redis...")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

print("Loading model...")
# Ensure model.joblib is in the same directory
model = joblib.load("model.joblib")

print("Worker started. Waiting for jobs...")

while True:
    try:
        # blpop is great for throughput; it waits for a job without hammering CPU
        job = r.blpop("prediction_queue", timeout=5)
        
        if job:
            _, payload = job
            job_data = json.loads(payload)

            # Accessing the 'data' dictionary sent by app01.py
            student_data = job_data['data']
            
            # THE 12 FEATURES: Must exactly match ColumnTransformer order
            input_list = [
                student_data["G1"],           # 1
                student_data["G2"],           # 2
                student_data["absences"],     # 3
                student_data["failures"],     # 4
                student_data["studytime"],    # 5
                student_data["Mother_edu"],   # 6
                student_data["Father_edu"],   # 7
                student_data["Trip"],         # 8
                student_data["health"],       # 9
                student_data["higher"],       # 10 (String: "yes"/"no")
                student_data["sex"],          # 11 (String: "M"/"F")
                student_data["school"]        # 12 (String: "GP"/"MS")
            ]
            
            # CRITICAL FIX: dtype=object allows strings and numbers to coexist in the array
            # This is required for ColumnTransformers handling categorical data.
            features = np.array(input_list, dtype=object).reshape(1, -1)
            
            # Run prediction
            prediction = model.predict(features)[0]
            
            results = {
                "job_id": job_data["id"],
                "prediction": int(prediction),
                "status": "completed",
                "timestamp": time.time()
            }
            
            # Store result with an expiration (1 hour) so Redis memory stays clean
            r.set(f"result:{job_data['id']}", json.dumps(results), ex=3600)
            
            print(f"✅ Processed job: {job_data['id']} | Prediction: {prediction}")

    except KeyError as e:
        print(f"❌ Data Error: Missing field {e} in incoming request")
    except Exception as e:
        print(f"⚠️ Worker error: {e}")