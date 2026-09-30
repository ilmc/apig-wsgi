# Compatibility suite investigation 003

## Question

What durable compatibility knowledge is carried by the current test suite, and does that evidence justify reorganising the runtime and tests?

## Current shape

The project currently concentrates almost all behavioural coverage in `tests/test_apig_wsgi.py`, while almost all runtime behaviour lives in `src/apig_wsgi/__init__.py`.

The physical layout is compact, but the test file is not conceptually monolithic. It contains distinct compatibility domains that correspond closely to the runtime's real responsibilities.

## Behavioural knowledge preserved by the suite

### API Gateway format v1

The v1 tests preserve behaviour around:

- single-value and multi-value headers;
- single-value and multi-value query parameters;
- exact query-string encoding of `+`, `%`, and repeated values;
- path unquoting;
- request-body decoding and `CONTENT_LENGTH`;
- base64-encoded request bodies;
- special WSGI mappings for `Content-Type`, `Host`, `X-Forwarded-For`, `X-Forwarded-Proto`, and `X-Forwarded-Port`;
- missing and `None` headers as emitted by AWS test/invocation paths;
- request context exposure;
- full event exposure;
- Lambda context exposure;
- WSGI `exc_info` propagation;
- iterable response consumption, including empty chunks.

This is compatibility knowledge rather than incidental implementation coverage.

### Application Load Balancer

The ALB tests demonstrate a subtle distinction from API Gateway v1: ALB query-string values are already represented in a form where reserved URI characters must not be encoded again.

The tests explicitly distinguish values such as `+`, `%3D`, `%24`, and `%25` between API Gateway v1 and ALB behaviour. A bespoke rewrite that merely reused the API Gateway v1 query encoder could therefore be observably wrong while still appearing plausible.

The suite also covers ALB health-check events where host, port, and scheme information may be absent.

### API Gateway format v2

The v2 tests preserve another materially different contract:

- raw query strings are accepted directly;
- request cookies may arrive through the dedicated `cookies` collection;
- a residual `Cookie` header is defensively merged with that collection;
- response `Set-Cookie` headers are emitted through the v2 `cookies` response field rather than ordinary headers;
- output headers are normalized differently from v1;
- binary responses are enabled by default;
- request source IP and HTTP protocol come from the v2 request context.

These are protocol-shape differences, not merely alternative syntax for the same transformation.

### Binary response policy

The suite encodes a non-trivial content policy:

- textual and JSON-family content types normally remain text;
- custom non-binary prefixes can replace the defaults;
- a content encoding such as gzip or brotli forces binary transmission;
- missing content type can result in binary transmission where binary support is active;
- binary defaults differ between API Gateway v1, ALB, and v2.

This is one of the clearest examples of value that lies in accumulated tests rather than implementation volume.

### WSGI semantics

The tests also preserve framework-independent WSGI behaviour:

- `start_response` exception information must propagate correctly;
- yielded empty byte strings do not corrupt the response;
- response iterables are consumed according to WSGI semantics;
- the generated environ contains expected WSGI keys as well as `apig_wsgi` extension keys.

## Evidence of test-structure debt

The suite's conceptual domains are clearer than its physical structure.

One concrete example is in `TestV2Events`: `test_get_binary_support_default_text_content_types_encoded` is named and located as a v2 test but invokes `make_v1_event()`. Its assertions also expect the v1 `multiValueHeaders` response shape.

This gives a misleading impression of v2 coverage for that case. The finding does not demonstrate a runtime defect; it demonstrates that a large mixed test module can obscure which event family a test actually exercises.

A dedicated v2 regression test is added by this undertaking so that the intended v2 behaviour is exercised without altering upstream-derived runtime code.

## Architectural correspondence

The test domains map naturally onto the conceptual runtime boundaries already identified:

| Compatibility evidence | Runtime responsibility |
| --- | --- |
| event-family selection and unknown versions | event classification / handler orchestration |
| v1 and ALB query/header/path/body cases | request adaptation |
| v2 raw-query/cookie/context cases | request adaptation |
| status, headers, cookies and multi-value output | response adaptation |
| binary/media policy | response serialization policy |
| `exc_info`, iterable consumption and context | WSGI orchestration |

The correspondence is strong enough that physical reorganisation could improve auditability without requiring an architectural redesign.

## Judgement

There is evidence for reorganising the **tests** before reorganising the runtime.

The strongest durable asset is the compatibility matrix encoded by the tests. Splitting that matrix by event family and behaviour would make gaps and accidental cross-family coverage easier to detect while leaving production behaviour untouched.

There is not yet equally strong evidence that the runtime must be split. The implementation is small and internally coherent enough that additional modules could add navigation cost without reducing meaningful complexity.

## Next experiment

The next substantial experiment should reorganise tests by compatibility domain while preserving assertions and keeping runtime code unchanged. That experiment should be judged on whether it makes coverage claims easier to audit and maintain, not on whether it produces more files.

Only after that should the undertaking reconsider splitting the runtime into event classification, request adaptation, response adaptation, and orchestration modules.
