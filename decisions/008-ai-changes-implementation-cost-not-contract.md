# Decision 008: AI changes implementation cost, not compatibility authority

## Status

Adopted for this undertaking.

## Context

Investigation 009 considered whether modern AI-assisted coding materially reduces the value of a small adapter such as `apig-wsgi`.

AI can generate the obvious Lambda-event/WSGI translation quickly. The project history, however, shows that many important behaviours were discovered through real AWS and WSGI incompatibilities rather than through obvious interface mapping.

## Decision

Treat AI as reducing implementation cost, not as replacing compatibility authority.

A bespoke or generated adapter should be evaluated against explicit behavioural contracts rather than by implementation speed, code size or apparent simplicity.

## Consequences

- Do not infer equivalence from a short successful happy-path demo.
- Use the focused compatibility contract as the minimum preservation surface for any bespoke-adapter experiment.
- Use the full upstream-derived suite before claiming parity with `apig-wsgi`.
- When a generated implementation fails a historical edge case, treat the missing requirement as evidence about specification cost rather than simply patching until the comparison looks favourable.
- Bespoke implementations remain valid when their deployment contract is intentionally narrower than the library's supported surface.

## Practical interpretation

AI strengthens the case for keeping behavioural knowledge explicit.

If implementation becomes cheap while compatibility discovery remains expensive, tests and historical evidence become a larger share of the project's durable value, not a smaller one.

## Revisit trigger

Revisit this decision if a future generated adapter can reproduce the known compatibility surface from a genuinely concise, implementation-independent specification and remain maintainable across subsequent AWS changes.

Until then, fast generation is evidence about coding economics, not about behavioural equivalence.