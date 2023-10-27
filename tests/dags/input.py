from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
}

# Create the DAG
dag = DAG(
    'input_name_example',
    default_args=default_args,
    description='An example DAG that prompts for a name and prints it',
    schedule_interval=None,  # This DAG is not scheduled
    catchup=False,  # Don't run missed intervals
)

# Python function to get user input
def get_name():
    name = input("Please enter your name: ")
    return name

# Python function to print the name
def print_name(**kwargs):
    ti = kwargs['ti']
    name = ti.xcom_pull(task_ids='get_name_task')
    print(f'Hello, {name}!')

# Define the tasks
get_name_task = PythonOperator(
    task_id='get_name_task',
    python_callable=get_name,
    provide_context=True,  # Pass the context to the function
    dag=dag,
)

print_name_task = PythonOperator(
    task_id='print_name_task',
    python_callable=print_name,
    provide_context=True,  # Pass the context to the function
    dag=dag,
)

# Set up task dependencies
get_name_task >> print_name_task
