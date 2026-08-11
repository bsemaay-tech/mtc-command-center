# KICKOFF — SEC102 composite pathproof round 8: evidence-harness status adjudication (Codex r7, the last finding)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r8. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch ONLY
`SELF_QA_SEC102_R8.md` (new — carry forward the r7 self-QA content and fix the §13 wrapper),
`STATUS_SEC102.md`, the round-8 report, and the scoped `.gitattributes` (add r8 fixtures if any).
You MAY touch `composite_pathproof.py` ONLY if the fix genuinely requires it (it should not —
this is an evidence-harness fix). Do NOT touch `pathscope_prover.py`, block files, RP6/RP7,
prereg drafts. Concurrent Max lane owns `SELF_QA_RP6.md`/`STATUS_RP6_P0.md` — do NOT touch.
Never git checkout/reset/stash any tracked file.

## Context — commit `0e0086c0`
Codex r7 audit CONFIRMED the command-word WHITELIST is a FIXPOINT (the one-class regress is
over) and ACCEPTED the interpreter-vocabulary residual as a disclosed production-gate decision.
Both original CRITICALs, R3-F2/F3, and the command-word policy are all closed. **This is the
last finding before SEC102's Codex flagship slot closes.**

## The single finding (Codex r7 — HIGH, Pattern 6/10)
`SELF_QA_SEC102_R7.md:1616,1622,1626,1632`: the §13 paste-and-run EVIDENCE wrapper reads each
extracted PowerShell block's stdout but NEVER its child process status or stderr. It tests only
whether the published stdout subset is present and bases its own exit solely on the mismatch
counter. So a child can emit the expected subset and THEN fail (nonzero exit), or emit an
unadjudicated stderr diagnostic, while the wrapper reports the block reproduced — output
interpreted before execution completeness is proved.

## Required repair (Codex's spec)
1. Require every extracted child to return process status 0 before its stdout can count as
   reproduced.
2. Require stderr to be empty, OR explicitly adjudicate a documented non-empty-stderr contract
   per block (state which blocks legitimately produce stderr and why).
3. Add D026 RED/GREEN: a harmless deliberate child failure AFTER an expected summary line — RED
   under the current wrapper (it reports reproduced), GREEN after the wrapper rejects it. No
   attack fixture, no sensitive body.
4. Re-run all ten published evidence blocks plus the outer wrapper and record the REAL status
   (child rc + stderr per block).

## Deliverables
`SELF_QA_SEC102_R8.md` (the r7 self-QA carried forward with the §13 wrapper fixed + the new D026
child-failure evidence + the ten-block re-run with real per-block rc/stderr) + `STATUS_SEC102.md`
(note the harness finding closed; keep the interpreter-vocabulary residual disclosed) +
`SEC102_R8_REPORT_2026-08-11.md`. Keep the 58-case matrix and all carried fences passing. If you
touched `composite_pathproof.py`, re-derive its size + SHA-256 and justify why. No commit — the
Lead commits and reproduces the matrix + the new child-failure D026 + the ten-block wrapper
verbatim.
