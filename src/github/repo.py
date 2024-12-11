"""GitHub Repository Interactions

This module provides a `Repo` class that simplifies interacting with a GitHub repository using the GitHub API.
It supports fetching information about branches, issues, commits, and pull requests. The class uses a
`GitHubSession` for authenticated communication with GitHub's API.

Usage:
- Instantiate the `Repo` class with the repository owner and name, as well as an authenticated `GitHubSession`.
- Use methods like `branches`, `issues`, `commits`, and `pull_requests` to interact with the repository data.

Dependencies:
- `GitHubSession`: Used for making authenticated requests to the GitHub API.
- `RequestBuilder`: A utility class for constructing requests to the GitHub API."""


import typing as t
from datetime import datetime

from github.auth import GitHubSession
from utils.request import RequestBuilder


class Repo:
    """A class that represents a GitHub repository and provides methods to interact with the repository
    using the GitHub API.
    This class supports fetching branches, issues, commits, and pull requests from a GitHub repository
    by utilizing a `GitHubSession` object for API communication.
    :param owner: The owner of the repository (e.g., 'octocat').
    :param repo_name: The name of the repository (e.g., 'Hello-World').
    :param session: A `GitHubSession` object to handle the authenticated session for API requests."""

    BASE_URL = "https://api.github.com/repos"

    def __init__(self, owner: str, repo_name: str, session: t.Type[GitHubSession]) -> None:
        """Initializes a `Repo` object for interacting with a GitHub repository.
        :param owner: The owner of the GitHub repository (e.g., 'octocat').
        :param repo_name: The name of the GitHub repository (e.g., 'Hello-World').
        :param session: An authenticated `GitHubSession` object to send requests to the GitHub API."""

        self.owner = owner
        self.repo_name = repo_name
        self.base_url = self.BASE_URL + "/" + self.owner + "/" + self.repo_name
        self.session = session

    @property
    def branches(self):
        """Fetches the list of branch names for the repository.
        This property sends a GET request to the 'branches' endpoint of the GitHub API
        and returns a list of branch names in the repository.
        :return: A list of branch names (e.g., ['main', 'dev', 'feature-branch'])."""

        endpoint = 'branches'
        request_builder = RequestBuilder().set_method('GET').set_base_url(self.base_url).set_endpoint(endpoint)
        request = request_builder.build()
        response = self.session.send_request(request)
        return [branch['name'] for branch in response]

    def issues(
            self,
            labels: t.Optional[str] = None,
            assignee: t.Optional[str] = None,
            milestone: t.Optional[str] = None
    ):
        """Fetches issues for the repository, with optional filtering by labels, assignee, and milestone.
        This method sends a GET request to the 'issues' endpoint of the GitHub API,
        and allows filtering by labels, assignee, and milestone.
        :param labels: A comma-separated string of labels to filter issues by.
        :param assignee: The GitHub username of the assignee to filter issues by.
        :param milestone: The milestone to filter issues by.
        :return: A list of issues returned by the GitHub API."""

        endpoint = 'issues'
        request_builder = RequestBuilder().set_method('GET').set_base_url(self.base_url).set_endpoint(endpoint)
        if labels:
            request_builder.add_query_param(labels=labels)
        if milestone:
            request_builder.add_query_param(milestone=milestone)
        if assignee:
            request_builder.add_query_param(assignee=assignee)
        request = request_builder.build()
        response = self.session.send_request(request)
        return response

    def commits(
            self,
            branch: str,
            since: t.Optional[datetime.date] = None,
            until: t.Optional[datetime.date] = None,
            author: t.Optional[str] = None,
            n: int = 10
    ):
        """Fetches commits for a specific branch in the repository, with optional filtering by date range and author.
        This method sends a GET request to the 'commits' endpoint of the GitHub API and
        supports filtering by branch, date range (`since` and `until`), and author.
        :param branch: The branch name (e.g., 'main') to fetch commits from.
        :param since: The start date for filtering commits (optional).
        :param until: The end date for filtering commits (optional).
        :param author: The GitHub username of the author to filter commits by (optional).
        :param n: The number of commits to retrieve (defaults to 10, with a max of 100).
        :return: A list of commits returned by the GitHub API."""

        endpoint = 'commits'
        request_builder = RequestBuilder().set_method('GET').set_base_url(self.base_url).set_endpoint(endpoint)
        request_builder.add_query_param(sha=branch).add_query_param(per_page=min(n, 100))
        if author:
            request_builder.add_query_param(author=author)
        if since:
            iso8601_str = since.strftime('%Y-%m-%dT%H:%M:%SZ')
            request_builder.add_query_param(since=iso8601_str)
        if until:
            iso8601_str = until.strftime('%Y-%m-%dT%H:%M:%SZ')
            request_builder.add_query_param(until=iso8601_str)
        request = request_builder.build()
        response = self.session.send_request(request)
        return response

    def pull_requests(self, draft_only=False, state: t.Literal['open', 'closed'] = 'open'):
        """Fetches pull requests for the repository, with optional filtering by draft status and state.
        This method sends a GET request to the 'pulls' endpoint of the GitHub API,
        and allows filtering by state (`open` or `closed`) and draft status.
        :param draft_only: Whether to return only draft pull requests (defaults to False).
        :param state: The state of the pull requests to retrieve (`open` or `closed`).
        :return: A list of pull requests returned by the GitHub API."""

        endpoint = 'pulls'
        request_builder = RequestBuilder().set_method('GET').set_base_url(self.base_url).set_endpoint(endpoint)
        request_builder.add_query_param(state=state)
        request = request_builder.build()
        response = self.session.send_request(request)
        if draft_only:
            response = [pr for pr in response if pr.get('draft', False)]
        return response
