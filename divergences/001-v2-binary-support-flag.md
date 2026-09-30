# Divergence 001: respect `binary_support=False` for payload format v2

## Status

Active fork-only runtime divergence.

## Summary

`ilmc/apig-wsgi` differs from the current upstream behavior for API Gateway payload format v2 when `make_lambda_handler(..., binary_support=False)` is used.

The public API documents `binary_support` as controlling whether binary responses are supported, with `None` selecting event-family defaults. Upstream v1 and ALB handling honor explicit boolean values, while payload format v2 constructs its response with binary support enabled unconditionally.

The fork changes the v2 response construction from unconditional `True` to:

```python
True if binary_support is None else binary_support
```

This preserves the established v2 default while honoring an explicit `False`.

## Evidence

The fork contains a regression test using a payload format v2 event and an `application/octet-stream` response whose bytes are valid UTF-8. This makes the option behavior directly observable:

- default/`None`: binary handling remains enabled for v2;
- explicit `False`: response remains plain with `isBase64Encoded=False`.

## Scope

This is intentionally narrow:

- one runtime expression;
- one focused regression test;
- no new public parameter;
- no event-family redesign;
- no structural refactor.

## Upstream relationship

`adamchainz/apig-wsgi` is read-only evidence for this undertaking. Do not open or comment on an upstream issue or pull request for this divergence.

When comparing with upstream in future, check whether upstream independently changes the same behavior. If it does, reassess whether this divergence can disappear naturally during synchronization.

## Revisit trigger

Revisit if:

- upstream independently honors explicit v2 `binary_support=False`;
- AWS changes payload v2 binary-response semantics;
- the documented option semantics are intentionally narrowed upstream;
- a regression demonstrates that disabling v2 binary support is invalid or misleading.
