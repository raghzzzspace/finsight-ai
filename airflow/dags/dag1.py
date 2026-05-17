from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_spark():
    subprocess.run(["python", "app/spark/spark_jobs.py"])

with DAG(
    dag_id="finsight_spark_etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="run_spark_job",
        python_callable=run_spark
    )