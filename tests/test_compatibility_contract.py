from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from apig_wsgi import make_lambda_handler


def recording_app(
    response_headers: list[tuple[str, str]] | None = None,
    response_body: bytes = b"ok",
) -> tuple[Callable[..., Iterable[bytes]], dict[str, Any]]:
    observed: dict[str, Any] = {}

    def app(
        environ: dict[str, Any],
        start_response: Callable[..., Callable[[bytes], int]],
    ) -> Iterable[bytes]:
        observed["environ"] = environ
        start_response("200 OK", response_headers or [("Content-Type", "text/plain")])
        return [response_body]

    return app, observed


def test_alb_query_string_preserves_already_encoded_reserved_characters() -> None:
    app, observed = recording_app()
    handler = make_lambda_handler(app)
    event = {
        "requestContext": {"elb": {"targetGroupArn": "arn:example"}},
        "httpMethod": "GET",
        "path": "/",
        "queryStringParameters": {"a": "foo%3Dbar+plus"},
        "headers": {"Host": "example.com"},
        "body": "",
        "isBase64Encoded": False,
    }

    handler(event, None)

    assert observed["environ"]["QUERY_STRING"] == "a=foo%3Dbar+plus"


def test_v2_merges_cookie_collection_and_cookie_header() -> None:
    app, observed = recording_app()
    handler = make_lambda_handler(app)
    event = {
        "version": "2.0",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "Host": "example.com",
            "Cookie": "second=2",
        },
        "cookies": ["first=1"],
        "requestContext": {
            "http": {
                "method": "GET",
                "sourceIp": "1.2.3.4",
                "protocol": "HTTP/1.1",
            }
        },
        "body": "",
        "isBase64Encoded": False,
    }

    handler(event, None)

    assert observed["environ"]["HTTP_COOKIE"] == "first=1;second=2"


def test_binary_defaults_differ_between_v1_and_alb() -> None:
    app, _ = recording_app(
        response_headers=[("Content-Type", "application/octet-stream")],
        response_body=b"\x13\x37",
    )
    handler = make_lambda_handler(app)

    v1_response = handler(
        {
            "version": "1.0",
            "httpMethod": "GET",
            "path": "/",
            "headers": {"Host": "example.com"},
            "queryStringParameters": None,
            "body": "",
            "isBase64Encoded": False,
        },
        None,
    )
    alb_response = handler(
        {
            "requestContext": {"elb": {"targetGroupArn": "arn:example"}},
            "httpMethod": "GET",
            "path": "/",
            "headers": {"Host": "example.com"},
            "queryStringParameters": None,
            "body": "",
            "isBase64Encoded": False,
        },
        None,
    )

    assert v1_response["isBase64Encoded"] is False
    assert alb_response["isBase64Encoded"] is True


def test_response_iterable_is_closed_after_consumption() -> None:
    observed: dict[str, bool] = {"closed": False}

    class ResponseIterable:
        def __iter__(self):
            yield b"hello"
            yield b""
            yield b" world"

        def close(self) -> None:
            observed["closed"] = True

    def app(environ, start_response):
        start_response("200 OK", [("Content-Type", "text/plain")])
        return ResponseIterable()

    handler = make_lambda_handler(app)
    response = handler(
        {
            "version": "1.0",
            "httpMethod": "GET",
            "path": "/",
            "headers": {"Host": "example.com"},
            "queryStringParameters": None,
            "body": "",
            "isBase64Encoded": False,
        },
        None,
    )

    assert response["body"] == "hello world"
    assert observed["closed"] is True
