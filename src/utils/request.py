"""This module defines a `Request` class to represent HTTP requests and a `RequestBuilder` class for constructing
requests in a flexible and fluent manner.

- `Request`: A data class representing an HTTP request, including attributes for method, endpoint, base URL,
  query parameters, data, JSON body, and headers. The `url` property constructs the full URL from the base URL
  and endpoint, while the `validate` method checks the required fields.

- `RequestBuilder`: A builder class for constructing `Request` objects. It provides methods for setting the HTTP
  method, endpoint, base URL, query parameters, data, JSON body, and headers. The `build` method validates the
  constructed request and returns it.

Usage example:
    request = RequestBuilder().set_method("GET").set_base_url("https://api.github.com").set_endpoint("repos/owner/repo/pulls").build()
    print(request.endpoint)  # Outputs: 'repos/owner/repo/pulls'"""


from dataclasses import dataclass
from dataclasses import field
import typing as t


@dataclass
class Request:
    """Represents an HTTP request with method, endpoint, base URL, query parameters,
    data, JSON body, and headers.
    :param method: HTTP method (e.g., 'GET', 'POST').
    :param endpoint: The endpoint to be appended to the base URL.
    :param base_url: The base URL for the API.
    :param query_params: Dictionary of query parameters to be included in the request.
    :param data: Dictionary of data to be sent in the body of the request (e.g., for 'POST' requests).
    :param json: JSON payload to be sent in the body of the request.
    :param headers: Dictionary of headers to be sent with the request.
    :property url: Constructs the full URL by combining the base URL and endpoint.
    :raises ValueError: If the method, base URL, or endpoint is not provided."""

    method: t.Optional[str] = None
    endpoint: t.Optional[str] = None
    base_url: t.Optional[str] = None
    query_params: t.Dict[str, t.Any] = field(default_factory=dict)
    data: t.Dict[str, t.Any] = field(default_factory=dict)
    json: t.Dict[str, t.Any] = field(default_factory=dict)
    headers: t.Dict[str, t.Any] = field(default_factory=dict)

    @property
    def url(self):
        """Constructs the full URL by combining the base URL and endpoint.
        :return: The full URL as a string."""

        return f'{self.base_url}/{self.endpoint}'

    def validate(self):
        """Validates the required fields of the request.
        :raises ValueError: If the HTTP method, base URL, or endpoint is missing."""

        if not self.method:
            raise ValueError("HTTP method is required.")
        if not self.base_url:
            raise ValueError("Base URL is required.")
        if not self.endpoint:
            raise ValueError("Endpoint is required.")


class RequestBuilder:
    """A builder class for constructing a `Request` object by providing a fluent interface
    to set HTTP method, endpoint, base URL, query parameters, data, JSON body, and headers.
    Usage:
        request = RequestBuilder().set_method("GET").set_base_url("https://api.github.com").set_endpoint("repos/owner/repo/pulls").build()
    :param _request: The `Request` object being constructed."""

    def __init__(self):
        """Initializes a new `RequestBuilder` instance with an empty `Request` object."""

        self._request = Request()

    def set_method(self, method):
        """Sets the HTTP method for the request.
        :param method: The HTTP method (e.g., 'GET', 'POST').
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.method = method
        return self

    def set_endpoint(self, endpoint: str):
        """Sets the endpoint for the request.
        :param endpoint: The API endpoint to append to the base URL.
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.endpoint = endpoint
        return self

    def set_base_url(self, base_url: str):
        """Sets the base URL for the request.
        :param base_url: The base URL (e.g., 'https://api.github.com').
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.base_url = base_url
        return self

    def add_query_param(self, **kwargs: t.Dict[str, t.Any]):
        """Adds query parameters to the request.
        :param kwargs: Key-value pairs of query parameters to add.
        :return? The `RequestBuilder` instance to allow for method chaining."""

        self._request.query_params.update(kwargs)
        return self

    def set_data(self, **kwargs):
        """Sets the data to be sent in the body of the request.
        :param kwargs: Key-value pairs of data to send in the request body.
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.data.update(kwargs)
        return self

    def set_json(self, **kwargs):
        """Sets the JSON payload to be sent in the body of the request.
        :param kwargs: Key-value pairs to send as JSON.
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.json.update(kwargs)
        return self

    def set_headers(self, **kwargs):
        """Adds headers to the request.
        :param kwargs: Key-value pairs of headers to add.
        :return: The `RequestBuilder` instance to allow for method chaining."""

        self._request.headers.update(kwargs)
        return self

    def build(self) -> Request:
        """Builds the final `Request` object after validation.
        :return: The constructed `Request` object.
        :raises ValueError: If the request is not valid (method, base URL, or endpoint missing)."""

        self._request.validate()
        request = self._request
        self._request = Request()
        return request
