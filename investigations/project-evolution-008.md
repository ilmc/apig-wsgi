# Investigation 008: project evolution from 2018 to 2026

## Question

How has `apig-wsgi` actually evolved, and what does that history say about its present role after the rise of ASGI and newer Lambda integration mechanisms?

## Source

The upstream changelog is unusually useful because it records not just version support but many concrete AWS compatibility changes and the incidents that motivated them.

## Phase 1: establish the WSGI-to-Lambda bridge (2018)

The first release in March 2018 provided the core proposition: run an ordinary WSGI application behind API Gateway.

The early releases immediately added binary-response support and base64 request-body handling. This shows that even the original apparently simple translation boundary already depended on API Gateway transport details beyond ordinary WSGI request/response mapping.

The core value in this phase was enablement: make existing Python web applications usable in Lambda without requiring applications to understand API Gateway event structures.

## Phase 2: broaden AWS compatibility (2019–2021)

The densest product evolution happened from 2019 through 2021.

Important changes included:

- explicit ALB compatibility and integer response status handling;
- request-context exposure for authorizers;
- binary handling for compressed responses;
- configurable non-binary content types;
- multi-value headers and query parameters;
- full-event and Lambda-context exposure;
- ELB health-check compatibility;
- API Gateway payload format 2.0 support;
- path unquoting and query-string re-encoding fixes;
- ALB-specific query-string encoding fixes;
- handling `requestContext` being `None`.

This period is important because it demonstrates where the project accumulated its durable knowledge. Most changes were not about adding framework features. They were corrections and extensions at the AWS/WSGI translation boundary.

Several changes also show why a small adapter can carry disproportionate compatibility value. For example:

- adding `statusDescription` appeared reasonable but had to be reverted immediately because API Gateway rejected the response;
- a multi-value-header change accidentally broke ordinary `HTTP_CONTENT_TYPE` and `HTTP_HOST` behavior and required a follow-up fix;
- API Gateway v1, API Gateway v2 and ALB required subtly different query, header and binary-response treatment.

The historical pattern is therefore one of edge-case discovery rather than architectural expansion.

## Phase 3: protocol stabilization and Python maintenance (2022–2026)

After 2021, the rate of new AWS-facing capabilities drops significantly.

Notable protocol-level work still occurred:

- API Gateway v2 switched to `rawPath` to preserve trailing slashes and avoid framework redirect loops;
- ALB binary support became enabled by default;
- any non-empty `Content-Encoding` now forces binary transmission rather than special-casing gzip;
- `application/problem+json` became a default non-binary content type.

But much of the visible release work from 2022 onward is maintenance:

- Python 3.11, 3.12, 3.13, 3.14 and 3.15 support;
- dropping end-of-life Python versions;
- type-hint improvements;
- packaging/build modernization, including switching to `uv_build`.

This is the profile of a stable compatibility utility rather than an actively expanding application framework.

## Relationship to ASGI

The changelog does not show `apig-wsgi` attempting to react to ASGI by broadening scope.

That absence is meaningful.

During the same period that ASGI and FastAPI became common, `apig-wsgi` continued to maintain the WSGI/AWS boundary and support current Python versions. It did not become a generic Python web-to-Lambda adapter.

This suggests that ASGI affected the project primarily by reducing the greenfield population for WSGI adapters, not by invalidating the adapter's existing responsibility.

A FastAPI application needs an ASGI-aware boundary, but that does not imply that Flask/Django WSGI deployments stop needing correct Lambda translation.

## What changed about the value proposition

In 2018 the most visible value was avoiding the work of writing a Lambda adapter at all.

By 2026 that implementation work is much cheaper. A competent developer with an AI assistant can produce the obvious event-to-WSGI mapping quickly.

The changelog shows why that does not erase the library's value.

The difficult asset is the sequence of learned incompatibilities:

- transport encoding;
- event-format differences;
- ALB behavior;
- AWS test-console anomalies;
- WSGI path semantics;
- cookies and multi-value headers;
- compressed/binary response policy;
- framework-sensitive path handling.

A bespoke implementation can be short while still being subtly wrong in several of these areas.

## Current lifecycle interpretation

`apig-wsgi` appears to be in a mature-maintenance lifecycle:

1. the core abstraction is stable;
2. the main AWS event families are supported;
3. new releases are usually ecosystem maintenance or narrow compatibility corrections;
4. there is little evidence for product-scope expansion;
5. the historical test/bug record is increasingly more valuable than implementation novelty.

This is not equivalent to abandonment. The package remains maintained and tracks current Python versions.

It is also not evidence that every possible AWS behavior should be absorbed into the core. The stage-path investigation demonstrates that some deployment concerns remain better expressed as middleware or explicit configuration.

## Implication for this undertaking

The fork should not search for a dramatic modernization project simply to justify its existence.

The most credible future contributions are likely to be:

- preserving or clarifying existing protocol semantics;
- adding focused regression coverage for discovered edge cases;
- fixing small, reproducible compatibility defects;
- improving documentation where AWS topology is easy to misunderstand;
- upstreaming generally useful fixes rather than establishing a divergent implementation.

The project's historical trajectory supports restraint as a maintenance strategy.