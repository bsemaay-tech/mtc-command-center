# Worktree cleanup — Batch 2 revalidation slate (PREPARED, AWAITING OWNER APPROVAL)

**Nothing here is removed.** Owner instruction 2026-08-17: prepare the Batch 2
revalidation slate only; remove no additional worktree until the owner approves the
exact list. Registered worktrees now: **149**.

## Classes (fresh sweep 2026-08-17, post-deployment)

| Class | Count | Disposition |
|---|---|---|
| Protected / DO NOT TOUCH | 7 | never in any batch |
| Clean + remotely reachable + idle ≥2 days | 91 | removal candidates (this slate draws from here) |
| Dirty tree | 33 | Group C — per-tree keep/discard decision, not here |
| Unreachable HEAD | 18 | Group C/D — needs push or inspection, not here |

Protected set (unchanged): `C:/LAB/Tradingview_LAB_CLEAN`, `C:/P2RT` (runs live
`MTC-Bridge-P2`), `C:/R7FINAL` (deployment-owner session working tree),
`C:/BRIDGE_RELEASE_INTEGRATION_20260815`, `C:/P9IMP`, `C:/GEMINI`,
`C:/BRIDGE_HELP_IMPL`.

## PROPOSED BATCH 2 — first 10 (for owner approval)

Each was revalidated this sweep: directory exists, clean tree, HEAD reachable from
the named `origin/*` ref, idle ≥2 days. Removal would be `git worktree remove`
only — no `--force`, no prune — and each will be RE-checked (clean + reachable +
live-process + scheduled-task cross-check) immediately before removal, exactly as
Batch 1's amended procedure.

| # | Path | HEAD | Reachable via |
|---|---|---|---|
| 1 | `C:/GAAUD_3BR2_CDX` | `7aad0377` | `origin/codex/gate-a-3b-shm-validation` |
| 2 | `C:/GAAUD_3BR2_CLA` | `7aad0377` | `origin/codex/gate-a-3b-shm-validation` |
| 3 | `C:/GAAUD_3BR2_DS` | `7aad0377` | `origin/codex/gate-a-3b-shm-validation` |
| 4 | `C:/GAAUD_3BR2_GLM` | `7aad0377` | `origin/codex/gate-a-3b-shm-validation` |
| 5 | `C:/GAAUD_4_GLM` | `5a9bb922` | `origin/codex/gate-a-credential-free-disarmed` |
| 6 | `C:/GAAUD_5A_CDX` | `5a9bb922` | `origin/codex/gate-a-credential-free-disarmed` |
| 7 | `C:/GAAUD_5A_CLA` | `5a9bb922` | `origin/codex/gate-a-credential-free-disarmed` |
| 8 | `C:/GAAUD_5A_CLD` | `5a9bb922` | `origin/codex/gate-a-credential-free-disarmed` |
| 9 | `C:/GAAUD_BUILD_CODEX` | `c5a4070a` | `origin/codex/gate-a-build-determinism` |
| 10 | `C:/GAAUD_BUILD_GLM` | `c5a4070a` | `origin/codex/gate-a-build-determinism` |

All ten are spent Gate-A audit-lane worktrees (multi-model review copies at frozen
SHAs); their commits are on `origin`. Safe removal candidates.

## Deliberately HELD OUT of Batch 2 (flag for a separate owner decision)

- `C:/AUD62A` `C:/AUD62B` `C:/AUD62C` `C:/AUD62D` — clean and reachable via
  `origin/integration/bridge-release-20260815`, but these were the integration
  candidate's audit worktrees for the release that JUST deployed. Recommend
  confirming with the deployment-owner session that they are finished before
  removal, even though they scan clean. Not in this batch.
- Any `C:/tmp/*` worktree — left for the C:\tmp artifact sweep, a separate item.

## After approval

On the owner's explicit "approve batch 2" (or a pared list), remove the approved
paths one-by-one under the full amended precheck (exit-code-asserted clean +
reachability, live process + scheduled-task cross-check, capture-then-test on
`--contains`), no force, no prune, stop on any mismatch; then report per-path
results and the new registered count. Remaining clean candidates roll into Batch 3.
