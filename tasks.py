from celery_app import celery
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task(bind=True, max_retries=3)
def predict_student(self, data):
    start_time = time.time()

    try:
        logger.info(f"Task started | id={self.request.id}")
        time.sleep(5)

        score = data["G1"] + data["G2"] - data["absences"]
        result = "Pass" if score > 20 else "Fail"

        duration = round(time.time() - start_time, 2)

        logger.info(
            f"Task completed | id={self.request.id} | "
            f"prediction={result} | score={score} | duration={duration}s"
        )

        return {
            "prediction": result,
            "score": score,
            "duration": duration
        }

    except Exception as e:
        logger.error(f"Task failed | id={self.request.id} | error={str(e)}")
        raise self.retry(exc=e, countdown=5)
import subprocess

@celery.task
def run_feast_materialize():
    logger.info("?? Phase 7: Starting Automated Feast Materialization...")
    # Use a future date to ensure all data is synced
    future_date = "2026-12-31T23:59:59"
    try:
        # Pushes data from Parquet to Online Store (SQLite)
        subprocess.run(["feast", "materialize-incremental", future_date], check=True)
        logger.info("? Online Store Refreshed successfully!")
        return "Success"
    except Exception as e:
        logger.error(f"? Materialization Failed: {e}")
        return str(e)
