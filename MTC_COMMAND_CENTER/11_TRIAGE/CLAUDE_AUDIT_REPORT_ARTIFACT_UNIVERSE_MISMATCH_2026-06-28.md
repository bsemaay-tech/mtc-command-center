# Claude Audit Report — Artifact Contract Universe-Mismatch Boolean (NEXT_STEPS 11e)

**Auditor:** Claude Opus 4.8
**Date:** 2026-06-28
**Scope:** Codex patch making `provenance.universe_mismatch` a strict boolean in the
profile-result converter + read model, with a separate human-readable
`universe_mismatch_reason`, preserving backward compatibility with legacy artifacts.

---

## 1. Verdict

**PASS WITH NITS**

The core change is correct, minimal, backward-compatible, and well-tested. All validation
commands pass (22 targeted tests + 87 full-suite tests, both `OK`). The only deductions are
(a) an out-of-scope `styles.css` change present in the working tree that is unrelated to this
item, and (b) a minor missing reader test for the new-boolean passthrough path. Neither
affects correctness of the universe-mismatch logic.

---

## 2. Findings (ordered by severity)

### NIT-1 — Out-of-scope file in working tree: `apps/web/styles.css`
`styles.css` is modified in the working tree but is **not** in the declared intended-file set
for item 11(e). The diff is a pure cosmetic theming swap (`var(--faint)` → `var(--muted)`)
across ~10 unrelated selectors (`.value-muted`, `.empty-cell`, `.score-chip.na`,
`.si-gate-cell .val.locked`, `.rail-row .v.locked`, `.subscore .pts.absent`,
`table.matrix .cell-empty`, `.artifact-item .a-state.plan`, `.empty-state`, badge). It has
nothing to do with universe-mismatch and is almost certainly bleed-over from the parallel
IMPECCABLE UI pilot. **Recommendation:** commit `styles.css` separately from the 11(e)
artifact-contract work so the two changes have clean, independent history. No code defect.

### NIT-2 — No reader test for the new-boolean passthrough preserving reason
`test_night_artifacts_reader.py` adds a good legacy-string normalization test, but there is no
reader-level test asserting that a *new* artifact (`universe_mismatch: true` +
`universe_mismatch_reason: "..."`) passes through with both fields intact. The converter test
covers boolean emission, and `_normalize_profile_provenance` handles the bool branch via
`setdefault`, so behavior is correct — but a direct reader assertion would close the loop.
Low priority.

### Observations (no action required)
- `_normalize_profile_provenance` correctly returns a **copy** (`dict(provenance)`); source
  artifact dicts are not mutated, satisfying the "no rewriting artifact files" requirement.
- `setdefault("universe_mismatch_reason", ...)` preserves a pre-existing reason rather than
  clobbering it — correct precedence.
- Frontend `profileRowFlags` keeps a string fallback (`typeof prov.universe_mismatch === "string"`),
  so it renders correctly for both reader-normalized (bool) rows and any raw legacy artifact
  read directly. Defensive and correct.
- Converter `build_document` note generation switched to
  `m["provenance"].get("universe_mismatch_reason")` guarded by `.get("universe_mismatch")`,
  so the human-readable note text is preserved.

---

## 3. Audit questions — answers

1. **Converter emits boolean + reason text?** YES. `map_row` sets
   `universe_mismatch: bool(mismatch_reason)` and `universe_mismatch_reason: mismatch_reason`
   (`build_profile_result_artifact.py:153-154`). Helper renamed `_universe_mismatch` →
   `_universe_mismatch_reason`.
2. **Reader normalizes legacy string without rewriting files?** YES.
   `_normalize_profile_provenance` (`night_artifacts_reader.py:286-308`) maps string→`True`,
   sets reason from the string, operates on a copy; handles bool and other-type branches too.
3. **Frontend shows flags + detail for both new and legacy artifacts?** YES.
   `profileRowFlags` (`app.js:1675-1681`) derives `mismatchReason` from `universe_mismatch_reason`
   or a string fallback, and sets `universeMismatch = prov.universe_mismatch === true || !!mismatchReason`.
4. **Backward-compatible with existing `backtest_profile_result.json`?** YES. Verified against
   the real legacy artifact at
   `03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json`,
   which stores `universe_mismatch` as a string and has no `_reason` field. Reader normalizes it
   to `True` + reason text; file is not modified.
5. **Tests adequate?** MOSTLY. Converter tests now assert `is True` + reason substring; reader
   adds a legacy-string normalization test. See NIT-2 for the one missing reader case.
6. **Avoided protected scopes?** YES. No schemas, no result-artifact rewrites, no backtest
   execution, no Pine/MTC_V2/parity/broker/execution, no scorecard semantics, no trading logic.
   Only the 6 intended files changed (+ the unrelated `styles.css`, NIT-1). Reader does not
   write to disk.
7. **Validation commands pass?** YES. See section 4.

---

## 4. Commands run and results

```
git status --short --branch
  -> master...origin/master [ahead 1]; 6 intended files + styles.css (out-of-scope) +
     handoff files modified; 2 untracked triage docs.

python -m py_compile build_profile_result_artifact.py night_artifacts_reader.py
  -> PY_COMPILE_OK

node --check apps/web/app.js
  -> NODE_CHECK_OK

PYTHONPATH=. python -m unittest tests.test_build_profile_result_artifact tests.test_night_artifacts_reader
  -> Ran 22 tests ... OK

PYTHONPATH=. python -m unittest discover tests
  -> Ran 87 tests in 43.641s ... OK
```

Legacy artifact shape verified:
```
grep universe_mismatch <legacy backtest_profile_result.json>
  -> "universe_mismatch": "strategy id implies US equities universe but soak symbol is XRPUSDT; ..."
     (string; no universe_mismatch_reason key) -> normalized to True + reason by reader.
```

---

## 5. Fixes applied

None. Read-only audit. No staging, commits, branches, or destructive git operations performed.

---

## 6. Protected-scope confirmation

CONFIRMED. The patch does not touch `*.pine`, `MTC_V2`, parity, `06_SCHEMAS`, broker/live/paper
execution, backtest engines, `top_results.json`, or scorecard/trading semantics. No artifact
files are rewritten (reader normalizes in-memory on a copy). The only deviation from the
declared file set is the unrelated cosmetic `styles.css` change (NIT-1), recommended to be
committed separately.
