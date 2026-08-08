# NEXT SESSION HANDOFF — Gate A ran, A-4 FAILED, repair needs authorization (2026-08-08)

**Supersedes `NEXT_SESSION_HANDOFF_2026-08-03B.md` entirely.** That file's "single remaining blocker"
(the second flagship audit) is closed, and Gate A has since run.

Companion records, in read order:
1. `11_TRIAGE/GATE_A_RESULT_2026-08-08.md` — the Gate A run, with the A-4 traceback.
2. `11_TRIAGE/GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md` — D025 acceptance.
3. `11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md` — the re-baselined Gate A inputs.

---

## State in one screen

| Thing | State |
|---|---|
| Candidate `ebada020a59edf539f60acfbb3a6bf870c8679e9` | **ACCEPTED** 2026-08-08 under D025. Both flagships accepting, zero required findings from any auditor |
| Gate A A-0 identity · A-1 clean-host · A-2 install · A-3 Linux suite | **PASS · PASS · PASS · PASS** |
| Gate A **A-4** starts DISARMED | **FAIL** — service exits 1 in 482 ms, never listens |
| Gate A A-5 … A-9 | **NOT RUN** — first-FAIL rule; each presupposes a running service |
| `origin/master` | `637307e8`, unchanged — nothing Gate A is merged |
| Docs line | `feature/donchian-crypto-ladder` @ `cc413dc3` (pushed) |
| Staging host | `gatea-staging` / `172.24.55.233`, `ebada020` install retained, unit re-masked, inactive, no listener |

## The blocker, stated exactly

A-4 fails because **the shipped deploy artifact never selects the credential-free DISARMED start
mode.** This is flagship NIT 1, which Addendum B §B.3 declared in advance, now reproduced in
production form.

```
bridge/app.py:282   module-level  runtime_app = create_app(
bridge/app.py:150                 runtime_broker = broker or _build_broker(root, dry_run)
bridge/app.py:244                 resolve_hyperliquid_credentials()
bridge/settings.py:113            raise RuntimeError
RuntimeError: Hyperliquid credentials not found: set both HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY …
```

Confirmed on the host, executed as the service account: `resolve_start_mode` → **`credentialed`**. The
installed unit's `ExecStart` is bare `python -m bridge.app`; the env template names no
`MTC_BRIDGE_START_MODE`; `install.sh` leaves every env variable unset by design. So the
credential-free path that `17402a58` added, and that both flagships verified in-process, is
**unreachable from the deployment**.

**It fails closed — say this accurately.** Nothing armed. **Zero** broker connection attempts: the
exception fires while *constructing* the broker, before any network I/O, and both the journal and
`ss -tnp` show nothing. No listener ever opened. The store persisted `app_state=DISARMED`,
`schema_version=4`. A-4 fails because one of its three required confirmations — *the ARM path
refuses* — **cannot be obtained at all** (`POST /api/arm` → `Errno 111 Connection refused`, i.e. no
application refusal to observe). Non-execution is never acceptance.

**Not a regression of `ebada020`.** The identical failure is in the unit's journal at
`Aug 01 23:35:27`. It was invisible on 2026-08-02 because that run died at A-2 and never reached A-4.
Repairing the CRLF defect is precisely what let the gate advance far enough to expose this. The gap
lives in `deploy/`, outside the nine-file merge scope, so `ebada020` is **not** retroactively rejected.

## What the next session must do — and what it must not do

**No product code was modified during the Gate A run. The repair is a product change and needs a new
explicit authorization from Barış.**

1. **Get authorization, then wire the start mode into the deploy artifact.** Either
   `ExecStart=… -m bridge.app --start-mode credential_free_disarmed` in
   `deploy/linux/systemd/mtc-bridge-first-start.service.template:34` and
   `mtc-bridge-steady.service.template:37`, or name `MTC_BRIDGE_START_MODE` in
   `deploy/linux/env/mtc-bridge.env.template` and have `install.sh` set it.
2. **Ask the design question rather than assuming:** should module-level `create_app()` at
   `app.py:282` construct a broker at import time at all? A first DISARMED start arguably should not,
   under any mode. That is a bigger change than the wiring and should be decided, not slipped in.
3. **Fold in the cosmetic-but-misleading message** at `bridge/settings.py:113`: it tells a Linux
   operator to set variables in `HKEY_CURRENT_USER\Environment`, a Windows registry path, in the
   failure message of a Linux-only systemd service.
4. **Then: new frozen SHA → rebuilt artifact → fresh flagship round under D025 → Gate A from A-0.**
   Do not restart mid-gate. A-0→A-3 passing gives high confidence the rerun reaches A-4 quickly.
5. **NIT 3 stays separately owed:** `test_order_state.py::test_gc_referents_of_{transitions,raw_aliases}_contain_no_mutable_container`
   fail on CPython 3.12 and pass on 3.14. The production venv **is** 3.12, so the production floor is
   amber until this is scoped. Pre-existing on `637307e8`, out of Gate A scope.

**Hard stop — unchanged, needs a new explicit instruction from Barış:** merge to master, WP-V /
deployment, credential handling, broker or exchange access, ARM, orders, TESTNET, mainnet, KVM2,
Pine/parity/MTC/trading changes, any economic action.

## Facts worth not rediscovering

**Gate A is re-runnable cheaply.** The step scripts are on the host at `/tmp/a01.sh`, `/tmp/a2.sh`,
`/tmp/a3.sh`, `/tmp/a4.sh`, `/tmp/a4d.sh`, sources in `C:\tmp\gatea_*.sh`. They are already
re-baselined onto `ebada020`; a new SHA needs only the constants at the top changed. Host logs:
`~/gatea-A0A1-20260808.log`, `~/gatea-A2-dryrun-20260808.log`, `~/gatea-A2-install-20260808.log`,
`~/gatea-A3-suite-20260808.log`, `~/gatea-A3-20260808.log`, `~/gatea-A4-20260808.log`,
`~/gatea-A4-diag-20260808.log`, `~/gatea-teardown-20260808.log`, plus
`/var/log/mtc-bridge/bridge.err.log` — **which is where the real traceback lives; the journal shows
only systemd's lines**, because the unit sets `StandardError=append:…`.

**The host was carrying a stale install and roughly 14 G of debris.** Both were cleared under Barış's
explicit authorization on 2026-08-08 (disk 64% → 30%). The torn-down install was release `a1dd5b46…`
from the failed 2026-08-02 attempt, and **its venv was the `a1dd5b46…` interpreter every prior Linux
run used** — that is why Addendum B's venv pin is superseded and A-3 ran on the venv A-2 installed
(same CPython 3.12.3 / pytest 9.1.1). Teardown evidence preserved at
`~/teardown-a1dd5b46-20260808/`. `rollback.sh` takes `--to-release-sha` and is **not** an uninstaller.

**Codex routing corrections are now in `AI_ACCOUNT_AND_MODEL_ROUTING.md`** — the `free` /
`.codex_OLD` route is **Plus**, not Free, and carried the binding flagship audit; a home's
`models_cache.json` is **not** evidence of model availability (a live probe overrides it); the
launcher needs its Codex flags as `-CodexArgs $array`; an isolated audit worktree needs
`--dangerously-bypass-approvals-and-sandbox`, and a non-repo scratch dir needs
`--skip-git-repo-check`.

**D025 rule 3 names the flagship pair as `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh** (`AGENTS.md:66`).
GLM-5.2 is canonical auditor 4 and holds no flagship slot. The 2026-08-03 records had described
GLM-5.2 as the first flagship; that reading does not match the rule, so a fourth round was run rather
than accepting on the weaker reading. Recorded honestly: the integration merge was authored by a Claude
Lead session, so the cross-model axis on the merge comes from round 3 (`gpt-5.6-sol`), not round 4.

## Budget

≈14–17 h of the 50-hour plan remained before this session; WP-A (3 h), WP-R (6 h) and WP-V (8 h) total
17 h and are all still ahead. The A-4 repair, its artifact rebuild and its flagship round are **again
unbudgeted work**, as the Gate A repair queue was. **Re-plan with Barış before committing to the
remainder** rather than absorbing it silently.
