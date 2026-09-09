# REVIEW_CHECKLIST

Run before committing, before opening a PR, and before declaring any
task "done". Tick mentally; if any box fails, fix or escalate.

> For trading-strategy / backtest code specifically, also run
> `STRATEGY_CODE_REVIEW_CHECKLIST.md` (repaint, lookahead, leakage, execution,
> Pine⇄Python conversion).

## Scope

- [ ] Change matches the scope approved in Gate 1.
- [ ] No unrelated edits in the diff.
- [ ] No speculative features, no premature abstractions.
- [ ] No new dependencies added without explicit approval.

## Safety

- [ ] No file in `DO_NOT_TOUCH.md` was modified.
- [ ] No Pine logic / MTC strategy behavior changed (or change was
      explicitly approved by Barış).
- [ ] No parity-suite regression risk introduced (or risk noted and
      acknowledged).
- [ ] No secrets, tokens, or credentials added.
- [ ] No destructive git operation queued.

## Code Quality

- [ ] Minimal diff.
- [ ] No dead code, no commented-out blocks left behind.
- [ ] Comments explain WHY, never WHAT, and only when non-obvious.
- [ ] Error handling only at real boundaries (no defensive stubs for
      impossible paths).

## Tests / Verification

- [ ] Tests run and pass (if a suite exists).
- [ ] Lint / typecheck clean (if configured).
- [ ] Manual verification done if UI / chart / Pine output changed.
- [ ] Parity smoke test run if backtest or strategy code touched.

## Adversarial Review

- [ ] A different AI model reviewed the diff (Gate 5).
- [ ] Reviewer findings addressed or explicitly deferred.

## Memory Write-Back (Gate 7)

- [ ] `GLOBAL_HANDOFF.md` updated.
- [ ] `NEXT_STEPS.md` updated.
- [ ] `SESSION_LOG.md` got a one-line entry.
- [ ] `DECISIONS.md` updated if a sticky decision was made.
- [ ] `ACTIVE_FILES.md` updated if working set changed.
- [ ] `PROJECT_MEMORY.md` updated if a stable repo fact changed.

## Commit Hygiene

- [ ] Commit message follows existing repo style (see `git log`).
- [ ] No `--no-verify`, no `--no-gpg-sign`, no `--force` unless
      explicitly approved.
- [ ] Branch / PR target is correct.
