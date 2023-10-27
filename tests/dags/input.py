from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Define DAG
dag = DAG(
    'input_name_example',
    schedule_interval=None,  # This DAG is not scheduled
    start_date=days_ago(1),
    catchup=False,
)

# Python function to perform a task using parameters
def multiply_numbers(**kwargs):
    # Retrieve parameters from the context
    params = kwargs['dag_run'].conf

    # Get the values of 'number1' and 'number2' from the parameters
    number1 = params['number1']
    number2 = params['number2']

    # Perform the task (multiply numbers)
    result = number1 * number2

    # Print the result
    print(f"The result of {number1} * {number2} is {result}")

# Create a PythonOperator that uses parameters
multiply_task = PythonOperator(
    task_id='multiply_task',
    python_callable=multiply_numbers,
    provide_context=True,  # Pass the context to the function
    dag=dag,
)

# Set the task dependencies (no dependencies in this case)
multiply_task
