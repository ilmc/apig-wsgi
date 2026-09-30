# Undertaking state

**As of 30 September 2026**

## Authority

`ilmc/apig-wsgi` is the writable authority for this undertaking.

`adamchainz/apig-wsgi` is read-only external evidence. Do not write upstream and do not create or comment on pull requests or issues as part of this undertaking.

## Current interpretation

`apig-wsgi` is a mature WSGI-to-Lambda compatibility utility.

Its continuing value is primarily:

- translating API Gateway/ALB/Function URL event semantics into WSGI behavior;
- preserving learned AWS edge cases;
- providing a compact direct-handler path for WSGI applications;
- retaining executable compatibility knowledge in tests.

ASGI does not invalidate this boundary. Mangum occupies the corresponding direct ASGI-to-Lambda boundary. AWS Lambda Web Adapter moves adaptation outward to an ordinary HTTP-process boundary.

The fork should not add ASGI/FastAPI support or HTTP-process lifecycle features merely to modernize its image.

## Runtime relationship to upstream

The fork remains structurally close to upstream, but now contains three intentional compatibility divergences:

1. **Payload v2 `binary_support=False`** — explicit `False` is honored instead of v2 always enabling binary response handling.
2. **Payload v2 Cookie-header fallback** — a header-only fallback no longer produces a leading semicolon in `HTTP_COOKIE`.
3. **Payload v2 duplicate response headers** — duplicate non-cookie WSGI response headers are comma-combined rather than silently losing earlier values.

Each divergence has a focused regression test and a record under `divergences/`.

## Deliberately rejected directions

Current evidence does not justify:

- adding ASGI or FastAPI support;
- turning the package into a multi-framework adapter;
- emulating AWS Lambda Web Adapter;
- splitting the compact runtime into architectural modules for aesthetics;
- automatically stripping API Gateway stage prefixes;
- publishing a separate fork distribution;
- replacing the implementation simply because AI can generate a small adapter quickly.

## Test and CI posture

The upstream-derived repository workflow defines a Python 3.10–3.15 matrix and a 100% coverage gate.

The fork currently shows no GitHub Actions workflow runs, including for direct `main` pushes. Therefore local changes must not be described as CI-verified.

Fork runtime changes should remain small, regression-backed and easy to compare with upstream until executable CI is observed.

## External ecosystem result

The adapter-boundary investigation found:

- `apig-wsgi`: direct WSGI callable ↔ Lambda events;
- Mangum: direct ASGI callable ↔ Lambda events;
- AWS Lambda Web Adapter: ordinary local HTTP server ↔ Lambda extension/runtime adapter.

These are neighboring architectural choices, not a linear replacement sequence.

## Maintenance mode

Default to observation and evidence-driven compatibility work.

Active runtime work should require a concrete behavioral inconsistency with a realistic event shape and a focused regression.

Do not create work merely to keep the fork active.

## Remaining optional experiments

Two experiments remain meaningful but are not required for the current scope conclusion:

1. **Deployed adapter-boundary measurements** — cold/warm behavior, package/image size, memory, and HTTP-process readiness overhead. This requires a real AWS deployment environment.
2. **AI bespoke-adapter control** — generate an implementation from an independent concise specification and compare it with the focused/full compatibility contracts. A genuinely blinded run should use a fresh context that has not inspected this implementation.

Neither experiment should be replaced by invented benchmark numbers or a contaminated claim of independent reimplementation.
