# W7 — KVM2 secret contract and state contract (Phase-2 draft)

Status: **PREPARATION ONLY / DRAFT / NO AUTHORITY / NO HOST ACTION**
Date: 2026-08-15 night. Lane W7, single output file; repository read-only.

## Source legend

All paths under `C:\RO` unless noted. Citation form `name:line`.

- `W7` — `C:\tmp\lane_kick\W7.md`
- `DECISIONS` — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md`
- `BREAKDOWN` — `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md`
- `TASKS` — `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `READINESS` — `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md`
- `SECRET_INVENTORY` — `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/SECRET_INVENTORY.md`
- `STATE_CONTINUITY` — `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md`
- `ENV_TEMPLATE` — `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template`

## 0. Missing cited source

`W7:41` says "See
`MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md`".
That file **does not exist** — a glob over `C:\RO` for `*TABLETOP*` returns nothing
tonight. What would settle it: the file landing at the cited path (a parallel
lane's output) or an owner-corrected pointer. Until then, D5's own record is the
only cited statement of the clean-start requirement, and this draft binds only on
`DECISIONS:89-110`. Nothing below may be read as anticipating the tabletop's
contents.

## 1. Governing decisions, scope, and boundary

- **D4 (binds §2):** the KVM2 TESTNET wallet is deferred — "this we will do
  later". No wallet is provisioned, requested, or inferred; deploy checklist
  item 4 stays open and blocks the first start; nothing in the deploy sequence
  may proceed past the point that requires it; no agent may ask for, generate,
  store, or reference a key value (`DECISIONS:80-87`; `W7:32-36`).
- **D5 (binds §3):** "start clean" — a fresh-database reset, deliberately
  overriding the recorded recommendation of WAL-consistent migration
  (`DECISIONS:89-97`; the recommendation being overridden is at
  `READINESS:186-189`; `STATE_CONTINUITY:3-5` still records the pre-decision
  state and lags D5 — D5 governs).
- This is Phase-2 rebuild-kit preparation only: design artifacts, no
  reprovision or install (`TASKS:92-94`). The breakdown assigns exactly these
  two contract designs to R31 (`BREAKDOWN:70`), whose audit tier is T2
  documentation/evidence with self-verification only (`BREAKDOWN:27-29`).
- No host, network, deployment, service, credential, broker/exchange, ARM,
  order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or
  economic action is authorized or performed by this document (`W7:49-51`;
  `DECISIONS:133-135`; `BREAKDOWN:210-212`). No product code changes. No
  sub-delegation (`W7:53-56` — none used).

## 2. Secret contract (P2-05 secret contract, drafted under D4)

The contract describes the **mechanism for a secret that does not exist yet**.
No value and no placeholder that resembles one appears anywhere in this section
or its sources' intent (`W7:43-44`; `SECRET_INVENTORY:1-4`).

### 2.1 Required end state

1. **Deferred now.** Until the owner lifts D4, no wallet exists, and no agent
   requests, generates, stores, or references a key value (`DECISIONS:84-87`).
   Checklist item 4 remains open and blocks the first start; the deploy
   sequence stops at the point that requires the wallet (`DECISIONS:85-86`).
2. **Sanctioned mechanism, when the owner acts (P4-03 only).** A newly created,
   separately revocable, **KVM2-specific Hyperliquid TESTNET agent wallet** —
   never the main wallet key — with the names `HL_ACCOUNT_ADDRESS` (account
   identifier, no spending authority) and `HL_API_WALLET_KEY` (VPS-specific
   agent authority) delivered through an approved secret channel directly into
   `/etc/mtc-bridge/mtc-bridge.env` at `root:root`, mode `0600`, referenced by
   `EnvironmentFile=` in the bridge unit (`READINESS:168-172`;
   `ENV_TEMPLATE:3-5,15-20`; `SECRET_INVENTORY:8-9`). An equivalent store is
   admissible only under a fresh owner P4-03 record and only if it meets every
   property of this section.
3. **One store only.** The root-owned system environment file is the only
   sanctioned store. No secret value may appear in a repository `.env` or any
   project-local, home, or working-tree env/dot file, in the repository, in
   chat, in a prompt, in a task list, in shell history, in a screenshot, or in
   a plaintext backup (`W7:37-39`; `ENV_TEMPLATE:6-10`; `READINESS:172-173`;
   `TASKS:286-288`).
4. **Install-time state.** The installer creates only a comment-only contract
   file with every variable left unset, never writes a value, and stops if
   definitions already exist; installation itself provisions no TESTNET secret
   and fails closed if any secret value is present (`ENV_TEMPLATE:3-5`;
   `SECRET_INVENTORY:20-21`; `TASKS:278-284`).
5. **Backups exclude secrets.** Every inventoried secret is excluded from
   backup (`SECRET_INVENTORY:8-13`).
6. **`HL_LIVE_ACK` is forbidden.** It must be absent from the env file, the
   unit, the service process environment, manifests, and evidence
   (`SECRET_INVENTORY:15-18`; `ENV_TEMPLATE:30-35`).
7. **Optional names** (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
   `ANTHROPIC_API_KEY`, `XAI_API_KEY`): same storage class and exclusion rules;
   each feature stays silently disabled while unset (`ENV_TEMPLATE:22-28`;
   `SECRET_INVENTORY:10-13`).
8. **Authority and lifecycle.** Provisioning is owner-only P4-03 work under an
   authorization separate from install (P4-01 grants no secret authority);
   rotation/revocation triggers per name are as inventoried (incident, host
   change, suspected exposure, cutover, provider reset, destination change)
   (`TASKS:265-268,285-293`; `ENV_TEMPLATE:6-11`; `SECRET_INVENTORY:8-13`).

### 2.2 Verification

- **Tonight, documentation level:** the contract carries names, storage rules,
  consumers, and triggers only — no value, no value-shaped placeholder
  (`W7:43-44`). P2-05 acceptance evidence is the inventory field set
  (name/purpose/owner/issuer/allowed consumer/storage class/mode
  requirement/rotation trigger/revocation procedure/backup
  inclusion-exclusion) with values absent (`TASKS:131-135`).
- **Deferred-state check:** absence of any request, generation, storage, or
  reference of a key value by any agent or artifact tonight
  (`DECISIONS:87`).
- **Future P4-03 mechanism checks** (owner-executed, separately authorized,
  recorded without exposing other secrets): env file `root:root 0600`; unit
  `EnvironmentFile=` binding present; `HL_LIVE_ACK`-absent proof over
  unit/files/process; no value in repo, chat, shell history, or backup
  (`TASKS:14-17,285-293`).

### 2.3 Violation signature

Any one of these is a contract violation:

- a key value, or any placeholder shaped like one, in the repository, a
  repo-local `.env` or other dotfile, chat, a prompt, a task list, shell
  history, a screenshot, or a plaintext backup (`W7:43-44`; `ENV_TEMPLATE:8-10`);
- any agent requesting, generating, storing, or referencing a key value
  (`DECISIONS:87`);
- a secret provisioned without a separate P4-03, or P4-01 cited as its
  authority (`TASKS:291-293`);
- `HL_LIVE_ACK` present in any form (`TASKS:292-293`; `SECRET_INVENTORY:15-18`);
- the env file not root-owned `0600`, or any secret value provisioned or
  present at install/verify time (`TASKS:283-284`);
- the main wallet key used instead of a VPS-specific agent wallet
  (`ENV_TEMPLATE:17-20`; `READINESS:161-163`);
- a secret inside any backup (`SECRET_INVENTORY:8-13`).

### 2.4 Out of scope

- Provisioning, requesting, generating, storing, or referencing the wallet in
  any form — deferred by D4 (`DECISIONS:80-87`).
- Any host action tonight: no env file is created, inspected, or modified.
- Monitoring/backup provider credentials: not inventoried until P5-01
  separately names provider, issuer, consumer, least-privilege scope, storage
  class, revocation owner, cost, and attempt bound (`SECRET_INVENTORY:16-18`;
  `TASKS:384-399`).
- ARM, mainnet, orders, TESTNET execution, product-code change, merge to
  master (`W7:49-51`).
- Choosing the concrete approved secret channel: **UNKNOWN** — the cited
  sources require it but define it nowhere (`READINESS:169-170`). Settled only
  by the owner's future P4-03 authorization record.

## 3. State contract (P2-06 state contract, drafted under D5)

### 3.1 Required end state

1. **Cutover starts clean.** The destination receives a fresh database, not a
   WAL migration — a deliberate owner override of the recorded recommendation
   (`DECISIONS:89-97`; `READINESS:175-193`). `STATE_CONTINUITY:3-5` still
   reads "choice OPEN / WAL recommended / fresh reset not selected"; D5
   supersedes that on selection, and the artifact must be reconciled before
   Phase-3 consumes it.
2. **What the destination legitimately holds at first start:** no inherited
   daily-loss counter, no consecutive-loss counter, no order history, and no
   foreign-position record (`DECISIONS:100-101`). Each "no" is a **proven
   zero** — an invariant digest of the fresh artifact recording
   daily-loss absent/zero, consecutive-loss zero, order history empty, foreign
   positions/orders none — not a merely unrun check.
3. **Preserve or block.** The fresh reset must preserve or block on lost
   daily-loss, consecutive-loss, order, and foreign-position evidence
   (`DECISIONS:102-107`; `READINESS:191-193`). Concretely: the P4-05 ordered
   checklist takes the final WAL-consistent source capture plus its SHA-256
   and only then applies the accepted policy — migrate, or execute the
   accepted conservative reset (`TASKS:320-322`). Under D5 the reset branch
   runs instead of migration, so the captured source bundle and its hash are
   the retrievable form of the otherwise-lost evidence ("carry that evidence
   forward in some retrievable form", `DECISIONS:105`); any failure, mismatch,
   or unknown in the capture, its hash, or the semantic checks blocks the
   cutover (`TASKS:324-325`, stop at `326-330`). The crosswalk states the same
   requirement branch-neutrally: after old-writer quiesce, P4-05 proves final
   WAL capture, transfer/reset, integrity/semantics, **and both hashes**
   (`TASKS:256`). "Start clean" is not "start blind" (`DECISIONS:106-107`).
4. **Single-writer proof unchanged and mandatory.** Whatever happens to the
   database: DISARMED confirmed; fresh reconcile; raw empty positions and
   orders from the exchange captured **before** old-writer termination;
   Windows task stopped/disabled; child processes absent; port 8790 closed on
   the old host; old-host authority revoked; a **second** timestamped raw
   exchange-side positions/orders capture after revocation; responses
   preserved without secrets (`DECISIONS:108-110`; `TASKS:313-319`;
   `READINESS:195-211`).
5. **Destination artifact identity (reset branch).** The fresh database is
   produced by exactly one accepted reset procedure; its SHA-256 plus the
   zero-invariant digest of item 2 constitute the destination state artifact,
   recorded alongside the source capture hash in a timestamped ordered record
   (`TASKS:321-325`; both-hashes requirement `TASKS:256`). The one DISARMED
   first start must verify this exact artifact loaded by recorded hash before
   starting (`TASKS:342-348`).
6. **Integrity and semantic gates.** SQLite `integrity_check` passed;
   application-level semantic checks for daily-loss, consecutive-loss, foreign
   positions/orders, and corrupt/unknown state; any mismatch or unknown
   evidence blocks the cutover (`TASKS:321-325`). Foreign exchange
   positions/orders are never inferred from SQLite; they remain raw
   exchange-side checks under owner control (`STATE_CONTINUITY:23-26`).
7. **D5 open sub-question carried, undecided:** whether the pre-cutover risk
   state must be archived off-host or may be left on the old machine. The Lead
   recommends archiving as the only record of the paper period; it is a
   one-sentence owner follow-up, not a blocker for pre-cutover work
   (`DECISIONS:112-116`). This contract requires the source capture and hash
   of item 3 either way and takes no position on off-host archiving.
8. **Recovery classes stay owner-open.** RPO/RTO per class (bridge
   state/risk, logs/evidence, config/release) remain undecided; backups must
   be encrypted off-host, versioned/retention-locked, with an isolated restore
   drill and secrets excluded (`STATE_CONTINUITY:28-43`; `TASKS:136-146`).

### 3.2 Verification

- **Tonight, documentation level:** the contract binds D5 exactly, defines the
  destination zeros, the block conditions, and the artifact identity. No
  runtime state is claimed — no cutover, host, or exchange observation exists
  to cite (`READINESS:206-211` lists the UNVERIFIED set).
- **Future cutover** (only under separately authorized P4-04A quiesce plus
  P4-05 cutover): the full ordered evidence of item 4, the final source
  capture plus SHA-256 of item 3, and the integrity/semantic/hash-pair/
  timestamped-record gates of items 5-6 (`TASKS:304-330`).
- **First start** (only under P4-06/P4-07): the exact accepted destination
  state artifact verified loaded by recorded hash before start; first start
  DISARMED and TESTNET-only; exactly one loopback listener `127.0.0.1:8790`
  and no public 8790; restart count zero; health and reconciliation confirmed;
  `HL_LIVE_ACK`-absent proof; forced log-rotation test executed and passed
  (`TASKS:337-348`).
- **Unknown is a blocking result, not a pass:** any non-empty, stale, unknown,
  failed, reordered, or ambiguous check blocks; a failed or ambiguous
  observation must stop the cutover (`TASKS:326-330`; `READINESS:211`).

### 3.3 Violation signature

- The destination holds any inherited daily-loss or consecutive-loss counter,
  order history, or foreign-position record not created by its own post-reset
  operation (`DECISIONS:100-101`, inverted).
- The reset is executed without the final source capture, without its recorded
  SHA-256, or a failed/unknown capture does not block — silent evidence loss
  (`DECISIONS:102-107`; `TASKS:320-325,326-330`).
- Any cutover check missing, stale, reordered, or ambiguous; the
  post-revocation raw exchange recheck absent; a second writer appears
  (`TASKS:326-330`; `READINESS:206-211`).
- First start with the destination state artifact absent, unverified, or
  hash-mismatched (`TASKS:347-348`).
- A fresh database of unknown provenance — not produced by the one accepted
  reset procedure (`TASKS:320-322,337-348`).
- "Start clean" treated as license to skip the evidence question — start-blind
  (`DECISIONS:106-107`).
- Any restore path that resets or hides risk evidence (`TASKS:144-146`).

### 3.4 Out of scope

- Executing any quiesce, cutover, or other host action — separately authorized
  P4-04A/P4-05 only (`TASKS:304-330`; `W7:49-51`).
- Deciding the D5 archive sub-question — owner one-sentence follow-up
  (`DECISIONS:112-116`).
- Designing the WAL migration branch — not selected by D5 (`DECISIONS:93-97`);
  only the final source capture of item 3 survives from that tooling, per the
  checklist order (`TASKS:320-322`).
- Owner RPO/RTO acceptance, backup/restore drills, and monitoring-provider
  choices (`STATE_CONTINUITY:30-43`; `TASKS:136-146`).
- ARM, mainnet, orders, trading, product-code change, merge to master
  (`W7:49-51`).

## 4. Explicitly not established (UNKNOWN)

1. The tabletop file cited by `W7:41` does not exist — see §0.
2. The concrete approved secret channel is required but undefined in the cited
   sources (`READINESS:169-170`); only the future P4-03 owner record settles it.
3. The exact fresh-database producer: the cited sources define the WAL bundle
   tool (`STATE_CONTINUITY:9-14`) but no cited document defines the reset
   branch's concrete creation command. This contract fixes its required
   properties (one accepted procedure, provenance, recorded SHA-256,
   zero-invariant digest, both-hashes record) and nothing more; the producer
   must be bound in the fail-closed reset specification the owner approves
   (`READINESS:191-193`). That specification should also confirm this draft's
   reading that the final source capture precedes and survives the
   migrate-or-reset branch point (`TASKS:320-322`).
4. `STATE_CONTINUITY.md` is not yet reconciled to D5 (`STATE_CONTINUITY:3-5`
   vs `DECISIONS:89-97`).
5. RPO/RTO per recovery class — open owner decisions
   (`STATE_CONTINUITY:30-35`).
6. The off-host-archive sub-question — open (`DECISIONS:112-116`).

## 5. Self-verification and boundary

- Exactly one file written by this lane: this one (`W7:9-10`). The repository
  was touched read-only; no git command was run at all, so nothing took the
  index lock (`W7:5-8`).
- Both owner decisions are reflected: D4 in §2 (deferred mechanism, no value,
  no value-shaped placeholder, item 4 still blocking); D5 in §3 (fresh
  database, proven zeros, preserve-or-block, unchanged item-6 single-writer
  proof).
- Every factual claim carries a `file:line` citation; open points are marked
  UNKNOWN with what would settle them. No hour estimate was requested or
  produced; no number is presented as derived.
- No secret value and no placeholder that looks like one appears; only names
  already published in the cited repository artifacts.
- No host, network, deployment, service, credential, broker/exchange, ARM,
  order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or
  economic action is authorized or performed (`W7:49-51`).
