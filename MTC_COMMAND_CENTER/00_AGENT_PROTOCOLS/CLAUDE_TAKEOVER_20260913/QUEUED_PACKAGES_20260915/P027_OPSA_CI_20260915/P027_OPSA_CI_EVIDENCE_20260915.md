# WP-P0-27 — OPS-A tests in CI (builder item c of `OD-20260915-BUILD-ABC-1`) — evidence, 2026-09-15 night

**Authority:** owner "all" (~14:41Z) on the overnight handoff §1 item 4 → `OD-20260915-BUILD-ABC-1` item (c). **Built by the Claude Opus 5 Lead (session 5, `03c6c8`) as the disclosed builder; the Lead does not accept its own change.** Workflow files carry the T1 roster before merge (`CI_POLICY.md`).

| Step | Fact |
|---|---|
| Worktree / branch | `C:/tmp/P027_OPSA_CI_20260915`, `feature/p027-opsa-tests-ci-20260915` from `origin/master` `fcac0ac6` |
| Change | ONE new file `.github/workflows/opsa-tests.yml`: workflow `OPS-A tests`, job `opsa-tests` → check context **`OPS-A tests (Python 3.12, Windows)`**; `windows-2025`; `core.longpaths` before `actions/checkout@v4` (`persist-credentials: false`); `actions/setup-python@v5` 3.12; `python -m unittest test_opsa -v` in `MTC_COMMAND_CENTER/tools/opsa`; `permissions: contents: read`; concurrency group; `timeout-minutes: 10`; installs nothing (stdlib suite). Separate file from PR #193's `research-gates.yml` on purpose (no cross-PR conflict; #193 is under T1 review). |
| Local pre-check | `python -m unittest test_opsa` on the master bytes (CT13 `tools/opsa`, pinned 3.12.12): **`Ran 33 tests … OK`**; YAML loads (`yaml.safe_load`: one job, four steps, `on` pull_request/push master); `git diff --check` clean; repo guard **PASS** in the worktree |
| Commit | `63b7bbe0` (authorship + authority + non-required status in the message), pushed |
| PR | **#194** https://github.com/bsemaay-tech/mtc-command-center/pull/194 (OPEN, not draft, `mergeStateStatus: CLEAN`) |
| GREEN run | `OPS-A tests` run **34983809921** on `63b7bbe0`: **success** (14:45:35Z); all PR checks SUCCESS (`pr194_state.json`, `opsa_tests_run_34983809921_GREEN.json`) |
| RED arm (D026) | throwaway branch `demo/opsa-tests-red-20260915` = `63b7bbe0` + one failing test (`CiRedProbeTests.test_ci_red_probe`, `assert False`) → draft PR **#195** → run **34983897746 FAILURE** at step `OPS-A unit tests` (`Ran 34 tests`, `FAILED (failures=1)`, the probe's assertion message in the log — `RED_RUN_34983897746_failed_excerpt.txt`); `gh pr view 195` at capture time showed `OPS-A tests (Python 3.12, Windows): FAILURE` and `mergeStateStatus: BLOCKED` — the BLOCKED came from the required `Bridge suite (Python 3.12)` check still being pending at that moment, not from the informational OPS-A job (which cannot block a merge by itself; `pr195_state_RED.json`); PR #195 closed unmerged, remote + local branch deleted (ls-remote 0), worktree removed. `master` untouched. |
| What this proves | the suite executes on a GitHub-hosted Windows runner from a clean checkout and the job turns RED on a real failing test. It proves nothing about `master` until PR #194 passes its T1 review and is merged by a separate word. |
| Not done | merge; making the context required (later owner step after WP-P0-26 acceptance per the CI policy's progressive rule); the P0-26 candidate `d81b07f6` (39 tests) is NOT what CI runs — CI runs whatever `test_opsa.py` is on the PR's head/master (33 tests on `fcac0ac6`) |

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
