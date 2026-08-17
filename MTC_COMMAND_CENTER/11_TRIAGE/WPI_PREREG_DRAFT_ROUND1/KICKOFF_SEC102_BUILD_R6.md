# KICKOFF — SEC102 composite pathproof round 6: COMPREHENSIVE fail-closed command-word policy

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER (you built r3–r5). Codex audits
r6. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence:
`composite_pathproof.py`, `sec102_r6_fixtures/`, `SELF_QA_SEC102_R6.md`, `STATUS_SEC102.md`,
the round-6 report, and the scoped `.gitattributes` (add r6 fixtures). Do NOT touch
`pathscope_prover.py`, block files, RP6/RP7, prereg drafts. A concurrent Max lane owns
`SELF_QA_RP6.md`/`STATUS_RP6_P0.md` — do NOT touch. Never git checkout/reset/stash any tracked
file.

## Input — commit `e3906cec`. All prior CRITICALs closed EXCEPT the command-word coverage,
which keeps reopening one class at a time (r4 numeric-fd, r5 named-fd/indexed-assign, and now
r5-audit found a pathname-expanded/glob command word leafed while it can resolve to an
interpreter). Both original CRITICALs, R3-F2, R3-F3 stay closed — do NOT regress them.

## The finding (Codex r5) and WHY r6 must be comprehensive
`SEC102_CODEX_T1_AUDIT_R5_2026-08-11.md`: a pathname-expanded command word is classified as a
benign leaf even when Bash can resolve it to a recognized interpreter; the following script
operand is then outside both direct matchers and the word-conservation check — a silent no-edge
CRITICAL. This is the FOURTH command-word form found across r4→r5-audit. Closing it in isolation
invites a fifth. STOP the one-class-at-a-time regress by making the command-word policy
FAIL-CLOSED comprehensively.

## Required repair — the fixpoint
Replace the "classify command word, leaf if not a recognized interpreter/source" logic with a
CLOSED admissibility policy: a command word (in every command position the scanner reaches —
after prefix/redirection/assignment stripping, inside `$( )`, in `-c`/`-exec`/xargs strings if
modeled) is ADMISSIBLE as a benign non-edge leaf ONLY when it is a PROVEN-STATIC literal that is
NOT a recognized interpreter/source — i.e. a single unquoted/quoted word with no pathname-
expansion metacharacter (`* ? [ ] { }` glob, brace), no parameter/command/arithmetic expansion,
no process substitution, no tilde, no backslash-constructed name, no here-string-fed target.
EVERY command word that is dynamic, expandable, substituted, or otherwise not a proven-static
benign literal is UNMODELED → the stage STOPs (rc 3), never a silent leaf. A command word that
IS a recognized interpreter/source still derives its edge as today. Conversely, a static literal
that is not an interpreter stays a benign leaf so the 44 carried GREENs keep passing.

This is the SAME fail-closed principle already applied to prefixes — extended to the command
word itself, so no unmodeled command-word form can silently disappear.

## Deliverables
Repaired `composite_pathproof.py` + NEW RED fixtures for at least: pathname-expanded/glob command
word, parameter-expansion command word, command-substitution command word, tilde command word —
each currently (`e3906cec`) leafing a hidden interpreter/source operand into a PASS, each must
become STOP after the repair. Independent D026 mutations. ALL carried cases still passing (the
44 GREENs must hold — a static non-interpreter literal must remain a benign leaf) +
`SELF_QA_SEC102_R6.md` (literal commands + rc + output, RED-before-GREEN, cwd-robust external
paste-run harness like r5; add r6 fixtures to `.gitattributes`) + `STATUS_SEC102.md` +
`SEC102_R6_REPORT_2026-08-11.md`. State the honest residual: after this, the command-word policy
is fail-closed; the remaining disclosed limit is the interpreter-VOCABULARY list (a recognized
interpreter set, not a proof that the list is exhaustive) — do NOT claim to close that here; keep
it disclosed. Re-derive + record size + SHA-256 for every artifact. No commit — the Lead commits
and reproduces the matrix + new REDs verbatim.
