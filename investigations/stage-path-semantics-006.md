# Investigation 006: API Gateway stage and path semantics

## Question

Does the long-standing upstream issue about API Gateway stage prefixes indicate a current defect in `apig-wsgi`, or is it better treated as deployment/application-specific path configuration?

## Historical upstream evidence

Upstream issue #194 describes deployments where API Gateway stage names appear in the effective path seen by the WSGI application. Contributors proposed several remedies:

- reconstructing `PATH_INFO` from `resource` plus `pathParameters.proxy`;
- wrapping the generated Lambda handler and rewriting `event['path']`;
- using WSGI middleware / Flask `DispatcherMiddleware`;
- moving the stage component into `SCRIPT_NAME` and removing it from `PATH_INFO`.

The upstream maintainer explicitly said he would consider a PR that changed the WSGI environ, provided the example application reproduced the problem alongside the fix. A later commenter reported that the issue still affected payload format 2.0.

This is therefore a genuine historical compatibility concern rather than a hypothetical feature request.

## Current AWS semantics

Current AWS documentation still makes stage and path treatment depend on the endpoint and mapping model.

For REST APIs using the default `execute-api` hostname, the deployed URL includes the stage component, for example `/prod/user`.

For custom domains with API mappings, API Gateway strips the configured mapping path before invoking the mapped API stage. The externally visible URL path and the path presented to the API are therefore deliberately not always identical.

For HTTP API payload format 2.0, AWS documents an additional distinction: `rawPath` does not include the API mapping value when a custom domain mapping is used. AWS explicitly recommends payload format 1.0 `path` when the mapping value itself is required.

These current rules confirm that there is no single universally correct transformation of "stage or mapping prefix" into WSGI `SCRIPT_NAME` and `PATH_INFO` without considering how the API is exposed.

## WSGI interpretation

WSGI gives `SCRIPT_NAME` and `PATH_INFO` different meanings:

- `SCRIPT_NAME` identifies the initial portion of the request URL corresponding to the application mount point;
- `PATH_INFO` identifies the remaining path within the application.

A stage name can resemble an application mount point when users invoke an API through the default execute-api hostname. But with a custom domain mapping, AWS may remove that mapping before the Lambda event reaches the adapter.

Automatically treating `requestContext.stage` as `SCRIPT_NAME` therefore risks inventing a path prefix that the caller did not use, especially for `$default` stages or custom domains.

Conversely, always passing the raw event path through as `PATH_INFO` can be inconvenient for applications deployed behind non-default stages.

## Current judgement

The upstream issue remains conceptually valid, but it does **not** currently justify an unconditional core behaviour change in this fork.

The problem is a boundary/configuration ambiguity:

- what URL prefix the client sees;
- what API Gateway removes or preserves;
- what the Lambda event reports;
- where the WSGI application considers itself mounted.

A correct library feature would need to express that distinction explicitly rather than guess from `requestContext.stage`.

## Plausible improvement shapes

If this undertaking pursues the issue, safer options would be one of:

1. **Documentation-only guidance** showing middleware for deployments that intentionally treat a stage as an application mount point.
2. **An explicit opt-in handler option** that controls stage/mount handling and is disabled by default.
3. **A more general mount-prefix option** whose semantics are defined in WSGI terms rather than AWS-stage terms.

An implicit automatic rewrite is the least attractive option because custom domain mappings and `$default` stages make inference unreliable.

## Evidence required before code

Before proposing a runtime change, reproduce at least these cases as event fixtures:

- REST API format 1.0 through the default execute-api hostname with a named stage;
- REST/HTTP API behind a custom domain mapping;
- HTTP API format 2.0 with `$default` stage;
- format 2.0 behind a custom domain API mapping;
- a path whose first application segment happens to equal the stage name, to test collision risk.

For each case, define the externally visible URL and the desired WSGI `SCRIPT_NAME`/`PATH_INFO` pair before touching implementation.

## Conclusion

Issue #194 is a useful candidate for further compatibility work because it concerns exactly the kind of translation edge case where this project's accumulated value lives.

However, current AWS documentation strengthens the case for explicit mount semantics rather than a simple "strip the stage" patch.
