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
with DAG('print_name_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    # Define three PythonOperator tasks, each printing a name.
    def print_name_1():
        print("Task 1: John")

    def print_name_2():
        print("Task 2: Jane")

    def print_name_3():
        print("Task 3: Alice")

    # Create three PythonOperator tasks.
    print_name_task_1 = PythonOperator(
        task_id='print_name_task_1',
        python_callable=print_name_1
    )

    print_name_task_2 = PythonOperator(
        task_id='print_name_task_2',
        python_callable=print_name_2
    )

    print_name_task_3 = PythonOperator(
        task_id='print_name_task_3',
        python_callable=print_name_3
    )

# Define the task order: the three tasks should run sequentially.
print_name_task_1 >> print_name_task_3
