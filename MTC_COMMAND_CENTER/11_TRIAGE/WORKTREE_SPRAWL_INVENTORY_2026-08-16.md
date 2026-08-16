# Worktree Sprawl Inventory - 2026-08-16

Generated: 2026-08-16 22:44:38 (read-only inventory, no git state was modified, no files removed)

Source repo: `C:\LAB\Tradingview_LAB_CLEAN`

Method: `git worktree list --porcelain` enumerated 160 registered worktrees. For each: dirty-tree check (`git status --porcelain`), upstream/unpushed-commit check (`git rev-list --count @{u}..HEAD`), reachability from `origin/master` and from any pushed `origin/*` branch (`git merge-base --is-ancestor` / `git branch -r --contains`), and top-level last-write time. This is a PREPARE-ONLY inventory - nothing was deleted, pruned, checked out, reset, or stashed anywhere.

## Summary counts

| Class | Count |
|---|---|
| ACTIVE (do not touch) | 30 |
| SAFE-REMOVE (candidate, awaiting approval) | 73 |
| NEEDS-REVIEW (dirty / unpushed / no-upstream / unreachable) | 57 |
| STALE-REGISTRATION (dir missing on disk) | 0 |
| Total registered worktrees | 160 |

## ACTIVE - do not touch (30)

Known-active pinned set, plus anything with a top-level last-write within 2 days of 2026-08-16 22:44:38 (other AI sessions may be working in these trees with uncommitted work).

| Path | Branch / SHA | Dirty Lines | Unpushed | Reachable-from-master | Last Write | Reason |
|---|---|---|---|---|---|---|
| `C:/AUD62A` | detached:62bf661 | 0 | detached | no | 2026-08-16 11:52:41 | Known-active pinned set (do not touch) |
| `C:/AUD62B` | detached:be68953 | 0 | detached | no | 2026-08-16 14:00:34 | Known-active pinned set (do not touch) |
| `C:/AUD62C` | detached:a746078 | 0 | detached | no | 2026-08-16 15:09:27 | Known-active pinned set (do not touch) |
| `C:/AUD62D` | detached:acdf4e3 | 0 | detached | no | 2026-08-16 16:37:08 | Known-active pinned set (do not touch) |
| `C:/AUTHCON` | detached:678d4be | 1 | detached | no | 2026-08-15 20:33:16 | Last write within 2 days (2026-08-15 20:33:16) |
| `C:/BRDG` | detached:ddc8a9c | 1 | detached | no | 2026-08-15 20:07:27 | Last write within 2 days (2026-08-15 20:07:27) |
| `C:/BRIDGE_HELP_IMPL` | codex/bridge-help-wiki-impl | 0 | no-upstream | no | 2026-08-16 22:38:30 | Last write within 2 days (2026-08-16 22:38:30) |
| `C:/BRIDGE_RELEASE_INTEGRATION_20260815` | integration/bridge-release-20260815 | 0 | no-upstream | no | 2026-08-16 22:04:41 | Known-active pinned set (do not touch) |
| `C:/CLAIMCHK` | detached:93479b0 | 1 | detached | no | 2026-08-15 21:08:40 | Last write within 2 days (2026-08-15 21:08:40) |
| `C:/FRZMAP` | detached:ddc8a9c | 1 | detached | no | 2026-08-15 20:07:35 | Last write within 2 days (2026-08-15 20:07:35) |
| `C:/GEMINI` | codex/gemini-coder | 0 | no-upstream | no | 2026-08-16 21:31:12 | Known-active pinned set (do not touch) |
| `C:/LAB/Tradingview_LAB_CLEAN` | codex/bridge-help-wiki | 139 | no-upstream | no | 2026-08-16 22:39:22 | Known-active pinned set (do not touch) |
| `C:/MRGRUN` | detached:93479b0 | 1 | detached | no | 2026-08-15 21:08:34 | Last write within 2 days (2026-08-15 21:08:34) |
| `C:/P10BASE` | detached:ddc8a9c | 0 | detached | no | 2026-08-15 20:06:25 | Last write within 2 days (2026-08-15 20:06:25) |
| `C:/P10FIX` | codex/bridge-suite-anomaly-repairs-20260815 | 0 | 0 | no | 2026-08-15 20:37:32 | Last write within 2 days (2026-08-15 20:37:32) |
| `C:/P11LED` | detached:ddc8a9c | 1 | detached | no | 2026-08-15 20:07:19 | Last write within 2 days (2026-08-15 20:07:19) |
| `C:/P9IMP` | codex/p9-15-producer-20260816 | 0 | 0 | no | 2026-08-16 02:30:06 | Known-active pinned set (do not touch) |
| `C:/PLANREC` | detached:4f367ce | 1 | detached | no | 2026-08-15 21:32:06 | Last write within 2 days (2026-08-15 21:32:06) |
| `C:/PSC` | codex/pathscope-accounting-redesign-20260815 | 0 | 0 | no | 2026-08-15 21:59:07 | Last write within 2 days (2026-08-15 21:59:07) |
| `C:/PSCAUD` | detached:ec98cbd | 1 | detached | no | 2026-08-16 01:12:20 | Last write within 2 days (2026-08-16 01:12:20) |
| `C:/PSRETRY` | detached:40091b2 | 1 | detached | no | 2026-08-15 19:06:13 | Last write within 2 days (2026-08-15 19:06:13) |
| `C:/R7AC` | detached:d4e90cb | 1 | detached | no | 2026-08-15 00:40:07 | Last write within 2 days (2026-08-15 00:40:07) |
| `C:/R7AX` | detached:d4e90cb | 1 | detached | no | 2026-08-15 00:52:00 | Last write within 2 days (2026-08-15 00:52:00) |
| `C:/R7FINAL` | codex/rp7-r1-r4-repair-20260815 | 0 | 0 | no | 2026-08-15 07:38:41 | Known-active pinned set (do not touch) |
| `C:/R7T0CDX` | detached:4d28deb | 1 | detached | no | 2026-08-15 10:39:33 | Known-active pinned set (do not touch) |
| `C:/R7T0CLA` | detached:4d28deb | 1 | detached | no | 2026-08-15 10:39:25 | Known-active pinned set (do not touch) |
| `C:/RELDES` | detached:678d4be | 1 | detached | no | 2026-08-15 20:34:58 | Last write within 2 days (2026-08-15 20:34:58) |
| `C:/RO` | detached:c84497c | 0 | detached | no | 2026-08-15 21:57:47 | Last write within 2 days (2026-08-15 21:57:47) |
| `C:/tmp/PHW` | chore/housekeeping-phase-watch | 2 | 0 | yes | 2026-08-16 22:37:34 | Known-active pinned set (do not touch) |
| `C:/WBS` | detached:4f367ce | 1 | detached | no | 2026-08-15 21:32:13 | Last write within 2 days (2026-08-15 21:32:13) |

## SAFE-REMOVE - candidates, older than 2 days, clean tree, fully pushed / reachable (73)

Clean working tree AND (branch fully pushed with 0 commits ahead of its upstream, OR detached HEAD reachable from origin/master or from a pushed origin/* branch).

| Path | Branch / SHA | Dirty Lines | Unpushed | Reachable-from-master | Last Write | Reason |
|---|---|---|---|---|---|---|
| `C:/AIROUTE` | codex/ai-account-provider-routing | 0 | 0 | no | 2026-08-02 10:56:32 | Clean, branch 'codex/ai-account-provider-routing' fully pushed to origin/codex/ai-account-provider-routing (0 ahead) |
| `C:/G5R` | feature/exit-aware-gauntlet | 0 | 0 | no | 2026-07-16 12:03:11 | Clean, branch 'feature/exit-aware-gauntlet' fully pushed to origin/feature/exit-aware-gauntlet (0 ahead) |
| `C:/GA3B` | codex/wal-bundle-linux-sidecars | 0 | 0 | no | 2026-08-02 22:23:16 | Clean, branch 'codex/wal-bundle-linux-sidecars' fully pushed to origin/codex/wal-bundle-linux-sidecars (0 ahead) |
| `C:/GA3BR2` | codex/gate-a-3b-shm-validation | 0 | 0 | no | 2026-08-02 21:50:34 | Clean, branch 'codex/gate-a-3b-shm-validation' fully pushed to origin/codex/gate-a-3b-shm-validation (0 ahead) |
| `C:/GA4RED` | detached:637307e | 0 | detached | yes | 2026-08-03 00:01:23 | Clean, detached HEAD reachable from origin/master |
| `C:/GAAUD_3B` | detached:df00634 | 0 | detached | no | 2026-08-02 10:03:43 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3B_CDX` | detached:df00634 | 0 | detached | no | 2026-08-02 18:01:20 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3B_CLA` | detached:df00634 | 0 | detached | no | 2026-08-02 17:59:18 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3BR2_CDX` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:51:11 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3BR2_CLA` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:38:29 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3BR2_DS` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:38:44 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_3BR2_GLM` | detached:7aad037 | 0 | detached | no | 2026-08-02 23:22:54 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_4_GLM` | detached:5a9bb92 | 0 | detached | no | 2026-08-03 00:01:22 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_5A_CDX` | detached:5a9bb92 | 0 | detached | no | 2026-08-02 16:45:02 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_5A_CLA` | detached:5a9bb92 | 0 | detached | no | 2026-08-02 16:45:09 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_5A_CLD` | detached:5a9bb92 | 0 | detached | no | 2026-08-02 16:18:40 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_BUILD_CODEX` | detached:c5a4070 | 0 | detached | no | 2026-08-02 12:52:56 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_BUILD_GLM` | detached:c5a4070 | 0 | detached | no | 2026-08-02 12:52:48 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_BUILD_R2_CDX` | detached:82e92c9 | 0 | detached | no | 2026-08-03 01:41:41 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_BUILD_R2_GLM` | detached:82e92c9 | 0 | detached | no | 2026-08-03 01:44:39 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_C5` | detached:c5a4070 | 0 | detached | no | 2026-08-02 16:08:23 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_C5_CDX` | detached:c5a4070 | 0 | detached | no | 2026-08-02 16:16:16 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_C5_CLA` | detached:c5a4070 | 0 | detached | no | 2026-08-02 16:44:55 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_CLAUDE` | detached:7be1c42 | 0 | detached | no | 2026-08-02 10:50:01 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_CODEX` | detached:7be1c42 | 0 | detached | no | 2026-08-02 11:07:04 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM` | detached:ed3d053 | 0 | detached | no | 2026-08-08 15:57:50 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM_CDX_R2` | detached:2ce41e3 | 0 | detached | no | 2026-08-08 18:39:39 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM_CLA` | detached:ed3d053 | 0 | detached | no | 2026-08-08 16:03:11 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM_CLA_R2` | detached:2ce41e3 | 0 | detached | no | 2026-08-08 18:53:35 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM_DS_R2` | detached:2ce41e3 | 0 | detached | no | 2026-08-08 19:03:27 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_DISARM_GLM_R2` | detached:2ce41e3 | 0 | detached | no | 2026-08-08 18:32:32 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_GA3BR2_CDX` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:38:14 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_GA3BR2_CLA` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:41:06 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_GA3BR2_DSV4` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:38:23 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_GA3BR2_GLM` | detached:7aad037 | 0 | detached | no | 2026-08-02 22:38:31 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAAUD_INT_GLM` | detached:ebada02 | 0 | detached | no | 2026-08-03 14:46:13 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GADISARM` | codex/gate-a-disarmed-start-mode | 0 | 0 | no | 2026-08-08 20:15:44 | Clean, branch 'codex/gate-a-disarmed-start-mode' fully pushed to origin/codex/gate-a-disarmed-start-mode (0 ahead) |
| `C:/GAE3C` | detached:b2c369f | 0 | detached | no | 2026-08-09 03:05:18 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAE3D` | detached:b2c369f | 0 | detached | no | 2026-08-09 03:05:29 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAE3G` | detached:b2c369f | 0 | detached | no | 2026-08-09 03:05:35 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAE3X` | detached:b2c369f | 0 | detached | no | 2026-08-09 03:05:24 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAE3X2` | detached:b2c369f | 0 | detached | no | 2026-08-09 03:18:59 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAC` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:01:32 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAD` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:01:43 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAG` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:01:49 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAX` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:01:37 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAX2` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:16:34 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAEAX3` | detached:61d88f1 | 0 | detached | no | 2026-08-09 02:24:48 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/GAREPORT` | codex/gate-a-overnight-report | 0 | 0 | no | 2026-08-03 03:36:47 | Clean, branch 'codex/gate-a-overnight-report' fully pushed to origin/codex/gate-a-overnight-report (0 ahead) |
| `C:/GARESIDUAL` | codex/gate-a-residual-evidence-tests | 0 | 0 | no | 2026-08-03 03:46:47 | Clean, branch 'codex/gate-a-residual-evidence-tests' fully pushed to origin/codex/gate-a-residual-evidence-tests (0 ahead) |
| `C:/GATEA4` | codex/gate-a-credential-free-disarmed | 0 | 0 | no | 2026-08-02 14:01:25 | Clean, branch 'codex/gate-a-credential-free-disarmed' fully pushed to origin/codex/gate-a-credential-free-disarmed (0 ahead) |
| `C:/GATEAFIX` | codex/gate-a-build-determinism | 0 | 0 | no | 2026-08-02 11:44:01 | Clean, branch 'codex/gate-a-build-determinism' fully pushed to origin/codex/gate-a-build-determinism (0 ahead) |
| `C:/GATEAINTEGRATION` | codex/gate-a-integration | 0 | 0 | no | 2026-08-03 04:53:45 | Clean, branch 'codex/gate-a-integration' fully pushed to origin/codex/gate-a-integration (0 ahead) |
| `C:/K2VPS` | codex/kvm2-vps-bridge-readiness | 0 | 0 | yes | 2026-07-26 21:23:58 | Clean, branch 'codex/kvm2-vps-bridge-readiness' fully pushed to origin/codex/kvm2-vps-bridge-readiness (0 ahead) |
| `C:/KVM2F61_PROBE` | detached:f61ed91 | 0 | detached | yes | 2026-07-26 22:57:12 | Clean, detached HEAD reachable from origin/master |
| `C:/LAB/MTC_MODULAR` | codex/modular-monorepo | 0 | 0 | no | 2026-07-25 10:19:36 | Clean, branch 'codex/modular-monorepo' fully pushed to origin/codex/modular-monorepo (0 ahead) |
| `C:/LAB/TIERPOL` | feature/two-tier-policy | 0 | 0 | no | 2026-07-23 13:00:34 | Clean, branch 'feature/two-tier-policy' fully pushed to origin/feature/two-tier-policy (0 ahead) |
| `C:/MORNAUD_5A` | detached:5a9bb92 | 0 | detached | no | 2026-08-02 23:42:15 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/MORNAUD_C5` | detached:c5a4070 | 0 | detached | no | 2026-08-02 23:33:26 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/P1IF` | feature/interim-daily-loss-wiring | 0 | 0 | yes | 2026-07-18 16:22:33 | Clean, branch 'feature/interim-daily-loss-wiring' fully pushed to origin/feature/interim-daily-loss-wiring (0 ahead) |
| `C:/P2RT` | detached:008e065 | 0 | detached | yes | 2026-07-13 18:03:34 | Clean, detached HEAD reachable from origin/master |
| `C:/TSP0` | feature/ts-p0-baseline | 0 | 0 | yes | 2026-07-19 23:55:07 | Clean, branch 'feature/ts-p0-baseline' fully pushed to origin/feature/ts-p0-baseline (0 ahead) |
| `C:/WP2AC` | detached:779bd03 | 0 | detached | no | 2026-08-09 09:12:48 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2AD` | detached:779bd03 | 0 | detached | no | 2026-08-09 09:13:02 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2AG` | detached:779bd03 | 0 | detached | no | 2026-08-09 09:12:55 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2AUD` | detached:779bd03 | 0 | detached | no | 2026-08-09 09:11:32 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2CAND` | detached:2ce41e3 | 0 | detached | no | 2026-08-09 09:14:22 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2CL` | detached:313bc18 | 0 | detached | no | 2026-08-09 10:21:43 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2PKG2` | detached:2bd4ae8 | 0 | detached | no | 2026-08-09 11:00:35 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WP2PKG3` | detached:3fa3355 | 0 | detached | no | 2026-08-09 11:11:41 | Clean, detached HEAD reachable from a pushed origin/* branch (not master) |
| `C:/WPL` | codex/50h-wpl-verification | 0 | 0 | no | 2026-08-01 23:04:19 | Clean, branch 'codex/50h-wpl-verification' fully pushed to origin/codex/50h-wpl-verification (0 ahead) |
| `C:/WPS` | feature/ts-p1-009b-s2-closure | 0 | 0 | yes | 2026-08-01 20:02:58 | Clean, branch 'feature/ts-p1-009b-s2-closure' fully pushed to origin/feature/ts-p1-009b-s2-closure (0 ahead) |
| `C:/WPSAUD5` | detached:732b37c | 0 | detached | yes | 2026-08-01 10:09:27 | Clean, detached HEAD reachable from origin/master |

## NEEDS-REVIEW - dirty tree, unpushed commits, no upstream, or unreachable detached HEAD (57)

| Path | Branch / SHA | Dirty Lines | Unpushed | Reachable-from-master | Last Write | Reason |
|---|---|---|---|---|---|---|
| `C:/BTL2` | feature/ibkr-bridge-final | 0 | no-upstream | yes | 2026-07-16 13:17:44 | Branch 'feature/ibkr-bridge-final' has no upstream tracking branch |
| `C:/CDXFAILOVER` | codex/codex-account-failover | 1 | no-upstream | no | 2026-07-31 18:21:53 | Dirty tree: 1 changed line(s) in git status --porcelain |
| `C:/GA5E` | codex/gatea-a5-readiness-e | 0 | no-upstream | no | 2026-08-09 00:16:03 | Branch 'codex/gatea-a5-readiness-e' has no upstream tracking branch |
| `C:/GA5F` | codex/gatea-a5-fail-checkpoint | 0 | no-upstream | no | 2026-08-09 00:10:15 | Branch 'codex/gatea-a5-fail-checkpoint' has no upstream tracking branch |
| `C:/GADTR` | codex/gatea-d-transfer-checkpoint | 0 | no-upstream | no | 2026-08-09 00:02:10 | Branch 'codex/gatea-d-transfer-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A6_PASS_CLAUDE` | codex/gatea-a6-pass-checkpoint | 0 | no-upstream | no | 2026-08-09 03:56:54 | Branch 'codex/gatea-a6-pass-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A6_PREFLIGHT_GLM` | codex/gatea-a6-preflight-checkpoint | 0 | no-upstream | no | 2026-08-09 03:50:01 | Branch 'codex/gatea-a6-preflight-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A7_PASS_CLAUDE` | codex/gatea-a7-pass-checkpoint | 0 | no-upstream | no | 2026-08-09 04:07:42 | Branch 'codex/gatea-a7-pass-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A7_PREFLIGHT_GLM` | codex/gatea-a7-preflight-checkpoint | 0 | no-upstream | no | 2026-08-09 04:01:53 | Branch 'codex/gatea-a7-preflight-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A8_PASS_CLAUDE` | codex/gatea-a8-pass-checkpoint | 0 | no-upstream | no | 2026-08-09 04:20:39 | Branch 'codex/gatea-a8-pass-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A8_PREFLIGHT_GLM` | codex/gatea-a8-preflight-checkpoint | 0 | no-upstream | no | 2026-08-09 04:12:37 | Branch 'codex/gatea-a8-preflight-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A9_PASS_CLAUDE` | codex/gatea-a9-pass-final-checkpoint | 0 | no-upstream | no | 2026-08-09 04:34:38 | Branch 'codex/gatea-a9-pass-final-checkpoint' has no upstream tracking branch |
| `C:/GATEA_A9_PREFLIGHT_GLM` | codex/gatea-a9-preflight-checkpoint | 0 | no-upstream | no | 2026-08-09 04:26:04 | Branch 'codex/gatea-a9-preflight-checkpoint' has no upstream tracking branch |
| `C:/GATEA_HOUR_LEDGER_DS` | codex/gatea-hour-ledger-checkpoint | 0 | no-upstream | no | 2026-08-09 05:20:00 | Branch 'codex/gatea-hour-ledger-checkpoint' has no upstream tracking branch |
| `C:/GATEA_POST_GATE_INVENTORY_GLM` | codex/gatea-post-gate-inventory-checkpoint | 0 | no-upstream | no | 2026-08-09 04:44:10 | Branch 'codex/gatea-post-gate-inventory-checkpoint' has no upstream tracking branch |
| `C:/GATEA_POST_GATE_ROADMAP_CLAUDE` | codex/gatea-post-gate-roadmap-checkpoint | 0 | no-upstream | no | 2026-08-09 05:01:50 | Branch 'codex/gatea-post-gate-roadmap-checkpoint' has no upstream tracking branch |
| `C:/KVM2GLM` | codex/kvm2-cycle4-glm | 10 | no-upstream | yes | 2026-07-26 13:37:25 | Dirty tree: 10 changed line(s) in git status --porcelain |
| `C:/KVM2P03` | codex/kvm2-p0-p3-readiness | 52 | no-upstream | yes | 2026-07-26 22:56:34 | Dirty tree: 52 changed line(s) in git status --porcelain |
| `C:/LAB/MTC_AIONUI_PILOT` | pilot/aionui-evaluation-2026-08-01 | 1 | no-upstream | no | 2026-08-02 21:36:02 | Dirty tree: 1 changed line(s) in git status --porcelain |
| `C:/LAB/MTC_HANDOFF_UI` | codex/handoff-dashboard-prototype | 0 | no-upstream | no | 2026-07-25 14:26:33 | Branch 'codex/handoff-dashboard-prototype' has no upstream tracking branch |
| `C:/LAB/worktrees/gatea-a5a9-prereg-d` | codex/gatea-a5a9-prereg-d | 0 | no-upstream | no | 2026-08-08 22:52:59 | Branch 'codex/gatea-a5a9-prereg-d' has no upstream tracking branch |
| `C:/PG2A` | detached:2fa120b | 0 | detached | no | 2026-08-09 07:45:23 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PG2C` | detached:2fa120b | 0 | detached | no | 2026-08-09 07:45:16 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PG2D` | detached:2fa120b | 0 | detached | no | 2026-08-09 07:45:38 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PG2G` | detached:2fa120b | 0 | detached | no | 2026-08-09 07:45:30 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGAA` | detached:f8a6bc0 | 0 | detached | no | 2026-08-09 06:48:25 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGAC` | detached:f8a6bc0 | 0 | detached | no | 2026-08-09 06:48:18 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGAD` | detached:f8a6bc0 | 0 | detached | no | 2026-08-09 06:48:50 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGAG` | detached:f8a6bc0 | 0 | detached | no | 2026-08-09 06:48:41 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGR` | detached:2fa120b | 0 | detached | no | 2026-08-09 06:31:15 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/PGRK` | detached:4599b46 | 1 | detached | no | 2026-08-09 08:02:04 | Dirty tree: 1 changed line(s) in git status --porcelain |
| `C:/tmp/gatea_postgate_prereg_glm` | detached:7c4cac2 | 0 | detached | no | 2026-08-09 05:38:54 | Clean but detached HEAD NOT reachable from origin/master or any pushed origin/* branch (possible orphaned/unpushed work) |
| `C:/tmp/glm-gatea-a3-postcheck-wt` | codex/gatea-a3-postcheck | 0 | no-upstream | no | 2026-08-08 22:10:45 | Branch 'codex/gatea-a3-postcheck' has no upstream tracking branch |
| `C:/tmp/glm-gatea-a4-pass-wt` | codex/gatea-a4-pass | 0 | no-upstream | no | 2026-08-08 22:26:52 | Branch 'codex/gatea-a4-pass' has no upstream tracking branch |
| `C:/tmp/glm-gatea-checkpoint-a3-wt` | codex/gatea-a3-checkpoint | 0 | no-upstream | no | 2026-08-08 21:35:55 | Branch 'codex/gatea-a3-checkpoint' has no upstream tracking branch |
| `C:/tmp/glm-gatea-runkit-c-wt` | codex/gatea-runkit-c | 0 | no-upstream | no | 2026-08-08 21:43:15 | Branch 'codex/gatea-runkit-c' has no upstream tracking branch |
| `C:/tmp/postgate_runkit_design_claude` | detached:851d2aa | 5 | detached | no | 2026-08-09 05:58:04 | Dirty tree: 5 changed line(s) in git status --porcelain |
| `C:/TSP1001` | feature/ts-p1-001-order-state | 0 | no-upstream | yes | 2026-07-25 21:20:54 | Branch 'feature/ts-p1-001-order-state' has no upstream tracking branch |
| `C:/TSP1002` | feature/ts-p1-002-durable-identity | 12 | no-upstream | yes | 2026-07-25 22:50:33 | Dirty tree: 12 changed line(s) in git status --porcelain |
| `C:/TSP1002A2` | feature/ts-p1-002-durable-identity-a2 | 5 | no-upstream | yes | 2026-07-25 23:16:56 | Dirty tree: 5 changed line(s) in git status --porcelain |
| `C:/TSP1002A3` | feature/ts-p1-002-durable-identity-a3 | 5 | no-upstream | yes | 2026-07-25 23:38:04 | Dirty tree: 5 changed line(s) in git status --porcelain |
| `C:/TSP1002A4` | feature/ts-p1-002-durable-identity-a4 | 5 | no-upstream | yes | 2026-07-25 23:55:11 | Dirty tree: 5 changed line(s) in git status --porcelain |
| `C:/TSP1002A5` | feature/ts-p1-002-durable-identity-a5 | 0 | no-upstream | yes | 2026-07-26 00:13:17 | Branch 'feature/ts-p1-002-durable-identity-a5' has no upstream tracking branch |
| `C:/TSP1002A6` | feature/ts-p1-002-durable-identity-a6 | 0 | no-upstream | yes | 2026-07-26 00:48:07 | Branch 'feature/ts-p1-002-durable-identity-a6' has no upstream tracking branch |
| `C:/TSP1003A1` | feature/ts-p1-003-unknown-submission-a1 | 8 | no-upstream | yes | 2026-07-26 01:23:29 | Dirty tree: 8 changed line(s) in git status --porcelain |
| `C:/TSP1003A2` | feature/ts-p1-003-unknown-submission-a2 | 3 | no-upstream | yes | 2026-07-26 01:42:18 | Dirty tree: 3 changed line(s) in git status --porcelain |
| `C:/TSP1003A3` | feature/ts-p1-003-unknown-submission-a3 | 10 | no-upstream | yes | 2026-07-26 02:08:01 | Dirty tree: 10 changed line(s) in git status --porcelain |
| `C:/TSP1003A4` | feature/ts-p1-003-unknown-submission-a4 | 9 | no-upstream | yes | 2026-07-26 02:29:42 | Dirty tree: 9 changed line(s) in git status --porcelain |
| `C:/TSP1003A5` | feature/ts-p1-003-unknown-submission-a5 | 11 | no-upstream | yes | 2026-07-26 03:10:17 | Dirty tree: 11 changed line(s) in git status --porcelain |
| `C:/TSP1003A6` | feature/ts-p1-003-unknown-submission-a6 | 0 | no-upstream | yes | 2026-07-26 09:31:50 | Branch 'feature/ts-p1-003-unknown-submission-a6' has no upstream tracking branch |
| `C:/TSP1004` | feature/ts-p1-004-partial-fill-protection | 15 | no-upstream | yes | 2026-07-26 11:16:38 | Dirty tree: 15 changed line(s) in git status --porcelain |
| `C:/TSP1004A2` | feature/ts-p1-004-partial-fill-protection-a2 | 17 | no-upstream | yes | 2026-07-26 12:26:43 | Dirty tree: 17 changed line(s) in git status --porcelain |
| `C:/TSP1004A3` | feature/ts-p1-004-partial-fill-protection-a3 | 0 | no-upstream | yes | 2026-07-26 13:00:36 | Branch 'feature/ts-p1-004-partial-fill-protection-a3' has no upstream tracking branch |
| `C:/TSP1004A4` | feature/ts-p1-004-partial-fill-protection-a4 | 11 | no-upstream | yes | 2026-07-26 14:12:24 | Dirty tree: 11 changed line(s) in git status --porcelain |
| `C:/TSP1004A5` | feature/ts-p1-004-partial-fill-protection-a5 | 0 | no-upstream | yes | 2026-07-26 14:35:08 | Branch 'feature/ts-p1-004-partial-fill-protection-a5' has no upstream tracking branch |
| `C:/TSP1009` | feature/ts-p1-009-kill-evidence-recovery | 0 | no-upstream | yes | 2026-07-28 08:23:19 | Branch 'feature/ts-p1-009-kill-evidence-recovery' has no upstream tracking branch |
| `C:/TSP1009B` | feature/ts-p1-009b-evidence-epoch | 0 | no-upstream | yes | 2026-07-29 15:31:04 | Branch 'feature/ts-p1-009b-evidence-epoch' has no upstream tracking branch |

## STALE-REGISTRATION - registered but directory missing (0)

None found. All 160 entries returned by `git worktree list --porcelain` correspond to directories that currently exist on disk (no "prunable" markers in the porcelain output either).

## Proposed cleanup commands - SAFE-REMOVE only

NOT EXECUTED - AWAITING OWNER/LEAD APPROVAL. These are read-only-generated suggestions. Nothing below has been run. Review the SAFE-REMOVE table above before approving; each of the 73 worktrees below was clean (0 dirty lines) and either fully pushed to its upstream or a detached HEAD already reachable from origin/master or a pushed origin/* branch at the time of this inventory.

```
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/AIROUTE"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/G5R"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GA3B"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GA3BR2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GA4RED"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3B"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3B_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3B_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3BR2_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3BR2_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3BR2_DS"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_3BR2_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_4_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_5A_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_5A_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_5A_CLD"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_BUILD_CODEX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_BUILD_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_BUILD_R2_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_BUILD_R2_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_C5"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_C5_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_C5_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_CLAUDE"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_CODEX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM_CDX_R2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM_CLA_R2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM_DS_R2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_DISARM_GLM_R2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_GA3BR2_CDX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_GA3BR2_CLA"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_GA3BR2_DSV4"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_GA3BR2_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAAUD_INT_GLM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GADISARM"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAE3C"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAE3D"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAE3G"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAE3X"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAE3X2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAC"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAD"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAG"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAX2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAEAX3"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GAREPORT"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GARESIDUAL"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GATEA4"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GATEAFIX"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/GATEAINTEGRATION"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/K2VPS"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/KVM2F61_PROBE"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/LAB/MTC_MODULAR"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/LAB/TIERPOL"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/MORNAUD_5A"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/MORNAUD_C5"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/P1IF"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/P2RT"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/TSP0"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2AC"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2AD"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2AG"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2AUD"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2CAND"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2CL"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2PKG2"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WP2PKG3"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WPL"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WPS"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree remove "C:/WPSAUD5"
git -C C:\LAB\Tradingview_LAB_CLEAN worktree prune
```

Notes:
- If any `worktree remove` fails because git detects untracked-but-present files it didn't expect, re-check that path by hand before forcing anything - do not add --force blindly.
- Run `git worktree prune` only after the remove commands above have actually been executed and approved, not standalone.

## NEEDS-REVIEW next actions

- Dirty trees (18) - inspect uncommitted changes, decide commit vs. discard vs. leave as-is (owner call, do NOT auto-discard):
  - `C:/CDXFAILOVER` (1 changed lines, branch `codex/codex-account-failover`)
  - `C:/KVM2GLM` (10 changed lines, branch `codex/kvm2-cycle4-glm`)
  - `C:/KVM2P03` (52 changed lines, branch `codex/kvm2-p0-p3-readiness`)
  - `C:/LAB/MTC_AIONUI_PILOT` (1 changed lines, branch `pilot/aionui-evaluation-2026-08-01`)
  - `C:/PGRK` (1 changed lines, branch `detached:4599b46`)
  - `C:/tmp/postgate_runkit_design_claude` (5 changed lines, branch `detached:851d2aa`)
  - `C:/TSP1002` (12 changed lines, branch `feature/ts-p1-002-durable-identity`)
  - `C:/TSP1002A2` (5 changed lines, branch `feature/ts-p1-002-durable-identity-a2`)
  - `C:/TSP1002A3` (5 changed lines, branch `feature/ts-p1-002-durable-identity-a3`)
  - `C:/TSP1002A4` (5 changed lines, branch `feature/ts-p1-002-durable-identity-a4`)
  - `C:/TSP1003A1` (8 changed lines, branch `feature/ts-p1-003-unknown-submission-a1`)
  - `C:/TSP1003A2` (3 changed lines, branch `feature/ts-p1-003-unknown-submission-a2`)
  - `C:/TSP1003A3` (10 changed lines, branch `feature/ts-p1-003-unknown-submission-a3`)
  - `C:/TSP1003A4` (9 changed lines, branch `feature/ts-p1-003-unknown-submission-a4`)
  - `C:/TSP1003A5` (11 changed lines, branch `feature/ts-p1-003-unknown-submission-a5`)
  - `C:/TSP1004` (15 changed lines, branch `feature/ts-p1-004-partial-fill-protection`)
  - `C:/TSP1004A2` (17 changed lines, branch `feature/ts-p1-004-partial-fill-protection-a2`)
  - `C:/TSP1004A4` (11 changed lines, branch `feature/ts-p1-004-partial-fill-protection-a4`)

- Branches with no upstream (29) - decide push-to-origin vs. abandon per branch (checkpoint/audit-lane branches from the 2026-08-08/09 Gate-A run and 2026-08-16 bridge-help-wiki work; likely safe to abandon once the parent work is confirmed landed, but verify before deleting):
  - `C:/BTL2` - branch `feature/ibkr-bridge-final`
  - `C:/GA5E` - branch `codex/gatea-a5-readiness-e`
  - `C:/GA5F` - branch `codex/gatea-a5-fail-checkpoint`
  - `C:/GADTR` - branch `codex/gatea-d-transfer-checkpoint`
  - `C:/GATEA_A6_PASS_CLAUDE` - branch `codex/gatea-a6-pass-checkpoint`
  - `C:/GATEA_A6_PREFLIGHT_GLM` - branch `codex/gatea-a6-preflight-checkpoint`
  - `C:/GATEA_A7_PASS_CLAUDE` - branch `codex/gatea-a7-pass-checkpoint`
  - `C:/GATEA_A7_PREFLIGHT_GLM` - branch `codex/gatea-a7-preflight-checkpoint`
  - `C:/GATEA_A8_PASS_CLAUDE` - branch `codex/gatea-a8-pass-checkpoint`
  - `C:/GATEA_A8_PREFLIGHT_GLM` - branch `codex/gatea-a8-preflight-checkpoint`
  - `C:/GATEA_A9_PASS_CLAUDE` - branch `codex/gatea-a9-pass-final-checkpoint`
  - `C:/GATEA_A9_PREFLIGHT_GLM` - branch `codex/gatea-a9-preflight-checkpoint`
  - `C:/GATEA_HOUR_LEDGER_DS` - branch `codex/gatea-hour-ledger-checkpoint`
  - `C:/GATEA_POST_GATE_INVENTORY_GLM` - branch `codex/gatea-post-gate-inventory-checkpoint`
  - `C:/GATEA_POST_GATE_ROADMAP_CLAUDE` - branch `codex/gatea-post-gate-roadmap-checkpoint`
  - `C:/LAB/MTC_HANDOFF_UI` - branch `codex/handoff-dashboard-prototype`
  - `C:/LAB/worktrees/gatea-a5a9-prereg-d` - branch `codex/gatea-a5a9-prereg-d`
  - `C:/tmp/glm-gatea-a3-postcheck-wt` - branch `codex/gatea-a3-postcheck`
  - `C:/tmp/glm-gatea-a4-pass-wt` - branch `codex/gatea-a4-pass`
  - `C:/tmp/glm-gatea-checkpoint-a3-wt` - branch `codex/gatea-a3-checkpoint`
  - `C:/tmp/glm-gatea-runkit-c-wt` - branch `codex/gatea-runkit-c`
  - `C:/TSP1001` - branch `feature/ts-p1-001-order-state`
  - `C:/TSP1002A5` - branch `feature/ts-p1-002-durable-identity-a5`
  - `C:/TSP1002A6` - branch `feature/ts-p1-002-durable-identity-a6`
  - `C:/TSP1003A6` - branch `feature/ts-p1-003-unknown-submission-a6`
  - `C:/TSP1004A3` - branch `feature/ts-p1-004-partial-fill-protection-a3`
  - `C:/TSP1004A5` - branch `feature/ts-p1-004-partial-fill-protection-a5`
  - `C:/TSP1009` - branch `feature/ts-p1-009-kill-evidence-recovery`
  - `C:/TSP1009B` - branch `feature/ts-p1-009b-evidence-epoch`

- Unpushed commits ahead of upstream (0) - push or explicitly abandon:

- Detached HEAD unreachable from origin/master or any pushed origin/* branch (10) - these commits exist ONLY in these local worktrees; if the work is wanted, push a branch pointing at the SHA before any removal is considered:
  - `C:/PG2A` - SHA `2fa120b`
  - `C:/PG2C` - SHA `2fa120b`
  - `C:/PG2D` - SHA `2fa120b`
  - `C:/PG2G` - SHA `2fa120b`
  - `C:/PGAA` - SHA `f8a6bc0`
  - `C:/PGAC` - SHA `f8a6bc0`
  - `C:/PGAD` - SHA `f8a6bc0`
  - `C:/PGAG` - SHA `f8a6bc0`
  - `C:/PGR` - SHA `2fa120b`
  - `C:/tmp/gatea_postgate_prereg_glm` - SHA `7c4cac2`

## Local branches merged into origin/master (candidates for later branch cleanup - no deletion commands here)

`git branch --merged origin/master` (excluding master itself) returned 45 local branches. These are NOT worktree paths - some may still be checked out in one of the worktrees listed above (check the Branch column before deleting any of them). No branch-deletion commands are included per instructions; this is a flag list only for a later, separate cleanup pass.

- `chore/housekeeping-phase-watch`
- `codex/kvm2-cycle4-closeout-clean`
- `codex/kvm2-cycle4-glm`
- `codex/kvm2-p0-p3-readiness`
- `codex/kvm2-vps-bridge-readiness`
- `feature/chatgpt-mentor-bundle-plan`
- `feature/faz3b-stage1-sweep`
- `feature/faz3b-stage2-prereg`
- `feature/ibkr-bridge-audit-codex-gpt5`
- `feature/ibkr-bridge-audit-cursor-composer`
- `feature/ibkr-bridge-audit-deepseek-v4-pro`
- `feature/ibkr-bridge-audit-gemini`
- `feature/ibkr-bridge-audit-github-copilot`
- `feature/ibkr-bridge-audit-kimi`
- `feature/ibkr-bridge-final`
- `feature/ibkr-paper-bridge`
- `feature/interim-daily-loss-wiring`
- `feature/mcc-audit-cleanup`
- `feature/mcc-audit-fixes`
- `feature/mcc-ui-impeccable-fixes`
- `feature/quantlens-keltner-golden`
- `feature/strategy-param-specs`
- `feature/ts-p0-baseline`
- `feature/ts-p1-001-order-state`
- `feature/ts-p1-002-durable-identity`
- `feature/ts-p1-002-durable-identity-a2`
- `feature/ts-p1-002-durable-identity-a3`
- `feature/ts-p1-002-durable-identity-a4`
- `feature/ts-p1-002-durable-identity-a5`
- `feature/ts-p1-002-durable-identity-a6`
- `feature/ts-p1-003-unknown-submission-a1`
- `feature/ts-p1-003-unknown-submission-a2`
- `feature/ts-p1-003-unknown-submission-a3`
- `feature/ts-p1-003-unknown-submission-a4`
- `feature/ts-p1-003-unknown-submission-a5`
- `feature/ts-p1-003-unknown-submission-a6`
- `feature/ts-p1-004-partial-fill-protection`
- `feature/ts-p1-004-partial-fill-protection-a2`
- `feature/ts-p1-004-partial-fill-protection-a3`
- `feature/ts-p1-004-partial-fill-protection-a4`
- `feature/ts-p1-004-partial-fill-protection-a5`
- `feature/ts-p1-009b-evidence-epoch`
- `feature/ts-p1-009b-s2-closure`
- `feature/ts-p1-009-kill-evidence-recovery`
- `feature/validation-terminal`

---
End of inventory. No git state, working tree, or file was modified anywhere except this report file.
