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
    'install_git',
    default_args=default_args,
    description='Install Git using Airflow',
    schedule_interval=None,  # This DAG is not scheduled
    catchup=False,
)

# Use a BashOperator to install git
install_git_task = BashOperator(
    task_id='install_git',
    bash_command='sudo apt-get update && sudo apt-get install -y git', 
    dag=dag,
)

# Set the task dependencies
install_git_task
