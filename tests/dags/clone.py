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
git_repo_url = 'git@gitlab.intelligrape.net:tothenew/mycloud-scripts.git'
target_directory = '/tmp/mycloud-scripts'  # Adjust the target directory

# Retrieve the SSH key from the Airflow Variable
ssh_key = Variable.get("ssh_key")

# Create a temporary file and write the SSH key to it
ssh_key_file = '/tmp/ssh_key'
with open(ssh_key_file, 'w') as f:
    f.write(ssh_key)

# Ensure the temporary file is readable only by the owner
import os
os.chmod(ssh_key_file, 0o600)

# Define the GIT_SSH_COMMAND with the path to the temporary SSH key file
git_ssh_command = f'GIT_SSH_COMMAND="ssh -i {ssh_key_file}"'

# Task to set up the SSH key
set_up_ssh_key = BashOperator(
    task_id='set_up_ssh_key',
    bash_command=(
        'mkdir -p ~/.ssh && '
        f'cp {ssh_key_file} ~/.ssh/id_rsa && chmod 600 ~/.ssh/id_rsa'
    ),
    dag=dag,
)

# Clone the GitLab repository using the SSH key
clone_task = BashOperator(
    task_id='clone_repo',
    bash_command=(
        f'{git_ssh_command} git clone {git_repo_url} '
        f'{target_directory}'
    ),
    dag=dag,
)

# Set the task dependencies
set_up_ssh_key >> clone_task
