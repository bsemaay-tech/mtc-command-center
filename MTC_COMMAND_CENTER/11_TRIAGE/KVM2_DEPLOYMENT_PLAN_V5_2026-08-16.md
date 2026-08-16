# KVM2 deployment plan V5 — final candidate `a7460784` — 2026-08-16

Status: **PLAN — NOT AUTHORIZED TO EXECUTE. SUPERSEDES V4.** V5 incorporates
V2 §0 (tenancy model), §2 (bootstrap/upgrade split), §6–§8, V3 §D1–§D4, and
V4 §2.1/§2.3–§2.6 by reference as amended below; **no earlier version has
independent authority, and every executable command an operator runs is
restated IN THIS FILE — the incorporated texts supply context and
constraints, never commands.** Implements every remaining REQUIRED from the
round-2 verdicts (Codex R2/R3/R4; Claude R3) on top of the round-3 candidate
repairs. Round accounting: this plan + its fresh T0 pair = **round 3 (final)
of the un-reset Plan-V3 T0 cap.**

## 1. Exact identities (final pins)

| Item | Value |
|---|---|
| **Final replacement initial-release candidate** | `a7460784c1563c140ee7c75197aeab2b0170da8a` — tip of `integration/bridge-release-20260815` (pushed); lineage `62bf661b` → `be689537` → `a7460784`. KVM2 remains empty and untouched; this replaces the initial-release candidate before any deployment. |
| Round-3 candidate delta vs `be689537` | 8 files, +301/−107: fail-closed UFW ALLOW parser (ranges, destination-address form, unmodelled/app-profile grammar STOPs), Bridge-only hourly logrotate runner (`deploy/linux/cron/mtc-bridge-logrotate`) with honest nominal-threshold wording, D026-falsifiable rebuilds of the dry-run-manifest / read-only-verifier / unit-ceiling tests, strict+bounded `status_ts` freshness test. |
| Candidate test state | `1373 passed, 1 warning` — implementer run 176.91 s AND Lead-independent run 186.88 s. All round-2 D026 mutations demonstrated RED in scratch, GREEN on final bytes (`RIC2_REPAIR_REPORT_2026-08-16.md`). |
| Payload | `C:\tmp\payload-a7460784`, built from the clean worktree at `a7460784`; `RELEASE_SHA256SUMS` sha256 `2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0` |
| Launcher | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` **v3** — 8651 B, sha256 `533f29db75ebfa12d1bb1ecbe7f40d241d94364c4f41d74d293268b0f053adca`. No key file of any kind is opened: the expected agent fingerprint is the pinned literal `SHA256:8b6bl/srDevzQ1rycf9FcQFgZXblSMddqak/9JsHBC8` (Lead-computed from the public file 2026-08-16), required verbatim in `ssh-add -l -E sha256` output. |
| Host / access | unchanged: `srv1856225` = `152.239.123.231`, `baris`, pinned host key, owner-loaded agent |
| Retired pins | candidates `62bf661b` (payload `1078ac22…`) and `be689537` (payload `58705d92…`), launchers v1 (`9c9beaeb…`) and v2 (`e6e8bfa4…`) — superseded, never installed. |

## 2. Exact executable command set (overrides every earlier command block)

**Stage 1 — transfer + dry run** (first §9-gated action):

```
scp -o BatchMode=yes -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=C:\Users\BarışSemaay\.ssh\known_hosts" -r C:\tmp\payload-a7460784 baris@152.239.123.231:~/payload-a7460784
ssh baris@152.239.123.231  # same pinned options; then on the host:
sudo bash ~/payload-a7460784/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha a7460784c1563c140ee7c75197aeab2b0170da8a \
    --manifest-sha256 2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0 \
    --source ~/payload-a7460784 --dry-run
```

Operator reads the COMPLETE ID-keyed mutation manifest; any action outside
the V2 §0 Bridge boundary → STOP.

**Stage 2 — one bounded install + verify:**

```
sudo bash ~/payload-a7460784/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha a7460784c1563c140ee7c75197aeab2b0170da8a \
    --manifest-sha256 2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0 \
    --source ~/payload-a7460784
sudo bash /opt/mtc-bridge/releases/a7460784c1563c140ee7c75197aeab2b0170da8a/IBKR_PAPER_BRIDGE/deploy/linux/verify.sh \
    --release-sha a7460784c1563c140ee7c75197aeab2b0170da8a \
    --manifest-sha256 2581ed3fbb020c03bb4e0dc41f35d60a54ee949d892164c705a34050abd9b8c0
```

**Stage 3 — operational evidence, in THIS order** (reordered per round-2
Codex R4 / Claude R3; all inside the Bridge boundary):

1. **State capture FIRST** (produces the rehearsal input). On the host:

   ```
   sudo tar -C / -czf ~/bridge-state-initial.tar.gz var/lib/mtc-bridge etc/mtc-bridge/install_manifest.json
   sudo python3.12 /opt/mtc-bridge/releases/a7460784…/IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create \
       --source /var/lib/mtc-bridge/bridge.db --out-dir ~/bridge-state-manifest
   sha256sum ~/bridge-state-manifest/bundle_manifest.json   # record → <STATE_MANIFEST_SHA256>
   ```

   The bundle manifest file `~/bridge-state-manifest/bundle_manifest.json`
   is the host-resident state-manifest input; its recorded 64-hex sha is the
   second input. (If the fresh install's DB does not yet exist, the empty
   state dir is the captured truth; `wal_state_bundle.py` runs against the
   initialized DB the installer creates — if none exists, the rehearsal input
   is the tar's sha256 and `rollback.sh` is exercised with the manifest the
   installer wrote; the execution record states which branch was taken.)

2. **Rollback rehearsal** — the literal command, no `--to-*` arguments in the
   initial rehearsal:

   ```
   sudo bash /opt/mtc-bridge/releases/a7460784…/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh \
       --state-manifest-file ~/bridge-state-manifest/bundle_manifest.json \
       --state-manifest-sha256 <STATE_MANIFEST_SHA256>
   ```

   Honest description: this writes/replaces
   `/etc/mtc-bridge/rollback_manifest.json` (authorized by §9) and stops+masks
   the already-masked never-started unit (recorded as such). It deletes
   nothing.
3. Off-host encrypted copy of the stage-3.1 archive to the operator PC;
   restore to temp; hash-compare (backup/restore leg).
4. Monitoring baseline (Bridge paths vs headroom budget; disk usage of
   `/var/log/mtc-bridge` vs the 10 G budget — the compensating control for
   the nominal-only log threshold).
5. Tenancy re-inventory diff vs `KVM2_READONLY_INVENTORY_2026-08-16.md`; only
   the Bridge rows + `/etc/cron.hourly/mtc-bridge-logrotate` may differ;
   reserved Hermes/web paths must still not exist.

**Partial-install disposition** (unchanged from V4 §2.2, restated): on any
install failure — stop; capture the dry-run-manifest-keyed list of performed
mutations; remove exactly those artifacts per the V2 §7 enumeration (which
now includes `/etc/cron.hourly/mtc-bridge-logrotate`); re-verify the clean
baseline; report. Retry needs a new owner sentence.

## 3. D3-5/D3-6 evidence mechanism (round-2 Codex R3 / Claude R6 — final form)

Runs only after the separate first-start sentence, during the D3 matrix:

1. **Persistence leg (deterministic, service-independent):** read-only SQLite
   census before and after the ARM attempt — orders-table row count + rowids
   + `bridge.db`/WAL file sha256, via `sqlite3` read-only URI from the
   operator's root session. Required: exact equality.
2. **Response leg:** the dashboard's own ARM control (well-formed
   `X-Confirm`), exact HTTP 409 detail `ARM unavailable in credential-free
   DISARMED start mode; exchange access is disabled`, `/api/status` before
   and after `state=DISARMED` with unchanged `state_version`.
3. **Network leg (continuous, attributed):** BEFORE the attempt window,
   install and start an audit rule capturing connect() syscalls attributed
   to the `mtc-bridge` UID: `auditd` + `auditctl -a exit,always -F arch=b64
   -S connect -F uid=<mtc-bridge uid> -k mtcbridge_net`. `auditd` is not on
   the host today; §9 explicitly authorizes installing the single distro
   package `auditd` and this one rule for the evidence window (both named in
   the tenancy re-inventory; rule removed and package left installed-inactive
   or removed after the window, recorded either way). Required: zero connect
   events to non-loopback destinations for the whole window. If auditd
   cannot be installed or the rule cannot be proven active, the row STOPs —
   sampled `ss -ntupH` loops may be recorded as supplemental but never
   substitute.

## 4. §9 — the single authorization ask (present ONLY after both round-3 verdicts accept)

> "I authorize the one-attempt masked DISARMED installation of exact
> replacement release `a7460784c1563c140ee7c75197aeab2b0170da8a` onto
> Hostinger KVM2 (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_V5_2026-08-16.md —
> that is: payload transfer, dry run, one bounded install, read-only
> verification, and Bridge-scoped operational evidence in plan §2 stage-3
> order (state capture, rollback rehearsal including its rollback-manifest
> write, off-host encrypted backup + restore check, monitoring baseline,
> tenancy re-inventory), all inside the V2 §0 Bridge tenancy boundary plus
> the single named cron file. It also pre-authorizes, for the later D3
> evidence window only, installing the distro `auditd` package and one
> UID-scoped connect-audit rule as written in plan §3. No service start, no
> enable, no secret, no firewall change, no TESTNET/mainnet, no broker, no
> ARM, no orders, no action on reserved Hermes/web identities, no public
> exposure of port 8790 ever. The D3 matrix itself runs only after my
> separate first-start sentence. A failed attempt stops, restores the clean
> baseline per plan §2, and reports; any retry needs a new sentence."

## 5. Review contract — final round-3 T0 pair

Subjects: THIS file + launcher v3 + candidate `a7460784` (execute the 1373
suite; verify every round-2 REQUIRED closed on mechanism — Codex R1–R7,
Claude R1–R3 — including the D026 mutation set from `RIC2_REPAIR_REPORT`;
re-attack fresh). This is the cap's last round: an accepting pair yields the
§4 owner ask; any REQUIRED exhausts the cap and goes to the owner.
