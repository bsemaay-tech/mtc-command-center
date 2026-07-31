# Source-scenario reconciliation

- Status: **BLOCKED / PLACEHOLDER**
- Prepared: 2026-07-26
- Execution authority: none

The external scenario source referenced by KVM2-P0-05 was not supplied or
available in this authorized local batch. Its bytes, source SHA-256, normative
numbered sets, headings, titles, and line spans therefore cannot be verified.
No scenario mapping is invented.

When the source becomes available under separate authorization, record only its
SHA-256 (never its private location), enumerate every normative set, and assign
each scenario a deterministic ID:

`heading-slug + local-number + normalized-title + source-line-span`

Each ID must map exactly once to `Required`, `Allowed-later`, `Deferred`, or
`Forbidden`, with governing section, rationale, and conflict note. A mechanical
zero-unmapped-ID check is required. The master plan plus execution companion
and lower Bridge VPS task remain authoritative; the external source is
advisory. Any conflict is a blocker pending owner resolution.

Current reconciliation result: **UNAVAILABLE SOURCE / ZERO CLAIMED MAPPINGS /
P0-05 OPEN**.
