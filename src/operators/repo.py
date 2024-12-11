"""GitHub Operators for Airflow

This module provides custom Airflow operators for interacting with the GitHub API. These operators are used
to retrieve various data from a GitHub repository, including pull requests, branches, commits, and issues.
The operators authenticate with the GitHub API using a session retrieved from a previous task and interact
with the repository through the `Repo` class.

Operators:
- `GitHubOperator`: Base operator for setting up the repository session.
- `GitHubPullRequestOperator`: Retrieves pull requests from the specified GitHub repository.
- `GitHubBranchesOperator`: Retrieves branches from the specified GitHub repository.
- `GitHubCommitsOperator`: Retrieves commits from a specific branch of the repository.
- `GitHubIssuesOperator`: Retrieves issues from the repository with optional filters.

Dependencies:
- `Repo`: Interacts with the GitHub API to fetch repository data.
- `GitHubSession`: Manages the GitHub authentication and session handling."""

import pickle
import typing as t
from datetime import datetime

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from github.repo import Repo


class GitHubOperator(BaseOperator):
    """Base Airflow Operator for interacting with the GitHub API.
    This operator retrieves a GitHub session from XCom and creates a `Repo` object for interacting with a
    specified GitHub repository.
    :param owner: The owner of the repository (GitHub username or organization).
    :param repo_name: The name of the repository.
    :param session_name: The name of the session to retrieve from XCom.
    :param auth_task_id: The task ID of the task that retrieves the authentication token.
    :param kwargs: Additional arguments passed to the `BaseOperator`."""

    @apply_defaults
    def __init__(self, owner: str, repo_name: str, session_name: str, auth_task_id: str, **kwargs):
        """Initializes the GitHubOperator.
        :param owner: The owner of the repository (GitHub username or organization).
        :param repo_name: The name of the repository.
        :param session_name: The name of the session to retrieve from XCom.
        :param auth_task_id: The task ID of the task that retrieves the authentication token.
        :param kwargs: Additional arguments passed to the `BaseOperator`."""

        super().__init__(**kwargs)
        self.owner = owner
        self.repo_name = repo_name
        self.session_name = session_name
        self.auth_task_id = auth_task_id
        self.repo = None

    def execute(self, context):
        """Executes the GitHub operator by retrieving the session from XCom and initializing the `Repo` object.
        The session is deserialized from XCom, and a `Repo` object is created using the provided repository
        information (owner and name) and the authenticated session.
        :param context: The context dictionary passed by Airflow to the operator during execution."""

        ti = context['ti']
        session_serialized = ti.xcom_pull(task_ids=self.auth_task_id, key=self.session_name)
        session = pickle.loads(session_serialized)
        self.repo = Repo(owner=self.owner, repo_name=self.repo_name, session=session)


class GitHubPullRequestOperator(GitHubOperator):
    """Airflow Operator for retrieving pull requests from a GitHub repository.
    This operator fetches pull requests from the specified GitHub repository, with optional filters for
    draft status and state (open or closed).
    :param draft_only: Boolean flag to filter only draft pull requests.
    :param state: The state of the pull requests to retrieve (open or closed).
    :param kwargs: Additional arguments passed to the `GitHubOperator`."""

    @apply_defaults
    def __init__(self, draft_only=False, state: t.Literal['open', 'closed'] = 'open', **kwargs):
        """Initializes the GitHubPullRequestOperator.
        This method initializes the operator with options to filter pull requests by draft status and state
        (open or closed).
        :param draft_only: Boolean flag to filter only draft pull requests.
        :param state: The state of the pull requests to retrieve (open or closed).
        :param kwargs: Additional arguments passed to the `GitHubOperator`."""

        super().__init__(**kwargs)
        self.draft_only = draft_only
        self.state = state

    def execute(self, context):
        """Executes the pull request retrieval by calling the `pull_requests` method of the `Repo` object.
        :param context: The context dictionary passed by Airflow to the operator during execution.
        :return: Pull requests from the GitHub repository, possibly filtered by draft status and state."""

        super().execute(context)
        return self.repo.pull_requests(draft_only=self.draft_only, state=self.state)


class GitHubBranchesOperator(GitHubOperator):
    """Airflow Operator for retrieving branches from a GitHub repository.
    This operator fetches the branches from the specified GitHub repository."""

    def execute(self, context):
        """Executes the branch retrieval by accessing the `branches` property of the `Repo` object.
         :param context: The context dictionary passed by Airflow to the operator during execution.
         :return: A list of branch names from the GitHub repository."""

        super().execute(context)
        return self.repo.branches


class GitHubCommitsOperator(GitHubOperator):
    """Airflow Operator for retrieving commits from a GitHub repository.
    This operator fetches commits from a specific branch in the specified GitHub repository.
    Optional filters can be applied for author, date range (since and until), and the number of commits.
    :param branch: The branch to retrieve commits from.
    :param since: The starting date for filtering commits (optional).
    :param until: The ending date for filtering commits (optional).
    :param author: The author of the commits to filter (optional).
    :param n: The maximum number of commits to retrieve (default is 10).
    :param kwargs: Additional arguments passed to the `GitHubOperator`."""

    @apply_defaults
    def __init__(
            self,
            branch: str,
            since: t.Optional[datetime.date] = None,
            until: t.Optional[datetime.date] = None,
            author: t.Optional[str] = None,
            n: int = 10,
            **kwargs
    ):
        """Initializes the GitHubCommitsOperator.
        This method initializes the operator with parameters for fetching commits from a specific branch
        of the repository, with optional filters for author, date range (since and until), and number of commits.
        :param branch: The branch to retrieve commits from.
        :param since: The starting date for filtering commits (optional).
        :param until: The ending date for filtering commits (optional).
        :param author: The author of the commits to filter (optional).
        :param n: The maximum number of commits to retrieve (default is 10).
        :param kwargs: Additional arguments passed to the `GitHubOperator`."""

        super().__init__(**kwargs)
        self.since = since
        self.until = until
        self.branch = branch
        self.author = author
        self.n = n

    def execute(self, context):
        """Executes the commit retrieval by calling the `commits` method of the `Repo` object.
        :param context: The context dictionary passed by Airflow to the operator during execution.
        :return: Commits from the specified branch in the GitHub repository."""

        super().execute(context)
        return self.repo.commits(since=self.since, until=self.until, branch=self.branch, author=self.author, n=self.n)


class GitHubIssuesOperator(GitHubOperator):
    """Airflow Operator for retrieving issues from a GitHub repository.
    This operator fetches issues from the specified GitHub repository, with optional filters
    for labels, assignee, and milestone.
    :param labels: The labels to filter the issues by (optional).
    :param assignee: The assignee to filter the issues by (optional).
    :param milestone: The milestone to filter the issues by (optional).
    :param kwargs: Additional arguments passed to the `GitHubOperator`."""

    @apply_defaults
    def __init__(
            self,
            labels: t.Optional[str] = None,
            assignee: t.Optional[str] = None,
            milestone: t.Optional[str] = None,
            **kwargs
    ):
        """Initializes the GitHubIssuesOperator.
        This method initializes the operator with optional filters for retrieving issues from the GitHub repository,
        including labels, assignee, and milestone.
        :param labels: The labels to filter the issues by (optional).
        :param assignee: The assignee to filter the issues by (optional).
        :param milestone: The milestone to filter the issues by (optional).
        :param kwargs: Additional arguments passed to the `GitHubOperator`."""

        super().__init__(**kwargs)
        self.labels = labels
        self.assignee = assignee
        self.milestone = milestone

    def execute(self, context):
        """Executes the issue retrieval by calling the `issues` method of the `Repo` object.
        :param context: The context dictionary passed by Airflow to the operator during execution.
        :return: A list of issues from the GitHub repository, possibly filtered by labels, assignee, and milestone."""

        super().execute(context)
        return self.repo.issues(labels=self.labels, assignee=self.assignee, milestone=self.milestone)
