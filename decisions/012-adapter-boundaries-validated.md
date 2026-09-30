# Decision 012: keep adapter boundaries separate

## Status

Adopted after Investigation 011.

## Decision

Retain the existing scope decisions: `apig-wsgi` remains a WSGI-to-Lambda adapter and should not absorb ASGI or HTTP-process adaptation responsibilities.

Treat Mangum and AWS Lambda Web Adapter as neighboring solutions at different boundaries, not as feature backlogs for this package.

## Evidence

Current Mangum remains a direct ASGI-to-Lambda adapter supporting the major Lambda HTTP event sources and ASGI lifespan semantics.

Current AWS Lambda Web Adapter moves adaptation to a local HTTP-process boundary and includes process-oriented capabilities such as readiness checks, streaming, SnapStart hooks, and framework/language independence.

These are materially different responsibilities from translating Lambda events into WSGI calls.

## Consequences

- FastAPI/ASGI support is not a modernization target for `apig-wsgi`.
- HTTP server lifecycle/readiness/streaming features are not targets for this package.
- Future work should remain centered on WSGI/AWS correctness and preservation of compatibility knowledge.
- A deployed performance comparison remains optional evidence and must not be replaced with guessed benchmarks.

## Revisit trigger

Revisit only if the application-protocol boundary itself changes materially or if a concrete user problem cannot be served cleanly by the existing WSGI, ASGI, or HTTP-process options.
