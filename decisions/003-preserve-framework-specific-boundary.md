# Decision 003: preserve the framework-specific boundary

## Status

Adopted for this undertaking.

## Context

Current ecosystem evidence shows three distinct deployment/adaptation approaches:

1. direct WSGI-to-Lambda adaptation, represented by `apig-wsgi`;
2. direct ASGI-to-Lambda adaptation, represented by Mangum;
3. HTTP-process adaptation, represented by AWS Lambda Web Adapter.

These mechanisms solve related problems at different boundaries.

FastAPI is ASGI-native. Adding FastAPI/ASGI support to `apig-wsgi` would therefore broaden the package from a WSGI adapter into a multi-interface adapter while duplicating a role already served by established ASGI tooling.

## Decision

Preserve `apig-wsgi` as a WSGI-specific adapter unless future evidence demonstrates a concrete WSGI-related need that requires changing that boundary.

Do not add ASGI support, FastAPI-specific support, an embedded ASGI server, or Lambda Web Adapter-like process management merely to modernise the project.

## Rationale

The project's durable value is the quality of its compatibility translation between WSGI and AWS Lambda invocation shapes.

Broadening the interface would:

- weaken the package's conceptual boundary;
- create duplicate responsibility with existing ASGI adapters;
- materially expand the compatibility surface;
- make the project harder to reason about without clear evidence of consumer need.

The existence of newer deployment mechanisms is evidence for keeping the scope precise, not for making the package imitate them.

## Consequence

Future code work in this fork should focus on one of:

- preserving or clarifying WSGI/Lambda compatibility;
- improving the auditability of compatibility tests;
- fixing demonstrated defects;
- contributing narrowly useful maintenance improvements upstream.

A feature whose purpose is primarily to make the project look current is not sufficient justification.
