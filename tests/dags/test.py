from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Define a Python function to print "Hello, World!"
def print_hello_world():
    print("Hello, World!")

# Define the DAG
with DAG(
    'hello_world_dag',
    schedule_interval=None,  # This DAG is not scheduled
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # Create a PythonOperator task to run the print_hello_world function
    print_hello_world_task = PythonOperator(
        task_id='print_hello_world_task',
        python_callable=print_hello_world,
    )
