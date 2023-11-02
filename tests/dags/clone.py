from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'git_clone_from_gitlab',
    default_args=default_args,
    description='Clone a GitLab repository using SSH key',
    schedule_interval=None,  # This DAG is not scheduled
    catchup=False,
)

# Define the GitLab repository URL and target directory
git_repo_url = 'git@github.com:Harshit-992/python-script.git'
target_directory = '/tmp/mycloud-scripts'  # Adjust the target directory

# Retrieve the SSH key from the Airflow Variable
ssh_key = Variable.get("ssh_key")
clone_task = BashOperator(
    task_id='clone_repo',
    bash_command=(
        f'git clone {git_repo_url} '
        f'{target_directory}'
    ),
    dag=dag,
)
