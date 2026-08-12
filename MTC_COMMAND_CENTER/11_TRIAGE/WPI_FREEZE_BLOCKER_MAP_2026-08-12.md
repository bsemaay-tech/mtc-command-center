# WP-I Stage-1 freeze blocker map — 2026-08-12 ~13:45

Supersedes the 10-item map in `MORNING_HANDOFF_2026-08-11.md` §4. Every item here must close
before Stage-1 freeze. Status as of this write; tonight's Claude Pro second-flagship audits
(23:00) will move items 1a–1c and 3.

## Scoreboard

| # | Blocker | 2026-08-11 state | NOW (2026-08-12 13:45) |
|---|---|---|---|
| 1a | RP6-P0 dual-flagship acceptance | open | **Codex PASS-WITH-NITS** (r16 byte-span census fixpoint); Claude Pro audit **PENDING 23:00**, now carrying the **RP6-11** priority target (see below) |
| 1b | RP7-WPI-RO dual-flagship acceptance | open | **Codex PASS** (r9 descriptor-bound status body); Claude Pro audit **PENDING 23:00** |
| 1c | Transport set dual-flagship acceptance | open | **Codex PASS** (`TRANSPORT_CODEX_R6B_CONFIRM`, commit `7e4b5e9f`, Codex slot CLOSED); F1 owner-ratified accept-with-disclosure, NOT a blocker; Claude Pro audit **PENDING 23:00**. *STATUS_TRANSPORT.md header corrected 2026-08-12 ~18:20 — it had never recorded the r6 cycle at all* |
| 2 | §8.2 rows 1–9 implemented by no executable | owner decision needed | **DECIDED: BUILD ALL NINE**, applied only AFTER RP7 dual acceptance. Not yet built — still a blocker, now with a decided path |
| 3 | §10.2 prover unsound | repair banked | pathscope r2 repaired (9+5 silent-sink classes closed; finding-6 honest `ALLOW-LEXICAL` + residual R1). Codex FILTER-BLOCKED on the source; GLM read favorable but supplemental. **Claude Pro EXECUTION-audit PENDING 23:00** |
| 4 | §10.2 needs a composite whole-program proof | design accepted | **CLOSED 2026-08-12** — SEC102 composite pathproof ACCEPTED-WITH-DISCLOSURE by owner decision (see below) |
| 5 | §10.1 needs 11 extensions + access grammar; 3 families unresolved | open | **CLOSED** — prereg R3 merges all 11 EXTEND items + the capability-qualified grammar; FAM-01/02/03 owner-RATIFIED 2026-08-12, MERGE-CONFLICT register MC-01..03 RESOLVED. Implementation of the three closures in the frozen composite remains part of item 8 |
| 6 | Attestation / preregistration / commit order circular | two-commit fix drafted | **CLOSED in the draft** — two-commit capture-then-consume procedure merged into prereg R3 (§5.2) with the mechanical order-violation check. Execution of the procedure is item 9 |
| 7 | `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs | open | **OPEN** — unchanged. A freeze-input wiring item |
| 8 | Close-script preregistered contract vs actual bytes disagree | open | **RECLASSIFIED 2026-08-12** — the contract disagreement is GONE (plan and script both three-arg; the stale record is corrected). What remains is a freeze-input fill: `EXPECT_UID`/`EXPECT_GID` are `<PIN-AT-FREEZE>`, so the close boundary cannot yet be exercised. Merges into item 7's class |
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

## NEW 2026-08-12 ~14:40 — one open D026 gap, and the freeze-input picture

**RP6-11 — RESOLVED 2026-08-12 ~15:40 by round 17, with one claim corrected on the way.**
`AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` mapped 39 closure rows
(**as first written**: 28 fully closed, 11 supplemental/unlocated, 15 disclosed residuals —
**superseded, the current figures are 29 / 10 / 15 with 0 open**, see the correction section
below) and surfaced exactly one current-audit RED with no repaired GREEN: the round-15 F3
**dynamically-resolved inventory-mutation target**.

The GLM advance read-audit answered it with a claim that turned out to be **half right**:

- **WRONG — "the r16 fence admits a variable-mutating `eval` and certifies it CLEAN."** The
  checked-in fence already refuses `eval`, `source` and `.` as
  `UNMODELED kind=indirect_execution_builtin:*` (`SELF_QA_RP6.md:16763-16765`). Codex found this
  and said so in its own r17 report rather than building on a bad premise. **The Lead's earlier
  "confirmed by direct source read" was partial** — it verified that `eval` is in
  `admissible_bare` and absent from the enumerated mutating-builtin list (both true) and then
  accepted the conclusion without checking whether another branch catches it. It does.
  Membership in `admissible_bare` only suppresses the unbound-invocation check; classification
  happens elsewhere.
- **RIGHT — `dynamic_targets=0` was a hardcoded literal presented as a measurement**
  (`:17571`), beside a genuinely measured `variable_targets=$n_vt`. R17's pass-format audit found
  **six** such literal-zero fields across three r16 success lines.

**Round 17 (Codex, `gpt-5.5` xhigh) closes the real half by inversion, not enumeration:** a
closed effect model over the tokenizer stream where any bare word outside the modelled set is an
opaque execution surface that fails with an unmodeled record, and `dynamic_targets` is now
measured as `dynamic_variable_target + indirect_execution_builtin + effect_model_unmodeled`.
Because the shipped fence already refuses these constructs, the RED side uses a temporary r16
fence with **only** the indirect-execution refusal removed — labelled explicitly, not implied as
a live defect. Two structurally different class members (`eval` by name concatenation,
`dot_source` via a constructed runtime file).

**Lead verbatim run:** `R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS`, outer
rc 0, carried r16 grammar `50/50` with no previously-killed mutant surviving,
`r17_literal_zero_measurements=0`, block identity unchanged (110817 B, `5132bacd…`).
`RP6-P0.sh` is byte-identical — QA-layer round like r10→r16.

**Freeze-input ledger findings** (`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`, 45 rows: FILLED 2,
LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 1, REQUIRES-HOST 13):

- **Item 7 sharpened.** `run_p0.sh` defines, exports and logs all five `P0_ATTESTED_*` values as
  `<PIN-AT-FREEZE>` literals while RP6 requires and cross-checks them. With 17 remaining freeze
  literals **RP6 cannot produce an end-to-end P0 PASS** — the Codex r16 acceptance is a
  source/audit acceptance, not a host end-to-end PASS. That distinction must be carried into
  Audit 2 and never blurred.
- **Item 8 materially narrowed.** Plan rows 07/08 and `remote_close_tree_wpi.sh` now AGREE on the
  three-argument contract (`EV_DIR RUNID WORK_ROOT`); the inherited-TMPDIR question is settled in
  the bytes (run-owned `close_work_$RUNID`, disjointness proven, `TMPDIR` exported to it). The
  residual contradiction was **documentary** — and it is now **CORRECTED** (2026-08-12 ~15:05).
  GLM's advance transport read-audit cross-checked the ledger and found
  `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` stale in **two** respects, not one: the two-arg
  claim *and* the "exits FAIL on argc" claim (an argv-count violation returns **rc 3 STOP**, not
  rc 1 FAIL — operator-side composition input is never a host finding). Both are struck and
  corrected in place with sources. What actually blocks the close boundary today is the unfilled
  `EXPECT_UID`/`EXPECT_GID` pins, which STOP execution before the RUNID/`EV_DIR` grammar checks —
  i.e. item 8 is now a **freeze-input fill** problem, not a contract disagreement.
- **Item 9 has an exact ordering chain now:** allocate one burn-ledger base → derive
  `REMOTE_BASE`/`EV_*`/transport paths → fill RP7's `WPI_FIXED_EVIDENCE_ROOT` **before** RP7
  bytes are frozen (RP7 rejects a marker evidence root) → run the FAM-03 frozen-composite
  conservation proof. Until that sequence runs, the RO evidence-root literal and the transport
  retrieval/bind paths are not frozen inputs.

## NEW BLOCKER-CLASS 2026-08-12 evening — four Audit-2 components with NO producing step

`AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md` scoped the three
NOT-YET-AVAILABLE packets to 42 components and asked which have no defined producing step at all.
**Five do.** These are not documents that can be written later from existing material — each
needs a **procedure to be decided first**, and four of them are technical:

| ID | Component | Why it is a gap |
|---|---|---|
| **P9-15** | Frozen-SHA static minimum-security / secret-scan / egress inventory | The checklist *requires* the record but names no command, author, output contract, or point between Commit 2 and WP-I closure that produces it. Requirement exists; executable contract does not |
| **P10-10** | Mandated-suite **definition** — `MANDATED_COMMAND`, `EXPECTED_EXIT_CODE`, pass/fail counts, accepted-failure IDs and signatures, skip/xfail counts, `BASELINE_SOURCE` | No authoritative command or baseline source has ever been selected. **This is a decision, not a document** |
| **P10-11** | Frozen-SHA suite **execution record** | Undefined *because* P10-10 is unresolved — you cannot specify how to record a run whose command is not chosen. Cascades from P10-10 |
| **P10-12** | Accepted **anomaly register** | The current anomaly set is wholly unresolved, and the refreshed package forbids inferring the old two-failure example. Codex's requirement is exact: **an empty anomaly set must be an observed and adjudicated result, never a hardcoded count** — the same defect class as RP6's `dynamic_targets=0` |
| P11-08 | Owner ratification of the freeze-time ledger | **Deliberately not automatable** — an owner action. Naming it as a gap is correct, not a failure |

**P10-10 is the root of a three-component cascade and is the highest-value item here**: deciding
what the mandated suite actually *is* unblocks P10-11 and P10-12 together.

Ordering note carried from the ledger: freeze blockers 7 and 9 (the `P0_ATTESTED_*` fills and the
`REMOTE_BASE` allocation ordering) sit **upstream of packet 9**, so packet 9's producing steps
cannot begin until those close.

## RP6 self-QA carries EIGHT unpasted transcript slots — isolated to RP6

A full-coverage claim audit of `SELF_QA_RP6.md` (all 18,799 lines, 1,863 output lines checked)
found **eight placeholder transcript slots still unresolved**, while the document states at
`:13492-13505` and `:15995-16000` that they were resolved and are real captured output:

`:15341` `@@R15_GRAMMAR_TRANSCRIPT@@` · `:15651` `@@R15_F1_RED_TRANSCRIPT@@` · `:15763`
`@@R11_GUARDS_TRANSCRIPT@@` · `:15807` `@@RERUN_BLOCK@@` · `:18241` `@@R16_GRAMMAR_TRANSCRIPT@@`
· `:18524` `@@R16_F1_RED_TRANSCRIPT@@` · `:18645` `@@R11_GUARDS_TRANSCRIPT@@` · `:18690`
`@@RERUN_BLOCK@@` — plus `STATUS_RP6_P0.md:284` `@@STATUS_EXEC_BLOCK@@`.

These hold the round-15 closure, the **round-16 discriminating-power proof**, the guard census
and the mandated rerun vector — the document-local support for the fixpoint claim itself.

**Two things that bound this correctly:**

1. **The evidence exists; it is not pasted.** The Lead ran `R16_GRAMMAR` verbatim (50/50) and
   `R17_DYNAMIC_TARGETS` verbatim (15/15, carried r16 grammar 50/50) from outside the repo, and
   the Codex r16 audit independently reproduced its run. The live question is whether the
   document carries its own proof, not whether the proof was ever obtained.
2. **The defect is isolated to RP6.** A Lead sweep of every other self-QA and STATUS file —
   RP7, transport, pathscope, SEC102 r11, and all four STATUS documents — found **zero**
   standalone placeholders. This is not a package-wide practice.

*Lead-accuracy note: an earlier Lead grep reported three, not eight — the pattern omitted digits
and silently missed every slot with a round number in its name. The corrected figure was
re-derived and matches the audit exactly. Fourth time today a narrower check missed what a wider
one found, and the first time the narrow check was the Lead's own.*

## Record-quality findings 2026-08-12 evening — a pattern worth naming

Four record defects were found today, and **none of them was found by an auditor**. Three came
from Lead spot-checks or independently-dispatched cross-checks; one came from a systematic sweep
dispatched because of the first three. Listed because the pattern, not the individual defects, is
the finding:

1. **False implementer attribution** — both r17 records named `gpt-5.6-sol`; the run log recorded
   `gpt-5.5`. Corrected in both files.
2. **Summary updated, detail left stale** — the D026 map's `RP6-11` table row still read
   `UNLOCATED`/`OPEN` after the Lead updated only the summary for round 17. Corrected; counts
   moved to 39 rows / 29 closed / 10 supplemental / 15 residuals / 0 open, which also dissolved
   the map's only double-count.
3. **Stale line citation** — the freeze-input ledger cited `STATUS_RP6_P0.md:311-312`; round 17
   and the attribution fix had shifted it to `:396-397`. Claim content was true throughout.
4. **A whole audit cycle missing from a status file** — `STATUS_TRANSPORT.md` never recorded the
   round-6 Codex cycle, including a REQUEST_CHANGES on a false "nine-file unchanged" byte-identity
   claim and the r6b PASS that closed the Codex slot. The file had been edited the same day for
   the owner's F1 ratification, and that edit went in without the audit history. State was
   **understated**, not overstated.

**Verified clean in the same sweeps:** 14 artifact identities re-derived and all matching; the
17-vs-27 freeze-literal figures reconciled (distinct definitions vs raw occurrences, both
correct); all eleven RP6 consumer citations still accurate; the R15:180 citation accurate.

**Honest limitation recorded:** Claude/Max run logs carry no model header and
`RP6_R16_MAX_RUN_2026-08-12.log` is 0 bytes, so implementer attribution can be machine-verified
only for Codex-implemented rounds. Max-implemented rounds rest on the dispatch record alone.

## Repo-wide durability item (open, freeze-time)

The scoped `WPI_PREREG_DRAFT_ROUND1/.gitattributes` pins the SEC102 fixtures `-text` and the two
tools `text eol=lf` so a fresh Windows checkout cannot break the frozen identity hashes. **The
same risk applies to every fixture-based block (RP6, RP7, transport)** — a repo-wide durability
sweep is still an open freeze-time item. Deliberately NOT executed today: tonight's verbatim
re-runs depend on the current checkout identities, so changing attributes mid-cycle would
invalidate them. Schedule it after tonight's audits complete.
