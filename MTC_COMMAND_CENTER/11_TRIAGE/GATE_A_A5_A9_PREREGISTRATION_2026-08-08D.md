# GATE A — A-5..A-9 PREREGISTRATION (run-kit D, 2026-08-08)

> **STATUS: NOT RUN.** This preregistration freezes the A-5..A-9 command/evidence plan and
> the run-kit D *source* only. It has **not** been packaged, transferred, or executed.
> **A-5..A-9 are NOT RUN.** No gate result is claimed. This document does not authorize
> execution; Gate A staging action awaits the owner's existing preregistered authorization
> and the Lead's independent script validation, packaging, transfer, and verification.

Candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b` (credential-free DISARMED; A-0..A-4 PASS).
This is a bounded GLM-5.2 documentation/tooling checkpoint. It edits only the files named in
the task (the preregistration doc, the run-kit D members, and the three memory/handoff
prepends). No product code or product artifact changed; no install mutation, credential,
broker/exchange access, successful ARM, order, TESTNET/mainnet, wallet, master merge, or
economic action is authorized or occurred. The Lead's real source review of the first patch is
authoritative over the implementer's older records-branch source read; it found and repaired
binding defects (see §9). STATUS remains NOT RUN — the kit is still not packaged, transferred,
or executed, and the repaired bindings await the Lead's re-audit.

## 1. Exact paths (frozen)

| Item | Value |
|---|---|
| Release SHA | `2ce41e34bceb599d80af24c5c33d835820ec321b` |
| Release app root | `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE` |
| A-9 release scan root | `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` |
| venv Python (`PY`) | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python` |
| systemd unit | `mtc-bridge-first-start.service` |
| State DB | `/var/lib/mtc-bridge/bridge.db` |
| API | `127.0.0.1:8790` (`GET /api/status` only; **never** `POST /api/arm` in this kit) |
| Env file | `/etc/mtc-bridge/mtc-bridge.env` (**never** print its contents) |
| Staging VM IP (A-8 host) | `172.24.55.233` |
| Remote evidence logs | `/home/gatea/gatea-A{5,6,7,8,9}-20260808D.log` |
| Host evidence log (A-8) | `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log` |
| Run-kit D dir | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/` |

## 2. Per-gate criteria (pre-registered, do not improvise)

**A-5 — unclean SIGKILL / manual-restart consistency.** Preconditions: unit active/running,
`Restart=no`, `MainPID>0`, captured `NRestarts`, listener exactly loopback, `GET /api/status`
exact credential-free DISARMED (`state=DISARMED`, `mode=credential_free_disarmed`,
network/exchange_conn/credential_lookup disabled, `exchange_enabled=false`,
`arm_enabled=false`, `state_version=1`), and a read-only **logical** DB snapshot
(`quick_check=ok`, `app_state=DISARMED`, `schema_version=4`, sorted per-table counts).
SIGKILL the main process with the exact Ubuntu option
`sudo systemctl kill --kill-whom=main --signal=SIGKILL $UNIT`. Bounded-wait the old
`/proc/PID` gone and `MainPID=0`; sleep 3s; require `ActiveState` failed/inactive, **no**
`:8790` listener, `NRestarts` unchanged, `Result=signal`, `ExecMainStatus=9` (proves no
auto-restart before explicit action). Then `reset-failed` + exactly one `start`; bounded-wait
active; require a new positive `MainPID` that differs, `NRestarts` unchanged, `Restart=no`,
loopback-only listener, identical API state, and a **byte-identical** recomputed logical DB
snapshot (quick_check/meta/schema included). **Does NOT** POST `/api/arm`; **does not** read
the env file.

**A-6 — empty-startup reconcile dry-run.** Production service/PID/API credential-free DISARMED
before and after, unchanged. `cd` the release; `mktemp -d /home/gatea/gatea-A6-temp.XXXXXX`
(trap cleanup). Embedded venv Python builds an in-process app via
`create_app(..., start_mode='credentialed', broker=MockBroker(bars=[]))` (the installed
candidate supports the kwarg and the injected MockBroker blocks `_build_broker`), so no
credential resolver/network path runs; `await
asyncio.wait_for(engine.start(lookback=0), timeout=30)` with `await engine.stop()` always in
`finally`. Require `state=DISARMED`, `reconcile_ready=true`, `reconcile_error=null`,
`deferred_event_queue_depth=0`, `len(_queued_events)=0`, mock `connected=true`,
orders/fills empty, position `None`; require the temp DB `quick_check=ok`,
`app_state=DISARMED`, `schema_version=4`. Recorded **honestly**: an empty broker proves no
raise/hang/leftover queue on empty startup — **not** queue-drain-under-load; no full-reconcile
requirement because baseline schema 4 intentionally disables it.

**A-7 — read-only status / persisted-state / log evidence.** `GET /api/status` 200 parsed by
Python; exact credential-free DISARMED fields; reported `state` **equals** the DB `app_state`;
DB `quick_check=ok`, `schema_version=4`. Require the documented `/var/log/mtc-bridge/bridge.log`
and `bridge.err.log` are regular files and currently nonempty; record bytes, mode,
owner/group, SHA-256. Require the journal query succeeds and record a bounded line count + tail
with **no credential grep**. `/api/health` is **not** probed (route absent). `reconcile_ready`
is **not** required true (a credential-free service correctly reports it false).

**A-8 — loopback binding proof (two-part gate; neither alone passes).** *Remote* enumerates
the local-address column of every `ss -H -ltn 'sport = :8790'` line and requires a nonempty
set where every address is loopback (`127.0.0.1:8790` or IPv6 loopback form); wildcard, the VM
IP, or any non-loopback fails; records `ip -brief address` and `ufw status verbose` read-only.
*Host* runs bounded `TcpClient.ConnectAsync` probes from the Windows host (fixed VM IP
`172.24.55.233`): **port 22 must succeed** (reachability control) and **port 8790 must fail**;
prints booleans/errors only and exits nonzero (`A8_HOST_FAIL`) unless port 22 succeeds and 8790
fails (else it prints exactly `A8_HOST_PASS` and exits 0). A-8 PASS = remote ends `A-8 PASS` **and** host shows
`port22_ok=True` **and** `port8790_ok=False`.

**A-9 — content-redacted secret scan.** Recursive scan of **exactly**
`/opt/mtc-bridge/releases/<SHA>` and `/etc/mtc-bridge` (not the venv, not `/home/gatea`) using
`sudo grep -RIlE --binary-files=without-match` so only file **paths** ever print (never matched
text). For each of nine categories the grep rc is captured separately: rc 0/1 allowed (0 =
match, 1 = none); rc > 1 (grep error) fails the script. Output is category count + matched
paths only. The scan necessarily reads bytes under those trees (including the root-readable env
file), but no value or matched text is ever printed, copied, or persisted; patterns are passed
as `grep ... -e <ERE> -- <paths>` so a leading-dash ERE is never parsed as an option. The nine
category tokens (in order): `private_key_block`, `aws_access_key`, `github_token`,
`slack_token`, `openai_token`, `anthropic_token`, `xai_token`, `telegram_bot_token`,
`ethereum_private_key`. **Any hit is FAIL/BLOCK, never auto-dismissed** (Lead adjudicates). Nine EREs:
private-key block `-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----`; AWS
`AKIA[0-9A-Z]{16}`; GitHub `(gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{50,255})`;
Slack `xox[baprs]-[A-Za-z0-9-]{20,}`; OpenAI `sk-(proj|svcacct)-[A-Za-z0-9_-]{20,}`; Anthropic
`sk-ant-[A-Za-z0-9_-]{20,}`; xAI `xai-[A-Za-z0-9_-]{20,}`; Telegram
`[0-9]{8,10}:[A-Za-z0-9_-]{35}`; Ethereum `0x[0-9a-fA-F]{64}`.

## 3. Shared script contract

Each Bash script: `set -Eeuo pipefail`; fixed evidence log under `/home/gatea`; refuses to
overwrite an existing log (exit 2); redirects stdout+stderr to the log; `EXIT` trap records the
exact rc; uses the installed venv Python for all JSON/SQLite work (**never** assumes the
`sqlite3` CLI); outputs structured `key=value` evidence; ends with exactly `A-<n> PASS` only if
all assertions hold; never hashes its own still-open log from inside itself; no writes outside
`/home/gatea` except the runbook-authorized service/DB state caused by the A-5 SIGKILL + one
explicit start; never `POST /api/arm`; A-5/A-6/A-7/A-8 never read the env file, while A-9
scans bytes under the release + `/etc/mtc-bridge` (which includes the root-readable env file)
via `grep -l` — paths only, and no value or matched text is printed, copied, or persisted
(category counts + paths only). First genuine FAIL stops; the script performs no
auto-restart/mask on its own failure.

## 4. Local validation, packaging, transfer, order (Lead-owned)

Before A-5, the Lead must: independently validate the scripts (`bash -n` for each `.sh`,
PowerShell parser for `gatea_A8_host.ps1`, CR-byte check = 0 for every kit file); create the
manifest (`SHA256SUMS`) and tar; transfer to `/home/gatea` and verify exact tar SHA-256/bytes,
the exact member set, `sha256sum -c` all OK, and the five on-host `bash -n` checks. Run
strictly **A-5 → A-6 → A-7 → A-8 (remote + host) → A-9**, stopping at the first FAIL. After
every gate PASS, update `_AI_MEMORY` (`NEXT_STEPS.md`, `GLOBAL_HANDOFF.md`) and
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` **before** the next gate. Evidence-log SHA-256 +
sizes are captured post-run (the scripts never hash their own open logs). Full operational
detail is in `GATE_A_RUN_KIT_D_2026-08-08/README.txt`.

## 5. First-FAIL response

At the first genuine FAIL: preserve the evidence log; run only read-only diagnostics as needed;
then STOP. If the failure leaves the service in an unsafe state, safe-stop and mask the unit
(`sudo systemctl stop mtc-bridge-first-start.service` then
`sudo systemctl mask mtc-bridge-first-start.service`) and write the result + memory. A script's
own internal failure triggers **no** auto-restart/mask; the Lead handles the safe first-FAIL
response. (Scripts may legitimately need a one-time `reset-failed` + `start` — that is A-5's
runbook-authorized restart, not an auto-restart.)

## 6. GLM routing record (per AGENTS.md §GLM SUPPLEMENTAL ROUTING)

```
Classification      : Tier 4 — protected Gate-A restart/persistence/reconcile evidence tooling + docs
Protected           : yes — scripts exercise a DISARMED staging service; they change no product code
Model + provider    : GLM-5.2 via Z.AI Coding Plan
Cheaper-model rationale : owner exact-model request (GLM-5.2) + protected safety-evidence surface
Exact paths         : MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md;
                      MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/{README.txt,gatea_A5.sh,
                      gatea_A6.sh,gatea_A7.sh,gatea_A8.sh,gatea_A8_host.ps1,gatea_A9.sh};
                      _AI_MEMORY/{NEXT_STEPS.md,GLOBAL_HANDOFF.md};
                      11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md
Context/tool budget : single bounded documentation/tooling task; targeted reads only
Fallback            : none — exact-model request; no silent downgrade
External API credits: no
```

GLM never replaces the mandatory audit roster; this is implementation/tooling, not a Gate-5
audit. No external API credits; no fallback/downgrade.

## 7. GLM read-only proposal report (Lead-accepted architecture)

- Report: `C:\WPI_ARTIFACTS\glm-a5a9-prereg-report-20260808C.md`
- SHA-256: `2ad0f42355769a3463d5c737e57a482e6873d084635b66b7575ae7a146d35792`
- Lead accepted the architecture. Specific assumptions were rejected/corrected before freeze
  (table below).

## 8. Lead correction table (proposal → frozen)

| # | Proposal assumption (rejected/corrected) | Frozen correction in run-kit D |
|---|---|---|
| 1 | Relied on the `sqlite3` CLI being present | All SQLite work via the installed **venv Python** (`sqlite3` module); never assume the CLI |
| 2 | Whitespace grep over raw `/api/status` JSON | Parse the JSON with **Python**; emit/assert `key=value` |
| 3 | A-5 POSTs `/api/arm` (redundant) | A-5 **never** POSTs `/api/arm` (restart-consistency test, not an arm test) |
| 4 | Wrong kill option spelling `--kill-who` | Exact Ubuntu option `systemctl kill --kill-whom=main --signal=SIGKILL $UNIT` |
| 5 | Writes under `/tmp` | Writes only under `/home/gatea` (evidence log + A-6 temp dir) |
| 6 | Unqualified log-size assumptions | Record actual bytes/mode/owner/group/SHA-256 of the log files |

## 9. Lead-audit repair notes (run-kit D source review — Lead verification authoritative)

The Lead's real source review of the first GLM-5.2 patch found binding defects in the run-kit D
**source**; all were repaired in this round. The Lead review is authoritative over the
implementer's older records-branch source read (the installed candidate at the release path in
§1 is the authoritative API surface for this gate). STATUS is unchanged: **A-5..A-9 are NOT RUN;
the kit is NOT packaged, transferred, or executed.** The repaired bindings await the Lead's
re-audit; no gate result is claimed.

| # | Defect (first patch) | Repair applied to the FROZEN SOURCE |
|---|----------------------|--------------------------------------|
| R1 | A-5 & A-8 parsed the `ss -H -ltn` PEER column (index 4) instead of LOCAL (index 3) — a repeat of the A-4 peer-column false negative | Collect the LOCAL addr at **index 3**; require `>= 5` fields; comment states index 3 = local and index 4/peer is forbidden; all-listeners/nonloopback assertions kept |
| R2 | A-6 claimed `create_app` has **no** `start_mode` kwarg (older records-branch read) | Installed candidate IS authoritative — `create_app(..., start_mode='credentialed')` restored explicitly; all "unsupported" claims removed; MockBroker blocks `_build_broker`/credential resolution/network |
| R3 | A-6 printed `RESULT=FAIL` but exited 0, letting Bash reach `A-6 PASS` (false PASS) | Timeout / any start exception / failed assertion / any stop exception now all exit nonzero; `try/finally` always attempts `engine.stop()` after start begins; requires `engine.status()['deferred_event_queue_depth'] == 0` AND `len(order_manager._queued_events) == 0` |
| R4 | A-6 used unguarded `rm -rf "$TMP"` in the EXIT trap | Validates the exact `/home/gatea/gatea-A6-temp.` prefix + is a directory + not a symlink; deletes only maxdepth-1 `*.db` regular files then `rmdir`; logs and returns nonzero on validation/cleanup failure; preserves rc otherwise |
| R5 | `gatea_A8_host.ps1` exited 0 even when port 22 failed or 8790 succeeded | After evidence write/print: if `host_probe_ok` is false prints `A8_HOST_FAIL` and `exit 1`, otherwise prints exactly `A8_HOST_PASS` and `exit 0` |
| R6 | A-9 first ERE begins with `-`; `grep "$ere"` could parse it as an option | `grep -RIlE --binary-files=without-match -e "$ere" -- "$REL" "$ETC"` (retains `-RIlE --binary-files=without-match`) |
| R7 | A-9 category tokens were short labels | Canonical names in order: `private_key_block`, `aws_access_key`, `github_token`, `slack_token`, `openai_token`, `anthropic_token`, `xai_token`, `telegram_bot_token`, `ethereum_private_key` (exactly nine counts) |
| R8 | A-9 docs falsely claimed the env file is "not read" | Truthful: A-9 reads bytes incl. the root-readable env file, but `grep -l` emits paths only — no value/matched text printed, copied, or persisted; only category counts + paths. (A-5/A-6/A-7/A-8 still do not read the env file.) |

**Lead evidence already supplied (syntax/byte checks only — not gate execution):** `bash -n` on
all five Bash scripts returns rc 0; the PowerShell parser for `gatea_A8_host.ps1` reports 0
errors; CR-byte count is 0 for every new kit/preregistration file. The repaired bindings
themselves await the Lead's re-audit; the worker has not executed the gates and claims no result.

## 10. Authorization boundary & hard exclusions

Existing owner authorization covers the preregistered A-5..A-9 sequence only. Hard exclusions
unchanged: no credential value, broker/exchange access, successful ARM, order, TESTNET/mainnet,
wallet, master merge, or economic action. The service intentionally remains active/static,
loopback-only, credential-free DISARMED (`state_version=1`), no broker connection, no
credentials — the prerequisite for A-5. No product/artifact change; no gate result; no
prohibited action.

## 11. Records (companion, read order)

- `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt` — invocation, validation, transfer, order, post-run hashes.
- `11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md` — A-4 seven-condition standard (§D.4) and rebaselined inputs.
- `11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md` — A-4 PASS (prerequisite state for A-5).
- `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`, `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` — live state (newest section first).

## 12. Lead-audit repair round 2 notes (run-kit D A-6 source review — Lead verification authoritative)

A focused follow-up repaired **exactly the three remaining REQUIRED A-6 defects** found by the
round-1 re-audit, all in `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A6.sh` ONLY. `gatea_A5.sh`,
`gatea_A7.sh`, `gatea_A8.sh`, `gatea_A8_host.ps1`, and `gatea_A9.sh` are **unchanged**. Only the
task-named files were edited: `gatea_A6.sh` + `README.txt`, this preregistration doc (this §12), and
the three memory/handoff prepends. The Lead review remains authoritative over the implementer's
older records-branch source read. STATUS is unchanged: **A-5..A-9 are NOT RUN; the kit is NOT
packaged, transferred, or executed.** The round-2 bindings await the Lead's final re-audit; no gate
result is claimed, and worker validation beyond the provided Lead evidence is not claimed.

| # | Defect (round-1 re-audit) | Repair applied to `gatea_A6.sh` (frozen source) |
|---|---------------------------|--------------------------------------------------|
| R9 | Partial-start cleanup: `started=True` was assigned only AFTER `engine.start()` returned, so a timeout/exception that created tasks left `started=False` and `finally` skipped `engine.stop()` | A `stop_required` flag is set immediately BEFORE invoking `engine.start()`; the `finally` block always attempts `await engine.stop()` whenever start was invoked (including after a timeout or a start exception). A stop exception keeps the exit nonzero; when start already failed, the original start exception is preserved (the stop exception raised in `finally` is caught/recorded, not re-raised, and no `RESULT=PASS` is printed) so a stop failure never synthesizes success |
| R10 | SQLite sidecar cleanup: deleting only `*.db` did not match `bridge.db-wal` / `bridge.db-shm`, so a valid run could falsely fail at `rmdir` | After strict target validation — exact path regex `/home/gatea/gatea-A6-temp` + `.` + exactly six `[A-Za-z0-9]` chars, a real directory, NOT a symlink — delete ONLY maxdepth-1 regular files whose exact basenames are `bridge.db`, `bridge.db-wal`, or `bridge.db-shm`; then require no entries remain and `rmdir`. Never recursive deletion. An invalid target, a refusal, or cleanup residue forces a nonzero exit |
| R11 | Notifier/outbound hardening: the optional Telegram notifier could create an unrelated outbound path | Before `create_app`, six keys (`HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`, `MTC_BRIDGE_STATE_DB`) are popped from the isolated process environment WITHOUT reading or printing their values. Explicit `start_mode='credentialed'`, an explicit temp `store_path`, and an injected `MockBroker(bars=[])` are passed. `engine.notifier is None or engine.notifier.enabled is False` is required; only `notifier_disabled=true/false` is printed and it is bound into the PASS assertion. No environment value is printed |

No product code or product artifact changed; no install mutation, credential, broker/exchange
access, successful ARM, order, TESTNET/mainnet, wallet, master merge, or economic action is
authorized or occurred. The round-2 bindings await the Lead's final re-audit (`bash -n`,
PowerShell parser, CR-byte = 0, `git diff --check`) — the worker has not executed the gates and
claims no result.

## 13. Lead-audit repair round 3 notes (run-kit D A-6/A-7 source review — Lead verification authoritative)

The final focused repair round. Same worktree and unit as rounds 1-2. Only the task-named files
were edited: `gatea_A6.sh`, `gatea_A7.sh`, this preregistration doc (this §13), `README.txt`, and
the three top checkpoint sections (`_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`,
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`). No new files; no Git/SSH/staging/execution/product
edits; no credentials, ARM, orders, broker-network access, packaging, or transfer. The Lead review
remains authoritative over the implementer's older records-branch source read. STATUS is unchanged:
**A-5..A-9 are NOT RUN; the kit is NOT packaged, transferred, or executed.** The round-3 bindings
await the Lead's final acceptance; no gate result is claimed, and worker validation beyond the
provided Lead evidence is not claimed.

| # | Defect (round-2 re-audit) | Repair applied (frozen source) |
|---|---------------------------|--------------------------------|
| R12 | A-6 env keys were popped AFTER `from bridge.app import create_app`, so any module-level default app construction during import could see the parent process values | The six keys (`HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`, `MTC_BRIDGE_STATE_DB`) are popped via `os.environ.pop(_k, None)` BEFORE `from bridge.app import create_app` / `from bridge.broker.mock import MockBroker`. Required order: stdlib imports + release `sys.path`; the pop loop; only then the bridge imports; then explicit app construction. `os.environ.pop` removes and discards the process-local value; no value is printed, copied, persisted, or retained. It is not claimed the values are "never read"; Gate-A preconditions already established the keys absent, so clearing is defense in depth. The env FILE (`/etc/mtc-bridge/mtc-bridge.env`) is not opened by A6 |
| R13 | A-6 wording claimed the env values are "never read" / "not read" | Corrected wording everywhere in the edited top/current sections: `os.environ.pop` removes and discards process-local values; state that no value is printed, copied, persisted, or retained; Gate-A preconditions established the keys absent; clearing is defense in depth; the env FILE is not opened by A6. A-9 keeps its separate truthful statement that it scans bytes (incl. the env file) but emits paths/counts only |
| R14 | A-7 relied only on the logically-equivalent pair of DISARMED checks; it never explicitly asserted `db_app == api_state` | After separately validating the API state and the DB `app_state`, A-7 explicitly asserts and records `db_app == api_state` (explicit equality, not merely the two DISARMED checks). On mismatch it exits nonzero. All existing A-7 checks (API exact DISARMED; DB quick_check/schema/app_state; logs; journal) are preserved |

**Lead evidence already supplied (syntax/compile checks only — not gate execution; the worker
recorded it and did not run it):** `bash -n` on all five Bash scripts returns rc 0; the PowerShell
parser for `gatea_A8_host.ps1` reports 0 errors; `git diff --check` is clean; every embedded
Python heredoc compiled successfully (A-5 3 blocks, A-6 3, A-7 2, A-8 1). The round-2 lifecycle,
sidecar-cleanup, and notifier work is accepted. The round-3 bindings themselves await the Lead's
final acceptance; the worker claims no gate result.

No product code or product artifact changed; no install mutation, credential, broker/exchange
access, successful ARM, order, TESTNET/mainnet, wallet, master merge, or economic action is
authorized or occurred. The round-3 bindings await the Lead's final acceptance.

## 14. Final Lead acceptance

**Verdict: ACCEPT.** The third/final repair round was independently re-audited against the actual
files and accepted installed candidate. Evidence: all five Bash scripts pass `bash -n`; the A-8
PowerShell parser reports zero errors; all nine embedded Python heredocs compile (A-5: 3, A-6: 3,
A-7: 2, A-8: 1); `git diff --check` is clean; all seven kit members plus this preregistration file
have zero CR bytes. Required safety/evidence bindings were inspected line by line and reproduce.

This accepts only the frozen source/preregistration. **A-5..A-9 remain NOT RUN; the kit is not yet
packaged, transferred, or executed.** Next bounded unit is package + transfer verification only,
followed by an `_AI_MEMORY` checkpoint before A-5. First genuine FAIL still stops the sequence.
