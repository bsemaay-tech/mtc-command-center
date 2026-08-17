# KVM2 deployment EXECUTED — first DISARMED start LIVE — 2026-08-17

Status: **DEPLOYED AND RUNNING DISARMED.** Executed overnight under the
owner's signed V6 §3 sentence + overnight completion authorization
(`OWNER_AUTHORIZATION_INSTALL_2026-08-16.md`, all sections). Every stage
below quotes real observed output committed in this record.

## What is running

| Item | Value |
|---|---|
| Host | `srv1856225` (Hostinger KVM2, `152.239.123.231`) |
| Release | `/opt/mtc-bridge/releases/be007fd802bbfd2eb181d66038c374865d1562ee` — root-owned, sealed read-only, per-SHA hash-locked venv (56 packages) |
| Service | `mtc-bridge-first-start.service` — **active** since `2026-08-17T00:25:02Z`, `NRestarts=0`, PID 76403, unit sha256 `7696f4a9…` |
| State | `DISARMED`, `mode=credential_free_disarmed`, `network=disabled`, `exchange_conn=disabled`, `arm_enabled=false`, `service_health=healthy` |
| Listener | exactly `127.0.0.1:8790`; public probe `TcpTestSucceeded=False` |
| Secrets | none exist; env file names-only `0600 root:root` |
| Firewall | untouched (UFW default-deny, 22 only) |

## Execution chain (all rc 0 unless noted)

1. Stage 0: old payload `~/payload-acdf4e37` removed.
2. Stage 1: payload `payload-be007fd8` transferred (SCP rc 0); dry run printed
   the complete 32-action manifest — every action inside the signed boundary —
   then exited pre-mutation.
3. Stage 2: ONE bounded install (rc 0): identities, dirs, release copy, venv
   (hash-locked, `verify_lock PASS lock+installed; packages=56`), sealing,
   env names-only, unit installed MASKED (`→ /dev/null`), logrotate + hourly
   cron runner, manifest. `verify.sh`: **VERIFY PASS** — every assertion
   green incl. MemoryHigh/Max, metadata modes, exact unit/venv binding.
4. Stage 3.1–3.2: state archive `bridge-state-initial.tar.gz`
   (sha256 `2a1c42c5001e38e2925ae2565831cc7eb899a74babf4253f989abd1ee7161dc2`);
   rollback rehearsal rc 0 (honest: wrote `rollback_manifest.json`, unit
   stop/mask no-op recorded); re-verify PASS.
5. Stage 3.3: archive copied to EFS-encrypted `C:\tmp\KVM2_BRIDGE_ENCRYPTED`;
   `certutil` hash == host record (exact); restore to EFS dir + **member-by-
   member sha256 compare: 2 members, 0 mismatches**. Deviation of record:
   Windows tar lacks `-d`; Python tarfile hash-compare substituted
   (equal-or-stronger check).
6. Stage 3.4: baseline — disk 3.5G/96G, bridge tenant 1.2G (budget ≤10G),
   RAM 481Mi used, unit inactive-then-started.
7. Stage 3.5: re-inventory — only Bridge objects + cron runner + venv package
   differ from the clean baseline; reserved Hermes/web paths absent.

## First DISARMED start + D3 matrix

- **Start:** unmask + start, `active` at `00:25:02Z`, zero restarts.
- **D3-1** loopback-only: `ss` shows exactly `127.0.0.1:8790` ✅
- **D3-2** internet-unreachable: operator-side probe to `152.239.123.231:8790`
  → `TcpTestSucceeded=False` ✅
- **D3-3** tunnel from the owner's Windows PC (launcher option set): HTTP 200,
  exact `<title>Crypto Paper Bridge</title>` ✅
- **D3-4** dashboard facts: `host_identity=srv1856225`,
  `release_sha=be007fd8…`, `service_start_ts=2026-08-17T00:25:03Z`, fresh
  `status_ts`, `state=DISARMED`, `service_health=healthy` ✅
- **D3-5** persistence: read-only sqlite census `orders count=0 max_rowid=0`,
  `app_state=DISARMED`, DB sha256 prefix `e3ba06536f7dbba337dee3c1` ✅
- **D3-6** ARM refusal: well-formed dashboard-equivalent request
  (`X-Confirm = state_version`) → **HTTP 409**, exact detail
  `ARM unavailable in credential-free DISARMED start mode; exchange access is
  disabled`; state `DISARMED` and `state_version=1` unchanged before/after ✅
  (Disclosure: two refusal probes ran — the tunnel one and a host-loopback one
  to capture the exact detail body; both 409, zero state change.)
- **Network leg (auditd window 00:24:43Z → 03:23:02Z):** rule active whole
  window, `lost 0`. Extraction found **1** line matching the key in
  `audit.log`; the rule-registration `CONFIG_CHANGE` record itself carries the
  key string, so the count is consistent with **zero connect syscalls** by
  uid 999 — corroborated by `network=disabled`, loopback-only bind, and every
  `ss` snapshot. **Honest limit:** the record body was destroyed before
  adjudication because the auditd purge ran before the record was captured
  (Lead sequencing error). The leg is recorded INCONCLUSIVE-BENIGN, not
  proven-zero. **Disclosed follow-up:** one fresh audit window with
  capture-before-purge ordering, under its own sentence, at the next
  maintenance touch. Not material to the keyless DISARMED deployment (no
  credential exists to leak; engine is never constructed; inbound is deny).
- Window closed: rule removed (`RULE_LIST_EMPTY_0`), auditd + libauparse0
  purged (`PURGE_RC=0`, package absent), disposition recorded.

## Standing state at close

Service **left running DISARMED** per the overnight authorization. Owner
opens it any time with `KVM2_RUNKIT/Open-BridgeDashboard.ps1` (agent must be
loaded). Next separately gated steps: TESTNET secret provisioning
(owner-only), TESTNET ARM (own sentence), Dashboard V2 (queued). Mainnet,
real money, orders: forbidden.
