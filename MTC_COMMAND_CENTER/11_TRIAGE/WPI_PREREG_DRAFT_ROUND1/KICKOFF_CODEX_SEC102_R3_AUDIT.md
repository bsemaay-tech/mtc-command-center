# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 3 (OUTPUT-HYGIENE)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR. You authored rounds 1–2; Claude/Max
implemented round 3 (fixing the 2 CRITICALs Claude's r2 audit found), so you are the
independent cross-model check on r3. Fresh session, read-only: edit nothing except your verdict
file, no git mutation, no host, no network. T1 surface; prove `git status --porcelain` clean at
the end.

## OUTPUT-HYGIENE (SEC102 fixtures are attack-shaped: an `evil/library.sh` does
`cat /etc/shadow` + a curl exfil). Redirect fixture output to files; in your own output quote
only `COMPOSITE_PATHPROOF verdict=`, `CLAIM id=... verdict=`, `CASES=`, `FAILED_COUNT=`,
`DERIVED_EDGE ... disposition=`, `FREEZE_INPUT ... disposition=`, `RESIDUAL ...` lines. Refer to
the evil fixture by name (`evil-divergent-operand`), never reproduce its body or the
forbidden-path/exfil literals. Do NOT author new attack fixtures; run the published ones.
Verdict first.

## Bytes — commit `35860a0a`
`composite_pathproof.py` 96825 B (was 84950 at r2). `SELF_QA_SEC102_R3.md`, `STATUS_SEC102.md`,
`SEC102_R3_REPORT_2026-08-11.md`, `sec102_r3_fixtures/`, `sec102_r2_fixtures/` (two fixtures
repointed; two that were byte-identical at r2 are now distinct).

## Claude's r2 BLOCK (what r3 had to fix)
`SEC102_CLAUDE_T1_AUDIT_R2_2026-08-11.md` — F1 CRITICAL: operand↔member bound by basename, so a
deployed path pointing at non-member bytes was never analyzed (silent PASS over a real sink).
F2 CRITICAL: plan allocations and `constants.env` were two unreconciled sources for the same
variable. F3 MEDIUM: RENDER skipped non-shell members.

## Round-3 dispositions (Lead reran verbatim)
- Matrix `CASES=37 FAILED_COUNT=0` (26 r2 + 11 new).
- F1 fixed: exact `deploy_path` member matching, basename fallback deleted; the evil divergent
  operand now `verdict=STOP reason=source_operand_deploy_identity_unbound` (`CLAIM id="F9"`),
  python rc 3 — was silent PASS at r2.
- F2 fixed: allocation↔constants reconciliation; divergence → `CLAIM id="F10"
  reason=allocation_constants_value_divergence`, rc 3.
- F3 fixed: non-shell members STOP at RENDER. 3 mutation discriminators (restore basename
  fallback / disable the two comparisons / revert non-shell STOP) each turn a RED back to PASS.
- Honest residual disclosed on every FREEZE report: deployed identity is a declared, lexically
  compared string, NOT host-object verification — a plan declaring `deploy_path` falsely is not
  detected at this stage.

## Audit contract
1. Re-run the published matrix + the F1/F2 RED fixtures VERBATIM (output to files); confirm
   37/37 and that the evil divergent operand and the allocation/constants divergence both reach
   rc 3 (STOP), not PASS. Non-execution ≠ acceptance (D025 r1); RED-before-GREEN (D026).
2. **Adversarial (describe by mechanism, do not author attack shell):** can you still get a
   composite `PASS rc=0` while a member's ANALYZED bytes differ from its EXECUTED bytes, or
   while a variable the prover resolves differs from the plan allocation? Try: a `deploy_path`
   that is a symlink/alias to a member, a second variable not covered by the reconciliation, a
   render/freeze member the graph derivation skips. Any silent composite PASS over a real sink
   is CRITICAL and re-opens F1/F2.
3. Judge the honest residual: is "declared lexical deploy identity, not host-object verified"
   an acceptable explicitly-scoped limit for this stage, or does it leave a reachable false-PASS
   the design claims to close? (A disclosure is not a control — but an honestly-scoped weaker
   claim is acceptable where the composite cannot reach the host.)
4. Note (not necessarily your finding to fix): the r3 report flags a `.gitattributes`
   `text=auto` + `autocrlf` durability risk — a fresh Windows checkout would materialise CRLF
   and break FREEZE identity pins. Confirm whether it applies and how severe.
5. 13 defect patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R3_2026-08-11.md`.
