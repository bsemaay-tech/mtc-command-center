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

---

## FULL CANDIDATE LIST — 83 clean/reachable/idle worktrees (owner requested, 2026-08-17)

Every row: clean tree, HEAD reachable from the named `origin/*` ref, idle ≥2 days,
not in the protected set. Removal (on approval) is `git worktree remove` only — no
`--force`, no prune — each RE-checked (clean + reachable + live-process +
scheduled-task cross-check) immediately before removal. `AUD62A-D` remain HELD OUT
pending deployment-owner confirmation and are not in this 83.

Note: the 10 former "rescue-first" dirs (PG2A/C/D/G, PGAA/AC/AD/AG, PGR,
tmp/gatea_postgate_prereg_glm) are now reachable via the pushed `rescue/local-only-*`
branches, so they are safe-removable too and appear below.

```
Path                          HEAD     Reachable via (origin/…)
GAAUD_3BR2_CDX                7aad0377 codex/gate-a-3b-shm-validation
GAAUD_3BR2_CLA                7aad0377 codex/gate-a-3b-shm-validation
GAAUD_3BR2_DS                 7aad0377 codex/gate-a-3b-shm-validation
GAAUD_3BR2_GLM                7aad0377 codex/gate-a-3b-shm-validation
GAAUD_4_GLM                   5a9bb922 codex/gate-a-credential-free-disarmed
GAAUD_5A_CDX                  5a9bb922 codex/gate-a-credential-free-disarmed
GAAUD_5A_CLA                  5a9bb922 codex/gate-a-credential-free-disarmed
GAAUD_5A_CLD                  5a9bb922 codex/gate-a-credential-free-disarmed
GAAUD_BUILD_CODEX             c5a4070a codex/gate-a-build-determinism
GAAUD_BUILD_GLM               c5a4070a codex/gate-a-build-determinism
GAAUD_BUILD_R2_CDX            82e92c98 codex/gate-a-build-determinism
GAAUD_BUILD_R2_GLM            82e92c98 codex/gate-a-build-determinism
GAAUD_C5                      c5a4070a codex/gate-a-build-determinism
GAAUD_C5_CDX                  c5a4070a codex/gate-a-build-determinism
GAAUD_C5_CLA                  c5a4070a codex/gate-a-build-determinism
GAAUD_CLAUDE                  7be1c429 codex/gate-a-build-determinism
GAAUD_CODEX                   7be1c429 codex/gate-a-build-determinism
GAAUD_DISARM                  ed3d0534 codex/gate-a-disarmed-start-mode
GAAUD_DISARM_CDX_R2           2ce41e34 codex/gate-a-disarmed-start-mode
GAAUD_DISARM_CLA              ed3d0534 codex/gate-a-disarmed-start-mode
GAAUD_DISARM_CLA_R2           2ce41e34 codex/gate-a-disarmed-start-mode
GAAUD_DISARM_DS_R2            2ce41e34 codex/gate-a-disarmed-start-mode
GAAUD_DISARM_GLM_R2           2ce41e34 codex/gate-a-disarmed-start-mode
GAAUD_GA3BR2_CDX             7aad0377 codex/gate-a-3b-shm-validation
GAAUD_GA3BR2_CLA             7aad0377 codex/gate-a-3b-shm-validation
GAAUD_GA3BR2_DSV4            7aad0377 codex/gate-a-3b-shm-validation
GAAUD_GA3BR2_GLM             7aad0377 codex/gate-a-3b-shm-validation
GAAUD_INT_GLM                 ebada020 codex/gate-a-disarmed-start-mode
GADISARM                      2ce41e34 codex/gate-a-disarmed-start-mode
GAE3C                         b2c369f7 codex/bridge-suite-anomaly-repairs-20260815
GAE3D                         b2c369f7 codex/bridge-suite-anomaly-repairs-20260815
GAE3G                         b2c369f7 codex/bridge-suite-anomaly-repairs-20260815
GAE3X                         b2c369f7 codex/bridge-suite-anomaly-repairs-20260815
GAE3X2                        b2c369f7 codex/bridge-suite-anomaly-repairs-20260815
GAEAC                         61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAEAD                         61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAEAG                         61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAEAX                         61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAEAX2                        61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAEAX3                        61d88f12 codex/bridge-suite-anomaly-repairs-20260815
GAREPORT                      b5a48e6f codex/gate-a-overnight-report
GARESIDUAL                    3121e7c7 codex/gate-a-residual-evidence-tests
GATEA4                        a0275b5c codex/gate-a-credential-free-disarmed
GATEAFIX                      0bdf8cf4 codex/gate-a-build-determinism
GATEAINTEGRATION              ebada020 codex/gate-a-disarmed-start-mode
K2VPS                         6fe0130f master
KVM2F61_PROBE                 f61ed919 master
LAB/MTC_HANDOFF_UI            d08a7078 codex/modular-monorepo
LAB/MTC_MODULAR               d08a7078 codex/modular-monorepo
LAB/TIERPOL                   ef185d13 codex/modular-monorepo
MORNAUD_5A                    5a9bb922 codex/gate-a-credential-free-disarmed
MORNAUD_C5                    c5a4070a codex/gate-a-build-determinism
P1IF                          acb83b5b master
PG2A                          2fa120b9 rescue/local-only-2fa120b9
PG2C                          2fa120b9 rescue/local-only-2fa120b9
PG2D                          2fa120b9 rescue/local-only-2fa120b9
PG2G                          2fa120b9 rescue/local-only-2fa120b9
PGAA                          f8a6bc0f rescue/local-only-f8a6bc0f
PGAC                          f8a6bc0f rescue/local-only-f8a6bc0f
PGAD                          f8a6bc0f rescue/local-only-f8a6bc0f
PGAG                          f8a6bc0f rescue/local-only-f8a6bc0f
PGR                           2fa120b9 rescue/local-only-2fa120b9
tmp/gatea_postgate_prereg_glm 7c4cac2b rescue/local-only-7c4cac2b
TSP0                          cfb08b81 master
TSP1001                       8edf81ca master
TSP1002A5                     eba350ce master
TSP1002A6                     fbd63474 master
TSP1003A6                     677c3a29 master
TSP1004A3                     65eaedb0 master
TSP1004A5                     7f72f71c master
TSP1009                       f5438c5b master
TSP1009B                      678e8b94 master
WP2AC                         779bd038 codex/bridge-suite-anomaly-repairs-20260815
WP2AD                         779bd038 codex/bridge-suite-anomaly-repairs-20260815
WP2AG                         779bd038 codex/bridge-suite-anomaly-repairs-20260815
WP2AUD                        779bd038 codex/bridge-suite-anomaly-repairs-20260815
WP2CAND                       2ce41e34 codex/gate-a-disarmed-start-mode
WP2CL                         313bc187 codex/bridge-suite-anomaly-repairs-20260815
WP2PKG2                       2bd4ae8d codex/bridge-suite-anomaly-repairs-20260815
WP2PKG3                       3fa33555 codex/bridge-suite-anomaly-repairs-20260815
WPL                           d9d38d9b codex/50h-wpl-verification
WPS                           16cbc717 master
WPSAUD5                       732b37c3 master
```

These 83 fall into three natural groups the owner can approve wholesale or in parts:
Gate-A audit lanes (GAAUD_*/GAE*/GAEA*/MORNAUD_*/WP2* — the bulk), the rescue-backed
PG*/tmp dirs, and old TS-P1/WP feature checkouts. Awaiting the owner's exact approved
subset; nothing removed.

---

## RECONCILIATION: 91 vs 83 (owner question, 2026-08-17 evening)

Both numbers were correct for what they counted; the slate text failed to say so.
**91 = every clean + remotely-reachable worktree** outside the protected seven.
**83 = the removable slate** after the additional "idle ≥ 2 days" guard. The 8
excluded by that guard, path by path (all clean and reachable, just touched within
2 days — re-eligible for a later batch once idle):

| Path | Idle (days) at sweep |
|---|---|
| `C:/AUD62A` | 1.3 |
| `C:/AUD62B` | 1.2 |
| `C:/AUD62C` | 1.2 |
| `C:/AUD62D` | 1.1 |
| `C:/P10BASE` | 1.9 |
| `C:/P10FIX` | 1.9 |
| `C:/PSC` | 1.9 |
| `C:/RO` | 1.9 |

ALL removals remain HELD — nothing is removed until the owner approves a named
subset of the 83-path list above.

---

## BATCH 2 EXECUTION RECORD — first ten, 2026-08-17 evening (owner-approved exact list)

Per-item fresh prechecks immediately before each removal: clean tree
(exit-asserted), remote reachability (capture-then-test), live process scan,
Windows SERVICE scan, scheduled-task scan. `git worktree remove` only — no
`--force`, no prune. Result: **10 of 10 REMOVED, zero mismatches.**

| Path | SHA | Reachable via |
|---|---|---|
| `C:/GAAUD_3BR2_CDX` | `7aad0377` | `origin/codex/gate-a-3b-shm-validation` |
| `C:/GAAUD_3BR2_CLA` | `7aad0377` | same |
| `C:/GAAUD_3BR2_DS` | `7aad0377` | same |
| `C:/GAAUD_3BR2_GLM` | `7aad0377` | same |
| `C:/GAAUD_4_GLM` | `5a9bb922` | `origin/codex/gate-a-credential-free-disarmed` |
| `C:/GAAUD_5A_CDX` | `5a9bb922` | same |
| `C:/GAAUD_5A_CLA` | `5a9bb922` | same |
| `C:/GAAUD_5A_CLD` | `5a9bb922` | same |
| `C:/GAAUD_BUILD_CODEX` | `c5a4070a` | `origin/codex/gate-a-build-determinism` |
| `C:/GAAUD_BUILD_GLM` | `c5a4070a` | same |

Registered worktrees after: **139**. All other candidates remain HELD.
