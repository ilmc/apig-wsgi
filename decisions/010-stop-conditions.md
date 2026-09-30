# Decision 010: explicit stop conditions

## Status

Adopted for this undertaking.

## Context

The undertaking has already tested several plausible reasons to modify the fork:

- reorganising the runtime for architectural clarity;
- adding ASGI/FastAPI support;
- automatically rewriting API Gateway stage prefixes;
- treating AI-generated code as a reason to replace the maintained library.

None has yet produced evidence for a fork-specific runtime direction.

## Decision

Treat stopping or narrowing as a successful outcome when the investigation no longer identifies a concrete compatibility, maintenance or user problem worth pursuing.

## Stop conditions

The undertaking may move to observation-only maintenance when all of the following remain true:

1. upstream is actively maintained enough for current Python/AWS compatibility;
2. no reproducible runtime defect has been identified in the fork's supported scope;
3. no material user need justifies deliberate divergence;
4. newer ASGI/HTTP-process approaches are better handled by their own tools rather than absorbed here;
5. the remaining questions are primarily historical or comparative rather than actionable.

## What observation-only means

Observation-only does not mean abandonment.

It means:

- periodically compare the fork with upstream before undertaking new work;
- investigate concrete compatibility reports when they appear;
- preserve the undertaking evidence and focused compatibility contract;
- avoid creating work merely to keep the fork visibly active.

## Re-entry triggers

Resume active work when there is new evidence such as:

- an upstream compatibility issue that can be reproduced and improved;
- a new AWS proxy event behaviour affecting supported WSGI deployments;
- a regression introduced by Python/runtime changes;
- a meaningful upstream maintenance gap;
- evidence from the adapter-boundary experiment that changes an existing decision.

## Rationale

A mature utility can be healthy while changing very little. The undertaking should not confuse activity with value.