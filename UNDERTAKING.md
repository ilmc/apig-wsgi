# apig-wsgi Undertaking

**Established: 30 September 2026**

## Purpose

This fork exists to investigate the continuing role and architectural value of `apig-wsgi` in the Python-on-AWS-Lambda ecosystem.

The immediate purpose is not to create a divergent distribution or to modernise the project for its own sake. The undertaking should determine what remains materially valuable about a purpose-built WSGI-to-Lambda adapter after the rise of ASGI frameworks, direct ASGI adapters, AWS Lambda Web Adapter, and dramatically cheaper bespoke implementation through AI-assisted development.

`ilmc/apig-wsgi` is the authority for this undertaking. The public upstream repository `adamchainz/apig-wsgi` is historical and external evidence and remains the natural destination for improvements that belong to the upstream project rather than to a deliberate fork.

## Triggering context

The founder previously used `apig-wsgi` to run Flask APIs on AWS Lambda after moving away from Zappa and toward directly owning Lambda and AWS deployment tooling. The project was one of the early resources that made that transition practical and understandable.

The founder has since moved primarily to FastAPI. FastAPI is ASGI rather than WSGI and therefore does not use `apig-wsgi`. This prompted two related questions:

1. How has `apig-wsgi` evolved since it was actively used?
2. How have ASGI, newer Lambda integration mechanisms, and cheaper custom implementation changed the problem `apig-wsgi` originally solved?

This personal history is useful provenance and motivation. It is not evidence by itself that the project is obsolete, that ASGI should be added, or that any code change is required.

## Current baseline

At establishment, the fork is synchronized with upstream at commit `31a62c32999b8ce5b755638c95293637146afabd` (`Upgrade dependencies (#588)`, 29 September 2026).

The package remains a small, focused WSGI adapter. Most runtime behavior lives in `src/apig_wsgi/__init__.py`; most behavioral tests live in `tests/test_apig_wsgi.py`.

The public API remains centered on:

```python
from apig_wsgi import make_lambda_handler
```

No fork-specific runtime behavior is established by this undertaking yet.

## Questions to investigate

The undertaking should distinguish several questions that are easy to conflate:

- Is WSGI-to-Lambda adaptation still a useful bounded problem for existing Flask, Django and other WSGI applications?
- Has ASGI reduced the future growth of that niche without eliminating its installed-base value?
- What role is now served by direct ASGI adapters such as Mangum?
- What changes when Lambda integration happens at an HTTP-process boundary rather than a WSGI/ASGI callable boundary, as with AWS Lambda Web Adapter?
- How much value in `apig-wsgi` is implementation code versus accumulated executable knowledge of API Gateway, ALB, headers, cookies, binary bodies and event variants?
- Does reorganizing the source or tests materially improve maintainability and reasoning, or merely produce aesthetic churn?
- Are any findings worth contributing upstream?

## Operating principles

1. **Investigate before changing behavior.** A fork is not evidence that divergence is useful.
2. **Preserve external behavior by default.** Existing users and the mature compatibility surface are more important than internal fashion.
3. **Treat tests as evidence.** Edge-case coverage may be a more durable asset than the implementation itself.
4. **Prefer upstream contribution where appropriate.** If a change improves `apig-wsgi` generally, upstream is the default destination.
5. **Do not add ASGI merely because ASGI is now common.** Existing ASGI and HTTP-process solutions must be treated as alternatives and evidence, not as features that this package must absorb.
6. **Keep the undertaking independently legible.** Investigations, experiments and decisions belong in this repository rather than only in transient conversation.
7. **Stop when the evidence says to stop.** A conclusion that the project is mature, well-bounded and needs no fork-specific code is a successful result.

## Initial work

The first phase is documentary and observational:

- record the project's trajectory and the architectural alternatives that followed it;
- map the current implementation into its actual responsibilities;
- identify the compatibility knowledge preserved by the tests;
- decide whether any source/test reorganization is worth doing;
- only then consider behavior changes or upstream contributions.

## Initial non-goals

Unless evidence changes the decision, do not:

- add ASGI or FastAPI support to `apig-wsgi`;
- turn the package into a general multi-framework Lambda adapter;
- reimplement Mangum or AWS Lambda Web Adapter;
- create a fork-specific release;
- rewrite working code merely because AI makes rewriting cheap;
- add infrastructure, telemetry or process solely to make the undertaking appear active.

## Success posture

Success is an evidence-backed understanding of what remains valuable in `apig-wsgi` and the smallest useful action that follows from that understanding.

That may be a focused upstream improvement, a behavior-preserving internal reorganization, a comparative experiment, or simply a documented conclusion that the existing project is already appropriately scoped and mature.
