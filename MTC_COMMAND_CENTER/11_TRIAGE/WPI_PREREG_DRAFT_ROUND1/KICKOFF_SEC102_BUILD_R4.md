# KICKOFF — SEC102 composite pathproof round 4: three MEDIUM findings (Codex r3 audit)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER (you built r3). Codex audits r4.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch
ONLY `composite_pathproof.py`, `sec102_r3_fixtures/` (+ new fixtures), `SELF_QA_SEC102_R4.md`,
`STATUS_SEC102.md`, the round-4 report, AND — for R3-F3 only — a `.gitattributes` entry SCOPED
to the SEC102 fixture paths (see below). Do NOT touch `pathscope_prover.py`, the block files,
RP6/RP7, or the prereg drafts. A concurrent Max lane owns `SELF_QA_RP6.md`/`STATUS_RP6_P0.md` —
do NOT touch those; never git checkout/reset/stash any tracked file.

## Input — commit `10659bd5`

`composite_pathproof.py` 96825 B. Both r2 CRITICALs are CONFIRMED CLOSED by Codex's r3 audit
(`SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`) — do NOT touch the deploy-identity binding or the F2
reconciliation core; only extend as the findings require. Its "Required repair" text per
finding BINDS.

### R3-F1 (MEDIUM) — RENDER coverage shares the graph detector's blind spot
The RENDER coverage check has the same blind spot as the graph detector it depends on.
**Repair:** close the RENDER coverage gap so a member the graph detector misses is not silently
covered; add a D026 RED (a render member in the blind spot) that currently passes and must STOP.

### R3-F2 (MEDIUM) — F10 passes without a terminal disposition for every plan allocation
F10 reports PASS before every plan allocation has a constants-side entry: a plan allocation
ABSENT from the constants table produces no F10 failure (the composite still STOPs via F5/F6,
but F10's own PASS sentence is false — Pattern 9).
**Repair (pick one, justify):** (1) give every plan allocation a terminal F10 disposition and
make F10 STOP when an allocation that can affect prover semantics is absent from constants; OR
(2) if constants-only runtime values are intentionally allowed, narrow the F10 claim to exactly
that. Add a D026 test whose discriminator asserts **F10 itself** flips PASS→STOP (a downstream
F5/F6 STOP is supplemental and does NOT close this claim defect).

### R3-F3 (MEDIUM) — clean Windows checkout changes pinned fixture bytes (evidence durability)
Repo `.gitattributes` is `* text=auto` and this clone has `core.autocrlf=true`, so a fresh
Windows checkout materializes CRLF and the committed LF pins no longer match — the FREEZE matrix
cannot reproduce (Pattern 10, since the harness is claimed as literal paste-and-run evidence).
**Repair:** add a `.gitattributes` that forces the SEC102 fixture files to preserve bytes
exactly — e.g. in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes`:
`sec102_r1_fixtures/** -text`, `sec102_r2_fixtures/** -text`, `sec102_r3_fixtures/** -text`
(and any r4 fixtures dir) so those blobs are treated as binary (no EOL conversion). Then
DEMONSTRATE the matrix reproduces from a fresh checkout WITH `core.autocrlf=true` active (e.g.
check the fixtures out into a temp worktree with autocrlf on and re-derive the pinned SHA-256s +
run the matrix). Do NOT change global line-ending behavior or touch files outside the SEC102
fixture scope. Do NOT merely document a local prerequisite — the attribute must make it durable.

## Deliverables

Updated `composite_pathproof.py` + the scoped `.gitattributes` + new RED fixtures for R3-F1 and
R3-F2 (each currently PASS, must STOP; R3-F2's discriminator must flip F10 itself) + the fresh-
checkout durability demonstration for R3-F3 + all 37 prior cases still passing (regression) +
`SELF_QA_SEC102_R4.md` (literal commands + rc + output, RED-before-GREEN, cwd-robust) +
`STATUS_SEC102.md` + `SEC102_R4_REPORT_2026-08-11.md`. Re-derive + record size + SHA-256 for
every artifact. Read `../DESIGN_DEFECT_PATTERNS_2026-08-10.md`. No commit — the Lead commits and
reproduces the matrix + new REDs + the durability demo verbatim.
