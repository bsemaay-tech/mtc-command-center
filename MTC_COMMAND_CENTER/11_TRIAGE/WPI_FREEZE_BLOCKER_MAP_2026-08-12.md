# WP-I Stage-1 freeze blocker map — 2026-08-12 ~13:45

Supersedes the 10-item map in `MORNING_HANDOFF_2026-08-11.md` §4. Every item here must close
before Stage-1 freeze. Status as of this write; tonight's Claude Pro second-flagship audits
(23:00) will move items 1a–1c and 3.

## Scoreboard

| # | Blocker | 2026-08-11 state | NOW (2026-08-12 13:45) |
|---|---|---|---|
| 1a | RP6-P0 dual-flagship acceptance | open | **Codex PASS-WITH-NITS** (r16 byte-span census fixpoint); Claude Pro audit **PENDING 23:00** |
| 1b | RP7-WPI-RO dual-flagship acceptance | open | **Codex PASS** (r9 descriptor-bound status body); Claude Pro audit **PENDING 23:00** |
| 1c | Transport set dual-flagship acceptance | open | **Codex PASS** (r6b confirm); F1 owner-ratified accept-with-disclosure, NOT a blocker; Claude Pro audit **PENDING 23:00** |
| 2 | §8.2 rows 1–9 implemented by no executable | owner decision needed | **DECIDED: BUILD ALL NINE**, applied only AFTER RP7 dual acceptance. Not yet built — still a blocker, now with a decided path |
| 3 | §10.2 prover unsound | repair banked | pathscope r2 repaired (9+5 silent-sink classes closed; finding-6 honest `ALLOW-LEXICAL` + residual R1). Codex FILTER-BLOCKED on the source; GLM read favorable but supplemental. **Claude Pro EXECUTION-audit PENDING 23:00** |
| 4 | §10.2 needs a composite whole-program proof | design accepted | **CLOSED 2026-08-12** — SEC102 composite pathproof ACCEPTED-WITH-DISCLOSURE by owner decision (see below) |
| 5 | §10.1 needs 11 extensions + access grammar; 3 families unresolved | open | **CLOSED** — prereg R3 merges all 11 EXTEND items + the capability-qualified grammar; FAM-01/02/03 owner-RATIFIED 2026-08-12, MERGE-CONFLICT register MC-01..03 RESOLVED. Implementation of the three closures in the frozen composite remains part of item 8 |
| 6 | Attestation / preregistration / commit order circular | two-commit fix drafted | **CLOSED in the draft** — two-commit capture-then-consume procedure merged into prereg R3 (§5.2) with the mechanical order-violation check. Execution of the procedure is item 9 |
| 7 | `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs | open | **OPEN** — unchanged. A freeze-input wiring item |
| 8 | Close-script preregistered contract vs actual bytes disagree | open | **OPEN** — unchanged (prereg §4.7 states the gate; bytes not yet reconciled) |
| 9 | `REMOTE_BASE` must be allocated before the RO block is frozen | open | **OPEN** — ordering understood and preregistered; the allocation + targeted fills are Stage-1 execution work |
| 10 | Audit-2 readiness package obsolete (NEEDS-UPDATE: 20) | open | **15/20 CLOSED 2026-08-12** (all 9 stale claim groups + packets 1–6, new acceptance matrix). Packets 7–11 honestly OPEN: D026 consolidation, freeze-input ledger, WP-I execution evidence, frozen-SHA bundle, authority/ledger record |

**Closed since yesterday: items 4, 5, 6 and most of 10. Three Codex flagship acceptances banked
(1a/1b/1c) awaiting their second flagship tonight.**

## Item 4 detail — SEC102, closed today

Owner decision 2026-08-12 ~13:10: **ACCEPT WITH DISCLOSURE** (Option 1 of
`SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md`), with Codex's explicit
concurrence that no round 12 should be opened. `composite_pathproof.py` is byte-identical
across rounds 8–11 and HEAD (129658 B, `adbf27fd…c05a`). Both original CRITICALs, the
command-word whitelist fixpoint, R3-F2/F3, and the evidence-harness chain r7→r11 are closed and
cross-model verified.

Four trusted-base assumptions ride forward as **disclosures, not controls**, and must be carried
into the successor preregistration verbatim: (1) the outer Python runtime/startup/import graph is
unbound (Codex R11-F1); (2) `powershell.exe` is PATH-resolved (residual 51, adjudicated honest);
(3) byte identity is against the on-disk document, not a pinned checkout — a rewriting clone
fails LOUDLY (residual 41); (4) the interpreter vocabulary is an owner-ratified production-gate
item (decision C). All four require an actor who already controls this host.

GLM-5.2 second-opinion evidence is being attached separately; it is evidence, not a gate.

## What actually stands between here and Stage-1 freeze

1. **Tonight (23:00):** four Claude Pro second-flagship audits → items 1a, 1b, 1c, 3.
2. **After RP7 dual acceptance:** build §8.2 rows 1–9 (item 2), then re-audit the changed bytes.
3. **Freeze-input wiring:** items 7, 8, 9 — `P0_ATTESTED_*`, the close-script contract
   reconciliation, and `REMOTE_BASE` allocation ordering, plus implementing the three ratified
   §10.1 family closures in the frozen composite.
4. **Stage-1 execution:** committed pre-attestation command → grant-#6 input acquisition →
   targeted fills → final successor/runkit commit (the two-commit order from item 6).
5. **Audit-2 package:** packets 7–11 (item 10), most of which can only close after the WP-I run
   produces real evidence.

**We are not close to freeze, but the shape has changed:** yesterday's blockers were mostly
"the proof tools are unsound"; today's are mostly "the wiring and the run have not happened yet."
The remaining proof-tool question is item 3, and it has a scheduled auditor tonight.

## Repo-wide durability item (open, freeze-time)

The scoped `WPI_PREREG_DRAFT_ROUND1/.gitattributes` pins the SEC102 fixtures `-text` and the two
tools `text eol=lf` so a fresh Windows checkout cannot break the frozen identity hashes. **The
same risk applies to every fixture-based block (RP6, RP7, transport)** — a repo-wide durability
sweep is still an open freeze-time item. Deliberately NOT executed today: tonight's verbatim
re-runs depend on the current checkout identities, so changing attributes mid-cycle would
invalidate them. Schedule it after tonight's audits complete.
