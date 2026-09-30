# Investigation 009: AI-assisted bespoke adapters

## Question

If a capable developer can now ask an AI system to produce a Lambda-to-WSGI adapter in a very short time, what value remains in a maintained library such as `apig-wsgi`?

## Distinguish two costs

AI changes two different costs unevenly.

### Implementation cost

The obvious translation is small:

1. identify the AWS event family;
2. construct a WSGI environ;
3. call the WSGI application;
4. collect status, headers and body;
5. serialize a Lambda proxy response.

Generating that structure is now cheap. Even without AI, the current implementation is compact enough to understand in one sitting.

### Compatibility-discovery cost

The historical project record contains requirements that are much less obvious from first principles:

- API Gateway v1 query values need different quoting behavior from ALB query values;
- API Gateway v2 has dedicated cookie request/response fields;
- multi-value headers change the output shape;
- binary defaults differ across event families;
- compressed textual responses must still travel as binary;
- missing content type affects binary policy;
- `requestContext` may be `None` in direct Lambda invocation paths;
- ALB health checks can omit normal host/scheme information;
- v2 must use `rawPath` to preserve trailing-slash semantics;
- WSGI response iterables need cleanup through `close()`;
- seemingly plausible fields such as ALB/API Gateway `statusDescription` can produce incompatible responses.

AI can implement these once specified. It does not eliminate the need to know that they matter.

## The prompt problem

A request such as:

> Convert an API Gateway Lambda proxy event into a WSGI request and return the response.

is underspecified relative to the project's learned compatibility surface.

A generated implementation may be internally tidy and pass happy-path examples while still differing from production behavior on headers, query encoding, cookies, binary payloads or event-family defaults.

The relevant comparison is therefore not:

> Can AI write something shorter than `apig-wsgi`?

It clearly can.

The relevant comparison is:

> Can the generated implementation satisfy the known compatibility contract, and how much specification/test evidence must be supplied before it does?

## Role of the focused compatibility contract

Decision 006 established a small contract of particularly non-obvious behaviors:

- ALB reserved-character query preservation;
- v2 cookie collection/header merging;
- different v1/ALB binary defaults;
- WSGI iterable cleanup.

These cases provide an appropriate minimum challenge for a bespoke-control experiment.

A generated adapter that cannot satisfy this small contract has not yet reproduced even the representative edge knowledge accumulated by the library.

Passing the focused contract would still not prove parity with the full suite. It would only justify continuing the comparison.

## Where bespoke code can still win

A custom adapter may be rational when the deployment surface is intentionally narrow.

Examples include an application that guarantees:

- only one event format;
- no ALB support;
- known text-only responses;
- no multi-value headers;
- no unusual cookie handling;
- no need for general third-party WSGI compatibility.

In that situation the correct bespoke implementation may legitimately omit most of `apig-wsgi`'s compatibility surface.

The value of custom code is then not that it secretly replaces the full library. It is that the application has explicitly narrowed the contract.

## Where a library still wins

A maintained adapter remains attractive when:

- multiple AWS proxy event families are possible;
- arbitrary WSGI applications/frameworks must work;
- edge behavior should be inherited rather than rediscovered;
- upgrades in AWS/Python behavior should be absorbed centrally;
- test evidence matters more than minimizing line count.

## Implication

AI makes a full rewrite easier to attempt, which increases rather than decreases the importance of explicit compatibility tests.

Without a contract, 'we can rewrite this quickly' measures typing speed.

With a contract, it becomes a meaningful engineering comparison.

## Proposed future experiment

If the undertaking wants to test the AI hypothesis directly:

1. generate a bespoke adapter from a concise requirements prompt without exposing the `apig-wsgi` implementation;
2. run it against the focused compatibility contract;
3. record failures;
4. improve the prompt/specification rather than copying implementation details;
5. then run against the full upstream suite;
6. compare implementation size and, more importantly, the amount of compatibility specification required to reach parity.

The experiment should treat discovered failures as the result, not as an obstacle to be hidden by iterative copying.