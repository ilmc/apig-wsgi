# Decision 004: retain the compact runtime and upstream-derived test layout

## Status

Adopted for this undertaking.

## Context

The undertaking began by asking whether reorganising the codebase into explicit event, request, response and handler modules would make the project more legible and better aligned with ACK-style evidence-driven management.

Investigation showed that those conceptual boundaries are real, but the runtime remains small and internally coherent. The test-layout experiment likewise found that the large test module already exposes its major compatibility families through classes and event builders.

The audit did identify a mislabeled v2 coverage case. A targeted regression test fixed that gap without requiring broad source movement.

## Decision

Do not split `src/apig_wsgi/__init__.py` or wholesale reorganise `tests/test_apig_wsgi.py` merely to make the repository look more architecturally explicit.

Preserve the compact upstream-derived structure until a demonstrated maintenance or compatibility problem makes a split materially useful.

## Rationale

A physical split would currently create more provenance and synchronization cost than demonstrated maintenance benefit.

The important architecture can be made explicit through investigations, decisions and focused tests without forcing the production package to mirror the documentation structure.

This keeps the fork close to upstream while still making the undertaking legible.

## Consequences

- `make_lambda_handler` and its supporting implementation remain where upstream keeps them.
- New runtime modules should be introduced only when a concrete change benefits from that separation.
- Existing tests remain largely untouched; new focused regression files are acceptable when they expose a real coverage gap.
- ACK artefacts describe conceptual boundaries without requiring the codebase to imitate those artefacts.
- Future fork divergence should be judged by user or maintenance value, not by architectural aesthetics.

## Revisit trigger

Revisit this decision if one of the following becomes true:

- a compatibility change requires touching multiple unrelated parts of the runtime and the monolith materially increases risk;
- repeated upstream-sync conflicts make the current fork strategy impractical;
- a new event family or compatibility domain creates genuinely independent logic;
- test maintenance repeatedly suffers from fixture or event-family confusion that focused regression files cannot address cleanly.
