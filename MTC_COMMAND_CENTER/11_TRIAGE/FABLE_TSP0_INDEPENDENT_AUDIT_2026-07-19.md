# FABLE TS-P0 INDEPENDENT AUDIT — 2026-07-19

- Auditor: Claude Fable 5, fresh session (no builder context beyond the published
  build report/handoff; every claim below reproduced on real code and real runs).
- Scope: TS-P0-001..004 in `C:\TSP0` (`feature/ts-p0-baseline`, base `008e065e`,
  HEAD `7777273f`) per `FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md`.
- Routing note: NEXT_STEPS routed this audit to Codex
  (`CODEX_TSP0_AUDIT_PROMPT_2026-07-19.md`) while the handoff names a Fable
  auditor. This report executes the full 12-point checklist as Fable; whether a
  Codex cross-audit still runs is Barış's call.

## VERDICT: **PASS-WITH-NITS**

No BLOCK finding. All safety boundaries held; every builder claim I tested
reproduced. Five nits (N1–N5), none gating push/PR; N1 and N4 deserve follow-up
edits, N3 is a handoff-doc correction recorded here.

## Reproduced evidence

| Check | Result |
| --- | --- |
| Worktree facts | HEAD `7777273f`, porcelain clean, stash empty, branch `feature/ts-p0-baseline`, merge-base `008e065e` ✔ |
| Green suite | **210 passed** from `C:\TSP0` AND from `C:\TSP0\IBKR_PAPER_BRIDGE` (PYTHONUTF8=1) ✔ |
| RED proofs | All three reproduced at HEAD (impl moved aside / Task C parent-restored → collection ImportError/ModuleNotFoundError); worktree restored porcelain-clean ✔ |
| Integration vs real pair | exit 2, DRIFT; P2RT porcelain empty + HEAD `008e065e` after run (no mutation) ✔ — see N3 for the handoff's stale expected-reasons list |
| Repo guard | PASS (main worktree preflight; dirty set = known pre-existing user files only) |
| Commit isolation | `git diff --name-status 008e065e..HEAD`: only 2 modified bridge files + 9 added files; **zero pre-existing test files edited** (checklist item 11) ✔ |

## Adversarial checklist results (items 1–12)

1. **Hash scope** ✔ — `SOURCE_SCOPE`/`CONFIG_SCOPE` in `check_runtime_baseline.py:38-43`
   match `RUNTIME_BASELINE_CONTRACT.md:80-88` exactly; walk is rooted at scope
   entries so out-of-scope files are excluded by construction.
2. **Line-ending normalization** ✔ — `_hash_file` only collapses `\r\n`→`\n`; any
   real content change still alters the hash. Binary sniff (NUL in first 8KB)
   forces raw hashing, so a NUL-prefixed file cannot smuggle a text change —
   raw mode detects every byte difference. Fixture test
   `test_line_ending_only_difference_not_hash_drift` reproduced in the suite.
3. **Symlink/denylist** — dir symlinks are not traversed by `rglob("**")`; a file
   symlink would expose only a SHA-256 digest of its target (hash oracle, no
   content leak; symlink creation is privileged on Windows) → acceptable (N5
   note). **Denylist gap CONFIRMED:** `_is_secret_name("prod.env") == False`,
   `config.env` also False (pattern `^\.env(\..*)?$` is prefix-anchored) → N2.
4. **Dirty-state** ✔ — hashing walks the filesystem, not git, so a
   `.gitignore`-hidden file inside scope still changes the tree hash (the
   ignore-hole is closed); P2RT's ignored `data/`/`__pycache__` are outside
   scope / excluded dirs; real-pair run shows `excluded: []`, `dirty: false`.
5. **Exit codes** ✔ — subprocess-level probes: MATCH→0 (self-pair), drift→2
   (real pair), argparse-missing→3, bad expected-commit→3, missing repo root→3;
   manifest `exit_code` field equals the real process exit in both 0 and 2 cases.
6. **Byte-stability** ✔ — two subprocess runs with the same `--timestamp`
   produced byte-identical stdout JSON.
7. **Secret leakage** ✔ — `test_secret_safe_output` verified in-suite: sentinel
   in `.env`/`secrets.key` appears nowhere in stdout/stderr/manifest, spy-hash
   proves the files are never opened, both recorded under `excluded`, exit 2.
8. **Release-evidence re-sign** ✔ — probe: tampered `source_tree_hash` +
   recomputed `integrity_sha256` on a well-formed manifest → validate exit 2,
   failures `['source_tree_hash_mismatch']` (live-state comparison catches what
   the checksum cannot). `create` verified: refuses release≠HEAD,
   rollback==release, unknown rollback. Adjacent crash found → N1.
9. **Window false-active (core acceptance)** ✔ — decision order in
   `window.py:76-88` matches the documented contract (reset→started→liveness→
   interrupted→ARMED→else); liveness staleness precedes RUNNING, so RUNNING with
   stale/missing liveness is structurally unreachable; exhaustive
   `itertools.product` sweep test asserts exactly this property.
   `record_window_start` (window.py:136-142) sets only STARTED/clears RESET —
   never clears `window_interrupted_ts` → re-arm stays INTERRUPTED ✔.
   Engine wiring: `detect_interruption` runs at startup BEFORE the first
   `record_liveness` (engine.py start()), so a gap cannot be bridged by fresh
   liveness ✔. Engine-less `init_runtime_state` emits `no_store` → DOWN ✔.
   `window_status` store failure → DOWN + `store_unreadable` ✔.
10. **No-mutation** ✔ — in-suite snapshot test plus real-pair proof: P2RT
    porcelain empty and HEAD `008e065e` unchanged after my integration re-run.
11. **Existing-caller regression** ✔ — only three NEW test files added; no
    pre-existing test file touched; baseline 164 remain inside the 210.
12. **Task D** ✔ — all 12 ADR-0018..0029 headers `Status: Accepted`; the three
    claimed wording fixes verified in place (ADR-0018:56, ADR-0025:14,
    ADR_INDEX:53); `_AI_MEMORY/DECISIONS.md` newest entry is D017 (2026-07-18) —
    no build-session edit; the flagged stale sentence inside D016 exists as
    reported and was correctly left alone. Residual same-class wording → N4.

## Nits

- **N1 (release_evidence robustness / exit-code contract):** a re-signed
  manifest whose `hashes` field is not a dict passes the structural checks
  (the key check is guarded by `isinstance(..., dict)` and records nothing when
  the type is wrong, `release_evidence.py:165-168`) and a recomputed
  `integrity_sha256` passes the checksum, so live comparison hits
  `manifest["hashes"]["source_tree_hash"]` → uncaught `TypeError` → traceback,
  **exit 1** (contract promises 0/2/3). Reproduced via subprocess. Fails loud,
  never validates — but the exit-code contract is violated on adversarial
  input. Fix: `hashes` non-dict → `missing_field:hashes` (exit 2) or
  EvidenceError (exit 3).
- **N2 (denylist basename gap):** `prod.env` / `config.env` are not matched by
  the secret denylist and would be opened+hashed if ever placed inside
  `IBKR_PAPER_BRIDGE/config/`. Exposure is digest-only. Either extend the
  pattern with `.*\.env$` or record the current scope as accepted in
  `RUNTIME_BASELINE_CONTRACT.md`.
- **N3 (handoff doc stale expectation):** `FABLE_TSP0_AUDIT_HANDOFF` §Integration
  re-run expects `source_tree_hash_equal: true` and exactly two drift reasons —
  that was true at the Task A commit only. At final HEAD the correct result is
  THREE reasons including `source_tree_hash_mismatch` (Task C's
  engine.py/routes.py/window.py legitimately differ from P2RT@`008e065e`).
  Tool behavior is correct; the handoff expectation is stale. This report is
  the correction of record.
- **N4 (TS-P0-004 incomplete wording sweep):** three residual present-tense
  "Proposed status …" sentences remain in rationale prose (ADR-0020:62,
  ADR-0025:51, ADR-0029:49) — same inconsistency class as the three fixed.
  Headers + ratification lines govern, so the record is consistent at the
  authoritative level, but the closure report's "now consistently reflects the
  ratified D016 state" overstates. Follow-up: one docs-only wording pass.
- **N5 (note, no action):** symlink-in-scope hashing yields a digest oracle of
  the target file; acceptable given Windows symlink privileges — worth one line
  in the contract's attack-surface list.

## Per task

| Task | Verdict |
| --- | --- |
| TS-P0-001 `fa449ce2` | **PASS** (N2, N5 notes) |
| TS-P0-002 `42d0ca9f` | **PASS-WITH-NITS** (N1) — contract itself stays DRAFT pending Barış |
| TS-P0-003 `7777273f` | **PASS** — no findings; core never-false-active property verified in code and by sweep |
| TS-P0-004 docs-only | **PASS-WITH-NITS** (N4) |

## Boundaries kept by this audit

No push/PR/merge, no deploy, no P2RT write (read-only git/file access only; even
the optional status GET was skipped), no ARM/DISARM, no scheduler/DB action, no
dependency additions, protected scopes untouched, main worktree never
cleaned/reset. TSP0 mutations were move-aside/restore only; final porcelain clean.

## Unblocked for Barış (unchanged from build report)

1. TS-P0-001 hash-scope confirm (fold N2 decision into it).
2. TS-P0-002 release-evidence contract approval (fold N1 fix first or accept as
   follow-up).
3. TS-P0-003 reset-policy confirm.
Push/PR of `feature/ts-p0-baseline` stays gated on Barış after (optionally) the
Codex cross-audit.
