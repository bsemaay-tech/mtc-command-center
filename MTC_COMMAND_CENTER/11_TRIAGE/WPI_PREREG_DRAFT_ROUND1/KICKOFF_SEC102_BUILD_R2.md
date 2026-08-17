# KICKOFF — §10.2 composite whole-program proof: build round 2 (render + freeze stages + prover integration)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, IMPLEMENTER (you authored the design + round 1).
The Claude flagship will audit. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no
network, no commit. Scope fence: touch ONLY `composite_pathproof.py`, its fixtures dir
`sec102_r1_fixtures/` (or a new `sec102_r2_fixtures/`), `SELF_QA_SEC102_R2.md`,
`STATUS_SEC102.md`, and the round-2 report. Do NOT edit `pathscope_prover.py` (a separate
audited artifact — you consume it, you do not modify it), the block files, or the prereg
drafts. Concurrent lanes own RP6/RP7 — never git checkout/reset/stash any tracked file.

## Context — commit `d490b301`

Round 1 built the scaffold + ALLOCATE stage end-to-end (6 RED + 1 GREEN fixtures, render/freeze
fail-closed STOP rc 3, Lead-reproduced). `composite_pathproof.py` 29640 B, SHA-256
`77f1076163310f331cac3effd91ccc60aaaee841757eaea54288ca5b40472c90`. Your design
(`SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`) requires one entrypoint-driven whole-program
proof per stage in allocate → render → freeze order.

The path-scope prover is now REPAIRED and committed: `pathscope_prover.py` 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` — 9 findings + 5 more
silent-sink classes closed; explicit `Spec` registry; unlisted option/command → rc-3 coverage
record; finding 6 is an honest DISCLOSURE (`ALLOW-LEXICAL`, symlink/mount as residual R1).
Its output grammar changed: `resolved_count`/`unresolved_count` are gone, replaced by seven
distinct counts + `kind=` per record.

## Task — round 2

1. **RENDER stage** proof, end-to-end, per the design: whole-program traversal of the render
   phase with per-claim GREEN + RED fixtures. Inability to evaluate STOPs (rc 3), never PASS
   and never FAIL (pattern 1). Every input member gets a disposition (pattern 13).
2. **FREEZE stage** proof, end-to-end, same discipline.
3. **Prover component integration:** replace the round-1 stub with a real adapter that invokes
   the repaired `pathscope_prover.py` behind the interface your design defined, consuming its
   NEW output grammar (seven counts + `kind=`, `ALLOW-LEXICAL`, coverage records). The
   composite must treat a prover `STOP`/coverage-record/`REJECT` as its own STOP/FAIL per the
   design's mapping — a prover silent-sink or unresolved must never become a composite PASS.
   Carry the prover's residual R1 (symlink/mount not established) forward as an explicit
   composite-level residual, not a silent assumption — a disclosure is not a control.
4. Keep the ALLOCATE stage and its round-1 fixtures passing (regression).

## Deliverables

Updated `composite_pathproof.py` + render/freeze/integration fixtures + `SELF_QA_SEC102_R2.md`
(literal commands + rc + output, RED before GREEN per D026; `PENDING-LEAD-EXECUTION` only where
your session truly cannot execute) + `STATUS_SEC102.md` (what R2 covers, what remains, every
limitation stated as a limitation) + `SEC102_R2_REPORT_2026-08-11.md`. Re-derive + record size
+ SHA-256 for every artifact. Read `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` (all 13) first.
No commit — the Lead commits and reproduces the fixtures.
