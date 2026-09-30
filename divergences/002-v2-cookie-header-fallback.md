# Divergence 002: avoid a leading separator in v2 Cookie-header fallback

## Status

Active fork-only compatibility fix.

## Summary

Payload format v2 normally provides parsed cookies in the event `cookies` collection. The runtime also contains an explicit defensive fallback for a `Cookie` header that remains in `headers`.

When the collection was empty and only the fallback header was present, the previous concatenation produced a WSGI value beginning with a semicolon:

```text
;session=abc
```

The fork now emits:

```text
session=abc
```

When both the parsed collection and fallback header are present, the existing behavior remains unchanged and separates them with a single semicolon.

## Scope

The change only affects the defensive payload-v2 Cookie-header fallback. It does not change normal parsed-cookie events, response cookies, v1 behavior, or public API surface.

A focused regression test covers the header-only case.

## Upstream relationship

`adamchainz/apig-wsgi` is read-only evidence for this undertaking. This divergence is tracked only in `ilmc/apig-wsgi`.

When observing future upstream changes, check whether equivalent delimiter handling appears independently and reconcile locally if appropriate.
