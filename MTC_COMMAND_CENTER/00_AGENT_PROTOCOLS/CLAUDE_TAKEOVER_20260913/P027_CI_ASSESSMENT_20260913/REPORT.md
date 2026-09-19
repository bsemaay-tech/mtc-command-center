# REPORT — WP-P0-27 continuous-check assessment (P27CI / D YES)

**Lane:** Grok 4.6, SuperGrok subscription, no delegates, no other providers.
**Date:** 2026-09-13.
**Working directory only:** `C:/tmp/P027_CI_20260913/`.
**Authorization:** owner "D YES" = read-only assessment. No workflow edits. Preserve existing Bridge tests and protected merge checks.

## What this lane did

Read, and only read, the inputs named in `TASK_GROK.md`:

- Plan `### WP-P0-27` at `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:590-602` and ticket #43 at `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md:20`.
- Prior lane `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/` (`CI_POLICY.md`, `LANE_REPORT.md`, `LINUX_RED_DIAGNOSIS.md`, `RED_GREEN_PLAN.md`).
- All three current root workflows under `C:/CT13/.github/workflows/`.
- `C:/CT13/MTC_COMMAND_CENTER/tools/repo_guard.ps1`, `MTC_REPO_GUARD_PROTOCOL.md`, `REVIEW_POLICY.md`, Bridge `tests/` modules, `TESTS.md`.
- Protected-paths hook and policy; Architecture.md §14.4; owner ruling HIST-2026-0032; common gitdir hooks listing.
- START_HERE P0-27 row; SESSION_LOCK; P021/P030/P022/P026 adjacent records needed to classify remaining plug-ins.

Wrote only inside the working directory. Did not run Git (including `git status` / `git rev-parse HEAD`). Did not use the network. Did not install packages, contact a host, send a message, install a schedule, or trade. Did not spawn agents.

## Deliverables

| File | Role |
|---|---|
| `CI_CHECK_INVENTORY.md` | Check table: location (file:line), what it proves, event, LIVE / DECLARED-BUT-NOT-WIRED / MISSING. Bridge entry-point list. Hook confirm/refute. |
| `CI_ASSESSMENT.md` | Per remaining check IMPLEMENT (YAML described, not applied, with tier) or DEFER (reason + unblock). No-weaken statement. Owner questions with recommended answers. |
| `REPORT.md` | This file, including NOT VERIFIED. |
| `SHA256SUMS.txt` | SHA-256 of the three Markdown deliverables. |

## Headline (not an acceptance)

Functioning repo-root CI exists: Bridge suite + compileall, Pine empty-allowlist guard, and WP-P0-20 research-gate checkers. The recorded protected merge check is still exactly `Bridge suite (Python 3.12)` under ruleset 21444962. That is not a claim that WP-P0-27 is accepted, that every plan guard is continuous, or that GitHub's live ruleset was re-queried today.

Do not describe OPS-C as fully built. Do not repeat "no functioning CI" as a current fact. Do not weaken the Bridge pytest command or the required Bridge context.

IMPLEMENT later (new non-required stdlib jobs only): OPS-A `test_opsa.py`, three P030 checkers, P022 tracker tests. Everything else DEFER, including making Pine or research-gates required, golden/parity/admission CI, ops freshness/currency/expiry/monitoring, concurrent-writer and cleanup guards, paging, and the protected-paths hook.

## Protected-paths hook (task lesson)

**Refuted as an in-force mechanical guard; confirmed as an unwired script.**

- Architecture still describes a mechanical pre-commit guard (`C:/CT13/MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md:1289-1300`).
- Corrected policy: trailer is hand-validated; script "installed nowhere and invoked by nothing" (`C:/CT13/MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:24-30`).
- No root workflow names it. Common hooks dir listing for this worktree's gitdir contained only `*.sample` files.
- Owner ruling 2026-09-10 rejected CI wiring and `core.hooksPath` (`TASK_HISTORY.json:289`; policy `:82-84`).

## Boundaries observed

- Read-only outside cwd.
- No Git command in any repository.
- No network, credentials, deployment, host, schedule, or trading.
- No decision, acceptance, or authorization. Owner items in `CI_ASSESSMENT.md` are questions with recommended answers.
- Factual claims in the inventory/assessment are cited as `absolute/path:line` with a quote. Claims that could not be cited are in NOT VERIFIED below.

## NOT VERIFIED

This section is required to be non-empty. Each item is something this lane could not cite from a file:line it read, or could not re-measure because Git/network/execution are forbidden.

1. **Live GitHub ruleset 21444962 as of 2026-09-13.** Last citable dump is `CI_POLICY.md:41-71` dated 2026-08-25 (`gh api` commands listed there were not re-run). Protocol files still *assert* the same required context (`AGENTS.md:50-51`; `TESTS.md:26-27`; `research-gates.yml:8-9`). Whether GitHub still has that exact ruleset, required context list, empty bypass, and strict up-to-date policy today is not re-verified.

2. **Live GitHub Actions conclusions on current `master`.** Handoffs cite green Bridge/Pine/research runs (e.g. `P022_HANDOFF.md:38` run `34747043884`; `P021_P030_HANDOFF.md:24`). This lane did not fetch those runs.

3. **GitHub-native failure email delivery** to the Lead inbox. `RED_GREEN_PLAN.md:101` still says "Pending email proof". `CI_POLICY.md:36-38` says delivery depends on account notification settings. Not observed here.

4. **`core.hooksPath` on this checkout and on the canonical repo.** Policy measured it unset on 2026-09-10 (`PROTECTED_PATHS_POLICY.md:35`). This lane did not run `git config`. The common `hooks/` directory listing is a directory listing, not a Git config value.

5. **Completeness of the common `hooks/` directory** beyond the names listed in this session (all `*.sample`). No file in-tree enumerates that directory with line numbers.

6. **What the "Vercel" check is.** `HANDOFF.md:10-11` and `P021_P030_HANDOFF.md:24` mention Vercel checks passing. There is no Vercel workflow under `C:/CT13/.github/workflows/`. Identity (GitHub App vs something else), required-status, and current existence are unverified.

7. **Pytest collection counts and pass/fail of the Bridge suite (or any other suite) on this tree.** Modules were read; they were not executed. `LANE_REPORT.md:43` historical `1370 passed, 1 warning` (also `:177`) is a 2026-08-25 record, not this checkout.

8. **Whether P021's 103 tests still pass, and the exact five commands behind `39 + 7 + 5 + 6 + 46`.** Count is a handoff record (`P021_P030_HANDOFF.md:30`); logs live outside the repository (`C:/tmp/p021_*_postmerge.log`) and were not opened.

9. **WP-P0-27 package-acceptance state** (Lead call, `CI_POLICY.md:18-19`). This assessment is not that call.

10. **Whether `master` is green right now**, and whether the D026 GREEN/RED/GREEN demonstration table in `RED_GREEN_PLAN.md:99-102` was later filled in some other evidence pack. `CI_POLICY.md:115-120` records historical green runs through 2026-08-25; this lane did not extend that series.

11. **Deployed KVM2 / host CI-adjacent state** (restore proofs, monitoring, paging). Repository records treat it as UNVERIFIED pending G9 (`MASTER_WORK_PACKAGE...md:581`). This lane did not contact the host.

12. **Hash identity of workflow files versus `origin/master`.** `LANE_REPORT.md:30-32` recorded blob `3394d9ff...` on 2026-08-25. This lane did not run `git hash-object` or `git rev-parse`. The files were read as they stand on disk in `C:/CT13`.

13. **Ticket #43 resolution comment body** on GitHub. Only the fold's gist was read (`WAYFINDER_DECISION_FOLD_2026-08-23.md:20`). The fold itself says "the full detail of every decision lives in its ticket's resolution comment" (`:5`).

14. **Pydantic / extra-dependency closure** needed to run P021 or `mtc_contracts` tests on a GitHub-hosted runner. Not measured; that is why those jobs are DEFER rather than IMPLEMENT.

15. **Whether `actions/checkout@v4` in root `ci.yml` leaves `HEAD` as `master` or detached.** Checkout step is `uses: actions/checkout@v4` with `persist-credentials: false` and no `ref:` (`C:/CT13/.github/workflows/ci.yml:27-29`). `C:/CT13/MTC_COMMAND_CENTER/tools/repo_guard.ps1:63-66` BLOCKs when `git rev-parse --abbrev-ref HEAD` is `master` or `main`. This lane did not run Actions, so the Actions branch name is not a cited fact.

16. **Whether REVIEW_POLICY candidate OD-20260909-1 is activated on `origin/master`.** `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md:6-8` says it is prospective. `C:/CT13/MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:17-19` records "Protected integration is tracked by PR #167; activation requires the merged PR and protected CI on its final head." Live merge/CI of that PR was not queried.

## What this is not

Not a workflow PR. Not package acceptance. Not a ruleset change. Not authorization to implement the three described jobs. Not a claim that remaining DEFER items are optional forever — they stay named, with unblocks.

## Corrections P27FIX

Text-only pin and contradiction fixes after `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKP27_grok_audit/GROK_AUDIT_REPORT.md`. No IMPLEMENT/DEFER classification changed. NOT VERIFIED grew from 14 items to 16 (items 15–16 added; none removed).

- `CI_ASSESSMENT.md:9` — quoted `REVIEW_POLICY.md:6-8` prospective-activation caveat; tier labels are classification vocabulary, not an in-force claim.
- `CI_ASSESSMENT.md:19` — `ci.yml` pin `:1-11` → `:1-12` so `contents: read` is inside the range.
- `CI_ASSESSMENT.md:37` — "keep running" → "keeps running".
- `CI_ASSESSMENT.md:40`, `:231`, `:330` — dropped "would BLOCK every push"; cited local `repo_guard.ps1:63-66` HEAD test and `ci.yml:27-29`; Actions HEAD name is NOT VERIFIED #15. `:231` also replaced "Local-only by design" with `MTC_REPO_GUARD_USAGE.md:7-9` preflight bytes.
- `CI_ASSESSMENT.md:63` — 8/16 MET pin `START_HERE.md:33` → `:35`.
- `CI_ASSESSMENT.md:67`, `:79`, `:91` — T0 quote pin `REVIEW_POLICY.md:19` → `:20`.
- `CI_ASSESSMENT.md:79` — WP-P0-10 T0 pin `MASTER_WORK_PACKAGE...md:386` → `:387`.
- `CI_ASSESSMENT.md:85` — pydantic/`mtc_contracts` imports `test_p021_eligibility.py:14-16` → `:10-12`.
- `CI_ASSESSMENT.md:107` — remaining P013/P020 work `START_HERE.md:41-42`/`:33` → `:43`/`:35`.
- `CI_CHECK_INVENTORY.md:9` — Status-column qualifiers documented; Vercel remains NOT VERIFIED (`:92`).
- `CI_CHECK_INVENTORY.md:52` — Bridge failure annotation is a later step of job `bridge` (`ci.yml:19`, `:47-48`), not a downstream job.
- `CI_CHECK_INVENTORY.md:54` — `ALERT_NEEDLES` is `:9`; `ALLOWLIST` is `:10`.
- `CI_CHECK_INVENTORY.md:62` — quoted "the binding this checks for does not yet exist" at `:12-14`; token `NOT_BOUND` at `:28`.
- `CI_CHECK_INVENTORY.md:63` — file set is git-tracked-or-trackable (`generate_index.py:16-18`); `--check` byte-identical is `:61-65`.
- `CI_CHECK_INVENTORY.md:73` — `test_compat.py` pytest `:5`, pydantic `:6`.
- `CI_CHECK_INVENTORY.md:87` — default packet path `check_review_report.py:24`.
- `CI_CHECK_INVENTORY.md:88` — local master/main BLOCK cited; Actions HEAD name NOT VERIFIED.
- `CI_CHECK_INVENTORY.md:90` — inert `tests.yml` push paths listed from `:3-10`.
- `REPORT.md` NOT VERIFIED — added items 15 (Actions HEAD name) and 16 (OD-20260909-1 activation).
- `SHA256SUMS.txt` rewritten (LF) for the three edited deliverables.

## Lead mechanical corrections (2026-09-13 21:09Z)
Applied by the Claude Lead after the Grok delta re-audit (lane GKP26B/GKP27B) reported all prior findings RESOLVED and only these residual pin/attribution items; each was verified against the source bytes before editing:
- CI_CHECK_INVENTORY.md:81 brief pin 2783->2784
- CI_ASSESSMENT.md:169 G6 attribution (plan P029 :621, not REVIEW_POLICY G6 :68)
- REPORT.md:71 LANE_REPORT.md:43 pin for `1370 passed, 1 warning`

