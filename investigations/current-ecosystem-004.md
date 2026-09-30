# Current ecosystem investigation 004

## Question

What has changed around `apig-wsgi` since its original WSGI-to-Lambda role, and what does that imply for the continuing value of this project?

## Current ecosystem

### FastAPI and ASGI

FastAPI is an ASGI framework. Its normal deployment model is to run behind an ASGI server such as Uvicorn, Hypercorn, Daphne, or Granian.

That creates a clean boundary with `apig-wsgi`: FastAPI is not a WSGI application and should not be made one merely to fit this package.

The rise of ASGI therefore does not make `apig-wsgi` incorrect; it narrows the class of applications for which it is directly applicable.

### Mangum

Mangum occupies the direct ASGI analogue of the space that `apig-wsgi` occupies for WSGI. It adapts ASGI applications to AWS Lambda and API Gateway invocation semantics.

That means a FastAPI application can remain ASGI-native while using a Lambda handler adapter rather than an HTTP server process.

For this undertaking, Mangum is important evidence that adding ASGI support to `apig-wsgi` would duplicate an established boundary rather than naturally extend the current one.

### AWS Lambda Web Adapter

AWS Lambda Web Adapter moves the adaptation boundary again.

Instead of adapting Lambda events directly to a Python framework interface such as WSGI or ASGI, it allows an ordinary web application process to listen on HTTP inside the Lambda execution environment. The adapter translates Lambda invocation events to HTTP and forwards them to that process.

This approach is framework- and language-independent. A FastAPI application can therefore run with its normal ASGI server while Lambda-specific translation happens outside the application/framework boundary.

The 1.0 generation also makes clear that AWS regards the adapter as a maintained deployment mechanism rather than merely an experiment.

### Bespoke adapters in the AI era

The implementation size of a framework-to-Lambda adapter is small enough that a capable engineer assisted by current coding models can produce a plausible custom implementation quickly.

That changes the economics of implementation but does not erase compatibility risk.

The difficult part is not writing a handler that works for one happy path. It is preserving accumulated distinctions such as:

- API Gateway v1 versus v2 response shapes;
- ALB versus API Gateway query-string treatment;
- multi-value headers;
- cookies;
- binary request and response handling;
- content-encoding interactions;
- missing or `None` AWS fields;
- WSGI `start_response` semantics;
- Lambda and request-context exposure.

The existing test suite demonstrates that these details are the durable part of the project.

## Adaptation-boundary progression

A useful way to view the ecosystem is:

```text
application deployment abstraction

Zappa-style deployment automation
        ↓
WSGI application → apig-wsgi → Lambda event model
        ↓
ASGI application → Mangum → Lambda event model
        ↓
web application + normal server → Lambda Web Adapter → Lambda event model
```

These are not strictly successive replacements. They put responsibility at different boundaries.

## What remains valuable about `apig-wsgi`

The project still has a coherent role for WSGI applications where:

- the application already exposes WSGI;
- a direct Lambda handler is desirable;
- running an HTTP server process inside Lambda would add unnecessary machinery;
- users value a mature compatibility layer rather than maintaining event translation themselves.

Its continuing value is therefore not that WSGI is the newest Python web interface. It is that WSGI remains a stable interface used by real applications and the package captures AWS compatibility knowledge for that interface.

## What appears to have diminished

The package is less likely to be the default answer for a newly designed Python API because:

- many new APIs use ASGI-native frameworks such as FastAPI;
- Mangum already covers direct ASGI-to-Lambda adaptation;
- Lambda Web Adapter makes framework-specific adaptation optional for applications willing to run a normal web server process;
- bespoke glue is cheaper to create than it was when this project began.

This affects growth opportunity more than correctness.

## Implication for the fork

The fork should not attempt to recover relevance by broadening into ASGI or by competing with Lambda Web Adapter.

A more useful undertaking is to understand and preserve the architectural lesson:

> small adapter libraries derive durable value from compatibility knowledge and boundary clarity, not from implementation volume.

That conclusion should guide any reorganisation here. A refactor is useful only if it makes those compatibility boundaries easier to inspect and maintain.

## Sources checked

Current external evidence reviewed for this investigation includes:

- FastAPI deployment documentation describing FastAPI as ASGI and its use with ASGI servers;
- Uvicorn documentation identifying Mangum as an AWS Lambda adapter for ASGI applications;
- the current AWS Lambda Web Adapter repository and its 1.0 migration documentation;
- current AWS Lambda runtime documentation.

These are external ecosystem evidence. `ilmc/apig-wsgi` remains authoritative for decisions in this undertaking.
