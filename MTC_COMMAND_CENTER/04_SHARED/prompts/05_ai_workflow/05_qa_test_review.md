# 05 — QA / Test Review  (Gate 4)

Use **right after Gate 3 (impl)**, before adversarial review.

## Inputs to provide

- The diff.
- The Gate 2 test plan, if produced.

## Prompt

```
You are running Gate 4 (QA) for Tradingview_LAB_CLEAN.

Steps:

1. TEST SUITE: if the affected module has a test suite, run it. Capture
   the exact command and the pass/fail output. Do not paraphrase
   failures — quote them.

2. LINT / TYPECHECK: if configured for the affected language
   (ruff/pyright for Python, etc.), run it. Capture command + output.

3. PARITY SMOKE: if the change touches anything inside
   MTC_COMMAND_CENTER/02_MTC_BACKTEST/ or affects strategy output,
   run the smallest parity smoke that exercises the change. Quote the
   pass/fail result.

4. MANUAL VERIFICATION: if the change is UI / chart / Pine plotting,
   describe what was visually verified. If it cannot be verified
   without launching the chart, say so explicitly — do NOT claim
   success.

5. REGRESSION RISK NOTE: one short paragraph on what could break
   elsewhere. Be specific.

Report format:
- Commands run + verbatim output (truncated only if huge — keep
  failures intact).
- PASS / FAIL per check.
- GATE DECISION: proceed to Gate 5 / loop back to Gate 3 / escalate.

Never claim PASS without evidence. Never invent test output.
```

## WRITE-BACK

- Append a one-line entry to `SESSION_LOG.md` with the QA result.
- If a new parity edge case was discovered, note it in `NEXT_STEPS.md`.
