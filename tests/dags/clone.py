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

# Define the environment dictionary
environment = {
    'GIT_SSH_COMMAND': f'ssh -i <(echo $\'{ssh_key}\')',
}

# Clone the GitLab repository using the SSH key
clone_task = BashOperator(
    task_id='clone_repo',
    bash_command=f'git clone {git_repo_url} {target_directory}',
    environment=environment,  # Use the environment dictionary
    dag=dag,
)

# Set the task dependencies
clone_task
