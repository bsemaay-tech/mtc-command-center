# 5a9bb922 — canonical flagship round under the narrow owner authorization

Date: 2026-08-02
Target: `codex/gate-a-credential-free-disarmed` @ `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002`
Parent: `origin/master` `637307e83951ffe23e768ed8e50ddaf8712b0660`

## 1. Outcome

| Auditor | Session | Verdict |
|---|---|---|
| `gpt-5.6-sol` xhigh | fresh, `C:\GAAUD_5A_CDX`, full mandated evidence executed | **REQUEST_CHANGES** — two required findings |
| `claude-opus-5` xhigh | 3 fresh sessions, `C:\GAAUD_5A_CLA` | **BLOCK on process grounds** — see §4 |
| `claude-opus-5` (Lead) | recovery session | Lead verification only |

**NOT ACCEPTED.** Two required findings, both reproduced by the Lead on real source. No repair is
authorized and none was implemented.

## 2. The two required findings — reproduced by the Lead

### R1 — `MTC_BRIDGE_START_MODE` is ignored by `create_app()`, and invalid values fail **open**

`bridge/app.py:111` hardcodes `resolve_start_mode(cli_value=start_mode, env={})`, and `create_app`'s
`start_mode` parameter defaults to the literal `"credentialed"` rather than `None`. So the
environment branch inside `resolve_start_mode` is reachable only from `__main__`.

Lead reproduction, real candidate code, `_build_broker` patched so no credential resolver runs:

```
--- via create_app (the public factory) ---
env='credential_free_disarmed' -> credential_free=False  broker_calls_delta=1  raised=No
env=''                         -> credential_free=False  broker_calls_delta=1  raised=No
env='disarmed-ish'             -> credential_free=False  broker_calls_delta=1  raised=No

--- via explicit argument (the only path the tests cover) ---
start_mode=''            -> raised ValueError
start_mode='disarmed-ish'-> raised ValueError
```

Two distinct defects, not one:

1. **Silent downgrade.** A caller that sets the safety environment variable and calls `create_app()`
   gets ordinary credentialed startup — `_build_broker` runs, the real credential resolver is
   reached. That is precisely the failure mode this branch exists to prevent.
2. **Fail-open on invalid values.** Through the factory, `""` and `"disarmed-ish"` do **not** raise;
   they silently select credentialed. The branch record claims "empty or unknown explicit values
   raise before broker/runtime selection" — true only for the explicit-argument path, which is the
   only path the tests exercise.

`gpt-5.6-sol` additionally measured the module-level ASGI app: `module_app_credential_free_disarmed=False`.
`python -m bridge.app` is unaffected (`main_env_mode_flag=True`, `main_env_engine_is_none=True`), and
the two shipped systemd templates use that entrypoint and set no value today — so current deployment
templates are not exposed. The exposure is any other caller.

**Correction to the Lead's earlier record:** this was filed as non-blocking documentation nit **F2**.
That classification was wrong. The consequence is not a misleading sentence, it is a silent fall-back
to credentialed startup. Both flagships independently raised it as required; the Lead's reproduction
agrees.

### R2 — the broker-absence assertion is vacuous

`tests/test_credential_free_disarmed.py:64`, `assert not hasattr(app.state, "bridge_broker")`.
Measured in both modes:

```
line63_engine_is_none:        credential_free=True   credentialed=False
line64_not_has_bridge_broker: credential_free=True   credentialed=True
```

`bridge_broker` is never assigned anywhere in the tree; the assertion is unconditionally true. Line
63 discriminates, line 64 cannot. Previously recorded as optional nit **F1**; `gpt-5.6-sol` rates it
Medium/required. It supplies false assurance about exactly the property the module exists to prove.

## 3. A third defect surfaced, and it is **not** in this candidate's scope

A fresh `claude-opus-5` session found, and the Lead reproduced on real frozen code:

```
durable state at startup : KILLED
GET /api/status reports  : KILLED | version 1
POST /api/disarm no hdr  : 200 DISARMED      <- no X-Confirm header exists on this route
durable state after      : DISARMED
durable state on restart : DISARMED
```

An unauthenticated `POST /api/disarm` clears a durable KILLED latch. The branch description states
"Existing KILLED state is preserved"; measured, it is not.

**Control run — the same happens on the credentialed path** whenever `engine is None`, and the route
is byte-identical to the parent. So the *code* defect is pre-existing and outside this diff's scope;
what belongs to this candidate is the **false claim**. Recommended disposition: correct the claim in
the branch record, and raise the `/api/disarm` KILLED-latch gap as its own authorized work item. It
is not a repair this candidate may absorb.

**Lead correction:** the Lead's first probe of this appeared to show `/api/status` reporting
`DISARMED` over a durable `KILLED` — i.e. the status endpoint lying about the kill latch. That was a
setup artifact: the meta was written after `create_app` had already built the in-memory status. Under
the correct sequence (seed KILLED, close, restart) `/api/status` reports `KILLED` correctly. Not a
defect; recorded because the wrong version was nearly filed.

## 4. Why there is no `claude-opus-5` flagship verdict — three dispatches lost to harness config

None of the three is a finding about the candidate.

1. **Dispatch 1** stopped and asked for approval on `git checkout <sha> -- <paths>`. Cause: the
   authorization text listed `git checkout <branch>` under "not permitted … **any** of them", which
   the auditor reasonably read as covering the path-restoring form that D026 requires. Text fixed to
   permit the path form explicitly.
2. **Dispatches 2 and 3** were run with `--dangerously-skip-permissions` instead of
   `--permission-mode bypassPermissions`. That was a Lead error: the stricter behaviour followed, and
   `git` mutation, `Edit`, and `ssh` were all denied with *"This command requires approval"* in a
   session where nothing could grant it. `--permission-mode bypassPermissions` is the form that
   works, as the `c5a4070a` session proved.
3. A separate, real trap was diagnosed along the way and is now written into the authorization text:
   `ssh -i C:\HyperV\…` silently loses its backslashes and becomes
   `C:HyperVGATEA-STAGINGsshgatea_ed25519` → `Permission denied (publickey)`, which reads exactly
   like an authorization refusal and is not one. Forward slashes plus an explicit
   `UserKnownHostsFile` (the profile path contains non-ASCII characters) is the working form.

A fourth dispatch was **not** launched. `gpt-5.6-sol` had already returned REQUEST_CHANGES with two
required findings that the Lead reproduced, so the branch cannot be accepted this round whatever the
second flagship returns; spending another full audit cycle would not change the disposition. The
flagship floor is therefore recorded as **incomplete for acceptance purposes** — which is honest, and
adequate for a rejection.

Both blocked sessions behaved correctly under the constraint: neither substituted reasoning for
measurement, and one explicitly refused to route around the permission gate by wrapping `ssh` in a
Python subprocess, calling it a real security boundary rather than a bug to engineer past.

## 5. A boundary event to record

Fresh `claude-opus-5` dispatch 2 executed the **real** `_build_broker` / `resolve_hyperliquid_credentials`
path once, to prove the credentialed branch was taken. It self-disclosed this, printed no credential
value, issued no HTTP request, and did not call `engine.start()` or ARM; no exchange connection
occurred, and it did not repeat the call. The owner authorization forbids credential inspection, so
this touched the boundary. The auditor prompt now requires that the credentialed branch be proved
**only** with a patched `_build_broker`. Recorded rather than waved through.

## 6. What both flagships independently confirmed as sound

- Windows W1 `2 failed, 1309 passed, 1 warning`, exactly the two known names.
- Linux locked interpreter: focused `5 passed`; full `25 failed, 1286 passed, 1 warning`, composition
  independently counted as 23 `test_wal_state_bundle.py` + 2 `test_order_state.py`.
- D026 exact-parent `4 failed, 1 passed`; the single GREEN is the no-regression test and is not
  vacuous.
- Import probe: `bridge.settings` and every `bridge.broker.*` module stay out of `sys.modules` after
  a credential-free `create_app(start_runtime=True)`. The credential-free claim holds structurally.
- ARM-guard falsification, measured on the product, not just the test: without the guard
  `POST /api/arm` returns **200**, `state_version` increments to 2, and durable `app_state` becomes
  **ARMED** with no engine and no broker. The guard is load-bearing.
- Broker-exclusion falsification: removing `and not credential_free_disarmed` reaches `_build_broker`,
  2 tests RED, restore 5 passed.
- Route-by-route behaviour with `engine is None`: config 200 / ARM stale-confirm 409 / ARM
  current-confirm 409 mode refusal / disarm 200 / kill 200 durable KILLED / kill-ack 409.

## 7. Safety

`gpt-5.6-sol` returned `HEAD = 5a9bb922…` with empty `git status --porcelain`. No commit, branch
checkout, reset, stash, clean, merge or push. No deletion outside each auditor's own scratch; the
retained `lead-ga3b-*`, `lead-build-round2-*`, `audit3b` and `audit-opus5` trees were left intact. No
broker or exchange connection, ARM transition, order, TESTNET, mainnet, wallet, KVM2, deployment, or
economic action. Except as recorded in §5, no credential value was read, printed, or transmitted.
