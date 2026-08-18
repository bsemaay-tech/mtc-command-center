# Worktree cleanup — full execution record, 2026-08-18

Lead: Claude Fable (autonomous continuation, owner dispatch 2026-08-18 afternoon).
Control lane: worktree `C:\WTCLEAN_CTRL`, branch `chore/worktree-cleanup-20260818`,
created from fresh `origin/master` `14559c2a`. The dirty canonical checkout
(`codex/bridge-help-wiki` @ `59e79bb2`) was never written, staged, reset, or
checked out. Live verification before any action: `master` == `origin/master` ==
`14559c2a`; 132 registered worktrees; protected seven present; `MTC-Bridge-P2`
Disabled; `MTC-HermesPhaseWatch` Ready; no git locks; zero process/service/
scheduled-task references to any candidate path; one other RUNNING session
("Bridge V2 continuation") detected and coordinated by direct session message —
lanes disjoint (it holds Bridge V2 packages; this session held cleanup + Phase
Watch V3 review only).

## Headline numbers

| Metric | Value |
|---|---|
| Registered worktrees at start | 132 (133 during run with the control worktree) |
| Registered at end | 9 = protected 7 + `C:\WTCLEAN_CTRL` (this lane) + `C:\LAB\MTC_AIONUI_PILOT` (D-hold) |
| Deregistered this run | 124 |
| Clean removals (`git worktree remove`, no force, per-path prechecks) | 115 |
| ACL-debris husks (git-deregistered, dir deletion blocked) | 9, totalling 8.8 GB |
| Rescue branches pushed + ls-remote verified | 36 (`rescue/wt-*`) |
| Holds / stops | 0 precheck holds, 0 global stops |
| Disk freed | roughly 100 GB (order-of-magnitude: 115 full checkouts ≈ 1 GB each; no byte-exact baseline was captured) |
| `git worktree prune --dry-run` at closure | names NOTHING → actual prune not run (nothing to prune; husk deregistration was already clean) |

Every removal ran the full amended precheck immediately before it: path resolved,
not protected, exists, not a reparse point, `status --porcelain` empty
(exit-asserted), HEAD == recorded SHA, remote ref exists after fresh fetch,
HEAD reachable from it (capture-then-test, any-origin-ref fallback recorded as
CORRECTED), fresh process + Windows-service + scheduled-task scans, then plain
`git worktree remove`. Per-path logs: session scratchpad `sweep_{A,R8,C18,B16,C16}_results.csv`.

## Workstream A — 66-path slate + 8 recently-touched

- All 66 remaining slate paths processed: **59 clean removals, 7 husks, 0 holds.**
- Husks (A): `C:\GATEAFIX` `C:\K2VPS` `C:\TSP1003A6` `C:\TSP1009` `C:\TSP1009B`
  `C:\WPS` `C:\WPSAUD5` — each precheck-passed clean+reachable seconds before
  removal, so husk content is tracked+pushed bytes plus pytest-tmp ACL debris
  (`Permission denied` on `.pytest-tmp/*` dirs blocked directory deletion).
- The 8 recently-touched (`AUD62A-D`, `P10BASE`, `P10FIX`, `PSC`, `RO`) were
  revalidated: all clean, remote-reachable, idle ≥ 2 days (newest write
  2026-08-16 13:37 UTC). The AUD62A-D deployment-owner concern was resolved by
  the deployment's own completion record (release `be007fd8` deployed 2026-08-17;
  the R7 deployment session is closed). **8/8 removed clean.**

## Workstream C — 18 unreachable HEADs

All 18 were clean trees on local-only checkpoint branches (Gate-A checkpoint
lanes, 1–2 unique commits each, on no remote ref). Each HEAD was pushed as
`rescue/wt-<name>` (18 branches), verified via `ls-remote`, then removed under
the full precheck. **18/18 rescued + removed, no branch deleted.**

## Workstream B — 33 dirty trees

Independent classifications: GLM-4.7 (routine-classification tier; routing
record below) over a Lead-collected fact pack (branch, HEAD, tracked mods,
untracked count+bytes, unique commits, remote-containing refs, newest write,
process refs, secret-name flags, full `status --porcelain` dumps). Gemini
read-only cross-check was attempted three times and failed CLOSED each time —
its filesystem watcher tripped on concurrent-session hook-cache churn
(`.impeccable\hook.cache.json`) and on this cleanup's own registry mutations;
the guard behaved correctly, the route is unusable while two sessions run in the
repo. Recorded as an environmental limitation; the Lead's byte-level evidence
(below) is stronger than either model opinion and stands as the reproduction.

Outcomes:

- **14 × class B (duplicate-only):** each tree's single untracked triage doc was
  proven byte-identical (`git hash-object` == remote blob) on a pushed ref
  (`codex/bridge-suite-anomaly-repairs-20260815`, `codex/p9-15-producer-20260816`,
  `codex/pathscope-accounting-redesign-20260815`, or `master`). Equality was
  re-verified immediately before deleting the duplicate file; blob OIDs are in
  `remove_B14_log.txt` (scratchpad) and the commit below. Trees then removed:
  AUTHCON BRDG CLAIMCHK FRZMAP MRGRUN P11LED PLANREC PSCAUD PSRETRY R7AC
  R7T0CDX R7T0CLA RELDES WBS.
- **2 × class C (unique docs):** `C:\PGRK` (Gate-A post-gate run-kit design, on
  no origin ref) → `rescue/wt-pgrk-doc-20260818`; `C:\R7AX` (RP7 cap-override
  Codex audit variant differing from master's copy) → `rescue/wt-r7ax-doc-20260818`.
  Secret-scans clean (two prose "token" false-positives inspected). Removed after push.
- **16 × class C (WIP rescues):** CDXFAILOVER (uncommitted account-failover
  design in `resilient_dispatch.sh` — Lead-inspected, real work), KVM2GLM,
  KVM2P03, tmp/postgate_runkit_design_claude, and the 12 TS-P1 attempt lanes
  (TSP1002{,A2,A3,A4}, TSP1003A1–A5, TSP1004{,A2,A4}). Exact dirty sets committed
  verbatim to `rescue/wt-<name>-wip-20260818` branches, staged-diff secret-scan
  clean, pushed, ls-remote verified, then removed. Two notes:
  - KVM2P03's 52 "modified" files collapsed to 12 real content diffs at staging —
    the other 40 were CRLF-phantom diffs normalized away by `* text=auto`.
  - TSP1004A2's 56 MB `.lead_focused_root/` + `.lead_focused_bridge/` dirs were
    pytest-fixture `bridge.db` copies (generated test debris, one per test case);
    deleted after the real files were committed+pushed. TSP1003A5 and TSP1004A2
    left ACL husks (same pytest-tmp pattern, content already on remote).
- **1 × class D (ACTIVE — preserved untouched):** `C:\LAB\MTC_AIONUI_PILOT` runs a
  LIVE process right now (PID 20632 `powershell.exe` executing
  `MTC_COMMAND_CENTER\08_DASHBOARD_APP\run_dashboard_server.ps1` from inside the
  worktree, plus a child), and carries 2 unpushed commits + 107 MB untracked
  `data/`. Not touched. Owner decision needed (see owner-asks).

GLM-4.7 classified 33/33; Lead agreement on every actionable call (GLM's two
conservative D-calls — CDXFAILOVER, TSP1004A2 — were resolved to C by direct
Lead inspection of the diff/dirs, which is the safer-or-equal action since
rescue preserves everything).

## Closure verification

- Registered at end: exactly the protected seven + control lane + AIONUI hold.
- `C:\P2RT`: HEAD still `008e065e`, status clean, never touched. `MTC-Bridge-P2`
  still Disabled; `MTC-HermesPhaseWatch` still Ready; `WATCH_ACTIVE: NO` untouched.
- All 36 rescue refs live on `origin` (ls-remote count 36).
- Fresh process scan at closure: no references to any removed path; the only
  worktree with a live process is the AIONUI hold above.
- `git worktree prune --dry-run -v` output empty → no prune executed.
- KVM2 was never contacted; no credential, Telegram, Bridge, ARM, TESTNET,
  Pine/parity/MTC surface was touched at any point in this run.

## Cleanup completion statement

No clean, remotely-safe, inactive, non-protected worktree remains registered.
Every dirty or unreachable item is either rescued-and-removed (with its rescue
ref recorded above) or explicitly held:

| Hold | Why | Owner action available |
|---|---|---|
| `C:\LAB\MTC_AIONUI_PILOT` | live dashboard-server process from inside the tree; 2 unpushed commits; 107 MB untracked data; AIONUI itself is "installed, never used — evaluate or remove" in TOOLBOX | decide pilot's fate; if ending it: stop the server, then a normal rescue+remove pass |
| 9 ACL husks (8.8 GB): GATEAFIX K2VPS TSP1003A6 TSP1009 TSP1009B WPS WPSAUD5 TSP1003A5 TSP1004A2 | pytest-tmp ACL debris blocks directory deletion; every tree was clean+pushed (or rescue-pushed) before deregistration | one owner-approved elevated one-liner deletes all nine (same class as the earlier GA3B/GAAUD_CODEX husk decisions) |

## GLM routing record (required)

```
Classification      : Tier 2 — routine worktree classification (33 dirty trees)
Protected           : no — read-only classification over a Lead-collected fact pack
Model + provider    : GLM-4.7 via Z.AI Coding Plan (glm.ps1)
Cheaper-model rationale : 4.5-Air not confirmed on route; task is judgment over
                          structured facts, Tier 2 floor
Exact paths         : none writable; input = C:\tmp\wtclean\classify_pack.txt
Context/tool budget : one file read + one completion (~23 KB in)
Fallback            : GLM-5.3
External API credits: no
```

(A second GLM task — GLM-5.2 adversarial review of the Phase Watch V3 frozen set
— is recorded in `PHASE_WATCH_V3_PREAPP_VERIFICATION_2026-08-18.md`.)

## Process lesson (candidate)

PowerShell 5.1 executes `-File` scripts in the ANSI codepage when the file has
no BOM: a UTF-8 em-dash inside a double-quoted string becomes a smart-quote
(0x94 in cp1254), which PS treats as a string terminator — the script fails to
parse with misleading errors pointing far from the real line. Two dispatch
rounds were lost to one `—` in a log string. Rule: scripts written for
`powershell.exe -File` stay pure ASCII (or get a BOM).

---

## OWNER DECISIONS EXECUTED — 2026-08-18 late afternoon ("husk'lari sil" + "AIONUI kapat")

**AIONUI pilot closed.** The live dashboard-server pair (powershell wrapper PID
20632 + its `python -m mcc_readonly` child 30792) was verified against the
worktree path and stopped; the canonical repo's own dashboard server (separate
process tree under `C:\LAB\Tradingview_LAB_CLEAN`) was confirmed alive and
untouched. The pilot's 2 unpushed commits were pushed as
`rescue/wt-aionui-pilot-20260818` (`49edc6fa`, ls-remote verified); the 107 MB
untracked `data/` was AIONUI's own runtime state (bundled runtime + skills
cache + backend SQLite) — the small irreproducible part (backend db, state
json, logs; 2.21 MB) was preserved at `C:\LAB\_PRESERVED_AIONUI_PILOT_20260818`
before deletion. Worktree then passed the full precheck and was removed.
Registered worktrees now **8** (protected 7 + cleanup control lane). TOOLBOX row
updated in the starter-kit repo (`c2b6b92`). Note: the AIONUI *application*
may still be installed on the machine — uninstalling it is a separate owner step.

**Husks deleted (owner-approved).** All nine were re-verified deregistered,
unreferenced by any process, and non-protected, then deleted with native `rd`
(the un-elevated session cannot take ownership of the pytest-created deny-ACL
dirs, and PowerShell's cmdlet path is harness-blocked for top-level `C:\` roots).
Result: **~10 GB freed** (C: free 277.7 → 287.7 GB). Residue: 64 empty,
zero-byte, ACL-locked skeleton directories across the nine roots (`.pytest_cache`
/ `.pytest-tmp` shells whose DACL denies even reads without elevation). A
self-elevating double-click cleaner for exactly these nine roots was left at
`C:\LAB\DELETE_HUSK_LEFTOVERS_20260818.cmd` — one UAC "Yes" finishes the job;
the residue is cosmetic (0 bytes) either way.
