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
with DAG('print_table_of_2_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    # Define a PythonOperator to print the table of 2.
    def print_table_of_2():
        for i in range(1, 11):
            result = 2 * i
            print(f"2 x {i} = {result}")

    print_table_task = PythonOperator(
        task_id='print_table_task',
        python_callable=print_table_of_2
    )

# Define the task order: print_table_task should run.
print_table_task
