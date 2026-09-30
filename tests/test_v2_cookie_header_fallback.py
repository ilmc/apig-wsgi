from apig_wsgi import make_lambda_handler


def test_v2_cookie_header_only_has_no_leading_separator() -> None:
    observed = {}

    def app(environ, start_response):
        observed["cookie"] = environ["HTTP_COOKIE"]
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"ok"]

    handler = make_lambda_handler(app)
    handler(
        {
            "version": "2.0",
            "rawPath": "/",
            "rawQueryString": "",
            "headers": {
                "Host": "example.com",
                "Cookie": "session=abc",
            },
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

    assert observed["cookie"] == "session=abc"
