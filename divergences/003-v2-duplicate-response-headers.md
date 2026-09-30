# Divergence 003: preserve duplicate payload-v2 response headers

## Status

Active fork-only compatibility fix.

## Summary

Payload format v2 represents response headers as a single string-to-string map and handles `Set-Cookie` separately through the response `cookies` collection.

A WSGI application can emit the same non-cookie response header more than once. The upstream-derived v2 serializer converted the WSGI header list directly into a dictionary one item at a time, causing earlier values to be overwritten by the last value.

The fork now comma-combines duplicate non-cookie values while preserving the existing dedicated `Set-Cookie` handling.

Example:

```text
X-Test: one
X-Test: two
```

becomes the payload-v2 response entry:

```text
x-test: one,two
```

rather than silently retaining only `two`.

## Evidence

AWS documents payload format v2 as lacking `multiValueHeaders`; duplicate request header values are combined with commas. Current Mangum likewise comma-combines duplicate non-cookie response headers for its API Gateway v2 handler while returning cookies separately.

A focused fork regression test protects the behavior.

## Scope

This change affects only duplicate non-cookie payload-v2 response headers. It does not alter v1 multi-value-header behavior or `Set-Cookie` handling.

## Upstream relationship

`adamchainz/apig-wsgi` is read-only evidence. No upstream issue, pull request, review, or comment should be created from this undertaking.

Observe future upstream behavior and reconcile locally if equivalent handling appears independently.
