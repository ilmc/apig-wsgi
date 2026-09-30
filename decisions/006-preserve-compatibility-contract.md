# Decision 006: preserve a small explicit compatibility contract

## Status

Adopted for this undertaking.

## Context

The full upstream-derived suite contains the project's detailed behavioural coverage. Investigation 007 identified a smaller set of cases that communicate the project's durable value particularly well because they encode protocol or WSGI semantics that are easy to overlook in a bespoke rewrite.

## Decision

Keep a small fork-specific compatibility-contract test module alongside the upstream-derived suite.

The contract should remain deliberately selective rather than becoming a parallel test architecture.

## Included concerns

The initial contract covers:

- ALB query-string preservation of already-encoded reserved characters;
- API Gateway v2 cookie collection/header merging;
- differing binary defaults between API Gateway v1 and ALB;
- WSGI response-iterable cleanup through `close()`.

## Rationale

These cases make the project's accumulated compatibility knowledge directly reviewable without forcing a wholesale reorganisation of upstream tests.

They also provide useful sentinels for future experiments, AI-assisted rewrites or alternative adapters: a replacement that handles only the obvious happy path can be compared against concrete historical semantics.

## Constraint

Do not grow this file merely because a behaviour is interesting.

A case belongs in the focused contract only when it is:

1. materially part of the adapter's value;
2. non-obvious enough to be lost in a plausible rewrite;
3. compact enough to explain without recreating the full suite.

Everything else should remain in the normal upstream-derived tests.

## Runtime consequence

None. This decision adds preservation coverage only and establishes no fork-specific runtime behaviour.