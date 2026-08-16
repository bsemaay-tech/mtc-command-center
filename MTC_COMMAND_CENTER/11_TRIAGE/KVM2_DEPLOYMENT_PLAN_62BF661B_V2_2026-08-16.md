# KVM2 deployment plan V2 — candidate `62bf661b` — multi-tenant host — 2026-08-16

Status: **PLAN — NOT AUTHORIZED TO EXECUTE. SUPERSEDES V1**
(`KVM2_DEPLOYMENT_PLAN_62BF661B_2026-08-16.md`; V1 was superseded before any
review verdict existed). Implements the owner's multi-tenant requirement and
bootstrap/upgrade split (`OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md`).
Host-touching → **T0 review (exact `claude-opus-5` + `gpt-5.6-sol`, xhigh)
before execution**, then ONE owner sentence (§9) before the first
configure/install action on KVM2.

## 0. Host tenancy model (permanent, owner-declared 2026-08-16)

`srv1856225` will host three tenants. Only the Bridge is installed now.

| Tenant | Status | Linux identity | Filesystem home | Ports |
|---|---|---|---|---|
| **MTC Bridge** | installed by this plan | `mtc-bridge` (nologin, created by installer) | `/opt/mtc-bridge/**`, `/etc/mtc-bridge`, `/var/lib/mtc-bridge`, `/var/log/mtc-bridge` | loopback `127.0.0.1:8790` ONLY — never public, never behind the future reverse proxy |
| Hermes agent | FUTURE — nothing installed now | reserved: `hermes` | reserved: `/opt/hermes`, `/var/lib/hermes`, `/var/log/hermes` | reserved: loopback ports per its own later plan |
| Websites | FUTURE — nothing installed now | reserved: `webapp` (+ reverse proxy under its own package user) | reserved: `/opt/web`, `/var/www` | **80/443 reserved for this tenant** |

Tenancy rules binding on every Bridge action in this plan:

- Bridge work touches ONLY the four Bridge paths, the `mtc-bridge` user, its
  unit + mask, `/etc/logrotate.d/mtc-bridge`, and (during install) the
  payload dir under `/home/baris`. The reserved names/paths above are
  RESERVATIONS — this plan must never create, modify, inspect or delete them.
- **No global Python packages** (per-SHA venv only, hash-locked), no shared
  application directories, no system-wide runtime changes.
- **No host-wide security change.** UFW rule set is NOT modified (install.sh
  never touches the firewall; verify.sh only reads it). "SSH-only" is the
  present observed state, not a requirement — 80/443 remain free to be opened
  by the future web tenant under its own authorization. No kernel, PAM,
  sysctl, apparmor, mount or Docker-blocking change of any kind.
- **Service-specific ops:** Bridge backup, monitoring, logrotate and rollback
  cover Bridge paths only, enumerated in §7 — never "everything under /opt",
  never a host-wide operation.
- **Isolation:** the hardened unit (`ProtectSystem=strict`, `ProtectHome`,
  dedicated nologin user, empty capability sets, two writable paths) means a
  Bridge compromise is confined to `/var/lib/mtc-bridge` +
  `/var/log/mtc-bridge`; future tenants run as different users with 0750
  homes, unreadable to `mtc-bridge`. Recorded as a standing property to
  re-verify when each future tenant arrives.

### Resource headroom (recorded so the Bridge can never crowd future tenants)

Host: 2 vCPU, 7.8 Gi RAM, 96 G disk (1.4 G used). Bridge measured on the
GATEA staging run (2 d 13 h): **46.9 MiB peak RAM, 3 min 43 s total CPU, DB
WAL &lt;1 MiB/day; logs capped at 64 MiB by logrotate.** Budget declared for
the Bridge tenant: ≤1 GiB RAM, ≤10 G disk, negligible CPU — leaving ≥6.8 Gi
RAM and ≥85 G disk for Hermes + websites. Enforcement now = §5.4 monitoring
check against this record (no unit edit: the accepted unit's bytes are part
of the audited candidate and are not modified; a `MemoryMax` line becomes a
candidate change for a future release, noted in §8).

## 1. Exact identities

| Item | Value |
|---|---|
| Release candidate | `62bf661b065dec5b5d9895d83575581fe369252d` — dual-flagship T0 ACCEPTED (`BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md`) |
| Payload (built 2026-08-16, local Stage 0 complete) | `C:\tmp\payload-62bf661b`; `RELEASE_SHA256SUMS` sha256 `1078ac22d3139be1ea50ede33fcb3dbc2ef01c5c860b46941c27ec8b550c175d` |
| Target host | `srv1856225` = `152.239.123.231` (Hostinger KVM2), inventoried clean 2026-08-16 |
| Access | `baris@152.239.123.231`, pinned host key, owner-loaded ssh-agent, passwordless sudo |
| Command authority | Candidate's own `deploy/linux/COMMANDS.md` Stages A–C + `install.sh` / `verify.sh` / `rollback.sh` from the hash-bound payload |
| Mode pin | `MTC_BRIDGE_START_MODE=credential_free_disarmed`; unit masked, no `[Install]`, `Restart=no` |

## 2. ONE-TIME BOOTSTRAP vs REPEATABLE UPGRADE — the split

**Bootstrap (once, this plan, §3–§5):** payload transfer → dry run → one
bounded install (creates `mtc-bridge` user, directory skeleton, first
release + venv + masked unit + logrotate) → verification → operational
evidence (rollback rehearsal, backup/restore, monitoring baseline, tenancy
re-inventory). Forecast: **7–12 h** including audits — paid ONCE.

**Upgrade (every later release, §8):** the layout is side-by-side by design —
each release lives at `/opt/mtc-bridge/releases/<SHA>` with its own venv, and
the unit hard-codes the exact SHA. An upgrade adds a new release beside the
old one and re-binds; the old release stays installed as the rollback target
(`rollback.sh` re-binds to a prior installed SHA without deleting state).
User, skeleton, env file, logrotate, backup and monitoring are reused, never
recreated. The full bootstrap is **never repeated**.

## 3. Bootstrap stage 1 — transfer + dry run (FIRST action needing the §9 sentence)

```
scp -i <identity> -r C:\tmp\payload-62bf661b baris@152.239.123.231:~/payload-62bf661b/
sudo bash ~/payload-62bf661b/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha 62bf661b065dec5b5d9895d83575581fe369252d \
    --manifest-sha256 1078ac22d3139be1ea50ede33fcb3dbc2ef01c5c860b46941c27ec8b550c175d \
    --source ~/payload-62bf661b --dry-run
```

Read the complete printed plan. Verify every mutating action it names falls
inside the §0 Bridge boundary. Anything outside → STOP, report, no stage 2.

## 4. Bootstrap stage 2 — the one bounded install attempt + verify

```
sudo bash ~/payload-62bf661b/.../install.sh --release-sha 62bf661b… \
    --manifest-sha256 1078ac22… --source ~/payload-62bf661b
sudo bash ./deploy/linux/verify.sh --release-sha 62bf661b… --manifest-sha256 1078ac22…
```

Required end state (verify.sh asserts, read-only, repeatable): release sealed
root-owned read-only; hash-locked venv; `mtc-bridge` nologin user; unit
**masked**, not started, not enabled; env file `0600 root:root` names-only;
**UFW untouched; port 8790 closed; no new listener**. Record unit SHA-256 +
lock SHA-256 from `install_manifest.json`. Exactly one attempt; failure → §7
rollback + new owner sentence for retry.

## 5. Bootstrap stage 3 — operational evidence (same authorization; no start, no secrets)

1. **Rollback rehearsal:** exercise `rollback.sh` stop+mask semantics
   (no-op on a never-started masked unit — record that), assert it deletes
   nothing and touches only §0 Bridge paths; re-run `verify.sh`.
2. **Logrotate:** `/etc/logrotate.d/mtc-bridge` present; `logrotate -d`
   dry-run recorded. Service-specific only.
3. **Backup/restore (Bridge-scoped):** tar `/var/lib/mtc-bridge` +
   `/etc/mtc-bridge/*.json` to an off-host encrypted archive on the operator
   PC; restore to temp; hash-compare. Standing provider/retention = open
   owner choice, recorded, non-blocking for a DISARMED install.
4. **Monitoring baseline (Bridge-scoped):** `systemctl is-failed`, disk usage
   of the four Bridge paths vs the §0 headroom budget, log sizes — via the
   existing SSH route; interim until the owner picks standing monitoring.
5. **Tenancy re-inventory:** full read-only sweep diffed against
   `KVM2_READONLY_INVENTORY_2026-08-16.md`; the ONLY deltas may be the §0
   Bridge rows. Reserved Hermes/web paths must still not exist. Any other
   delta → STOP.

## 6. Later, separately gated (NOT covered by §9)

- **Secrets:** owner types TESTNET values directly on a trusted session;
  never through an AI or chat; `HL_LIVE_ACK` absent asserted.
- **First DISARMED start:** own owner sentence naming the exact SHA; one
  start; loopback-only; TESTNET-only; clean-stop verification.
- **State:** fresh reset (owner 2026-08-15 §D5) — no WAL migration.
  Fail-closed obligation kept: before any TESTNET start, prove the fresh DB
  empty AND old Windows writer quiesced + old agent revoked (COMMANDS.md
  Stage E quiesce, on the old host, own authorization).
- ARM / mainnet / orders / live trading remain forbidden.

## 7. Rollback / removal boundary (exact enumeration — nothing else, ever)

`rollback.sh` (stop+mask, preserves state, deletes nothing); full removal if
wanted = delete exactly: `/opt/mtc-bridge/`, `/etc/mtc-bridge/`,
`/var/lib/mtc-bridge/`, `/var/log/mtc-bridge/`, the `mtc-bridge` user, the
unit file + mask symlink, `/etc/logrotate.d/mtc-bridge`,
`~/payload-62bf661b`. **Explicitly barred from touching:** anything under the
reserved Hermes/web identities and paths (§0), any other user, any firewall
rule, any package, any port, any container, any non-Bridge service — present
or future. Removal returns the host to the inventoried clean baseline.

## 8. Repeatable upgrade procedure (created by this bootstrap; forecasts)

For a future accepted release `<NEW_SHA>` (each upgrade requires its own
tier-required acceptance of the candidate and one owner install sentence,
scope identical to §9 with the new SHA):

1. Build payload locally (`package.sh --release-sha <NEW_SHA>`), record
   manifest SHA. (~15 min)
2. Transfer; `install.sh --dry-run`; then one bounded install → creates
   `/opt/mtc-bridge/releases/<NEW_SHA>` + `venvs/<NEW_SHA>` + new unit
   **beside** the old release; user/skeleton/env/logrotate reused. (~30–60 min)
3. `verify.sh` for `<NEW_SHA>`; tenancy re-inventory diff. (~15–30 min)
4. Swap under the start policy in force at that time; old release retained as
   the `rollback.sh` re-bind target until the owner authorizes pruning.

Forecasts (hands-on, excluding the candidate's own local acceptance work):

| Upgrade class | Definition | Host work | With tier audits of the host action |
|---|---|---|---|
| Small | docs/test-only delta, deps unchanged, no schema change | ~1 h | **1–2 h** |
| Normal | code change, deps unchanged | ~1.5–2 h | **2–4 h** |
| Major | lock/dependency change, schema migration, or unit change | ~2–3 h + migration proof | **4–8 h** |

Never the 7–12 h bootstrap again. A unit change (e.g. adding `MemoryMax`) is
by definition ≥ Normal because the unit hash is part of the verified install.

## 9. The single authorization ask (present AFTER the T0 review of THIS plan)

> "I authorize the one-attempt masked DISARMED installation of exact accepted
> release `62bf661b065dec5b5d9895d83575581fe369252d` onto Hostinger KVM2
> (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md stages
> 3–5: transfer, dry run, one bounded install, read-only verification, and
> Bridge-scoped operational evidence — inside the §0 Bridge tenancy boundary
> only. No service start, no enable, no secret, no firewall change, no
> TESTNET/mainnet, no broker, no ARM, no orders, no action on reserved
> Hermes/web identities. A failed attempt stops and reports; retry needs a
> new sentence."

## 10. Compact diff V1 → V2

1. NEW §0: three-tenant model with reserved users/paths/ports; tenancy rules;
   no host-wide security changes; 80/443 reserved; "SSH-only = present state,
   not permanent"; isolation property; resource headroom record + Bridge
   budget (≤1 GiB RAM / ≤10 G disk vs measured 46.9 MiB / ~1 MiB-day).
2. NEW §2: explicit one-time-bootstrap vs repeatable-upgrade split.
3. NEW §8: reusable side-by-side upgrade procedure + small/normal/major
   forecasts (1–2 / 2–4 / 4–8 h); bootstrap never repeated.
4. §5 ops evidence made explicitly Bridge-scoped; added tenancy re-inventory
   with reserved-path absence check.
5. §7 rollback rewritten as an exact enumeration with an explicit bar on
   touching future-tenant anything.
6. §9 sentence updated: tenancy boundary named; reserved-identity exclusion
   added.
7. Stage-0 payload facts folded in (already built; manifest sha
   `1078ac22…`).
8. Everything else (candidate identity, COMMANDS.md anchoring, one-attempt
   rule, secrets/start gates, fresh-reset) carried unchanged from V1.
