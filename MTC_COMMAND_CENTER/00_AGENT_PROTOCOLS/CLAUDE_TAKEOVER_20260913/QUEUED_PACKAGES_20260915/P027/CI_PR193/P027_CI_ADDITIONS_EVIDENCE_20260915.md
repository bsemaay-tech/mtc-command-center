# WP-P0-27 — CI additions PR #193 evidence (2026-09-15, Claude Opus 5 Lead 743291)

**Authority:** `OD-20260915-P027-CI-ADDITIONS-GO-1` (owner "go" ~10:52Z). **Scope kept:** one file, `.github/workflows/research-gates.yml`; informational workflow; ruleset 21444962's required contexts untouched (`Bridge suite (Python 3.12)`, `pine-alert-guard`). **PR open, NOT merged** (workflow files carry the T1 roster — `CI_POLICY.md`).

| Step | Fact |
|---|---|
| Worktree | `C:/tmp/P027_CI_20260915` on `feature/p027-research-gates-additions-20260915` from `origin/master` `fcac0ac6` |
| Commit 1 | `55ab90b8` — jobs `p030-checkers` (windows-2025: the three repo-root P0-30 checkers) and `contracts-and-lint` (ubuntu-24.04: hash-locked Bridge lock install → `MTC_COMMAND_CENTER/contracts` pytest → `ruff==0.16.4` → `ruff check --select E9,F821,F811,F401,F841 MTC_COMMAND_CENTER/tools/opsa MTC_COMMAND_CENTER/contracts`); guard PASS before commit (`LEAD_GUARD_CI_PR.txt`) |
| PR | https://github.com/bsemaay-tech/mtc-command-center/pull/193 (opened 11:04Z) |
| First run | `Research gates` run 34961383292: `Contracts tests and Ruff` SUCCESS, `Research gate checkers` SUCCESS, **`P0-30 checkers (Windows)` FAILURE at the checkout step** — `error: unable to create file MTC_COMMAND_CENTER/03_QUANTLENS/research/restart_transcript_intake_audit_…: Filename too long` (Windows 260-char default; the repo carries longer paths). `research_gates_run_34961383292_RED_checkout.json` |
| Commit 2 | `a3325836` — `git config --system core.longpaths true` step before `actions/checkout` in the Windows job (nothing else changed) |
| Green run | `Research gates` run 34963602576 on `a3325836`: `P0-30 checkers (Python 3.12, Windows)` SUCCESS (11:30:02Z→11:30:42Z), `Contracts tests and Ruff (Python 3.12)` SUCCESS (11:30:02Z→11:30:29Z), `Research gate checkers (Python 3.12)` SUCCESS; `CI` run 34963602580 SUCCESS; `Pine Defang Guard` run 34963602573 SUCCESS. `research_gates_run_34963602576.json`, `pr193_state_GREEN.json` (`mergeStateStatus: CLEAN`) |
| What this proves | the three P0-30 checkers, the 50 contracts tests and the Ruff step execute on GitHub-hosted runners from a clean checkout (R2 "light lint", R10, R12 of the reconciliation move from MISSING/PARTIAL to "wired, informational"). It proves nothing about master until the PR is reviewed (T1) and merged by a separate word. |
| Local pre-checks | contracts 50 passed from `MTC_COMMAND_CENTER/contracts` (P020 venv 3.12.12); Ruff clean on the two scoped directories at `fcac0ac6`; other surfaces NOT clean (3 findings repo root, 21 `IBKR_PAPER_BRIDGE`, 69 `03_QUANTLENS/tools`) — deliberately excluded so the job does not start red |
| Not done | merge; wiring `tools/opsa/test_opsa.py` (OPS-A suite, also uncovered — follow-up candidate named in the PR body); widening Ruff |

Recorded by Claude Opus 5 Lead (743291).
