# Gate A — A-5 FAIL (run-kit D, 2026-08-09) — reproduced post-start readiness race; staging proven safe

> **STATUS: A-0 · A-1 · A-2 · A-3 · A-4 PASS · A-5 FAIL · A-6..A-9 NOT RUN.** A-5 is a genuine FAIL
> under the frozen run-kit D criteria: the frozen `gatea_A5.sh` failed its post-listener assertion
> immediately after the authorized manual restart, before the application finished binding the
> loopback listener. **It cannot be promoted to PASS from later diagnostics.** The staging state was
> independently proven safe, active, loopback-only, credential-free DISARMED, and DB-consistent a few
> seconds later, so the conditional stop/mask response was **not** required and was **not** performed.
> **A-6 through A-9 were NOT RUN** (first-FAIL rule). Next is protected run-kit repair — a new
> revision; D and its evidence are preserved unchanged.

This is a **bounded documentation checkpoint by GLM-5.2** in the isolated worktree `C:\GA5F` on
branch `codex/gatea-a5-fail-checkpoint` at `7421bc34ec67215f496e9a546dcadbb00bca0254`. The A-5
staging execution and the read-only on-disk diagnostics recorded here were **authorized staging
actions performed by the Lead** under the owner-approved preregistered `gatea-staging` Gate A rerun
sequence, and their results are recorded — not performed or mutated — by this documentation unit. No
product code or product artifact changed; no credential, broker/exchange access, successful ARM,
order, TESTNET/mainnet, wallet, master merge, or economic action is authorized or occurred. Hard
exclusions unchanged. **GLM-5.2 edited only documentation** (the four task-named files: this report
plus `_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, and
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`). The worker performed no staging action, script run,
install, service mutation, credential access, broker/exchange access, ARM, order, TESTNET/mainnet
action, master merge, economic action, or Git mutation.

---

## 1. Pre-checkpoint state (exactly as recorded)

| Item | Value |
|---|---|
| Active integration branch before this task | `feature/donchian-crypto-ladder` |
| Branch checkpoint SHA | `7421bc34ec67215f496e9a546dcadbb00bca0254` (`7421bc34`) |
| Accepted source candidate (unchanged) | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Run-kit D remote extraction path | `/home/gatea/gatea-run-kit-20260808D-2ce41e34` |
| Preregistration (Lead-accepted) | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` |
| Last completed gate state before this unit | **A-0 · A-1 · A-2 · A-3 · A-4 PASS · A-5..A-9 NOT RUN** |

---

## 2. Independent preflight PASS immediately before A-5

Read-only preflight against the staging host immediately before invoking A-5 — every item PASS:

- **Evidence log absent** before invocation (no pre-existing `/home/gatea/gatea-A5-20260808D.log`).
- **Script integrity:** `gatea_A5.sh: OK` against `SHA256SUMS` (run-kit D member, byte-identical to
  the accepted/verified kit).
- **Service / unit:** `active` and `static`; `Restart=no`; `MainPID=183225`; `NRestarts=0`;
  `Result=success`; `ExecMainStatus=0`.
- **Listener:** exactly `127.0.0.1:8790` (loopback only; no non-loopback listener).
- **API `GET /api/status` → HTTP 200:** exact credential-free **DISARMED**; mode
  `credential_free_disarmed`; `state_version=1`; `network`/`exchange_conn`/`credential_lookup`
  disabled; `exchange_enabled=false`; `arm_enabled=false`.
- **DB:** `PRAGMA quick_check=ok`; `app_state=DISARMED`; `schema_version=4`.

This is the A-4-prerequisite state (DISARMED, active/static, loopback-only, no broker/credentials)
carried into A-5 unchanged.

---

## 3. Exact invocation and result

| Item | Value |
|---|---|
| Invocation | `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh` |
| Route | the preregistered key-only SSH route to `gatea-staging` |
| Remote/SSH exit code | `1` |
| Elapsed | about `4.7 s` |

A-5 ran exactly once, from the verified run-kit D extraction path, over the preregistered key-only
SSH route. It returned a genuine nonzero (`1`) exit.

---

## 4. Evidence log identity (remote + local preserved copy)

| Item | Value |
|---|---|
| Remote evidence log | `/home/gatea/gatea-A5-20260808D.log` |
| Local preserved copy | `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log` |
| SHA-256 (remote **and** local — identical) | `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9` |
| Bytes | `1933` |
| Remote file metadata | mode `664`, owner `gatea`, group `gatea` |

The remote and local copies are byte-identical (same SHA-256, same size). The run-kit refuses to
overwrite a pre-existing evidence log; this log was newly written by the single A-5 run and is
preserved as-is. **Never overwrite or reuse `/home/gatea/gatea-A5-20260808D.log`.**

---

## 5. A-5 script evidence before failure (in script order)

Every A-5 pre-assertion and intermediate proof recorded by the script **passed** before the failing
post-start listener check:

- **Pre service state:** `ActiveState=active`; `Restart=no`; `MainPID=183225`; `NRestarts=0`.
- **Pre listener check:** listener count `1`, loopback-only — **PASS**.
- **Pre API check:** exact credential-free DISARMED — **PASS**.
- **Pre DB check:** `quick_check=ok`; `app_state=DISARMED`; `schema_version=4`; table counts
  `bars=0, decisions=0, directives=0, equity=0, events=0, fills=0, llm_calls=0, meta=2,
  order_identity=0, orders=0, risk_days=0, runs=0, signal_fingerprints=0, submission_attempts=0,
  submission_recovery_evidence=0, trades=0`.
- **SIGKILL action:** the frozen, authorized unclean-kill command
  `sudo systemctl kill --kill-whom=main --signal=SIGKILL mtc-bridge-first-start.service`.
- **Dead-window proof PASSED:** `MainPID=0`; the old PID (`183225`) gone; 3-second wait complete;
  `ActiveState=failed`; no listener; `NRestarts` remained `0`; `Result=signal`;
  `ExecMainStatus=9`.
- **Restart:** exactly one explicit `reset-failed` + `start` was performed (the runbook-authorized
  one-time restart, not auto-restart).
- **Post service state:** `MainPID=187338`; `NRestarts=0`; `Restart=no`.

### The failure (exact failure line)

Immediately after the single `start`, the post-start listener check saw **`listener_count=0`**. The
script then printed:

```
RESULT=FAIL
A5_FAIL reason=post listener not loopback-only
```

and the `EXIT` trap recorded **`rc=1`**. The assertion fired because the loopback listener was not
yet bound at the instant the script checked it — the application had not finished startup — even
though systemd had already reported the unit active.

---

## 6. Independent post-failure verification — safe-state proof (PASS)

A read-only independent verification performed a few seconds after the failure confirmed the staging
state is safe and consistent. Every item PASS:

- **Unit:** loaded/static; `active`/`running`; `MainPID=187338`; `Restart=no`; `NRestarts=0`;
  `Result=success`; `ExecMainCode=0`; `ExecMainStatus=0`.
- **Listener:** count `1`; exact address `127.0.0.1:8790`; non-loopback count `0`.
- **API `GET /api/status`:** exact credential-free DISARMED with the **same `state_version=1`** and
  the same disabled fields (`network`/`exchange_conn`/`credential_lookup` disabled;
  `exchange_enabled=false`; `arm_enabled=false`).
- **DB:** `quick_check=ok`; `app_state=DISARMED`; `schema_version=4`; the **exact same table counts**
  as preflight (`bars=0, decisions=0, … meta=2, … trades=0`).
- **Recorded verdict line:** `POSTFAIL_SAFE_STATE=PASS`.

### Safe-state conclusion → conditional stop/mask was not required

Because the staging state was independently proven safe, active, loopback-only, credential-free
DISARMED, and DB-consistent (counts unchanged from preflight, `state_version=1`, `Result=success`,
no non-loopback listener), the conditional stop/mask response of the preregistered first-FAIL runbook
(`GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §5) was **not required and was not performed**. No ARM,
no credentials, no broker/exchange, no orders, no TESTNET/mainnet, no wallet, no master merge, and no
economic action occurred.

---

## 7. Required classification — verdict recorded honestly

| Gate | Status |
|---|---|
| A-0 · A-1 · A-2 · A-3 · A-4 | **PASS** |
| **A-5** | **FAIL** — frozen script failed its post-listener assertion immediately after start |
| A-6 · A-7 · A-8 · A-9 | **NOT RUN** (first-FAIL rule; each presupposes an A-5-passed service) |

- The frozen A-5 script **failed its post-listener assertion**, so it **cannot be promoted to PASS**
  from the later safe-state diagnostics. The post-failure PASS in §6 proves staging is safe; it does
  **not** change the A-5 verdict.
- This is a **script/run-kit runtime-evidence failure**, not a product acceptance change. Candidate
  `2ce41e34…` remains accepted; A-0..A-4 PASS remain the last completed gates.

---

## 8. Lead diagnosis — reproduced run-kit readiness-race defect

**Lead diagnosis: reproduced run-kit readiness-race defect.** The script's `wait_active` returned as
soon as systemd reported the unit `active`, then it immediately performed the post-start listener
assertion. The service completed startup (bound `127.0.0.1:8790`) moments later — confirmed by the
independent post-failure check in §6, which found the listener present, `Result=success`, and the
exact same credential-free DISARMED state/counts.

- This is evidence that **the run-kit lacks a bounded application-readiness wait after the explicit
  `start`** (it gates on systemd-active, not on listener-up + API-DISARMED).
- It is **not** evidence of a product persistence/DISARMED invariant failure: the persisted store
  stayed `DISARMED` / `schema_version=4` with unchanged counts, `state_version` stayed `1`, the unit
  reached `Result=success`, and the listener came up loopback-only.
- The frozen run-kit D and its evidence are **preserved unchanged**; never overwrite or reuse
  `/home/gatea/gatea-A5-20260808D.log`.

---

## 9. Next steps contract — protected run-kit repair

1. **`[AI: Claude]` Repair the A-5 runtime-evidence defect in a new run-kit revision.** Do **not**
   mutate the preserved remote D kit/log. Add a bounded post-start readiness wait that requires
   **systemd active** **plus** a loopback listener **plus** the exact credential-free DISARMED API
   before the final assertions.
2. **Apply D026** (`AGENTS.md`): demonstrate **RED** against the exact readiness-race behavior (or an
   equivalent deliberate falsification/mutation), then **GREEN** with the fix; record the commands and
   their real output.
3. **Independent audit** of the actual repair and protected surface under the canonical roster / Lead
   acceptance rules. This is a **new runtime-defect repair unit**; do **not** treat the prior three
   source-review rounds as evidence that this runtime defect was tested.
4. **Preregister / package / transfer a new revision** with a new evidence-log identifier (for example
   revision **E**); verify hashes/bytes/LF/member set before any rerun. **Do not overwrite D evidence.**
5. **Rerun A-5 only after** the repaired revision is accepted and staged. **Stop again on any genuine
   FAIL.** **A-6 remains blocked** until A-5 passes and `_AI_MEMORY` is updated.

Hard exclusions unchanged: no credential value, broker/exchange access, successful ARM, orders,
TESTNET/mainnet, wallet, master merge, or economic action.

---

## 10. Reproduction / orientation (another lead, without trusting the handoff)

**Companion records (read order):**

- `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` — exact paths, per-gate criteria, shared
  script contract, **§5 first-FAIL response**, GLM routing record, Lead correction/repair tables.
- `11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md` — run-kit D package/transfer/verify
  (the frozen kit A-5 ran from); accepted tar SHA-256
  `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, `71680` bytes.
- `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt` — invocation, validation, execution order,
  evidence-log hashing.
- `11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md` — A-4 PASS (the prerequisite state A-5 inherited).
- `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`,
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` — live state (newest section first).

**Re-hash the evidence log (read-only) to confirm identity:**

- Remote `/home/gatea/gatea-A5-20260808D.log` and local
  `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log`: both SHA-256
  `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes.

**Verify the run-kit D member A-5 ran from (read-only on the kit):** against
`/home/gatea/gatea-run-kit-20260808D-2ce41e34/` — `sha256sum -c SHA256SUMS` (all OK, incl.
`gatea_A5.sh`); `bash -n gatea_A5.sh`; expect the byte/LF counts in the package-transfer record
(A5 `9719`/`261`).

---

## 11. Scope, safety, and routing

- **Documentation only.** GLM-5.2 edited only the four task-named files (this report plus the three
  memory/handoff prepends). No source, tests, scripts, manifests, credentials, trading/Pine/parity/
  MTC logic, or any other file changed.
- **No Git/SSH/service/test/build/deploy/source-repair action was executed by this documentation
  unit.** The A-5 staging execution and read-only diagnostics recorded were authorized Lead staging
  actions performed under the preregistered sequence; the worker recorded rather than performed or
  mutated them.
- **Routing (per `AGENTS.md` §GLM SUPPLEMENTAL ROUTING):** Tier 4 — protected Gate-A evidence tooling
  + docs; GLM-5.2 via Z.AI Coding Plan (owner exact-model request + protected safety-evidence
  surface). No external API credits; no fallback/downgrade. GLM does not replace the mandatory audit
  roster; this is documentation/tooling, not a Gate-5 audit.
- **Hard exclusions unchanged:** no credential value, broker/exchange access, successful ARM, order,
  TESTNET/mainnet, wallet, master merge, or economic action. The service intentionally remains
  active/static, loopback-only, credential-free DISARMED, `state_version=1`, no broker/credentials.
