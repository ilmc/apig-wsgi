# Decision 011: upstream is read-only evidence

## Status

Adopted for this undertaking.

## Context

The undertaking uses `ilmc/apig-wsgi` as its authority while consulting `adamchainz/apig-wsgi` for historical and current external evidence.

Earlier work assumed that generally useful runtime fixes might be proposed upstream. The founder has now explicitly constrained the undertaking not to write to the source project and not to add or comment on pull requests.

## Decision

Treat `adamchainz/apig-wsgi` as strictly read-only.

Do not create or modify upstream:

- source files or branches;
- issues;
- pull requests;
- pull-request reviews or comments;
- issue comments;
- other writable project state.

Use upstream only to understand history, current maintenance, compatibility behavior, and divergence.

## Consequences

- Runtime fixes discovered by this undertaking remain in `ilmc/apig-wsgi` unless the founder later changes this policy.
- Fork-specific divergences must be documented locally rather than tracked through an upstream contribution workflow.
- Decisions that previously said "prefer upstream" are superseded where they conflict with this explicit read-only rule.
- The fork may still remain close to upstream; synchronization is an evidence and maintenance concern, not a contribution channel.
- Pull-request workflow in the fork is not required for undertaking work unless the founder explicitly requests it.

## Rationale

Authority and evidence are separate concerns. The undertaking can learn from the public upstream project without participating in its writable workflow.

This keeps all active management inside the undertaking authority while preserving upstream as a clean external reference.
