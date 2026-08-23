# Repository Topology and AI-Context Inventory (Ticket #112)

**Scope:** Measure `C:\LAB\Tradingview_LAB_CLEAN` (repo `bsemaay-tech/mtc-command-center`) as it
IS — sizes, onboarding chain, AI_MEMORY structure, tags/branches, archives, the frozen legacy
repo relationship, stray dirs, dirty checkout state, and SESSION_LOCK usage history. Read-only:
git metadata commands (`ls-tree`, `log`, `branch`, `status`) against `origin/master` and the main
checkout, plus filesystem size checks. No content scans of large trees, no writes to the main
checkout, no reads inside the frozen legacy repo.

**Method:** all sizes are measured via `git ls-tree -r -l` against `origin/master` (blob sizes,
uncompressed) unless marked "on-disk" (filesystem, for untracked/external content). Dates are
`git log -1` last-touch commits for the given path on `origin/master` unless noted. Today's date
for staleness math: 2026-08-23.

---

## 1. Top-level directory map (origin/master, tracked bytes)

| Path | Tracked size | Notes |
|---|---|---|
| `MTC_COMMAND_CENTER/` | 1,023,024,023 B (~976 MiB) | dominates the repo; see §2 |
| `docs/` | 18,219,994 B (~17.4 MiB) | mostly migration-era artifacts, see §5 |
| `IBKR_PAPER_BRIDGE/` | 7,574,593 B (~7.2 MiB) | |
| `_deepseek_driver/` | 47,126 B | |
| `AGENTS.md` | 30,610 B | onboarding entrypoint, see §3 |
| `apply_migration.py`, `mtc_cli`, `verify_migration.ps1` | ~40 KB combined | migration tooling still at repo root |
| `.claude/`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.chatgpt-instructions.md`, `README.md`, `.gitattributes`, `.gitignore` | ~10 KB combined | multi-tool onboarding shims |

Total tracked repo content is dominated almost entirely by one subtree: `MTC_COMMAND_CENTER/`
is ~97% of tracked bytes.

## 2. `MTC_COMMAND_CENTER/` breakdown — where the size actually is

| Subdir | Tracked size | Files |
|---|---|---|
| `03_QUANTLENS/` | 868,782,376 B (~828 MiB) | dominant subtree, see below |
| `02_MTC_BACKTEST/` | 100,886,750 B (~96 MiB) | |
| `11_TRIAGE/` | 18,879,758 B (~18 MiB) tracked (**+ ~116 MiB untracked**, see §7) | |
| `12_PARITY_PINETS/` | 16,837,620 B (~16 MiB) | |
| `01_MTC_PROJECT/` | 6,933,414 B | |
| `00_INBOX/` | 3,818,521 B | |
| `_AI_MEMORY/` | 1,484,509 B | see §3–§4 |
| `08_DASHBOARD_APP/` | 702,663 B tracked (excludes untracked stray dirs, see §6) | |
| `10_ARCHIVE/` | 37 B (`.gitkeep` only — empty) | named archive slot exists but is unused |
| everything else (`05_REGISTRY`, `09_DOCS`, `04_SHARED`, adapters, schemas, prompts, tools, root docs) | ~570 KB combined | |

### 2a. `03_QUANTLENS/` (868 MiB) — the single largest rot concentration in the repo

| Subdir | Tracked size | Files | Last touched |
|---|---|---|---|
| `tools/night_runs/` | 347,917,298 B (~332 MiB) | 129 | 2026-06-06 (commit `b5ed1afa`) — **78 days stale** |
| `tools/overnight_runs/` | 94,383,927 B (~90 MiB) | 42 | 2026-05-31 (init commit `77a10e65`) — **84 days stale, never touched since migration day** |
| `research/data_acquisition_5m_2026_05_03/` | 255,742,487 B (~244 MiB) | 23 | 2026-05-31 (init commit) — **84 days stale** |
| `research/stage2_robustness_2026_05_03_CODEX_20260503_232808/` | 98,885,904 B (~94 MiB) | 263 | 2026-05-31 (init commit) |
| remaining `research/` dated batches (`overnight_intake_batch_*`, `restart_transcript_intake_audit_*` ×5 near-duplicate variants, `strategy_batch_*`, etc.) | ~30 MiB combined | ~1,000+ | all dated `2026_05_03`/`2026_05_04` in their directory names |

**Rot finding #1 (worst in the repo):** `tools/night_runs/` + `tools/overnight_runs/` +
`research/data_acquisition_5m_2026_05_03/` + `research/stage2_robustness_..._CODEX_.../` alone
total **~796 MiB of tracked git content**, all named after single dated batch runs from
2026-05-03/05-04/06-06, none touched since. This is one-off backtest/audit run output, not source
code, sitting permanently in git history and checked out on every clone.

**Rot finding #2 (gitignore drift):** `.gitignore` (root) explicitly lists
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_runs/` as an ignored path (under the QuantLens
evidence-only section: *"backtest results live on disk, not in git"*) — but the directory is
still **tracked**, at 90 MiB. The ignore rule was added after the directory was already committed;
`git rm -r --cached` was never run, so the rule has zero effect and the bytes stay in every clone
and every future pack. `tools/night_runs/` (332 MiB, the single largest tracked directory) is not
even mentioned in `.gitignore`.

### 2b. `02_MTC_BACKTEST/` (96 MiB) — mostly regenerable data

`data/` alone is 92,273,559 B (146 files) — likely OHLCV/candle caches sitting in git despite the
repo's stated doctrine (per AI_MEMORY) that native bundle data should be downloaded, not committed.
Source (`src/`, `scripts/`, `tests/`) is a small fraction (~1.3 MiB combined) of this subtree.

## 3. AI onboarding chain — files, sizes, and the mandated read order

Read order per `AGENTS.md` → `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`:

| Step | File | Size | Last touched |
|---|---|---|---|
| 1 | `AGENTS.md` (repo root) | 30,610 B (295 lines) | 2026-08-10 (`15e2d013`) — 13 days stale |
| 2 | `_AI_MEMORY/START_HERE.md` | 6,815 B (66 lines) | — |
| 3 | `_AI_MEMORY/LESSONS.md` | 7,587 B | — |
| 4 | `_AI_MEMORY/AI_RULES.md` | 11,351 B | — |
| 5 | `_AI_MEMORY/PROJECT_MEMORY.md` | 7,560 B | — |
| 6 | `_AI_MEMORY/GLOBAL_HANDOFF.md` ("if needed" — but START_HERE's own banner says read newest section **first**) | 249,291 B (~243 KiB) | 2026-08-17 (`5f848c35`) — 6 days stale |
| 7 | `_AI_MEMORY/NEXT_STEPS.md` | 341,744 B (~334 KiB) | 2026-08-17 (`5f848c35`, same commit) — 6 days stale |

**Mandatory-chain total: ~654 KB** (AGENTS.md + START_HERE.md + LESSONS.md + AI_RULES.md +
PROJECT_MEMORY.md + GLOBAL_HANDOFF.md + NEXT_STEPS.md), against a project instruction
("use token-efficient workflow") that assumes a lean chain. GLOBAL_HANDOFF.md and NEXT_STEPS.md
alone are 590 KB — 90% of the chain — and both are single monolithic append-only logs (211 and 201
historical commits respectively touching each file).

**Rot finding #3 (onboarding-chain bloat, growth is structural not incidental):** GLOBAL_HANDOFF.md
and NEXT_STEPS.md are edited via append (211 / 201 commits each), and the repo's own remediation
for this is periodic manual "rotation" into `_AI_MEMORY/archive/` (see §4) — which has already
happened at least once (2026-08-15, per the file's own rotation note) and the live files are
already back up to 243 KiB / 334 KiB six days after that rotation's referenced cutoff. The pattern
is self-repeating growth, not a one-time cleanup.

Both files were last touched together on 2026-08-17 by commit `5f848c35` ("preserve Help audit cap
boundary"), 6 days before this measurement (2026-08-23) — stale relative to a repo whose
`origin/master` HEAD (`ab35ca66`) is from today. Note: in the **main checkout** (not this
worktree) both files, plus `ACTIVE_FILES.md`, `DECISIONS.md`, and `SESSION_LOCK.md`, currently show
as locally modified/uncommitted (see §7) — i.e. there is pending onboarding-chain edit work sitting
uncommitted in the working tree at the time of this measurement.

## 4. `_AI_MEMORY/` structure and staleness

Top-level file count: 43 files + 3 subdirectories (`PARALLEL_AGENT_PROMPTS/`,
`PARALLEL_AGENT_REPORTS/`, `archive/`). Total tracked size 1,484,509 B (~1.4 MiB).

Notable files beyond the mandated chain (§3):
- `ACTIVE_FILES.md` — 65,759 B
- `AI_ACCOUNT_AND_MODEL_ROUTING.md` — 25,985 B
- `DECISIONS.md` — 28,999 B
- `SESSION_LOCK.md` — 20,774 B (see below)
- `MCC_COMPLETION_MASTER_PLAN.md` — 23,565 B
- `REPO_MAP.md` — 22,044 B (a second, `_AI_MEMORY`-local "map of the repo," distinct in scope from this ticket's deliverable and from `docs/INVENTORY_REPORT.md` in §5)
- 10 `RESULT_*_codex.md` files, 1.3–2.2 KB each — small one-off result notes, not obviously superseded but not indexed anywhere in the read order either

`PARALLEL_AGENT_PROMPTS/` — 7 files, 54,367 B. `PARALLEL_AGENT_REPORTS/` — 7 files, 26,095 B.
Both small; no rot concern.

### `_AI_MEMORY/archive/` — the rotation destination

| File | Size |
|---|---|
| `GLOBAL_HANDOFF_pre-2026-08-01.md` | 238,645 B |
| `NEXT_STEPS_pre-2026-08-01.md` | 129,822 B |
| `SESSION_LOG_pre-2026-07-06.md` | 113,220 B |
| `START_HERE_STALE_BANNER_2026-08-12.md` | 1,560 B |

Archive total: 483,247 B (~472 KiB). Combined with the live GLOBAL_HANDOFF/NEXT_STEPS lineage
(§3), the "current state" narrative for this repo is spread across ~1.07 MiB of prose split
between 2 live files and 3 archived files, with no index file listing what's in the archive or
when to consult it (START_HERE.md says "grep the archive before claiming an old entry does not
exist" — i.e. the burden is on every future agent to search blind).

### `SESSION_LOCK.md` — usage history

31 commits total. Oldest: `77a10e65` (2026-05-31, the init/migration commit — this file existed
from day one). File was **rebuilt** as a "workstream write-lock" on 2026-08-11
(`15d48088`/`67258da9`) after being something else before (init commit + prior history). Since
that rebuild it was actively edited through 2026-08-17 (`8c7d3b36`, "close overnight seven-workstream
cycle"). **No commits touching it since 2026-08-17** — 6 days with zero lock-file activity as of
this measurement, despite the file's stated purpose (an active per-session workstream lock) implying
frequent claim/release churn during any active session. It is also one of the 6 files currently
showing uncommitted local modifications in the main checkout (§7) — i.e. there may be an in-flight
edit not yet reflected in the committed history above.

## 5. `docs/` (top-level, 17.4 MiB tracked) — migration debris + name collisions with `_AI_MEMORY/`

All files below except `ACTIVE_FILES.md` were last touched by the single 2026-05-31 init/migration
commit (`77a10e65`) and have **never been touched again in 84 days**:

| File | Size | Last touched |
|---|---|---|
| `DEPENDENCY_AND_PATH_AUDIT.md` | 5,989,396 B (~5.7 MiB) | 2026-05-31 (migration) |
| `MIGRATION_MAP.md` | 142,404 B | 2026-05-31 (migration) |
| `INVENTORY_REPORT.md` | 135,976 B | 2026-05-31 (migration) |
| `DEPRECATED_FILES.md` | 55,447 B | 2026-05-31 (migration) |
| `EXCLUDED_PROJECTS.md` | 55,447 B | 2026-05-31 (migration) |
| `DECISION_REQUESTS.md` | 21,343 B | — |
| `AI_MEMORY_DRAFT.md` | 4,339 B | — |
| `MIGRATION_PLAN.md` | 3,095 B | — |
| `PHASE0_SUMMARY.md` | 2,648 B | — |
| `DECISIONS.md` | 2,136 B | 2026-05-31 (migration) |
| `ACTIVE_FILES.md` | 40,953 B | 2026-06-21 |
| `migration_manifests/`, `superpowers/` | (subdirs, not sized) | |

**Rot finding (duplicate blob):** `docs/DEPRECATED_FILES.md` and `docs/EXCLUDED_PROJECTS.md` have
the **identical git blob hash** (`3cbda4f712beb86d82923b9e261f00bbfab5b7ca`, both 55,447 B) — the
same file content committed twice under two different names at migration time, and neither has
been touched since. One of the two names is very likely dead weight.

**Rot finding (name collision with `_AI_MEMORY/`):** `docs/ACTIVE_FILES.md` (40,953 B) and
`docs/DECISIONS.md` (2,136 B) are same-named-but-different-content siblings of
`_AI_MEMORY/ACTIVE_FILES.md` (65,759 B) and `_AI_MEMORY/DECISIONS.md` (28,999 B). Nothing in the
onboarding chain (§3) points to the `docs/` copies; an agent that greps for `ACTIVE_FILES.md` or
`DECISIONS.md` by filename alone (rather than full path) will find two candidates with materially
different content and no disambiguation.

`docs/DEPENDENCY_AND_PATH_AUDIT.md` at 5.7 MiB is itself larger than the entire `_AI_MEMORY/`
directory (1.4 MiB) and larger than the entire mandated onboarding chain (§3, ~654 KB) — a
one-time migration-audit artifact from 2026-05-31 that has never been revisited and is not part of
any read order.

## 6. Stray directories (untracked, not in `origin/master`)

Confirmed via `git status` (untracked) and filesystem measurement — none of these are part of any
commit on `origin/master`:

| Path | Files | Size (on disk) |
|---|---|---|
| `.agents/skills/` (repo root) | 98 files | 251,489 B (~246 KiB) |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/Deepreseach/` | 10 files | 768,765 B (~751 KiB) |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/Deepresearc 2/` | 2 files | 70,726 B |

**Rot finding (misplaced, duplicated, and misspelled):** `apps/Deepreseach/` and
`apps/Deepresearc 2/` sit inside `08_DASHBOARD_APP/apps/`, alongside the real application source
(`apps/api/`, `apps/web/`, tracked). Both are pasted-in AI-chat exports (`Chatgbt.md`, `Gemini.md`,
`grok.md`, `preplexity.md`, a screenshots folder) — not application code. The two directory names
are themselves near-duplicate misspellings of "Deep Research" ("Deepreseach" / "Deepresearc 2"),
both untracked, both containing an overlapping `Chatgbt.md`/`Gemini.md` pair — i.e. this looks like
the same research-dump operation done twice into two differently-misspelled folders, neither ever
committed or cleaned up, inside a directory an agent would reasonably assume contains only app
source.

`.agents/skills/` is a Claude Code skills-lock installation directory (matches the untracked
`skills-lock.json` at repo root) — infrastructure/tooling state, not rot, but it is uncommitted and
undocumented in the onboarding chain.

## 7. Dirty main-checkout state (`C:\LAB\Tradingview_LAB_CLEAN`, branch `codex/bridge-help-wiki`)

Measured read-only via `git status`; **not modified by this research** (all writes went to the
isolated worktree `C:\WFR7A` on `research/repo-context-inventory` instead).

- Current branch `codex/bridge-help-wiki` is 73 commits ahead / 1 commit behind `origin/master`.
- **8 tracked files locally modified, uncommitted:** `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`, `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`, and 6 of the 7 core `_AI_MEMORY/` onboarding files: `ACTIVE_FILES.md`, `DECISIONS.md`, `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `SESSION_LOCK.md`, `START_HERE.md`.
- **152 untracked entries**, totaling **121,647,194 B (~116 MiB)** on disk. The largest single
  offenders are all raw agent-run `.log` transcripts under `MTC_COMMAND_CENTER/11_TRIAGE/` dated
  2026-08-11 through 2026-08-13 (10–12 days old at measurement time), e.g.:
  - `WPI_PREREG_DRAFT_ROUND1/SEC102_R2_CODEX_RUN_2026-08-11.log` — 14.75 MB
  - `RP6_R18_REPAIR_CODEX_RUN_2026-08-12.log` — 7.68 MB
  - `RULE2_SWEEP_CODEX_RUN_2026-08-12.log` — 5.41 MB
  - plus ~40 more `*_RUN_2026-08-1[1-3].log` files at 1–5 MB each.
  - Also included: the two `Deepreseach*` dirs (§6), `.agents/` (§6), `skills-lock.json`,
    `tmprepo_map_inventory.md` (a stray root-level file), and several `WPI_BLOCKS_DRAFT/` and
    `WPL_P2_STAGING_.../evidence/` subtrees.
- None of this untracked 116 MiB is covered by `.gitignore` — there is no `*.log` rule for
  `MTC_COMMAND_CENTER/11_TRIAGE/`, so every one of these files will keep showing up in `git status`
  indefinitely unless committed, moved, or a new ignore rule is added.

## 8. Tags and branches

- **Tags: 0** (confirmed via `git tag`, matches ticket's stated expectation).
- **Remote branches (`origin/*`): 121** total (including the `origin/HEAD -> origin/master`
  pointer), by namespace:

| Namespace | Count |
|---|---|
| `rescue/*` | 40 |
| `chore/*` | 21 |
| `feature/*` | 20 |
| `codex/*` | 18 |
| `research/*` | 16 |
| `prototype/*`, `master`, `integration/*`, `docs/*`, `claude/*` | 1 each |

- **Local branches: 164** — a mostly-disjoint superset dominated by ad hoc `wt-*`-prefixed branch
  names (e.g. `wt-tsp1004a4-wip-20260818`, `wt-gatea-a9-preflight-glm`) created for local worktrees
  that don't follow the `rescue/feature/codex/research/chore` remote convention at all — i.e. the
  local and remote branch-naming schemes have diverged into two different systems.
- **35 active local git worktrees** currently registered (`git worktree list`), each checked out to
  its own branch under `C:\` (e.g. `C:\WFB1`, `C:\WFK3`, `C:\WFMERGE54`, `C:\WFOLD`, `C:\R7FINAL`,
  `C:\WTCLEAN_CTRL`, plus this ticket's new `C:\WFR7A`) — most map 1:1 to a `research/*` or
  `feature/wayfinder-fold-*` branch, consistent with the wayfinder mapping/folding workflow
  referenced in AI_MEMORY.

## 9. Frozen legacy repo — `C:\LAB\tradingview-lab`

Existence and size only, per instructions (content not read):

- **Exists:** yes, and is itself a git repository (`.git/` present).
- **Size: 6,304,670,696 B (~6.01 GiB), 47,566 files, 36 top-level entries.**
- **Last filesystem write: 2026-05-31 18:51:34** — the same day as this repo's init/migration
  commit (`77a10e65`, 2026-05-31 17:52:41). The legacy repo has not been touched since the migration
  that created `Tradingview_LAB_CLEAN`.
- `AGENTS.md` (§3) explicitly names this directory as **"the FROZEN legacy repo — do NOT read its
  onboarding, run, or edit anything there,"** and instructs any agent whose entrypoint resolves
  under `C:\LAB\tradingview-lab\...` to stop and switch to this repo. The clean repo's `.gitignore`
  header also documents the migration path-prefix rewrites applied
  (`01_MASTER TEMPLATE_V2/` → `MTC_COMMAND_CENTER/01_MTC_PROJECT/`, etc.).
- At 6.01 GiB, the frozen legacy repo is **~6x the size of the entire tracked content of the live
  repo** (§1, ~1.02 GiB) — consistent with a broad multi-project archive that this repo split out a
  narrower slice from.

## 10. Summary — the 3 worst rot/duplication findings

1. **~796 MiB of tracked, single-batch dated run output in `03_QUANTLENS/`, most of it explicitly
   named in `.gitignore` as something that shouldn't be tracked but never removed from the index.**
   `tools/night_runs/` (332 MiB) + `tools/overnight_runs/` (90 MiB, ignored-but-still-tracked) +
   `research/data_acquisition_5m_2026_05_03/` (244 MiB) + `research/stage2_robustness_..._CODEX/`
   (94 MiB) — none touched since 2026-06-06 at the latest, most untouched since the 2026-05-31
   migration commit. This is ~78% of the entire repo's tracked bytes, and it is backtest/audit run
   evidence, not source.
2. **116 MiB of untracked agent-run `.log` files sitting uncommitted in the main checkout for
   10–12+ days**, dominated by `MTC_COMMAND_CENTER/11_TRIAGE/*_RUN_2026-08-1[1-3].log` (largest:
   14.75 MB), with zero `.gitignore` coverage — they will never stop showing up in `git status`
   until someone commits or ignores them. Compounded by 6 of the 7 mandated onboarding-chain files
   (`GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md`, `DECISIONS.md`, `SESSION_LOCK.md`,
   `START_HERE.md`) currently showing local uncommitted edits in the same checkout.
3. **Duplication and name collisions in the doc/memory layer**: `docs/DEPRECATED_FILES.md` and
   `docs/EXCLUDED_PROJECTS.md` are byte-identical (same git blob, 55,447 B) under two names, both
   dead since the 2026-05-31 migration; `docs/ACTIVE_FILES.md`/`docs/DECISIONS.md` collide by
   filename (but not content or size) with the canonical `_AI_MEMORY/ACTIVE_FILES.md`/`DECISIONS.md`
   that the onboarding chain actually points to; and the mandated onboarding chain itself
   (GLOBAL_HANDOFF.md + NEXT_STEPS.md, ~590 KB combined) has already needed one manual "rotation"
   into `_AI_MEMORY/archive/` (2026-08-15) and is back to 6-days-stale/243–334 KB per file only a
   week later — the growth pattern is structural (append-only logs with no size cap), not a
   one-time cleanup problem.

---

*Compiled 2026-08-23 for wayfinder research ticket #112 (parent #97, blocks #117). Read-only
measurement; no files in the main checkout or the frozen legacy repo were modified. All figures
above are reproducible via `git ls-tree -r -l origin/master`, `git log --follow`, `git branch -a`,
`git tag`, `git status`, and filesystem size checks against the paths cited.*
