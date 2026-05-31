# ADR-0015 - command allowlist and network gate

Status: Accepted

Context: Free-form dashboard shell execution is unsafe.

Decision: Dashboard-triggered commands must be named allowlisted operations; outbound network access requires explicit task permission.

Consequences: MVP-1 remains read-only and command-free.
