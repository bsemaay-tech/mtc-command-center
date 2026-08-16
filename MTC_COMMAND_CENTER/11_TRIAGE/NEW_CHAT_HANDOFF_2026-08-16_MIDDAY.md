# New-chat handoff — 2026-08-16 midday

Written at a clean stop by the Fable 5 Lead (session `f3a2cf9f`). Branch
`codex/rp7-r1-r4-repair-20260815`, HEAD **`e1dc3d95`**, worktree clean, pushed,
all session-lock rows released. 32 commits this session.

---

## 1. Copy-paste prompt for the new chat

```text
Work in C:\R7FINAL as the Lead on branch codex/rp7-r1-r4-repair-20260815.

Read first, in this order: root AGENTS.md; MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md;
the top section of _AI_MEMORY/GLOBAL_HANDOFF.md; _AI_MEMORY/SESSION_LOCK.md;
11_TRIAGE/NEW_CHAT_HANDOFF_2026-08-16_MIDDAY.md (this file, in full);
11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md;
11_TRIAGE/POSTMORTEM_ALREADY_DEPLOYED_2026-08-16.md;
11_TRIAGE/GATEA_STAGING_OBSERVATION_2026-08-16.md;
11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md.

Before your first write: verify HEAD, a clean worktree, and no active writer;
run the repo guard; then claim only the SESSION_LOCK rows you intend to write.

BEFORE STARTING ANY LARGE WORK, ASK BARIS THE OPEN QUESTION IN SECTION 3 OF THE
HANDOFF. It decides whether the remaining programme is ~15-25 hours or ~60-70,
and he is frustrated about elapsed time and spend. Do not launch a broad audit
fan-out before he answers.

Standing facts you must not re-litigate: all six owner decisions of 2026-08-16
are ANSWERED and APPLIED. Pathscope is CLOSED - supplemental with disclosure,
off the critical path, and a sixth cycle is forbidden. RP7 rows 1-9 stay T0
accepted at 80cbed46; do not touch those bytes. The two-commit chain (Option A)
is the selected ordering fix.

GATEA-STAGING is a LOCAL Hyper-V VM on this PC, currently Off, with a retained
checkpoint GATEA-STAGING-CH1-PRECHANGE-V1. The bridge is already installed on
it and already ran DISARMED on testnet for 2.5 days in August. KVM2 (Hostinger)
has nothing installed. NEVER state a deployment status without naming which of
those two hosts it refers to - conflating them caused a false report to the
owner and a public correction.

Owner authorization for GATEA-STAGING host actions is live and recorded in
11_TRIAGE/HOST_CHANNEL_AUTHORIZATION_2026-08-16.md: you may connect, configure,
use sudo/root, run controlled verification, and create evidence on that VM
only. Forbidden everywhere: Hostinger, KVM2 (including the sibling VM
KVM2-Ubuntu-2404-Staging), production, broker/exchange, ARM, orders,
TESTNET/mainnet, trading logic, merge to master. Never display, copy, replace,
or rotate private-key contents or any secret.

Preserve D026, audit tiers, single-writer locks, and exact-model rules. Do not
touch the dirty primary checkout C:\LAB\Tradingview_LAB_CLEAN. Answer and write
in English. End every reply with numbered next steps and a chosen default.
```

---

## 2. What happened this session, in one page

Barış answered all six pending owner decisions in chat at 07:55. Each became a
committed artifact the same morning, and every stale "waiting on the owner"
claim in the repository was corrected — 18 files bannered, then the Pathscope
disclosure sentence written byte-for-byte into all 30 documents that had treated
it as a gate.

Two flagship reviews ran on Claude Pro and both found real defects: the
Pathscope disclosure draft (5 REQUIRED, including that the repository still
carries the *older broken* prover while the audited fix sits unmerged, and that
one document's precondition would have made Audit 2 permanently undispatchable)
and the two-commit chain design (6 REQUIRED, including a second dependency
cycle of the same shape as the one Option A was chosen to fix).

Then the staging blocker dissolved. It had been recorded for days as "eight
facts only a server administrator can supply". There is no administrator and no
remote server: **GATEA-STAGING is a Hyper-V VM on Barış's own PC.** Under his
authorization the Lead took a checkpoint, started it, observed read-only, and
shut it down. Seven of the eight facts were answered immediately; the eighth
(a mutation-denial control) genuinely does not exist. Two recorded facts were
stale: the address, and the sudo scope — the account has full passwordless root,
not the narrow families recorded on 9 August.

**And the bridge was already there, and had already run:** a hardened systemd
unit, DISARMED, Hyperliquid TESTNET, from 2026-08-09 00:43:49Z to 2026-08-11
14:17:05Z — two days thirteen hours, clean shutdown, 461 KB of write-ahead log.

The Lead then **overstated that finding to the owner** — saying the plans were
wrong — and corrected it. The "never installed" rows describe **KVM2**, where
they are accurate. Post-mortem: `POSTMORTEM_ALREADY_DEPLOYED_2026-08-16.md`.

---

## 3. THE OPEN QUESTION — ask this first

Barış is weeks into what he expected to be a weekend project, at roughly
$2.2k/month. The Lead's diagnosis, which he has **not yet answered**:

Two projects are tangled. Getting the bridge onto the server is genuinely
10–20 hours. Proving it to audit standard is the remaining 60–70 hours and most
of the money — and nobody ever chose that standard; it accreted until it matched
what a regulated bank applies to a live money-moving system, while the actual
system is a disarmed paper bot on a disposable VM touching no real money.

Put to him, still awaiting an answer:

- **B — match the proof to the risk.** Full evidence only where a mistake costs
  real money or leaks a secret: broker credentials, live/mainnet paths, order
  placement, key handling. Everything else: one review, no repair loop.
  Estimated to cut the remainder to roughly 15–25 hours.
- **C — deploy first, document after.** Freeze the evidence programme, install
  on the VPS, start it disarmed on testnet, watch it run, and write evidence
  afterwards for what actually matters.

The Lead recommended **C then B**, with the money gate keeping its full standard
either way. Dashboard, same URL, already updated:
`https://claude.ai/code/artifact/7ceb461c-ba2a-49bb-bceb-a50aa5beddf2`

**If he says B and C:** stop generating audit paperwork for the plumbing, and
move to KVM2 deployment using the proven staging recipe (§5).
**If he says A (keep the standard):** work §4 in order.

---

## 4. Work queue if the standard stays

Ready to dispatch; kickoffs already written.

| # | Task | Kickoff | Notes |
|---|---|---|---|
| 1 | Re-audit two-commit chain V2 | `C:\tmp\lane_kick\AUD_TC2.md` | Claude Pro, T1. V2 claims to close all 6 REQUIRED + 7 NIT. **Pin the subject bytes first** — V1's review had to, because the file changed mid-review. |
| 2 | Independent review, Phase-2 V3 (all ten contracts) | `C:\tmp\lane_kick\KVR1.md` | T2. Verdicts of record are `PHASE2_V2_INDEPENDENT_VERDICTS_2026-08-16.md`; V3 files are `PHASE2_IFNS_CONTRACTS_V3_2026-08-16.md` and `PHASE2_SSRTMI_CONTRACTS_V3_2026-08-16.md`. |
| 3 | Review the P9-15 policy grammar draft | not written | `P9_15_POLICY_GRAMMAR_DRAFT_2026-08-16.md` is precondition 3 for the producer. Unreviewed, never treat as canonical. |
| 4 | Lead sign-off on the P9 producer kickoff | — | `P9_PRODUCER_KICKOFF_REPAIR_2026-08-16.md` carries a sign-off block with required fields; the producer stays undispatched until every field is concrete. |
| 5 | Re-derive prerequisite gate 2 | — | It is **UNKNOWN**, not satisfied. Removing Pathscope as its only open sub-item did not close it. |
| 6 | Audit the privileged channel design | not written | **Consider dropping this.** See §6. |

---

## 5. The proven deployment recipe (the most valuable asset found)

On GATEA-STAGING, from `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`.
Reusable for KVM2 nearly verbatim. Full text quoted in
`GATEA_STAGING_OBSERVATION_2026-08-16.md`.

- Release at `/opt/mtc-bridge/releases/<40-hex-commit>`, root-owned, read-only
  (`dr-xr-xr-x`); pinned venv beside it at `/opt/mtc-bridge/venvs/<same-commit>`;
  the unit names the exact commit, never a mutable `current` symlink.
- Dedicated `mtc-bridge` service account, uid 999, `/usr/sbin/nologin`.
- Installed **masked**, with **no `[Install]` section** — `systemctl enable` is
  structurally impossible, so it can never start at boot.
- `Restart=no` — a crash stays crashed for inspection.
- `MTC_BRIDGE_START_MODE=credential_free_disarmed` pinned inside the hashed unit.
- `NoNewPrivileges`, empty capability sets, `ProtectSystem=strict`,
  `ProtectHome`, `ProtectProc=invisible`, `PrivateTmp`, `PrivateDevices`,
  `RestrictNamespaces`, `RestrictSUIDSGID`, `LockPersonality`,
  `SystemCallFilter=@system-service` → `EPERM`,
  `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`, `UMask=0077`.
- Exactly two writable paths: `/var/lib/mtc-bridge`, `/var/log/mtc-bridge`.

Caveat that must travel with it: this is candidate `2ce41e34`, accepted for
**staging only**. Acceptance does not transfer to KVM2 or to a newer candidate.

---

## 6. Honest judgement to carry forward

**The privileged channel design is probably over-engineered now.** It proposes a
statically linked C account-shell gate, Landlock rulesets, seccomp filters and a
private mount namespace — for a disarmed paper bot on a disposable local VM. It
was written before we knew the machine was local and already deployed. It is
committed and its reasoning is sound, but under options B/C most of it is
unnecessary. Do not audit or build it without asking Barış whether he wants that
standard here.

**Pathscope is closed. Do not reopen it.** Five cycles, none accepted; a sixth
is forbidden by owner decision §6.

**Prefer looking over inferring.** Fifty documents reasoned about eight unknown
facts that twenty minutes of authorized observation answered. Eleven parallel
lanes produced nine documents in fifteen minutes, and four hours then went into
reviewing them — fan-out was never the bottleneck.

**Model routing.** Codex `secondary` and `free` are live; `fourth` is exhausted
until **2026-08-20 10:20**. Claude Pro is the reliable flagship audit route
(~8–11 min per verdict, both found real defects). Claude Max stays emergency
only. GLM-5.3 stalls silently under fan-out. Never route several heavy lanes to
one account, and health-check by reading log tails, not by watching for output
files.

---

## 7. State table

| Area | State |
|---|---|
| RP7 rows 1-9 | **Accepted** at `80cbed46`, dual T0 flagship. Untouched. |
| RP6 / transport / SEC102 | Accepted with disclosure, earlier and independently. |
| Pathscope | **CLOSED** — supplemental with disclosure, off critical path, no further cycle. Repo copy is the older R5 prover; the audited fix is unmerged. |
| Two-commit chain | V1 reviewed `REQUEST_CHANGES` (6 REQUIRED); **V2 committed, not yet re-audited**. |
| KVM2 Phase 2 | All ten contracts at **V3**; independent review not yet run. |
| Bridge release | Suite repairs accepted at T1, **not merged**; readiness verified read-only; frozen input refreshed `W := 7d4e9a96`. |
| Packet 9 | Producer blocked on Lead sign-off; policy grammar drafted, unreviewed. |
| Audit 2 | Blocked behind the freeze. 6 h hard cap, metering mandatory. |
| Prerequisite gate 2 | **UNKNOWN** — must be independently re-derived. |
| GATEA-STAGING | Bridge installed, ran 2.5 days in August, VM `Off`, checkpoint retained. |
| KVM2 / Hostinger | **Nothing installed. This is the real remaining work.** |

---

## 8. Boundaries at this stop

No Hostinger, KVM2, production, broker/exchange, ARM, order, TESTNET/mainnet,
Pine, parity, MTC, trading, merge-to-master, or economic action occurred. On
GATEA-STAGING the guest was read only — no file, package, service, account, or
configuration was modified; the only changes were to the VM object on the host
(checkpointing enabled, one checkpoint created, VM started and stopped). No key
content was ever read, printed, hashed, copied, replaced, or rotated. The
owner's read-only grant #6 permission remains **unspent**.
