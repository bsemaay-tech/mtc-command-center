# Gate A credential-free DISARMED candidate - frozen, not accepted

Date: 2026-08-02  
Lead: Codex app, `gpt-5.6-sol` xhigh  
Safety state: DISARMED, source/test only

## 1. Frozen candidate

- branch: `codex/gate-a-credential-free-disarmed`
- parent: `637307e83951ffe23e768ed8e50ddaf8712b0660` (`origin/master`)
- candidate: `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002`
- pushed: yes; local and origin matched `0 0`
- exact scope:
  - `IBKR_PAPER_BRIDGE/bridge/app.py`
  - `IBKR_PAPER_BRIDGE/bridge/api/routes.py`
  - `IBKR_PAPER_BRIDGE/tests/test_credential_free_disarmed.py`

The secondary-account Codex implementer first received the exact protected contract in a managed
`workspace-write` session. The CLI silently downgraded that session to read-only; it changed no file
and ran no test. A focused retry on the same counterpart used the next supported isolated-worktree
sandbox tier and produced the three-file candidate above.

## 2. Implemented behavior

The candidate adds an explicit `credential_free_disarmed` runtime mode selectable through
`--start-mode` or `MTC_BRIDGE_START_MODE`. The absent mode remains ordinary credentialed startup;
empty or unknown explicit values raise before broker/runtime selection.

In credential-free mode it initializes the local Store and FastAPI lifecycle but constructs neither
`HyperliquidBroker` nor `BridgeEngine`, does not call the credential resolver or Windows registry,
and reports `DISARMED` with network, exchange, credential lookup, and ARM capability disabled. A
correct-current-version `/api/arm` request returns HTTP 409 without changing `state_version` or the
durable DISARMED state. Existing KILLED state is preserved. Credentialed startup still follows the
existing `_build_broker` path.

## 3. Lead reproduction

Windows Python 3.14.2, candidate worktree:

- new focused module: **5 passed, 1 warning**
- affected bundle: **52 passed, 1 failed, 1 warning**; the only failure was the known canonical
  evidence-ledger working-copy hash mismatch
- full Bridge suite: **2 failed, 1309 passed, 1 warning**; exactly the known evidence-ledger hash
  and stale schema-version assertions
- `py_compile`: PASS
- `git diff --check`: PASS

D026 exact-parent RED was independently reproduced from a clean detached `origin/master` worktree.
The candidate's exact new test module was run with parent source forced through `PYTHONPATH` and
candidate `conftest.py` disabled: **4 failed, 1 passed, 1 warning**. Failures were the missing
`resolve_start_mode` behavior and missing `create_app(start_mode=...)` contract, not dependency or
listener failures. The same module was GREEN on the candidate as recorded above.

An LF-clean archive of the frozen SHA was extracted to the disposable `GATEA-STAGING` host for the
executing audit. Source SHA-256 values were recorded, but no Linux count is claimed here because no
auditor returned a complete command ledger.

## 4. Required executing-auditor disposition

The temporary roster required an executing GLM-5.2 audit before acceptance.

1. Fresh audit attempt 1 was stopped after it returned no output within the initial bounded wait.
   It left no process, temporary GLM configuration, source change, or test scratch. With no returned
   command ledger it is **BLOCK** under D025.
2. Fresh audit attempt 2 used a shorter command-first prompt and exact Windows/Linux commands. It
   hit the wrapper timeout after 784 seconds with no returned ledger. It is also **BLOCK** under
   D025, regardless of partial basetemp evidence.
3. The owner-authorized temporary substitution window expired at 14:53 local. No third audit was
   launched and the temporary authority was not extended implicitly.

## 5. Verdict and continuation

**NOT ACCEPTED.** Candidate `5a9bb922` is frozen, pushed, clean, and ready for a fresh canonical
executing audit, but it does not carry the temporary acceptance label. Reopen with renewed owner
authority or the restored canonical flagship/auditor roster. The next auditor must independently
execute the exact-parent RED, candidate GREEN, and complete Windows/Linux floors.

Queue D remains blocked independently because defect 3b reached its maximum-three-result hard stop.
Do not integrate, rebuild, rerun Gate A, merge to master, or touch KVM2 on this record.

## 6. Safety and cleanup

No service or uvicorn process was started. No credential lookup/value, registry secret, broker or
exchange connection, ARM transition, order, cancellation, TESTNET, mainnet, wallet, KVM2, deployment,
or economic action occurred. The disposable VM was used only for an LF-clean source copy and
test-only SSH. The exact remote audit source/basetemp root and all exact local pytest/audit scratch
roots were validated and removed. Product, parent-RED, and audit worktrees remained clean.
