# KICKOFF — SEC102 composite pathproof round 5: command-position conservation (Codex r4 CRITICAL)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER (you built r3/r4). Codex audits
r5. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence:
touch ONLY `composite_pathproof.py`, `sec102_r4_fixtures/` (+ new fixtures or a `sec102_r5_
fixtures/`), `SELF_QA_SEC102_R5.md`, `STATUS_SEC102.md`, the round-5 report, and the scoped
`.gitattributes` (add any r5 fixtures dir to it). Do NOT touch `pathscope_prover.py`, block
files, RP6/RP7, prereg drafts. A concurrent Max lane owns `SELF_QA_RP6.md`/`STATUS_RP6_P0.md`
— do NOT touch those; never git checkout/reset/stash any tracked file.

## Input — commit `bb02c25a`. R3-F2 and R3-F3 are CLOSED (Codex-verified) — do NOT regress them.

## The single CRITICAL to close (Codex r4)
`composite_pathproof.py:1279` `_shell_words` preserves command position ONLY for numeric
file-descriptor prefixes. Consequence:
- a valid Bash NAMED-file-descriptor redirection prefix (e.g. `{name}>...`) is emitted as a
  leaf word, and line ~1286 closes command position before the redirection and the following
  command;
- `SHELL_ASSIGNMENT_RE` (~:1294) accepts only SCALAR assignment words, so a valid INDEXED
  assignment prefix (e.g. `arr[0]=...`) is also classified as a leaf and closes command
  position.
In both cases the direct source/interpreter regexes do not match through the prefix, and
`_graph_word_conservation` sees no uncovered graph word — so a `source`/interpreter operand
after such a prefix produces NO edge and the composite can PASS over an unanalyzed program.
The missed command word is ALREADY in the declared detection vocabulary; the scanner loses its
command position before classification (Pattern 12 primary; Pattern 5 grammar incompleteness;
Pattern 9 claim overreach). Codex reproduced both via scanner-boundary probes on the committed
module.

**Repair (fail-closed principle):** make command-position conservation complete for EVERY
accepted Bash assignment and redirection prefix — numeric AND named file descriptors, scalar
AND indexed (and any other valid) assignment forms — so command position is preserved through
them and the following command word is classified. For any prefix form the scanner cannot fully
model, STOP (unmodeled-prefix) BEFORE classifying it as a benign leaf — never silently close
command position. This is the same fail-closed rule the FREEZE stage already applies elsewhere.

## Deliverables
Repaired `composite_pathproof.py` + NEW RED fixtures: one named-fd-prefix and one
indexed-assignment-prefix composite that currently (`bb02c25a`) PASS while hiding a
source/interpreter operand, and must become STOP after the repair; plus an unmodeled-prefix
fixture that must STOP. Independent D026 mutations for BOTH mechanisms (restore the numeric-only
handling → the RED returns to PASS). All 40 carried cases still passing (no fence weakened) +
`SELF_QA_SEC102_R5.md` (literal commands + rc + output, RED-before-GREEN, cwd-robust; add r5
fixtures to `.gitattributes`) + `STATUS_SEC102.md` + `SEC102_R5_REPORT_2026-08-11.md`. Re-derive
+ record size + SHA-256 for every artifact. Read `../DESIGN_DEFECT_PATTERNS_2026-08-10.md`. State
the honest residual scope. No commit — the Lead commits and reproduces the matrix + new REDs
verbatim.
