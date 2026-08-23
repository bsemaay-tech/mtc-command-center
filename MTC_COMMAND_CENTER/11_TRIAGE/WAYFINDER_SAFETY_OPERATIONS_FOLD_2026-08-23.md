# WAYFINDER SAFETY-OPERATIONS FOLD — 2026-08-23 (map #96)

**Status:** owner-decision record and plan-amendment pass. Planning only — **implementation authorized: NO.** Per D-12, nothing here authorizes trading code, Pine, Bridge behaviour, schema activation, host contact, credentials, deployment, testnet, live, ARM, DISARM, KILL, FLATTEN or any work package to start. **This document is not the owner's live signature and does not move any live-readiness row.**

**What this is.** The [Safety, Operations & Production Readiness decision map (#96)](https://github.com/bsemaay-tech/mtc-command-center/issues/96) settled the safety half of the platform: what the emergency controls are and who may use them, what happens when the host, the disk or the evidence fails, how credentials and access are governed, and where live readiness is actually stated. Two research tickets established current truth from repository evidence; four owner-grilled tickets settled the doctrine. **Detail lives in each ticket's resolution comment; this document indexes and applies.**

**Locked prior art.** Nothing in folds #37, #54, #67, #78 or #79 is reopened. KVM2 hosting, the daily/hourly backup cadence, subaccount and agent-wallet binding, custody direction, hybrid worker stores, kernel seams, lifecycle/ledger doctrine, admission/promotion separation, the post-live tail, Explorer display doctrine, Guardian policy, reconciliation ownership and worker/window failure semantics all remain binding. A carrier assignment below makes a settled decision executable; it does not re-decide it.

**Change-control position.** Amends the planning set at master `577e36eb4b44657b00e0ebd801bdb0e2b1da569a`. **Owner outcome documents are untouched. Requirement count stays 60 = 44 OWNER + 16 DERIVED. Package count stays 76** — **no package is added, removed or renumbered.** Existing carriers are amended in place. **Materiality: MATERIAL** — the fold adds ARM to the ratified control set, adds a command lifecycle with an explicit uncertainty rule, converts the live-trading gate into a status-bearing canonical register, and records eight current-truth readiness blockers. A fresh G1 acceptance round over the amended set is recommended before G1-IA for any affected package; that audit and every implementation authorization remain separate owner decisions.

---

## 1. Owner decisions

| Ticket | Ratified decision |
|---|---|
| [Decide: emergency-control and break-glass doctrine (#107)](https://github.com/bsemaay-tech/mtc-command-center/issues/107) | Four controls, one lifecycle. **ARM** permits eligible automated new entries and places none. **DISARM** blocks new risk while protection and exits continue. **KILL** persistently blocks new risk and cancels pending risk-increasing entry/add orders while valid reduce-only protection stays. **FLATTEN** adds scope-wide reduce-only closure and leaves the scope KILLED until recovery and reconciliation. Automated rules may DISARM/suspend; the Guardian vetoes intent and never writes lifecycle state; KILL and FLATTEN need an authenticated owner/operator request; **no automatic FLATTEN**. Authorization ladder: DISARM immediate from an authenticated private session · ARM fresh WebAuthn/FIDO2 + confirm · KILL fresh step-up + separated two-step confirmation · FLATTEN strongest confirmation naming scope and exposure. Notifications carry no control buttons. Unique command IDs, `REQUESTED → ACKNOWLEDGED → RECONCILED` or `FAILED`/`UNKNOWN`, **never auto-retry uncertainty** — freeze risky actions until venue reconciliation. Break-glass is an independent venue-side path from the approved phone and laptop that can cancel risk-increasing orders, close reduce-only and verify positions/orders, recording evidence afterwards; if the venue is unavailable the scope stays KILLED and the flatten is reported unconfirmed. Proven before testnet eligibility, before live eligibility, after a relevant control/credential change and after an incident; recurring drill interval `[OPEN]`; no secrets in the runbook. |
| [Decide: incident, backup and recovery doctrine (#108)](https://github.com/bsemaay-tech/mtc-command-center/issues/108) | Human-led, hours-scale recovery; exact target `[OPEN]`; no second host and no automatic failover. Back up operational DBs, ledgers, audit logs, approved configuration, deployment identity, release manifests and essential runbooks, preserving the already-ratified daily all-store and hourly active-window critical-ledger cadence; never auto-delete protected evidence; no plaintext secrets in ordinary backups. **A backup counts only after an isolated restore proves integrity, readability and reconciliation** — before any forward clock, after backup/schema changes, after a failed recovery and periodically, interval `[OPEN]`. Host/process failure blocks new risk and pages the owner while venue protection continues where possible; rebuild from the last accepted immutable release plus a verified backup, with portfolio reconciliation gating return; open-position emergencies use break-glass. Low disk blocks new risk and alerts before failure; full disk is fail-closed, never deletes protected evidence, preserves protection best-effort and requires repair plus reconciliation. Incident classes: safety/control, truth/evidence, availability — safety and unexplained evidence incidents page and suspend affected risk, serious ones require a postmortem before resumption. External monitoring covers heartbeat, feed/venue freshness, reconciliation, protection, disk and backup health; acknowledgements never clear faults; alerts contain no secrets or controls; timing and escalation `[OPEN]`. |
| [Decide: credentials and access architecture (#109)](https://github.com/bsemaay-tech/mtc-command-center/issues/109) | Simulation and internal paper hold no exchange credential; testnet uses testnet-only credentials; live uses distinct agent wallets per risk bucket/worker; **stages never share credentials**. A worker gets only its scoped credential; dashboard, research, AI and notification paths hold no exchange key; the master wallet stays offline and off KVM2; **until venue withdrawal restrictions are verified, agent keys are treated as able to move funds**. Secrets never enter Git, issues, docs, logs, evidence, ordinary backups or AI prompts; owner-gated provisioning exposes a value only to the required process through restricted OS storage; agents verify presence and permissions and never read or print values. Private mesh only, approved devices, named non-shared accounts, WebAuthn/FIDO2 plus an independent backup authenticator, fresh step-up on dangerous controls, research and execution access separated. Creation, activation, rotation, revocation, expiry and destruction permanently audited; immediate rotation on incident; expiry warnings and a proven revocation drill before live; calendar interval `[OPEN]` pending verified venue rules. Suspected compromise **auto-DISARMS the affected scope** and alerts the owner, who revokes, invokes KILL/FLATTEN or the venue route, isolates, rotates, preserves evidence and reconciles; live eligibility is blocked until a clean recovery; **still no automatic FLATTEN**. |
| [Decide: the live-gate readiness register (#110)](https://github.com/bsemaay-tech/mtc-command-center/issues/110) | **One canonical register is authoritative and supporting documents cannot declare readiness.** Row status enum `UNKNOWN`, `BLOCKED`, `IN PROGRESS`, `PROVEN`, `EXPIRED`; **only `PROVEN` counts**; each row records carrier, scope, exact evidence, commit/deployment identity, proof date, invalidation condition and blocker. Paper/shadow/testnet eligibility is automatic once owner-approved definitions are proven — no repeated owner signature; **only the live transition receives the owner's explicit signature, and this fold is not that signature.** Coverage spans strategy honesty, frozen identity, parity where applicable, paper/testnet evidence, reconciliation, Guardian, idempotency, emergency controls, break-glass, backup/restore, monitoring, disk-full, recovery/rollback, credentials, custody, venue review, incident response and signed capital limits; unratified thresholds `[OPEN]`. Claims, dashboards, AI opinions and test summaries alone do not count; evidence binds to the exact artifact and environment; failure-path tests need D026 RED/GREEN; emergency/restore/revocation/recovery drills need dated results. Relevant strategy/code/policy/config/credential/venue/host/capital changes invalidate affected rows; any hard row at `UNKNOWN`, `BLOCKED` or `EXPIRED` blocks the live signature; serious incidents suspend readiness until recovery and reconciliation. **Current status `NOT READY`.** |

Research inputs, both closed 2026-08-23: [Research: failure-mode catalog vs existing safety mechanisms (#105)](https://github.com/bsemaay-tech/mtc-command-center/issues/105) and [Research: ops baseline in the repo — deploy, rollback, backup, observability, credentials (#106)](https://github.com/bsemaay-tech/mtc-command-center/issues/106). Their files remain on their research branches; this fold carries only the verified findings that reached owner decisions.

---

## 2. Carrier assignments

**Existing carriers only. No package is created.**

| Responsibility | Building/owning carrier | Consumer/proof carrier |
|---|---|---|
| Exact emergency operations, uncertain commands, break-glass runbook | **WP-V2B-10** | WP-V2B-05 renders; WP-V2B-07 drills; WP-V4-01 consumes |
| Private access, authenticators, secret-delivery boundary on the operator side | **WP-V2B-06** | WP-V2B-10's FLATTEN is fail-closed until this lands; WP-V4-01 consumes |
| Authorized-stage testnet and drill evidence (break-glass, revocation, command lifecycle) | **WP-V2B-07** (Lane B) | WP-V4-01 consumes; Lane A holds no credential |
| Backup, restore, external dead-man, incident/recovery, disk/storage doctrine | **WP-P0-26 (OPS-A)** | WP-V2A-08 and WP-V2B-07 clocks remain gated on its acceptance |
| Continuous checks and ops verification | **WP-P0-27 (OPS-C)** — **planned, not built** | Every guard that claims to run automatically |
| Custody and the operational credential-lifecycle boundary | **WP-P0-29 (VEN-C)** | WP-V2B-06 access half; WP-V2B-07 first credentials |
| Canonical live-readiness register and the sole owner signature | **WP-V4-01** | Baris alone signs |

Guardian policy stays with WP-V2B-01, reconciliation ownership stays with WP-V2A-02/WP-V2B-03, and the Decision Orchestrator stays inside WP-V2A-03/04/05. No carrier moves.

---

## 3. Emergency doctrine

The control set is **ARM / DISARM / KILL / FLATTEN**, stated normatively in brief **§10.2a** as an amendment to the table already governing the four operations. ARM is permission and never an order. DISARM blocks new risk while protection and exits continue. KILL persistently blocks new risk and cancels pending risk-increasing entry and add orders while valid reduce-only protection stays live. FLATTEN adds scope-wide reduce-only closure and **leaves the scope KILLED until an explicit recovery and reconciliation step**.

Automated rules may DISARM or suspend. **The Guardian vetoes intent and never writes lifecycle state** — the map-#79 rule, unchanged. **KILL and FLATTEN require an authenticated owner/operator request, and there is no automatic FLATTEN**; the unbuilt automatic-reduction column of §10.2a stays unbuilt, unnamed on the live surface and unauthorized.

The authorization ladder is DISARM immediate from an authenticated private session · ARM fresh WebAuthn/FIDO2 plus confirmation · KILL fresh step-up plus a **separated two-step** confirmation · FLATTEN the **strongest** confirmation, naming scope and exposure. **Notifications contain no control buttons.**

Every command carries a **unique command ID** and moves `REQUESTED → ACKNOWLEDGED → RECONCILED`, or terminates `FAILED` or `UNKNOWN`. **Uncertainty is never auto-retried:** risky actions freeze until venue reconciliation establishes what happened.

Break-glass, stated in **§12.5a**: an independent venue-side path exercisable from the approved phone **and** the approved laptop, able to cancel risk-increasing orders, close exposure reduce-only and verify the resulting positions and orders, with evidence recorded afterwards rather than depending on our own software. **If the venue is unavailable, the scope remains KILLED and the flatten is reported unconfirmed.** It is proven before testnet eligibility, before live eligibility, after any relevant control or credential change, and after any incident, then re-drilled on a recurring interval that is `[OPEN]`. **The runbook contains no secrets.**

---

## 4. Operations and recovery doctrine

Recovery is **human-led and hours-scale**, with **no second host and no automatic failover**; the exact target is `[OPEN]`. Backup scope is operational databases, ledgers, audit logs, approved configuration, deployment identity, release manifests and essential runbooks, on the **already-ratified daily all-store and hourly active-window critical-ledger cadence**. **Protected evidence is never auto-deleted, and no plaintext secret enters an ordinary backup.**

**A backup counts only after an isolated restore proves integrity, readability and reconciliation** — before any forward clock, after backup or schema changes, after a failed recovery, and on a recurring interval that is `[OPEN]`.

Host or process failure **blocks new risk and pages the owner** while venue-side protection continues where possible; recovery rebuilds from the **last accepted immutable release plus a verified backup**, and **portfolio reconciliation gates the return**. Low disk **blocks new risk and alerts before failure**; full disk is **fail-closed**, never deletes protected evidence, preserves protection best-effort, and requires repair plus reconciliation.

Incidents fall into **safety/control, truth/evidence and availability** classes. Safety incidents and unexplained evidence incidents page and suspend the affected risk; serious safety or evidence incidents require a postmortem before resumption. External monitoring covers heartbeat, feed/venue freshness, reconciliation, protection, disk and backup health. **An acknowledgement never clears a fault**, and **alerts carry no secrets and no controls**. Timing and escalation values are `[OPEN]`.

---

## 5. Credential and access doctrine

**Stages never share credentials:** simulation and `INTERNAL_PAPER` hold none, `EXCHANGE_TESTNET` uses testnet-only credentials, live uses distinct agent wallets per risk bucket or worker. A worker receives **only its scoped credential**; the **dashboard, research, AI and notification paths hold no exchange key**; the **master wallet stays offline and off KVM2**; and **until the venue's withdrawal restrictions are primary-source verified, agent keys are treated as able to move funds**.

Secrets never enter **Git, issues, documents, logs, evidence, ordinary backups or AI prompts**. Provisioning is owner-gated and exposes a value only to the process that requires it through restricted operating-system storage. **Agents verify presence and permissions; they never read or print a value** (gate G6).

Access is **private mesh only, approved devices, named non-shared accounts**, with **WebAuthn/FIDO2 plus an independent backup authenticator** (D-16) and **fresh step-up on dangerous controls**. **Research and execution access stay separated** (O-33).

Creation, activation, rotation, revocation, expiry and destruction are **permanently audited**. Compromise triggers immediate rotation; **expiry warnings and a proven revocation drill are required before live**; the calendar interval is `[OPEN]` pending verified venue rules. **Suspected compromise auto-DISARMS the affected scope and alerts the owner**, who then revokes, invokes KILL/FLATTEN or the venue route, isolates, rotates, preserves evidence and reconciles. **Live eligibility is blocked until a clean recovery, and there is still no automatic FLATTEN.**

---

## 6. Live-register doctrine

`_AI_MEMORY/LIVE_TRADING_GATE.md` is **the one canonical register**. **No supporting document declares readiness.** Its **fourteen** top-level categories are preserved exactly as written, including their line positions, so existing citations (`:3-6`, `:8-10`, `:15-66`, `:68-74`) stay valid; the map-#96 structure is **appended below them** and nests subproofs under the existing categories. **No fifteenth category and no competing count is created.**

Row status is one of `UNKNOWN`, `BLOCKED`, `IN PROGRESS`, `PROVEN`, `EXPIRED`, and **only `PROVEN` counts**. Each row records carrier, scope, exact evidence, commit/deployment identity, proof date, invalidation condition and blocker. **Sub-live eligibility is automatic** once owner-approved definitions are proven; **only the live transition takes the owner's signature**, and **this fold is not it**.

**Draft numbers stay draft.** The numeric values already written into the gate — `robust_final = 1`, 30 lockbox trades, 99 % agreement, 8–16 weeks, 30 forward trades, the five-minute flatten target — are recorded as **draft proposals, `[OPEN]`**, with the qualitative requirement preserved in each case. Absolute-form requirements (zero unexplained breaks, zero unexplained orphans, no partial credit, no substitution, secrets outside the repository) are not thresholds and are not reopened.

**Current overall result: `NOT READY`.** No row is `PROVEN` and no per-strategy sign-off exists.

---

## 7. Amendments applied

| # | File · location | Amendment |
|---|---|---|
| A1 | Technical brief · §10.2a | Map-#96 amendment: ARM added to the control set, FLATTEN leaves the scope KILLED, who may act, the authorization ladder, notifications without controls, the `REQUESTED → ACKNOWLEDGED → RECONCILED` lifecycle with no auto-retry, and a pointer to the deployed-v4 current truth. |
| A2 | Technical brief · §12.5a | Map-#96 amendment: what the out-of-band path must reach, the two approved devices, the venue-unavailable rule, the proof occasions, the `[OPEN]` drill interval and the no-secrets rule. Carriers unchanged. |
| A3 | Technical brief · new §12.6 | Normative safety/operations/credentials/live-register fold section with ticket links, the current-truth blocker list (§12.6.5) and the carrier table (§12.6.6). |
| A4 | Work-package plan · §0 count paragraph | Records the map-#96 fold: no package added or renumbered, count stays 76, requirements stay 60 = 44 + 16, fresh G1 recommended. |
| A5 | Work-package plan · WP-P0-26 | Incident, recovery and storage doctrine; backup scope; restore-proof-before-clock; disk fail-closed; incident classes and monitoring; the current backup/monitoring/rollback truth. |
| A6 | Work-package plan · WP-P0-27 | Named as the continuous-check and ops-verification home, **explicitly planned and unbuilt**; rows stay `UNKNOWN`/`BLOCKED` while checks are manual. |
| A7 | Work-package plan · WP-P0-29 | Operational credential-lifecycle boundary: stage separation, least privilege, secret handling, audited lifecycle, compromise response, `[OPEN]` rotation interval. |
| A8 | Work-package plan · WP-V2B-06 | Private access, the independent backup authenticator, fresh step-up per the ladder, the secret-delivery boundary, notifications as a non-command surface, research/execution separation. |
| A9 | Work-package plan · WP-V2B-07 | Authorized-stage drill obligations: two-device break-glass, venue-unavailable recording, command-lifecycle evidence, revocation drill, proof occasions, `[OPEN]` interval; gates unchanged. |
| A10 | Work-package plan · WP-V2B-10 | Exact four-control semantics, authorization ladder, command IDs and uncertain-command rule, break-glass runbook additions, and the deployed-v4 accuracy note; still no drill and no venue contact. |
| A11 | Work-package plan · WP-V4-01 | The canonical register, status enum, row fields, automatic sub-live eligibility versus the sole live signature, coverage, evidence rules, invalidation, `NOT READY` and the carried blockers. |
| A12 | Requirements register · fold note and mapping extensions | Counts unchanged; canonical register named; draft numbers `[OPEN]`; carrier clarifications for D-09, D-11, D-16, O-22, O-33 and D-07; OPS-C recorded unbuilt. |
| A13 | `_AI_MEMORY/LIVE_TRADING_GATE.md` · appended below the existing content | Register doctrine, status enum, the single-signature boundary, evidence and invalidation rules, `NOT READY`, the threshold-ratification table, and the fourteen categories carrying their nested map-#96 subproofs, carrier, scope, exact evidence, commit/deployment identity, proof date, invalidation condition and honest current status/blocker. |

---

## 8. Current brownfield blockers preserved

Recorded from repository evidence (tickets #105 and #106). **No live inspection is claimed, and none of these is permission to repair anything.**

- The deployed Bridge runs **schema v4**; the v5–v9 safety mechanisms are **code-complete and tested but inactive** on that deployed database.
- The deployed **`/api/kill?flatten=true`** path only latches `KILLED` and blocks submissions — under v4 it **does not cancel and does not flatten**.
- There is **no recurring backup and no repeatable restore drill** for live KVM2 state; one install-time archive was restored once.
- There is **no active live monitoring or alerting**; Phase-Watch is inactive and the Telegram deployment is held.
- **`Restart=no` and the absence of systemd install enablement are deliberate** — and without monitoring, an outage could go unnoticed.
- **Rollback was never proven** as a real alternate-release rollback.
- **Disk-full has no current code path and no ratified implemented mechanism.**
- **Deployment execution evidence is stranded off master**, and **master carries stale deployment wording** (consistent with F-14/F-15: deployed version, configuration and schema version remain unverified).
- **Zero functioning CI.** OPS-C (WP-P0-27) is planned and unbuilt.

---

## 9. What remains open

- Every numerical value this doctrine implies: recovery-time target, restore-proof interval, drill and rotation intervals, alert timing and escalation, confirmation timeouts, disk thresholds and every live-gate draft number listed in §6.
- G1 re-acceptance of this material amendment, and G1-IA for every amended package.
- The exact implementation design inside each package boundary, including monitoring technology, backup transport and the register's storage form.
- Whether venue withdrawal restrictions actually bind agent keys — until primary-source verified, the least-trust stance holds (WP-P0-28/WP-P0-29).
- Repository topology, owned by map #97, and the operator surfaces owned by map #95.

---

## 10. What this fold does not do

- No source, trading, Pine, Bridge-runtime, schema, migration, host, credential, deployment, testnet or live change.
- No database opened or modified; no process, service, server, worker, broker or venue contacted.
- No package started and no G1/G1-IA/G2–G9 gate satisfied.
- **No live signature, no readiness row moved to `PROVEN`, and no claim that any deployed safety mechanism is active.**
- No settled map reopened; no owner outcome document changed; no requirement or package added, removed or renumbered.
- No invented numeric value, and no draft gate number promoted to a ratified threshold.

---

## 11. Verification

- Base: `origin/master` at `577e36eb4b44657b00e0ebd801bdb0e2b1da569a`.
- Branch: `feature/wayfinder-fold-map96-20260823` in isolated worktree `C:\WF111`.
- Editing discipline: exact anchored patches only; no broad replacement, no protected path and no owner outcome document. The live-gate additions are appended **below** the existing content so that every `_AI_MEMORY/LIVE_TRADING_GATE.md:n-m` citation in the document set stays exact.
- Post-pass checks: repo-wide marker searches, package/requirement counts, exact changed-path review, whitespace check.
- Counts: requirements **60 = 44 + 16** unchanged; packages **76** unchanged (no package added, removed or renumbered).
