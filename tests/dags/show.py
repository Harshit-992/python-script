from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow import DAG
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
    
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 0,
    'on_failure_callback': task_failure_callback
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
    bash_command='pw',
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
