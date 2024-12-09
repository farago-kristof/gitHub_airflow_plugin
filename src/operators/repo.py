import pickle
import typing as t
from datetime import datetime

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from github.repo import Repo


class GitHubOperator(BaseOperator):
    @apply_defaults
    def __init__(self, owner: str, repo_name: str, session_name: str, auth_task_id: str, **kwargs):
        super().__init__(**kwargs)
        self.owner = owner
        self.repo_name = repo_name
        self.session_name = session_name
        self.auth_task_id = auth_task_id
        self.repo = None

    def execute(self, context):
        ti = context['ti']
        session_serialized = ti.xcom_pull(task_ids=self.auth_task_id, key=self.session_name)
        session = pickle.loads(session_serialized)
        self.repo = Repo(owner=self.owner, repo_name=self.repo_name, session=session)


class GitHubPullRequestOperator(GitHubOperator):
    @apply_defaults
    def __init__(self, draft_only=False, state: t.Literal['open', 'closed'] = 'open', **kwargs):
        super().__init__(**kwargs)
        self.draft_only = draft_only
        self.state = state

    def execute(self, context):
        super().execute(context)
        return self.repo.pull_requests(draft_only=self.draft_only, state=self.state)


class GitHubBranchesOperator(GitHubOperator):
    def execute(self, context):
        super().execute(context)
        return self.repo.branches


class GitHubCommitsOperator(GitHubOperator):
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
        super().__init__(**kwargs)
        self.since = since
        self.until = until
        self.branch = branch
        self.author = author
        self.n = n

    def execute(self, context):
        super().execute(context)
        return self.repo.commits(since=self.since, until=self.until, branch=self.branch, author=self.author, n=self.n)


class GitHubIssuesOperator(GitHubOperator):
    @apply_defaults
    def __init__(
            self,
            labels: t.Optional[str] = None,
            assignee: t.Optional[str] = None,
            milestone: t.Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.labels = labels
        self.assignee = assignee
        self.milestone = milestone

    def execute(self, context):
        super().execute(context)
        return self.repo.issues(labels=self.labels, assignee=self.assignee, milestone=self.milestone)
