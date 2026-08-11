# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 5 (OUTPUT-HYGIENE)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r5 (closing your reopened
R3-F1 command-position CRITICAL); you are the independent cross-model check. Fresh session,
read-only: edit nothing except your verdict file, no git mutation, no host, no network. T1.
Prove `git status --porcelain` clean at the end.

## OUTPUT-HYGIENE (fixtures include an attack-shaped evil member + prefix-hidden source operands).
Redirect fixture output to files; quote only `COMPOSITE_PATHPROOF verdict=`, `CLAIM id=...
verdict=`, `CASES=`, `FAILED_COUNT=`, `OFF_EXPECTATION=`, `RESIDUAL ...` lines. Refer to prefix
forms by class name (named-fd, indexed-assign, unmodeled-prefix); never reproduce the shell body
or forbidden-path/exfil literals. Do NOT author new attack fixtures. Verdict first.

## Bytes — commit `7da76479`. `composite_pathproof.py`. NEW `sec102_r5_fixtures/` (12).
`.gitattributes` (r5 fixtures added). `SELF_QA_SEC102_R5.md`, `STATUS_SEC102.md`,
`SEC102_R5_REPORT_2026-08-11.md`. R3-F2/F3 and both original CRITICALs stay closed.

## Your r4 finding (REQUEST_CHANGES, CRITICAL — R3-F1 reopened)
`_shell_words:1279` preserved command position ONLY for numeric fd prefixes; a named-fd
redirection prefix or an indexed-assignment prefix was emitted as a leaf, closing command
position before a following `source`/interpreter operand that was then never scanned → silent
no-edge → composite could PASS over an unanalyzed program.

## Round-5 dispositions (Lead reran verbatim)
- Matrix `CASES=44 FAILED_COUNT=0` (40 carried + 4 new).
- `_shell_words` now conserves command position across every assignment/redirection prefix
  (numeric+named fd, scalar+indexed assignment) and STOPs on any unmodeled prefix instead of
  leafing it. The 3 new REDs (named-fd-source, indexed-assign-source, unmodeled-prefix) each now
  `verdict=STOP rc=3` — was silent PASS at `bb02c25a`.
- 20-cell mutation matrix `OFF_EXPECTATION=0` (M1 numeric-only kills only named-fd RED; M4 only
  the function-body; M3 only unmodeled; M2 restores r4 handling, kills two, stated not hidden;
  M5 model⊥fence). Prefix battery 16/16 blind forms killed, 9/9 controls PASS both sides, 1
  disclosed conservative false stop; r4 battery re-run 32/32 + 5/5.
- Max built a cwd-EXTERNAL paste-and-run harness over the self-QA; its first run failed 12/12
  and exposed 5 real overclaims in the evidence doc (incl. a published "real output" blob hash
  not obtained by running) — all fixed, failure recorded in §12, final `MATCHED=12 DIFFERED=0`.
- Disclosed residuals (STATUS 24–27): detection VOCABULARY is still a list (the interpreter-
  vocabulary half of R3-F1, untouched this round — an interpreter name not in the recognized set
  derives no edge); the prefix-completeness claim is a reading of the Bash grammar, not a proof;
  ran under Python 3.14.2.

## Audit contract
1. Re-run the matrix + the 3 new prefix RED fixtures VERBATIM (output to files); confirm 44/44
   and all three reach STOP with command position conserved (not a downstream check doing it).
2. **Adversarial (describe by mechanism, no attack shell):** any OTHER prefix or command-position
   form (e.g. a further redirection operator, a compound-assignment, a coproc/time/`!` prefix, a
   here-string) that still leaves a following source/interpreter operand unscanned while the
   composite PASSes? Any silent composite PASS over a real sink re-opens CRITICAL.
3. Judge the disclosed interpreter-vocabulary residual: is "recognized interpreter set + disclosed
   list-completeness limit" an acceptable explicitly-scoped limit for this stage, or does the
   design claim closure it does not deliver? (A disclosure is not a control — but an honestly
   scoped weaker claim can be acceptable where a static tool cannot enumerate every interpreter.)
4. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If PASS, note the T1
   gate still needs the GLM-5.2 second opinion (>300 lines; GLM ~05:28).

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`.
