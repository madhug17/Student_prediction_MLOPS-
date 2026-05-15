
from datetime import datetime
import pandas as pd

# If you have SQLAlchemy code, comment it out for now.
# Use the local path where we pushed the CSV file earlier.
df = pd.read_csv('/opt/airflow/student-mat.csv')

print("CSV loaded successfully!")
# Your training logic (XGBoost, Random Forest, etc.) goes below...

with DAG(
    dag_id="student_training_pipeline",
    start_date=datetime(2026, 4, 28),
    schedule=None,
    catchup=False
) as dag:

    # Task 1: Run your actual training script
    train_model = BashOperator(
        task_id="run_training",
        # This tells Airflow to run your python script
        bash_command="python /opt/airflow/training.py" 
    )