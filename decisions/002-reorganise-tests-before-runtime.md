# Decision 002: reorganise tests before runtime

## Status

Adopted for this undertaking.

## Context

The current runtime is concentrated in `src/apig_wsgi/__init__.py` and the behavioural suite in `tests/test_apig_wsgi.py`.

Investigation 003 found that the tests preserve substantial compatibility knowledge across API Gateway v1, API Gateway v2, ALB, WSGI semantics, binary response policy, query encoding, cookies, and AWS-specific edge cases.

It also found a concrete auditability problem: a test located and named as a v2 encoded-response test invokes a v1 event and asserts the v1 response shape.

## Decision

Reorganise the tests by compatibility domain before reorganising production code.

Do not split the runtime merely because conceptual boundaries can be named.

A runtime reorganisation must be justified by evidence from the test-layout experiment that the current production layout materially impedes comprehension, maintenance, or safe change.

## Constraints

The test reorganisation should:

- preserve public runtime behaviour;
- preserve existing behavioural assertions unless an assertion is demonstrated to be mislabeled or incorrect;
- make event-family coverage auditable;
- avoid introducing shared test abstractions that hide the event shapes under test;
- keep AWS protocol distinctions explicit;
- prefer compatibility-domain names over implementation-oriented names.

## Immediate consequence

A dedicated regression test now exercises the intended API Gateway v2 encoded-text response path directly.

The next substantial experiment may split the monolithic suite into event-family and cross-cutting compatibility modules. It should remain a test-only change unless the experiment itself reveals a concrete production-code problem.
