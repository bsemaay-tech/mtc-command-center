# Lane Q — fail-closed CSV row repair in registry_reader (D15)

Scope: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py`
(`_candidate_csv_row` / `_read_candidate_csv`), test file
`MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_registry_reader.py`. Follow-up to
Lane K's finding #7 (`OVERNIGHT_LANE_K_NONPROTECTED_STATIC_HUNT_2026-09-07.md`, lines
156-181): `_candidate_csv_row` repairs malformed CSV rows (unquoted commas in
`mtc_overlap`) with a fixed `fields[:12] + join(fields[12:-4]) + fields[-4:]` split, then
`zip(header, repaired)` unconditionally — if the repair does not land on exactly
`len(header)` columns (e.g. the registry CSV's header has drifted from the 17-column,
12-leading/4-trailing shape the split assumes), `zip` silently truncates/misaligns instead
of raising, and the dashboard would show a row with dropped or shifted columns with no
warning.

## Fix

Fail closed the same way the rest of this reader already treats malformed input (both
`_read_candidate_jsonl` and `_read_promoted_strategies` `continue`/skip a record they can't
parse rather than emit a guessed value): when the repaired row's length doesn't match the
header's length, `_candidate_csv_row` now returns `None`, and `_read_candidate_csv` skips
that row (`continue`) instead of calling `_candidate_from_row` on a `None`. Rows that repair
to exactly `len(header)` columns are unaffected — same output as before. No output schema
change; `build_strategy_registry`'s payload shape is untouched.

```diff
diff --git a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py
index df7d6c3d..52921d3e 100644
--- a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py
+++ b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py
@@ -56,6 +56,10 @@ def _read_candidate_csv(path: Path, quantlens_root: Path) -> list[dict[str, Any]
         header = next(reader, [])
         for fields in reader:
             row = _candidate_csv_row(header, fields)
+            if row is None:
+                # Malformed row whose repair didn't land on the header's
+                # column count: fail closed rather than zip a misaligned row.
+                continue
             candidates.append(_candidate_from_row(row, path, quantlens_root))
     return candidates
 
@@ -177,7 +181,7 @@ def _normalize_source_url(value: Any) -> str:
     return url
 
 
-def _candidate_csv_row(header: list[str], fields: list[str]) -> dict[str, Any]:
+def _candidate_csv_row(header: list[str], fields: list[str]) -> dict[str, Any] | None:
     if len(fields) <= len(header):
         return dict(zip(header, fields))
 
@@ -186,6 +190,12 @@ def _candidate_csv_row(header: list[str], fields: list[str]) -> dict[str, Any]:
     repaired = fields[:12]
     repaired.append(",".join(field.strip() for field in fields[12:-4]))
     repaired.extend(fields[-4:])
+    if len(repaired) != len(header):
+        # The repair didn't land on the header's shape (e.g. the header has
+        # drifted from the 12-leading/4-trailing layout this split assumes).
+        # Fail closed instead of zipping a row that would silently drop or
+        # misalign columns.
+        return None
     return dict(zip(header, repaired))
```

## Tests added (D026)

Added to the existing `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_registry_reader.py`
(imports `_candidate_csv_row` alongside `build_strategy_registry`):

1. `test_csv_row_repair_mismatched_column_count_is_rejected` — direct unit test:
   a 20-column header (17-column schema plus 3 drifted trailing columns) with a
   21-field malformed row (unquoted comma inside `mtc_overlap`) enters the repair
   branch; the fixed 12+1+4 split always yields 17 columns, which can never match a
   20-column header. Asserts `_candidate_csv_row(header, fields) is None`.
2. `test_reads_candidate_csv_skips_row_whose_repair_does_not_match_header` —
   full-pipeline regression via `build_strategy_registry` on a temp CSV with the same
   20-column header, one good row (`QL_GOOD`) and one malformed row (`QL_BAD`, reviewer
   name `alice`). Asserts only `QL_GOOD` is present, `QL_BAD` is absent, and `"alice"`
   (the malformed row's reviewer value) never leaks into any surviving candidate's
   field values — before the fix it leaked into `candidate_folder` of the `QL_BAD`
   candidate that was wrongly emitted.
3. `test_reads_candidate_csv_row_that_repairs_cleanly` — positive test: the original
   17-column header with an 18-field row (unquoted comma inside `mtc_overlap`) still
   repairs to exactly 17 columns and parses correctly (`candidate_id == "QL_REPAIR"`,
   `notes == "next-step"`), confirming the fix does not regress the already-working
   repair path.

### RED (before the fix — captured, then discarded after the fix was applied)

```
self.assertGreater(len(fields), len(header))
>       self.assertIsNone(_candidate_csv_row(header, fields))
E       AssertionError: {'candidate_id': 'QL_BAD', 'status': 'PROTOTYPED', 'title': 'Bad',
'source_url': '', 'market_type': 'CRYPTO', 'timeframe': '1h', 'candidate_kind':
'entry|exit', 'commercial_value_score': '5', 'complexity_score': '2', 'repaint_risk':
'LOW', 'lookahead_risk': 'LOW', 'closed_source_risk': 'LOW', 'mtc_overlap':
'oops,unquoted comma here,next,folder,2026-05-01', 'next_action': '2026-05-30',
'candidate_folder': 'alice', 'created_at': 'ok', 'updated_at': 'false'} is not None

tests/test_registry_reader.py:90: AssertionError
_ RegistryReaderTests.test_reads_candidate_csv_skips_row_whose_repair_does_not_match_header _
            registry_payload = build_strategy_registry(root)
            candidate_ids = [c["candidate_id"] for c in registry_payload["candidates"]]
>           self.assertEqual(candidate_ids, ["QL_GOOD"])
E           AssertionError: Lists differ: ['QL_GOOD', 'QL_BAD'] != ['QL_GOOD']
E
E           First list contains 1 additional elements.
E           First extra element 1:
E           'QL_BAD'
E
E           - ['QL_GOOD', 'QL_BAD']
E           + ['QL_GOOD']

tests/test_registry_reader.py:127: AssertionError
=========================== short test summary info ============================
FAILED tests/test_registry_reader.py::RegistryReaderTests::test_csv_row_repair_mismatched_column_count_is_rejected
FAILED tests/test_registry_reader.py::RegistryReaderTests::test_reads_candidate_csv_skips_row_whose_repair_does_not_match_header
2 failed, 3 passed in 0.07s
```

Note the pre-fix output above is itself the proof of the bug Lane K flagged: `alice`
(the malformed row's `reviewer` field) leaked into the wrongly-zipped candidate's
`candidate_folder` field — a real misaligned-column leak, not a hypothetical one.

### GREEN (after the fix)

`tests/test_registry_reader.py` only:
```
.....                                                                    [100%]
5 passed in 0.04s
```

Full dashboard suite from `apps/api`:
```
....................................................................... [ 56%]
......................................................                   [100%]
125 passed, 1 subtests passed in 4.17s
```
(122 baseline + 3 new tests = 125; baseline confirmed green before this change with the
same command.)

## Lint / diff hygiene

- `ruff check --isolated --no-cache --select E9,F821,F811` on both changed files:
  `All checks passed!`
- `git diff --check` on both changed files: clean (no trailing-whitespace/conflict-marker
  issues).

## Deviations from Lane K's illustrative diff

Lane K's finding #7 sketched `return dict(zip(header, fields))  # give up on repair,
fall back to raw truncation` as a possible minimal diff. That fallback is itself an
unchecked `zip` of two different-length sequences (raw `fields` against `header`) and
would reintroduce the same silent truncation/misalignment class of bug for any row where
`len(fields) != len(header)` — which is guaranteed true here since this branch is only
reached when `len(fields) > len(header)`. Implemented `return None` + skip instead,
matching the fail-closed pattern this reader already uses for other malformed records
(`_read_candidate_jsonl` and `_read_promoted_strategies` both skip unparseable/wrong-type
records rather than emit a best-effort guess).

## NEXT ACTION

None required for this fix; it is complete and merged into this worktree's history. A
related but out-of-scope observation from Lane K (finding #8, BOM handling) still applies
to `pipeline_reader.py`/`audit_reader.py`/`optimization_reader.py`/`backtest_reader.py`,
which Lane P owns — not touched here.

## WAITING FOR OWNER

Nothing.
