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
folder_path = '~/clone/ssh/'

ssh_key = Variable.get("ssh_key")

build_jar = BashOperator(
    task_id='build_jar',
    bash_command=f"""pwd
                     mkdir -p {folder_path}
                     echo "{ssh_key}" > {folder_path}ssh_key
                     ls {folder_path}
                     cat {folder_path}ssh_key
                     ls {folder_path}
                     mkdir -p /home/airflow/.ssh
                     touch /home/airflow/.ssh/known_hosts
                     ssh-keyscan gitlab.intelligrape.net >> ~/.ssh/known_hosts
                     chmod 600 {folder_path}ssh_key
                     ssh-agent bash -c 'ssh-add {folder_path}ssh_key; git clone git@gitlab.intelligrape.net:tothenew/ckdataprocessengine.git '
                     git checkout prod-merge-CKPIP-28
                     ls 
                     cd ckdataprocessengine
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt about
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt clean
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt assembly
                     ls
                     
                                         

    """,
    dag=dag,
)

ri_config = BashOperator(
    task_id='ri_config',
    bash_command=f"""pwd
                     mkdir -p {folder_path}
                     echo "{ssh_key}" > {folder_path}ssh_key
                     ls {folder_path}
                     cat {folder_path}ssh_key
                     ls {folder_path}
                     mkdir -p /home/airflow/.ssh
                     touch /home/airflow/.ssh/known_hosts
                     ssh-keyscan gitlab.intelligrape.net >> ~/.ssh/known_hosts
                     chmod 600 {folder_path}ssh_key
                     ssh-agent bash -c 'ssh-add {folder_path}ssh_key; git clone git@gitlab.intelligrape.net:tothenew/mycloud-scripts.git '
                     ls 
                     cd mycloud-scripts
                     ls
                     git checkout ck-data-pipeline-auto-demo-uat
                     python3 optimized_config/auto_ri_config.py 2023 10                     

    """,
    dag=dag,
)
refresh_buckets_data = BashOperator(
    task_id='refresh_buckets_data',
    bash_command=f"""pwd
                     mkdir -p {folder_path}
                     echo "{ssh_key}" > {folder_path}ssh_key
                     ls {folder_path}
                     cat {folder_path}ssh_key
                     ls {folder_path}
                     mkdir -p /home/airflow/.ssh
                     touch /home/airflow/.ssh/known_hosts
                     ssh-keyscan gitlab.intelligrape.net >> ~/.ssh/known_hosts
                     chmod 600 {folder_path}ssh_key
                     ssh-agent bash -c 'ssh-add {folder_path}ssh_key; git clone git@gitlab.intelligrape.net:tothenew/mycloud-scripts.git '
                     ls 
                     cd mycloud-scripts
                     ls
                     git checkout ck-master-refresh-emr-pipeline-auto-demo
                     python3 ck_auto_demo_emr/buckets_json.py
                     

    """,
    dag=dag,
)


