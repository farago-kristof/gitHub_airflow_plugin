import pickle
import typing as t

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from github.auth import GitHubSessionPool


class GitHubAuthOperator(BaseOperator):
    @apply_defaults
    def __init__(self, token: str, session_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.token = token
        self.session_name = session_name

    def execute(self, context: t.Dict) -> None:
        session = GitHubSessionPool().get_session(self.token)
        ti = context['ti']
        ti.xcom_push(key=self.session_name, value=pickle.dumps(session))
