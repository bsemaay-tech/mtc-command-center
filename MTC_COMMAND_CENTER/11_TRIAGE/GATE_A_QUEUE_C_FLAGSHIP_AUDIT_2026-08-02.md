# Queue C `5a9bb922` — `claude-opus-5` canonical executing flagship audit

Date: 2026-08-02
Auditor: `claude-opus-5` xhigh, executing
Target: `codex/gate-a-credential-free-disarmed` @ `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002`
Parent: `origin/master` `637307e83951ffe23e768ed8e50ddaf8712b0660`
Audit worktree: `C:\GAAUD_5A_CLD` (fresh, detached, clean at close)

Supersedes the blocked disposition in `GATE_A_CREDENTIAL_FREE_DISARMED_CANDIDATE_2026-08-02.md` §4,
which recorded two GLM attempts that returned no ledger. This is the fresh canonical executing audit
that record asked for.

## 1. Verdict — classification corrected 2026-08-02

**Claude accepting verdict / Lead verification**, with one verified optional nit (§5, F1).

This work was performed in the recovery session in which the same model also acted as Lead — not a
fresh independent auditor session. On the owner's instruction it is recorded as Lead verification,
**not** a canonical flagship verdict, and a fresh no-resume `claude-opus-5` xhigh auditor session was
launched separately on the exact frozen SHA.

No `gpt-5.6-sol` verdict was available at the time of writing: Codex CLI could not execute on this
host. The diagnosis is in `GATE_A_C5A4070A_RETROSPECTIVE_AUDIT_2026-08-02.md` §6. Under **D025 rule
3** this branch is **not** canonically accepted — do not integrate, rebuild, rerun Gate A, merge, or
touch KVM2 on this record, and do not label it fully accepted until the flagship floor is satisfied.

## 2. Executed evidence

Windows: Python 3.14.2, pytest 9.0.2. Linux: `GATEA-STAGING` Ubuntu 24.04 with the locked
interpreter `/opt/mtc-bridge/venvs/a1dd5b46…/bin/python` (3.12.3, pytest 9.1.1) — no new venv.
Archive transport verified by SHA-256 on both ends
(`41b882420757fabf4256148bd6a05ec5c20ee00b71bb2d3928160a8b64ed7e78`).

| Check | Prior record | This audit |
|---|---|---|
| Windows full Bridge suite | 2 failed, 1309 passed | `2 failed, 1309 passed, 1 warning in 148.63s` |
| Windows focused new module | 5 passed | `5 passed, 1 warning` |
| Linux focused new module | not established | **`5 passed, 1 warning in 0.88s`** |
| Linux full Bridge suite | **no count claimed** | **`25 failed, 1286 passed, 1 warning in 168.25s`** |

The Linux floor is established here for the first time. The two Windows failures are the known
ledger working-copy CRLF and stale `schema_version` cases. The 25 Linux failures are the known
defect-3b `test_wal_state_bundle.py` cascade plus the two Python-3.12 `test_order_state.py`
GC-referent cases — the same composition as every other branch off this parent, with nothing new
introduced by Queue C. Counted, not assumed:

```
23 FAILED tests/test_wal_state_bundle.py
 2 FAILED tests/test_order_state.py
 0 FAILED anywhere else
```

Collection totals corroborate each other: 1311 tests on **both** platforms — parent 1306 plus this
branch's 5 new tests.

## 3. D026 — exact-parent RED

```
git checkout 637307e8 -- bridge/app.py bridge/api/routes.py
pytest tests/test_credential_free_disarmed.py   ->  4 failed, 1 passed
git checkout 5a9bb922 -- (same two files)       ->  5 passed
git status --porcelain                          ->  empty
```

The one test that passes against the parent is
`test_ordinary_credentialed_runtime_still_uses_existing_broker_path` — correct, that is the
no-regression test and it must be green on both sides. The other four are genuinely parent-RED.

## 4. Independent falsification — the ARM guard is load-bearing, and it is a safety guard

The `/api/arm` 409 was removed from `routes.py` and the module re-run:

```
mutant  ->  1 failed, 4 passed
            FAILED test_status_is_truthful_and_current_version_arm_is_durably_rejected
restored -> 5 passed, git status --porcelain empty
```

What the mutant actually does, measured rather than argued — credential-free app, correct
`X-Confirm` version:

```
POST /api/arm            -> 200
durable app_state after  -> ARMED
```

Without the guard, `arm()` falls through to the `engine is None` branch and calls
`_set_state(request, "ARMED")`. A bridge started with **no broker, no credentials and no exchange
access** would durably record itself as ARMED. With the guard it returns 409, `state_version` is
unchanged, the store still reads `DISARMED`, and a restart on the same database still reads
`DISARMED`. This is a real safety property, not a cosmetic refusal.

## 5. Findings

**F1 — verified optional nit, non-blocking: one assertion is vacuous.**
`tests/test_credential_free_disarmed.py:64`

```python
assert not hasattr(app.state, "bridge_broker")
```

`app.state.bridge_broker` is never set anywhere in `bridge/`. Measured, not inferred:

```
credentialed app  has state.bridge_broker : False
credential-free   has state.bridge_broker : False
```

The assertion cannot fail in any mode, on the candidate or on the parent. It is exactly the class of
assertion D026 exists to stop. It is not blocking because the same test's other guards — a patched
`_build_broker` that raises, `calls == []`, and `bridge_engine is None` — do turn RED against the
parent.

**Owner disposition, 2026-08-02: leave it unchanged for now.** Editing the frozen candidate to
delete a non-blocking assertion would invalidate the SHA that every audit in this cycle is measuring,
which costs more than the nit. The cleanup is scheduled separately, after Gate A, unless a flagship
reproduces it as a *required* finding. The replacement, when it happens, should measure the actual
property — e.g. `"bridge.broker.hyperliquid" not in sys.modules` after a credential-free start.

**F2 — nit, documentation only.** The candidate record says the mode is "selectable through
`--start-mode` or `MTC_BRIDGE_START_MODE`". `create_app` calls `resolve_start_mode(cli_value=start_mode, env={})`
with a non-`None` default, so the **environment variable is only ever consulted through the
`__main__` entrypoint**, never through `create_app`. That is the safer design — a stray environment
variable cannot silently reconfigure an embedded app — but the sentence as written overstates it.

## 6. What was verified structurally

- `bridge/app.py` at the candidate carries **no** module-level import of `bridge.settings`,
  `HyperliquidBroker`, `MockBroker`, `BridgeEngine`, `RiskEngine` or the strategy. The single
  remaining `settings` reference is the deferred
  `from bridge.settings import resolve_hyperliquid_credentials` inside `_build_broker`.
- `bridge/api/routes.py` imports nothing from `bridge.settings` or `bridge.broker` at module level.
- Every mutating route already guards `engine is not None`, so credential-free mode cannot produce a
  500 from a missing engine; `/api/arm` was the one path that would otherwise have *succeeded*
  wrongly, which is why it needed the explicit refusal.
- Empty or unknown explicit modes raise `ValueError` before broker selection; `dry_run` and an
  injected `broker` are both rejected in credential-free mode.

## 7. Safety

DISARMED, source and test only. No service or uvicorn process started, no credential read or
written, no registry access, no broker or exchange connection, no ARM transition, no order, no
TESTNET, no mainnet, no wallet, no deployment, no economic action. `KVM2-Ubuntu-2404-Staging`
remains powered off and untouched. Every mutation was restored and `git status --porcelain` verified
empty afterwards.

Scratch: `C:\GAAUD_5A_CLD`, `C:\tmp\opus5audit\` on Windows; `~/opus5-5a`, `~/opus5-5a.tar`,
`~/opus5-5a-basetemp` on `GATEA-STAGING`.
