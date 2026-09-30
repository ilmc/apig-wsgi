# Experiment 003: stage and mount-path compatibility

## Purpose

Determine whether `apig-wsgi` should offer any explicit support for mapping API Gateway stage or API-mapping prefixes into WSGI `SCRIPT_NAME` and `PATH_INFO`.

## Why this experiment exists

Upstream issue #194 is old but still relevant to the adapter boundary: AWS deployment topology can change the path Lambda receives, while WSGI applications care about the distinction between their mount point (`SCRIPT_NAME`) and in-application route (`PATH_INFO`).

The experiment must avoid assuming that a stage name is always a mount prefix.

## Case matrix

For every case record four values before writing code:

1. externally visible request URL;
2. representative Lambda event fields;
3. desired `SCRIPT_NAME`;
4. desired `PATH_INFO`.

### Case A: REST API v1, default execute-api domain, named stage

Example external URL:

`https://example.execute-api.region.amazonaws.com/prod/users/123`

Question: should a WSGI app configured as the API root see `SCRIPT_NAME=/prod` and `PATH_INFO=/users/123`, or is the stage part of `PATH_INFO` by design?

The answer must be explicit configuration, not inferred preference.

### Case B: REST API with custom domain API mapping

Example external URL:

`https://api.example.com/orders/users/123`

where `orders` maps to a stage.

Current AWS documentation says the API mapping is stripped before API invocation. The adapter therefore may not receive enough information in the normal path field to reconstruct the externally visible mount prefix reliably.

### Case C: HTTP API v2 with `$default` stage

Example external URL:

`https://example.execute-api.region.amazonaws.com/users/123`

Expected default: `SCRIPT_NAME=''`, `PATH_INFO='/users/123'`.

Any algorithm that blindly uses `requestContext.stage` would risk producing `SCRIPT_NAME='/$default'`, which is not present in the client URL.

### Case D: HTTP API v2 with custom domain mapping

AWS documents that `rawPath` excludes the API mapping value. Verify that an adapter cannot infer the externally visible mapping prefix from `rawPath` alone.

### Case E: collision

Stage name: `prod`
Application path: `/prod/users/123`

A naive "strip the first segment if it equals the stage" algorithm would alter a legitimate application route. This case must remain correct under any proposed option.

## Candidate semantics to compare

### Control: current behaviour

Use the event path directly as `PATH_INFO` and keep `SCRIPT_NAME` empty.

### Candidate 1: explicit stage-prefix mode

An opt-in mode treats a named non-default stage as a mount prefix only when the event path actually begins with that stage segment.

Evaluate collision ambiguity and custom-domain behaviour.

### Candidate 2: explicit mount prefix

Caller supplies a mount prefix explicitly when constructing the Lambda handler.

This is conceptually cleaner in WSGI terms and does not require the adapter to guess AWS topology. Evaluate whether this is useful enough to justify API surface.

### Candidate 3: documentation/middleware only

Keep core behaviour unchanged and document how to adjust `SCRIPT_NAME`/`PATH_INFO` in WSGI middleware for deployments that require it.

## Success criteria for a library change

A code change is justified only if it:

- has precise semantics across all cases above;
- does not silently rewrite legitimate application paths;
- handles `$default` safely;
- does not pretend to recover custom-domain mapping information that AWS omits;
- makes a common deployment materially easier than simple WSGI middleware;
- can be proposed upstream without turning `apig-wsgi` into deployment-policy machinery.

## Failure / narrowing criterion

If explicit middleware is clearer and no broadly correct adapter behaviour emerges, record that as the result and do not add an option.

## Initial hypothesis

Documentation or middleware is currently the strongest control. An explicit mount-prefix option may be defensible, but an automatic stage-stripping feature is unlikely to have sufficiently reliable semantics.
