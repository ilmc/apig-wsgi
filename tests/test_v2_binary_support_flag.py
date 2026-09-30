from apig_wsgi import make_lambda_handler


def test_v2_respects_explicit_binary_support_false() -> None:
    def app(environ, start_response):
        start_response("200 OK", [("Content-Type", "application/octet-stream")])
        return [b"binary-ish"]

    handler = make_lambda_handler(app, binary_support=False)
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

    assert response == {
        "statusCode": 200,
        "cookies": [],
        "headers": {"content-type": "application/octet-stream"},
        "isBase64Encoded": False,
        "body": "binary-ish",
    }
