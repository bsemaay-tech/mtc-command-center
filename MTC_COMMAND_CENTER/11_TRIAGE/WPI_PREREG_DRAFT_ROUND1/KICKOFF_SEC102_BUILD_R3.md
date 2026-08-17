# KICKOFF — SEC102 composite pathproof round 3: fix the two CRITICAL identity-binding defects

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. You AUDITED round 2 and found
these defects, so you understand them exactly; Codex `gpt-5.6-sol` (the round-1/2 author) will
audit round 3 as the independent cross-model flagship, so separation holds on the re-audit.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch
ONLY `composite_pathproof.py`, `sec102_r2_fixtures/` (add fixtures; keep existing), a new
`sec102_r3_fixtures/` if you prefer, `SELF_QA_SEC102_R3.md`, `STATUS_SEC102.md`, and the round-3
report. Do NOT touch `pathscope_prover.py` (consumed, not modified), the block files, RP6/RP7,
or the prereg drafts. Concurrent lanes are writing other files — never git checkout/reset/stash
any tracked file. UNIX LF for shell fixtures.

## Input — commit `35a15219`

`composite_pathproof.py` 84950 B. Your own round-2 audit is
`SEC102_CLAUDE_T1_AUDIT_R2_2026-08-11.md` — its findings and its "Required before re-audit"
list BIND. This is a scope note, not a new authority: it is tool-internal plan-schema work
inside WP-I (the `sec102-composite-plan-v1` format), NOT the repo's protected `06_SCHEMAS`
trading surface and NOT any host/ARM/credential action.

## The binding repairs (from your §7 required-list)

### F1 (CRITICAL) — operand↔member bound by basename, so analyzed bytes ≠ executed bytes
`_member_for_operand` (`:900`) and `SubprocessPathProver._build_analysis_unit` (`:1380`)
resolve/lookup members by `posixpath.basename(...)`. Consequence: any operand ending in
`/library.sh` binds to member `library`, the prover splices the PINNED member's bytes, and the
real operand target is only a `test -r` readability probe — so a deployed path pointing at
non-member bytes (your falsification: `/safe/fixture/evil/library.sh` doing
`cat /etc/shadow; curl exfil`) is never analyzed and all stages PASS.
**Repair:** add an explicit schema field for each member's DEPLOYED path (the absolute path it
is referenced by); match an operand to a member by EXACT deployed-path identity (normalized
realpath equality), never basename; DELETE the basename fallback in both sites; an operand that
matches no member by exact identity is a STOP (rc 3), never a PASS or a readability-probe-only
path. The analysis unit must be built from the member's own pinned bytes AND the composite must
prove the operand's target IS that member (identity), or STOP.

### F2 (CRITICAL) — plan allocations and `constants.env` are two unreconciled sources
The composite resolves `$LIBRARY_PATH` from plan allocations to pick the member, then emits the
operand RAW so the prover re-resolves the SAME variable from `constants.env` — a separately
pinned file — and nothing compares the two. Falsification: allocation
`LIBRARY_PATH=/safe/fixture/library.sh` vs `constants.env`
`LIBRARY_PATH=/safe/fixture/somewhere/else/library.sh` → two rows name two files, PASS rc 0.
**Repair:** reconcile the two sources — either GENERATE `constants.env` from the plan
allocations (single source of truth) so they cannot diverge, or compare every variable the
prover resolves from `constants.env` against the plan allocation and STOP on any divergence.
Survives the F1 fix, so it must be fixed independently.

### F3 (MEDIUM) — RENDER claims graph closure while silently skipping non-shell members
Non-shell members must STOP graph derivation at RENDER exactly as they already do at FREEZE.

### N1, N2 (nits) — driven-vs-undriven arm counts stated; relabel the `73e92844` run as
pre-feature schema rejection.

## Deliverables

Repaired `composite_pathproof.py` + NEW RED fixtures for F1 (a directory-divergent operand
whose target is non-member bytes) and F2 (an allocation/constants divergence) — both currently
`PASS rc=0`, both must become STOP/FAIL nonzero — plus the existing 26 cases still passing
(regression) + `SELF_QA_SEC102_R3.md` (literal commands + rc + output, RED-before-GREEN per
D026; the reproduction harness must be cwd-robust — your N-note said the r2 harness mis-asserts
from the wrong cwd) + `STATUS_SEC102.md` + `SEC102_R3_REPORT_2026-08-11.md`. Re-derive + record
size + SHA-256 for every artifact. Read `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` (all 13).
State the composite's honest residual limitations. No commit — the Lead commits and reproduces
the full matrix + both new RED fixtures verbatim.
