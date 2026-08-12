# KICKOFF — Codex T2: the current-cycle D026 consolidation map (Audit-2 packet 7)

You are Codex `gpt-5.6-sol` xhigh, ANALYST/EDITOR. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit, **no block-byte edits**. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md`.
Do not touch `RP6-P0.sh`, `RP7-WPI-RO.sh`, the transport set, `composite_pathproof.py`,
`pathscope_prover.py`, prereg drafts, or any STATUS/SELF_QA file. Never git checkout/reset/stash.

## Why this exists
`AUDIT2_COHERENCE_CODEX_2026-08-10.md` missing-material packet 7 is still OPEN: the package maps
mostly the older WP-L/B3 cycle and does **not** map the current WP-I repair cycles. This is one
of the five remaining Audit-2 packets and it is the one that can be closed today, because all
its inputs already exist in the repo.

## What to produce
For **every closure test offered as evidence in the current WP-I cycle**, one row with:
exact RED command + output signature, the exact pre-fix or mutation identity that made it RED,
exact GREEN command + output signature, and the final accepted bytes (path + size + SHA-256)
the GREEN was measured on.

Cover all five workstreams, reading their published self-QA and audit chains:

1. **RP6-P0** — `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` (rounds 10→16) + `RP6_CODEX_T0_AUDIT_R*`.
   The census regress r10→r16 closed one evasion class per round; r16 is the exact-byte-span
   fixpoint (`R16_GRAMMAR` 50/50). Block bytes UNCHANGED since r10a
   (110817 B, `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`).
2. **RP7-WPI-RO** — `SELF_QA_RP7.md` (round 9) + `RP7_CODEX_T0_AUDIT_R9`. The descriptor-bound
   status body, the `return 7` mutant, the deleted `wpi_alloc_leaf`.
3. **Transport set** — `SELF_QA_TRANSPORT.md` (rounds 4→6b) + the Codex audit chain. Note F1 is
   owner-ratified accept-with-disclosure (OPEN, not a blocker) — map it as a disclosed residual
   with no GREEN, not as a missing test.
4. **SEC102 composite pathproof** — `WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R11.md` (the accepted
   round) + `SEC102_CODEX_T1_AUDIT_R7..R11`. Includes the harness chain D026s: r8 newline
   (`WRITTEN_CRLF=110` vs `BYTE_IDENTICAL=1`), r10 object pinning (`WINERROR=32`), r11
   nameless channel (`FALSE_ACCEPT_UNDER_R10=1`, `M4_CHANNEL_LOAD_BEARING=1`).
   Module bytes UNCHANGED r8→r11 (129658 B, `adbf27fd…c05a`).
5. **pathscope prover r2** — `SELF_QA_PATHSCOPE.md` + the round-1 Codex findings + the GLM
   read-audit. RED 511 / GREEN 644, determinism `equal=True`.

## Rules that make this map honest
- **Do not upgrade an unlocated row.** If a claimed test has no exact RED location, say
  `UNLOCATED — supplemental` and leave it. The older register's failure mode was exactly this.
- **A current audit RED with no repaired GREEN stays OPEN** — list those separately and count
  them; that count is a freeze-relevant number.
- **Helper-only or non-literal fence evidence is supplemental**, never closure.
- Where a test's GREEN was measured on bytes that have since changed, say so — the GREEN does
  not carry forward to different bytes.
- Mark clearly which rows were **Lead-run verbatim**, which were **auditor-reproduced**, and
  which are **author-claimed only**. That three-way split is the point of the map.

## Deliverable shape
A short preamble stating what the map covers and its honest limits; then one table per
workstream; then a summary block with: total closure tests mapped, fully-closed (RED+GREEN on
current bytes), open (RED without GREEN), unlocated/supplemental, and disclosed residuals with
no test by design. End with a plain sentence on whether packet 7 can now be marked CLOSED in
`AUDIT2_HANDOFF_PACKAGE.md`'s changelog (the Lead will make that edit — do not make it yourself).

Print a summary of the counts when done.
