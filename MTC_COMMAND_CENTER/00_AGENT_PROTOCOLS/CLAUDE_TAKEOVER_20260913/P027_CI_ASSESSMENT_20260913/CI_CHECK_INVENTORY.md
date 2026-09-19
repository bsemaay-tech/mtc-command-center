# CI check inventory — WP-P0-27 (read-only, 2026-09-13)

This file lists every continuous-check named by WP-P0-27, every check that actually runs in repo-root GitHub Actions YAML, and the local guards that look like CI but are not wired. Status values are only:

- **LIVE** — a repo-root workflow file invokes it on a GitHub-hosted runner.
- **DECLARED-BUT-NOT-WIRED** — a script, test module, or policy exists in the tree, and no repo-root workflow invokes it.
- **MISSING** — the plan names it and this checkout has no executable check to run.

A Status cell may append a qualifier after one of those three values (for example "as a **recorded** setting", "LIVE as a workflow; DECLARED-BUT-NOT-WIRED as a required merge check", or "inert nested artifact"). The Vercel row is **NOT VERIFIED** as a repo workflow because no root YAML names it; that qualifier is not a fourth enum member and does not shrink NOT VERIFIED.

This lane did not call GitHub, did not run tests, and did not run Git. Live GitHub ruleset/run state is a record in documents, not a re-measurement. See `REPORT.md` NOT VERIFIED.

Owner routing for this lane: read-only assessment. No workflow was edited.

## How to read the stale "no CI" sentences

Ticket #43 and the WP-P0-27 plan still say the repository has no functioning CI. Those sentences are the 2026-08-23 starting fact, not the 2026-09-13 tree.

- `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md:20` — "Fact: the repo has **no functioning CI at all** (no root workflows; the two `02_MTC_BACKTEST` workflows are inert imported artifacts that never ran here)."
- `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:591` — "the repository currently has **no functioning CI at all** (no root workflows; the two `02_MTC_BACKTEST` workflows are inert imported artifacts that never ran in this repo)."
- `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:594` — "It is planned and unbuilt: the repository has zero functioning CI"

The 2026-09-13 START_HERE instruction for this package is the opposite of repeating that as current fact:

- `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/START_HERE.md:52` — "P0-27 | Preserve existing Bridge tests/protected merge checks. Assess remaining checks individually for implementation or explicit deferral; do not declare no functioning CI or weaken existing checks."

This checkout has three repo-root workflows: `C:/CT13/.github/workflows/ci.yml`, `pine-defang-guard.yml`, `research-gates.yml`. Nested `02_MTC_BACKTEST` YAML is still present and is still not a root workflow.

## Named WP-P0-27 outputs (the remaining-check list)

From `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:593`:

> "repo-root `.github/workflows/` on GitHub-hosted runners (no secrets — the guards are local RED/GREEN fixtures with no venue contact); day-one job running the Bridge suite plus light lint; the progressive required-check policy — **checks required on PRs into master; direct Lead pushes remain allowed (standing delegation unchanged) but a red master run notifies immediately and master never stays red (fix forward or revert)**; failure notification wired (GitHub email day one, the WP-P0-26 paging channel when it lands); the plan guards (WP-P0-10 golden suite, WP-P0-23 no-`alert(`/`alertcondition(` guard, WP-P0-21 admission fixtures, §9.6 parity set, contract tests) plug in as their packages deliver them; the two inert workflows recorded as inert and retired with the Q5 engine, unported."

From the same file `:594`:

> "restore-proof freshness, drill currency, credential-expiry warnings, monitoring health and the guards other packages deliver."

From the same file `:595`:

> "The guards: **block concurrent writers** by checking the shared claim (issue, branch, worktree, paths, live-dependency status) that WP-P0-05's close-out discipline produces, with `SESSION_LOCK` as a checked mirror rather than the sole guard; and **block cleanup whenever ownership, process/scheduled-task dependency or checkout purpose is `UNKNOWN`** — **`UNKNOWN` is a stop, and git cleanliness, pushed state and mtime do not establish liveness.**"

Future job IDs already reserved in prior-lane policy `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md:159-164`: `ops_restore_proof_freshness`, `ops_drill_currency`, `ops_credential_expiry`, `ops_monitoring_health` — "Placeholder only; unbuilt."

## Inventory table

| Check | Where it lives today (file:line) | What it proves | Runs on (event) | Status |
|---|---|---|---|---|
| Bridge suite (Python 3.12) — pytest | `C:/CT13/.github/workflows/ci.yml:44-45` `run: python -m pytest IBKR_PAPER_BRIDGE/tests -q` | Canonical Bridge pytest tree, unfiltered. Entry points listed below. | `pull_request` / `push` to `master` (`ci.yml:3-9`) | LIVE |
| Light lint — compileall | `C:/CT13/.github/workflows/ci.yml:41-42` `run: python -m compileall -q IBKR_PAPER_BRIDGE` | Bridge Python sources compile on CPython 3.12 | same as Bridge job | LIVE |
| Hash-locked Bridge install | `C:/CT13/.github/workflows/ci.yml:36-39` `python -m pip install --require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock` | Day-one job uses the pinned Bridge closure, not an unpinned install | same | LIVE |
| Bridge failure annotation / step summary | `C:/CT13/.github/workflows/ci.yml:47-55` `echo "::error title=Bridge CI failed::..."` and "Master must not remain red" | Failed Bridge job is visible in the GitHub UI; it is not email and not phone paging | `if: ${{ failure() }}` as a later step of the same `bridge` job (`ci.yml:19` job id `bridge`; `:47-48` the failure step) | LIVE |
| Stale-run cancellation (CI) | `C:/CT13/.github/workflows/ci.yml:14-16` `cancel-in-progress: true` | A newer commit for the same PR/ref cancels the older CI run | same triggers | LIVE |
| Pine alert / `alert(` `alertcondition(` empty-allowlist guard | Workflow: `C:/CT13/.github/workflows/pine-defang-guard.yml:19-20` `python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py`. Scanner: `C:/CT13/MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py:9` `ALERT_NEEDLES = (b"alert(", b"alertcondition(")` and `:10` `ALLOWLIST: frozenset[str] = frozenset()`. Also invoked locally by `C:/CT13/MTC_COMMAND_CENTER/tools/repo_guard.ps1:157-168`. | Every `.pine` file in the git root walk contains neither needle, or the job fails. Allowlist is empty. | Workflow `on: push` and `on: pull_request` with no branch filter (`pine-defang-guard.yml:3-5`). Local: when an agent runs repo_guard. | LIVE (CI + local). **Not** a required merge check in recorded policy (see merge-protection section). |
| Research gate — shared risk calculator | `C:/CT13/.github/workflows/research-gates.yml:52-53` `python check_shared_risk_calculator.py` | Offline WP-P0-20 risk-calculator regression fence (`C:/CT13/check_shared_risk_calculator.py:1` "Offline regression fence; expected quantities use exact rational arithmetic.") | `pull_request` / `push` to `master` (`research-gates.yml:16-22`) | LIVE |
| Research gate — market data collector | `research-gates.yml:55-56` `python check_market_data_collector.py` | WP-P0-20 collector checker (stdlib job; workflow header `:13` "Every module here is stdlib-only") | same | LIVE |
| Research gate — UNSIMULATED_CONTROLS manifest | `research-gates.yml:58-59` `python check_unsimulated_controls.py` | Unsimulated-controls manifest fence | same | LIVE |
| Research gate — control-parity checklist v1 | `research-gates.yml:61-62` `python check_control_parity_checklist.py` | Control-parity checklist checker | same | LIVE |
| Research gate — statistical battery v1 | `research-gates.yml:64-65` `python check_statistical_battery.py` | Statistical-battery checker | same | LIVE |
| Research gate — cost-model registry | `research-gates.yml:67-68` `python check_cost_model_registry.py` | Cost-model registry checker | same | LIVE |
| Research gate — evidence class | `research-gates.yml:70-71` `python check_evidence_class.py` | Evidence-class checker | same | LIVE |
| Research gate — allocator import identity (self-test) | `research-gates.yml:73-74` `python check_allocator_import_identity.py --self-test` | Self-test of the import-identity tool, not `--require-bound` acceptance. Tool text `C:/CT13/check_allocator_import_identity.py:12-14` says "the binding this checks for does not yet exist". Token `NOT_BOUND` is defined at `:28`. | same | LIVE |
| Research gate — triage index is current | `research-gates.yml:76-77` `python MTC_COMMAND_CENTER/11_TRIAGE/generate_index.py --check` | `INDEX.md` matches a regenerated git-tracked-or-trackable file set (`generate_index.py:16-18` `git ls-files --cached --others --exclude-standard`; `:61-65` `--check` exits 0 only if byte-identical) | same | LIVE |
| WP-P0-20 acceptance state (report only) | `research-gates.yml:82-92` `if: always()` / `continue-on-error: true` / `python check_p020_acceptance.py \|\| true` | Prints acceptance-harness state into the step summary. Explicitly not a gate: `research-gates.yml:79-81` "The acceptance harness reports state; it is not a gate. It exits non-zero until every criterion is MET, which is correct and is not a CI failure" | same, always, non-blocking | LIVE (report-only; cannot fail the workflow) |
| Research-gates stale-run cancellation | `research-gates.yml:27-29` `cancel-in-progress: true` | Same shape as CI | same | LIVE |
| Required merge check `Bridge suite (Python 3.12)` | Recorded configuration: `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md:64-67` "one required context, **`Bridge suite (Python 3.12)`**". Current protocol: `C:/CT13/AGENTS.md:50-51` "Master receives changes only by PR with `Bridge suite (Python 3.12)` green on the up-to-date head under ruleset 21444962, no bypass." Governance: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:26-27` "Master acceptance still requires the exact protected `Bridge suite (Python 3.12)` on an up-to-date head" | PRs into `master` cannot merge without that check green on an up-to-date head, **as recorded**. Direct push bypass is recorded empty (`CI_POLICY.md:68-69`). | GitHub ruleset 21444962 (repository setting, not YAML) | LIVE as a **recorded** setting dated 2026-08-25. Current GitHub API state is NOT VERIFIED (no network). |
| GitHub-native failure email | `CI_POLICY.md:36-38` "GitHub's native Actions failure notification/email is the day-one notification channel; delivery is subject to each recipient's GitHub notification settings." D026 email proof in `RED_GREEN_PLAN.md:101` is still "Pending email proof". | Native GitHub notification if the subscribed account has it enabled | GitHub account setting, not a workflow step | DECLARED-BUT-NOT-WIRED as a repo-owned check (platform-native; delivery unproven in the D026 table) |
| WP-P0-26 paging channel on CI failure | Plan `:593` "the WP-P0-26 paging channel when it lands". `CI_POLICY.md:112-113` "the WP-P0-26 paging channel may become an additional channel only after that separate package lands and is accepted." | Phone/push on a red master run | none | MISSING |
| WP-P0-23 as a **required** check | Workflow is LIVE (row above). Required-list policy: `CI_POLICY.md:94-97` "Only `Bridge suite (Python 3.12)` is in rule 21444962's required list. ... its `pine-alert-guard` check is green on `59bf7723` but is **not** required — that is this policy operating as designed, not an oversight." Plan `:599` "WP-P0-10 and WP-P0-23 may not claim continuous protection before this package is accepted". | Same scanner as the LIVE pine job, but merge-blocking | not in the recorded required list | LIVE as a workflow; DECLARED-BUT-NOT-WIRED as a required merge check |
| WP-P0-10 kernel economic golden suite (25 families) | Plan `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:382-388`. Brief M6 `.../MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2925`. No root workflow names it. Bridge `test_golden_generation.py:13-18` is the Keltner strategy golden, not the 25 kernel families. | 25 deterministic kernel families, each D026 RED/GREEN | none in CI | MISSING as a CI job. Kernel-family fixtures are not an accepted CI suite in this checkout. |
| WP-P0-21 admission / eligibility fixtures | Tests exist: `C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py:1-40` (imports `pydantic`, `mtc_contracts`, `p021_evidence_contracts`). Handoff record `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:30` "Python 3.12, `39 + 7 + 5 + 6 + 46 = 103/103` PASS". No workflow step. | Local eligibility/evidence-contract suite (synthetic). Package not accepted (`P021_P030_HANDOFF.md:37-38`). | local Lead runs only | DECLARED-BUT-NOT-WIRED |
| §9.6 parity set (three tests) | Brief `.../MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1836-1842`. Line 1838: "Run in CI; each must be capable of failing". Test 2 line 1841: "Nothing equivalent exists today." Test 3 line 1842: "it is not surfaced." Inert nested `C:/CT13/MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/parity.yml:41-42` `python scripts/parity_regression.py` is the retired-engine workflow, not root CI. | (1) kernel determinism, (2) simulator↔worker OrderIntent identity, (3) execution divergence report | none at repo root | MISSING (tests 2–3 do not exist). Nested parity.yml is inert, not this check. |
| Contract tests — `mtc_contracts` package | `C:/CT13/MTC_COMMAND_CENTER/contracts/tests/` (`test_compat.py:5-6`; `:5` `import pytest`; `:6` `from pydantic import BaseModel, ValidationError`). No root workflow. | Package handshake, sizing methods, immutability, trials/eligibility types | none | DECLARED-BUT-NOT-WIRED |
| Contract tests — Bridge config contract | `C:/CT13/IBKR_PAPER_BRIDGE/tests/test_config_contract.py:1-20` collected by the LIVE Bridge pytest command | Shipped `bridge.yaml` identity and config-contract refusals | Bridge suite events | LIVE (subset of Bridge suite) |
| Restore-proof freshness (`ops_restore_proof_freshness`) | Reserved `CI_POLICY.md:161`. No workflow job. Local OPS-A tests `C:/CT13/MTC_COMMAND_CENTER/tools/opsa/test_opsa.py:1-10` are the regression layer, not a freshness gate on an accepted restore proof. | Fail closed when the latest accepted restore proof is absent, malformed, stale, or of unknown identity | none | MISSING |
| OPS-A local unit/falsification suite | `C:/CT13/MTC_COMMAND_CENTER/tools/opsa/test_opsa.py:3` `python -m unittest test_opsa -v`; README `:19`. Stdlib only (`README.md:8`). | Repeatable backup/heartbeat/watchdog falsifications on fixtures. Package acceptance OPEN (`README.md:4-6`). | none in CI | DECLARED-BUT-NOT-WIRED |
| Drill currency (`ops_drill_currency`) | Reserved `CI_POLICY.md:162`. Owner-ratified currency windows are `[OPEN]` in WP-P0-26 (`MASTER_WORK_PACKAGE...md:580` detect-to-delivery bound `[OPEN]`). | Required drills still inside owner-ratified windows | none | MISSING |
| Credential-expiry warnings (`ops_credential_expiry`) | Reserved `CI_POLICY.md:163`. `CI_POLICY.md:168-169` "Any future check that contacts a host, reads account state, handles a credential ... must be separately authorized". | Warn before expiry without reading/printing/storing values | none | MISSING |
| Monitoring health (`ops_monitoring_health`) | Reserved `CI_POLICY.md:164`. | Accepted monitoring evidence; `UNKNOWN` is a stop | none | MISSING |
| Concurrent-writer mechanical delivery guard | Plan `:595`. WP-P0-05 `MASTER_WORK_PACKAGE...md:341` "the mechanical half of that check — claim, ownership and liveness verification that actually runs — is **WP-P0-27, planned and unbuilt**." `C:/CT13/AGENTS.md:47-48` "`SESSION_LOCK.md` is a checked mirror/history, not the guard. Mandatory GitHub-issue claims were retired; WP-P0-27's mechanical claim check remains unbuilt." `C:/CT13/MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:12-13` "WP-P0-27's mechanical ownership/liveness verifier remains planned rather than assumed." | Block overlapping writers using a shared claim; `UNKNOWN`/`ACTIVE` is STOP | none | MISSING |
| Cleanup-ownership UNKNOWN guard | Plan `:595`. Brief `...BRIEF_2026-08-21.md:2784` "Mechanical guards block concurrent writers, and block cleanup, when ownership, process/scheduled-task dependency or checkout purpose is `UNKNOWN`." | Cleanup/delete/move refused while ownership or liveness is `UNKNOWN` | none | MISSING |
| P030 market-data contract checker | `C:/CT13/check_p030_market_data_contracts.py:1` and `:1247-1248` `main()`. Not in `research-gates.yml`. | Synthetic P030 identity/event-family goldens | none | DECLARED-BUT-NOT-WIRED |
| P030 closed-partition backup adapter tests | `C:/CT13/check_p030_closed_partition_backup_adapter.py:1` and `:1791-1792` `unittest.main`. | Synthetic stable-prefix backup/restore refusals | none | DECLARED-BUT-NOT-WIRED |
| P030 OPS-A heartbeat adapter tests | `C:/CT13/check_p030_opsa_heartbeat_adapter.py:1` and `:248-249` `unittest.main`. | Synthetic heartbeat-adapter confinement | none | DECLARED-BUT-NOT-WIRED |
| P022 reduced local tracker tests | `C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p022_research_tracker.py:1-4` and `:814` `__main__`. Handoff `P022_HANDOFF.md:38` GitHub Bridge/Research/Pine passed; this file is not a workflow step. | Reduced-scope tracker CLI/disclose seam | none | DECLARED-BUT-NOT-WIRED |
| `mtc_cli` tests | `C:/CT13/mtc_cli/tests/test_audit.py` exists; no root workflow | CLI audit helper | none | DECLARED-BUT-NOT-WIRED |
| Section-16 `check_review_report.py` | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/check_review_report.py:24` `PACKET = Path(r"C:\LAB\Tradingview_LAB_CLEAN\_gemini_packets_20260830\P012_R30_20260908")` — default packet path is a machine-local directory | Review-report citation gate for Section-16 packets | none (and not a merge check) | DECLARED-BUT-NOT-WIRED (local review tool; hardcoded packet path) |
| Repo guard dry-run (branch, freshness, dirty, staged, protected-scope, risky untracked, pine, unpushed) | `C:/CT13/MTC_COMMAND_CENTER/tools/repo_guard.ps1` (header `:2-3` "READ-ONLY"; protocol `MTC_REPO_GUARD_PROTOCOL.md:49-50`). No workflow references it (search of `C:/CT13/.github`). | Local preflight. BLOCKs when `git rev-parse --abbrev-ref HEAD` is `master` or `main` (`repo_guard.ps1:63-66`). Root CI checkout is `actions/checkout@v4` with no `ref:` (`ci.yml:27-29`); whether Actions would see that branch name is NOT VERIFIED. | agent preflight / before commit / before merge — not GitHub Actions | DECLARED-BUT-NOT-WIRED as CI |
| Protected-paths pre-commit hook | Script `C:/CT13/MTC_COMMAND_CENTER/09_DOCS/hooks/protected_paths_hook.py:1-2`. Policy `C:/CT13/MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:27-30` "it is installed nowhere and invoked by nothing." Architecture still describes it as the mechanical guard: `C:/CT13/MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md:1289` "To turn the protected-paths policy into a mechanical guard" and `:1292` "A pre-commit hook lives at 09_DOCS/hooks/protected_paths_hook". No `.github` workflow references it. Common gitdir `C:/LAB/Tradingview_LAB_CLEAN/.git/hooks` listing in this lane contained only `*.sample` files. | Trailer `APPROVED-PATCH-PLAN: <task_id>` plus TASK_HISTORY APPROVED/COMPLETED, **if it ran**. It does not run. | nowhere | DECLARED-BUT-NOT-WIRED (script exists; not installed; not CI). See hook section below. |
| Inert `02_MTC_BACKTEST` Test Suite | `C:/CT13/MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/tests.yml:3-10` `on: push` branches `main, develop` paths `mtc_backtest/src/**`, `mtc_backtest/tests/**`, `mtc_backtest/scripts/**`, `mtc_backtest/pyproject.toml`, `mtc_backtest/requirements.txt` | ruff + pytest of the imported backtest tree | would run only if this file were a **root** workflow and those branches/paths existed here | DECLARED-BUT-NOT-WIRED / inert nested artifact. Plan `:593` "unported". |
| Inert `02_MTC_BACKTEST` Parity Regression | `.../parity.yml:1-18` includes `schedule: - cron: "15 1 * * *"` and `python scripts/parity_regression.py` | Retired-engine parity/DST jobs | same nested limitation; also a scheduled job, which WP-P0-27 non-goals forbid at root (`MASTER_WORK_PACKAGE...md:602` "no scheduled data jobs") | DECLARED-BUT-NOT-WIRED / inert. Do not port. |
| Vercel check (mentioned in handoffs) | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:10-11` "Exact-head Bridge, Pine, research and Vercel checks passed." No file under `C:/CT13/.github/workflows/`. | Unknown in this lane | unknown | NOT VERIFIED as a repo workflow. Recorded as a GitHub check name in handoff prose only. |

## Bridge pytest entry points

The LIVE suite command is exactly `python -m pytest IBKR_PAPER_BRIDGE/tests -q` (`ci.yml:45`). Autouse fixture `C:/CT13/IBKR_PAPER_BRIDGE/tests/conftest.py:13-21` monkeypatches Telegram credential resolution so tests cannot fall through to real HKCU credentials.

Canonical local command (may ignore an extra directory) is recorded in `C:/CT13/IBKR_PAPER_BRIDGE/TESTS.md:5` `python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1`. CI does not pass that ignore; it points pytest at `IBKR_PAPER_BRIDGE/tests` only.

This lane did not execute pytest. The table below is from reading the modules CI will collect.

| Module | file:line (identity) | What the file says it covers |
|---|---|---|
| `conftest.py` | `:13-16` | Autouse: no real Telegram credentials |
| `test_api.py` | `:5-13` | FastAPI TestClient + MockBroker engine API |
| `test_bars.py` | `:11` `test_wall_clock_timer_finalizes_quiet_candle_once` | Bar finalizer / quiet-candle close |
| `test_config_contract.py` | `:18-20` shipped `bridge.yaml` SHA-256 pin | Config-contract identity and refusals |
| `test_dashboard_static.py` | `:13-15` static root / `help_map.json` | Dashboard static assets |
| `test_deployment_wrapper.py` | `:4-9` | P2 supervisor script has no hardcoded clean-lab path |
| `test_engine_dryrun.py` | `:18-36` BridgeEngine / OrderManager / Store | Engine dry-run / kill / durable-row paths (no module docstring) |
| `test_funding_payload_retention.py` | `:1-13` | Synthetic funding-payload persistence across restart |
| `test_golden_generation.py` | `:13-18` | Keltner `golden_signals.json` synced with strategy YAML — **not** WP-P0-10's 25 families |
| `test_hyperliquid_broker.py` | `:14-15` imports `bridge.broker.hyperliquid` | Hyperliquid broker unit tests (offline; not executed here) |
| `test_interim_risk_wiring.py` | `:1-8` | DAILY_LOSS / CONSECUTIVE_LOSS gates see persisted values |
| `test_linux_deployment.py` | `:1-4` | Structural tests of the inert KVM2 package; no host/network |
| `test_llm_gate.py` | `:6` `LLMGate, NullLLMGate` | LLM gate |
| `test_mock_broker.py` | `:11` `test_mock_broker_market_fill_and_sl_priority` | MockBroker fill / stop-loss priority |
| `test_mtc_funding_export.py` | `:1-8` | Synthetic MTC funding exporter contract |
| `test_order_identity.py` | `:1-3` | TS-P1-002 identity |
| `test_order_lifecycle.py` | `:12` `test_sl_fills_on_later_bar` | Order lifecycle / later-bar SL fill |
| `test_order_state.py` | `:13` pydantic / `bridge.engine.types` | Order-state mappings including GC-referent tests |
| `test_p1_failure_drills.py` | `:6-13` MockBroker + BridgeEngine | P1 failure drills |
| `test_partial_fill_protection.py` | `:1-9` | TS-P1-004 protect-or-flatten, MockBroker only |
| `test_reconciliation.py` | `:1-6` | TS-P1-005 full reconciliation adversarial suite |
| `test_release_evidence.py` | `:1-4` | `release_evidence.py` against temp git repos |
| `test_risk.py` | `:7-15` RiskEngine reason codes | Risk engine |
| `test_runtime_baseline.py` | `:1-5` | `check_runtime_baseline.py` against temp git repos |
| `test_scaffold.py` | `:1-3` | `bridge.app` imports |
| `test_smoke_p0.py` | `:9-20` | Smoke helpers; credential-format tests use env monkeypatch |
| `test_store.py` | `:10-15` Store / kill ids | Persistence store |
| `test_strategy.py` | `:10` `KeltnerTrailEma8` | Strategy unit tests against fixtures |
| `test_task11_polish.py` | `:7-14` TestClient + TelegramNotifier | Task-11 polish / notifier wiring |
| `test_unknown_submission.py` | `:12-15` `BrokerOutcomeUnknown` | Unknown-submission / pre-send failure |
| `test_wal_state_bundle.py` | `:1-4` | WAL capture/verify against tmp_path only |
| `test_window_state.py` | `:1-6` | Soak window: DOWN must not present as ARMED |

`C:/CT13/IBKR_PAPER_BRIDGE/tests/fixtures/` holds `BTC_1h.csv`, `BTC_1h_real.csv`, `golden_signals.json` — data for the modules above, not a separate CI job.

## Protected merge checks (recorded, not re-queried)

`CI_POLICY.md:41-71` is the 2026-08-25 ruleset dump: ruleset id `21444962`, name "Protect master – required CI", enforcement `active`, required context exactly `Bridge suite (Python 3.12)`, `strict_required_status_checks_policy: true`, `bypass_actors` empty. First merge through it: PR #127 (`CI_POLICY.md:76-84`).

`research-gates.yml:8-11`:

> "This workflow is deliberately NOT a required check. Ruleset 21444962 requires exactly `Bridge suite (Python 3.12)`, and nothing in this file changes that. WP-P0-27 remains the carrier for progressive CI activation"

`REVIEW_POLICY.md:59` — "Live release, owner permission, protected CI and merge gates remain separate."

This assessment does not add, remove, or rename that required context.

## Protected-paths hook — confirm or refute "mechanical guard, installed nowhere"

**Claim under test.** Architecture and the pre-correction policy treat the hook as the mechanical commit guard:

- `C:/CT13/MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md:1289` "To turn the protected-paths policy into a mechanical guard:"
- `ARCHITECTURE.md:1292` "- A pre-commit hook lives at 09_DOCS/hooks/protected_paths_hook (Python or PowerShell)"
- `ARCHITECTURE.md:1300` "- The hook is enabled per-clone via `git config core.hooksPath 09_DOCS/hooks`"
- Owner ruling `C:/CT13/MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json:289` records the pre-correction sentence: "PROTECTED_PATHS_POLICY.md line 24 states that 09_DOCS/hooks/protected_paths_hook.py 'is the mechanical guard for commits'."

**Bytes in this checkout refute installation and CI wiring; they confirm the script exists.**

1. The script is present and is a real checker: `C:/CT13/MTC_COMMAND_CENTER/09_DOCS/hooks/protected_paths_hook.py:63-89` (`main` scans staged paths, requires `APPROVED-PATCH-PLAN`, returns 1 otherwise).
2. Corrected policy: `C:/CT13/MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:24-25` "**The `APPROVED-PATCH-PLAN` trailer is a required practice, validated by hand. It is not currently enforced by any mechanism.**"
3. Same file `:27-30` "A script exists at `09_DOCS/hooks/protected_paths_hook.py` ... **But it is installed nowhere and invoked by nothing.**"
4. Same file `:34-37` measured 2026-09-10: shared common gitdir `hooks/` "only `.sample` files"; `core.hooksPath` unset; "any CI workflow under `.github/` | no reference to it".
5. Same file `:80` "**Do not cite this hook as a control that is in force.**"
6. Same file `:82-84` owner was offered CI wiring and `core.hooksPath` install on 2026-09-10 and "**deliberately not chosen**".
7. This lane re-read all three files under `C:/CT13/.github/workflows/` — none names `protected_paths_hook`.
8. This checkout's gitdir pointer is `C:/CT13/.git:1` `gitdir: C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/CT13`. Listing `C:/LAB/Tradingview_LAB_CLEAN/.git/hooks` showed only Git sample hooks (`pre-commit.sample`, `commit-msg.sample`, …). There is no non-sample `pre-commit` and no `protected_paths_hook` in that directory. `core.hooksPath` was not queried (Git commands are forbidden in this lane).

**Also independently broken even if installed:** `PROTECTED_PATHS_POLICY.md:45-66` — `touches_protected()` would not have matched the paths the policy has actually been used for; `protected_patterns()` only appends policy lines starting `01_MASTER` (`protected_paths_hook.py:39`).

**Verdict.** The "mechanical guard for commits" wording is a stale description (Architecture.md; pre-correction policy). The hook file exists. It is not installed in the common hooks directory this worktree uses, and it is not invoked by any CI workflow. Enforcement remains hand validation, by owner ruling HIST-2026-0032 (`TASK_HISTORY.json:283-289`).
