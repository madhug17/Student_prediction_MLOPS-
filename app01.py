from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import time
import logging

# Internal imports - Ensure these files exist in your folders
from schemas.input_schema import StudentData
from schemas.output_schema import PredictionResponse
from services.prediction_service import load_model
from auth import create_access_token, verify_token

# -------- CONFIG & LOGGING --------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This must match the field name in your PredictionResponse schema
MODEL_VERSION = "v1.0.0"

app = FastAPI(title="Student Performance API", version=MODEL_VERSION)
security = HTTPBearer()
model = load_model()

# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- RATE LIMITER MIDDLEWARE --------
request_store = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    
    # Clean up old timestamps (older than 60s)
    request_store[ip] = [t for t in request_store.get(ip, []) if now - t < 60]
    
    if len(request_store[ip]) >= 20: 
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    request_store[ip].append(now)
    return await call_next(request)

# -------- AUTH DEPENDENCY --------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    return payload

# -------- ROUTES --------

@app.get("/")
def home():
    return {
        "status": "ready", 
        "model_loaded": model is not None,
        "version": MODEL_VERSION
    }

@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "1234":
        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 1. SINGLE PREDICTION
@app.post("/v1/predict", response_model=PredictionResponse)
def predict(data: StudentData, user=Depends(get_current_user)):
    if not model:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Convert Pydantic to DataFrame
        input_df = pd.DataFrame([data.model_dump()])
        
        # Get raw prediction and probabilities
        pred = model.predict(input_df)
        prob_array = model.predict_proba(input_df)
        
        # Calculate confidence
        confidence = float(prob_array.max())*100

        # The return keys MUST match PredictionResponse in output_schema.py
        return {
            "prediction": "Pass" if int(pred) == 1 else "Fail",
            "confidence": round(confidence, 4),
            "model_version": MODEL_VERSION 
        }
    except Exception as e:
        logger.error(f"Inference error: {e}")
        # Providing more detail helps debug during development
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

# 2. BATCH PREDICTION
@app.post("/v1/predict-batch")
def predict_batch(data: List[StudentData], user=Depends(get_current_user)):
    if not model:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    if len(data) > 100:
        raise HTTPException(status_code=413, detail="Batch too large (Max 100)")

    try:
        # Convert list of students to one DataFrame
        input_df = pd.DataFrame([d.model_dump() for d in data])
        
        preds = model.predict(input_df)
        probs = model.predict_proba(input_df)
        
        results = []
        for i in range(len(preds)):
            results.append({
                "prediction": "Pass" if int(preds[i]) == 1 else "Fail",
                "confidence": round(float(probs[i].max()), 4),
                "model_version": MODEL_VERSION
            })

        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Batch inference error: {e}")
        raise HTTPException(status_code=500, detail="Batch processing failed")