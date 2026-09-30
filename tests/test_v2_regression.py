from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import pytest

from apig_wsgi import make_lambda_handler


DEFAULT_TEXT_CONTENT_TYPES = [
    "text/plain",
    "text/html",
    "application/json",
    "application/problem+json",
    "application/vnd.api+json",
]


def make_v2_event() -> dict[str, Any]:
    return {
        "version": "2.0",
        "rawQueryString": "",
        "rawPath": "/",
        "headers": {"Host": "example.com"},
        "cookies": [],
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "",
                "sourceIp": "1.2.3.4",
                "protocol": "https",
            }
        },
        "body": "",
        "isBase64Encoded": False,
    }


@pytest.mark.parametrize("text_content_type", DEFAULT_TEXT_CONTENT_TYPES)
def test_v2_encoded_text_response_is_binary(text_content_type: str) -> None:
    def app(
        environ: dict[str, Any],
        start_response: Callable[..., Callable[[bytes], int]],
    ) -> Iterable[bytes]:
        start_response(
            "200 OK",
            [
                ("Content-Type", text_content_type),
                ("Content-Encoding", "brotli"),
            ],
        )
        return [b"Hello World\n"]

    handler = make_lambda_handler(app, binary_support=True)

    response = handler(make_v2_event(), None)

    assert response == {
        "statusCode": 200,
        "cookies": [],
        "headers": {
            "content-type": text_content_type,
            "content-encoding": "brotli",
        },
        "isBase64Encoded": True,
        "body": "SGVsbG8gV29ybGQK",
    }
