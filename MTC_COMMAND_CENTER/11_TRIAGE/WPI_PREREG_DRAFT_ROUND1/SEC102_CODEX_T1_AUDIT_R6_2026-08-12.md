# VERDICT: REQUEST_CHANGES

TIER: T1

APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, `xhigh` per the explicit kickoff; independent read-only audit. T1 maximum: two rounds.

## Required finding

`composite_pathproof.py:207`, `composite_pathproof.py:1268`, `composite_pathproof.py:1449`, `composite_pathproof.py:1476`, `composite_pathproof.py:1518`: **CRITICAL — the command-word admission policy is not closed.** Three option-enabled pathname-pattern classes—one-or-more, exactly-one, and negated—contain none of the characters covered by the round-6 expansion fence. At the scanner boundary, each is split/admitted as benign command-position leaves; the opaque check is clear and word conservation reports no reason. With the relevant shell option enabled, any of these classes can pathname-resolve to an already-recognized interpreter or source command and hide the following operand. This is a genuinely new admission gap, not another interpreter name and not the disclosed vocabulary residual.

Minimum required repair:

1. Refuse every option-enabled pathname-pattern operator class before any part can be admitted as a leaf, including the three missed classes, in every scanner-reachable command position.
2. Add D026 evidence that is RED against the exact round-6 behavior or an equivalent deliberate mutation and GREEN after repair. The falsification must prove both the scanner disposition and the terminal STOP.
3. Extend the declared grammar battery and closure sweep to cover the complete operator family, then rerun the matrix and all carried fences.
4. Narrow the closure claim until the new evidence supports it.

## Reproduced evidence

The published 52-case matrix was executed verbatim with output redirected to a temporary file:

```text
CASES=52 FAILED_COUNT=0
```

The four kickoff-named command-word cases were rerun independently. Their terminal lines were:

- Glob class:

  ```text
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
  ```

- Parameter-expansion class:

  ```text
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
  ```

- Command-substitution class:

  ```text
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
  ```

- Tilde class:

  ```text
  COMPOSITE_PATHPROOF verdict=STOP rc=3 reason=render_stage_incomplete
  ```

The proven-static non-interpreter control remains a benign leaf:

```text
COMPOSITE_PATHPROOF verdict=PASS rc=0 reason=render_stage_closed
```

The published pre-feature/current comparison also completed successfully:

```text
CASES=8 RC_LEVEL_NEW_REDS=5 OFF_EXPECTATION=0
```

The published mutation, grammar-closure, carried-prefix, carried-discriminator, hygiene, AST, and fixture-identity blocks all completed with successful process status. No raw fixture rows, shell bodies, or sensitive literals are reproduced here.

## Evidence-package accuracy

`KICKOFF_CODEX_SEC102_R6_AUDIT.md:26`, `KICKOFF_CODEX_SEC102_R6_AUDIT.md:36`, `SELF_QA_SEC102_R6.md:384`, and `SELF_QA_SEC102_R6.md:1413`: the evidence labels need correction. The matrix contains 44 pre-round-6 cases and eight round-6 additions, not 48 carried cases. Two of the four kickoff-named fixtures were already terminal STOPs on the pre-feature code, so they are carried controls rather than new rc-level REDs. The self-QA discloses both facts, but the kickoff/closure wording still overclaims them.

## Residual judgments

- Interpreter vocabulary: acceptable as an explicitly scoped limitation at this stage because it remains a separate disclosed production-gate blocker. It does not excuse the required finding above, which can resolve to an interpreter already in the declared vocabulary.
- Conservative false-stops: acceptable fail-closed behavior for this stage. The static benign control proves the policy is not a blanket STOP.
- Expansion-character-set residual: not acceptable merely as a disclosed epistemic limit once a concrete missed operator family is demonstrated. It is an admission-policy defect.

## Thirteen-pattern adjudication

| Pattern | Result |
|---|---|
| 1 — STOP/PASS/FAIL ordering | PASS |
| 2 — Host and namespace identity | PASS within explicit non-host scope |
| 3 — Host-object, symlink, mount identity | PASS as an explicit non-claim |
| 4 — External interpreter/environment boundary | PASS as a disclosed production blocker |
| 5 — Grammar incompleteness | REQUEST_CHANGES: concrete missed operator family |
| 6 — Probe status before adjudication | PASS |
| 7 — Incomplete-reader path | PASS; unchanged |
| 8 — Deployed identity | PASS within lexical scope |
| 9 — Claim wording vs predicate | REQUEST_CHANGES: closure and RED/count wording overclaim |
| 10 — Declared vs executed evidence | PASS for the blocks rerun here |
| 11 — Instrument defects | PASS for reproduced baseline/mutation evidence |
| 12 — Unmodeled behavior disappearing | REQUEST_CHANGES: missed classes disappear as benign leaves |
| 13 — Terminal-disposition conservation | PASS on the published batteries |

## Scope and hygiene

- Commit `c5e443b2` and every kickoff-listed tracked artifact/fixture were byte-identical in the working tree when audited.
- No protected, Pine, parity, MTC, trading, host, network, or live surface was touched.
- No attack fixture was authored. Fixture output was redirected to temporary files and removed after inspection.
- No git mutation was performed. This verdict is the only repository file authored by this audit.
- A globally clean `git status --porcelain` cannot be truthfully proved: the shared worktree was already dirty in unrelated workstreams before the audit began. The frozen audited inputs themselves were clean and byte-identical; the pre-existing changes were preserved untouched.

## T1 follow-up

The GLM-5.2 second-opinion condition is triggered both by this flagship finding and by the greater-than-300-line package. It was not invoked in this session because the kickoff explicitly prohibited network access.
