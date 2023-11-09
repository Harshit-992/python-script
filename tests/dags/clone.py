from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import os
from datetime import datetime, timedelta
from airflow.hooks.base_hook import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookHook

def task_failure_callback(context):
    slack_msg = f"""
    :red_circle: Airflow Task Failed.
    *Task*: {context.get('task_instance').task_id}
    *Dag*: {context.get('task_instance').dag_id}
    *Execution Time*: {context.get('execution_date')}
    *Log Url*: {context.get('task_instance').log_url}
    """

    slack_hook = SlackWebhookHook(slack_webhook_conn_id='slack_conn')
    slack_hook.send(text=slack_msg)

def task_success_callback(context):
    slack_msg = f"""
    :large_green_circle: Airflow Task Succeded.
    *Task*: {context.get('task_instance').task_id}
    *Dag*: {context.get('task_instance').dag_id}
    *Execution Time*: {context.get('execution_date')}
    *Log Url*: {context.get('task_instance').log_url}
    """

    slack_hook = SlackWebhookHook(slack_webhook_conn_id='slack_conn')
    slack_hook.send(text=slack_msg)
    
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 0,
    'on_failure_callback': task_failure_callback
}

dag = DAG(
    'auto_demo_processing',
    default_args=default_args,
    description='Clone a GitLab repository using SSH key',
    schedule_interval=None,  
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
                     git branch
                     git checkout prod-merge-CKPIP-28
                     git branch
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt about
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt clean
                     /home/airflow/.sdkman/candidates/sbt/1.9.7/bin/sbt assembly
                     aws s3 cp target/scala-2.12/CkDataProcessEngine-assembly-0.1.jar  s3://ck-data-pipeline-auto-demo-config-prod-data/spark_utility/92/
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
refresh_data = BashOperator(
    task_id='refresh_data',
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
                     python3 ck_auto_demo_emr/main.py --year 2023 --month 10 --app ck-auto-demo --env prod --build_number 92 --flow refresh-data --template payer --payer '674600239845,741843927392' --core_node_spot_percent 80

    """,
    dag=dag,
)
emr_process = BashOperator(
    task_id='emr_process',
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
                     python3 ck_auto_demo_emr/main.py --year 2023 --month 10 --app ck-auto-demo --env prod --build_number 92 --flow process-data --template payer --payer '674600239845,741843927392' --core_node_spot_percent 80
                     python3 ck_auto_demo_emr/main.py --year 2023 --month 10 --app ck-auto-demo --env prod --build_number 92 --flow terminate-cluster --template payer --payer '674600239845,741843927392' --core_node_spot_percent 80
                     
    """,
    dag=dag,
    on_success_callback=task_success_callback
)
master_refresh = BashOperator(
    task_id='master_refresh',
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
                     git checkout ck-payer-analytics-snowflake-demo
                     python3 ck_auto_emr_demo/main.py --year 2023 --month 10 --env 'prod' --payer '674600239845,741843927392' --build_number '92'
                   
    """,
    dag=dag,
)
[build_jar, ri_config, refresh_data] >> emr_process >> master_refresh
