# CI assessment — remaining checks (WP-P0-27, owner decision D YES)

Read-only. No workflow, ruleset, hook, or test was changed. Classifications are recommendations for a later authorized implementation lane, not an instruction to apply them now.

START_HERE for this package (`C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/START_HERE.md:52`):

> "Preserve existing Bridge tests/protected merge checks. Assess remaining checks individually for implementation or explicit deferral; do not declare no functioning CI or weaken existing checks."

Plan audit tier for this package (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:598`): "**T1** (it governs whether guards actually run)." Review-policy consequence table: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:19-23`. Highest applicable consequence wins (`REVIEW_POLICY.md:25-27`). A new job that only runs already-written hermetic checkers stays T1. A job that would become the home of parity, golden, credential, or acceptance-evidence logic is T0. Activation caveat (`REVIEW_POLICY.md:6-8`): "OD-20260909-1 is prospective. These revised defaults take effect only after this candidate satisfies the pre-change T0 contract and authorized protected integration. Until then, the previously operative obligations continue". Recorded activation condition (`C:/CT13/MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:17-19`): "Protected integration is tracked by PR #167; activation requires the merged PR and protected CI on its final head." Tier labels on IMPLEMENT/DEFER rows use the consequence table as classification vocabulary; they are not a claim that OD-20260909-1 is already in force.

Progressive activation (`MASTER_WORK_PACKAGE...md:595`): "OPS-C activates CI progressively — the day-one job plus the progressive required-check policy already stated above **is** that activation, and no big-bang enablement is introduced."

Required-list rule already in force as policy (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md:100-104`): a later guard becomes required only after the owning package delivers the executable check, D026 exists, the audit tier accepts it, and the Lead asks the owner to add the stable check context to ruleset 21444962. This lane does not ask GitHub to change that list.

## Functioning CI exists (do not declare otherwise)

Three repo-root workflows run on GitHub-hosted runners with `permissions: contents: read` and no secrets:

- `C:/CT13/.github/workflows/ci.yml:1-12` name `CI` (`:1`), PR/push `master` (`:3-9`), `permissions:` / `contents: read` (`:11-12`)
- `C:/CT13/.github/workflows/pine-defang-guard.yml:1-8`
- `C:/CT13/.github/workflows/research-gates.yml:14-25`

Day-one Bridge suite plus compileall is LIVE. The recorded protected merge check is still exactly `Bridge suite (Python 3.12)`.

The plan sentences that say "zero functioning CI" (`MASTER_WORK_PACKAGE...md:591`, `:594`) are the 2026-08-23 starting fact. Treating them as today's description would violate START_HERE. This assessment is not WP-P0-27 package acceptance (`CI_POLICY.md:18-19` "Whether the WP-P0-27 package gate now closes is the Lead's acceptance call, not this page's.").

## No existing check is weakened

This lane applied no YAML, ruleset, hook, pytest filter, xfail, ignore, skip, pin, or bypass change.

Any later implementation lane that follows this assessment must keep all of the following byte-identical unless a separately authorized T0/T1 review says otherwise:

1. `ci.yml` still runs `python -m pytest IBKR_PAPER_BRIDGE/tests -q` with no `-k`, `--ignore`, `-m`, `--maxfail`, or xfail added to that step (`ci.yml:44-45`).
2. `ci.yml` still uses `--require-hashes` against `IBKR_PAPER_BRIDGE/requirements.lock` (`ci.yml:36-39`) and `compileall` (`ci.yml:41-42`).
3. Ruleset 21444962 still requires `Bridge suite (Python 3.12)` and does not drop it. Adding another required context is an owner setting; replacing this one is a weaken.
4. `research-gates.yml` remains a non-required workflow (`research-gates.yml:8-11`) unless the owner later adds its check context. Its `continue-on-error` acceptance report (`research-gates.yml:82-85`) must not be turned into a failing gate while WP-P0-20 is unmet — that would train people to ignore a permanently red workflow (`research-gates.yml:79-81`).
5. `pine-defang-guard.yml` keeps running `check_no_pine_alerts.py` with the empty allowlist (`check_no_pine_alerts.py:10`). Do not populate `ALLOWLIST`.
6. Do not port `02_MTC_BACKTEST/.github/workflows/{parity.yml,tests.yml}` to repo root (`MASTER_WORK_PACKAGE...md:593` "unported"; `:602` "no porting of the retired engine's workflows"; `:602` "no scheduled data jobs").
7. Do not install `protected_paths_hook.py` into CI or `core.hooksPath` without a **new** owner decision. The 2026-09-10 ruling rejected both (`PROTECTED_PATHS_POLICY.md:82-84`; `TASK_HISTORY.json:289`).
8. Do not put `repo_guard.ps1` on the `master` push path. Locally it BLOCKs when `git rev-parse --abbrev-ref HEAD` is `master` or `main` (`repo_guard.ps1:63-66`). Whether GitHub-hosted `actions/checkout@v4` (`ci.yml:27-29`) yields that branch name is NOT VERIFIED.
9. No secrets, no self-hosted runner, no venue contact (`MASTER_WORK_PACKAGE...md:593`, `:601-602`).

## Remaining / missing checks, one by one

Each row is a check that is not already a LIVE required merge check, or that is LIVE as a workflow but not yet required, or that the plan still names as a future plug-in.

### 1. Pine defang as a **required** merge check — DEFER (required-status only)

**Today.** The scanner and workflow are LIVE. Required-status is deliberately off (`CI_POLICY.md:94-97`). Plan `:599` forbids WP-P0-23 from claiming continuous protection before WP-P0-27 is accepted.

**Minimal change if later implemented (not applied):** owner adds the existing check context `pine-alert-guard` (`pine-defang-guard.yml:11`) to ruleset 21444962 **in addition to** `Bridge suite (Python 3.12)`. No YAML change required.

**Review tier:** T1 for the setting documentation; the scanner itself is already T0-surface Pine routing (`MASTER_WORK_PACKAGE...md:547`) but the workflow already runs. Adding it as required is an owner repository-setting act (`CI_POLICY.md:102-103`).

**Why defer now.** Progressive policy is not complete until the Lead asks. Package acceptance for WP-P0-27 is still the Lead's call. Current GitHub required-list membership is NOT VERIFIED in this lane.

**Unblocks.** Lead acceptance of WP-P0-27 (or an explicit owner exception), a green `pine-alert-guard` run on the then-current `master`, and the owner adding the context without removing Bridge.

**Owner item.** See Q1.

### 2. Research gates as a **required** merge check — DEFER

**Today.** LIVE and explicitly not required (`research-gates.yml:8-11`). P020 acceptance harness is report-only because it is not MET (`research-gates.yml:79-81`). P020 remaining work is still open (`START_HERE.md:35` "Latest recorded full acceptance is 8/16 MET, NOT ACCEPTABLE").

**Minimal change if later implemented:** owner adds check context `Research gate checkers (Python 3.12)` (`research-gates.yml:33`) to ruleset 21444962 **in addition to** Bridge. Do not flip `check_p020_acceptance.py` to a failing step until every criterion is MET — that would make the workflow permanently red.

**Review tier:** T1 to add the already-running checkers as required; T0 if the required job is treated as WP-P0-20 acceptance evidence (`REVIEW_POLICY.md:20` "binding safety, acceptance or evidence logic").

**Unblocks.** WP-P0-20 accepted, Lead request, owner ruleset edit.

**Owner item.** See Q2. Recommended answer: **no**, not before P020 acceptance.

### 3. WP-P0-10 25-family golden suite in CI — DEFER

**Today.** MISSING. Plan `:382-388` / brief M6 `:2925`. Bridge `test_golden_generation.py` is a different golden (Keltner signals).

**Minimal change if later implemented:** a new job, not an edit of the Bridge pytest line, running the accepted 25-family command once WP-P0-10 (and the kernel that owns the fixtures) delivers it. Do not fold kernel goldens into `IBKR_PAPER_BRIDGE/tests`.

**Review tier:** **T0** (parity / economics / golden evidence — `REVIEW_POLICY.md:20`; package WP-P0-10 is T0 at `MASTER_WORK_PACKAGE...md:387`).

**Unblocks.** WP-P0-10 fixtures exist, each D026 RED/GREEN, owning kernel package accepted enough to pin a command, hash-locked install story if not stdlib.

### 4. WP-P0-21 admission fixtures in CI — DEFER

**Today.** DECLARED-BUT-NOT-WIRED. Tests exist (`test_p021_eligibility.py:10-12` imports `mtc_contracts` at `:10-11` and `pydantic` at `:12`). 103/103 is a Lead local record (`P021_P030_HANDOFF.md:30`), not a CI recipe. Package not accepted (`P021_P030_HANDOFF.md:37`). Thresholds remain unset/fail-closed (`HANDOFF.md:16` "Decision 6 keeps unmeasured limits unset and fail-closed").

**Why not IMPLEMENT now.** Wiring needs a published, hash-locked install (pydantic / `mtc_contracts`). Lane K refused new unpinned dependencies (`LANE_REPORT.md:201-202`). Folding these tests into the Bridge job would mix trees and risk slowing or destabilizing the protected suite — a weaken. Research-gates is stdlib-only (`research-gates.yml:13`) and cannot take them without becoming a pip job.

**Minimal change later:** a **new** non-required workflow, Python 3.12, hash-locked extra requirements (new lockfile owned by P021), running the five recorded suites. Do not add to ruleset 21444962 until P021 package acceptance.

**Review tier:** T1 for the workflow; T0 if the job is treated as eligibility/admission evidence (`REVIEW_POLICY.md:20`).

**Unblocks.** P021 Lead publishes the exact five commands plus a hash-locked dependency file; P021 package acceptance before required-status.

### 5. §9.6 three parity tests in CI — DEFER

**Today.** MISSING. Brief `:1838` says "Run in CI" but `:1841` test 2 "Nothing equivalent exists today" and `:1842` test 3 "is not surfaced." Nested `parity.yml` is the retired engine and must not be ported (`MASTER_WORK_PACKAGE...md:602`).

**Minimal change later:** new job(s) only after the three fixtures exist and are D026-proven. Test 1 (kernel determinism) is also the WP-P0-21 deterministic-replay row (`BRIEF:1390`). Test 2 needs a live worker in replay mode (V2A). Test 3 needs a surfaced Bridge divergence report.

**Review tier:** **T0** (parity).

**Unblocks.** Fixtures for all three; D026; no use of the nested `02_MTC_BACKTEST` workflow.

### 6. `mtc_contracts` contract tests in CI — DEFER

**Today.** DECLARED-BUT-NOT-WIRED (`contracts/tests/test_compat.py:5-8` pytest + pydantic). P013/P020 still have remaining package work (`START_HERE.md:43` "Remaining full work: accepted P020 B-01 interface dependency..."; `:35` "Latest recorded full acceptance is 8/16 MET, NOT ACCEPTABLE"). Bridge `test_config_contract.py` is already LIVE inside the protected suite — do not duplicate or move it.

**Minimal change later:** new non-required job with a hash-locked extra install, `pytest MTC_COMMAND_CENTER/contracts/tests`. Never merge these into the Bridge pytest path.

**Review tier:** T1 for the job; T0 if used as shared-contract acceptance.

**Unblocks.** Owning contracts package accepted; hash-locked extras; hermetic command.

### 7. `ops_restore_proof_freshness` — DEFER

**Today.** MISSING as the named freshness gate (`CI_POLICY.md:161`). Local `test_opsa.py` is a different layer (`test_opsa.py:5-10`: drill-level evidence lives in the 2026-08-25 restore-drill document; these tests are the regression layer). P026 package acceptance OPEN (`tools/opsa/README.md:4-6`). No accepted restore-proof artifact identity exists for CI to pin.

**Minimal change later:** new job `ops_restore_proof_freshness` that reads a committed or second-location proof manifest and fails closed on absent/malformed/stale/unknown identity — after WP-P0-26 defines that manifest. No host contact (`CI_POLICY.md:168-169`).

**Review tier:** T1 for the job once the fixture is local; any host-touching step is T0 + G9 (`MASTER_WORK_PACKAGE...md:584`).

**Unblocks.** WP-P0-26 accepted restore-proof format, identity, and freshness window.

### 8. OPS-A local `test_opsa.py` as a non-required job — IMPLEMENT (described, not applied)

**Today.** DECLARED-BUT-NOT-WIRED. Stdlib, documented command `python -m unittest test_opsa -v` from `MTC_COMMAND_CENTER/tools/opsa` (`test_opsa.py:3`; `README.md:8,19`). Same pattern as research-gates: "a gap stopped, not that package delivered" (`research-gates.yml:10-11`).

**Minimal workflow change (not applied).** Add a new repo-root file `.github/workflows/opsa-local.yml` (do **not** edit `ci.yml` or `research-gates.yml`):

```yaml
name: OPS-A local suite
on:
  pull_request: { branches: [master] }
  push: { branches: [master] }
permissions: { contents: read }
jobs:
  opsa-local:
    name: OPS-A local suite (Python 3.12)
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    env: { PYTHONUTF8: "1" }
    steps:
      - uses: actions/checkout@v4
        with: { persist-credentials: false }
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - name: OPS-A unit and falsification tests
        working-directory: MTC_COMMAND_CENTER/tools/opsa
        run: python -m unittest test_opsa -v
```

No pip, no secrets, no required-list edit. This does **not** satisfy `ops_restore_proof_freshness`.

**Review tier:** T1.

**Unblocks for required-status (separate):** WP-P0-26 acceptance + Lead request.

### 9. `ops_drill_currency` — DEFER

**Today.** MISSING. Currency windows are owner-gated and `[OPEN]` (`MASTER_WORK_PACKAGE...md:580`).

**Unblocks.** Owner-ratified windows and a local evidence file the job can read without host contact.

**Review tier:** T1 once the window values exist; inventing a window in CI would be T0 policy.

### 10. `ops_credential_expiry` — DEFER

**Today.** MISSING. No credential is in this package's authority (`MASTER_WORK_PACKAGE...md:621` WP-P0-29: "no credential is created, stored or handled inside this package" is P029; P027 `CI_POLICY.md:163` "without reading, printing or storing credential values"). Gate G6 (plan P029 `MASTER_WORK_PACKAGE...md:621`, the credential gate — not REVIEW_POLICY.md's G6, which is auditor packet reuse at `REVIEW_POLICY.md:68`): agents never read or print a value.

**Unblocks.** WP-P0-29 policy + a presence/expiry metadata source that is not a secret + G6 authorization for whatever the job inspects.

**Review tier:** **T0** (credentials / security).

### 11. `ops_monitoring_health` — DEFER

**Today.** MISSING. P026 monitoring/delivery not accepted (`HANDOFF.md:18`; `P021_P030_HANDOFF.md:40`).

**Unblocks.** Accepted monitoring evidence format; `UNKNOWN` fail-closed fixture.

**Review tier:** T1 for a local evidence check; T0 + G9 if it contacts a host.

### 12. Concurrent-writer mechanical guard — DEFER

**Today.** MISSING. WP-P0-05 assigned the mechanical half to WP-P0-27 and called it unbuilt (`MASTER_WORK_PACKAGE...md:341`). The original shared claim included a GitHub issue; that claim form was retired (`AGENTS.md:48`; `SESSION_LOCK.md:12` "The GitHub-issue claim was retired by owner decision on 2026-08-26."). `SESSION_LOCK.md` is a mirror, not the guard (`SESSION_LOCK.md:5`; `AGENTS.md:47`). There is no ratified machine-readable replacement schema for this lane to check.

**Why not IMPLEMENT a YAML job now.** A job that greps `SESSION_LOCK.md` would either no-op or false-block on stale rows (`SESSION_LOCK.md:14-28` still lists 2026-08/09 workstreams). That is not D026.

**Minimal change later.** After the owner names the replacement claim artifact (issue replacement, JSON claim, or a tightened SESSION_LOCK schema), add a stdlib checker and a non-required job. Fail closed on `UNKNOWN` / overlapping `ACTIVE` path claims. Do not treat git cleanliness, push, or mtime as liveness (`MASTER_WORK_PACKAGE...md:595`).

**Review tier:** T1 for the checker once the schema exists (delivery-boundary guard, not economic). Schema choice is an owner policy item (Q4).

**Unblocks.** Owner-ratified claim schema replacing the retired GitHub-issue claim; WP-P0-05 close-out producing that artifact.

### 13. Cleanup-ownership UNKNOWN guard — DEFER

**Today.** MISSING. No cleanup executor runs in CI. Brief M1 already says every `UNKNOWN` blocks cleanup (`BRIEF:2918`). A merge-time GitHub job cannot see another machine's worktrees or scheduled tasks.

**Minimal change later.** Put the guard in the cleanup tool itself (fail closed), with a D026 fixture, then optionally a CI job that only runs that fixture against synthetic UNKNOWN inputs — not a job that deletes anything.

**Review tier:** T1 for a synthetic fixture job; any real cleanup remains a separately authorized act (G8 for deletions — `MASTER_WORK_PACKAGE...md:663` pattern).

**Unblocks.** A named cleanup tool and a synthetic UNKNOWN fixture.

### 14. WP-P0-26 paging on CI failure — DEFER

**Today.** MISSING (`CI_POLICY.md:112-113`). Day-one channel is GitHub-native email (`CI_POLICY.md:36-38`).

**Unblocks.** WP-P0-26 paging channel accepted; then a workflow `if: failure()` that calls it **without introducing a secret this package does not own**. If the channel needs a secret, that is a separate owner authorization — not a silent `ci.yml` edit.

**Review tier:** T1 if it only notifies; T0 if it handles credentials.

### 15. GitHub email D026 proof — DEFER (Lead evidence, not a workflow)

`RED_GREEN_PLAN.md:101` "Pending email proof". Nothing in YAML can prove the Lead's inbox. Not an IMPLEMENT of workflow text.

**Unblocks.** Lead records a real failure-email timestamp, or records that GitHub notification settings do not deliver.

### 16. Protected-paths hook in CI or `core.hooksPath` — DEFER

**Today.** Script exists; not installed; not in CI. Owner rejected both wiring options on 2026-09-10 (`PROTECTED_PATHS_POLICY.md:82-84`; `TASK_HISTORY.json:289`). Even installed, `touches_protected()` misses the paths this policy is used for (`PROTECTED_PATHS_POLICY.md:45-66`).

**Minimal change if a new owner decision reverses that:** still not "just add a CI step" — first fix `protected_patterns()` so listed surfaces actually match, then decide local hook vs CI vs neither. A misconfigured required hook can block legitimate work (policy `:82-84`).

**Review tier:** **T0** (can block protected-path work; security/process gate).

**Owner item.** See Q3. Recommended answer: **do not reopen** until the matcher covers the real protected surfaces.

### 17. `repo_guard.ps1` as a GitHub job — DEFER

Documented as a local preflight (`MTC_REPO_GUARD_USAGE.md:7-9` `cd C:\LAB\Tradingview_LAB_CLEAN` then `pwsh -File MTC_COMMAND_CENTER\tools\repo_guard.ps1`). Locally it BLOCKs when `git rev-parse --abbrev-ref HEAD` is `master` or `main` (`repo_guard.ps1:63-66`). Root CI checkout is `actions/checkout@v4` with no `ref:` (`ci.yml:27-29`); whether that leaves `HEAD` as `master` or detached on a GitHub-hosted runner is NOT VERIFIED. Pine scanning is already LIVE via `pine-defang-guard.yml`.

**Unblocks.** None needed for CI. Keep as agent preflight.

### 18. P030 three stdlib checkers as a non-required job — IMPLEMENT (described, not applied)

**Today.** DECLARED-BUT-NOT-WIRED. Files are stdlib (`check_p030_market_data_contracts.py:1-11`; unittest mains at `check_p030_closed_partition_backup_adapter.py:1791-1792` and `check_p030_opsa_heartbeat_adapter.py:248-249`). Same "gap stopped, not package delivered" pattern as research-gates. Do not add them to `research-gates.yml` — that file is the WP-P0-20 surface (`research-gates.yml:1-6`).

**Minimal workflow change (not applied).** New `.github/workflows/p030-gates.yml`:

```yaml
name: P030 gates
on:
  pull_request: { branches: [master] }
  push: { branches: [master] }
permissions: { contents: read }
concurrency:
  group: p030-gates-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
jobs:
  checkers:
    name: P030 synthetic checkers (Python 3.12)
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    env: { PYTHONUTF8: "1", PYTHONDONTWRITEBYTECODE: "1" }
    steps:
      - uses: actions/checkout@v4
        with: { persist-credentials: false }
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python check_p030_market_data_contracts.py
      - run: python check_p030_closed_partition_backup_adapter.py
      - run: python check_p030_opsa_heartbeat_adapter.py
```

Do not add this check context to ruleset 21444962. P030 is not package-accepted (`P021_P030_HANDOFF.md:40`).

**Review tier:** T1.

### 19. P022 reduced tracker tests as a non-required job — IMPLEMENT (described, not applied)

**Today.** DECLARED-BUT-NOT-WIRED. File is stdlib (`test_p022_research_tracker.py:9-20`) with `__main__` at `:814`. Reduced milestone is merged; full P022 is not (`P022_HANDOFF.md:24`).

**Minimal workflow change (not applied).** New job, not an edit of Bridge pytest:

```yaml
# job name must stay stable if it is ever required later
name: P022 tracker
# same on: PR/push master, contents: read, ubuntu-24.04, Python 3.12, no pip
- run: python MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p022_research_tracker.py
```

Do not discover-and-run the whole `03_QUANTLENS/tools/tests/` tree (P021/pydantic and unrelated suites live there).

**Review tier:** T1.

### 20. `mtc_cli` tests / `check_review_report.py` / actionlint / ruff-from-inert-workflow — DEFER

None of these is a WP-P0-27 named plug-in. `check_review_report.py:24` hardcodes `C:\LAB\Tradingview_LAB_CLEAN\_gemini_packets_20260830\...` — not CI-portable. Inert `tests.yml:36-37` ruff is the retired engine; do not port (`MASTER_WORK_PACKAGE...md:602`). Lane K did not add actionlint (`LANE_REPORT.md:201-202`).

### 21. Inert nested workflows — DEFER (leave in place; do not enable; do not delete here)

Plan `:593` "recorded as inert and retired with the Q5 engine, unported." Deleting them is a G8-class exact-target act if they are historical artifacts, not a CI enablement. This assessment does not delete.

### 22. Direct-Lead-push bypass (plan vs live record) — DEFER (owner setting, not a check)

Plan `:593` wanted "direct Lead pushes remain allowed". Recorded ruleset has empty bypass (`CI_POLICY.md:68-69`, `:86-90`). Changing that is an owner edit of 21444962, never a lane action (`CI_POLICY.md:88-89`). Not classified IMPLEMENT.

## IMPLEMENT summary (later lane; not this one)

| # | Check | Minimal change | Required? | Tier |
|---|---|---|---|---|
| 8 | OPS-A `test_opsa.py` | new `opsa-local.yml`, unittest, no pip | no | T1 |
| 18 | P030 three checkers | new `p030-gates.yml`, no pip | no | T1 |
| 19 | P022 tracker tests | new `p022-tracker.yml` (or one combined optional workflow with three **named** jobs), no pip | no | T1 |

All three are additive. None edits `ci.yml`, `pine-defang-guard.yml`, or `research-gates.yml`. None touches ruleset 21444962.

If a later lane prefers one file instead of three, one workflow with three separately named jobs is acceptable; the job `name:` strings must stay stable.

## DEFER summary

| # | Check | Unblock |
|---|---|---|
| 1 | Pine required-status | P027 acceptance + Lead ask + owner ruleset add (keep Bridge) |
| 2 | Research-gates required-status | P020 accepted + Lead ask; keep acceptance harness report-only until MET |
| 3 | WP-P0-10 golden CI | 25-family fixtures + D026 + T0 |
| 4 | WP-P0-21 CI | hash-locked extra deps + exact commands; package acceptance before required |
| 5 | §9.6 parity CI | three fixtures exist; do not port nested parity.yml |
| 6 | `mtc_contracts` pytest | hash-locked extras; do not merge into Bridge |
| 7 | restore-proof freshness | P026 proof manifest + identity + freshness window |
| 9 | drill currency | owner-ratified windows |
| 10 | credential-expiry | P029 + G6-safe metadata; T0 |
| 11 | monitoring health | P026 monitoring evidence |
| 12 | concurrent-writer guard | replacement claim schema (issue claim retired) |
| 13 | cleanup UNKNOWN | cleanup tool + synthetic fixture; no delete in CI |
| 14 | P026 paging | P026 channel accepted; no silent secret |
| 15 | email D026 | Lead inbox evidence |
| 16 | protected-paths hook CI | new owner decision; matcher fix first |
| 17 | repo_guard in Actions | do not; local master/main BLOCK (`repo_guard.ps1:63-66`); Actions HEAD name NOT VERIFIED |
| 20 | review-report / ruff / actionlint | not a P027 named plug-in |
| 21 | delete nested inert YAML | Q5 retirement / exact-target authority |
| 22 | restore Lead-push bypass | owner ruleset edit only |

## Owner decision items (questions, with a recommended answer)

Nothing in this file is an authorization.

**Q1.** After WP-P0-27 is accepted, should the owner add existing check context `pine-alert-guard` to ruleset 21444962 **in addition to** `Bridge suite (Python 3.12)`?

- Recommended: **YES**, once a green run of that check exists on the then-current `master` and Bridge remains required. That is the progressive policy working as designed (`CI_POLICY.md:100-104`), not a weaken.
- Do not add it in this assessment lane.

**Q2.** Should `Research gate checkers (Python 3.12)` become required before WP-P0-20 is accepted?

- Recommended: **NO**. The workflow already says it is not required (`research-gates.yml:8-11`). The acceptance harness is still unmet and must stay non-gating (`research-gates.yml:79-81`).

**Q3.** Reopen installing `protected_paths_hook.py` via CI and/or `core.hooksPath` (rejected 2026-09-10)?

- Recommended: **NO**, until `protected_patterns()` / `touches_protected()` match the paths the policy is actually used for (`PROTECTED_PATHS_POLICY.md:45-73`). Hand validation remains the in-force control (`PROTECTED_PATHS_POLICY.md:80`).

**Q4.** Now that GitHub-issue claims are retired (`AGENTS.md:48`), what machine-readable shared claim should WP-P0-27's concurrent-writer checker read?

- Recommended: **specify a small committed-or-artifact JSON claim** (branch, worktree, exact paths, owner, live/scheduled dependency, ACTIVE/RELEASED) produced at lane start; keep `SESSION_LOCK.md` as the checked mirror. Do not treat SESSION_LOCK prose rows as the executable guard.

**Q5.** Authorize a later T1 lane to add the three non-required stdlib jobs in the IMPLEMENT summary (OPS-A local, P030 checkers, P022 tracker), without changing required checks?

- Recommended: **YES**. That is progressive activation and matches the research-gates "gap stopped" pattern. It does not accept P026/P030/P022.

**Q6.** Restore an explicit Lead/admin bypass for direct pushes to `master` (plan `:593` vs recorded empty bypass `CI_POLICY.md:68-69`)?

- Recommended: **NO change in this lane.** Current recorded behavior (PR-only, Bridge green, up-to-date head, no bypass) is stricter than the original plan and is already how agents are told to merge (`AGENTS.md:50-51`). Re-opening a bypass is an owner security choice, not a missing test.

## Explicit non-weaken statement

No existing check is weakened by this assessment: the Bridge pytest command, compileall, hash-locked install, pine empty-allowlist scanner, research-gates checkers, report-only P020 harness, and the recorded required context `Bridge suite (Python 3.12)` are left as they are. Remaining work is classified IMPLEMENT or DEFER without applying YAML. IMPLEMENT items are new files/jobs only. DEFER items wait on named unblocks rather than being silently dropped or marked proven.
