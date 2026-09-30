# Decision 009: upstream-first maintenance

## Status

Adopted for this undertaking.

## Context

The fork began synchronized with `adamchainz/apig-wsgi` and the undertaking has not identified a reason for a divergent runtime distribution.

The investigations so far support a mature-maintenance posture: preserve WSGI/Lambda compatibility, add focused evidence where useful, and avoid broad modernization without a concrete user or protocol need.

## Decision

Treat upstream as the default destination for generally useful runtime fixes and compatibility improvements.

The fork remains authoritative for the undertaking's evidence, decisions, experiments and any intentionally local controls, but should not accumulate runtime divergence by default.

## Rules

A runtime change should normally be prepared so that it can be proposed upstream when it:

- fixes a reproducible AWS/WSGI compatibility defect;
- improves correctness for supported event families;
- adds regression coverage for generally applicable behaviour;
- modernizes maintenance without changing project scope.

A change may remain fork-only when it is primarily:

- undertaking evidence or decision material;
- an experiment or comparison harness;
- a local preservation/control test that would duplicate upstream's preferred test organization;
- an intentionally narrower or different policy that upstream has no reason to adopt.

## Sync posture

Keep the fork close enough to upstream that comparisons remain meaningful.

Do not resolve upstream divergence by mechanically preserving every fork-local change. If a fork-specific runtime change makes synchronization materially harder, re-evaluate whether that change belongs here at all.

## Consequence

The fork is not intended to become a competing distribution unless future evidence explicitly justifies that outcome.