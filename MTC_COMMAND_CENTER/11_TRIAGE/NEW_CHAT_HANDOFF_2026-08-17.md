# New-chat handoff — 2026-08-17 — BRIDGE DEPLOYED AND RUNNING DISARMED

Written at a clean stop by the Fable 5 Lead (accelerated-completion +
overnight-deployment session). Branch `codex/rp7-r1-r4-repair-20260815`,
worktree `C:\R7FINAL`, all committed and pushed, all session-lock rows
released.

---

## 1. Copy-paste prompt for the new chat

```text
Work in C:\R7FINAL as the Lead on branch codex/rp7-r1-r4-repair-20260815.

Read first, in order: root AGENTS.md; MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md;
the top sections of _AI_MEMORY/GLOBAL_HANDOFF.md; _AI_MEMORY/NEXT_STEPS.md;
_AI_MEMORY/SESSION_LOCK.md; 11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-17.md (this
file, in full); 11_TRIAGE/KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md.

Before your first write: verify HEAD, clean worktree, no active writer; run
the repo guard; claim only the SESSION_LOCK rows you intend to write.

STANDING FACTS — do not re-litigate:
- THE BRIDGE IS DEPLOYED AND RUNNING DISARMED on Hostinger KVM2
  (srv1856225, 152.239.123.231): release be007fd802bbfd2eb181d66038c374865d1562ee,
  active since 2026-08-17T00:25:02Z, loopback-only 127.0.0.1:8790,
  credential-free, ARM refused at application level (409 proven). Owner views
  it via 11_TRIAGE/KVM2_RUNKIT/Start-BridgeDashboard.cmd (one-click; runs the
  audited launcher; ssh-agent key must be loaded by the owner).
- The full acceptance chain (4 T0 rounds + confirmation passes + owner
  materiality standard) and the execution evidence are committed —
  KVM2_DEPLOYMENT_PACKAGE_ACCEPTED_2026-08-16.md and
  KVM2_DEPLOYMENT_EXECUTED_2026-08-17.md. Do not re-open accepted findings.
- KVM2 is a future MULTI-TENANT host: hermes + webapp users, /opt/hermes,
  /opt/web, /var/www, ports 80/443 are RESERVED for later tenants; Bridge
  work never touches them. python3.12-venv is owner-authorized baseline.
- The two-commit-chain evidence lane remains OWNER-PAUSED (no cap waiver; do
  not reopen). Pathscope is CLOSED (supplemental, no further cycle).
- SSH to KVM2 needs the isolated option set incl. explicit
  -o UserKnownHostsFile="C:\Users\BarışSemaay\.ssh\known_hosts" (Turkish char
  in HOME breaks defaults). Codex accounts: secondary exhausted -> Aug 22,
  fourth -> Aug 20, free was live; recheck live before dispatch.

SEPARATELY GATED (each needs its own explicit owner sentence):
TESTNET wallet provisioning (owner types keys, never through AI); TESTNET
ARM; the disclosed follow-up network-audit window (auditd, capture BEFORE
purge this time); Dashboard V2 build start; any KVM2 change; merge to
master. Mainnet, real money, orders, live trading: forbidden.

NEXT WORK QUEUE (owner-priority order):
1. Dashboard V2 package when the owner says start — spec anchor plan V3 §D4 +
   V6 lineage; polished read-only owner view + separate private control
   dashboard; T1 visual work / T0 for host, auth, reverse-proxy, control
   endpoints; include the background-tunnel convenience so the CMD window
   eventually disappears.
2. Daily DISARMED health glances (read-only ssh: systemctl is-active, disk,
   /api/status) — cheap, no authorization needed.
3. The strategy-research pivot: QuantLens four-gate pipeline toward ONE
   promotable candidate (716 scored, 0 promotable today) — the real product.
4. Housekeeping session when owner agrees: worktree sprawl cleanup
   (C:\AUD62A/B/C/D, C:\MRGRUN, C:\RO, integration worktree), C:\tmp artifact
   sweep into repo where durable, evidence-programme disposition decision.

Preserve D026, audit tiers, single-writer locks, exact-model rules. English
only. End every reply with numbered next steps + a chosen default.
```

---

## 2. What this session did (one paragraph)

Owner approved ACCELERATED FULL COMPLETION morning; by night the session:
merged the Gate-A/WP-I release, took the candidate through four dual-flagship
T0 rounds + owner-scoped confirmation passes (lineage `62bf661b`→`be689537`→
`a7460784`→`be007fd8`, suite 1360→1381 green, every REQUIRED repaired with
D026 RED/GREEN), built the multi-tenant deployment plan V6 + pinned command
annex + one-click dashboard launcher (v4), executed the owner-signed install
sentence end-to-end on KVM2 (two live fail-closed dry-run stops each cured
under owner sentences — venv package, UFW comment grammar), performed the
first DISARMED start, proved the D3 matrix (network leg inconclusive-benign,
follow-up window queued), and left the bridge RUNNING. Gate 2 re-derived
SATISFIED-WITH-DISCLOSURES; privileged channel ruled not load-bearing; chain
lane owner-paused; Pathscope closed.

## 3. Open follow-ups (recorded, unscheduled)

- Network-leg audit window redo (capture before purge) — needs owner sentence.
- Disclosed-follow-up register from the round-4 verdicts (D3-phase wording
  harmonization etc.) — resolve before the D3/TESTNET sentences are drafted.
- Old GATEA-STAGING VM: still Off with retained checkpoint; decide its fate.
- Monthly AI budget decision + worktree cleanup.
