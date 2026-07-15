# CODEX PROMPT — Queue 2: Branch Consolidation (2026-07-13)

Author: Claude Fable 5 (auditor). Executor: Codex GPT-5 (builder).
Scope: shared checkout `C:\LAB\Tradingview_LAB_CLEAN` ONLY. Cleared by Fable audit 2026-07-13
(see GLOBAL_HANDOFF `## [Claude Fable 5] 2026-07-13 — AUDIT PASS`).

## ROLE

You are Codex, the builder/executor. Execute the tasks below top-down. Produce an
evidence-rich report (every claim backed by a pasted command + output + file:line), then STOP
for Fable audit. Do not continue to queue 3.

## HARD RAILS (violating any = task failure)

1. **NEVER touch `C:\P2RT`.** The P2 runtime is pinned there and ARMED (Day 0 =
   2026-07-13T15:17:05Z). No file reads needed there for this task; no writes ever.
   Queue 2d (P2RT sync) is explicitly OUT of this prompt — it happens only in a planned
   restart window approved by Barış.
2. TESTNET only; `HL_LIVE_ACK` stays unset; never print/log `HL_API_WALLET_KEY`.
3. Before EVERY commit: secret grep on staged files —
   `git diff --cached | grep -cE "[0-9a-fA-F]{64,}"` must be 0.
4. A repo hook flips HEAD back to `master` between tool calls. EVERY commit must be ONE
   inline command: `git checkout <branch> && git add <explicit paths> && git commit -m "..."`.
   Verify the staged set with `git diff --cached --name-only` INSIDE the same command chain
   (between add and commit) when practical, or immediately re-verify with `git show --stat HEAD`
   after.
5. NEVER `git add .` / `git add -A`. Explicit paths only.
6. NO `git checkout`/`reset`/`stash` of a tracked file that carries uncommitted foreign work,
   EXCEPT the single sanctioned restoration in Task 1c below (its content was audited stale;
   archive first as instructed).
7. NO push to any remote. PRs are proposed as text only (Task 3); Barış pushes/merges.
8. `PYTHONUTF8=1` for all pytest runs. Bridge suite must pass from BOTH CWDs (repo root via
   `python -m pytest IBKR_PAPER_BRIDGE/tests -q` AND from inside `IBKR_PAPER_BRIDGE/`).
9. Run `pwsh -File MTC_COMMAND_CENTER/tools/repo_guard.ps1` (dry-run) before the first commit
   and before the merge. Proceed only on PASS; paste output in the report.
10. Report failures as failures. Fable audits everything against real code and runs.

## STATE YOU MUST KNOW (verified by Fable 2026-07-13)

- Shared checkout session branch: `feature/donchian-crypto-ladder` (hook reverts HEAD to
  master between calls — always re-checkout inline).
- Local ref `feature/ibkr-bridge-final` tip = `54278b66` (docs: Day-0 reset after EMA fix
  `f209acd2`; 121 tests). This equals the P2RT runtime tip. NO divergence.
- **The working-tree `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` (modified) and untracked
  `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md` are STALE intermediate
  rewrites** from an earlier audit session: they still claim Day 0 `13:00:28Z`, commit
  `59c334c0`, 119 tests — all superseded by `f209acd2`/`54278b66` (Day 0 `15:17:05.383618Z`,
  121 tests). Committing them as-is would REGRESS the bridge branch tip. Task 1 tells you
  exactly how to reconcile.

## TASK 1 — Commit stray files to their correct branches (queue 2a)

Current stray set (from `git status --porcelain`; re-run it first and reconcile against this
list; GLOBAL_HANDOFF/NEXT_STEPS will also show Fable's audit edits — that is expected):

| Path | Disposition |
|---|---|
| `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md` (untracked) | → `feature/quantlens-keltner-golden` |
| `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md` (untracked, STALE) | → `feature/ibkr-bridge-final` AFTER banner fix (1b) |
| `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` (modified, STALE) | archive + restore (1c). DO NOT commit. |
| `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/` (untracked) | → `feature/mcc-ui-impeccable-fixes` |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/` (untracked) | investigate: if UI-pilot output → `feature/mcc-ui-impeccable-fixes`; if generated/build junk → propose gitignore, do not commit; state which in report |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md` (untracked) | → `feature/faz3b-stage2-prereg` — BUT first check whether that branch already contains a committed version; if yes, diff and either commit the delta or report identical |
| `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`, `NEXT_STEPS.md` (modified, shared) | → `feature/donchian-crypto-ladder` (session HEAD branch), together with this prompt file and your report (1e) |
| `MTC_COMMAND_CENTER/03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/MEGA_walk_forward_checkpoint.pkl` + `MEGA_walk_forward_partial.json` (untracked) | interrupted-run artifacts, NOT verdict evidence. Do NOT commit the `.pkl`. Check sizes; propose gitignore entries in the report; leave on disk. |
| `Youtube transcrip/` (untracked) | Barış's own folder. DO NOT touch, DO NOT commit. List in report only. |

Ordering note: do 1c (restore 03_STATUS) BEFORE any `git checkout feature/ibkr-bridge-final`,
otherwise checkout may refuse or drag the dirty file across branches. Similarly move the
untracked `19_...md` aside (1b) before checking out `feature/ibkr-bridge-final`, because that
branch already tracks a file at the same path.

### 1a. Golden report → quantlens branch

```
git checkout feature/quantlens-keltner-golden && git add IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md && git commit -m "docs(bridge): golden parity report"
```

First verify the file's content actually describes the 858-signal golden work (read it); if it
references anything else, stop and report instead of committing.

### 1b. Incident doc → bridge branch, banner updated first

1. Move the untracked working copy aside:
   `mv IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md <scratchpad>/19_stale_copy.md`
2. `git checkout feature/ibkr-bridge-final` (inline with next steps as needed).
3. Compare `<scratchpad>/19_stale_copy.md` against the committed version
   (`git show feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`).
   The stale copy's structure (containment record + `RESOLVED / SUPERSEDED` banner) is GOOD;
   its banner facts are STALE.
4. Produce the final version: keep the banner structure, but the banner must state BOTH
   resets: first ARM `13:00:28Z` at `59c334c0` (auto-disarmed `13:29:59Z` on `DATA_STALE`),
   then the approved EMA-8 fix `f209acd2` and the **current Day 0 = 2026-07-13T15:17:05.383618Z**
   at tip `54278b66`, 121 tests. Do not alter the historical containment narrative below the
   banner.
5. Inline commit to `feature/ibkr-bridge-final` with message
   `docs(bridge): supersede incident doc banner with EMA-fix Day-0 reset`.

### 1c. 03_STATUS.md — archive + restore, NO commit

1. Archive the stale working copy:
   `cp IBKR_PAPER_BRIDGE/docs/03_STATUS.md MTC_COMMAND_CENTER/11_TRIAGE/ARCHIVE_03_STATUS_stale_working_copy_2026-07-13.md`
   (create it as an untracked archive; commit it nowhere unless Fable asks).
2. Restore the tracked file to session-branch HEAD content:
   `git checkout feature/donchian-crypto-ladder -- IBKR_PAPER_BRIDGE/docs/03_STATUS.md`
   — sanctioned because Fable audited the working copy as strictly-stale (novel content =
   minor wording only; canonical current status lives at `54278b66` on the bridge branch).
3. Confirm `git status --porcelain` no longer shows `03_STATUS.md` as modified.

### 1d. UI audits → UI branch

Read a sample of `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/` to confirm it is the UI-pilot audit
output, then inline commit the directory's explicit file list (enumerate files; no `-A`) to
`feature/mcc-ui-impeccable-fixes`. Same pattern for `08_DASHBOARD_APP/sites/` IF it belongs to
the UI work (see table).

### 1e. Shared handoff files → session branch

Inline commit `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`,
`MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`,
`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_BRANCH_CONSOLIDATION_PROMPT_2026-07-13.md`, and (when
written) your report to `feature/donchian-crypto-ladder`.

## TASK 2 — Merge golden branch into bridge branch (queue 2b)

1. Guard dry-run (rail 9).
2. `git checkout feature/ibkr-bridge-final && git merge feature/quantlens-keltner-golden`
   (one inline chain; if the hook interrupts a conflicted merge mid-resolution, resolve and
   `git commit` inline the same way).
3. If conflicts: resolve honestly, list every conflicted file + resolution rationale in the
   report. If the merge is already-contained/fast-forward, say so with `git log` proof.
4. Bridge suite from BOTH CWDs (rail 8) on the merged branch. Expect ≥121 passing (golden
   parity tests may add to the count); paste both tails. Any failure = STOP, report, no
   further tasks.

## TASK 3 — PR proposals to master (queue 2c; TEXT ONLY, no push)

For each of `feature/ibkr-bridge-final` (post-merge), `feature/mcc-ui-impeccable-fixes`,
`feature/donchian-crypto-ladder`, `feature/faz3b-stage2-prereg`:

- `git log --oneline master..<branch> | head -30` and
  `git merge-base master <branch>` + `git diff --stat master...<branch> | tail -3`.
- Dry-run conflict probe WITHOUT committing anything to master, e.g.
  `git merge-tree $(git merge-base master <branch>) master <branch>` (or
  `git merge-tree --write-tree master <branch>` on newer git) and grep for conflict markers.
- Report per branch: title, one-paragraph body, commit count, files touched, conflict list
  (honest — include cross-branch conflicts, e.g. all four may touch GLOBAL_HANDOFF/NEXT_STEPS),
  and your recommended merge ORDER for Barış.

## TASK 4 — Test-suite Telegram leak fix (ADDED 2026-07-13, Barış-approved)

**Bug (Fable-verified on real code + live Telegram):** the test suite sends REAL Telegram
messages to Barış's chat. Chain: `create_app()` always calls `build_notifier()`
(`bridge/app.py:107`) → `resolve_telegram_credentials()` falls back to HKCU registry (E1) and
finds the real creds → `test_api.py` POSTs `/api/arm` → real `[INFO] state -> ARMED` lands in
Telegram. Confirmed deliveries: 15:03/15:04Z (your pre-deploy suite runs) and 15:27/15:28Z
(Fable's audit suite runs). Your Task 2 suite runs will have produced two more.

**Fix (test-only; runtime code untouched):** in `IBKR_PAPER_BRIDGE/tests/conftest.py` add an
autouse fixture that neutralizes Telegram credential resolution for every test:

```python
import pytest


@pytest.fixture(autouse=True)
def _no_real_telegram(monkeypatch):
    # Empty PROCESS env is NOT enough: resolve_user_env falls through to the
    # HKCU registry (settings.py E1 pattern). Patch the resolver at BOTH import
    # sites so build_notifier() stays silently disabled in tests.
    monkeypatch.setattr(
        "bridge.settings.resolve_telegram_credentials", lambda: ("", "")
    )
    monkeypatch.setattr(
        "bridge.engine.notify.resolve_telegram_credentials", lambda: ("", "")
    )
```

CRITICAL detail: `bridge/engine/notify.py` does `from bridge.settings import
resolve_telegram_credentials` — patching only `bridge.settings` misses the copied reference;
patch both names as above.

**Acceptance:**
1. `test_task11_polish.py::test_build_notifier_disabled_without_creds` and
   `..._enabled_sends_via_http_sender` still pass (their own test-level monkeypatches override
   the autouse fixture; verify, don't assume).
2. Full suite green from BOTH CWDs.
3. Grep proof in the report that no test path reaches `_http_sender` with registry creds
   anymore (only explicit test monkeypatches construct senders).

Commit to `feature/ibkr-bridge-final` (inline pattern, secret grep first).
**Do NOT touch `C:\P2RT`** — the pinned runtime keeps the old conftest until the next planned
sync window; until then any suite run inside `C:\P2RT` will still emit fake Telegram messages.
State this caveat in the report.

## DELIVERABLE

`MTC_COMMAND_CENTER/11_TRIAGE/BRANCH_CONSOLIDATION_REPORT_2026-07-13.md` containing: every
command run + pasted output (trim noise, keep verdict lines), per-commit hash + staged file
list + secret-grep result, guard outputs, both test-suite tails, PR proposal section, and an
honest "anomalies / left undone" section. Update `GLOBAL_HANDOFF.md` with a dated
`## [Codex GPT-5] 2026-07-13 — Branch consolidation` section and tick nothing in NEXT_STEPS
you did not actually finish. Then STOP for Fable audit.
