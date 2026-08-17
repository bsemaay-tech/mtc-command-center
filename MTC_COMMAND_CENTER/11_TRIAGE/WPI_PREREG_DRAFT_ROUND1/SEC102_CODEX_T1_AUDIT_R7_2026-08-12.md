# VERDICT: REQUEST_CHANGES

TIER: T1

APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, `xhigh` per the explicit kickoff;
fresh independent read-only audit. T1 maximum: two rounds.

The round-7 command-word policy itself is a fixpoint for the class under review. The
package is nevertheless non-accepting because its published paste-and-run verifier can
accept a child block without adjudicating that block's process status or stderr.

## Required finding

`SELF_QA_SEC102_R7.md:1616`, `SELF_QA_SEC102_R7.md:1622`,
`SELF_QA_SEC102_R7.md:1626`, `SELF_QA_SEC102_R7.md:1632`: **HIGH — the section-13
evidence wrapper reads stdout but never the child process status or stderr.** It invokes
each extracted PowerShell block with captured output, tests only whether the published
stdout subset is present, and bases its own exit solely on the mismatch counter. A child
can therefore emit the expected subset and then fail, or emit an unadjudicated stderr
diagnostic, while the wrapper reports the block reproduced. This is Design Defect Pattern
6 overlaid by Pattern 10: output is interpreted before execution completeness is proved.

Minimum required repair:

1. Require every extracted child to return process status 0 before its stdout can count as
   reproduced.
2. Require stderr to be empty, or explicitly adjudicate a documented non-empty stderr
   contract per block.
3. Add D026 RED/GREEN evidence using a harmless deliberate child failure after an expected
   summary: RED under the current wrapper, GREEN after the wrapper rejects it. Do not add
   an attack fixture or reproduce any sensitive body.
4. Re-run all ten published blocks plus the outer wrapper and record the real status.

## Command-word fixpoint judgment

The round-7 source repair passes the decisive mechanism review:

- The implemented full-match predicate admits exactly ASCII letters, digits, and the five
  documented ordinary punctuation classes. It admits neither an empty word nor sampled
  non-ASCII words.
- Every admitted character is inert in a raw, unquoted Bash command word. Pathname,
  parameter, command and arithmetic expansion; process substitution; tilde and brace
  expansion; extglob; quote removal; job resolution; and assignment-only expansion each
  require at least one excluded character or are classified before the benign-leaf gate.
- The scanner conserves the ambiguous opening delimiter into every non-NAME raw token.
  The NAME-only function-definition exception cannot contain an extglob operator.
- Every other scanner-reached command-position word becomes unmodeled and reaches terminal
  STOP. No blacklist completeness assumption remains.
- The exhaustive character/position sweep, grammar battery, pre-feature comparison,
  mutation discriminators, carried batteries, and all 58 matrix cases independently
  completed with process status 0 and empty stderr in this audit.

The one-class command-word regress is therefore over. The required finding is in the
evidence wrapper, not in `composite_pathproof.py`.

## Reproduced evidence

The 58-case matrix was run verbatim with fixture output redirected to a temporary file:

```text
CASES=58 FAILED_COUNT=0
```

The matrix independently asserted that all four extglob-class REDs and the novel-operator
RED reached STOP with process status 3, while the safe-static non-interpreter GREEN still
passed. No raw case row, command body, or sensitive literal is reproduced here.

All ten published PowerShell evidence blocks were then extracted byte-for-byte, executed
from outside the repository, and checked independently of section 13. Every child returned
process status 0 and empty stderr. This establishes the current evidence despite the
published outer wrapper's defect; it does not make that reusable verifier correct.

D026 evidence was also reproduced: the pre-feature comparison and the blacklist-restoration
discriminator were RED on the frozen prior behavior and GREEN on round 7. The discriminator
restored the affected extglob class to its defective benign disposition while leaving the
unrelated REDs intact.

## Residual judgments

- **Interpreter vocabulary:** accepted as an honestly disclosed production-gate decision,
  not closed. A safe-static literal naming an executable-capable program outside the
  recognized-name set can still be treated as benign. Round 7 neither worsens nor conceals
  that separate limitation.
- **Conservative false-stops:** accepted fail-closed behavior at this stage. The safe-static
  GREEN proves the policy is not a blanket STOP.
- **Prior findings:** the 58-case matrix and all carried blocks reproduced; no prior
  CRITICAL, R3-F2, or R3-F3 regression was found.

## Thirteen-pattern adjudication

| Pattern | Result |
|---|---|
| 1 — STOP/PASS/FAIL ordering | PASS on the 58-case matrix |
| 2 — Host and namespace identity | PASS within the explicit no-host scope |
| 3 — Host-object, symlink, mount identity | PASS as an explicit non-claim |
| 4 — External interpreter/environment boundary | PASS as a disclosed production blocker |
| 5 — Grammar completeness | PASS for the safe-character command-word fixpoint |
| 6 — Probe status before adjudication | REQUEST_CHANGES: section 13 ignores child status and stderr |
| 7 — Incomplete-reader path | PASS; unchanged |
| 8 — Deployed identity | PASS within lexical scope |
| 9 — Claim wording vs predicate | PASS for the round-7 fixpoint and residual wording |
| 10 — Falsifiable/reproducible evidence | REQUEST_CHANGES: outer verification can false-accept an incomplete child run |
| 11 — Declared vs executed instrument | PASS for the audited source and independently executed blocks |
| 12 — Unmodeled behavior disappearing | PASS for command-word characters; vocabulary remains disclosed |
| 13 — Terminal-disposition conservation | PASS on the published batteries and matrix |

## Scope and hygiene

- Frozen commit: `df983737b98660bc45a5ea6f87db04c3c6651ce9`.
- Every kickoff-listed tracked artifact audited from the working tree was byte-identical to
  the frozen commit. The only later scoped tracked file was the kickoff itself.
- No protected, Pine, parity, MTC, trading, host, network, or live surface was touched.
- No new attack fixture was authored. All fixture and harness output was redirected to
  temporary files; only the permitted matrix summary is quoted above.
- No git mutation was performed. This verdict is the only repository file authored by the
  audit.
- Tracked `git status --porcelain --untracked-files=no` was clean at entry and immediately
  before this verdict was written. During final verification, a concurrent tracked edit
  appeared in the separate RP6 workstream; it was preserved untouched. Full porcelain was
  also not clean at entry because the shared worktree already held unrelated untracked
  artifacts. The SEC102 audited scope remains clean, and the only audit-created repository
  status delta is this verdict file. A repository-wide clean-status proof would therefore
  be false.

## T1 follow-up

The GLM-5.2 second-opinion condition is triggered both by this flagship finding and by the
greater-than-300-line package. It was not invoked here because the kickoff prohibits network
access. Repair and re-audit remain within the T1 two-round cap.
