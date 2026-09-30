# Experiment: test layout 001

## Purpose

Determine whether reorganising the compatibility suite by event family and behavioural concern materially improves auditability without changing runtime behaviour.

## Hypothesis

The current single test module obscures which AWS event family a test actually exercises and makes compatibility gaps harder to see.

A behaviourally organised suite should make the compatibility matrix easier to inspect while preserving the same runtime contract.

## Control

The current upstream-derived suite in `tests/test_apig_wsgi.py` is the control.

It already provides broad coverage and should not be treated as defective merely because it is physically large.

## Proposed experimental layout

```text
tests/
    support.py
    test_apig_v1.py
    test_alb.py
    test_apig_v2.py
    test_wsgi_semantics.py
    test_unknown_events.py
```

Cross-cutting binary-response assertions may remain within each event-family module rather than being abstracted into a shared matrix if that keeps the event-specific response shape visible.

## Constraints

The experiment must:

- leave `src/apig_wsgi/` unchanged;
- preserve existing compatibility assertions;
- keep concrete AWS event shapes visible;
- avoid a fixture layer so abstract that tests cease to communicate protocol details;
- preserve v1, ALB, and v2 differences explicitly;
- add explicit coverage where the audit has demonstrated that an apparent event-family test actually exercises another family;
- run under the project's existing pytest, mypy, Ruff, and coverage expectations.

## Success criteria

The reorganisation is useful only if a reviewer can answer these questions more easily than with the control:

1. Which tests define API Gateway v1 compatibility?
2. Which behaviours differ for ALB despite sharing much of the v1 event shape?
3. Which tests define v2 cookie and response-header semantics?
4. Where are binary defaults for each event family verified?
5. Which tests concern WSGI semantics rather than AWS event parsing?
6. Are there obvious compatibility claims that are not actually exercised by the event family implied by the test name/location?

## Failure criteria

Abandon or narrow the reorganisation if it:

- requires substantial helper indirection;
- duplicates large amounts of setup merely to achieve smaller files;
- makes tests harder to read independently;
- creates churn without exposing compatibility boundaries more clearly;
- encourages production-code changes solely to fit the proposed test layout.

## Current observation

The audit has already produced one positive signal for the hypothesis: a v2-named encoded-response test in the control invokes a v1 event and asserts the v1 response format.

A dedicated v2 regression test has been added separately before any wholesale reorganisation. This allows the compatibility claim to exist independently of whether the larger layout experiment is ultimately adopted.

## Next execution step

Perform the reorganisation as a mechanically reviewable test-only change, then compare the resulting suite against the success criteria above before deciding whether to retain it.
