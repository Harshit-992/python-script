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
folder_path = os.path.expanduser('~/tmp/clone/ssh/')

ssh_key = Variable.get("ssh_key")

def setup_ssh_key():
    os.makedirs(folder_path, exist_ok=True)

    ssh_key_file = os.path.join(folder_path, 'ssh_key')

    with open(ssh_key_file, 'w') as f:
        f.write(ssh_key)

    os.chmod(ssh_key_file, 0o600)
def list_files_in_folder():
    files = os.listdir(folder_path)
    for file in files:
        print(f'File in folder: {file}')
        
setup_task = PythonOperator(
    task_id='setup_ssh_key',
    python_callable=setup_ssh_key,
    dag=dag,
)
list_files_task = PythonOperator(
    task_id='list_files_in_folder',
    python_callable=list_files_in_folder,
    dag=dag,
)
clone_task = BashOperator(
    task_id='clone_repo',
    bash_command=(
        f'ssh-agent bash -c "ssh-add {folder_path}ssh_key && git clone {git_repo_url} {target_directory}"'
    ),
    dag=dag,
)

setup_task >> list_files_task >> clone_task
