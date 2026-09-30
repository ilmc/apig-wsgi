# Decision 001: Preserve WSGI scope

## Status

Adopted provisionally on 30 September 2026.

## Decision

Do not add ASGI or FastAPI support to `apig-wsgi` as an initial direction for this undertaking.

## Rationale

`apig-wsgi` has a clear and mature responsibility: adapt AWS Lambda proxy events and responses to the WSGI interface.

ASGI applications represent a different application interface and already have dedicated adapter approaches. AWS Lambda Web Adapter also moves adaptation to an HTTP-process boundary rather than a WSGI/ASGI callable boundary.

Adding ASGI support merely because ASGI is now common would blur the package's responsibility before evidence shows a user problem that this repository is uniquely suited to solve.

The existence of newer approaches is therefore an investigation topic, not by itself a feature request.

## Consequences

- Preserve the existing WSGI public API and behavior by default.
- Compare newer Lambda integration approaches externally before considering scope expansion.
- Prefer upstream-compatible maintenance improvements over fork-specific feature growth.
- Revisit this decision only if evidence identifies a concrete unmet need that cannot be served more cleanly by existing ASGI or HTTP-process adapters.
