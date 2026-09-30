# Undertaking maintenance guide

This repository is a fork of `adamchainz/apig-wsgi` used as the authority for an ACK-managed investigation of the project's continuing role and compatibility value.

The fork is not currently intended to become a competing runtime distribution.

## Default posture

- Preserve the package's WSGI-specific scope.
- Prefer upstream for generally useful runtime fixes.
- Keep fork-specific runtime divergence near zero unless evidence justifies it.
- Preserve investigations, decisions and experiments here because they belong to this undertaking even when no code change follows.
- Treat focused compatibility tests as preservation evidence, not as a replacement for the upstream-derived suite.

## Before starting runtime work

Answer these questions in the repository:

1. What concrete behaviour is wrong or missing?
2. Which AWS event/deployment topology reproduces it?
3. What WSGI behaviour should result?
4. Is the desired behaviour general enough to belong upstream?
5. Can documentation or WSGI middleware solve the problem more precisely than core adapter policy?
6. Which existing compatibility tests should protect the change?

If these questions cannot be answered, investigate before modifying `src/`.

## Upstream synchronization

Before substantial work:

1. compare `main` with `adamchainz/apig-wsgi`;
2. understand new upstream runtime/test changes;
3. update undertaking assumptions if upstream has already solved or changed the relevant problem;
4. avoid building a local solution on stale behavior.

Fork-only evidence files do not need to mirror upstream organization.

Runtime changes should remain easy to isolate from undertaking-only files.

## Contribution path

For a generally useful defect or maintenance improvement:

1. reproduce it with the smallest realistic event fixture;
2. add a regression test;
3. implement the narrow fix;
4. check the focused compatibility contract and full suite;
5. document any AWS topology assumptions;
6. prefer an upstream PR rather than establishing permanent fork behavior.

## Appropriate fork-only work

Examples:

- architectural or historical investigations;
- decision records;
- comparison experiments;
- preservation/control tests used by this undertaking;
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