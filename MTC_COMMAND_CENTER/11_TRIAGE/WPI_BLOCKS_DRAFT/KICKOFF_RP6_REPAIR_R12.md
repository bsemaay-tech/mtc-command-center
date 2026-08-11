# KICKOFF — RP6-P0 round 12: two findings from the Codex r11 T0 audit

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex is auditor of record.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF only,
zero CR bytes. Never `git checkout` a block file — use `git cat-file blob <sha>:<path>`.
Scope fence: touch ONLY `RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report.
A concurrent Max lane owns `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` — do NOT touch those. Files here
carry uncommitted concurrent-lane work; never git checkout/reset/stash any tracked file.

## Input bytes

`RP6-P0.sh` at commit `55a1c6ec`, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. Three of four round-10
findings are CLOSED (guards executable, R9RED status-preserved rc1, STOP-vs-FAIL both
classifiers). Do not touch what works.

## Binding scope

`RP6_CODEX_T0_AUDIT_R11_2026-08-11.md` — REQUEST_CHANGES ×2.

### 1 (HIGH) — the census still misses constructed/quoted emitter command words
The R11 census (`SELF_QA_RP6.md:6847-6856`) greps for the CONTIGUOUS text `p0_stop`/`p0_fail`
or the contiguous result literal. A valid reachable emitter can be assembled from adjacent
quoted+unquoted segments, e.g. inserted after `p0_probe_kind() {`:
```bash
[ -z "${P0_R11_CMDQUOTE_MUTANT:-}" ] || p0_s""top "r11_cmdquote detail=quoted_command_word"
```
`bash -n` = 0; the shell resolves `p0_s""top` to `p0_stop` and emits `P0_STOP` at rc 3; but
the census reports `unmodeled=0` and the fence PASSes. Pattern 12 — the census is not
fail-closed against constructed command words. `STATUS_RP6_P0.md:20-21` and
`RP6_R11_REPORT_2026-08-11.md:86-90` overstate the property as fail-closed.
**Repair:** replace/strengthen the census so quoted, continued, or otherwise constructed
wrapper command words and result literals cannot disappear. An AST/tokenizer-backed check, or
an explicit fail-closed source-style policy that REJECTS every syntax it does not model
(rather than assuming a contiguous grep token), is acceptable. Add the command-word-
fragmentation mutant (`p0_s""top` and at least one more form, e.g. `p0_stop` via `${x}`
expansion or a line-continuation split) to D026: RED on the current fence, nonzero on the
repaired fence. Correct the STATUS/report fail-closed wording to exactly what the new census
guarantees.

### 2 (MEDIUM) — a stale F4 overclaim comment inside the live R10_F4 harness
`SELF_QA_RP6.md:6194-6199`: the in-harness comment still says "Every input class that leaves
the binding unset is shown" then lists only omitted/unfilled/disagreeing pins. The prose
above the fence was narrowed but this comment was not (Pattern 9). One-line fix:
**Repair:** change the comment to "the three input classes this fence executes" (or
equivalent) and retain the explicit list. No harness widening.

## Deliverables

Repaired `RP6-P0.sh` (only if finding 1's census lives in the block; if the census is a QA
harness, the change may be QA-only — say which) + `SELF_QA_RP6.md` + `STATUS_RP6_P0.md` +
`RP6_R12_REPORT_2026-08-11.md` (per-finding disposition, D026 RED-before-GREEN executed for
the census mutant). Do not weaken any carried fence without a per-change discriminating-power
proof. No commit — the Lead commits and runs every published command verbatim.
