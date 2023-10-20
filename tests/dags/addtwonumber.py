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
with DAG('sum_of_two_numbers_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    # Define a PythonOperator to calculate and print the sum.
    def print_sum_of_numbers():
        num1 = 10  # Replace with your first number
        num2 = 20  # Replace with your second number
        result = num1 + num2
        print(f"The sum of {num1} and {num2} is {result}")

    print_sum_task = PythonOperator(
        task_id='print_sum_task',
        python_callable=print_sum_of_numbers
    )

# Define the task order: print_sum_task should run.
print_sum_task
