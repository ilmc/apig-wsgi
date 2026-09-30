# Decision 005: do not automatically strip API Gateway stages from paths

## Status

Adopted for this undertaking.

## Context

Upstream issue #194 documents real deployments where API Gateway stage prefixes interfere with WSGI routing or URL generation. Historical discussion produced workable middleware patterns and an upstream maintainer invitation for a reproducing PR.

Current AWS documentation, however, confirms that path semantics vary by deployment topology:

- default execute-api URLs include named stages in the public URL;
- custom-domain API mappings are stripped before API invocation;
- HTTP API payload format 2.0 `rawPath` does not include the API mapping value;
- `$default` stages have no corresponding `/$default` component in the public URL.

## Decision

Do not add automatic core behaviour that infers a WSGI mount point from `requestContext.stage` or unconditionally strips a matching first path segment.

## Rationale

The adapter cannot reliably infer the externally visible application mount point from the stage name alone.

Automatic rewriting can be wrong when:

- the API uses a custom domain mapping;
- the stage is `$default`;
- an application route legitimately begins with the same segment as the stage;
- the caller intentionally considers the stage part of application routing.

WSGI `SCRIPT_NAME` is an application-mount concept, while API Gateway `stage` is a deployment concept. They sometimes correspond, but they are not equivalent.

## What remains open

This decision does not reject all improvements in this area.

A future change may still be justified if Experiment 003 demonstrates useful, precise semantics for:

- an explicit mount-prefix option;
- a narrowly defined opt-in stage-prefix mode;
- or documentation/middleware guidance that is materially clearer than adding API surface.

## Immediate consequence

No runtime change is proposed from issue #194 at this stage.

The undertaking preserves the issue as a strong example of why the project's compatibility knowledge matters and why apparently small Lambda-path transformations require careful deployment-context evidence.
