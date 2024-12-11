import pickle
import typing as t

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base import BaseHook

from github.auth import GitHubSessionPool


class GitHubAuthOperator(BaseOperator):
    @apply_defaults
    def __init__(self, conn_id, session_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.token = self.retrieve_token(conn_id)
        self.session_name = session_name

    def execute(self, context: t.Dict) -> None:
        session = GitHubSessionPool().get_session(self.token)
        ti = context['ti']
        ti.xcom_push(key=self.session_name, value=pickle.dumps(session))

    @staticmethod
    def retrieve_token(conn_id):
        conn = BaseHook.get_connection(conn_id)
        return conn.password
