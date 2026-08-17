# Gate A — A-4 PASS (run `C`, 2026-08-08) — `2ce41e34` — seven conditions evidenced

> **Lead verdict: Gate A A-4 PASS under Addendum D (§D.4 / §C.4).** Gate A is **IN PROGRESS through
> A-4**; **A-5–A-9 NOT RUN** (first-FAIL rule; each presupposes a running service). Candidate
> `2ce41e34bceb599d80af24c5c33d835820ec321b` and the product/artifact are **unchanged** by this unit. This
> is a bounded GLM-5.2 documentation checkpoint recording an already-executed, already-Lead-verified
> staging step; it is not an implementation or audit and does not alter candidate acceptance, the product
> bits, the artifact, D025 acceptance, or the repair-round count.

## Worker statement (accurate scope)

This checkpoint was authored by **GLM-5.2** and **only edits documentation** — the four files named in the
task (`GATE_A_A4_PASS_2026-08-08C.md` created; `NEXT_SESSION_HANDOFF_2026-08-08.md`,
`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md` updated). The A-4 staging execution and the
read-only on-disk diagnostics recorded here were **authorized staging actions performed earlier** under the
owner-approved preregistered `gatea-staging` rerun sequence, and their results were **Lead-verified before
this checkpoint**. **This is not "no staging action or diagnostic results occurred"** — they did occur,
within the authorized boundary; the GLM worker's role was to *record* them, not to perform or mutate them.
The GLM worker performed **no** staging action, script run, install, service mutation, credential access,
broker/exchange access, ARM, order, TESTNET/mainnet action, master merge, economic action, or Git mutation.

No product code or product artifact changed in this unit. No credentials, broker/exchange access,
successful ARM, orders, TESTNET/mainnet, master merge, or economic action is authorized or occurred. The
existing owner authorization covers only the preregistered A-5 through A-9 sequence; hard exclusions are
unchanged (credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge,
economic action).

## Main A-4 execution — run-kit C `gatea_A4.sh` under Addendum D

Transferred C script `gatea_A4.sh`, SHA-256
`78aa7fca7bfe7eb256a562d08d61e7d16b4ffcd3b164b89a5df420a01a8fd9b4` (byte-identical to the frozen run-kit C
member). Run on `gatea-staging`; main log `/home/gatea/gatea-A4-20260808C.log`, SHA-256
`19ed99773ca8dbfb84bfc6a93289daf4077419dd6d46c23343f5d4cfbf007c06`, `10152` bytes; script exit `0`, bound
to the step-8 refusal-probe exit `0`.

Recorded evidence, in script order:

- **Service start:** start exit `0`; unit reaches and stays **`active (running)`**, PID `183225`; the unit
  is `static` (started by the first-start path, not auto-enabled). Resolved running `Environment=` exactly
  includes `MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db` and
  `MTC_BRIDGE_START_MODE=credential_free_disarmed`; the env file remained empty / no credentials. (§D.5
  host evidence captured verbatim.)
- **Listener:** exactly local **`127.0.0.1:8790`**; no non-loopback listener.
- **GET `/api/status` → 200:** state `DISARMED`, mode `credential_free_disarmed`,
  `network`/`exchange_conn`/`credential_lookup` disabled, `exchange_enabled=false`, `arm_enabled=false`,
  `state_version=1`.
- **Fail-closed preconditions** all passed before any POST.
- **POST `/api/arm` with `X-Confirm: 1`** returned application HTTP **409**, exact body
  `ARM unavailable in credential-free DISARMED start mode; exchange access is disabled` — an
  **application-level refusal**, not `Errno 111 Connection refused`.
- **Post-refusal GET** remained identical `DISARMED`, `state_version` unchanged at `1`.
- **No broker attempt** in the journal, `/var/log/mtc-bridge/bridge.err.log`, or outbound service sockets.
  The error log contains only normal Uvicorn startup; SHA-256
  `179d162d67d0aa48e66fe51cb1ca7184bf6cff2d759ce74807417f27d71d0f24`, `199` bytes.

## Main-script evidence defect and Lead closure

The main script's **step 0 and step 10** each ran a nested `sudo bash -c '<sqlite …>'` command with
**shell-quoting syntax errors**, so those two on-disk (SQLite meta) reads could not be harvested by the
main script itself. This is a **run-script evidence-harvesting defect**, not a candidate/product defect;
the step-8 application refusal probe (the gate-critical check) and all other steps are unaffected, and the
main exit `0` is legitimately bound to the step-8 probe exit `0`.

Because of that quoting defect the Lead **did not accept A-4 from the main exit alone**. `dbdiag3`
closed the required post-attempt persisted-DB evidence. Separately, `postdiag2` closed the main script's
pre-POST timing gap by re-confirming listener/sockets/logs/environment/API after the refusal. The result
is A-4 PASS resting on the main log **plus** two canonical clean read-only diagnostics, not on the main
log alone.

## On-disk (read-only) diagnostic evidence — classification

All diagnostics are read-only (no service mutation, no credential access, no broker). Each helper-only
false-negative/noncanonical log is **preserved as evidence** (not deleted) alongside its canonical
replacement.

### DB diagnostics (persisted store)

| Log | SHA-256 | Bytes | Classification |
|---|---|---:|---|
| `/home/gatea/gatea-A4-dbdiag-20260808C.log` | `2c31405659ace6c2acb0d5f21e02fbd9761ecfefc9ad44a35d523664c686cf08` | 558 | **Non-accepting diagnostic** — read succeeded and showed `app_state=DISARMED` / schema `4` / `quick_check=ok`, but the helper falsely expected stale schema `2` and exited `1`. Preserved. |
| `/home/gatea/gatea-A4-dbdiag2-20260808C.log` | `b4488d46559610c532e93b044fbb3073905fc330f102e1fe2b3aae502a411341` | 497 | **Noncanonical** — logic correctly accepted schema `4` and exited `0`, but the human PASS line still said schema `2`. Preserved. |
| `/home/gatea/gatea-A4-dbdiag3-20260808C.log` | `530f846c7fc2f4f50de6a13eecd2274726b32947082dfcbf9ffaa12baef8a5c8` | 497 | **Canonical clean DB log** — active; WAL/SHM present; meta exactly `app_state=DISARMED` / `schema_version=4`; `PRAGMA quick_check=ok`; PASS; rc `0`. |

Canonical DB script SHA `ca9cef4a50bf7e95e746b7749093263710213ab7b1e4256e3645632df7e15756`; runner
`7bbafaf8500d10151af2cd8ba9f5c4634c5fb9953da4c193c691aca10f9f5740`; `bash -n` rc `0`, `0` CR bytes.

### Post-refusal diagnostics (listener/sockets/env/API re-confirmation)

| Log | SHA-256 | Bytes | Classification |
|---|---|---:|---|
| `/home/gatea/gatea-A4-postdiag-20260808C.log` | `043d59017eea1887943ce41bfbdb45d17a1d83bd6a2a806df411433d6f39bfb6` | 1079 | **Non-accepting helper** — falsely treated the `ss` peer column `0.0.0.0:*` as local exposure and exited `1`. Preserved. |
| `/home/gatea/gatea-A4-postdiag2-20260808C.log` | `ed06554cf93951921b15d378b9c2ac01f019c7c58815942cdf561e5168672183` | 1111 | **Canonical clean post log** — active; running env exact; local-address column exactly `127.0.0.1:8790`; journal/errlog/outbound broker hits all `0`; API exact credential-free `DISARMED`, `state_version=1`; failures `0`, rc `0`. |

Canonical post script SHA `bfb98af1214ef39091827b57919545620e0bde5923d12ba67ea20d842e1e2608`; runner
`f45c32839f4b7f6533e916fd8f202d686bd045f6053425af898b586c1c6f7a98`; `bash -n` rc `0`, `0` CR bytes.

## Seven-condition → evidence map (Addendum D §D.4 / §C.4)

| # | Condition | Primary evidence | Canonical read-only corroboration |
|---|---|---|---|
| 1 | Unit reaches and stays `active (running)` | Main log: start exit `0`, active/running PID `183225`, unit static | postdiag2: active |
| 2 | Listener on `127.0.0.1:8790` only | Main log: exactly local `127.0.0.1:8790`, no non-loopback listener | postdiag2: local-address column exactly `127.0.0.1:8790` (first postdiag `0.0.0.0:*` false negative superseded) |
| 3 | `GET /api/status` durably non-`ARMED` | Main log: state `DISARMED`, mode `credential_free_disarmed`, all conn/exchange flags disabled/false, `state_version=1`; post GET identical | postdiag2: API exact credential-free `DISARMED`, `state_version=1` |
| 4 | `POST /api/arm` refused by the **application** (connection-refused does **not** count) | Main log: all fail-closed preconditions passed; POST `X-Confirm: 1` → HTTP `409`, exact body `ARM unavailable in credential-free DISARMED start mode; exchange access is disabled`; main exit `0` bound to step-8 probe exit `0` | (gate-critical step; corroborated by unchanged post GET) |
| 5 | No broker connection attempted | Main log: no broker in journal / `bridge.err.log` (startup only, 199 B) / outbound sockets | postdiag2: journal/errlog/outbound broker hits all `0` |
| 6 | Persisted store `app_state=DISARMED`, state version unchanged | Main log: pre/post GET `state_version=1` unchanged | dbdiag3: meta exactly `app_state=DISARMED` / `schema_version=4`, `PRAGMA quick_check=ok`, PASS, rc `0` (dbdiag stale-schema and dbdiag2 cosmetic superseded) |
| 7 | Run records the actually-selected start mode | Main log: resolved `Environment=` includes `MTC_BRIDGE_START_MODE=credential_free_disarmed` and `MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db`; env file empty | postdiag2: running env exact |

All seven conditions hold, each with primary evidence plus an independent read-only confirmation where
applicable.

## Why the helper defects do not weaken the product verdict

- Every defect is in a **run-script evidence harvester** (the main script's two nested `sudo bash -c`
  SQLite quoting calls; the dbdiag stale-schema expectation; the dbdiag2 cosmetic PASS label; the postdiag
  `ss` peer-column misread) — **none** is a candidate/product behavior defect. The candidate bits, the
  service behavior, and the persisted store are observed identically across the main log and **both**
  canonical diagnostics.
- The main exit `0` is bound to the **step-8 application refusal probe** exit `0`, which is the
  gate-critical check and is unaffected by the SQLite quoting bug. The Lead therefore did not accept on the
  main exit alone; it accepted on the main log **plus** the two canonical clean read-only logs.
- **No criterion went unobtained.** Each missing or false-negative helper check was reproduced
  independently and replaced by a clean read-only canonical log with corrected logic and rc `0`: the
  persisted-store facts are closed by `dbdiag3`, and the post-refusal listener/socket/env/API facts are
  closed by `postdiag2`. The non-accepting/noncanonical logs are preserved as evidence of the defect and
  its closure, not concealed.
- Net effect: the helper scripts were weak; the **product** is consistently corroborated as
  credential-free `DISARMED`, schema `4`, `state_version=1`, `127.0.0.1:8790` only, no broker attempt,
  and exact application-level `409` refusal. The defects weaken the helpers, not the verdict.

## Current state and authorization boundary

The service **intentionally remains active/static**, loopback-only, credential-free `DISARMED`,
`state_version=1`, with no broker connection and no credentials. This is the **prerequisite for the A-5
unclean-restart test** and is left in place deliberately; it is not a leak.

Existing authorization covers the **preregistered A-5 through A-9 only**. Hard exclusions unchanged:
credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, economic
action. No pytest rerun; no product/artifact change; candidate `2ce41e34` accepted, Gate A IN PROGRESS
through A-4.

## Next steps

1. **[AI: Claude]** Before executing A-5, recover the exact A-5–A-9 commands from the canonical runbook and
   addenda and preregister a bounded command/evidence plan. Do not improvise protected tests.
2. **[AI: Claude]** Execute **A-5 first** (unclean kill/restart; state/DB consistency / `DISARMED`); stop at
   first FAIL. On failure preserve evidence, stop+mask the service safely, and write result/memory. On PASS
   update `_AI_MEMORY` before A-6.
3. **[AI: Any]** Preserve the old `GATE_A_RESULT_2026-08-08.md`; the final rerun record will be
   `GATE_A_RESULT_2026-08-08B.md`.

## Records

Companion records, in read order: `11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md` (A-4
seven-condition standard, §D.4); `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08C.md` (run-kit C and the
A-0–A-3 rerun checkpoint through this unit); `_AI_MEMORY/GLOBAL_HANDOFF.md` and
`_AI_MEMORY/NEXT_STEPS.md` (live state, newest section first); `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`
(newest checkpoint block).
