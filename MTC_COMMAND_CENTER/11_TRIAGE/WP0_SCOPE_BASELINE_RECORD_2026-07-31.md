# WP-0 — SCOPE AND BASELINE REVIEW (2026-07-31)

**Work package:** WP-0 of the accepted 50-Hour DISARMED Safety MVP plan.
**Budget:** 2 h. **Status:** COMPLETE.
**Lead Orchestrator / acceptance authority:** Claude `claude-opus-5`.

## 0. Authorisation basis

Execution authority for WP-0 and all downstream work packages comes from the standing owner
authorisation `11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`, not from a point-in-time
approval. That document also supersedes the plan's §23c/§39-10 actor assignment **for this
execution only**: Claude is Lead Orchestrator and sole acceptance authority; Codex CLI
`gpt-5.6-sol` is the counterpart flagship implementer. No safety, testing, scope, audit, model, or
evidence requirement is weakened by that role swap.

The same document grants, in advance, the three approvals the plan places behind separate future
owner gates (WP-V deployment approval, the ARM gate, the first TESTNET paper order). Every
objective prerequisite in the Gate A / Gate B / Gate C checklists still applies in full.

## 1. Plan artifact identity — VERIFIED

| Item | Value |
|---|---|
| Path | `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md` |
| Git blob | `9ecae648701fea832b1ad2fa5be2833b9936edf5` |
| Blob size | 85 016 bytes |
| **SHA-256 of committed blob** | **`a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee`** |
| Accepted hash in the audit record | `a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee` |
| Match | **YES** |

Hashed from the committed blob (`git show origin/master:<path> | sha256sum`), never from the
working copy. The on-disk file hashes differently because of CRLF conversion on checkout; that
hash is not the artifact identity and is not used anywhere in this programme.

The plan document is **not edited**. Its accepting verdict is bound to `a07c90cc…`; the eight
optional nits recorded in `PLAN50H_REPAIR_AUDIT_CYCLE_2026-07-30.md` remain deliberately
unapplied.

## 2. Baseline — RE-BASELINED TO LIVE `origin/master`

| Ref | Commit | Note |
|---|---|---|
| Plan §Executive Summary / §34 baseline | `3cccc4c283cd1faa78bab2dbc4ae90fc72733d13` | stale as of this record |
| Older note | `9b8a908a` | stale |
| **Live `origin/master` (fetched 2026-07-31)** | **`561be664d3d46103d68023a9951065343e772f1e`** | **frozen WP-0 baseline** |
| Local `master` | `8721bce0` | stale; not used |
| Session HEAD | `60536da7` on `feature/donchian-crypto-ladder` | in sync with its remote |

### 2.1 Delta `3cccc4c2 → 561be664` — DOCUMENTATION ONLY

14 commits. Files changed by top-level area:

| Area | Files |
|---|---:|
| `MTC_COMMAND_CENTER/11_TRIAGE` | 57 |
| `MTC_COMMAND_CENTER/09_DOCS/ADR` | 14 |
| `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM` | 12 |
| `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow` | 9 |
| `MTC_COMMAND_CENTER/_AI_MEMORY` | 7 |
| `MTC_COMMAND_CENTER/00_INBOX/USER_INTAKE` | 6 |
| `AGENTS.md`, `.gitignore`, `09_DOCS/AI_TOOLING` | 3 |

Verified explicitly:

```
git diff --name-only 3cccc4c2..origin/master -- IBKR_PAPER_BRIDGE   → (empty)
git diff --name-only 3cccc4c2..origin/master -- '*.py'              → (empty)
```

**The Bridge tree is byte-identical between the plan's assumed baseline and the live
`origin/master`.** Re-baselining to `561be664` therefore invalidates no plan assumption about
code. Only `.gitignore` and Markdown changed.

**Recorded delta decision:** WP-0 freezes the baseline at `561be664` for all documentation and
record work, and at the identical Bridge tree for all implementation work. No re-audit of prior
accepted artifacts is triggered by the re-baseline.

## 3. FINDING F-0-1 — the "old-base Linux package" is already merged

**The plan's premise that a Linux package must be *ported* from a divergent old-base commit is
factually stale.** Verified:

```
git merge-base --is-ancestor 6fe0130f origin/master   → YES (ancestor)
git diff --stat 6fe0130f origin/master -- IBKR_PAPER_BRIDGE/deploy \
    IBKR_PAPER_BRIDGE/requirements.{in,lock,txt} \
    IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py \
    IBKR_PAPER_BRIDGE/tests/test_deployment_wrapper.py  → (empty — identical)
```

`6fe0130f45f3c821e230ee30d1e61f548741a6a1` is an **ancestor** of both `3cccc4c2` and `561be664`.
The complete Linux deployment package is already present on `origin/master`, byte-identical to the
old-base version:

```
IBKR_PAPER_BRIDGE/deploy/linux/{install,package,rollback,verify}.sh
IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py
IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template
IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template
IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template
IBKR_PAPER_BRIDGE/requirements.{in,lock,txt}
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py       (34 tests)
IBKR_PAPER_BRIDGE/tests/test_deployment_wrapper.py     (1 test)
```

### Disposition — NOT a blocker; WP-L shrinks

This is a stale premise, not a safety defect, and it makes WP-L strictly **smaller and safer**:

* the plan's binding instruction "No wholesale merge or cherry-pick" is trivially satisfied —
  there is nothing to merge or cherry-pick, and **no cross-branch Git operation will be performed
  in WP-L**;
* the plan's WP-L deliverable (a semantic-port manifest with rationale and static verification,
  then Ubuntu revalidation of every listed path) remains fully executable and still meaningful;
* what changes is only the *nature* of Phase 1: from "select and port paths from a divergent
  branch" to "verify that the already-merged package is semantically correct against the current
  head, and correct any path the merged P1-001..008 work invalidated".

The plan document is not edited. This finding is reported to the owner in the final deliverable.

The plan's caveat that the package is **builder-self-QA only, independently unaccepted, and not
Ubuntu-staged** is unaffected and remains binding — being on `master` is not acceptance.

## 4. FINDING F-0-2 — TS-P1-009B S2 blockers reproduced on real source

The Lead independently located both terminal blockers in the real tree at
`C:/TSP1009B` (branch `feature/ts-p1-009b-evidence-epoch`, HEAD
`678e8b946e34a55eca85f88d2e6ca54514b182f7`). These are not restatements of an implementer report.

### B1 — sub-1e-12 `trades.exit_px` / `pnl` tampering evades detection

`IBKR_PAPER_BRIDGE/bridge/store/db.py:6522-6551`, inside
`_assert_kill_flatten_closure_in_tx`. The durable `trades` row is compared to the recomputed
expectation with a **tolerance band**:

```python
or not math.isclose(trade_exit_px, expected["exit_px"], rel_tol=0.0, abs_tol=1e-12)
or not math.isclose(trade_pnl,     expected["pnl"],     rel_tol=0.0, abs_tol=1e-12)
```

while the parallel `TRADE_CLOSED` decision-payload comparison 10 lines above (`db.py:6513-6518`)
is **exact**, with a type check:

```python
type(payload[key]) is type(expected_payload[key])
and math.isfinite(payload[key])
and payload[key] == expected_payload[key]
```

`expected["exit_px"]` and `expected["pnl"]` are derived deterministically from the same durable
fill aggregate on every evaluation, so exact equality is achievable and the tolerance buys
nothing. The band is a live evasion window: a `trades.exit_px` or `trades.pnl` perturbation
smaller than 1e-12 absolute passes the closure assertion, and the episode proceeds to ACK/DISARM
on tampered durable evidence.

Related but semantically distinct, and to be assessed separately rather than changed reflexively:
`db.py:6410-6412` applies `abs_tol=1e-12` to `exit_qty` vs `entry_qty`, which is an aggregate
*completeness* check, not an evidence-integrity check.

### B2 — stale recovery commits the lifecycle close before the epoch rejection

`IBKR_PAPER_BRIDGE/bridge/engine/orders.py:1599-1702`, in
`_recover_applied_kill_flatten_lifecycles`:

```
1662   self._assert_kill_epoch_active()      # pre-check
1663   self._ingest_fill(...)                 # DURABLE WRITE — commits the lifecycle close
1680   self._assert_kill_epoch_active()      # post-check — too late
```

The epoch assertion is a **separate statement** on either side of the durable write rather than a
condition *of* the write. If the epoch is invalidated between the pre-check and the commit inside
`_ingest_fill`, the trade close is already durable when the post-ingestion assertion finally
raises `_KillEvidenceFault`. A superseded recovery process can therefore write a lifecycle close
that a newer epoch has already revoked — the exact failure class the epoch contract's
`31_KILL_EVIDENCE_EPOCH_CONTRACT.md` §Objective item 2 exists to prevent.

The required shape is CAS-fenced: epoch ownership must be validated **inside the same durable
transaction** as the lifecycle-close write, so a stale epoch rolls the write back instead of being
detected after commit.

### S2 commit chain

| Commit | Date | Meaning |
|---|---|---|
| `8d004590` | — | **S1 accepted** (`fix(bridge): close F5 durable kill precommit gap`) |
| `85e5096d` | 2026-07-29 16:33 | S2 initial implementation |
| `ad179740` | 2026-07-29 17:11 | S2 repair round 1 |
| `94e0897b` | 2026-07-29 18:21 | S2 repair round 2 |
| `678e8b94` | 2026-07-29 18:47 | S2 repair round 3 — **terminally BLOCKED** |

S3: unstarted. Diff `8d004590..678e8b94` = 3 files, +1859/−13 (`orders.py`, `db.py`,
`test_engine_dryrun.py`).

## 5. Gate-1 follow-up — NEW S2 repair cycle authorisation

Recorded per the plan §15 requirement and §16 Hard Stop.

* The historical S2 repair loop is **closed and exhausted**; its three rounds are spent.
* The standing owner authorisation opens a **NEW** owner-authorised repair/re-audit cycle for S2.
  This is explicitly *not* a fourth round of the exhausted historical cycle.
* The new cycle carries its own bound: **maximum three non-accepting rounds.** After a third
  non-accepting verdict in the new cycle, stop, report to the owner, and do not proceed to WP-L.
* Authorisation source: standing prompt, not a point-in-time approval — recorded here by name as
  the prompt requires.

## 6. Frozen scope — path allowlist

### 6.1 WP-S allowed paths (exhaustive)

| Path | Why |
|---|---|
| `IBKR_PAPER_BRIDGE/bridge/store/db.py` | B1 lives here; S3 durable surface |
| `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` | B2 lives here |
| `IBKR_PAPER_BRIDGE/bridge/broker/base.py` | only if S3 requires the worker-safe guard interface |
| `IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py` | S2/S3 contract tests |
| `IBKR_PAPER_BRIDGE/tests/test_store.py` | durable-store contract tests |
| `IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md` | contract text for S2/S3 |
| `MTC_COMMAND_CENTER/11_TRIAGE/**` | records only |
| `MTC_COMMAND_CENTER/_AI_MEMORY/{GLOBAL_HANDOFF,NEXT_STEPS}.md` | Gate-7 write-back only |

Touching `bridge/engine/engine.py` or `bridge/broker/hyperliquid.py` requires an explicit
recorded Lead scope extension with the reason; it is not pre-authorised.

### 6.2 Forbidden in every work package

* `*.pine`, `MTC_COMMAND_CENTER/01_PINE`, `MTC_V2`, any `parity` path,
  `MTC_COMMAND_CENTER/02_MTC_BACKTEST`, `MTC_COMMAND_CENTER/07_ADAPTERS`.
* `IBKR_PAPER_BRIDGE/bridge/engine/strategies/**` and
  `IBKR_PAPER_BRIDGE/config/strategies/**` — strategy behaviour is frozen.
* **Any risk threshold value** in `IBKR_PAPER_BRIDGE/config/bridge.yaml` — position size,
  leverage, daily-loss, drawdown, equity floor, exposure, liquidation. These are owner-defined.
  Wiring may be repaired; values may never be invented or changed.
* Any credential, wallet, key, endpoint secret, or private infrastructure identifier — never
  written to the repo, a report, or an LLM prompt.
* `origin/master` history rewriting, force-push, `git reset --hard`, `git add .`, stashing
  unrelated work, deleting unclassified files.

## 7. Immutable integration / release plan

1. **WP-S branch base.** WP-S continues the accepted S1 stack, so its branch is cut from
   `678e8b94` — the exact artifact the plan and the authorisation name as terminally blocked —
   **not** from `origin/master`. This is recorded as a deliberate deviation from the
   authorisation's generic "branch from `origin/master`" instruction, and it is safe because
   `merge-base(678e8b94, origin/master) = 3cccc4c2` and the Bridge tree is byte-identical between
   `3cccc4c2` and `561be664` (§2.1). Branching from `678e8b94` is therefore equivalent to
   branching from `origin/master` plus the accepted S1 stack, with zero Bridge conflict surface.
2. **Isolation.** Each work package gets its own branch and its own `git worktree`. The shared
   checkout is never used for package implementation. A hook flips `HEAD` back to `master` between
   tool calls, so every commit is issued as one inline `checkout; add <explicit paths>; commit`.
3. **Git ownership.** The Lead performs every Git operation. Codex's sandbox has read-only `.git`
   and cannot run Git; commit/push/fetch/merge is never delegated.
4. **Checkpoint freeze.** Every audit is run against an exact committed SHA, and every artifact
   identity is taken from the committed blob, never the working copy.
5. **Merges to `master`.** `git checkout master` fails in the shared checkout (untracked files
   would be overwritten). Merges are performed in a temporary `git worktree`, pushed, and the
   worktree removed — the pattern that landed PR #34.
6. **Acceptance never carries forward.** Any post-audit change requires a new exact SHA and a
   re-run of the affected audit on that exact artifact.

## 8. Linux semantic-port manifest (WP-L Phase 1 input)

Given F-0-1, the manifest lists what must be **verified**, not copied. All five minimum paths
named in plan §17 are present on `origin/master` and independently unaccepted.

| # | Plan §17 minimum path | Artifact on `origin/master` | Static evidence today | WP-L Phase 1 action |
|---|---|---|---|---|
| 1 | systemd service unit (startup, restart, graceful shutdown) | `deploy/linux/systemd/mtc-bridge-first-start.service.template`, `…-steady.service.template` | `test_first_start_unit_is_separate_masked_design_and_restart_no`, `test_steady_unit_is_separate_restart_enabled_and_not_enableable`, `test_installer_never_installs_the_steady_profile` | re-verify both templates against current head; confirm the steady profile stays inert |
| 2 | signal-handler integration (SIGTERM → DISARMED shutdown) | `bridge/app.py:72-83` lifespan; unit `KillSignal=SIGTERM`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL` | **none — see §9 gap I-R4** | assess; no code change without Lead sign-off |
| 3 | path / file-permission assumptions | `deploy/linux/install.sh`, `lib/common.sh`, `logrotate/mtc-bridge` | `test_canonical_paths_ownership_modes_and_no_symlink_contract_are_structural`, `test_payload_tree_rejects_symlinks_and_special_entries` | re-verify path constants against current head |
| 4 | environment isolation (env vars, config loading) | `deploy/linux/env/mtc-bridge.env.template`, `bridge/app.py` `MTC_BRIDGE_STATE_DB` handling | `test_state_path_default_is_preserved_and_posix_env_override_resolves`, `test_state_path_cli_wins_and_bad_values_fail_closed`, `test_env_template_contains_names_and_comments_but_no_definitions` | re-verify; confirm the template still carries names only, no values |
| 5 | dependency installation on Ubuntu (pip lockfile, apt) | `requirements.{in,lock,txt}`, `deploy/linux/verify_lock.py`, `install.sh` | `test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency`, `test_lock_generation_contract_targets_python_312_linux_with_hashes`, `test_installer_uses_per_sha_venv_hashes_and_binary_wheels_only` | re-verify the lock still covers every direct dependency at current head |

**Nothing is ported. Nothing is cherry-picked. No cross-branch Git operation occurs in WP-L.**

All 35 supporting tests are **static/structural** — they parse the shell scripts, unit templates
and lockfile on Windows. They prove *design*, not Ubuntu execution. Executed-Ubuntu evidence for
every one of these paths is deferred to WP-L Phase 2 on the Gate-A-authorised staging host, per
plan §17 and the §18 Staging Host Lifecycle. **No Ubuntu execution of any kind before Gate A.**

## 9. DISARMED VPS invariant map (plan §19 requirement)

Gap classes per plan §19: **COVERED** (existing code + test prove the invariant on Ubuntu — no new
work) · **SMALL-GAP** (narrow missing test or trivial wiring fix — contingency hours only, after
explicit Lead sign-off per gap) · **FULL-TASK** (needs a new P1-010..012 / canonical Master Roadmap
Phase 2 / Phase 4 task — Deferred Delivery Stage 2, or BLOCK if indispensable).

A fourth operational state is recorded honestly and is **not** a plan gap class:
**COVERED-STATIC** — the invariant is proven by tests that execute on Windows against Linux
artifacts, so design is proven but Ubuntu execution is not. Every COVERED-STATIC row must be
promoted to COVERED by executed-Ubuntu evidence during WP-L Phase 2 / WP-I staging / WP-A. This
distinction is the whole reason the plan retains the staging host through WP-A; collapsing it
would be fabricating evidence.

### 9.1 §5.1 Order Safety

| Invariant | Evidence | Class |
|---|---|---|
| deterministic request identity | `docs/23_ORDER_IDENTITY_CONTRACT.md`; `tests/test_order_identity.py` (69) | COVERED |
| no blind retry after ambiguous submission | `docs/24_UNKNOWN_SUBMISSION_CONTRACT.md`; `tests/test_unknown_submission.py` (23); `test_kill_transport_unknown_replays_same_identity_query_only`, `test_kill_write_not_applied_response_without_direct_query_never_resends` | COVERED |
| duplicate requests cannot create duplicate exposure | `test_drill_duplicate_candle_creates_one_decision_and_order`, `test_drill_disconnect_reconnect_dedupes_to_one_order`, `test_duplicate_final_fill_is_idempotent_across_restart` | COVERED |
| partial fills protected or safely flattened | `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md`; `tests/test_partial_fill_protection.py` (134) | COVERED |
| deterministic order-state transitions | `docs/22_ORDER_STATE_CONTRACT.md`; `tests/test_order_state.py` (63) | COVERED |
| unknown order state blocks new risk | `test_active_partial_recovery_blocks_readiness`, `test_arm_is_refused_while_a_recovery_is_active`, `test_failed_full_gate_blocks_new_entry_while_persisted_armed` | COVERED |
| kill/disarm idempotent | `test_kill_duplicate_reuses_episode_and_action_without_second_write`, `test_kill_flatten_unknown_replay_is_query_only_after_one_write` | COVERED |
| killed/disarmed state survives restart | `bridge/app.py:109-110` (non-KILLED forced to DISARMED at startup); `test_kill_persists_across_restart`, `test_gates_persist_across_restart`, `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | COVERED |

### 9.2 §5.2 Reconciliation

| Invariant | Evidence | Class |
|---|---|---|
| deterministic local↔exchange comparison | `docs/26_FULL_RECONCILIATION_CONTRACT.md`; `tests/test_reconciliation.py` (51) | COVERED |
| orders / fills / positions reconciled | same suite | COVERED |
| balances / equity reconciled where required | `docs/27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md`; `tests/test_risk.py` (38) | COVERED |
| pending actions represented | `test_cancel_reservation_persists_pending_cancel_before_unknown_io` | COVERED |
| incomplete snapshot is unhealthy | `test_light_reconcile_alone_never_grants_full_readiness`, `test_a_restart_interrupted_attempt_makes_readiness_false` | COVERED |
| stale reconciliation blocks new risk | `test_arm_requires_fresh_reconcile_evidence`, `test_full_reconcile_freshness_bound_is_derived_from_the_cadence` | COVERED |
| foreign state not auto-mutated | `test_kill_cancels_owned_entry_and_preserves_foreign_order`, `test_kill_ignores_another_runs_valid_filled_history`, `test_kill_mixed_or_opposite_position_never_flattens` | COVERED |

### 9.3 §5.3 Risk

| Invariant | Evidence | Class |
|---|---|---|
| realised PnL / equity / daily-loss on the real execution path | `docs/28_FULL_TSP1007_RISK_CONTROLS.md`; `tests/test_risk.py`, `tests/test_interim_risk_wiring.py` (31) | COVERED |
| drawdown limits | `RiskConfig.max_intraday_drawdown_pct` wired from `config/bridge.yaml`; `tests/test_risk.py` | COVERED |
| exposure / leverage / liquidation distance | `docs/29_TSP1008_EXPOSURE_LEVERAGE_LIQUIDATION.md`; merged TS-P1-008 | COVERED |
| position state | `tests/test_order_lifecycle.py`, `tests/test_reconciliation.py` | COVERED |
| risk fails closed on incomplete/stale input | `test_equity_stop_reset_rejects_substituted_policy_and_stale_evidence`, `test_any_nonzero_reconciled_position_blocks_a_new_entry` | COVERED |

### 9.4 §5.4 Recovery

| Invariant | Evidence | Class |
|---|---|---|
| process restart | `test_kill_restart_after_reservation_is_query_only`, `test_close_and_decision_rollback_then_exact_fill_restart_recovers` | COVERED |
| restart during submission / unknown submission | `test_broker_exception_leaves_reserved_restart_blocks`, `tests/test_unknown_submission.py` | COVERED |
| restart during partial fill | `tests/test_partial_fill_protection.py`; `test_kill_partial_flatten_never_mints_second_close` | COVERED |
| reconnect | `test_drill_ws_death_triggers_auto_reconnect`, `test_drill_ws_death_survives_three_minute_outage_within_retry_budget` | COVERED |
| stale WebSocket data | `test_drill_data_stale_auto_disarms`, `test_data_stale_emits_and_disarms_once`, `test_engine_status_window_down_after_staleness` | COVERED |
| REST fallback | `test_kill_exact_ioc_query_fill_without_websocket_fill_reaches_safe_flat_and_ack` | COVERED |
| database backup / restore | `tests/test_wal_state_bundle.py` (41) — `test_create_then_verify_round_trip`, `test_manifest_records_online_backup_and_both_ends_integrity` | COVERED |
| malformed / corrupted database copies | `test_verify_fails_closed_on_a_corrupt_bundle_database`, `test_verify_detects_bundle_hash_mismatch`, `test_corrupt_schema_version_string_fails`, `test_future_or_corrupt_schema_version_fails_closed` | COVERED |
| recovery checkpoints | `tests/test_engine_dryrun.py` kill-episode checkpoint set | COVERED |

### 9.5 §5.5 Security and Provenance

| Invariant | Evidence | Class |
|---|---|---|
| dependency locking + inventory | `requirements.lock`; `test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency` | COVERED-STATIC → WP-I |
| SBOM-equivalent evidence | derived from the hashed lock | COVERED-STATIC → WP-I |
| secret scanning | `test_program_tree_has_no_private_host_ip_user_or_key_path`, `test_env_template_contains_names_and_comments_but_no_definitions`, `test_secret_safe_output`, `test_manifest_leaks_no_path_or_identifier` | COVERED-STATIC → WP-I |
| outbound-network inventory | not yet produced as an artifact | **SMALL-GAP** — WP-I deliverable, inside WP-I's 6 h |
| release / runtime identity | `tests/test_release_evidence.py` (13), `tests/test_runtime_baseline.py` (14) | COVERED |

### 9.6 Plan §19 minimum DISARMED restart invariants

§19 tightens these four: **SMALL-GAP is not available**. Anything not COVERED is FULL-TASK →
Deferred Delivery Stage 2 or BLOCK.

| ID | Invariant | Evidence | Class |
|---|---|---|---|
| I-R1 | restart while flat and DISARMED → starts DISARMED, no order submitted | `bridge/app.py:109-110` forces `app_state=DISARMED` on every start unless `KILLED`; ARM is an explicit API action; `test_gates_persist_across_restart` | COVERED (code+test) / COVERED-STATIC on Ubuntu → **WP-A must execute on the staging host** |
| I-R2 | killed/disarmed state persistent after restart | `test_kill_persists_across_restart`, `test_killed_alive_is_interrupted`, `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | COVERED (code+test) / COVERED-STATIC on Ubuntu → **WP-A** |
| I-R3 | database state-file integrity after restart | `tests/test_wal_state_bundle.py` (41); `test_bundle_never_contains_a_wal_shm_trio`, `test_invariants_preserve_risk_and_history` | COVERED (code+test) / COVERED-STATIC on Ubuntu → **WP-A** |
| I-R4 | SIGTERM → clean DISARMED shutdown, no dangling state | `bridge/app.py:72-83` lifespan `finally: await engine.stop()`; unit `KillSignal=SIGTERM`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`. `engine.stop()` (`engine.py:228-235`) stops the feed and cancels tasks — it does **not** write a DISARMED state or close the store. **No test asserts SIGTERM/lifespan shutdown leaves no dangling state.** | **OPEN — see below** |

#### I-R4 — Lead assessment, recorded rather than resolved

The safety property is **substantially carried by the startup fail-closed at `app.py:109-110`**,
not by shutdown-time disarm: whatever `app_state` is left in the database, the next start forces
`DISARMED` unless it is `KILLED`. A dirty shutdown therefore cannot produce an armed restart.

What is genuinely unproven is the *"no dangling state"* half — that the process exits inside
`TimeoutStopSec=45` without `FinalKillSignal=SIGKILL`, and that the SQLite WAL is left clean.
Both are **Ubuntu-execution facts** that cannot be established on Windows and are exactly what the
retained staging host exists to prove.

**Disposition:** I-R4 is carried into WP-A as the single highest-risk minimum restart invariant,
to be resolved by executed evidence on the Gate-A-authorised staging host. It is **not**
pre-classified FULL-TASK and it is **not** silently treated as COVERED. If WP-A's Ubuntu execution
shows the process does not shut down cleanly, §19 forbids SMALL-GAP treatment for this invariant
and the outcome is FULL-TASK → Deferred Delivery Stage 2 or BLOCK, reported to the owner. No code
change to the shutdown path is authorised on the strength of this record alone.

### 9.7 Plan §19 minimum reconnect / stale-data invariants

| Invariant | Evidence | Class |
|---|---|---|
| WebSocket disconnect while DISARMED → no order submitted | `test_drill_ws_death_triggers_auto_reconnect`, `test_drill_disconnect_reconnect_dedupes_to_one_order`; entries require ARM | COVERED (code+test) → WP-A executes on Ubuntu |
| stale feed / timestamp gap while DISARMED → no order submitted | `test_drill_data_stale_auto_disarms`, `test_data_stale_emits_and_disarms_once` | COVERED (code+test) → WP-A executes on Ubuntu |
| reconciliation after reconnect → clean output, no positions in DISARMED | `tests/test_reconciliation.py`; `test_active_recovery_suppresses_ordinary_reconcile_repair` | COVERED (code+test) → WP-A executes on Ubuntu |

### 9.8 Map summary

| Class | Count |
|---|---:|
| COVERED (code + test) | 30 |
| COVERED-STATIC — needs executed-Ubuntu promotion in WP-L Ph2 / WP-I / WP-A | 3 (§5.5) + all Ubuntu-execution rows |
| SMALL-GAP (contingency, per-gap Lead sign-off) | 1 — outbound-network inventory artifact (§5.5), absorbed by WP-I's own 6 h |
| FULL-TASK | 0 |
| OPEN, carried to WP-A | 1 — I-R4 SIGTERM clean-shutdown evidence |

**No FULL-TASK gap was found. No new P1-010..012 / canonical Master Roadmap Phase 2 / Phase 4 task
is scheduled.** The one SMALL-GAP is an artifact WP-I already owes under its own scope, so it does
not draw contingency.

## 10. Test baseline

Environment: Python 3.14.2, pytest 9.0.2, `IBKR_PAPER_BRIDGE` as CWD.
`IBKR_PAPER_BRIDGE/TSP1009B.pytest_tmp_s1r1/` is ACL-locked and untracked — plain `pytest` aborts
collection with `PermissionError`, so every run uses `--ignore=TSP1009B.pytest_tmp_s1r1`.

Collection at `678e8b94`: **1115 tests collected**.

Full suite at `678e8b94`, `python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly`:

```
2 failed, 1113 passed, 3 warnings in 115.62s
FAILED tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
FAILED tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history
```

**This is the frozen WP-S entry floor: 2 failed / 1113 passed.** Both failures are pre-existing and
unrelated to the S2 blockers — the 009B branch touches only `orders.py`, `db.py` and
`test_engine_dryrun.py`, neither failing test among them.

| Failure | Cause | Disposition |
|---|---|---|
| `test_canonical_ledger_and_all_three_row_fixtures_validate` | `kvm2_ledger_validator.LedgerValidationError: publishable artifact hash mismatch` against `11_TRIAGE/KVM2_PROGRAM/evidence/` | stale KVM2 programme ledger, out of WP-S scope; carried in the floor |
| `test_invariants_preserve_risk_and_history` | asserts `inv["schema_version"] == "2"`, store reports `"4"` | stale test expectation against the current default schema v4; out of WP-S scope; carried in the floor |

WP-S may not regress this floor. Neither failure may be "fixed" opportunistically inside WP-S —
both are outside the frozen allowlist in §6.1.

## 11. Hour accounting — WP-0

| Activity | Hours |
|---|---:|
| Canonical pre-read (AGENTS, START_HERE, AI_RULES, plan, plan-audit record, handoff, next-steps) | 0.5 |
| Live repo verification, fetch, re-baseline, delta proof, F-0-1 | 0.4 |
| S2 blocker reproduction on real source (F-0-2) | 0.4 |
| Invariant map compilation + semantic-port manifest | 0.5 |
| Record authoring | 0.2 |
| **WP-0 total** | **2.0 / 2 h budget** |

On budget. Approximate AI spend attributable to WP-0: ~$12 (Lead-only; no implementer or auditor
dispatch, no secondary-model delegation).

## 12. Outputs produced (plan §15 checklist)

- [x] Owner-accepted revised plan — artifact identity verified against `a07c90cc…`.
- [x] Gate-1 authorisation for the NEW S2 repair cycle — §5.
- [x] Immutable integration/release plan — §7.
- [x] Exact Linux semantic-port manifest — §8.
- [x] Baseline confirmed and re-based to `561be664`; allowed/forbidden path allowlist frozen — §2, §6.
- [x] DISARMED VPS invariant map with COVERED / SMALL-GAP / FULL-TASK classification — §9.

## 13. Safety statement

No implementation, staging, VPS, deployment, TESTNET, ARM, broker, runtime, or live-capital action
occurred during WP-0. No Ubuntu execution of any kind occurred. No credential, wallet secret, API
key, or private infrastructure identifier was read, written, or sent to any model. No risk
threshold was invented or changed. WP-0 is read-only against the Bridge tree plus this record.
