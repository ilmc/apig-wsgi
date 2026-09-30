from apig_wsgi import make_lambda_handler


def test_v2_combines_duplicate_response_headers() -> None:
    def app(environ, start_response):
        start_response(
            "200 OK",
            [
                ("Content-Type", "text/plain"),
                ("X-Test", "one"),
                ("X-Test", "two"),
            ],
        )
        return [b"ok"]

    handler = make_lambda_handler(app)
    response = handler(
        {
            "version": "2.0",
            "rawPath": "/",
            "rawQueryString": "",
            "headers": {"Host": "example.com"},
            "cookies": [],
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                    "sourceIp": "1.2.3.4",
                    "protocol": "HTTP/1.1",
                }
            },
            "body": "",
            "isBase64Encoded": False,
        },
        None,
    )

    assert response["headers"]["x-test"] == "one,two"
