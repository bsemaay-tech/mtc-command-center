# Remaining task register — host-labelled — 2026-08-16

Built under `OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`. This is the
canonical Bridge progress table; it replaces every prior remaining-hours claim.
**The retired figures (10–20, 15–25, 41.5–77.5, 60–70 h) must not be quoted** —
they mixed hosts, counted obsolete Pathscope critical-path work, counted
already-completed staging work, and carried rows without sourced estimates.

Labels: host ∈ {GATEA-STAGING, LOCAL RELEASE, KVM2/HOSTINGER, OWNER};
state ∈ {DONE, REUSABLE-NOT-TRANSFERABLE, OPEN, UNKNOWN, REMOVED}.
Hours: `measured` = clocked on this machine; `forecast` = estimate, so marked.
CodeBurn figures are local estimates, not invoices or account balances.

**No remaining-hours total is published in this version.** Per the approved
contract, a range is published only after (a) current-release acceptance
completes and (b) the read-only KVM2 inventory replaces the UNKNOWN rows.

## LOCAL RELEASE (this PC, repo work)

| Row | State | Evidence / note |
|---|---|---|
| Bridge suite-anomaly repairs | DONE | T1 accepted at `7d4e9a96` (audit committed on branch tip). |
| Merge runbook + input refresh `W := 7d4e9a96` | DONE | `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md` + `..._INPUT_REFRESH_2026-08-16.md`; readiness verified read-only. |
| Integration merge executed (worktree `C:\BRIDGE_RELEASE_INTEGRATION_20260815`) | OPEN → in progress 2026-08-16 | §2.1–§5.1 complete: 33/33 blob fence PASS, 32-path scope PASS, credential parity with Gate-A PASS (7 paths/17 occurrences — runbook §5.1 path list had an authoring defect, corrected against live Gate-A). Suite running. |
| Full integrated suite `1360 passed, 1 warning` | OPEN | Running at time of writing; result recorded in the execution record. |
| Merge commit + execution record | OPEN | After suite; runbook §6. |
| Tier-required acceptance of integrated candidate | OPEN | T0 pair (exact `claude-opus-5` + `gpt-5.6-sol`, xhigh) on the release diff; Codex `secondary` probed live 2026-08-16. |
| Two-commit chain V2 re-audit | OPEN | T1; kickoff `C:\tmp\lane_kick\AUD_TC2.md`; pin subject bytes first. Feeds Stage-1 freeze. |
| Prerequisite gate 2 re-derivation | UNKNOWN | Must be independently re-derived at freeze-prerequisite review; removing Pathscope did not close it. |
| Packet-9 policy grammar review + producer sign-off | OPEN | T2 review; producer blocked on Lead sign-off fields. |
| Stage-1 freeze chain (two-commit, Option A) | OPEN | Waits on chain V2 re-audit + gate-2 re-derivation; grant #6 binds only to the final commit. |
| Audit 2 (6 h hard cap, metered) | OPEN | Blocked behind freeze; both sessions metered per owner §4. |
| WP-A + final freeze + Audit 3/Gate 6 | OPEN | Only as required by approved policy and exact tier. |
| Release-evidence lock contract defect (`release_evidence.py` names `requirements.txt`) | OPEN | Needed before its manifest is current dependency evidence; T1-scale local fix. |
| Pathscope (all critical-path work) | REMOVED | Owner §6: supplemental-with-disclosure; sixth cycle forbidden. |
| Privileged mutation-denial channel (audit/build) | REMOVED | `PRIVILEGED_CHANNEL_LOAD_BEARING_DECISION_2026-08-16.md`; design retained as reference. |

## GATEA-STAGING (local Hyper-V VM, disposable)

| Row | State | Evidence / note |
|---|---|---|
| Hardened Ubuntu deployment pattern | REUSABLE-NOT-TRANSFERABLE | Candidate `2ce41e34` installed 2026-08-08, ran DISARMED on Hyperliquid TESTNET 2026-08-09→11 (2 d 13 h), clean stop. Proves the recipe; transfers **no acceptance** to the current candidate or to KVM2. |
| Eight channel facts | DONE | Observed 2026-08-16; mutation-denial control intentionally absent (see channel decision). |
| Fresh current-candidate staging checks | OPEN (scope TBD) | Decide after current-release acceptance which checks are still load-bearing; a single rehearsal install of the accepted release is recommended but not yet committed to. |
| VM state | DONE (parked) | `Off`, checkpoint `GATEA-STAGING-CH1-PRECHANGE-V1` retained. |

## KVM2 / HOSTINGER (the real deployment target)

**Live-verified 2026-08-16 (`KVM2_READONLY_INVENTORY_2026-08-16.md`): the host
is a clean hardened Ubuntu 24.04.4 baseline with NOTHING bridge-related
installed** — `/opt` empty, SSH-only firewall, no app processes, no backups or
monitoring. "Nothing is installed" is now an observed fact, not an inference.

| Row | State | Evidence / note |
|---|---|---|
| Identify exact VPS + safe access route | DONE (2026-08-16) | Host `152.239.123.231` (host key pinned in local known_hosts, all three types); identity `~/.ssh/hostinger_kvm2`; principal `baris` per local shell history. Host-key verification succeeds with explicit known_hosts path. No secret displayed. |
| Inventory OS/services/files/firewall/listeners/storage/backups/monitoring | DONE (2026-08-16) | `KVM2_READONLY_INVENTORY_2026-08-16.md` — owner loaded key into ssh-agent; full read-only sweep, no config change, no secret displayed. Host `srv1856225`, clean baseline, SSH-only surface, monarx-agent on loopback, no backups/monitoring. |
| Host-specific deployment + rollback plan | DRAFTED (2026-08-16) | Skeleton in the inventory record from observed facts + proven GATEA recipe; candidate `62bf661b`. Execution needs clause-6 owner authorization. |
| Baseline reproduction, archive of existing state | OPEN | Only after separate configure/install authorization. |
| Masked DISARMED install of exact accepted release | OPEN | Root-owned, immutable, pinned venv, exact commit path; masked/unenabled/unstarted. Separate authorization required. |
| Pre-start verification (identity, permissions, writable paths, firewall, closed listeners) | OPEN | — |
| First DISARMED start + operational checks | OPEN | Separate authorization required. |
| Clean stop, logs, monitoring, backup, restore, rollback verification | OPEN | — |
| KVM2 Phase-2 contracts V3 independent review | OPEN | T2; verdicts of record are V2 (0/10 accept); V3 unreviewed. |

## OWNER

| Row | State | Note |
|---|---|---|
| KVM2 configure/install/start authorization | OPEN | Presented as one exact plan after inventory + release acceptance (contract clause 6). |
| TESTNET agent wallet provisioning + TESTNET activation | OPEN | Deferred by owner decision (2026-08-15 §D4); own explicit authorization + safe secret channel; no value ever in repo/chat. |
| Pre-cutover archive execution | OPEN | Owner runs it on the retiring machine per §5 procedure draft. |
| Risk-state continuity | DONE (decided) | Fresh reset selected (2026-08-15 night §D5); fail-closed preserve-or-block proof still required at cutover. |
| Mainnet / real money / ARM / orders | FORBIDDEN | Unchanged. |

## Hours

- Measured to date: owner-ratified ~55 h through 2026-08-13, plus unratified
  overrun since (not summed here — needs the CodeBurn/ledger pass).
- Forecast: **not published in this version** by contract.
