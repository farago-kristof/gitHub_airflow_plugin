from dataclasses import dataclass
from dataclasses import field
import typing as t


@dataclass
class Request:
    method: t.Optional[str] = None
    endpoint: t.Optional[str] = None
    base_url: t.Optional[str] = None
    query_params: t.Dict[str, t.Any] = field(default_factory=dict)
    data: t.Dict[str, t.Any] = field(default_factory=dict)
    json: t.Dict[str, t.Any] = field(default_factory=dict)
    headers: t.Dict[str, t.Any] = field(default_factory=dict)

    @property
    def url(self):
        return f'{self.base_url}/{self.endpoint}'

    def validate(self):
        if not self.method:
            raise ValueError("HTTP method is required.")
        if not self.base_url:
            raise ValueError("Base URL is required.")
        if not self.endpoint:
            raise ValueError("Endpoint is required.")


class RequestBuilder:
    def __init__(self):
        self._request = Request()

    def set_method(self, method):
        self._request.method = method
        return self

    def set_endpoint(self, endpoint):
        self._request.endpoint = endpoint
        return self

    def set_base_url(self, base_url):
        self._request.base_url = base_url
        return self

    def add_query_param(self, **kwargs):
        self._request.query_params.update(kwargs)
        return self

    def set_data(self, **kwargs):
        self._request.data.update(kwargs)
        return self

    def set_json(self, **kwargs):
        self._request.json.update(kwargs)
        return self

    def set_headers(self, **kwargs):
        self._request.headers.update(kwargs)
        return self

    def build(self):
        self._request.validate()
        request = self._request
        self._request = Request()
        return request


req = RequestBuilder().set_method("GET").set_base_url("https://api.github.com").set_endpoint("repos/owner/repo/pulls").build()
print(req.endpoint)