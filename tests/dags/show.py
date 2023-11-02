from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'show_current_directory_and_files',
    default_args=default_args,
    description='Show current directory and list files',
    schedule_interval=None,  # This DAG is not scheduled
    catchup=False,
)

# Use the "pwd" command to display the current directory
show_current_directory = BashOperator(
    task_id='show_current_directory',
    bash_command='pwd',
    dag=dag,
)

# Use the "ls" command to list files in the current directory
list_files = BashOperator(
    task_id='list_files',
    bash_command='ls',
    dag=dag,
)

# Set the task dependencies
show_current_directory >> list_files
