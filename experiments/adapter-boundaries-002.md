# Experiment: adapter boundaries 002

## Purpose

Compare three ways of running Python web applications on AWS Lambda without assuming that one is universally superior:

1. WSGI application with `apig-wsgi`;
2. ASGI application with Mangum;
3. ordinary web application process with AWS Lambda Web Adapter.

The goal is to understand where responsibility sits, what compatibility surface each mechanism owns, and which operational trade-offs remain meaningful in 2026.

## Non-goal

This is not a framework popularity contest and not an attempt to prove that WSGI or ASGI is faster in general.

The application frameworks differ too much for a naive Flask-versus-FastAPI latency result to say anything useful about the adapter boundary.

## Candidate applications

Use deliberately trivial applications whose business behaviour is equivalent:

### WSGI control

A tiny Flask or bare WSGI application with:

- one text/JSON GET route;
- one POST body echo route;
- one cookie response;
- one binary response.

Run through `apig-wsgi` as a direct Lambda handler.

### ASGI direct-adapter case

A tiny FastAPI or Starlette application with equivalent routes.

Run through Mangum as a direct Lambda handler.

### HTTP-process case

Use the same ASGI application as the Mangum case, but run it under Uvicorn with AWS Lambda Web Adapter.

This is important: Mangum versus Lambda Web Adapter should use the same application wherever possible so that the experiment isolates the adaptation boundary rather than the framework.

## Questions

### Boundary clarity

For each mechanism:

- Which component knows it is running on Lambda?
- Which component owns API Gateway/ALB event interpretation?
- Which component owns cookies, binary responses, and header translation?
- Can the application run unchanged outside Lambda?
- Does the application require a server process?

### Compatibility surface

Record which event sources are supported and where compatibility logic lives.

Do not infer capability from a successful hello-world invocation. Explicitly inspect:

- API Gateway v1;
- API Gateway v2 / HTTP API;
- Lambda Function URL;
- ALB where supported;
- multi-value headers where relevant;
- request and response binary bodies;
- multiple response cookies;
- custom-domain/base-path behaviour.

### Deployment surface

Compare:

- handler configuration;
- package/layer/container requirements;
- whether a web server is required;
- readiness/health configuration;
- environment variables specific to the adapter;
- portability to another compute environment.

### Performance questions

If performance is measured, separate at least:

- cold initialization;
- warm invocation latency;
- package/image size;
- resident memory where observable;
- process-start/readiness overhead for the Web Adapter case.

Do not present microbenchmarks as application-level conclusions.

The likely interesting comparison is not raw request throughput inside one warm Lambda. It is the operational cost of each abstraction boundary.

### Failure behaviour

Test malformed/edge-shaped requests rather than only successful routes:

- absent optional AWS fields;
- base64 bodies;
- duplicate headers;
- multiple cookies;
- encoded paths and query strings;
- application exceptions.

This is where mature compatibility libraries should have an advantage over quickly written bespoke glue.

## Expected hypotheses

### `apig-wsgi`

Expected strengths:

- very small direct-handler path;
- no HTTP server process;
- mature WSGI-specific compatibility knowledge;
- easy fit for an existing Flask/Django WSGI application.

Expected limitation:

- not applicable to ASGI-native applications without changing their interface.

### Mangum

Expected strengths:

- direct Lambda handler for ASGI;
- no need to run a conventional HTTP server;
- natural fit for FastAPI/Starlette applications.

Expected limitation:

- remains an AWS-event-to-framework adapter and therefore owns AWS-specific translation logic.

### Lambda Web Adapter

Expected strengths:

- application/server can remain ordinary HTTP;
- framework/language independence;
- greater portability between Lambda and conventional server/container environments.

Expected costs:

- a server process and readiness lifecycle exist inside the Lambda environment;
- there is an additional process/proxy boundary;
- operational configuration moves from Python handler code into deployment/runtime configuration.

These are hypotheses to test, not conclusions.

## AI-assisted bespoke control

A fourth control may be useful: ask a capable coding model to implement the smallest direct FastAPI/ASGI-to-Lambda adapter needed for the experiment without using Mangum.

Freeze that implementation before exposing it to the compatibility matrices of the mature adapters.

Then test it against the same edge cases.

This would directly test the undertaking's AI-era hypothesis:

> implementation generation has become cheap, but discovering and retaining compatibility knowledge may still be expensive.

The useful result is not whether the generated adapter passes a hello-world test. It is how much mature edge-case behaviour it misses before being shown the accumulated compatibility requirements.

## Success criteria

This experiment is useful if it produces a clear map of responsibility and compatibility trade-offs that would change how a competent engineer chooses a Lambda web deployment mechanism.

It fails if it reduces to synthetic request-per-second numbers or framework preference.

## Repository implication

No result from this experiment automatically implies a change to `apig-wsgi`.

A result may instead confirm that the package is already occupying the correct narrow boundary and that the transferable value is the compatibility knowledge encoded by its tests.
