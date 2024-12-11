"""GitHub Authentication Operator for Airflow

This module provides a custom Airflow operator, `GitHubAuthOperator`, which authenticates with the GitHub API
and stores the session in XCom for further tasks. The operator retrieves a GitHub token from the Airflow
connection configuration and establishes an authenticated session using `GitHubSessionPool`.

Usage:
- The operator retrieves the authentication token using a connection ID and creates a session.
- The session is then serialized and pushed to XCom to be used by subsequent tasks.

Dependencies:
- `GitHubSessionPool`: Used to manage GitHub API sessions.
- `BaseHook`: Used to fetch the connection details (specifically, the token) from Airflow's connection management system."""


import pickle
import typing as t

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base import BaseHook

from github.auth import GitHubSessionPool


class GitHubAuthOperator(BaseOperator):
    """Airflow Operator to authenticate with the GitHub API and manage GitHub sessions.
    This operator retrieves a GitHub token from Airflow's connection management system,
    creates a keep-alive TCP session using the token, and stores the session in XCom.
    :param conn_id: The Airflow connection ID that contains the GitHub token.
    :param session_name: The name to associate with the GitHub session for use in downstream tasks.
    :param kwargs: Additional arguments to pass to the Airflow `BaseOperator`."""

    @apply_defaults
    def __init__(self, conn_id, session_name: str, **kwargs) -> None:
        """Initializes the GitHubAuthOperator, retrieves the GitHub token, and prepares session details.
        :param conn_id: The Airflow connection ID used to retrieve the GitHub token.
        :param session_name: The name to associate with the GitHub session, to be used in downstream tasks.
        :param kwargs: Additional arguments passed to the `BaseOperator` initialization."""

        super().__init__(**kwargs)
        self.token = self.retrieve_token(conn_id)
        self.session_name = session_name

    def execute(self, context: t.Dict) -> None:
        """Executes the authentication process by retrieving the GitHub session and pushing it to XCom.
        The session is created by calling `GitHubSessionPool().get_session` with the retrieved token.
        The session is serialized using `pickle` and pushed to XCom for use in downstream tasks.
        :param context: The context dictionary passed by Airflow to the operator during execution."""

        session = GitHubSessionPool().get_session(self.token)
        ti = context['ti']
        ti.xcom_push(key=self.session_name, value=pickle.dumps(session))

    @staticmethod
    def retrieve_token(conn_id):
        """Retrieves the GitHub token from Airflow's connection configuration.
        This method fetches the connection details for the provided connection ID and
        returns the password field, which is expected to be the GitHub token.
        :param conn_id: The Airflow connection ID from which the GitHub token is retrieved.
        :return: The GitHub token (password field of the connection)."""

        conn = BaseHook.get_connection(conn_id)
        return conn.password
