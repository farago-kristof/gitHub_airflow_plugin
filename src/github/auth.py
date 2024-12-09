import typing as t

import requests

from utils.decoartors import exponential_backoff
from utils.decoartors import singleton
from utils.request import Request


class GitHubSession:

    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Connection": "keep-alive"
        })

    @exponential_backoff()
    def send_request(self, request: Request) -> t.Optional[t.Dict]:
        """Sends an HTTP request to the GitHub API with retry logic.
        :param request: A GitHubRequest object containing method, endpoint, params, or data.
        :return: The response from the GitHub API (typically JSON)."""

        try:
            response = self.session.request(
                request.method,
                request.url,
                params=request.query_params,
                data=request.data,
                json=request.json
            )
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GitHub API request failed: {e}") from e


@singleton
class GitHubSessionPool:
    def __init__(self):
        self.pool = {}

    def get_session(self, token: str) -> GitHubSession:
        """Get an existing session from the pool, or create a new one if none exists."""
        if token not in self.pool:
            self.pool[token] = GitHubSession(token)
        return self.pool[token]

    def release_session(self, token: str):
        """Release the session from the pool, if necessary."""
        if token in self.pool:
            self.pool[token].session.close()
            del self.pool[token]
