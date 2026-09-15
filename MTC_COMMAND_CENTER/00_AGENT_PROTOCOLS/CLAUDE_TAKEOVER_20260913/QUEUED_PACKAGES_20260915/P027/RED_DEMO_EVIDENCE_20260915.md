# WP-P0-27 D026 demonstration — GREEN → deliberate RED → GREEN on the required check, executed 2026-09-15 08:16-08:22Z (Lead: Claude Opus 5, session 743291)

Plan followed: `11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/RED_GREEN_PLAN.md` §3 (throwaway branch, one failing test, draft PR into master, never merged).

| Step | Commit / object | Observed |
|---|---|---|
| Baseline GREEN on master | `fcac0ac6` (PR #191 merge) | `Bridge suite (Python 3.12)` success 2026-09-13T08:10:55Z→08:12:23Z; every master run since the first (2026-09-05) is success; **no `failure` conclusion existed in the last 200 CI runs before today** |
| RED probe | branch `demo/wp-p0-27-red-20260915` @ `9bf4ca0e` = master + `IBKR_PAPER_BRIDGE/tests/test_ci_red_probe.py` (`assert False, "deliberate WP-P0-27 D026 red probe (2026-09-15)…"`) | draft PR **#192** https://github.com/bsemaay-tech/mtc-command-center/pull/192 |
| RED run | https://github.com/bsemaay-tech/mtc-command-center/actions/runs/34946092493 | job `Bridge suite (Python 3.12)` **failure** 08:16:55Z→08:18:45Z; steps checkout/setup/install/compile success, **`Run Bridge test suite` failure**, `Publish failure annotation` success; log names `test_ci_red_probe` and the assertion message (`RED_RUN_34946092493_failed_log.txt`) |
| Required check blocks the merge | `gh pr view 192` while red (`PR192_state_RED.json`) | `mergeStateStatus: BLOCKED`, rollup `Bridge suite (Python 3.12): FAILURE`, `pine-alert-guard: SUCCESS`, `Research gate checkers: SUCCESS` (not required) |
| GREEN again | `179890c5` = probe file removed | run https://github.com/bsemaay-tech/mtc-command-center/actions/runs/34946405229 **success** 08:20:23Z→08:22:01Z; `gh pr view 192` → `mergeStateStatus: CLEAN` (`PR192_state_GREEN.json`) |
| Notification | GitHub-native Actions failure e-mail to the subscribed account (`CI_POLICY.md` §Day-one check) | **owner-side: did a "Run failed: CI" e-mail for run 34946092493 arrive? (one line)** — the workflow's `::error` annotation and step summary were emitted (see the failed log) |
| Closure | PR #192 closed without merge; branch `demo/wp-p0-27-red-20260915` deleted; local worktree removed | see the closure lines appended below |

Interpretation: the required check turns RED on a real failing test and the ruleset blocks the PR; removing the failure restores GREEN and the PR becomes mergeable — the D026 pair the acceptance gate demanded. The `Research gates` and `Vercel` checks are informational (not in ruleset 21444962). No master run was affected; nothing was merged.
2026-09-15T08:23:26Z closure: PR #192 CLOSED (not merged); remote branch deleted (ls-remote count above = 0); worktree C:/tmp/P027_RED_DEMO_20260915 removed; local branch deleted.
2026-09-15T08:23:44Z correction: the remote branch survived gh's --delete-branch (local worktree blocked it); deleted explicitly with git push --delete; ls-remote count now 0. PR #192 state CLOSED, merged=false.
2026-09-15T08:32Z owner statement (chat, verbatim "yes"): the GitHub "Run failed: CI" e-mail for run 34946092493 was received. Notification half CLOSED on the owner's word; an immutable artifact (message headers / sanitized screenshot) is NOT on record (Gemini counted-corroboration NIT F-02) — to be added only if the owner allows the Lead to read that one notification from his mailbox.

2026-09-15T11:48Z artifact: the owner forwarded a GitHub Actions failure e-mail (the PR #193 first-run notification of 11:06Z, run 34961383292 — not the 08:18Z demo mail) to the connector account; captured read-only with tokens redacted as `CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md`. It is the immutable artifact of the delivery channel Gemini F-02 asked for; the demo-run mail itself remains owner-confirmed only unless forwarded too.
