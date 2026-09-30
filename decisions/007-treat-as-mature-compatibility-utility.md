# Decision 007: treat apig-wsgi as a mature compatibility utility

## Status

Adopted for this undertaking.

## Context

Investigation 008 reviewed the upstream changelog from the first 2018 release through current 2026 maintenance.

The project's history shows a clear transition:

- initial enablement of WSGI applications on API Gateway;
- concentrated AWS compatibility expansion across ALB, multi-value fields, payload format 2.0, path/query handling and Lambda context;
- later stabilization dominated by Python-version support, packaging/tooling maintenance and occasional narrow protocol corrections.

## Decision

Manage this fork as an investigation and preservation effort around a mature compatibility utility, not as a product waiting for broad modernization.

New runtime work must be justified by a reproducible compatibility, maintenance or user problem.

## Consequences

- Do not create roadmap items merely to increase feature count.
- Do not add ASGI/FastAPI support to make the project appear current.
- Prefer focused regression tests over broad rewrites when a compatibility issue is discovered.
- Prefer upstream contribution for generally useful fixes.
- Treat support for current Python versions and AWS event semantics as legitimate maintenance rather than evidence that the project lacks direction.
- Treat a conclusion of 'no runtime change needed' as a valid successful outcome.

## Revisit trigger

Revisit this posture if evidence shows either:

1. substantial new AWS event behavior that the existing architecture cannot absorb cleanly; or
2. a significant active user need that is poorly served by existing WSGI, ASGI or HTTP-process adaptation options.

Absent such evidence, restraint is the default maintenance strategy.