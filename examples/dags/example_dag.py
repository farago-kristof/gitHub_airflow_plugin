from datetime import datetime

from airflow import DAG

from operators.auth import GitHubAuthOperator
from operators.repo import GitHubPullRequestOperator
from operators.repo import GitHubIssuesOperator
from operators.repo import GitHubBranchesOperator
from operators.repo import GitHubCommitsOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
}

default_task_args = {
    'owner': 'farad213',
    'session_name': 'github_session',
    'auth_id': 'authenticate',
    'repo_name': 'fugro_3'
}

with DAG('github_dag', default_args=default_args, schedule_interval=None) as dag:
    authenticate = GitHubAuthOperator(
        task_id=default_task_args['auth_id'],
        session_name=default_task_args['session_name'],
        token='{{ var.value.github_token }}'
    )

    fetch_pull_requests = GitHubPullRequestOperator(
        task_id='fetch_pull_requests',
        draft_only=True,
        **default_task_args
    )

    fetch_branches = GitHubBranchesOperator(
        task_id='fetch_branches',
        **default_task_args
    )

    fetch_commits = GitHubCommitsOperator(
        task_id='fetch_commits',
        branch='dev',
        **default_task_args
    )

    fetch_issues = GitHubIssuesOperator(
        task_id='fetch_issues',
        assigne='farad213',
        **default_task_args
    )

    authenticate >> [fetch_pull_requests, fetch_branches, fetch_commits, fetch_issues]
