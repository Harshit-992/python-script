from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Define a Python function to print the name
def print_name(**kwargs):
    name = kwargs['dag_run'].conf.get('name')
    print(f"Hello, {name}!")

# Define the DAG
with DAG(
    'input_name_example',
    schedule_interval=None,  # This DAG is not scheduled
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # Create a PythonOperator task to run the print_name function
    print_name_task = PythonOperator(
        task_id='print_name_task',
        python_callable=print_name,
        provide_context=True,  # Pass the context to the function
    )
