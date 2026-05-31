# ADR-0016 - MVP-1 read model and path/config contract

Status: Accepted

Context: MVP-1 must not invent file paths or schema assumptions during coding.

Decision: Freeze MVP-1 read files in `MVP1_READ_MODEL.md` and validate paths through `paths.schema.json`.

Consequences: API and UI share the same read contract.
