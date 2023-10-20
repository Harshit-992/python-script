from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define default_args with information about the DAG, such as owner, start_date, and schedule_interval.
default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,  # Number of retries upon failure
}

# Create a DAG instance with a unique ID and default_args.
with DAG('hello_airflow_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    # Define a PythonOperator to run a Python function.
    def print_hello():
        print("Hello, Airflow!")

    print_hello_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello
    )

# Define the task order: print_hello_task should run.
print_hello_task

