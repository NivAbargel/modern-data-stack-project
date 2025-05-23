from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="github_user_ingestion",
    default_args=default_args,
    description="Ingest GitHub user data into PostgreSQL",
    schedule_interval="@daily",  # every day at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False,  # do not backfill missed runs
    tags=["github", "ingestion"],
) as dag:

    run_ingestion_script = BashOperator(
        task_id="run_api_ingest",
        bash_command="python /app/api_ingest.py"
    )

    run_ingestion_script
