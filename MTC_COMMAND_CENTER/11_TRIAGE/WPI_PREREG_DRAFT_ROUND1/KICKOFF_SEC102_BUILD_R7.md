# KICKOFF — SEC102 composite pathproof round 7: WHITELIST-inversion of the static-literal test (the true fixpoint)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER (you built r3–r6). Codex audits
r7. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence:
`composite_pathproof.py`, `sec102_r7_fixtures/`, `SELF_QA_SEC102_R7.md`, `STATUS_SEC102.md`, the
round-7 report, scoped `.gitattributes` (add r7 fixtures). Do NOT touch `pathscope_prover.py`,
block files, RP6/RP7, prereg drafts. Concurrent Max lane owns `SELF_QA_RP6.md`/`STATUS_RP6_P0.md`
— do NOT touch. Never git checkout/reset/stash any tracked file.

## Input — commit `90868b86`. Codex r6 audit ACCEPTED the interpreter-vocabulary residual and
the conservative false-stops. Everything except one admission-policy gap is settled — do NOT
regress any of it.

## The finding + WHY r7 must invert the test
`SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`: the r6 "is this command word dynamic?" test is a
BLACKLIST of expansion metacharacters, and it missed the extglob operator family — one-or-more
`+(...)`, exactly-one/zero-or-one `?(...)`/`@(...)`, and negated `!(...)`. With `extglob`
enabled these pathname-resolve to a recognized interpreter/source and hide the operand — a
genuinely new admission gap. Blacklisting operators is INHERENTLY incomplete (extglob, and any
future/rarely-used operator, is missed). Closing only the three named classes invites an
eighth.

## Required repair — the fixpoint (invert to a WHITELIST)
Replace the "reject a command word that CONTAINS a known expansion metacharacter" test with:
a command word is admissible as a PROVEN-STATIC benign leaf ONLY when EVERY character of the
raw (pre-expansion) word token is in an explicit SAFE set — e.g. `[A-Za-z0-9._/+=:@%-]` plus a
justified, enumerated allow-list of any other char you can PROVE cannot introduce pathname
expansion, parameter/command/arithmetic expansion, process substitution, tilde, brace, extglob,
or quote-removal-driven resolution. ANY character NOT in that safe set makes the word NOT
proven-static → UNMODELED → the stage STOPs (rc 3). This closes the extglob family AND every
other operator (known or not) in one rule, because the default for an unrecognized character is
STOP, not admit. A recognized-interpreter command word still derives its edge; a genuinely
static non-interpreter literal (only safe chars) stays a benign leaf so the carried GREENs pass.
State the safe set explicitly and justify each member cannot introduce dynamic resolution.

## Deliverables
Repaired `composite_pathproof.py` + NEW RED fixtures for the three extglob classes (`+(`, `?(`
/`@(`, `!(`) hiding an interpreter operand — each currently (`90868b86`) admitted as benign leaf
→ PASS, each must become STOP — plus at least one "novel operator" RED (a valid but unusual
expansion char the old blacklist would miss) proving the whitelist catches the unenumerated case.
Independent D026 mutations (restore the blacklist → the REDs return to PASS). ALL carried cases
still passing (a safe-char static literal must remain a benign leaf) + `SELF_QA_SEC102_R7.md`
(literal commands + rc + output, RED-before-GREEN, cwd-robust external paste-run harness) +
`STATUS_SEC102.md` (narrow the command-word closure claim to exactly the whitelist property;
keep the interpreter-vocabulary residual disclosed as the production-gate item) +
`SEC102_R7_REPORT_2026-08-11.md`. Re-derive + record size + SHA-256. No commit — the Lead
commits and reproduces the matrix + new REDs verbatim.
