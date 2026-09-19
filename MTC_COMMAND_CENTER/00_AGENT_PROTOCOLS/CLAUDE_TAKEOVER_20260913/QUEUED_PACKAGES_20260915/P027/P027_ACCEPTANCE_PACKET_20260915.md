# WP-P0-27 (OPS-C, repo-root CI home) — acceptance packet for the owner — 2026-09-15 (night)

Prepared by the Claude Opus 5 Lead (session 5, `03c6c8`) from the 2026-09-15 reconciliation (`P027_REQUIREMENT_RECONCILIATION_20260915.md`, R1-R20, counted Gemini corroboration PASS-WITH-NITS 10:17Z, NITs applied) plus the facts re-read tonight (14:00-14:40Z: GitHub API, `origin/master` `fcac0ac6`, CT13 `f1bbac40`). **This packet accepts nothing.** Acceptance of WP-P0-27 is the owner's act on the Lead's recommendation (plan §WP-P0-27, audit tier T1). Everything here is documentary (T2/T3); no workflow, setting, host or venue was touched tonight.

## 0. The one-line decision asked of the owner
"**P0-27: accept day-one scope**" — or "**not yet**" (+ what is missing) — see §7 for what each word does and does not do.

## 1. What "day-one scope" means, in plain language
The repository has a working continuous-check home: three workflow files at the repository root run on GitHub's own runners on every pull request into `master` and every push to `master`; two of their checks are *required* — a pull request cannot be merged while either is red — and the rule allows no bypass for anyone. The day-one job runs the whole Bridge test suite. A red run on `master` triggers GitHub's failure e-mail. The plan's four acceptance clauses (§2) were each demonstrated with real runs. **What day-one does NOT include** (plan's progressive backlog, §4): the golden suite, the parity set, the safety-operations checks (restore-proof freshness, drill currency, credential expiry, monitoring health), the mechanical delivery guards, and making `Research gates` a required check. Those plug in later, each with its own evidence; accepting day-one does not claim them.

## 2. The plan's acceptance gate (line 599 of the master plan) — clause by clause
| Clause (plan text) | Evidence (verified tonight unless dated otherwise) | State |
|---|---|---|
| (a) "the root workflow runs green on the Bridge suite" | `ci.yml` blob `3394d9ff…` on `origin/master` `fcac0ac6`; check context `Bridge suite (Python 3.12)`; **61 `ci.yml` runs on `master`: 60 success, 1 failure** (GitHub API, tonight); last master run = PR #191 merge, success | ✔ |
| (b) "a deliberately broken test is shown to turn the run red and trigger the notification (D026)" | draft PR #192 (2026-09-15 08:16-08:23Z): `test_ci_red_probe.py` (`assert False`) → run **34946092493 FAILURE** at step `Run Bridge test suite` (log on record); probe removed → run **34946405229 success**; PR closed unmerged, branch deleted, `master` untouched. Notification: GitHub "Run failed: CI" e-mail for the RED run **owner-confirmed in chat ("yes", ~08:32Z)**; an immutable artifact of the delivery channel exists for the *PR #193* failure mail of 11:06Z (forwarded by the owner, Gmail id `1a0a4d879a3c386d`, tokens redacted) — the demo mail itself is owner-word only | ✔ (notification half: owner word + channel artifact) |
| (c) "the required-check setting on PRs is demonstrated" | ruleset **21444962 "Protect master – required CI"**, `enforcement: active`, required contexts `Bridge suite (Python 3.12)` + `pine-alert-guard`, strict up-to-date policy `true`, bypass actors **0** (API, tonight; ruleset `updated_at` 2026-08-29 11:25 local — `pine-alert-guard` was recorded as NOT required on 2026-08-25 (`CI_POLICY.md`) and still not required in the 2026-08-28-night stage handoff, and is required now, so that 08-29 update most likely added it; the audit log was not queried); while PR #192 was red `gh pr view` showed `mergeStateStatus: BLOCKED` with `Bridge suite (Python 3.12): FAILURE`; after the fix `CLEAN`; every merge since PR #127 (2026-08-25) went through the rule | ✔ |
| (d) "WP-P0-10 and WP-P0-23 may not claim continuous protection before this package is accepted" | **R19 sweep executed tonight** (CT13 `f1bbac40`, all `.md/.py/.yml/.json/.txt` outside `_AI_MEMORY/history/`): no merged record, register row or evidence pack describes WP-P0-10, WP-P0-23 or OPS-C as "built / running / protecting"; the only hits are the plan text itself, the Wayfinder fold's dependency column ("what this package unblocks"), and the 2026-09-13/15 assessment records that restate the rule. No register row says `PROVEN` for the safety-ops checks | ✔ (holds at the acceptance step) |

## 3. Requirement rows R1-R20 — condensed (full text and citations in the reconciliation)
| Row | Requirement | State at acceptance | In day-one scope? |
|---|---|---|---|
| R1 | root workflows, hosted runners, no secrets, no venue contact | IMPLEMENTED + VERIFIED | yes |
| R2 | day-one job = Bridge suite + light lint | Bridge suite ✔; lint = `compileall` only on `master`; Ruff step WIRED in PR #193 (open) | yes (lint at the `compileall` level; Ruff = backlog until PR #193's T1) |
| R3 | checks required on PRs into master | IMPLEMENTED + VERIFIED | yes |
| R4 | "direct Lead pushes remain allowed" | DEVIATES by owner decision (`OD-20260826-4/-6`: PR-only, no bypass) — recorded, no action | yes (as ruled) |
| R5 | red master notifies; master never stays red | IMPLEMENTED; RED path PROBE-VERIFIED (PR #192); e-mail OWNER-CONFIRMED + channel artifact; **plus the one real incident (§5)**: master red 2026-08-25 12:10Z, fixed forward, green 15:04Z, before protection existed | yes |
| R6 | D026 deliberate red demo | EXECUTED 2026-09-15 (PR #192) | yes |
| R7 | required-check demonstrated | VERIFIED | yes |
| R8 | WP-P0-23 no-`alert(` guard plugs in | IMPLEMENTED + REQUIRED (`pine-alert-guard`) | yes |
| R9 | WP-P0-10 golden suite in CI | NOT IN CI (dependent on P0-10, parked) | no — backlog |
| R10 | WP-P0-21 admission fixtures in CI | `check_market_data_collector.py` runs; three P0-30 checkers WIRED in PR #193 (open) | partly — backlog |
| R11 | §9.6 parity set in CI | NOT IN CI (parity package undelivered) | no — backlog |
| R12 | contract tests in CI | WIRED in PR #193 (open, informational) | no — backlog until PR #193's T1 |
| R13 | two inert `02_MTC_BACKTEST` workflows retired | RECORDED, NOT RETIRED (protected scope; harmless) | no — deferred to the engine retirement |
| R14 | safety-ops checks (restore-proof freshness, drill currency, credential expiry, monitoring health) | DEPENDENT on WP-P0-26 (candidate `d81b07f6` under review) | no — backlog |
| R15 | delivery-doctrine guards (concurrent-writer block, UNKNOWN-cleanup block) | MISSING (planned, not built; `AGENTS.md` says so) | no — backlog, separately scoped lane |
| R16 | progressive activation, no big-bang | IMPLEMENTED (two required contexts; `Research gates` informational) | yes |
| R17 | no self-hosted runner, no scheduled jobs, no ported retired workflows | VERIFIED | yes |
| R18 | rollback = delete the workflow files | VALID | yes |
| R19 | no continuous-protection claims by P0-10/P0-23 before acceptance | HOLDS (sweep tonight, §2d) | yes |
| R20 | notification also to the WP-P0-26 paging channel "when it lands" | DEPENDENT on WP-P0-26 (no channel exists) | no — backlog |

**Day-one scope = R1-R8, R16-R19 (12 rows).** Backlog = R9-R15, R20 (8 rows), each with its completion condition in reconciliation §4.

## 4. Evidence index (what to open if you want to see it yourself)
| # | Item | Where | Identity |
|---|---|---|---|
| E1 | The three workflows on `master` | `.github/workflows/` at `fcac0ac6` | blobs `ci.yml 3394d9ff…`, `pine-defang-guard.yml db5a950b…`, `research-gates.yml e8c520f6…` |
| E2 | The rule that blocks red merges | GitHub ruleset 21444962 (API query tonight) | active; 2 required contexts; strict; 0 bypass actors |
| E3 | RED demo | `RED_DEMO_EVIDENCE_20260915.md`; `RED_RUN_34946092493_failed_log.txt`; `PR192_state_RED.json` / `PR192_state_GREEN.json` | PR #192, runs 34946092493 (failure) / 34946405229 (success) |
| E4 | Failure e-mail — owner word | RUN_STATE 08:32Z; `RED_DEMO_EVIDENCE` 08:32Z line | chat "yes" |
| E5 | Failure e-mail — channel artifact | `CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md` (repository record; the copy staged for the Gemini packet is named `CI_FAILURE_EMAIL_ARTIFACT_MASKED.md` with the mailbox addresses masked — same content, same message id) | Gmail id `1a0a4d879a3c386d`, sender `notifications@github.com`, run 34961383292 (PR #193 first run) |
| E6 | Run history on `master` | GitHub API tonight | 61 `ci.yml` runs: 60 success, 1 failure (`110305c0`, 2026-08-25 12:10:43Z) |
| E7 | Requirement reconciliation R1-R20 | `P027_REQUIREMENT_RECONCILIATION_20260915.md` (+ addendum 11:42Z) | CT13 `QUEUED_PACKAGES_20260915/P027/` |
| E8 | Gemini T2 corroboration (read-only, `SUPPLEMENTAL_UNEXECUTED`) | `QUEUED_PACKAGES_20260915/GEMINI_RESPONSE_attempt3_COUNTED.md` + `LEAD_ADJUDICATION_GEMINI_CORROBORATION.md` | counted attempt 3, 10:04-10:17Z, PASS-WITH-NITS (3 NITs, 0 REQUIRED), all applied; R1-R20 AGREE on every row |
| E9 | Day-one package review lineage (2026-08-25) | `11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/` (4 docs) + `C:/tmp/LANE_PROMPTS_20260825/GLM_AG_P027_REPORT.md` | see §6 |
| E10 | PR #193 (the two extra informational jobs; NOT part of this acceptance) | `CI_PR193/P027_CI_ADDITIONS_EVIDENCE_20260915.md` | head `a3325836`, blob `609de49a…`, all checks SUCCESS, `mergeStateStatus: CLEAN`, OPEN, unmerged (tonight) |

## 5. Precision corrections found tonight (nothing changes the recommendation)
1. The reconciliation §1 said "across the last 200 CI runs there is no `failure` conclusion at all … until today no run had ever turned RED". **Wrong as a global statement.** The GitHub API (workflow `ci.yml`, branch `master`, tonight) returns **exactly one failed run: 32846169952 at `110305c0`, 2026-08-25 12:10:43Z** (the WAL merge; the two CPython-GC-referent tests) — repaired forward by `cef1d070`, green at 15:04:24Z, **before** the ruleset was created (15:24:47Z). So: (i) `master` has been red once, naturally, for 2 h 54 min, and the "fix forward, never stays red" rule was exercised for real; (ii) no *deliberate* red demonstration existed before PR #192 — that part of the sentence stands. The 200-run query of the morning evidently spanned all workflows / a shorter window. Corrected here; the reconciliation file is left as written with this packet as its erratum.
2. The e-mail artifact on record is the **PR #193** failure mail (11:06Z), not the demo-run mail (08:18Z). Both come from the same channel (`notifications@github.com` → the owner's GitHub-notification address). The demo mail stays owner-word evidence unless forwarded (the handoff's "no rush" line).

## 6. Review lineage — what verdicts actually exist (so the acceptance rests on the right thing)
- **Day-one package (workflow `ci.yml` + `CI_POLICY.md`, `LANE_REPORT.md`, `LINUX_RED_DIAGNOSIS.md`, `RED_GREEN_PLAN.md`), 2026-08-25:** T1 Gate-5 audit at branch head `4e3b0242` → **PASS-WITH-NITS, zero required findings** (`GLM_AG_P027_REPORT.md`; nits closed in `c34b9340`); merged to `master` as `d5e5e98e` ("lane K, T1 PASS-WITH-NITS 2026-08-25"). **The auditor in that T1 slot was GLM-5.3** (run through the Claude Code SDK with a model override — the run log's `unrecognized_model {"model":"glm-5.3"}` line), not an exact flagship. The stage contract allows GLM in the T1 slot for a diff over ~300 lines (this one was 798 insertions), so the slot was contract-conformant; it is stated here because the report calls itself "flagship auditor" and the owner should know which model it was.
- **The workflow file itself** (`ci.yml` blob `3394d9ff…`, byte-identical then and now) was additionally inside the **Codex `gpt-5.6-sol` xhigh T0 audit** of the WAL capture-ordering lane (round 1 at `67a53a32`, GitHub run 32806840756), which "independently verified" the blob identity (`WAL_CAPTURE_FIX_2026-08-25/FIX_EVIDENCE.md:24-25`).
- **Gemini corroboration** (mandatory since `OD-20260829-1`, i.e. after the 08-25 audit): the 2026-09-15 counted read-only review covered the reconciliation and the demo evidence (E8), not the workflow bytes as a code review.
- **`pine-defang-guard.yml`** came with WP-P0-23 (T0 lane, merged 2026-08-25) and is required by the ruleset; **`research-gates.yml`** came via PR #162 (2026-09-07, `11bddf3b`, informational, not required) — neither is part of the day-one acceptance object; both are the progressive policy operating.
- **No fresh exact-flagship review was run tonight** (Codex capped to Sep 19; Claude Pro Opus resets Wed 20:00Z; owner routing order: no Claude lanes for audits). If the owner wants an exact-flagship T1 read of the unchanged day-one files before accepting, that is one Opus lane on Wednesday (~20 min) or one Sol lane on Friday — the Lead's view is that it is optional: the bytes have not changed since the recorded T1 verdict and the acceptance clauses are demonstrated by runs, not by reading.

## 7. The Lead's recommendation and what each owner word does
**Recommendation: accept WP-P0-27 at day-one scope (R1-R8, R16-R19), with R9-R15 and R20 recorded as the progressive backlog.** All four acceptance clauses are demonstrated by real runs and a live rule; the only owner-side element is the failure e-mail, which the owner confirmed and whose channel has an immutable artifact.

| Owner word | What the Lead then does (G7 write-back, T3) | What it does NOT do |
|---|---|---|
| "accept day-one scope" | adds row `OD-20260915-P027-DAYONE-ACCEPT-1` to `C:/CT13/DECISIONS.md` (verbatim word, scope = 12 rows, backlog = 8 rows); appends the acceptance to `11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md` status line and the stage `HANDOFF.md`; records the R19 sweep result; updates the package map in the handoff §2 (P0-27 → ACCEPTED day-one) | does NOT merge PR #193 (T1 review of the workflow diff first — Wednesday Opus or Friday Sol); does NOT make `Research gates` required; does NOT let any document call OPS-C "protecting" beyond the two required checks; does NOT change the ruleset |
| "not yet" (+ reason) | records the reason as the open item; nothing else moves | — |
| "accept, and add the exact-flagship read first" | Wednesday Opus lane (queue slot after lanes 1-4, ~20 min) on the four day-one files at `fcac0ac6`; acceptance recorded after that verdict | — |

## 8. NOT VERIFIED (carried, honest)
- The demo-run e-mail as an immutable artifact (owner-word only); the PR #193 run mail proves the channel, not that specific message.
- A failing run of `pine-alert-guard` (required, but never red; its RED/GREEN evidence belongs to WP-P0-23's own record).
- Runner-side settings beyond what the GitHub API exposes; whether GitHub's e-mail reaches the owner for *every* failure (one channel artifact, one owner confirmation).
- `research-gates.yml`'s own review record (PR #162) — informational workflow, outside this acceptance.

## 9. Files
- This packet: `C:/tmp/CLAUDE_P0_RUN_20260913/P027_RECONCILIATION_20260915/P027_ACCEPTANCE_PACKET_20260915.md` → copied to CT13 `00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/QUEUED_PACKAGES_20260915/P027/`.
- Sweep command (R19): `grep -rn -i "continuous protection|continuously protect|continuous-protection|gates repository changes|protects master|protecting master|CI protects|guard protects"` over CT13 `f1bbac40` (`.md .py .yml .json .txt`, excluding `_AI_MEMORY/history/`) + `OPS-C` × `built|running|protect|PROVEN|live` + the four ops-check names × `PROVEN` — 0 claims.
- GitHub queries (tonight): `gh run list --workflow ci.yml --branch master --limit 300` (61 runs; 60 success / 1 failure); `gh api repos/…/rulesets/21444962`; `gh pr view 193 --json state,mergeStateStatus,headRefOid,statusCheckRollup`.
