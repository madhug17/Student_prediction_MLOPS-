from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import pandas as pd
import os

# --- LOGIC FUNCTIONS ---

def check_data_quality():
    path = '/opt/airflow/student-mat.csv'
    # If the file is missing, we jump to the stop path
    if not os.path.exists(path):
        print("Data file not found!")
        return 'stop_pipeline'
    
    df = pd.read_csv(path, sep=None, engine='python')
    
    # Requirement: Dataset must have at least 100 students
    if len(df) > 100:
        print(f"Quality Check Passed: {len(df)} rows found.")
        return 'train_xgboost_model'
    else:
        print(f"Quality Check Failed: Insufficient data ({len(df)} rows).")
        return 'stop_pipeline'

def evaluate_model_performance():
    # In a real setup, you'd pull the actual metric from your training task via XComs
    # For now, we simulate the validation logic
    accuracy = 0.92 
    threshold = 0.85
    
    if accuracy >= threshold:
        print(f"Validation Passed: {accuracy} >= {threshold}")
        return 'deploy_model'
    else:
        print(f"Validation Failed: {accuracy} < {threshold}")
        return 'reject_model'

# --- DAG DEFINITION ---

default_args = {
    'owner': 'Madhu',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='intelligent_retraining_orchestrator',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['capstone', 'mlops']
) as dag:

    # STAGE 1 & 2: Quality Check & Branching
    quality_check = BranchPythonOperator(
        task_id='quality_check_branch',
        python_callable=check_data_quality
    )

    # STAGE 3: Training (The Engine)
    # This runs only if quality_check returns 'train_xgboost_model'
    train_model = BashOperator(
        task_id='train_xgboost_model',
        bash_command='python /opt/airflow/training.py'
    )

    # STAGE 4 & 5: Evaluation & Deployment Decision
    val_branch = BranchPythonOperator(
        task_id='deployment_decision_branch',
        python_callable=evaluate_model_performance
    )

    # STAGE 6: Outcomes
    deploy = BashOperator(
        task_id='deploy_model',
        bash_command='echo "SUCCESS: Model deployed to production environment."'
    )

    reject = BashOperator(
        task_id='reject_model',
        bash_command='echo "REJECTED: Model accuracy below threshold."'
    )

    stop = BashOperator(
        task_id='stop_pipeline',
        bash_command='echo "ABORTED: Data quality issues detected."'
    )

    # FINAL NOTIFICATION (The Orchestration Wrap-up)
    # trigger_rule='one_success' ensures this runs if ANY path finishes
    summary = BashOperator(
        task_id='pipeline_summary',
        bash_command='echo "MLOps Orchestration Cycle Finished."',
        trigger_rule=TriggerRule.ONE_SUCCESS 
    )

    # --- THE ARCHITECTURE (Dependencies) ---
    quality_check >> [train_model, stop]
    train_model >> val_branch >> [deploy, reject]
    [deploy, reject, stop] >> summary