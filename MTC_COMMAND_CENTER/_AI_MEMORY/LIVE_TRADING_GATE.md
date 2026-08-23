# LIVE TRADING GATE

> Status: DRAFT.
> Track: SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
> Purpose: convert "live trading is forbidden" into "live trading is gated."
> Binding status: not binding until Baris signs this document.

Live trading remains blocked. No AI may recommend going live, imply live
readiness, or treat this gate as satisfied. Every item below requires dated
evidence for one specific strategy and explicit Baris sign-off.

The SYSTEM_TEST_ONLY vertical slice satisfies none of these requirements and
can never be cited as live-readiness evidence.

## Hard Preconditions

All items are required. There is no partial credit.

1. Strategy robustness:
   `robust_final = 1`, at least 30 lockbox trades, positive excess alpha versus
   buy-and-hold, CPCV/PBO reports, and multi-window stability, regenerated on a
   frozen tagged commit.
2. Reference lock:
   frozen parameters, tagged commit, hashed signal file, and deterministic
   rerun reproducing the same signal file.
3. Parity proof, if Pine participates in monitoring or signaling:
   dated artifact, at least 99 percent signal-flag agreement over full history,
   and trade-list diff within the approved tolerance. A parity artifact older
   than the last code change on either side is void.
4. Paper soak:
   pre-registered plan, immutable start date, 8 to 16 weeks minimum and at
   least 30 new forward trades, zero unexplained reconciliation breaks, and no
   restarted window unless a new plan is approved.
5. Testnet proof:
   executor or bridge soaked on exchange testnet, including duplicate-signal
   injection and kill-process-mid-open-position restart/reconcile behavior.
6. Reconciliation:
   daily three-way diff across expected signals, bridge or executor log, and
   exchange statement throughout the paper/testnet period. Unexplained orphan
   count must be zero.
7. Kill switch:
   three layers documented and drilled with timing evidence: signal source
   pause, bridge/executor halt, and API key revocation. Full flatten target:
   under five minutes. An un-rehearsed kill switch is not a kill switch.
8. Idempotency:
   every payload carries an idempotency key and dedup behavior is proven by
   deliberate duplicate delivery.
9. Failure drills:
   documented behavior for duplicate signal, dropped signal, malformed payload,
   wrong environment, and exit-with-no-position.
10. Capital limit:
    dedicated sub-account funded with pilot capital only. The hard number is
    signed by Baris before any live pilot.
11. Key security:
    withdrawal disabled, IP restricted, least privilege permissions, rotation
    schedule, and secrets stored outside the repo.
12. Incident response:
    one-page runbook for reconciliation break, exchange halt, runaway-signal
    alarm, open-position emergency, and broker/exchange support path.
13. Monitoring:
    MTC Command Center may render read-only heartbeat, position summary, and
    last reconciliation status. It must not send orders or mutate execution
    state.
14. Human approval:
    explicit written Baris sign-off on this checklist, per strategy and per
    capital increase. Never AI-recommended, never implied.

## Standing Rules

- Dashboard visibility is not gate evidence.
- Scorecard scores are not live-readiness evidence.
- Board/model consensus is not live-readiness evidence.
- SYSTEM_TEST_ONLY artifacts are not strategy evidence.
- Any attempt to bypass this checklist is a stop-everything incident.

## Per-Strategy Sign-Offs

None exist.

## Signature

- [ ] Baris accepted this draft gate on: ____________

---

# Register doctrine — wayfinder map #96 fold, 2026-08-23

**Everything above this line is unchanged, byte for byte.** The map-#96 structure is appended below it
so that the existing citations to this file — `:3-6` (draft status), `:8-10` (the no-recommendation
rule), `:15-66` (the fourteen hard preconditions) and `:68-74` (the standing rules) — remain exact.

**This document is the ONE canonical live-readiness register.** Ratified through wayfinder map #96,
ticket #110. **No supporting document declares readiness** — not the technical brief, not the work
package plan, not the traceability register, not a dashboard, not an evidence pack, not a fold record,
and not an AI. They supply evidence; this file is where readiness is stated.

**The fourteen categories above are preserved as the top level.** Map-#96 subproofs nest *under* them.
No fifteenth category is created and no competing count exists.

**Planning only. This fold is not a signature, and it authorizes nothing** (D-12).

## Row status

Every row carries exactly one status:

| Status | Meaning |
|---|---|
| `UNKNOWN` | Nobody has established the position. The default |
| `BLOCKED` | A named obstacle prevents proof |
| `IN PROGRESS` | Work is under way; nothing is proven yet |
| `PROVEN` | Proof exists, dated and bound to identity |
| `EXPIRED` | Was proven; an invalidating change has since occurred |

**Only `PROVEN` counts.** Every row records: **carrier · scope · the exact evidence · the commit and
deployment identity it binds to · the proof date · the invalidation condition · the current blocker.**

**The single-signature boundary.** Paper, shadow and testnet eligibility is **automatic** once the
owner-approved definitions are proven — no repeated owner signature per stage. **Only the live
transition receives the owner's explicit signature. This fold is not that signature and authorizes
no actual stage action.**

**What is not evidence.** Claims, dashboards, AI opinions and test summaries alone. Evidence binds to
the exact artifact and environment that produced it. **Failure-path tests require D026 RED/GREEN.**
**Emergency, restore, revocation and recovery drills require dated results.**

**Invalidation.** A relevant change to strategy, code, policy, configuration, credential, venue, host
or capital invalidates the affected rows. **Any hard row at `UNKNOWN`, `BLOCKED` or `EXPIRED` blocks
the live signature.** A serious incident suspends readiness until recovery and reconciliation.

## Current overall result: NOT READY

**No per-strategy sign-off exists, and no row is `PROVEN`.**

## Threshold ratification status

The numeric values written into the preconditions above are **draft proposals recorded in an unsigned
draft**, not owner-ratified thresholds. They are listed here so that nothing becomes ratified by
repetition. **The qualitative requirement in each case stands exactly as written above as a ratified
planning requirement — it is neither a proof nor a live signature; only the number is open.**

| Precondition | Draft numeric value | Status |
|---|---|---|
| 1 — Strategy robustness | `robust_final = 1`; at least 30 lockbox trades | Planning requirement ratified; **not PROVEN and not a live signature**. The numbers are **draft proposals, `[OPEN]`** |
| 3 — Parity proof | at least 99 % signal-flag agreement | Planning requirement ratified; **not PROVEN and not a live signature**. The number is **`[OPEN]`** |
| 4 — Paper soak | 8 to 16 weeks; at least 30 new forward trades | Planning requirement ratified; **not PROVEN and not a live signature**. The numbers are **`[OPEN]`** |
| 7 — Kill switch | full flatten target under five minutes | Planning requirement ratified (drilled, with timing evidence); **not PROVEN and not a live signature**. The target is **`[OPEN]`** |
| 10 — Capital limit | the hard number is not stated here | **`[OPEN]` by construction** — it requires Baris's signature |
| Recovery, drill, rotation, escalation intervals | none stated | **`[OPEN]`** — set by the owner, never inferred |

**Absolute-form requirements are not thresholds and are not reopened:** zero unexplained
reconciliation breaks, zero unexplained orphans, no partial credit, no substitution between
preconditions, and secrets stored outside the repository all stand as written.

## The fourteen categories with their map-#96 subproofs

**Carriers are proposals in `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, and naming
one here authorizes nothing.** Statuses below are the honest current position, not a work plan.

**How to read the evidence columns.** `None accepted` means no artifact has been accepted as proof for
that row — not that no artifact exists anywhere. Because **no row is `PROVEN`**, every
*commit/deployment identity* and *proof date* cell is `—`. The *invalidation condition* is stated in
advance so that a future proof carries its own expiry rule; stating it now proves nothing.

| # | Category (unchanged above) | Map-#96 subproofs nested under it | Carrier | Scope | Exact evidence | Commit / deployment identity | Proof date | Invalidation condition | Status · current blocker |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Strategy robustness | honest-strategy evidence regenerated on a frozen tagged commit | WP-P0-20, WP-P0-21 | Per strategy, per instrument/timeframe set, regenerated on **one** frozen tagged commit | `None accepted` | `—` | `—` | Any change to strategy logic, parameters, data set or simulator; any regeneration on a different commit; a superseding lockbox run | `BLOCKED` — zero tags exist in the repository |
| 2 | Reference lock | frozen identity; deterministic rerun | WP-P0-02, WP-P0-04 | Per strategy: the frozen parameter set, the tagged commit and the hashed signal file that together define its identity | `None accepted` | `—` | `—` | Any commit touching the referenced code path; any parameter edit; any signal-file hash mismatch on deterministic rerun | `BLOCKED` — zero tags exist in the repository |
| 3 | Parity proof | parity where Pine participates at all | WP-P0-06, WP-P0-23 | Per strategy, **only where Pine participates in monitoring or signalling**; full history, signal flags plus trade-list diff | `None accepted` | `—` | `—` | Any code change on either the Pine or the Python side after the artifact date voids the artifact; any tolerance change | `UNKNOWN` |
| 4 | Paper soak | `INTERNAL_PAPER` lane evidence only | WP-V2B-07 Lane A | Per strategy, `INTERNAL_PAPER` lane only, over **one** pre-registered immutable window with an immutable start date | `None accepted` | `—` | `—` | Restarting or altering the window without an approved new plan; any strategy or configuration change during it; any unexplained reconciliation break | `UNKNOWN` |
| 5 | Testnet proof | `EXCHANGE_TESTNET` lane evidence only | WP-V2B-07 Lane B | Per executor/bridge release, `EXCHANGE_TESTNET` venue only, including duplicate-signal injection and kill-process-mid-open-position restart/reconcile | `None accepted` | `—` | `—` | Any executor/Bridge release, schema activation, venue-API change or host change after the soak | `UNKNOWN` |
| 6 | Reconciliation | worker and portfolio reconciliation; recovery reconciliation gating return to operation | WP-V2A-02, WP-V2B-03 | Per account, daily three-way diff — expected signals · bridge/executor log · venue statement — across the whole paper/testnet period | `None accepted` | `—` | `—` | Any missing day; any unexplained orphan; any change to the reconciliation source set or matching rules | `UNKNOWN` |
| 7 | Kill switch | ARM / DISARM / KILL / FLATTEN semantics; the command lifecycle `REQUESTED → ACKNOWLEDGED → RECONCILED` with `FAILED`/`UNKNOWN` terminals and no auto-retry; the authorization ladder; **break-glass**: independent venue-side path from the approved phone and laptop, drilled, timed, re-proven after any relevant control or credential change and after any incident | WP-V2B-10, WP-V2B-06, WP-V2B-07 | Per deployed release and per venue account: all three kill layers, both approved devices, drilled with measured elapsed time | `None accepted` | `—` | `—` | Any control-path, credential, device, venue or schema change; any incident; expiry of the `[OPEN]` re-drill interval | `BLOCKED` — the deployed Bridge runs schema v4, where `/api/kill?flatten=true` only latches `KILLED` and blocks submissions; it neither cancels nor flattens |
| 8 | Idempotency | duplicate-delivery dedup proven deliberately | WP-P0-04, WP-V2A-05 | Per payload path, end to end, proven by deliberate duplicate delivery rather than by inspection | `None accepted` | `—` | `—` | Any change to payload schema, idempotency-key derivation, dedup window or delivery transport | `UNKNOWN` |
| 9 | Failure drills | the named failure paths, each D026 RED/GREEN | WP-V2B-07, WP-P0-27 | Per named failure path — duplicate signal, dropped signal, malformed payload, wrong environment, exit-with-no-position — each as a D026 RED/GREEN pair | `None accepted` | `—` | `—` | Any handler, validation or routing change; a drill result older than the last change to the path it covers | `UNKNOWN` |
| 10 | Capital limit | the signed capital limit, plus D-07's separate lower loss-at-stop cap | WP-V4-01 | Per strategy and per capital increase: a dedicated sub-account, the owner-signed hard number, and D-07's separate lower loss-at-stop cap | `None accepted` | `—` | `—` | Any capital increase; any sub-account or venue change; any change to either cap | `BLOCKED` — the lower loss-at-stop cap is undefined |
| 11 | Key security | stage-separated credentials; scoped per worker; no exchange key on dashboard, research, AI or notification paths; master wallet offline and off KVM2; owner-gated provisioning; audited creation/rotation/revocation/expiry/destruction; proven revocation drill; compromise auto-DISARMS the affected scope | WP-P0-29, WP-V2B-06, WP-V2B-07 | Per credential and per stage: scope, permissions, storage location and the audited lifecycle of each key, plus a dated revocation drill | `None accepted` | `—` | `—` | Any credential creation, rotation, revocation or permission change; any venue policy change; any device or access change; any suspected compromise | `UNKNOWN` |
| 12 | Incident response | the three incident classes; page-and-suspend on safety and unexplained-evidence incidents; postmortem before resumption; **backup and restore** proven by isolated restore before any forward clock; **recovery and rollback** from the last accepted immutable release plus a verified backup, gated by portfolio reconciliation; **disk-full** fail-closed with no deletion of protected evidence | WP-P0-26, WP-V2B-10 | Per host and per protected store: the one-page runbook, a proven isolated restore, a proven alternate-release rollback, and disk-full fail-closed behaviour on live KVM2 state | `None accepted` | `—` | `—` | Any backup, schema or host change; any failed recovery; any release that changes the rollback target; expiry of the `[OPEN]` restore-proof interval | `BLOCKED` — no recurring backup and no repeatable restore drill for live KVM2 state (one install-time archive, restored once); rollback never proven as a real alternate-release rollback; no disk-full code path or ratified mechanism exists |
| 13 | Monitoring | external heartbeat, feed/venue freshness, reconciliation, protection, disk and backup health; acknowledgement never clears a fault; alerts carry no secrets and no controls | WP-P0-26, WP-P0-27 | Per deployed host: external heartbeat and the named health checks, read-only surfaces only, with an alert path that carries no secrets and no controls | `None accepted` | `—` | `—` | Any monitoring or alert-path outage or change; any host, service or notification-channel change; an acknowledgement never clears the underlying fault | `BLOCKED` — no active live monitoring or alerting; Phase-Watch inactive, Telegram deployment held; `Restart=no` with no systemd install enablement is deliberate, so an outage could go unnoticed |
| 14 | Human approval | the single live signature; sub-live eligibility is automatic and takes no signature | Baris alone | Per strategy and per capital increase: the **one** explicit live signature. Sub-live eligibility is automatic and takes no signature | `None accepted` | `—` | `—` | Any hard row falling to `UNKNOWN`, `BLOCKED` or `EXPIRED`; any strategy, capital, venue or host change; a serious incident | `UNKNOWN` — none exists |

**Standing register blockers that cut across rows** (repository evidence, recorded 2026-08-23 from
research tickets #105 and #106 — no live inspection is claimed): the deployed Bridge runs **schema
v4**, so the v5–v9 safety mechanisms are code-complete and tested but **inactive** on that deployed
database; **deployment execution evidence is stranded off master and master carries stale deployment
wording**; and there is **zero functioning CI** — OPS-C (WP-P0-27) is planned and unbuilt, so no check
named above currently runs automatically. **These are blockers. They are not authorization to repair
them.**

