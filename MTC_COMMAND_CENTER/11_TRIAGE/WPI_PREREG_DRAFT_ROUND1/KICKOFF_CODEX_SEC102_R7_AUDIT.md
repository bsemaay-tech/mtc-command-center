# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 7 (OUTPUT-HYGIENE)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r7; you are the
independent cross-model check. Fresh session, read-only: edit nothing except your verdict file,
no git mutation, no host, no network. T1. Prove `git status --porcelain` clean at the end.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only `COMPOSITE_PATHPROOF verdict=`,
`CLAIM id=... verdict=`, `CASES=`, `FAILED_COUNT=`, `RESIDUAL ...` lines. Refer to command-word
forms by class (extglob-plus/qmark/at/bang, novel-operator, safe-static); never reproduce the
shell body or forbidden-path/exfil literals. Do NOT author new attack fixtures. Verdict first.

## Bytes — commit `df983737`. `composite_pathproof.py`. NEW `sec102_r7_fixtures/` (18).
`.gitattributes` (r7 fixtures added). `SELF_QA_SEC102_R7.md`, `STATUS_SEC102.md`,
`SEC102_R7_REPORT_2026-08-11.md`. All prior CRITICALs + R3-F2/F3 stay closed.

## Your r6 finding (the last blacklist gap)
The r6 expansion-metachar BLACKLIST missed the extglob operator family — closing operators one
at a time is inherently incomplete.

## Round-7 disposition — the WHITELIST fixpoint (Lead reran verbatim)
The static-literal test is INVERTED: a command word is admissible as a benign leaf ONLY when
EVERY character of the raw word is in an explicit proven-safe set; ANY other character →
UNMODELED → STOP rc 3. This closes the extglob family AND every other operator, known or future,
in one rule. Matrix `CASES=58 FAILED_COUNT=0`. The 4 new extglob REDs (`+(`, `?(`, `@(`, `!(`
at command position) and a NOVEL-operator RED (an unusual expansion char the old blacklist would
have missed) each `verdict=STOP rc=3` — the novel case proves the whitelist catches the
unenumerated operator. M1 discriminator: restoring the r6 blacklist returns exactly the 4 new
REDs to PASS. Max disclosed honestly: `?(` was already caught in r6 (4 real rc-level new REDs,
not 5), and corrected r6's false "extglob covered by construction" residual claim in STATUS.
Round-7 conservative false-stops are LARGER and DECLARED (`g++`, `tool@1.0`, `--opt=value`,
`"bash"`, `2a=b`, non-ASCII names, non-NAME funcdefs now STOP — the fail-closed cost of excluding
`+`/`@`/etc. from the safe set). Disclosed residual: interpreter VOCABULARY (production-gate item).

## Audit contract
1. Re-run the matrix + the 4 extglob REDs + the novel-operator RED VERBATIM (output to files);
   confirm 58/58 and every one STOPs. Confirm the carried GREENs (a safe-static non-interpreter
   literal) still pass — the whitelist must not over-STOP a genuinely safe static command.
2. **The decisive test — is this the fixpoint?** Construct-by-mechanism (no attack shell): is
   there ANY command word that reaches a sink-bearing operand while being admitted as a benign
   leaf — i.e. any character/form the safe-set test wrongly treats as static? Try a character IN
   the declared safe set that can nonetheless introduce dynamic resolution (that would be a
   safe-set membership error, a real finding), or a command position the scanner never reaches.
   If the safe set is genuinely closed (every dynamic/expansion/resolution path requires a
   non-safe character) and reaches every command position, the one-class regress is OVER.
3. Judge the safe set itself: is every member justified as unable to introduce pathname/parameter/
   command/arithmetic expansion, process substitution, tilde, brace, extglob, or quote-driven
   resolution? A wrongly-included member is a finding; the grown false-stops are acceptable
   fail-closed behavior if the safe set is sound.
4. Judge the disclosed interpreter-vocabulary residual (recognized-name set = production-gate
   decision, not a static-tool defect at this stage).
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If PASS/PASS-WITH-NITS,
   note the command-word policy is a fixpoint and the T1 gate still needs the GLM-5.2 second
   opinion (>300 lines; GLM ~05:28).

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md`.
