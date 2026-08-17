# KICKOFF — Claude flagship T1 audit: SEC102 composite pathproof round 2

You are `claude-opus-5` xhigh via the Max account, AUDITOR — the independent flagship for this
artifact. Codex `gpt-5.6-sol` IMPLEMENTED SEC102 (rounds 1 and 2), so you are the genuine
cross-model check. Fresh session. Read-only: edit nothing, no git mutation, no host, no
network, no commit. Prove you changed nothing: `git status --porcelain` clean at the end.
T1 surface; the diff exceeds 300 lines so this flagship audit + a GLM second opinion are the
required gate.

## Bytes under audit — commit `437593c5`

`composite_pathproof.py` 84950 B (was 29640 at round 1). `SELF_QA_SEC102_R2.md`,
`STATUS_SEC102.md`, `SEC102_R2_REPORT_2026-08-11.md`, `sec102_r2_fixtures/`. It consumes (does
not modify) the repaired `pathscope_prover.py` (122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`).

## Design + round-1 context

`SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md` — one entrypoint-driven whole-program proof per
stage, allocate → render → freeze order. Round 1 built allocate; round 2 adds render + freeze
+ the real prover integration.

## What round 2 claims

Render and freeze stages end-to-end; the prover stub replaced by a real adapter consuming the
repaired prover's NEW grammar (seven counts + `kind=`, `ALLOW-LEXICAL`, coverage records); a
prover `STOP`/coverage-record/`REJECT`/forbidden operand maps to composite STOP/FAIL (never a
silent composite PASS); the prover's residual R1 (symlink/mount not established) carried as an
explicit composite-level residual. The Lead ran the published 26-case matrix VERBATIM (7
allocate + 8 render + 11 freeze, RED-before-GREEN): 26/26 PASS.

## Audit contract

1. Re-run the published matrix (`SELF_QA_SEC102_R2.md` "How to reproduce") yourself; confirm
   26/26 and RED-before-GREEN (D026). A canonical auditor that cannot execute returns
   supplemental — so actually run it.
2. **Adversarial:** try to make the composite emit `PASS rc=0` while a stage member reaches a
   filesystem/network primitive that should be caught — e.g. a render source assembled so the
   prover is invoked on the wrong bytes, a freeze member whose declared identity is not the
   analyzed one, a prover coverage/residual signal the adapter drops, a non-shell member the
   analyzer skips silently. Any silent composite PASS over a real sink is CRITICAL.
3. Verify the prover-adapter mapping is faithful: does every prover STOP/REJECT/coverage/
   forbidden/residual actually propagate to a composite non-PASS? Read the adapter and test a
   fixture that exercises each branch.
4. Verify the "inability to evaluate STOPs, never PASS/FAIL" rule (pattern 1) holds at each new
   stage, and that every input member gets a disposition (pattern 13).
5. Judge whether the carried residual R1 and the documented Python/execute-source, launch/
   bootstrap, and runtime-family limitations are honestly stated as limitations (a disclosure
   is not a control — but an explicitly-scoped weaker claim is acceptable for this stage).
6. 13 defect patterns (`../DESIGN_DEFECT_PATTERNS_2026-08-10.md`). Verdict: PASS /
   PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `SEC102_CLAUDE_T1_AUDIT_R2_2026-08-11.md`. If you cannot execute, mark the
run steps and return supplemental — do not print PASS on a read.
