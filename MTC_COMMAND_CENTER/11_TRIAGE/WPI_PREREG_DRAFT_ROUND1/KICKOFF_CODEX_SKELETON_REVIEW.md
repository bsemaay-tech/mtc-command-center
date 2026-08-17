# KICKOFF — review the successor preregistration skeleton against what Stage 1 must prove

Fresh `gpt-5.6-sol` session, effort high. **Analysis only**, one output file, no commit,
no host contact, no network. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.

## Why this review exists

The successor preregistration is the document that must be committed **before** anything
runs. If it is wrong, the run is worthless — evidence produced against a defective
preregistration cannot be repaired afterwards. This review is the last cheap chance to
find what it omits.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md` — the skeleton.
2. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — the current draft it derives
   from; §10.1 (allowlist), §10.2 (what Stage 1 must emit), §4, §8.2.
3. `WPI_PREREG_DRAFT_ROUND1/SEC101_RECONCILIATION_CODEX_2026-08-10.md` — 20 bounded path
   families (8 covered / 11 extend / 1 change-block) plus 3 unresolved families.
4. `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_LEAD_RERUN_2026-08-10.md` — the Lead's reproducible
   prover run and its conclusions.
5. `WPI_BLOCKS_DRAFT/RP6-P0.sh`, `RP7-WPI-RO.sh` — current bytes (read-only).
6. `NEW_SESSION_KICKOFF_2026-08-10_EVENING.md` §5 — the six freeze-gate inputs, all still
   `<PIN-AT-FREEZE>`, and the trap in §5 about blind global fills.

## What to check

1. **Pin completeness.** Does the skeleton name every value that must be filled before any
   invocation — the projection digest, both trusted-interpreter paths, the row-8 execution
   domain literals, the transport covering-mount identity, and the four recorded in
   `TRANSPORT_REPAIR_R3_REPORT.md`? List anything the blocks require that the skeleton does
   not mention.
2. **Per-constant fill, never a blind replace.** `transport_runner.ps1`'s
   `$UNFILLED_MARKERS` array compares against the literal `<PIN-AT-FREEZE>` string, so a
   global search-and-replace would give that guard a real value and make it STOP on a
   correctly frozen file. Does the skeleton's fill procedure make a blind replace
   impossible, or merely discourage it?
3. **Ordering.** The read-only attestation command set (owner grant #6) produces the pins
   and must run **before** operation 01. Does the skeleton put it there, and does it forbid
   any op running before the preregistration is committed?
4. **RUNID minting.** The skeleton must mint RUNIDs and demonstrate the refusal set of
   `rp0_require_safe_component`. Are the proposed RUNIDs actually accepted by that
   predicate, and is the refusal demonstration specific rather than gestural?
5. **§10.2 realism.** The Lead's run shows the prover STOPs at rc 3 on the real inputs and
   that RP6's unresolved set starts at the evidence-allocation boundary (`RUNID`,
   `EV_STAGE_ID`, `rp0_require_safe_component` having no path-argument contract). Stage 1
   therefore cannot close either block's path set from the block source alone — it needs
   the composite wrapper + RP0-LIB + RP0-BOOTSTRAP + block input. Does the skeleton say so?
   If not, state exactly what it must say.
6. **§10.1 delta.** Does the skeleton have a place for the 11 EXTEND entries and the
   proposed access-qualifier grammar (`read-exact`, `read-tree`, `read-terminal`,
   `read-execute-exact`, `write-tree`, `connect`)? Is one qualifier per rule sufficient, or
   does it need refining?
7. **Anything preregistered that the blocks no longer do, or do differently.** Six RP6
   rounds and four RP7 rounds have moved; the draft may have drifted.

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/SKELETON_REVIEW_CODEX_2026-08-10.md`: a verdict
(`READY-TO-FILL` / `NEEDS-WORK: <n> items`), then one section per gap with the exact
sentence or clause you propose adding, then a short section listing anything in the
skeleton that is already correct and should not be touched. Do not edit the skeleton or
the draft — the Lead applies changes.
