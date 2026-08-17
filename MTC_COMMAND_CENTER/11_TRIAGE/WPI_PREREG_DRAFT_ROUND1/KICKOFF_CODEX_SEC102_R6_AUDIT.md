# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 6 (OUTPUT-HYGIENE)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r6; you are the
independent cross-model check. Fresh session, read-only: edit nothing except your verdict file,
no git mutation, no host, no network. T1. Prove `git status --porcelain` clean at the end.

## OUTPUT-HYGIENE. Redirect fixture output to files; quote only `COMPOSITE_PATHPROOF verdict=`,
`CLAIM id=... verdict=`, `CASES=`, `FAILED_COUNT=`, `RESIDUAL ...` lines. Refer to command-word
forms by class (glob, param-expansion, command-substitution, tilde, unmodeled); never reproduce
the shell body or forbidden-path/exfil literals. Do NOT author new attack fixtures. Verdict first.

## Bytes — commit `c5e443b2`. `composite_pathproof.py` (121837 B). NEW `sec102_r6_fixtures/`
(24). `.gitattributes` (r6 fixtures added). `SELF_QA_SEC102_R6.md`, `STATUS_SEC102.md`,
`SEC102_R6_REPORT_2026-08-11.md`. All prior CRITICALs + R3-F2/F3 stay closed.

## Your r5 finding (the LAST command-word class found one-at-a-time)
A pathname-expanded (glob) command word was leafed while it can resolve to a recognized
interpreter → following operand unscanned → silent no-edge. r4→r5 audits found four such
command-word classes in sequence.

## Round-6 disposition — the comprehensive fixpoint (Lead reran verbatim)
The command-word policy is now CLOSED: a command word is admissible as a benign non-edge leaf
ONLY when it is a PROVEN-STATIC literal that is not a recognized interpreter/source — no
pathname-expansion metachar, no parameter/command/arithmetic expansion, no process substitution,
no tilde, no backslash-constructed name. EVERY dynamic/expandable/substituted form is
UNMODELED → STOP rc 3. Matrix `CASES=52 FAILED_COUNT=0`; the 4 new REDs (glob, param,
substitution, tilde command words) each `verdict=STOP rc=3`. Conservative false-stops grew and
are disclosed (`[ -f x ]`, `\cat`, `~/bin/mytool`, and one r5 control now STOP). Max's cwd-
external paste-run harness self-caught 2 hand-transcribed evidence lines; corrected, recorded.
Disclosed residual (STATUS): the recognized-interpreter VOCABULARY is a list — r6 closed HOW a
command word is admitted, not WHICH interpreter names are recognized; this remains the stated
production blocker and is NOT claimed closed.

## Audit contract
1. Re-run the matrix + the 4 new command-word REDs VERBATIM (output to files); confirm 52/52 and
   each new RED STOPs. Confirm the 48 carried GREENs still pass (a static non-interpreter literal
   must remain a benign leaf — the policy must not over-STOP a genuinely benign static command).
2. **The decisive test:** is the command-word admission policy now genuinely CLOSED — is there
   ANY command-word form (in any command position the scanner reaches) that is neither a
   proven-static literal nor caught as UNMODELED, and that could resolve to an interpreter/source
   hiding an operand? Describe any by class in words; do not author shell. If none, the
   one-class-at-a-time regress is over. If one exists, it re-opens CRITICAL — but say whether it
   is a genuinely new admission gap or merely another interpreter NAME (the latter is the
   disclosed vocabulary residual, NOT an admission-policy defect).
3. Judge the disclosed vocabulary residual: acceptable explicitly-scoped limit for this stage
   (the composite recognizes a declared interpreter set; the production gate pins/decides the
   vocabulary), or a design overclaim? Also judge whether the grown false-stops are acceptably
   conservative (fail-closed) rather than a correctness regression on benign programs.
4. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If PASS or
   PASS-WITH-NITS, note the T1 gate still needs the GLM-5.2 second opinion (>300 lines; GLM
   ~05:28) and that the vocabulary residual is a separate, disclosed production-gate item.

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`.
