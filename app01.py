from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import redis.asyncio as redis
import json
import logging

# ---- IMPORT CELERY TASK ----
from tasks import predict_student

# ---- IMPORT TO CHECK TASK STATUS ----
from celery.result import AsyncResult

from pydantic import BaseModel
from dotenv import load_dotenv

# ---- PROMETHEUS METRICS ----
from prometheus_fastapi_instrumentator import Instrumentator

# ---- AUTH FUNCTIONS ----
from auth import create_access_token, verify_token

# ---- LOAD ENVIRONMENT VARIABLES ----
load_dotenv()

# ---- INIT FASTAPI APP ----
app = FastAPI(title="ML Prediction API - Producer Service")

# ---- ENABLE METRICS ENDPOINT ----
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# ---- LOGGING SETUP ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- REDIS CONNECTION POOL ----
pool = redis.ConnectionPool(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
    max_connections=50
)

# ---- REDIS CLIENT ----
redis_client = redis.Redis(connection_pool=pool)

# ---- AUTH SETUP ----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ---- CURRENT USER VALIDATION ----
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# ---- INPUT DATA MODEL ----
class StudentData(BaseModel):
    G1: int
    G2: int
    absences: int
    failures: int = 0
    studytime: int = 2
    Mother_edu: int = 4
    Father_edu: int = 4
    Trip: int = 2
    health: int = 5
    higher: str = "yes"
    sex: str = "M"
    school: str = "GP"


# =========================================================
# ROUTES
# =========================================================

# ---- HEALTH CHECK ROUTE ----
@app.get("/")
async def health():
    try:
        redis_ok = await redis_client.ping()

    except Exception as e:
        logger.error(f"Health check Redis fail: {e}")
        redis_ok = False

    return {
        "status": "online",
        "redis": redis_ok,
        "service": "producer"
    }


# ---- LOGIN ROUTE ----
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username == "admin" and form_data.password == "1234":

        token = create_access_token({"sub": form_data.username})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")


# ---- PREDICTION ROUTE ----
@app.post("/predict-easy")
async def predict_easy(
    data: StudentData,
    current_user: dict = Depends(get_current_user)
):
    try:
        payload = data.model_dump()

        # Send task to Celery
        task = predict_student.delay(payload)

        # Optional manual Redis queue tracking
        job = {
            "id": task.id,
            "data": payload,
            "status": "queued"
        }

        await redis_client.rpush("prediction_queue", json.dumps(job))

        return {
            "status": "queued",
            "task_id": task.id
        }

    except Exception as e:
        logger.error(f"TASK QUEUE ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Internal Queue Error: {str(e)}"
        )


# ---- RESULT CHECK ROUTE ----
@app.get("/result/{request_id}")
async def get_result(
    request_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        # IMPORTANT FIX:
        # bind Celery app explicitly
        task_result = AsyncResult(request_id, app=predict_student.app)

        if task_result.state == "PENDING":
            return {
                "status": "processing",
                "request_id": request_id,
                "state": task_result.state
            }

        if task_result.state == "FAILURE":
            return {
                "status": "failed",
                "request_id": request_id,
                "state": task_result.state,
                "error": str(task_result.result)
            }

        return {
            "status": "completed",
            "request_id": request_id,
            "state": task_result.state,
            "result": task_result.result
        }

    except Exception as e:
        logger.error(f"RESULT FETCH ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Result Fetch Error: {str(e)}"
        )


# ---- RUN APP ----
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app01:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )