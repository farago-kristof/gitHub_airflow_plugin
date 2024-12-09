import typing as t
from datetime import datetime

from github.auth import GitHubSession
from utils.request import RequestBuilder


class Repo:
    BASE_URL = "https://api.github.com/repos"

    def __init__(self, owner: str, repo_name: str, session: t.Type[GitHubSession]) -> None:
        self.owner = owner
        self.repo_name = repo_name
        self.base_url = self.BASE_URL + "/" + self.owner + "/" + self.repo_name
        self.session = session

    @property
    def branches(self):
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
        endpoint = 'pulls'
        request_builder = RequestBuilder().set_method('GET').set_base_url(self.base_url).set_endpoint(endpoint)
        request_builder.add_query_param(state=state)
        request = request_builder.build()
        response = self.session.send_request(request)
        if draft_only:
            response = [pr for pr in response if pr.get('draft', False)]
        return response
