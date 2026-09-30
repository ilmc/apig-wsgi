# Investigation 007: focused compatibility contract

## Question

Which behaviours best represent the durable value of `apig-wsgi` if the implementation itself is small enough to recreate quickly?

## Selection principle

The undertaking does not need a second copy of the existing test suite. A focused compatibility contract should preserve only behaviours that are easy to implement plausibly but incorrectly because they depend on AWS or WSGI edge semantics.

The selected cases are therefore deliberately few.

## Contract case 1: ALB query strings

API Gateway v1 and ALB share much of the request shape but do not have identical query-string treatment.

For ALB, already-encoded reserved characters must survive adaptation without an extra round of quoting. A generic implementation that simply reuses the API Gateway v1 encoder can therefore corrupt a valid request while looking locally reasonable.

The focused contract preserves an example containing both `%3D` and `+`.

## Contract case 2: API Gateway v2 cookies

Payload format 2.0 has a dedicated `cookies` collection. The adapter also defensively handles a residual ordinary `Cookie` header and merges it into the WSGI `HTTP_COOKIE` value.

This is a useful compatibility sentinel because it is specific to the event protocol rather than to Flask or another WSGI framework.

## Contract case 3: event-family binary defaults

Binary response policy differs by event family.

For a binary content type with no explicit `binary_support` setting:

- API Gateway v1 defaults binary support off;
- ALB defaults binary support on;
- API Gateway v2 is handled with binary support on.

The focused contract directly compares v1 and ALB using the same WSGI application and response. This preserves an intentional difference that a cleanup or rewrite might otherwise normalize accidentally.

## Contract case 4: WSGI iterable cleanup

WSGI applications may return iterable response objects with a `close()` method. The adapter consumes the iterable and must invoke `close()` even though most simple framework examples return ordinary iterables where this behaviour is invisible.

This case protects a framework-independent WSGI semantic rather than an AWS event detail.

## What was not duplicated

The focused contract intentionally does not reproduce the broader suite for:

- every query-string combination;
- every special header mapping;
- every textual content type;
- every cookie cardinality;
- request-context and Lambda-context exposure;
- all binary body combinations;
- all status/header response shapes.

Those remain appropriately covered by the upstream-derived suite.

## Result

These cases support the undertaking's emerging conclusion: the project's durable asset is not primarily the amount of adapter code. It is the set of protocol and WSGI distinctions that have been learned, encoded and regression-tested over time.

The focused contract provides a compact review surface for that claim while the full upstream suite remains the authoritative behavioural safety net.

## Defect assessment

No new runtime defect was identified by selecting these cases. They are preservation tests, not evidence for changing implementation.

This is itself useful evidence: the undertaking can make the project's accumulated value more explicit without manufacturing a code change.