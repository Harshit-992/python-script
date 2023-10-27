from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

# Define DAG
dag = DAG(
    'input_name_example',
    schedule_interval=None,  # This DAG is not scheduled
    start_date=days_ago(1),
    catchup=False,
)

# Define default parameter values using Variables
Variable.set("number1", "5")
Variable.set("number2", "7")

# Python function to perform a task using parameters
def multiply_numbers(**kwargs):
    # Get the values of 'number1' and 'number2' from Variables
    number1 = Variable.get("number1")
    number2 = Variable.get("number2")

    # Perform the task (multiply numbers)
    result = int(number1) * int(number2)

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
