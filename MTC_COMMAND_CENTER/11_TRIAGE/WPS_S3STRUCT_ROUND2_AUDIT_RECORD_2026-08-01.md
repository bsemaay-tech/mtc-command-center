# S3-STRUCT ROUND 2 — AUDIT RECORD AT `216682ba` (2026-08-01)

**Outcome: NOT ACCEPTED.** Both canonical flagships returned `REQUEST_CHANGES`. Three required
findings, each reproduced by the Lead on real source before it bound. Round 3 is the last repairable
round under the `AGENTS.md` bound of three non-accepting rounds.

## Roster result

| Auditor | Model / route | Suite executed | Verdict | Worktree |
|---|---|---|---|---|
| 1 | `claude-opus-5` xhigh, `C:/WPSAUD7` | yes — `2 failed, 1266 passed in 132.93s` | **REQUEST_CHANGES** (R-1, R-2, 8 nits) | clean, `HEAD` unchanged |
| 2 | `gpt-5.6-sol` xhigh, `C:/WPSAUD6` | yes — `2 failed, 1266 passed in 121.53s` | **REQUEST_CHANGES** (R-3) | clean, `HEAD` unchanged |
| 3 | `cline-pass/deepseek-v4-flash` | no (attempt 1) | **non-execution** — see below | n/a |
| 4 | GLM-5.2 via `Invoke-GlmAudit.ps1`, `C:/WPSAUD8` | no | **BLOCK** — see below | clean, `HEAD` unchanged |

Lead's own independent run at `216682ba`: `2 failed, 1266 passed in 100.06s`. Three independent runs
agree on the floor; the two failures are the known pre-existing pair.

## Auditor 4 — BLOCK, with the exact cause

The route itself is correct and is **not** a Cline route. Auditor 4 is dispatched through
`C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GlmAudit.ps1`, which calls `C:\Users\BarışSemaay\bin\glm.ps1`,
which injects `ZAI_GLM_CODING_PLAN_KEY` from Windows Credential Manager into the child process only
and points `claude` at `https://api.z.ai/api/anthropic` with GLM-5.2 mapped to every model tier.

The invocation ran and failed on authentication:

```
Failed to authenticate. API Error: 401 token expired or incorrect
GLM_EXIT_CODE=1
```

That is the verified `glm` invocation itself failing, which is the defined condition for recording
auditor 4 as BLOCK rather than as an absent route. The same credential was live-tested earlier on
2026-08-01 with `CREDENTIAL_PRESENT=true`, `GLM52_SUBSCRIPTION_OK`, `GLM_EXIT_CODE=0`, so the token
has expired or been rotated since that test.

**Owner action required to restore auditor 4:** refresh `ZAI_GLM_CODING_PLAN_KEY` in Windows
Credential Manager. The Lead does not handle credentials and made no attempt to read, set, or
duplicate one. `C:/WPSAUD8` was left clean at `216682ba`; nothing was audited.

## Auditor 3 — non-execution, then re-dispatched on a different delivery

Attempt 1 with `--auto-approve false` in a non-TTY session had **every** tool refused —
`run_commands` and `read_files` both returned `requires approval in a TTY session`. It retried the
same `git diff` three times and aborted having seen none of the diff. Under D025 rule 1 that is
non-execution, never acceptance.

Flipping `--auto-approve` was rejected as a fix: auto-approving a model with shell access inside a
git worktree is a genuine write risk, including `git push`, and the `git status --porcelain` check
catches a write only after it has happened. The delivery was changed instead — the narrow brief only
needed one file's round-2 delta, so the diff was put **inline in the prompt** and the auditor needed
no tools at all. That also removed the exploration that caused both of last cycle's timeouts.

**Attempt 2 also failed, for an unrelated reason.** With the diff inline it began echoing the diff
back verbatim rather than analysing it, and the response stream then broke on a malformed provider
chunk:

```
JSON Parse error: Expected '}' — model deepseek/deepseek-v4-flash
```

No verdict either time. Two attempts, two distinct causes — a harness approval gate and a provider
stream fault — on top of last cycle's two timeouts. Auditor 3 is recorded as **non-execution** for
round 2 and no third attempt was spent, the round already being settled by two flagship
`REQUEST_CHANGES` verdicts.

**Standing conclusion for this auditor:** four failed dispatches across two cycles, never once
producing a verdict. It should not be treated as reliable round-gating detection until one dispatch
completes end to end; budget it as opportunistic only.

## The three required findings

### R-1 — `orders.py:3473` — a normal, uncorrupted state latches `KILLED` *(claude-opus-5)*

`create_trade` does not list `entry_px` in its INSERT columns — verified at **both** `db.py:4858-4862`
and `db.py:7565-7570` — so every trade is created with `entry_px IS NULL` until an ENTRY fill. The
predecessor read `self._store_float(trade["entry_px"] or trade["expected_px"], …)`, and that `or`
existed precisely to select `expected_px` in that state. Round 1's eager read faults first;
`DurableRowFault` is a `RuntimeError` and is not caught by the
`except (InvalidOperation, TypeError, ValueError, OverflowError, LotQuantizationError)` at
`orders.py:3478-3484`.

The `else` branch is entered **exactly** when no ENTRY-fill aggregate exists — **exactly** when
`entry_px` is NULL. The `expected_px` fallback is therefore dead code and every entry into that
branch faults. At `732b37c3` the same state closed the trade normally.

**The shipped matrix masked it** with `UPDATE trades SET entry_px=100.0` in the trades arm — a line
that is not part of the corruption under test and exists only to stop the boundary faulting on the
ordinary NULL. This is the round's most important lesson: a green matrix proved nothing here.

Root cause is a contract gap, not a call-site bug: the registry treats "SQL NULL" as one fault case,
but `trades.entry_px` is NULL **by design** while `fills.fee` NULL is **corruption**.

### R-2 — `db.py:6655`, `:6664` — the boundary's fault type escapes an existing conversion contract *(claude-opus-5)*

Round 2 routed `trade_fill_totals` and `trade_costs` through `DURABLE_EVENT_ROWS`, but
`_expected_kill_flatten_closure_in_tx`'s containment clause at `db.py:6668-6680` catches only
`(InvalidOperation, KeyError, TypeError, ValueError, OverflowError)`. `DurableRowFault(RuntimeError)`
matches none. With `fills.fee` NULL on an APPLIED `KILL_FLATTEN` fill, operator ACK →
`acknowledge_kill_evidence` → `_assert_kill_flatten_closure_in_tx` raises a bare `RuntimeError` named
`DURABLE_FILLS_FEE_NULL` instead of `KillConflictError("KILL_FLATTEN_LIFECYCLE_CONFLICT")`. Same
escape at `db.py:6863` via `validate_applied_kill_flatten_lifecycle_closures`, called from
`orders.py:1709`. `trade_costs` previously used `COALESCE(SUM(fee), 0.0)` and never raised at all —
**the repair itself created the raise.**

### R-3 — `orders.py:3607-3621` — `DEFERRED` is reachable and escapes *(gpt-5.6-sol)*

**The Lead's round-2 rationale was wrong and is recorded as a Lead error.** The claim was that
`record_kill_lifecycle_deferral`'s identity query is strictly stronger than the close-path predicate,
so `DEFERRED` could not occur. Both flagships broke it, by different mechanisms:

- **`gpt-5.6-sol` (load-bearing):** the comparison only ever held for one database snapshot.
  `close_trade_once_with_decision` **rolls back and returns** before `record_kill_lifecycle_deferral`
  opens its **own separate** `BEGIN IMMEDIATE` (`db.py:5337-5377`). An ABA restoration in that window
  makes the already-inserted fill satisfy the deferral query, so `DEFERRED` is returned and
  `orders.py:3621` re-raises. **A snapshot argument can never be valid across two transactions.**
- **`claude-opus-5`:** even within one snapshot the predicates differ. The close binds on
  `resolved_epoch.episode_id` (`db.py:7656`); the deferral binds on `orders.group_id`;
  `_kill_lifecycle_identity` never requires them equal. Active epoch **A** plus an order still bound
  to an older, still-present episode **B** reaches `DEFERRED` with **no second `Store` at all**.

**Escape point, Lead-verified:** the re-raise sits inside `_ingest_fill`. The queued drains contain
it, but the direct kill-lifecycle callers at `orders.py:1302` and `orders.py:1683` do not pass
through `_ingest_queued_event`'s containment handler, so the conflict escapes there inside an active
kill episode.

## What both flagships agreed is settled — not re-opened in round 3

One registry-driven boundary (`DURABLE_EVENT_ROWS` over `DURABLE_EVENT_COLUMN_TYPES`), routed by
returning typed *rows* from the store rather than by wrapping call sites, which is what makes a new
consumer validated by default. Both legacy helpers deleted. Both matrices generated from declared
registries. Class-C join added as a conjunct with the epoch fence intact. Accessor total across
bytes, `memoryview`, `Decimal('NaN')`, `bool`, subnormals, `-2**63` accepted and `+2**63` rejected.
Allowlist exact, `engine.py` untouched, no broker/network/ARM/live path.

**Both auditors explicitly judged this NOT a fourth point fix** — all three findings are containment
gaps at the boundary's edges, not a return of the old pattern.

## Nits deferred to TS-P1-010 — deliberately not fixed in round 3

N-1 int64 range check applied to `FINITE_FLOAT` columns · N-2 two reason codes for one storage-class
fault · N-3 asymmetric TEXT policy between `INT64` and `FINITE_FLOAT` · the `trades.sl_initial` /
`tp_initial` registry gap at `orders.py:3069-3071` and `:3186` (reachable from `reconcile()` but not
from a queued broker event, so outside S3T-C as scoped).

## Hours

Recorded against the owner-authorised extension beyond the plan's contingency line, per the cycle
handoff §6 — not silently absorbed into the 5 h contingency, which stands at 2.0 h remaining.
