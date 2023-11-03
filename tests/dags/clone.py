from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import os

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

git_repo_url = 'git@gitlab.intelligrape.net:tothenew/mycloud-scripts.git'
target_directory = '/tmp/mycloud-scripts'
folder_path = '~/tmp/clone/ssh/'

ssh_key = Variable.get("ssh_key")

create_directory_task = BashOperator(
    task_id='create_directory',
    bash_command=f"""mkdir -p {folder_path}
                     echo "{ssh_key}" > {folder_path}ssh_key
                     ls {folder_path}
                     cat {folder_path}ssh_key

    """,
    dag=dag,
)

clone_task = BashOperator(
    task_id='clone_repo',
    bash_command=(
        f'ssh-agent bash -c "ssh-add {folder_path}ssh_key && git clone {git_repo_url} {target_directory}"'
    ),
    dag=dag,
)

create_directory_task >> clone_task
