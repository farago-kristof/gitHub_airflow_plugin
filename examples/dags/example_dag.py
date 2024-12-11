from datetime import datetime

from airflow import DAG

from operators.auth import GitHubAuthOperator
from operators.repo import GitHubPullRequestOperator
from operators.repo import GitHubIssuesOperator
from operators.repo import GitHubBranchesOperator
from operators.repo import GitHubCommitsOperator
from airflow.operators.python import PythonOperator

# Default arguments for DAG and tasks
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
}

default_task_args = {
    'owner': 'farad213',
    'session_name': 'github_session',
    'auth_task_id': 'authenticate',
    'repo_name': 'fugro_3'
}

def log_xcom(**kwargs):
    """
    Logs the XCom pushed by the previous task.
    :param kwargs: Context variables provided by Airflow.
    """
    task_instance = kwargs['ti']
    task_id = kwargs['task_id']
    xcom_value = task_instance.xcom_pull(task_ids=task_id)
    print(f"XCom value from task {task_id}: {xcom_value}")

with DAG('github_dag', default_args=default_args, schedule_interval=None) as dag:
    authenticate = GitHubAuthOperator(
        task_id=default_task_args['auth_task_id'],
        session_name=default_task_args['session_name'],
        conn_id='github_conn_id'
    )

    fetch_pull_requests = GitHubPullRequestOperator(
        task_id='fetch_pull_requests',
        draft_only=True,
        **default_task_args
    )

    log_pull_requests = PythonOperator(
        task_id='log_pull_requests',
        python_callable=log_xcom,
        provide_context=True,
        op_kwargs={'task_id': 'fetch_pull_requests'}
    )

    fetch_branches = GitHubBranchesOperator(
        task_id='fetch_branches',
        **default_task_args
    )

    log_branches = PythonOperator(
        task_id='log_branches',
        python_callable=log_xcom,
        provide_context=True,
        op_kwargs={'task_id': 'fetch_branches'}
    )

    fetch_commits = GitHubCommitsOperator(
        task_id='fetch_commits',
        branch='dev',
        **default_task_args
    )

    log_commits = PythonOperator(
        task_id='log_commits',
        python_callable=log_xcom,
        provide_context=True,
        op_kwargs={'task_id': 'fetch_commits'}
    )

    fetch_issues = GitHubIssuesOperator(
        task_id='fetch_issues',
        assignee='farad213',
        **default_task_args
    )

    log_issues = PythonOperator(
        task_id='log_issues',
        python_callable=log_xcom,
        provide_context=True,
        op_kwargs={'task_id': 'fetch_issues'}
    )

    authenticate >> [fetch_pull_requests, fetch_branches, fetch_commits, fetch_issues]
    fetch_pull_requests >> log_pull_requests
    fetch_branches >> log_branches
    fetch_commits >> log_commits
    fetch_issues >> log_issues
