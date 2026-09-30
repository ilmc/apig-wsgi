# Project trajectory 001

## Question

How did the problem solved by `apig-wsgi` change as Python web interfaces and AWS Lambda integration options evolved?

## Triggering provenance

The founder used `apig-wsgi` with Flask after moving away from Zappa and toward directly building and owning Lambda/AWS deployment tooling for many Lambda functions. The project was one of the early resources that made that transition practical.

The founder later moved primarily to FastAPI. FastAPI uses ASGI rather than WSGI, so `apig-wsgi` no longer sits on the active application path.

This history motivates the investigation but does not predetermine its conclusion.

## Initial architectural reading

`apig-wsgi` occupies a callable-adapter boundary:

```text
API Gateway / ALB Lambda event
            ↓
       apig-wsgi
            ↓
        WSGI app
            ↓
       apig-wsgi
            ↓
 Lambda proxy response
```

Its job is not to host a web server. It translates between AWS Lambda proxy event/response structures and the WSGI calling convention.

ASGI changes the application interface, not Lambda's invocation model. A FastAPI application therefore needs either a direct ASGI/Lambda adapter, an HTTP-process adapter, or custom translation rather than `apig-wsgi`.

## Successor approaches to compare

The undertaking should compare at least three architectural approaches:

1. **WSGI callable adapter** — represented by `apig-wsgi`.
2. **ASGI callable adapter** — represented by tools such as Mangum.
3. **HTTP-process adapter** — represented by AWS Lambda Web Adapter, where the application can run as an ordinary HTTP server and Lambda integration happens outside the application framework interface.

A fourth practical option now matters more than it once did:

4. **Small bespoke adapter** — increasingly cheap to create with strong tests and AI-assisted development, though the maintenance burden and edge-case knowledge remain real.

## Working hypotheses

These are hypotheses, not conclusions:

- ASGI likely reduced the future growth of pure WSGI adapter demand without removing the installed-base value of WSGI support.
- `apig-wsgi` may now be best understood as a mature compatibility utility rather than an expanding abstraction.
- HTTP-process adapters potentially reduce coupling to Python framework interfaces altogether.
- The durable value of `apig-wsgi` may be concentrated more in accumulated compatibility knowledge and tests than in the raw amount of implementation code.
- A rewrite or broadening of scope is not justified merely because alternative architectures now exist.

## Evidence needed next

- inspect upstream release/changelog history and current maintenance pattern;
- map the current test suite by behavior and edge case;
- compare the exact responsibility boundaries of `apig-wsgi`, Mangum and AWS Lambda Web Adapter;
- determine whether any compatibility cases in `apig-wsgi` remain uniquely useful or poorly documented elsewhere;
- test whether a source/test reorganization improves comprehension without behavior change.

## Current judgement

There is not yet evidence for an `apig-wsgi` behavior change.

The useful next step is to make the current architecture and compatibility surface explicit, then compare it with newer alternatives. If that yields no actionable gap, the correct conclusion may be that the project is already appropriately narrow and mature.
