# Upstream current-state investigation 005

## Question

Does current upstream activity suggest pressure to broaden `apig-wsgi` beyond its WSGI/Lambda boundary, or is the project behaving like a mature compatibility utility?

## Snapshot

At the time of this investigation, upstream `adamchainz/apig-wsgi` has:

- recent maintenance commits for dependency upgrades, Python 3.15 support, CI hardening, and build-backend modernisation;
- no open pull requests;
- one open issue, issue #194, originally opened in November 2020 and last updated in June 2023.

The fork was synchronized with upstream at commit `31a62c32999b8ce5b755638c95293637146afabd` when this undertaking began.

## Open issue evidence

The sole open issue concerns API Gateway stage-path behaviour with multi-stage/custom-domain deployments. The proposed capability is effectively an option to strip a stage prefix from the incoming path before exposing it to the WSGI application.

This is notable for what it is not:

- it is not a request for ASGI support;
- it is not a request for FastAPI support;
- it is not a request to embed an HTTP server;
- it is not a request to compete with Mangum or Lambda Web Adapter.

It is another edge case in translating AWS API Gateway request semantics into the expectations of an ordinary web application.

That is consistent with the project's existing value proposition: accumulated compatibility behaviour at the AWS/WSGI boundary.

## Maintenance pattern

Recent upstream commits are predominantly ecosystem maintenance rather than product-surface expansion:

- Python-version support;
- dependency refreshes;
- pre-commit updates;
- CI robustness;
- build tooling changes.

This is the pattern expected from a small stable utility whose core design is largely complete.

## Interpretation

The evidence does not support a narrative that the project has been displaced into irrelevance and needs reinvention.

A better interpretation is:

> `apig-wsgi` has moved from an important enabling abstraction in an earlier Lambda/Python ecosystem into a mature, narrow compatibility component for users who still have WSGI applications.

ASGI and HTTP-process adapters reduce the size of the future greenfield audience, but they do not invalidate the existing boundary.

## Implication for this undertaking

The fork should not manufacture a roadmap simply because upstream's visible feature activity is low.

Useful fork activity should instead come from one of three sources:

1. a demonstrated compatibility defect;
2. a maintainability/auditability improvement that preserves behaviour;
3. an investigation that produces transferable architectural knowledge.

The current undertaking is primarily in categories 2 and 3.

## Upstream relationship

If this fork discovers a narrow compatibility defect or a clearly beneficial test improvement, upstream contribution should remain the default disposition.

Long-lived behavioural divergence requires stronger evidence than documentation/evidence divergence because every behavioural fork creates an ongoing compatibility and maintenance obligation.
