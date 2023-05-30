from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'guru',
    'start_date': datetime(2023, 5, 30), #adjust the date as per your requirement
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_processing',
    default_args = default_args,
    schedule_interval = '@daily'
)

def run_generate_data():
    exec(open('/Users/guruprakaash/Documents/Project/generate_data.py').read())

def run_aggregate_data():
    exec(open('/Users/guruprakaash/Documents/Project/aggregate_data.py').read())

def run_clean_up():
    exec(open('/Users/guruprakaash/Documents/Project/clean_up.py').read())

generate_data_task = PythonOperator(
    task_id = 'generate_data',
    python_callable = run_generate_data,
    dag = dag
)

aggregate_data_task = PythonOperator(
    task_id = 'aggregate_data',
    python_callable = run_aggregate_data,
    dag = dag
)

clean_up_task = PythonOperator(
    task_id = 'clean_up',
    python_callable = run_clean_up,
    dag = dag
)

generate_data_task >> aggregate_data_task >> clean_up_task
