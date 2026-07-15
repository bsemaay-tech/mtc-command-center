# Branch Consolidation Report — 2026-07-13

Executor: Codex GPT-5. Audit gate: stop after this deliverable for Claude Fable 5.

## Verdict

**BUILDER COMPLETE — READY FOR FABLE AUDIT.** Queue 2a–2c and the later approved Task 4 were
executed in the shared checkout.
No remote was pushed. No mainnet action occurred. `HL_LIVE_ACK` was not changed. No file under
`C:\P2RT` was read or written. Queue 2d (runtime sync/restart) was not performed.

The consolidated bridge branch is `feature/ibkr-bridge-final` at `960369b9`. It contains the
reviewed golden tree integration (`6442b000`) and a content-neutral two-parent ancestry merge
(`908e1b34`), followed by the test-only Telegram isolation fix (`960369b9`). The golden tip is an
ancestor. Both bridge suites passed `122 passed, 1 warning` after the final change.

## 1. Initial state and guard

Command:

```powershell
git branch --show-current
git status --short
```

Relevant output:

```text
feature/donchian-crypto-ladder
 M IBKR_PAPER_BRIDGE/docs/03_STATUS.md
 M MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
 M MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md
?? IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md
?? IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md
?? MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md
?? MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/
?? MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/
?? interrupted Donchian checkpoint/partial artifacts
?? Youtube transcrip/
```

`pwsh` was unavailable (`CommandNotFoundException`), so the identical guard script was run with
installed Windows PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER/tools/repo_guard.ps1
```

Output before the first commit and again before the merge:

```text
[staged]    none
[protected] none
[untracked] no risky files
WARN: no upstream tracking branch
RESULT: PASS
```

## 2. Task 1 — stray-file reconciliation

### 2.1 Golden report

The report describes the real 858-signal work (`18_GOLDEN_REPORT.md:78`). It was already committed
on `feature/quantlens-keltner-golden`; no duplicate commit was created.

```text
WORKING=9af59f80a451ef6c0be493ef206259bcd9cfa5a4
TARGET =9af59f80a451ef6c0be493ef206259bcd9cfa5a4
```

The untracked duplicate was moved to
`C:\tmp\codex_branch_consolidation_20260713\18_golden_identical_copy.md` because it would have
blocked the later merge. The committed branch copy remains authoritative.

### 2.2 Incident document and stale status

The stale incident copy was moved to
`C:\tmp\codex_branch_consolidation_20260713\19_stale_copy.md`. Its containment narrative was
preserved byte-for-byte from `## Final verdict` onward:

```text
HISTORICAL_NARRATIVE_IDENTICAL=True
```

Only its supersession banner was updated to record both resets:

- first ARM `2026-07-13T13:00:28.6218649Z` at `59c334c0`;
- auto-DISARM `13:29:59Z` on `DATA_STALE`;
- EMA correction `f209acd2`;
- current Day 0 `2026-07-13T15:17:05.383618Z` at evidence tip `54278b66`;
- 121-test runtime proof.

Evidence: `feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md:3-9`.

Commit:

```text
STAGED_FILES
IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md
SECRET_GREP_COUNT=0
[feature/ibkr-bridge-final 6db8bf62] docs(bridge): supersede incident doc banner with EMA-fix Day-0 reset
```

The stale `03_STATUS.md` was archived and the session-branch tracked version restored exactly as
the prompt sanctioned:

```powershell
Copy-Item IBKR_PAPER_BRIDGE/docs/03_STATUS.md `
  MTC_COMMAND_CENTER/11_TRIAGE/ARCHIVE_03_STATUS_stale_working_copy_2026-07-13.md
git checkout feature/donchian-crypto-ladder -- IBKR_PAPER_BRIDGE/docs/03_STATUS.md
```

Post-command `git status --short` no longer listed `03_STATUS.md`. The archive remains untracked
and is intentionally not committed.

### 2.3 UI audits and Sites residue

Five files under `11_TRIAGE/UI_AUDITS/IMPECCABLE_PILOT_R3/` were sampled and then checked by blob
hash against `feature/mcc-ui-impeccable-fixes`:

```text
UI_FILE_COUNT=5
UI_MISMATCH_COUNT=0
```

They are genuine R3 UI-pilot evidence (`CRITIQUE_RESCORE_2026-07-13.md:8` says `32/40 — Good`),
but already committed on the UI branch. No duplicate commit was made.

`08_DASHBOARD_APP/sites/strategy-kpi-site/` is not UI-pilot evidence. The current checkout contains
only generated directories:

```text
.vinext/
.wrangler/
dist/
node_modules/
```

The actual site source is already tracked separately on `codex/strategy-kpi-site`. Generated
residue was not committed. Recommended future ignore entries, not applied in this task:

```gitignore
MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/**/.vinext/
MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/**/.wrangler/
MTC_COMMAND_CENTER/08_DASHBOARD_APP/sites/**/dist/
```

Root `.gitignore:30` already covers `node_modules`.

### 2.4 Stage-2 prereg and interrupted research artifacts

The working prereg is byte-identical to the committed file on `feature/faz3b-stage2-prereg`:

```text
WORKING=a5e40659004fcc1144df8d94caaa00c07dff22c8
BRANCH =a5e40659004fcc1144df8d94caaa00c07dff22c8
```

No empty/delta commit was created. The committed source remains `1d42b383`.

Interrupted, non-verdict artifacts were left on disk and not staged:

```text
MEGA_walk_forward_checkpoint.pkl  7617 bytes
MEGA_walk_forward_partial.json    11607 bytes
```

Recommended path-specific ignores, not applied:

```gitignore
MTC_COMMAND_CENTER/03_QUANTLENS/research/**/MEGA_walk_forward_checkpoint.pkl
MTC_COMMAND_CENTER/03_QUANTLENS/research/**/MEGA_walk_forward_partial.json
```

`Youtube transcrip/` was listed only and never touched.

### 2.5 Shared handoff material

The audited P2 reset handoff, revised `NEXT_STEPS.md`, and this task prompt had to be committed
before safe branch switching because checkout correctly refused to overwrite those tracked edits.

```text
STAGED_FILES
MTC_COMMAND_CENTER/11_TRIAGE/CODEX_BRANCH_CONSOLIDATION_PROMPT_2026-07-13.md
MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md
SECRET_GREP_COUNT=0
[feature/donchian-crypto-ladder 8a08928e] docs(memory): record audited P2 reset and consolidation prompt
```

## 3. Task 2 — golden into bridge

### 3.1 Dry-run and real conflicts

Pre-merge `repo_guard.ps1` returned `RESULT: PASS`. `git merge-tree --write-tree` predicted the
same three conflicts encountered by the real `--no-commit --no-ff` merge:

```text
CONFLICT (content): IBKR_PAPER_BRIDGE/docs/03_STATUS.md
CONFLICT (content): IBKR_PAPER_BRIDGE/tests/test_strategy.py
CONFLICT (content): MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
```

Resolution rationale:

1. `03_STATUS.md`: retained the bridge's current Day-0/EMA/P2 record and discarded the golden
   branch's obsolete READY/114-test block. Added the completed golden reference while removing
   the now-false SMA runtime statement. Current Day 0 is at
   `feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/docs/03_STATUS.md:9`.
2. `test_strategy.py`: retained real `BTC_1h_real.csv` golden assertions and the deterministic
   synthetic EMA proof. Removed the conflicting line that overwrote synthetic bars with real bars.
   Evidence at `feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/tests/test_strategy.py:31` and `:80`.
3. `GLOBAL_HANDOFF.md`: preserved both P2 and golden entries; clarified that SMA divergence was
   historical and later superseded by `f209acd2`.
4. `18_GOLDEN_REPORT.md`: added a post-report supersession banner while preserving that the
   858/858 golden proves entry parity only. Evidence at
   `feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:3-6`.

### 3.2 Integration and ancestry commits

The reviewed merged tree was first committed as `6442b000`:

```text
STAGED_FILES (11)
IBKR_PAPER_BRIDGE/config/strategies/keltner_trail_ema8.yaml
IBKR_PAPER_BRIDGE/docs/03_STATUS.md
IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md
IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv
IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json
IBKR_PAPER_BRIDGE/tests/test_golden_generation.py
IBKR_PAPER_BRIDGE/tests/test_strategy.py
IBKR_PAPER_BRIDGE/tools/generate_golden.py
MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py
MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md
DIFF_CHECK=PASS
SECRET_GREP_COUNT=0
[feature/ibkr-bridge-final 6442b000] merge: integrate QuantLens Keltner golden into bridge
```

Audit then caught that the same-branch checkout used after conflict staging had cleared
`MERGE_HEAD`; `6442b000` therefore had one parent. History was not rewritten. After another guard,
a content-neutral `ours` strategy merge recorded the already-integrated golden ancestry:

```text
STAGED_FILES=<empty>
SECRET_GREP_COUNT=0
[feature/ibkr-bridge-final 908e1b34] merge: record QuantLens golden branch ancestry
GOLDEN_ANCESTOR_AFTER=0
PARENTS=6442b000757912a0153ef8bd88058e45987e1513 4ee8a098a1b137957981aa645457dadc27f4b72e
git diff --stat 6442b000..908e1b34 = <empty>
```

This is an explicit anomaly, not hidden: `6442b000` carries the reviewed content; `908e1b34`
adds only the missing second-parent relationship.

### 3.3 Tests

Commands:

```powershell
$env:PYTHONUTF8='1'; python -m pytest IBKR_PAPER_BRIDGE/tests -q
$env:PYTHONUTF8='1'; python -m pytest tests -q  # from IBKR_PAPER_BRIDGE/
```

Outputs:

```text
repo root:          122 passed, 1 warning in 19.42s
IBKR_PAPER_BRIDGE:  122 passed, 1 warning in 19.40s
```

The only warning is the existing Starlette/httpx deprecation. `908e1b34` is tree-identical to the
tested `6442b000`, proven by the empty tree diff above.

## 4. Task 3 — text-only PR proposals

Commands run per branch:

```powershell
git log --oneline master..<branch> | Select-Object -First 30
git merge-base master <branch>
git rev-list --count master..<branch>
git diff --name-only master...<branch>
git diff --stat master...<branch> | Select-Object -Last 3
git merge-tree --write-tree master <branch>
```

Current individual master probes are all clean:

| Branch | Commits vs master | Files | Diff tail | Master conflict probe |
|---|---:|---:|---|---|
| `feature/ibkr-bridge-final` | 102 | 93 | 69,413 insertions / 1 deletion | exit 0, none |
| `feature/mcc-ui-impeccable-fixes` | 3 | 9 | 81 insertions / 77 deletions | exit 0, none |
| `feature/donchian-crypto-ladder` | 95 | 102 | 69,725 insertions / 14 deletions | exit 0, none |
| `feature/faz3b-stage2-prereg` | 1 | 3 | 313 insertions / 9 deletions | exit 0, none |

All four currently share merge base `af26d6a74979ec3e7176890557fde8b1a3431b99` with master.

### PR proposal 1 — bridge

**Title:** `Bridge P2 hardening, EMA-8 correction, and real QuantLens golden`

**Body:** Merge the complete Hyperliquid testnet paper-bridge build and audited P0/P2 safety
hardening, including reconnect/reconcile fail-closed behavior, supervisor and deployment docs,
the approved EMA-8 correction, the current Day-0 evidence record, and the real QuantLens
858-signal entry golden. It also prevents pytest from resolving real Telegram credentials through
the Windows registry. Both supported bridge test invocations pass 122 tests. This does not sync or
restart the pinned P2 runtime and does not authorize mainnet.

**Conflicts:** none against current master. Pairwise probes show `GLOBAL_HANDOFF.md` conflicts with
each other proposed branch; `NEXT_STEPS.md` auto-merges against UI/Faz but conflicts with Donchian.

### PR proposal 2 — UI

**Title:** `Polish MCC Strategy Detail and keep the right rail canonical`

**Body:** Land the three audited R3 UI-pilot commits: criteria-note deduplication, removal of
duplicate verdict surfaces in favor of the persistent right rail, and the honest 32/40 critique
rescore with before/after screenshots. Scope is UI/a11y/docs only; no trading or data-contract
behavior changes.

**Conflicts:** none against current master. Cross-branch conflict: `GLOBAL_HANDOFF.md` with all
three other branches; `NEXT_STEPS.md` auto-merges in the direct bridge/UI probe but conflicts in
some later combinations.

### PR proposal 3 — Faz3b prereg

**Title:** `Pre-register Faz3b Stage-2 exit confirmation`

**Body:** Add the DRAFT Stage-2 confirmation preregistration and its handoff/next-step records.
This is documentation only: D016 remains unapproved, and no runner, smoke, or confirmation run is
authorized by this PR.

**Conflicts:** none against current master. Cross-branch conflict: `GLOBAL_HANDOFF.md` with every
other branch; `NEXT_STEPS.md` conflicts with Donchian and may require union resolution after earlier
PRs land.

### PR proposal 4 — Donchian

**Title:** `Record Donchian crypto ladder NULL result and consolidation handoff`

**Body:** Land the audited BTC/ETH 1h/4h Donchian ladder evidence and corrected NULL verdict,
registry records, and the latest shared handoff/consolidation report. The branch currently appears
large because it shares bridge/golden history; merging the bridge PR first should reduce the
effective Donchian-only delta to its research and handoff commits. Nothing is promotable or ready
for forward paper.

**Conflicts:** none against current master. After the bridge ancestry correction, pairwise probes
show only `GLOBAL_HANDOFF.md` and `NEXT_STEPS.md` conflicts; the earlier `test_strategy.py` conflict
is eliminated.

### Recommended merge order

1. `feature/ibkr-bridge-final` — establishes the consolidated bridge/golden ancestry and reviewed
   test resolution.
2. `feature/mcc-ui-impeccable-fixes` — small independent UI delta; union shared handoff entries.
3. `feature/faz3b-stage2-prereg` — small documentation-only delta; preserve DRAFT/D016 gate text.
4. `feature/donchian-crypto-ladder` — land last because it carries the newest shared handoff,
   this consolidation report, and golden-derived history. Resolve `GLOBAL_HANDOFF.md` and
   `NEXT_STEPS.md` as a union, keeping Donchian's latest top sections while retaining UI/Faz entries.

Pairwise probe summary after ancestry repair:

```text
bridge + UI       -> GLOBAL_HANDOFF conflict
bridge + Donchian -> GLOBAL_HANDOFF, NEXT_STEPS conflicts
bridge + Faz      -> GLOBAL_HANDOFF conflict
UI + Donchian     -> GLOBAL_HANDOFF conflict
UI + Faz          -> GLOBAL_HANDOFF conflict
Donchian + Faz    -> GLOBAL_HANDOFF, NEXT_STEPS conflicts
```

## 5. Task 4 — pytest Telegram isolation

The prompt gained this Barış-approved task during execution. The verified leak chain was:

```text
create_app() -> build_notifier() -> resolve_telegram_credentials()
             -> HKCU fallback -> real sender during /api/arm tests
```

The bounded one-file edit was offered to Cline first; Cline failed before work with
`session not found`. The DeepSeek harness fallback edited only `IBKR_PAPER_BRIDGE/tests/conftest.py`
under an exact write allowlist. Codex then audited the real diff.

Implementation evidence at
`feature/ibkr-bridge-final:IBKR_PAPER_BRIDGE/tests/conftest.py:13-22`:

```python
@pytest.fixture(autouse=True)
def _no_real_telegram(monkeypatch):
    monkeypatch.setattr(
        "bridge.settings.resolve_telegram_credentials", lambda: ("", "")
    )
    monkeypatch.setattr(
        "bridge.engine.notify.resolve_telegram_credentials", lambda: ("", "")
    )
```

Both names are required because `bridge.engine.notify` imports a copied resolver reference.
Runtime code was untouched.

Focused acceptance:

```powershell
$env:PYTHONUTF8='1'
python -m pytest `
  IBKR_PAPER_BRIDGE/tests/test_task11_polish.py::test_build_notifier_disabled_without_creds `
  IBKR_PAPER_BRIDGE/tests/test_task11_polish.py::test_build_notifier_enabled_sends_via_http_sender -q
```

```text
2 passed, 1 warning in 0.45s
```

Grep proof:

```text
tests/conftest.py patches both resolver names to empty credentials for every test.
tests/test_task11_polish.py:80 explicitly supplies fake credentials.
tests/test_task11_polish.py:81 explicitly replaces _http_sender with fake_sender.
No other test path references _http_sender.
```

Full-suite outputs after the fixture change:

```text
repo root:          122 passed, 1 warning in 17.97s
IBKR_PAPER_BRIDGE:  122 passed, 1 warning in 17.76s
```

Commit:

```text
STAGED_FILES
IBKR_PAPER_BRIDGE/tests/conftest.py
DIFF_CHECK=PASS
SECRET_GREP_COUNT=0
[feature/ibkr-bridge-final 960369b9] test(bridge): block real Telegram credentials in pytest
```

Important runtime caveat: `C:\P2RT` was deliberately not synced or touched. Until the next
planned restart/sync window, a suite run from inside `C:\P2RT` still uses its old conftest and can
emit test Telegram messages. Do not run its suite during P2 unless that consequence is accepted.

## 6. Operational anomalies and left undone

- `pwsh` was unavailable; installed Windows PowerShell ran the same guard successfully.
- Two early Bash `-lc` commit wrappers failed before mutation because Windows argument parsing
  stripped quotes. The final stdin-fed Bash wrapper produced the required exact grep count.
- Initial golden checkout was refused because the report was already tracked on the target branch
  and shared handoff edits would be overwritten. Blob checks prevented a duplicate commit.
- `feature/ibkr-bridge-final` is registered to another worktree, so shared-checkout branch switches
  required `--ignore-other-worktrees`. No path under `C:\P2RT` was accessed.
- The first reviewed integration commit lost merge ancestry when same-branch checkout cleared
  `MERGE_HEAD`; `908e1b34` repairs ancestry without changing the tested tree.
- No push or PR creation was performed.
- P2RT sync/restart (queue 2d) was not performed.
- The pytest Telegram isolation fix exists only on the shared branch tip `960369b9`; the pinned
  runtime retains its old test fixture until the separately planned sync window.
- The stale-status archive, generated Sites residue, interrupted research artifacts, byte-identical
  UI/prereg working copies, and `Youtube transcrip/` remain untracked/on disk as documented.

## Stop condition

Stop here for Fable audit. Queue 3 was not started.
