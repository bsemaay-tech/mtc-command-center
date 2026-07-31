# FABLE TS-P0 AUDIT HANDOFF — 2026-07-19

For the INDEPENDENT Fable auditor of the TS-P0-001..004 build. Companion
build report: `FABLE_TSP0_BUILD_REPORT_2026-07-19.md`. Audit on real code and
real runs only — do not trust this document's claims without reproducing.

## Where

- Worktree: `C:\TSP0`, branch `feature/ts-p0-baseline`, base `008e065e`
  (= `origin/master`). Expected final HEAD: **`7777273f`**, porcelain clean.
- Per-task commits: Task A `fa449ce2` → Task B `42d0ca9f` → Task C `7777273f`.
  Task D is docs-only in the MAIN worktree's untracked
  `MTC_COMMAND_CENTER/09_DOCS/ADR/` (no commit; see build report).
- Runtime `C:\P2RT`: **READ-ONLY. Live Day 1 v1 window. Never write /
  checkout / restart / ARM / DISARM / touch scheduler or DB.** Allowed:
  `git -C C:\P2RT` read commands, file reads, one `GET /api/status`.

## Green-suite reproduction (both CWDs, PYTHONUTF8=1)

```
cd C:\TSP0                     && python -m pytest IBKR_PAPER_BRIDGE/tests -q   # expect 210 passed
cd C:\TSP0\IBKR_PAPER_BRIDGE   && python -m pytest tests -q                     # expect 210 passed
```

Baseline check: `git -C C:\TSP0 stash list` must be empty; baseline 164 count
is reproducible at the base commit via a THROWAWAY second worktree if desired
(`git worktree add <tmp> 008e065e`) — do NOT move C:\TSP0 itself.

## RED-proof reproduction (COMMITTED state only; worktree returns clean)

All three tasks were TDD; the impl is absent/old at each commit's parent while
the tests exist in the commit. Recipes (run at `C:\TSP0`, restore after each):

- Task A (at HEAD or `fa449ce2`):
  ```
  rm IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py
  python -m pytest IBKR_PAPER_BRIDGE/tests/test_runtime_baseline.py -q   # collection ImportError
  git checkout -- IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py
  ```
- Task B:
  ```
  rm IBKR_PAPER_BRIDGE/tools/release_evidence.py
  python -m pytest IBKR_PAPER_BRIDGE/tests/test_release_evidence.py -q   # collection ImportError
  git checkout -- IBKR_PAPER_BRIDGE/tools/release_evidence.py
  ```
- Task C (impl files existed before; restore them to the parent state):
  ```
  git restore --source=7777273f^ -- IBKR_PAPER_BRIDGE/bridge/engine/engine.py IBKR_PAPER_BRIDGE/bridge/api/routes.py
  rm IBKR_PAPER_BRIDGE/bridge/engine/window.py
  python -m pytest IBKR_PAPER_BRIDGE/tests/test_window_state.py -q       # ModuleNotFoundError
  git checkout -- IBKR_PAPER_BRIDGE/bridge
  ```

## Integration re-run (read-only)

```
cd C:\TSP0
python IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py --repo-root C:/TSP0 --runtime-root C:/P2RT --expected-commit 008e065e
```
Expect: exit **2**; drift_reasons exactly `repo_commit_mismatch_expected` +
`repo_runtime_commit_mismatch`; `runtime_commit_matches_expected: true`;
`source_tree_hash_equal: true`; `config_hash_equal: true`; both `dirty: false`.
Then verify `git -C C:\P2RT status --porcelain` empty and HEAD still
`008e065e…` — the tool must not have touched the runtime.

## Adversarial attack checklist (verify each, on real code)

1. **Hash-scope bypass:** plant a file OUTSIDE the declared scope (e.g.
   `IBKR_PAPER_BRIDGE/docs/x.py`) in a FIXTURE repo — must not affect hashes;
   plant INSIDE `bridge/` — must change `source_tree_hash`. Is the scope in
   `SOURCE_SCOPE`/`CONFIG_SCOPE` actually what the contract doc claims?
2. **Line-ending normalization abuse (new surface):** `_hash_file` strips
   `\r\n` in text files. Confirm a REAL content change that also flips line
   endings is still detected; confirm binary detection (NUL sniff, first 8KB)
   can't be used to smuggle a text change past normalization (e.g. file with
   early NUL then differing text hashes raw → detected anyway).
3. **Symlink / path traversal:** scope walk uses `rglob` under the root —
   check a symlink inside a fixture scope dir pointing outside (or at a
   secret) is either not followed into hashing of denylisted names or cannot
   leak content; secret denylist is basename-based — try `config/prod.env`?
   (`.env*` pattern is prefix-anchored: `^\.env(\..*)?$` — does `prod.env`
   slip through? If yes, is that acceptable scope or a nit?)
4. **Dirty-state false negative:** untracked file in fixture runtime →
   `runtime_dirty` must appear; ignored files (`.gitignore`d) do NOT set
   dirty — matches git porcelain semantics; confirm P2RT's ignored
   `data/`/`__pycache__` therefore can't hide REAL drift inside the hashed
   scope (they're outside scope / excluded dirs — verify).
5. **Exit-code lies:** force each verdict in fixtures and check the PROCESS
   exit code (subprocess-level, not just `main()` return): MATCH→0, any
   drift→2, RUNTIME_MISSING→2, bad repo root→3, malformed HEAD→3, argparse
   error→3. Confirm `exit_code` field inside the manifest always equals the
   real exit code.
6. **Byte-stability:** two runs with the same `--timestamp` → byte-identical
   JSON and MD; without `--timestamp` only `generated_at_utc` differs.
7. **Secret leakage:** planted `.env` + `secrets.key` with a sentinel string:
   sentinel must appear NOWHERE in stdout/stderr/JSON/MD; file must appear in
   `excluded` with reason; spy-hash test proves it is never opened. Also
   check `release_evidence` inherits this (it hashes via the same walk).
8. **Release-evidence integrity:** re-sign attack — tamper a hash AND
   recompute `integrity_sha256` (tests only tamper without re-sign for the
   integrity check): validate must STILL fail via live-state comparison
   (`*_mismatch`) when trees don't match. Confirm `create` refuses
   release-commit ≠ HEAD (no synthesized evidence) and rollback==release.
9. **Window-state false-active (core acceptance):** try to construct ANY
   store meta combination where `window_status` yields RUNNING with stale or
   missing liveness — the exhaustive sweep test claims impossible; verify the
   decision order in `compute_window_state` (reset→started→liveness→
   interrupted→armed) and that `record_window_start` does NOT clear
   `window_interrupted_ts` (re-arm must stay INTERRUPTED until
   `reset_window`). Check `init_runtime_state`'s engine-less `window` block
   also fails safe (`no_store` → DOWN).
10. **No-mutation:** full snapshot before/after tool runs on fixtures (test
    exists); ALSO verify against the real pair: P2RT porcelain + HEAD
    unchanged after your integration re-run.
11. **Existing-caller regression:** the 164 pre-existing tests are unmodified
    (diff `IBKR_PAPER_BRIDGE/tests` at `008e065e` vs `7777273f` — only the
    one fixture line in `test_runtime_baseline.py` (Task B) and three NEW
    test files should appear; no existing test file edited).
12. **Task D:** confirm the three ADR wording edits changed status wording
    only (git is no help — files untracked; compare against D016 text and the
    report's claimed before/after strings) and DECISIONS.md untouched by this
    session.

## Requested verdict form

**PASS / PASS-WITH-NITS / BLOCK** with per-task findings, each finding tied
to a file:line or a reproduced command output. Nits → name them explicitly so
they can fold into follow-up tasks. BLOCK requires a reproducible failing
command or a concrete violated constraint (card text, safety boundary, or
false claim in the build report).

## Boundaries for the auditor (same as builder)

No push/PR/merge, no deploy, no P2RT mutation, no ARM/DISARM, no scheduler/
DB/process action, no network calls except the one localhost status GET, no
dependency additions, protected scopes untouched. Main worktree carries
pre-existing user files — never clean/reset/stash there.

## Correction — 2026-07-20

The integration expectation above is commit-specific. At final build HEAD
`7777273f` (and the later audited repair `44338d61`), the correct real-pair
result is exit 2 with three drift reasons, including
`source_tree_hash_mismatch`, because Task C legitimately changed operational
bridge files relative to `C:\P2RT@008e065e`. The earlier two-reason expectation
was valid only at Task A commit `fa449ce2`. Do not weaken the approved hash
scope to remove the third reason.
