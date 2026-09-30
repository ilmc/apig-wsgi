# Undertaking maintenance guide

This repository is a fork of `adamchainz/apig-wsgi` used as the authority for an ACK-managed investigation of the project's continuing role and compatibility value.

The fork is the only writable authority for this undertaking. The public upstream repository is read-only evidence: do not create or update upstream issues, pull requests, reviews, comments, branches, or files from this undertaking.

The fork is not currently intended to become a competing published distribution.

## Default posture

- Preserve the package's WSGI-specific scope.
- Use upstream read-only for historical/current evidence and synchronization awareness.
- Keep fork-specific runtime divergence small and explicit unless evidence justifies it.
- Preserve investigations, decisions and experiments here because they belong to this undertaking even when no code change follows.
- Treat focused compatibility tests as preservation evidence, not as a replacement for the upstream-derived suite.
- Do not use pull-request discussion as an undertaking work surface unless the founder explicitly requests it.

## Before starting runtime work

Answer these questions in the repository:

1. What concrete behaviour is wrong or missing?
2. Which AWS event/deployment topology reproduces it?
3. What WSGI behaviour should result?
4. Is the desired behaviour general or intentionally fork-specific?
5. Can documentation or WSGI middleware solve the problem more precisely than core adapter policy?
6. Which existing compatibility tests should protect the change?

If these questions cannot be answered, investigate before modifying `src/`.

## Upstream synchronization

Before substantial work:

1. compare the fork's runtime assumptions with current `adamchainz/apig-wsgi` read-only;
2. understand new upstream runtime/test changes;
3. update undertaking assumptions if upstream has already solved or changed the relevant problem;
4. avoid building a local solution on stale behavior.

Upstream observation never implies permission to write upstream.

Fork-only evidence files do not need to mirror upstream organization.

Runtime changes should remain easy to isolate from undertaking-only files.

## Runtime-change path

For a demonstrated defect or maintenance improvement:

1. reproduce it with the smallest realistic event fixture;
2. add a regression test;
3. implement the narrow fix in `ilmc/apig-wsgi`;
4. check the focused compatibility contract and full suite where possible;
5. document any AWS topology assumptions;
6. record the divergence explicitly when upstream does not contain the behavior.

Do not open or comment on upstream pull requests or issues as part of this path.

## Appropriate fork-only work

Examples:

- architectural or historical investigations;
- decision records;
- comparison experiments;
- preservation/control tests used by this undertaking;
- narrowly justified compatibility fixes;
- intentionally local tooling that does not change the published package.

## Things that need stronger evidence

Do not do these merely because they are technically possible:

- add ASGI or FastAPI support;
- embed server/process adaptation;
- automatically infer WSGI mount points from API Gateway deployment stages;
- reorganise the compact runtime into more modules;
- publish a fork-specific package;
- replace upstream code with an AI-generated rewrite.

## Observation-only state

If there is no concrete defect or unmet user need, the appropriate maintenance mode is observation rather than invention.

The repository can remain useful as a preserved account of the adapter boundary, a compact compatibility contract, and a place to evaluate future changes when evidence appears.
