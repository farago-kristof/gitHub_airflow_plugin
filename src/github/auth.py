"""GitHub Session and Session Pool Management

This module provides functionality for managing GitHub API requests using a session-based approach.
- `GitHubSession`: A class that manages a keep-alice TCP session with GitHub and provides a method to send requests to the GitHub API with retry logic.
- `GitHubSessionPool`: A singleton class that maintains a pool of `GitHubSession` objects, ensuring that a single session is reused for each unique GitHub token.

Decorators:
- `exponential_backoff`: Automatically retries GitHub API requests with exponential backoff in case of failures.
- `singleton`: Ensures that only one instance of the `GitHubSessionPool` class exists. Makes it easy to access it from anywhere in the code base.

Usage:
- `GitHubSession`: Used to send authenticated requests to GitHub's API with automatic retries. Has the token saved in headers.
- `GitHubSessionPool`: Used to manage and reuse `GitHubSession` objects based on unique tokens."""

import typing as t

import requests

from utils.decoartors import exponential_backoff
from utils.decoartors import singleton
from utils.request import Request


class GitHubSession:
    """A class that manages a keep-alive TCP session with GitHub's API.
    This class handles sending requests to the GitHub API using the `requests` library.
    It supports automatic retries with exponential backoff in case of failures.
    :param token: The GitHub Personal Access Token used for authentication.
    Methods:
    - `send_request(request: Request)`: Sends an HTTP request to the GitHub API with retry logic."""

    def __init__(self, token):
        """Initializes a GitHubSession with the provided token.
        Sets up the necessary headers for authentication and communication with
        the GitHub API, including setting the Authorization token and the required
        Accept header for the GitHub API version.
        :param token: The GitHub Personal Access Token to authenticate the session."""

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Connection": "keep-alive"
        })

    @exponential_backoff()
    def send_request(self, request: Request) -> t.Optional[t.Dict]:
        """Sends an HTTP request to the GitHub API with retry logic.
        This method uses the provided `GitHubRequest` object to send a request to the
        GitHub API. It automatically retries the request with exponential backoff
        if the request fails.
        :param request: A `GitHubRequest` object containing method, endpoint, params, or data to be sent.
        :return: The response from the GitHub API in JSON format, or None if the response content is empty.
        :raises RuntimeError: If the GitHub API request fails after retry attempts."""

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
    """A singleton class that manages a pool of GitHubSessions, ensuring that each
    session is associated with a unique token and is reused across requests.
    This class allows for efficient management of sessions, reducing the need to
    repeatedly re-initialize sessions for the same token.
    Methods:
    - `get_session(token: str)`: Retrieves an existing session from the pool or creates a new one if necessary.
    - `release_session(token: str)`: Releases the session from the pool and closes the session connection."""

    def __init__(self):
        self.pool = {}

    def get_session(self, token: str) -> GitHubSession:
        """Get an existing session from the pool, or create a new one if none exists.
        :param token: The GitHub Personal Access Token used to identify the session.
        :return: A `GitHubSession` object associated with the given token."""

        if token not in self.pool:
            self.pool[token] = GitHubSession(token)
        return self.pool[token]

    def release_session(self, token: str) -> None:
        """Release the session from the pool, if necessary.
        :param token: The GitHub Personal Access Token associated with the session to be released."""

        if token in self.pool:
            self.pool[token].session.close()
            del self.pool[token]
