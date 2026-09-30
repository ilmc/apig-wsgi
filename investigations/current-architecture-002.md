# Current architecture 002

## Question

What responsibilities does the current implementation actually contain, and where are its durable compatibility assets?

## Current source shape

At the establishment baseline, most runtime behavior lives in `src/apig_wsgi/__init__.py` and most behavioral coverage lives in `tests/test_apig_wsgi.py`.

The runtime module combines several distinct responsibilities:

1. Lambda event classification.
2. Request body decoding.
3. API Gateway/ALB event to WSGI environ translation.
4. WSGI application invocation.
5. WSGI response capture.
6. Binary-response policy.
7. API Gateway/ALB response serialization.

This is compact rather than inherently incorrect. The concern is whether the physical layout makes future reasoning, comparison and maintenance harder than necessary.

## Architectural map

```text
Lambda event + context
        ↓
 event classification
        ↓
 request translation
        ↓
    WSGI environ
        ↓
   WSGI application
        ↓
 status + headers + body
        ↓
 response translation
        ↓
 Lambda proxy response
```

The central orchestration is small. Most compatibility complexity belongs at the two translation boundaries.

## Candidate internal boundaries

A behavior-preserving reorganization, if evidence supports it, could expose these responsibilities as:

- `events.py` — event kind detection and event-shape concerns;
- `request.py` — body decoding and WSGI environ construction;
- `response.py` — WSGI response capture, binary policy and Lambda serialization;
- `handler.py` — orchestration around the WSGI application;
- `__init__.py` — stable public export of `make_lambda_handler`;
- `compat.py` — compatibility typing already separated today.

This is a candidate map, not an approved refactor.

## Public API constraint

The established external entry point should remain:

```python
from apig_wsgi import make_lambda_handler
```

A source reorganization should initially have zero intended observable behavior change.

## Test-suite interpretation

The test suite should be treated as an executable compatibility specification rather than merely refactor safety.

The likely durable asset is coverage of behavior such as:

- API Gateway v1 and v2 event differences;
- ALB event behavior;
- query-string handling;
- single- and multi-value headers;
- cookies;
- request context and Lambda context exposure;
- body and base64 handling;
- response headers and duplicate headers;
- binary media decisions and base64 output;
- WSGI response lifecycle details.

These cases represent accumulated knowledge that is costlier to recreate reliably than the small adapter implementation itself.

## Candidate test organization

If a reorganization is later justified, tests could be grouped by externally meaningful behavior rather than internal functions, for example:

```text
tests/
    request/
        test_apig_v1.py
        test_apig_v2.py
        test_alb.py
    response/
        test_apig_v1.py
        test_apig_v2.py
        test_binary.py
        test_headers.py
        test_cookies.py
    test_handler.py
```

Again, this is a hypothesis. Moving tests without a measurable comprehension or maintenance benefit would be churn.

## Decision threshold for refactoring

Proceed with a behavior-preserving split only if at least one material benefit can be demonstrated, such as:

- easier mapping between behavior and tests;
- clearer comparison with alternative Lambda adapters;
- reduced coupling when fixing or extending one event format;
- easier contributor comprehension;
- simpler review of future compatibility changes.

Do not refactor solely because multiple files appear cleaner.

## Current judgement

The implementation already has clear conceptual boundaries even though they are physically co-located. The immediate asset to preserve is behavior, especially the compatibility knowledge encoded in tests.

No runtime change is yet justified.
