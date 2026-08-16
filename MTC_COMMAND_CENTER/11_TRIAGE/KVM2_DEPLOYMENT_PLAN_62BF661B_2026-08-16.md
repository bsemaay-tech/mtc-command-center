# KVM2 deployment plan — candidate `62bf661b` — 2026-08-16

Status: **PLAN — NOT AUTHORIZED TO EXECUTE.** This is the single exact
deployment action plan required by accelerated-contract clause 6
(`OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`). It is host-touching →
**T0 review (exact `claude-opus-5` + `gpt-5.6-sol`, xhigh) before execution**,
then ONE owner authorization sentence (§8) before the first configure/install
action on KVM2.

## 1. Exact identities

| Item | Value |
|---|---|
| Release candidate | `62bf661b065dec5b5d9895d83575581fe369252d` — dual-flagship T0 ACCEPTED (`BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md`), suite `1360 passed` ×3 independent runs |
| Target host | `srv1856225` = `152.239.123.231` (Hostinger KVM2), inventoried clean 2026-08-16 (`KVM2_READONLY_INVENTORY_2026-08-16.md`) |
| Access | `baris@152.239.123.231`, pinned host key, `hostinger_kvm2` identity via owner-loaded ssh-agent, passwordless sudo |
| Build source | Integration worktree `C:\BRIDGE_RELEASE_INTEGRATION_20260815` — clean, HEAD = candidate |
| Command authority | The candidate's own `IBKR_PAPER_BRIDGE/deploy/linux/COMMANDS.md` (Stages A–C) + `install.sh` / `verify.sh` / `rollback.sh` from the hash-bound payload |
| Mode pin | `MTC_BRIDGE_START_MODE=credential_free_disarmed` inside the hashed unit; unit masked, no `[Install]`, `Restart=no` |

## 2. Stage 0 — payload build (local, no host contact; no authorization needed)

Per COMMANDS.md Stage A, on the integration worktree:

```
bash ./IBKR_PAPER_BRIDGE/deploy/linux/package.sh \
    --release-sha 62bf661b065dec5b5d9895d83575581fe369252d \
    --repo C:\BRIDGE_RELEASE_INTEGRATION_20260815 \
    --out  <local payload dir>
sha256sum <payload>/RELEASE_SHA256SUMS       # record → <PAYLOAD_MANIFEST_SHA256>
```

`package.sh` refuses a dirty tree or wrong HEAD. Payload + manifest SHA-256
recorded in the execution record before any transfer. Online install variant
selected (KVM2 has no pip; the installer's venv bootstraps and installs the
56-package hash-locked `requirements.lock` with `--require-hashes --no-deps
--only-binary=:all:`); the offline wheelhouse path is the recorded fallback if
the install-time network fetch fails hash verification.

## 3. Stage 1 — transfer + dry run (KVM2; FIRST action needing the §8 sentence)

```
scp -i <identity> <payload> baris@152.239.123.231:~/payload-62bf661b/
sudo bash ~/payload-62bf661b/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha 62bf661b… --manifest-sha256 <PAYLOAD_MANIFEST_SHA256> \
    --source ~/payload-62bf661b --dry-run
```

Read the full printed plan. Anything unexpected → STOP, report, no Stage 2.

## 4. Stage 2 — the one bounded install attempt + verify

```
sudo bash ~/payload-62bf661b/.../install.sh --release-sha 62bf661b… \
    --manifest-sha256 <…> --source ~/payload-62bf661b
sudo bash ./deploy/linux/verify.sh --release-sha 62bf661b… --manifest-sha256 <…>
```

Required end state (verify.sh asserts, read-only, repeatable): release sealed
root-owned read-only at `/opt/mtc-bridge/releases/62bf661b…`; hash-locked venv;
`mtc-bridge` nologin user; unit installed **masked**, not started, not
enabled; env file `0600 root:root` names-only; **UFW unchanged, SSH-only;
port 8790 closed; no new listener**. Record unit SHA-256 + lock SHA-256 from
`install_manifest.json`. Exactly one attempt; a failure → §7 rollback + a new
owner sentence for any retry.

## 5. Stage 3 — operational evidence (same authorization, still no start, no secrets)

1. **Rollback rehearsal:** `rollback.sh` semantics exercised (stop+mask on a
   never-started masked unit is a no-op by design — record it; verify it never
   deletes state), then re-run `verify.sh`.
2. **Logrotate:** confirm `/etc/logrotate.d/mtc-bridge` installed; `logrotate
   -d` dry-run output recorded.
3. **Backup/restore:** tar the (empty) `/var/lib/mtc-bridge` +
   `/etc/mtc-bridge/*.json` manifests to an off-host encrypted archive on the
   operator PC; restore to a temp dir; hash-compare. Provider/retention for
   the standing backup remains the open owner choice (readiness item 8) —
   recorded, not blocking DISARMED install.
4. **Monitoring:** minimal — `systemctl is-failed` + disk/log checks via the
   existing SSH route, documented as interim; standing monitoring choice stays
   an owner item.
5. Full read-only re-inventory diffed against
   `KVM2_READONLY_INVENTORY_2026-08-16.md`: the ONLY deltas may be the bridge
   paths/user/unit recorded above. Any other delta → STOP.

## 6. Later, separately gated (NOT covered by §8)

- **Secrets (Stage D / KVM2-P4-03):** owner types TESTNET values directly on a
  trusted session; never through an AI or chat; `HL_LIVE_ACK` absent asserted.
- **First DISARMED start:** own owner sentence naming the exact SHA (wording
  in `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md` item 10), one start,
  loopback-only, TESTNET-only; clean-stop verification.
- **State:** owner decision 2026-08-15 §D5 = **fresh reset** — no WAL
  migration to KVM2. Fail-closed obligation kept: before any TESTNET start,
  prove the fresh DB is empty AND the old Windows writer is quiesced with the
  old agent revoked (COMMANDS.md Stage E quiesce steps, run on the old host
  under its own authorization). ARM/mainnet/orders remain forbidden.

## 7. Rollback (any stage)

`rollback.sh` (stop+mask, preserves state, never deletes), then if full
removal is wanted: remove release dir, venv, `/etc/mtc-bridge`,
`/var/lib|log/mtc-bridge`, `mtc-bridge` user, unit + mask + logrotate file —
returning the host to the inventoried clean baseline of
`KVM2_READONLY_INVENTORY_2026-08-16.md`. Removal commands executed only under
the same §8 authority, recorded.

## 8. The single authorization ask (present to Barış AFTER the T0 plan review)

> "I authorize the one-attempt masked DISARMED installation of exact accepted
> release `62bf661b065dec5b5d9895d83575581fe369252d` onto Hostinger KVM2
> (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_62BF661B_2026-08-16.md stages 1–3:
> transfer, dry run, one bounded install, read-only verification, and
> operational evidence. No service start, no enable, no secret, no firewall
> change, no TESTNET/mainnet, no broker, no ARM, no orders. A failed attempt
> stops and reports; retry needs a new sentence."

## 9. Execution preconditions checklist

- [ ] T0 review of THIS plan: both flagships accepting.
- [ ] Payload built + manifest SHA recorded (Stage 0 — may run now, local).
- [ ] Owner §8 sentence received in chat.
- [ ] ssh-agent loaded by owner at execution time.
