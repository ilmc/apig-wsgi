# Experiment observation: test layout 001

## Question

Does physically splitting the existing monolithic test suite by compatibility domain materially improve auditability enough to justify the churn?

## Observation

The suite is physically concentrated in `tests/test_apig_wsgi.py`, but its internal structure already follows the primary compatibility families: API Gateway v1, ALB, API Gateway v2, and unknown versions. Within those families, the tests cover query encoding, headers, bodies, cookies, binary response policy, WSGI exception propagation, request/full-event/context exposure, and iterator behaviour.

The audit found one concrete coverage-label defect: `TestV2Events.test_get_binary_support_default_text_content_types_encoded` is located and named as a v2 case but invokes `make_v1_event()` and asserts the v1 response shape. The undertaking added a separate v2 regression test that genuinely exercises the v2 path.

That finding shows an auditability risk, but not enough evidence for a wholesale split of the upstream-derived suite.

## Cost of a wholesale split

A full physical reorganisation would require moving a large body of stable tests, extracting or duplicating shared fixtures and event builders, and producing a large provenance-obscuring diff without changing runtime behaviour.

The main conceptual boundaries are already visible through classes and event-builder functions. The most important AWS distinctions can be audited in-place once they are explicitly documented.

A split could therefore make navigation superficially cleaner while making upstream comparison, blame history, and future synchronization materially harder.

## Result

The experiment does **not** justify a wholesale test-suite split at this time.

The smallest useful action is:

- retain the upstream-derived monolithic suite;
- document its compatibility domains;
- add narrowly targeted regression tests when the audit identifies a real gap or misleading coverage claim;
- consider extracting tests only when new work creates repeated friction in a specific domain.

## Consequence

Decision 002 should be interpreted as "improve compatibility auditability before runtime restructuring", not as a mandate to manufacture multiple test files.

The negative result is useful: the current physical structure is imperfect but not sufficiently harmful to justify a large refactor solely for ACK legibility.
