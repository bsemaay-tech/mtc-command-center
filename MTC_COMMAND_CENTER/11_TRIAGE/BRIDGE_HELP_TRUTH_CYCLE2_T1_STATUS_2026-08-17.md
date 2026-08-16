# Bridge Help truth cycle 2 — T1 status — 2026-08-17

## Classification and boundary

- Gate 1: bounded local Help/Wiki UI, index and tests.
- Highest surface: **T1** (non-economic product UI/test work).
- No deployment, host contact, credential access, ARM/order action, Pine/parity,
  MTC strategy or trading-logic change is authorized or claimed.

## Lead verification before audit

The six-file Help candidate remained isolated in `C:\BRIDGE_HELP_IMPL`. The
focused dashboard-static suite passed **41 tests** with one warning; JavaScript
syntax and `git diff --check` passed. The implementer had also reported 1,058
full-suite passes plus two pre-existing repository failures, neither attributed
to this Help diff.

## T1 round 1 verdict — REQUEST_CHANGES

Fresh Codex `gpt-5.6-sol`, effort `high`, independently reproduced two required
source-truth repairs:

1. The LLM gate is dormant and not constructed from configuration, but the
   runtime does read/serve the `llm:` configuration and the dashboard displays
   `veto_enabled`. Help must distinguish **read/display** from **activation**;
   it must not say no runtime code reads the switches or call the whole LLM page
   empty.
2. `NullLLMGate.check()` produces `SKIPPED`, and the engine stores a generic
   `LLM_SKIPPED` decision row. Help must not say nothing is logged. It may still
   say no directive or model-call record is persisted and keep the planned
   directive/store edges planned.

The auditor passed the focused 41-test suite, JavaScript syntax, diff checks and
the targeted D026 discrimination checks. Its read-only sandbox allowed 526
full-suite tests to pass, reproduced the known deployment-ledger failure, and
prevented 533 temp-dependent setups. No additional product failure was found
among runnable tests.

## Repair attempt and concrete blocker

The same counterpart implementer (`claude-opus-5`, `high`) reproduced both
findings and drafted the precise three-file repair, including a further wording
correction: `llm_directive_id` is a **trade-row** field, not a decision-row
field. Its first run had no edit permission and changed zero bytes. A fresh run
with explicit edit permission then stopped immediately because the Claude
weekly limit had been reached; the route reports reset at **2026-08-19 23:00
Europe/Chisinau**.

The required counterpart is therefore unavailable. Per the two-tier operating
model, the Codex lead did not silently implement the repair or substitute a
weaker model. No Help file was committed, transferred, deployed or accepted.
The existing isolated candidate remains intact.

## Next safe action

After the exact Claude route resets, apply the already bounded three-file
wording/test repair in `C:\BRIDGE_HELP_IMPL`, reproduce D026 RED/GREEN, run the
focused suite and JavaScript/diff checks, then use the final permitted fresh T1
audit round. Until then the Help/Wiki candidate is **useful but unaccepted**.

