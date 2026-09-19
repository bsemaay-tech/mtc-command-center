# GROK_V15_REPORT — GK20D detection pre-screen of P0-20 preselection V1.5

Auditor: grok-4.6. Supplemental only. This report cannot accept the package and does not
replace exact claude-opus-5 / gpt-5.6-sol reviewers.

Subject: scratch copy of `C:/tmp/P020_PRESELECT_20260913/` at
`C:/tmp/GROK_SCRATCH_GK20D_20260914/pkg/`, with the benchmark dir and derivation dir beside
it. Worked only there except read-only identity runs of the *pinned* live driver/plan
(`C:/tmp/P020_LEAD_20260912/benchmark/`), whose bytes are identical to the scratch copies.
No git command. No network. No `--i-have-t0-review-authorization` token that matches the
frozen digest. `--oneshot` invoked only without a token and with a wrong token, to observe
refusal. `run_bounded_benchmark.py --run` was not invoked.

`PRESELECTION_FROZEN.json` SHA-256 (scratch copy, pinned interpreter):
`b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` — MATCH to the brief
(21 417 bytes, V1.5). All eleven `SHA256SUMS.txt` rows matched. `procedure_code_sha256` in
that artifact equals the SHA-256 of the delivered `preselect_profile.py`:
`54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877`.

pytest (cwd scratch package, pinned interpreter, `-p no:cacheprovider`): **96 passed**
(builder count in `REPORT_R6.md` was 96). Live pinned benchmark tests: **5 passed**.
Scratch derivation tests: **15 passed**.

---

## Closure table

| finding | CLOSED / NOT CLOSED / PARTLY | file:line evidence |
| --- | --- | --- |
| (0) Real-stack instrument interval (the round-4 miss) | CLOSED | V2 `EconomicRecords.from_record_paths` + `for_evaluation(ts, records.runtime_instrument_config or {})` accepted **40/40** first and last timestamps of all five calibration windows and all fifteen measurement prefixes; every timestamp matched the frozen `first_ts`/`last_ts`. V1 control `2025-09-22T08:00:00Z` refused `REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE`. `--freeze` on a scratch plan pointing at a V1-ended record refused `PRESELECT_REFUSED_RECORD_INTERVAL: calibration 15m first_ts outside instrument record interval` (exit 2, no frozen file written). `verify_frozen_record_interval` (`preselect_profile.py:232-253`) is called from `verify_frozen_identity:628` before `reserve_outputs` (`cmd_oneshot:1185-1186`); the same outside-window case refused before reservation with `reserve_calls=[]` and no output files. |
| (0) Other `_records` / `_build_profile` input preconditions | CLOSED (listed; `test_only` is not a precondition) | `_records:311-344`: `from_record_paths` (sidecar + exact-byte JSON via `load_verified_json_record`), digest match vs `plan["p020_profile"]["records"][*]["sha256"]`, `instrument.symbol == "SYNTH-RULE2-01-GREEN"`, cost/funding `symbol_scope` the same. `_build_profile:351-354`: `for_evaluation(frame timestamp, records.runtime_instrument_config or {})`; owner-cap equality; row-9 unset. Frozen V2 instrument digest/symbol match; cost/funding digests and `symbol_scope` match. `test_only` is present on the three JSON records but is **not read** by `_records`, `_build_profile`, or `load_verified_instrument_record`. Driver never passes `runtime_instrument_config` into `from_record_paths`, so evaluation uses `{}`. |
| (0b) D5 driver family-set | CLOSED (behaviour); PARTLY (byte-diff vs `4b293de6`) | `_validate_plan:181-196`: no-`derivation` keeps the original five-name set; `derivation.family_order` accepts any five distinct `strategy_id`s subset of that list. Driver source contains no `PRESELECTION_FROZEN`. Live `--validate-plan` prints `PLAN_VALID`. Live `tests/test_validate_plan_family_set.py`: **5 passed** (original five; any five frozen families; outside-order refuse; duplicate refuse; wrong-size refuse). Hand-written plan has no `derivation` key. Mechanical revert of RECORD_PATHS V2→V1 plus the derivation branch did **not** restore digest `4b293de6…` (see Commands); inspection of `_validate_plan` shows no other new check. |
| (0c) Derivation tool | CLOSED | `load_json_once:30-39` one `read_bytes`, digest of that buffer, `json.loads` of that buffer. Swap probe: parsed object + recorded digest stayed on the original bytes after the on-disk file was replaced. `EXPECTED_FROZEN_SHA256:12` = V1.5 `b75489841a09…`. `derivation.family_order` emitted at `:167`. `strategy_family` = `strategy_id` at `:134`. `REFUSED_SELECTION_FAMILY_NOT_FROZEN` at `:99`. Tests include single-read, malformed, non-object, frozen-file-vs-pin (`tests/test_derive_benchmark_plan.py:233-298`). 15 passed. |
| (0d) N4-1 citations | CLOSED | `PRESELECTION_PREREG_V1.md:47-48` marks V1.4 changelog line numbers historical; function names authoritative. §(d)/(e)/(g) name `verify_frozen_identity`, `dataset_lines`, `frame_from_lines`, `trade_bearing_gate`, `lexicographic_first_matching`. Residual stale numbers remain in the body (see findings). |
| (0d) N4-2 truncate in commit | CLOSED | `ReservedOutputs.commit:664,667` `handle.truncate()` after each successful write. Test `test_successful_commit_truncates_after_each_write` (`tests/test_preselect.py:1424`). Runbook `:108` “exclusive create, not an exclusive lock”. |
| (0d) N4-3 per-handle abort + doc sentence | CLOSED | `abort:677-697` per-handle try/except so one failed ABORTED write cannot skip the other. `test_abort_is_best_effort_per_handle:1436`. Runbook phase table `:173` names “abort recovery is best-effort per handle”. |
| (0d) N4-4 `prereg_sha256` / `runbook_sha256` / `procedure_code_sha256` | CLOSED | `build_freeze:873-877` computes the three digests LAST. `verify_frozen_identity:578-590` re-checks them. Frozen artifact carries all three; `procedure_sha256` is gone (V1.4-only key). |
| (0d) Sol-4 runbook `-p no:cacheprovider` | CLOSED | `PRESELECT_RUNBOOK.md:32-33` (`PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`). |
| T1 (token hashes and parses the same frozen bytes; accepted digest carried into both outputs) | CLOSED | `require_t0_authorization:921-931`: one `read_bytes()`, `digest = sha256_bytes(raw)`, compare token, `return json.loads(raw), digest`. `cmd_oneshot:1184` unpacks `(frozen, accepted_digest)`. `_run_oneshot:1200` sets `frozen_sha256 = accepted_digest` into both records (`:1228`, `:1257`). `_run_oneshot` body has no `read_bytes` / `open(` / `FROZEN_PATH`. PROBE 1: swap after the accepted read left both outputs on the original digest and original selection. |
| T2 (verified plan object is the object executed; no post-preflight plan reload) | CLOSED | `verify_frozen_identity:591-596` reads `PLAN_PATH` once, hashes, `json.loads(plan_raw)`, returns it. `cmd_oneshot:1185-1188` passes that object into `_run_oneshot`. `trade_bearing_gate:1070` calls `driver._profile(..., plan)`. `load_plan()` exists at `:481-482` and is called only from `build_freeze:727`. PROBE 7: `_run_oneshot` has no `load_plan(` / `open(` / `read_text` / `read_bytes`. PROBE 2: plan mutated to `POST_PREFLIGHT` at reservation time; every `_profile` saw `PREFLIGHT`. |
| T3 (commit failure → both reserved files `ABORTED`; handles stay open; nothing deleted) | CLOSED | `commit:660-675` writes, truncates, flushes both while handles remain; `except` calls `abort`; `finally` closes. `abort:677-697` seek/truncate/write ABORTED/flush/close per handle. No `unlink` / `os.remove` in `preselect_profile.py`. PROBES 3–5: first-write, second-write, and flush failures each left **both** files `ABORTED`, neither deleted, no mixed payload/`ABORTED` pair. |
| T4 (runbook + prereg split outcomes by phase) | CLOSED | `PRESELECT_RUNBOOK.md:164-173` three-phase table (before reservation / partial reservation / post-both-reservations). `PRESELECTION_PREREG_V1.md:520-524` states the same split. |
| S1 (single `--oneshot` transaction, no inter-command file) | CLOSED | `main:1283-1307`: only `--freeze` / `--oneshot`. `_run_oneshot:1206-1254` builds the matrix in memory, `lexicographic_first_matching` (`:1225`), `verified_selection` (`:1234`), then the 15 trials. No file read between matrix and trials. |
| S2 (exclusive-create reservation, ABORTED records, no overwrite path) | CLOSED | `ReservedOutputs.reserve:654` `open(path, "xb")`; `reserve_outputs:700-715`; called at `cmd_oneshot:1186` after identity preflight. Residual: Windows shared `open("w")` into the empty reserved file — see (f) and findings. |
| S3 (one read per dataset) | CLOSED | `verify_frozen_identity:618-627` reads each dataset once with `read_bytes()` and returns those bytes. `dataset_lines:980-992` opens no file. `_run_oneshot:1201-1204` builds `lines_by_timeframe` from those bytes. |
| S4 (`len(trades)` only, never iterate) | CLOSED | `trade_bearing_gate:1085-1089`: `hasattr(trades, "__len__")` then `trade_count = len(trades)`. No `list(trades)`. |
| S5 (runbook wording) | CLOSED | Dual-sided codes and BLOCKED as a recorded outcome at `PRESELECT_RUNBOOK.md:176-180`. Tightened by T4. |
| NIT-1 (assert_disjoint at consumption) | CLOSED | `calibration_frame:1000` calls `assert_disjoint` before slicing window bytes. Also still in `plan_calibration_window:344`. |
| NIT-4 (`procedure_*sha256` recorded and re-checked) | CLOSED | Superseded by N4-4: field renamed `procedure_code_sha256`, still hashed from one procedure byte read (`:578-581`) and re-checked before driver load. |
| R1 (shared binary gate, clauses of `_execute_trial`) | CLOSED | `trade_bearing_gate:1031-1099` is the only predicate; both stages call it (`:1215`, `:1248`). See (a). Driver line numbers shifted ~11 after D5; clauses themselves did not. |
| R2 (selection re-derived, never trusted) | CLOSED | `verified_selection:1102-1152` applied to the in-memory record (`:1234`) before the 15 trials. |
| R3 (one-shot mechanical) | CLOSED | Exclusive-create reservation + two-output commit (S2+T3). Residual unchanged: an operator who deletes the artifacts outside the tool can run again. |
| R4 (only isolated rows parsed) | CLOSED | `frame_from_lines:965-977` parses given bytes via `io.StringIO`. Calibration uses window rows (`:995-1004`); measurement uses prefix bytes (`:1007-1028`). |
| R5 (counts only; no R / extra stats) | CLOSED | Gate body has no `float(`, `asdict`, `json.dumps`, `sha256` of trades. Only `stats.num_trades` is read (`:1090`). |
| R6 (frozen pins re-verified before driver load) | CLOSED | `cmd_oneshot:1184-1188`: token → `verify_frozen_identity` (HEAD, procedure/prereg/runbook, plan, compatibility, manifest, source pins, five dataset SHA-256s, **record interval**) → reserve → `_run_oneshot` which is the first `load_driver()` (`:1197`). |
| (g) V1.4 → V1.5 selection-rule identity | CLOSED | Flattened frozen-JSON diff vs V1.4 `f839c960…`: `selection_rule`, `family_ordering_rule`, `canonicalization`, `family_order` strategy ids + canonical bytes + sha256, all window `start_row`/`end_row`/`row_count`/`sha256`, all 15 prefix `(input_rows, sha256)`, `timeframe_order`, `calibration_window_rule`, and `limitations` are EQUAL. Changed/added keys are only `artifact_version`, `supersedes`, `execution_identity_recheck`, plan/driver pins, `procedure_code_sha256`/`prereg_sha256`/`runbook_sha256`, `instrument_record_interval`, and `first_ts`/`last_ts`. Removed: `procedure_sha256`. |

---

## Specific checks (a)–(g)

### (a) `trade_bearing_gate` vs `_execute_trial:459-493`

Compared to current `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py` (the
`:459-493` citation is the V1.4 numbering; after D5 the copy clause sits at `:470` and the
function runs `:460-504`). Present, in order, with the same refusal texts and
`driver.BenchmarkProfileBlocked` type:

| V1.4 driver line | current driver | clause | gate |
| --- | --- | --- | --- |
| 459 copy | 470 `pd.read_csv(...).copy()` | `frame.copy()` | `:1057` |
| 460-463 | 471-474 | OHLC-only schema | `:1058-1061` |
| 464-466 | 475-477 | null OHLC | `:1062-1066` |
| 467-468 | 478-479 | `timestamp` / `date` | `:1067-1068` |
| 469 | 480 | `before_ohlc` `copy(deep=True)` | `:1069` |
| 470 | 481 | `driver._profile(...)` | `:1070` |
| 471-473 | 482-484 | `build_signals` | `:1071-1073` |
| 474-477 | 485-488 | mutation check | `:1074-1077` |
| 478 | 489 | `signals, stop = result[:2]` | `:1078` |
| 479-483 | 490-494 | identical `simulate_slice` kwargs | `:1079-1083` |
| 484 | 495 | `event_list = list(events)` | `:1084` |
| 486-489 | 497-500 | `num_trades <= 0 or not event_list or len(event_list) != trade_count` | `:1090-1094` |
| 490-493 | 501-504 | `projection_source == "COMMITTED_TRANSITION_LEDGER"` | `:1095-1099` |

Missing or substituted (none reordered; same two substitutions as V1.3/V1.4):

1. **Driver `:470` `pd.read_csv(data_path).iloc[:N]`** is not in the gate. The frame is already isolated by `frame_from_lines` (R4). The gate still copies it.
2. **Driver `:496` `trade_list = [float(value) for value in trades]`** is **absent** (R5/S4). Replaced by `hasattr` + `len(trades)` (`:1085-1089`).
3. **Extra clause** between event_list and the count check: unsized series → `BENCHMARK_PROFILE_BLOCKED` (`:1085-1088`).

R1 remains CLOSED. The frozen `eligibility_predicate.implemented_by` still says
“`_execute_trial:459-493`”; that citation is now stale by ~11 lines (NIT).

### (b) Selection-rule change V1.3 → V1.4?

No. `REPORT_R5.md` claims T1–T4 only. V1.4 frozen `f839c960…` vs V1.5 (this package) leaves
selection, family order, canonical bytes, windows, prefixes and the LIMITATION line untouched
(see (g)). `CALIBRATION_WINDOWS:109-121` is still 2049+2048 / 1D 2049+361. The freeze
LIMITATION line at `cmd_freeze:889-901` is still

`LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13`

(printed in `REPORT_R6.md` freeze tails).

### (c) Swapped `PRESELECTION_FROZEN.json` between token read and execution

No. PROBE 1 swapped the on-disk file (reversed `family_order`) during the one
`FROZEN_PATH.read_bytes`; execution used the original bytes and both output records carried
the original digest. `verify_frozen_identity` and `_run_oneshot` never re-open `FROZEN_PATH`.

### (d) Mutated `BENCHMARK_PLAN.json` after preflight reaching `_profile`

No on this package’s execution path. PROBE 2 mutated the plan file to `POST_PREFLIGHT`
inside a replacement `reserve_outputs`. All `_profile` calls received `marker=PREFLIGHT`.
Real `_profile` / `_records` consume the passed `plan` object; driver `_load_plan` is not
on the `--oneshot` path.

### (e) After a commit exception: mixed payload/`ABORTED`, or a deleted reserved file?

Not on the three specified failure modes. PROBES 3–5 each left **both** files present as
`ABORTED` / `error=OSError`. Second-write failure overwrote the already-flushed calibration
payload with `ABORTED`. No delete path exists in the procedure.

### (f) Windows shared-write NIT vs commit truncate

**UNCHANGED at reservation; leftover-after-successful-commit is MITIGATED; not worse.**

Reservation is still `open(path, "xb")` (`:654`): exclusive create, not an exclusive lock.
PROBE 6: after reservation both files exist at size 0; later `open(path, "x")` raised
`FileExistsError`; later `open(path, "w")` wrote `SENTINEL_W` into both empty reserved files
while the handles were still held; `commit` then overwrote both with the real payload.
Same observation as V1.3/V1.4.

PROBE 6b: a *longer* shared write, then a short successful `commit`. V1.5 `truncate()` after
each write left **no leftover sentinel bytes**. That leftover case is mitigated. The
reservation-window crash/sentinel-spend case is not.

### (g) Selection-rule change V1.4 → V1.5?

No, other than the allowed identity/interval fields. Flattened-key diff (V1.4
`C:/tmp/P020_PRESELECT_LEAD_REPRO_V14_20260913/PRESELECTION_FROZEN.json` vs this V1.5):

Unchanged (required): `selection_rule`; family ids and
`fixed_parameter_record_canonical` / `_sha256`; datasets; `timeframe_order`; calibration
window `start_row` / `end_row` / `row_count` / `sha256`; measurement prefix `input_rows` /
`sha256`; `limitations` / owner D1 Option A.

Changed or added: `artifact_version` v1.4→v1.5; `supersedes`; `execution_identity_recheck`
(now names `procedure_code_sha256`, prereg/runbook, interval); plan pin
`1d98291fe…` → `8cf52e3d2a91…`; driver pin `4b293de6c…` → `b8a8f2552a…`; new
`instrument_record_interval` and per-window/prefix `first_ts`/`last_ts`;
`procedure_code_sha256` / `prereg_sha256` / `runbook_sha256`. Removed: `procedure_sha256`.

---

## Findings table

| # | severity REQUIRED / NIT | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | NIT | `preselect_profile.py:654` (`ReservedOutputs.reserve`) | `open(path, "xb")` is an exclusive create, not an exclusive lock. PROBE 6: after reservation, `open(path, "w")` wrote `SENTINEL_W` into both empty reserved files while the handles were still held. Commit truncate (N4-2) then overwrote them; PROBE 6b shows leftover bytes after a *successful* commit are now gone. | S2’s original exists-then-write attack is closed, and T3 mixed-payload commit failure is closed. A concurrent shared write can still occupy the reserved empty file until the handle writes. A crash in that window still spends the one shot on sentinel bytes. Unchanged in kind from V1.3/V1.4; not worse. |
| 2 | NIT | `BENCHMARK_PLAN.json:305-308`; `SYNTH-P020-BOUNDED-COST-V1.json:2-4`; `SYNTH-P020-BOUNDED-FUNDING-V1.json:2-4`; `BENCHMARK_RUNBOOK.md:59` | Cost, funding, the plan’s `p020_profile.records.effective_interval`, and the runbook’s “valid for … through `2025-09-22T08:00:00Z` exclusive” sentence still describe the V1 measurement-prefix interval. Instrument V2 ends `2026-05-01T00:00:00Z`. The new freeze check reads only the instrument record (`instrument_record_interval:185-210`). `_records`/`_build_profile` do not consult cost/funding intervals. `p020_economics.py` has no `effective_interval` reference. | A reader of the plan/runbook can conclude the 15m calibration window (last_ts `2025-10-13T15:45:00Z`) is still out of range. The engine path that actually aborted V1.4 (`instrument.for_evaluation`) is covered. Whether some later economics helper would refuse cost/funding timestamps is untested (no simulation). |
| 3 | NIT | `tests/test_preselect.py:1808-1842` (`RealInstrumentRecordSmoke`) | The smoke arm calls `for_evaluation` only on each window **start** and on CSV row 1 (prefix first_ts), with a hardcoded `runtime_config`, not `records.runtime_instrument_config or {}`, and not last_ts / all 15 prefixes. | Weaker than the freeze/preflight check, which *does* record and re-check first and last of every window and every prefix (`:223-253`, `:766-773`). This lane independently accepted 40/40 with `runtime_config={}`. A regression on last_ts would not be caught by this test. |
| 4 | NIT | `PRESELECTION_PREREG_V1.md:240-247`; frozen `eligibility_predicate.implemented_by`; gate comments `:459-493` | N4-1 marked changelog line numbers historical (`:47-48`) and prefers function names, but §(d) still cites `preselect_profile.py:456-522` (now `verify_frozen_identity:549-629`) and the gate/frozen text still says `_execute_trial:459-493` (copy is now `:470`). | Function names are authoritative, so this is not a silent rule change. A reviewer who follows the leftover numbers lands in the wrong function. |
| 5 | NIT | `benchmark/tests/test_validate_plan_family_set.py:44` | The family-set tests stub sidecars and `_sha256_path` but not `RECORD_PATHS` vs the plan’s absolute instrument path. They pass only when the driver is loaded from `C:/tmp/P020_LEAD_20260912/benchmark/` (ROOT matches the plan). A copy of the driver (this scratch tree) fails 4/5 with `external instrument record path mismatch`; `test_wrong_sizes_are_refused` still “passes” because it only asserts the `SystemExit` *starts with* `PLAN_INVALID:`. | Live pinned suite is 5 passed, so the D5 behaviour is real. The tests are coupled to `__file__` location and one of them can false-pass on an earlier PLAN_INVALID. |

No REQUIRED findings.

---

## RED probes (scratch copy, synthetic only except detect-0 real-stack)

Scripts: `C:/tmp/GROK_SCRATCH_GK20D_20260914/pkg/probes/red_probes.py` and
`probes/detect_v15.py`. Pinned interpreter. No CLI token matching the real V1.5 digest.
`observed_impl_head` stubbed via the synthetic environment / explicit monkeypatch so git is
not invoked.

### DETECT 0 — real-stack `for_evaluation` (40 timestamps)

`EconomicRecords.from_record_paths` on the pinned V2 instrument + V1 cost/funding.
`runtime_instrument_config or {}` was `{}`.

```
OBSERVED V2_accepted=40 V2_refused=0
OBSERVED V1_CONTROL_REFUSE ts=2025-09-22T08:00:00Z code=REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE
OBSERVED V2_ACCEPTS_15m_WINDOW_START ts=2025-09-22T08:00:00Z
```

All 40 CSV timestamps matched the frozen `first_ts`/`last_ts`.

### DETECT 0 — `--freeze` with the window outside the interval

Scratch plan pointed at a copy of the instrument whose `end_exclusive` was moved back to
`2025-09-22T08:00:00Z` (the 15m calibration start). `observed_impl_head` stubbed to
`IMPL_HEAD`. `ps.main(["--freeze"])`:

```
PRESELECT_REFUSED_RECORD_INTERVAL: calibration 15m first_ts outside instrument record interval
OBSERVED freeze_returncode=2 frozen_exists=False
```

### DETECT 0 — `verify_frozen_record_interval` before reservation

```
OBSERVED verify_V2_interval PASS
OBSERVED verify_V1_plan_vs_V2_frozen code=PRESELECT_REFUSED_RECORD_INTERVAL detail=... instrument interval drift
OBSERVED verify_window_outside_V1 code=PRESELECT_REFUSED_RECORD_INTERVAL detail=... calibration 15m first_ts outside instrument record interval
OBSERVED oneshot_interval_before_reserve code=PRESELECT_REFUSED_RECORD_INTERVAL ... reserve_calls=[] cal_exists=False elig_exists=False
```

### DETECT 0c — derivation swap probe (digest of parsed bytes)

```
OBSERVED SWAP_PROBE_PASS=True
parsed_note=original digest=<original> on_disk=<swapped>
```

### PROBE 1 — swap frozen file after the accepted `read_bytes` (T1)

```
OBSERVED oneshot_returncode=0
OBSERVED cal_frozen_sha256=<original> elig_frozen_sha256=<original>
OBSERVED on_disk_digest=<swapped>
OBSERVED selection={'15m': 'GEN_A', '1D': 'GEN_E', '1h': 'GEN_B', '2h': 'GEN_C', '4h': 'GEN_D'}
OBSERVED PROBE1_PASS: swap after token read did not change executed frozen bytes or recorded digest
```

### PROBE 2 — mutate `BENCHMARK_PLAN.json` after preflight (T2)

```
OBSERVED oneshot_returncode=0
OBSERVED unique_markers=['PREFLIGHT']
OBSERVED on_disk_marker='POST_PREFLIGHT'
OBSERVED PROBE2_PASS: _profile saw verified preflight plan, not the mutated file
```

### PROBE 3 — first `write` raises (T3)

```
OBSERVED commit_raised=OSError:synthetic write failure
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE3_PASS
```

### PROBE 4 — second `write` raises (T3)

```
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE4_PASS
```

### PROBE 5 — `flush` raises (T3)

```
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE5_PASS
```

### PROBE 6 — Windows shared write into reserved empty files

```
OBSERVED exclusive_create_sentinel={'calibration': 'REFUSED_FileExistsError', 'eligibility': 'REFUSED_FileExistsError'}
OBSERVED shared_write_sentinel={'calibration': 'WRITE_SUCCEEDED', 'eligibility': 'WRITE_SUCCEEDED'}
OBSERVED SENTINEL_W_IN_FINAL=False
OBSERVED PROBE6_PASS: reservation-window shared-write NIT is UNCHANGED
```

### PROBE 6b — truncate vs leftover bytes

```
OBSERVED leftover_sentinel=False
OBSERVED PROBE6b_PASS: leftover after successful commit is MITIGATED by truncate
```

### PROBE 7 — static scan of `_run_oneshot`

```
OBSERVED _run_oneshot_forbidden_hits=[]
OBSERVED load_plan_in_module_at_freeze_only=True
OBSERVED PROBE7_PASS
```

Writes were under temp directories, not the package outputs. After all CLI refusals and
probes: `PRESELECTION_CALIBRATION.json` and `PRESELECTION_ELIGIBILITY.json` do not exist in
the scratch package directory.

---

## Commands run with observed output

Pinned interpreter:
`C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`
(present). Cwd for package commands: `C:/tmp/GROK_SCRATCH_GK20D_20260914/pkg`.

Copy of the package / benchmark / derivation dirs into scratch (PowerShell `Copy-Item`;
derivation `tmp/pytest-of-*` skipped on access denied).

Frozen digest:

```
SIZE 21417
SHA256 b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b
MATCH True
```

SHA256SUMS (scratch copy): all eleven rows `True`, including `REPORT_R6.md`.

Package pytest:

```
$ …python.exe -m pytest tests -q -p no:cacheprovider
........................................................................ [ 75%]
........................                                                 [100%]
96 passed in 2.82s
EXIT=0
```

Live pinned benchmark pytest (cwd `C:/tmp/P020_LEAD_20260912/benchmark`; scratch copy of the
same bytes fails RECORD_PATHS vs absolute plan paths — finding 5):

```
.....                                                                    [100%]
5 passed in 0.04s
EXIT=0
```

Derivation pytest (cwd scratch `derive`):

```
...............                                                          [100%]
15 passed in 0.17s
EXIT=0
```

`--validate-plan` (live pinned driver; identity only, `_run` not reached):

```
PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified
EXIT=0
```

`--oneshot` without a token (scratch package):

```
PRESELECT_REFUSED_NO_T0_REVIEW: --i-have-t0-review-authorization <sha256 of PRESELECTION_FROZEN.json> is required
EXIT=2
```

`--oneshot` with a wrong token (`0` × 64):

```
PRESELECT_REFUSED_T0_TOKEN_MISMATCH: token does not match the frozen artifact digest
EXIT=2
```

Neither invocation created `PRESELECTION_CALIBRATION.json` or `PRESELECTION_ELIGIBILITY.json`.

Driver identity:

```
live/scratch run_bounded_benchmark.py 30031 b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3
live/scratch BENCHMARK_PLAN.json 19814 8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448
derive_benchmark_plan.py 8865 d7bdfab90189d2364e0105436bd7b9dcf9be4ef906136d00e2dc0e64d4821c85
```

Mechanical revert of RECORD_PATHS V2→V1 plus the `_validate_plan` derivation branch produced
sha256 `54f90b5f352482f001774136789b3a53b5c4f5f07c4d553b9b329b0a8a62a8a9`, **not** V1.4
`4b293de6c26ae61ffec22c8205b81a1bad0c6561c0c642e19a37596b5fd62736`. The V1.4 driver bytes
were not present in the scratch tree (no git). Behavioural D5 claims were verified on the
live pinned file instead.

RED / detect probes: `…python.exe probes\detect_v15.py` and `probes\red_probes.py` — output
in the previous sections. EXIT=0.

Not run: any `--i-have-t0-review-authorization` token equal to the V1.5 digest; `--oneshot`
with a valid token; `run_bounded_benchmark.py --run`; a real `--freeze` that would invoke
`git rev-parse HEAD`; any git command.

---

## NOT VERIFIED

- **This is not a T0 review and cannot accept.** Exact claude-opus-5 and gpt-5.6-sol have not
  run on these V1.5 bytes in this lane. V1.4 Sol/Opus/Gemini results do not carry over; the
  V1.4 token is spent/dead.
- **Live `git rev-parse HEAD` was not observed** (brief: no git command of any kind). Code
  compares it to frozen `impl_head` `b9b72f858dc830a9389517f79da5ea3c1fa6122c` and to
  `IMPL_HEAD` at freeze time; the live repository was not checked here. `--freeze` interval
  refusal used a stubbed `observed_impl_head`.
- **The real driver/engine path has never been run end to end.** Gate equivalence, T1 swap,
  T2 plan carry-through, T3 commit abort, S2 reservation, S3 single-read, D5 family-set and
  the 40 `for_evaluation` calls are proven on doubles / synthetic CSVs / pure record loads.
  `_load_engine` / real `_profile` / real `simulate_slice` are unexercised. No 45-cell
  calibration, no 15 locked trials, no eligibility result.
- **Byte-for-byte `_validate_plan` vs V1.4 digest `4b293de6…` was not reconstructed.** The
  two intended edit sites are visible; a mechanical revert did not restore that digest. Every
  other check inside current `_validate_plan` is present by inspection; the current
  hand-written plan validates.
- **Cost/funding `effective_interval` is not an `_records`/`_build_profile` precondition**
  and was not exercised. `p020_economics.py` has no `effective_interval` hit. A later helper
  that started checking those V1 end dates during `simulate_slice` is therefore untested.
- **Two-process reservation race was not launched.** Exclusive-create was probed in-process.
- **If `ReservedOutputs.abort` itself fails mid-loop**, `first_error` is stored and never
  re-raised (`:690-697`); `commit`’s `finally` may close remaining handles. Nested abort
  failure is untested beyond `test_abort_is_best_effort_per_handle` (calibration seek fails,
  eligibility still ABORTED).
- **Worktree cleanliness** of `C:/P020_IMPL_20260912` is unverified. `check_p020_acceptance.py`
  was not opened.
- **Bar quality inside windows** (monotonicity, gaps, duplicates) was not audited. The 161
  usable 1D bars remain arithmetic, not an observed trade count.
- **Eligibility-handle flush failure** was not separately injected; it shares the same
  `commit`/`abort` path as PROBE 5 / PROBE 4.

This report is a supplemental detection pre-screen only. It is not a review, not acceptance,
and not authorization to execute.

GROK_V15_VERDICT: NITS
