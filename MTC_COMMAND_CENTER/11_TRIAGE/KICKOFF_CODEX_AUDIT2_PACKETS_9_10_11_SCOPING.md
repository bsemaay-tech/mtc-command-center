# KICKOFF — Codex T2: scope Audit-2 packets 9, 10 and 11 to exact Stage-1 producing steps

You are Codex `gpt-5.6-sol` xhigh, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md`.
Do not edit any other package file, block, self-QA, STATUS, tool or prereg draft.
Never git checkout/reset/stash.

## Why
`AUDIT2_HANDOFF_PACKAGE.md` now records 16 of 20 coherence items closed, 1 partial, and three
genuinely NOT-YET-AVAILABLE:

- **Packet 9** — actual WP-I execution and closure evidence.
- **Packet 10** — one authoritative frozen-SHA audit bundle.
- **Packet 11** — final authority record and owner-ratified ledger closure.

These cannot be *written* today, and nobody should pretend otherwise. But they can be **scoped**:
each one is produced by a specific step of the Stage-1 sequence, and knowing exactly which step
produces which artifact is the difference between "we'll assemble it later" and a checklist that
cannot silently miss a component. Do that scoping.

## What to produce, per packet

1. **The exact component list.** Every field, file, digest, identifier or record the packet must
   contain for Audit 2 to start honestly. Derive it from the real sources — the successor
   preregistration R3 (especially §4.4 composite proof, §4.10 final merge, §5.2 two-commit
   ordering, §3 RUNID grammar), `AUDIT2_FREEZE_PREREQUISITES.md`, `AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md`,
   and the coherence review's own packet text. Cite `file:line` for each.
2. **The producing step.** For each component, name the exact Stage-1 / WP-I step that creates
   it: the committed pre-attestation command, the grant-#6 input acquisition, targeted fills,
   Commit 1, the attestation capture, Commit 2, transport ops 01–12, the host run, retrieval,
   local bind, or WP-I closure. If a component has **no** currently-defined producing step, say
   so — that is a gap worth more than a tidy table.
3. **The ordering constraints between them**, especially where packet 10's frozen-SHA bundle
   depends on packet 9's execution evidence being complete and immutable first, and where packet
   11's ledger ratification is an owner action that cannot be produced by any step at all.
4. **What can be prepared NOW versus what genuinely cannot.** Templates, field lists, and
   validation predicates can often be written before the values exist. Say which of the three
   packets could have a skeleton committed today with `<PENDING-STAGE-1>` markers, and which
   would be dishonest to skeletonise because their shape depends on results.

## Rules
- **Do not create the packets.** This is scoping, not fabrication. No placeholder value may look
  like a measurement — that exact failure (`dynamic_targets=0` as a hardcoded literal beside a
  real count) was found in RP6 today and is the reason this rule is explicit.
- Every claim carries a `file:line`.
- Where the preregistration and the Audit-2 package disagree about what a packet needs, quote
  both and say which governs.
- Note honestly that freeze blockers 7 and 9 (the `P0_ATTESTED_*` fills and the `REMOTE_BASE`
  allocation ordering) sit upstream of packet 9, so packet 9's producing steps cannot even begin
  until those close — see `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`.

## Deliverable shape
A short preamble on what scoping means here and what it deliberately does not do; then one
section per packet with the component list, producing steps, and gaps; then a combined ordering
diagram or ordered list; then a closing "what could be committed today" recommendation the Lead
can act on. Print the component counts and the count of components with no defined producing
step when done.
