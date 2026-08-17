# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 8 (evidence-harness fix)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r8; independent
cross-model check. Fresh session, read-only: edit nothing except your verdict file, no git
mutation, no host, no network. T1. Prove `git status --porcelain` clean at the end.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only summary/`CASES=`/`FAILED_COUNT=`/
`RC_LEVEL_NEW_REDS=`/`OFF_EXPECTATION=`/`ROLE=`/`child_rc` lines. Refer to fixtures by class name;
never reproduce a sensitive body. Do NOT author new attack fixtures. Verdict first.

## Bytes — commit `3f2c22ca`. `composite_pathproof.py` UNTOUCHED (r8 is harness-only — confirm
its worktree diff is empty vs the r7 commit). NEW `SELF_QA_SEC102_R8.md`, `SEC102_R8_REPORT`.
`STATUS_SEC102.md` updated. This is the LAST finding before SEC102's Codex flagship slot closes.

## Your r7 finding (HIGH, Pattern 6/10)
The §13 paste-run evidence wrapper read each extracted block's stdout but never its child process
status or stderr — a child could emit the expected subset then fail, or emit an unadjudicated
stderr diagnostic, while the wrapper reported "reproduced."

## Round-8 disposition (Lead confirmed composite untouched + matrix 58/58 verbatim)
1. §13 wrapper now requires each extracted child to return process status 0 AND stderr empty
   (strongest form: no published block writes stderr) before its stdout counts as reproduced;
   its own exit tracks that, not just the mismatch counter.
2. D026: 4 synthetic children (emit summary then fail / then write stderr) are ACCEPTED by the r7
   wrapper and REJECTED by the r8 wrapper — RED-before-GREEN at the rc level
   (`CASES=6 RC_LEVEL_NEW_REDS=4 OFF_EXPECTATION=0`); 2 well-behaved controls stay GREEN.
3. §13c re-runs all eleven published evidence blocks + the outer wrapper and records real per-block
   rc + stderr. Max honestly recorded that the D026 reason detector first mis-scored a control
   because a substring test matched `MISMATCH` inside `MISMATCHED=0`; it is word-bounded now.

## Audit contract
1. Confirm `composite_pathproof.py` is byte-identical to the r7 commit (harness-only round) and
   re-run the 58-case matrix VERBATIM → confirm no regression.
2. Run the §13 evidence-harness D026 VERBATIM: confirm the 4 child-failure/stderr children are RED
   under the r7 wrapper and GREEN (rejected) under the r8 wrapper, and the 2 controls stay GREEN.
   Confirm the word-bounded reason detector no longer mis-scores `MISMATCHED=0`.
3. Confirm §13c records real child rc + stderr for all eleven blocks and that the wrapper now fails
   if any child returns nonzero or writes unadjudicated stderr.
4. Any residual: does the wrapper still have a path where a child's incomplete execution is scored
   as reproduced? Judge whether "no block writes stderr" is a sound, enforced contract.
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. **If PASS/PASS-WITH-NITS,
   state that this closes the SEC102 Codex flagship slot** — both original CRITICALs, R3-F2/F3, the
   command-word whitelist fixpoint, and now the evidence harness are all closed; the sole remaining
   item is the disclosed interpreter-vocabulary production-gate decision, and the T1 gate then needs
   only the GLM-5.2 second opinion (which the Lead will dispatch, GLM window open).

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R8_2026-08-12.md`.
