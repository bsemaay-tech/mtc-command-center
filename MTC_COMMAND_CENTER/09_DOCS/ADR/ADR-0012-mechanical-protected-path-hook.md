# ADR-0012 - mechanical protected-path hook

Status: Accepted

Context: Documentation policy alone is not enough for agents with shell access.

Decision: Provide a git hook that blocks protected staged paths without an approval token.

Consequences: Protected-path enforcement becomes mechanically testable.
