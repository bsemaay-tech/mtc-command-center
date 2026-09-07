# Stale PR disposition — #20, #21, #22, #26 (2026-09-07)

**Class:** T3 process record; read-only comparison against current `master`
`afe52ea89473300e25555325def111cac599bdf1`, measured on the Windows host from an isolated
worktree (`git fetch origin pull/<n>/head`, `git merge-base`, `git merge-tree --write-tree`,
`git cat-file -e origin/master:<path>`). Owner instruction (2026-09-07): close a PR only when its
useful content is demonstrably merged, superseded, or invalid under current governance; record the
evidence first; do not rebase obsolete work merely to preserve it.

| PR | Head / base | Measured | Disposition |
|---|---|---|---|
| #20 `chore/repo-housekeeping-2026-07-15` | merge-base `8721bce0`, 1 ahead / 1,023 behind | `.gitignore` conflicts (`git merge-tree`). Both preserved prompt docs already exist on `master` (`11_TRIAGE/CODEX_GATE5_PROMPT_FAZ3B_STAGE2_2026-07-13.md`, `11_TRIAGE/CODEX_P2_RACE_FIX_PROMPT_2026-07-14.md`). Every ignore pattern the PR adds is already covered on `master`: `sites/**/dist|.vinext|.wrangler` (`.gitignore:194-196`), `research/**/*_checkpoint.pkl` and `*_partial.json` (`.gitignore:199-200`, which match `MEGA_walk_forward_checkpoint.pkl` / `MEGA_walk_forward_partial.json`). | **CLOSE — merged/superseded.** No content left to carry. |
| #21 `docs/exit-aware-plan-and-cleanup-2026-07-15` | merge-base `8721bce0`, 1 ahead / 1,023 behind | Conflicts on `_AI_MEMORY/archive/NEXT_STEPS_pre-2026-08-01.md`; `_AI_MEMORY/NEXT_STEPS.md` no longer exists on `master` (retired to history by the 2026-08-25 router fold, `552a41ec`). The plan doc (`EXIT_AWARE_GAUNTLET_TOOLING_PLAN_2026-07-15.md`) is self-labelled "PLAN ONLY — not approved to build"; its tooling was then built in PR #22 and BLOCKED at Gate-5 (below). Under OD-20260826-3/-8 promotion-gate implementation is stopped pending a specified decision package, so the plan cannot be approved in its July form. | **CLOSE — superseded/invalid under current governance.** If an exit-aware gauntlet is revived, it must be respecified under the OD-20260826-3 decision package, not resumed from this plan. |
| #22 `feature/exit-aware-gauntlet` | merge-base `8721bce0`, 10 ahead / 1,023 behind | `git merge-tree` reports no textual conflict (its five new files are absent from `master`; its four modified QuantLens tools are unchanged on `master` since the base). But the PR was **BLOCKED at Gate-5** by an independent Codex review that a Fable audit on `master` verified line-by-line (`11_TRIAGE/FABLE_AUDIT_CODEX_GATE5_PR22_2026-07-16.md`: A4/A5/A6/A9 CONFIRMED FATAL — the pre-reg's primary statistic had no executable implementation, gauntlet geometry unenforced, runner guards bypassable, decision table self-contradictory). The PR body itself lists `exit_aware_gauntlet.main()` as a stub and "Independent Gate-5 required". No required edit was ever applied (branch head unchanged since 2026-07-16). Current governance (OD-20260826-3: genuine DSR/BH-FDR/`robust_final`/positive-alpha gates need a specified decision package and separate approval; OD-20260826-8: promotion-pipeline implementation remains stopped; D015: FAZ 3B Stage 2 separately gated) forbids merging promotion-gate tooling on this basis. | **CLOSE — invalid under current governance (blocked, never repaired).** The branch stays on the remote for provenance; nothing is rebased. |
| #26 `feature/two-tier-policy` (draft) | merge-base `008e065e`, 1 ahead / 1,014 behind | All 19 files conflict (root `AGENTS.md` and the eight `04_SHARED/prompts/05_ai_workflow/*` prompts were rewritten by the MAP97 router fold; `_AI_MEMORY/DECISIONS.md` no longer exists on `master`). Its audit roster names `claude-opus-4-8`, superseded by D022 (exact `claude-opus-5`). Its substantive rules already live on `master` in `00_AGENT_PROTOCOLS/AGENTS.md` ("Lead and implementer are separate flagships"; exact `claude-opus-5` / `gpt-5.6-sol`; fresh, never-resumed audits; PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK; capped repair loops) and in root `AGENTS.md` ("Lead and implementer are separate flagships"). The `11_TRIAGE/contracts/` task-contract example is not on `master`; the mandatory claim mechanism it fed was retired by owner decision 6 (2026-08-26) and WP-P0-27's mechanical claim check is planned separately. | **CLOSE — superseded.** |

## Commands (from the isolated worktree)

```
git fetch origin pull/20/head:refs/pr/20   # likewise 21, 22, 26
git merge-base refs/pr/<n> origin/master
git rev-list --count <mb>..refs/pr/<n> ; git rev-list --count <mb>..origin/master
git merge-tree --write-tree --name-only origin/master refs/pr/<n>
git cat-file -e origin/master:<path>        # per added file
git grep -n -E "MEGA_walk_forward|vinext|wrangler|sites/" origin/master -- .gitignore
```

No branch was deleted, rebased, or force-pushed. Closing a PR does not delete its branch.

- **NEXT ACTION:** close the four PRs on GitHub with a comment pointing at this record.
- **WAITING FOR OWNER:** Nothing.
