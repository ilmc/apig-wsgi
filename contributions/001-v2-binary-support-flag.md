# Contribution 001: respect `binary_support=False` for v2 events

## Status

Implemented in this fork and pending upstream submission.

## Problem

`make_lambda_handler()` documents `binary_support` as controlling whether binary responses are supported, with `None` selecting the event-family default.

API Gateway v1 and ALB preserve explicit `True`/`False` values. Payload format v2 previously ignored an explicit `False` by constructing:

```python
V2Response(binary_support=True, ...)
```

This meant a caller could not disable v2 binary response handling even though the public option implied that behavior.

## Fork fix

Fork PR #6 changed v2 response construction to:

```python
binary_support=True if binary_support is None else binary_support
```

This preserves the existing v2 default while respecting an explicit boolean.

A focused regression test verifies that an `application/octet-stream` response containing UTF-8-safe bytes remains plain when `binary_support=False`.

## Upstream disposition

This is a generally useful correctness fix and should normally live in `adamchainz/apig-wsgi` rather than as permanent fork divergence.

The connected GitHub integration attempted to open an upstream PR but received HTTP 403 (`Resource not accessible by integration`).

The source branch remains:

`ilmc/apig-wsgi:fix/v2-binary-support-flag`

Suggested upstream PR title:

> Respect binary_support=False for v2 events

Suggested summary:

> Respect an explicit `binary_support=False` for API Gateway payload format v2 events. Keep the current v2 default when the argument is `None`, but pass through explicit boolean values. Add a regression demonstrating the documented option semantics.

## Fork policy

Keep this divergence explicit until one of the following happens:

1. upstream accepts the fix;
2. upstream rejects it with reasoning that changes the undertaking's interpretation of the option;
3. upstream independently changes the same behavior.

At that point, reconcile the fork with upstream rather than retaining duplicate behavior unnecessarily.