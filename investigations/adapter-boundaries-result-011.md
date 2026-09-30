# Investigation 011: adapter-boundary comparison result

**Observed: 30 September 2026**

## Question

How have ASGI and newer Lambda integration mechanisms changed the role that `apig-wsgi` originally occupied?

This is the evidence phase of Experiment 002. It compares responsibility boundaries rather than framework popularity or synthetic throughput.

## Sources

Current external evidence was read-only:

- Mangum: https://github.com/Kludex/mangum
- AWS Lambda Web Adapter: https://github.com/aws/aws-lambda-web-adapter
- the current `apig-wsgi` fork/upstream code and documentation.

No external project state was modified.

## Boundary 1: `apig-wsgi`

`apig-wsgi` is a direct WSGI-callable adapter.

The Lambda runtime invokes a Python handler created by `make_lambda_handler()`. The adapter interprets the AWS event, constructs a WSGI environ, invokes the WSGI application directly, consumes its iterable response, and serializes the result back into the event-family response shape.

Consequences:

- no conventional HTTP server process is required;
- AWS event knowledge lives in the Python library;
- WSGI applications can remain unaware of API Gateway/ALB event dictionaries;
- compatibility is tightly bounded to WSGI and the supported AWS event families;
- the package's accumulated tests are the main authority for subtle translation behavior.

This remains a coherent boundary for existing Flask, Django WSGI, and other WSGI deployments.

## Boundary 2: Mangum

Mangum currently describes itself as an adapter for running ASGI applications in AWS Lambda and supports Function URLs, API Gateway HTTP/REST APIs, ALB, and Lambda@Edge events.

It also advertises ASGI lifespan handling, binary media/payload compression, and compatibility with frameworks including FastAPI, Starlette, Quart and Django.

Architecturally this is the ASGI analogue of `apig-wsgi` rather than a replacement for its interface:

- Lambda still invokes a direct handler;
- the adapter still owns AWS event interpretation;
- the application is invoked through its framework protocol (ASGI rather than WSGI);
- no ordinary HTTP server is required for the Lambda invocation path.

For an ASGI-native application such as FastAPI, this is the natural direct-handler boundary.

## Boundary 3: AWS Lambda Web Adapter

AWS Lambda Web Adapter has moved the boundary further outward.

Its current documentation describes a Lambda extension that runs alongside an ordinary HTTP application and forwards translated Lambda requests to the application's local HTTP port. It is framework- and language-independent and supports API Gateway REST/HTTP APIs, Function URLs and ALB.

The current project also exposes operational features that do not naturally belong to a WSGI/ASGI callable adapter, including:

- readiness checks;
- container and ZIP/layer deployment modes;
- response streaming;
- graceful shutdown;
- response compression;
- SnapStart before-checkpoint/after-restore hooks;
- base-path removal configuration;
- portability of the same ordinary HTTP application/container to non-Lambda compute.

The application therefore speaks HTTP to a local process boundary rather than WSGI/ASGI directly to the Lambda event adapter.

This trades a larger runtime/deployment surface for stronger application portability and framework/language independence.

## What ASGI actually changed

ASGI did not make direct Lambda adaptation unnecessary.

It split the direct-adapter ecosystem by application protocol:

- WSGI applications need WSGI translation;
- ASGI applications need ASGI translation.

FastAPI's adoption therefore reduces the greenfield population for `apig-wsgi`, because a FastAPI application is not a WSGI application. Mangum demonstrates that the direct-handler pattern remains useful on the ASGI side.

The more fundamental alternative is Lambda Web Adapter, because it removes the framework-callable protocol from the Lambda integration boundary altogether.

## Responsibility comparison

| Concern | apig-wsgi | Mangum | Lambda Web Adapter |
| --- | --- | --- | --- |
| Application boundary | WSGI callable | ASGI callable | localhost HTTP server |
| Lambda entry style | direct Python handler | direct Python handler | extension/runtime adapter |
| AWS event translation | Python package | Python package | adapter extension |
| Conventional HTTP server required | no | no | yes |
| Framework/language scope | WSGI/Python | ASGI/Python | HTTP/framework/language independent |
| Application portability without Lambda adapter | WSGI app remains portable, handler is Lambda-specific | ASGI app remains portable, handler is Lambda-specific | same server/container model is explicitly portable |
| Lifespan/readiness responsibility | WSGI semantics | ASGI lifespan | process readiness/health lifecycle |
| Streaming/process features | limited by direct proxy model | direct adapter semantics | explicit response streaming and process lifecycle features |

## Implication for the fork

This evidence strengthens rather than weakens the decision to keep `apig-wsgi` WSGI-specific.

Adding ASGI would duplicate Mangum's boundary while making this package less conceptually precise. Emulating Lambda Web Adapter would be a completely different architecture involving server/process management rather than WSGI translation.

The useful continuing role for this fork is therefore:

1. preserve and investigate the WSGI/AWS compatibility boundary;
2. make local compatibility fixes when evidence supports them;
3. keep newer mechanisms as external comparison points rather than roadmap pressure;
4. use the focused compatibility contract to explain what a replacement or bespoke adapter must consciously give up or reproduce.

## What remains untested

A real deployed comparison could still measure cold initialization, warm latency, package/image size, resident memory, and Web Adapter readiness/process overhead.

Those measurements require an actual AWS deployment environment and are intentionally not inferred from documentation.

They are not required to answer the architectural scope question, which is now sufficiently clear.
