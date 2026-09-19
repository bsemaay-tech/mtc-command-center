# GROK_V14_REPORT — GK20C detection pre-screen of P0-20 preselection V1.4

Auditor: grok-4.6. Supplemental only. This report cannot accept the package and does not
replace exact claude-opus-5 / gpt-5.6-sol reviewers.

Subject: scratch copy of `C:/tmp/P020_PRESELECT_20260913/` at
`C:/tmp/GROK_SCRATCH_GK20C_20260914/pkg/`. Worked only there. No git command. No network.
No `--i-have-t0-review-authorization` token that matches the frozen digest. `--oneshot`
invoked only without a token and with a wrong token, to observe refusal.
`run_bounded_benchmark.py --run` was not invoked.

`PRESELECTION_FROZEN.json` SHA-256 (scratch copy, pinned interpreter):
`f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff` — MATCH to the brief
(18 968 bytes). `procedure_sha256` in that artifact equals the SHA-256 of the delivered
`preselect_profile.py`: `c2d435251e58fe372bf422e7f68b81cd9d95e9a1c2c7c720e0c6fbffb664a3af`.
All ten `SHA256SUMS.txt` rows matched.

pytest (cwd scratch copy, pinned interpreter, `-p no:cacheprovider`): **90 passed**.

---

## Closure table

| finding | CLOSED / NOT CLOSED / PARTLY | file:line evidence |
| --- | --- | --- |
| T1 (token hashes and parses the same frozen bytes; accepted digest carried into both outputs) | CLOSED | `require_t0_authorization:799-809`: one `frozen_path.read_bytes()`, `digest = sha256_bytes(raw)`, compare token to that digest, `return json.loads(raw), digest`. `cmd_oneshot:1062` unpacks `(frozen, accepted_digest)`. `_run_oneshot:1078` sets `frozen_sha256 = accepted_digest` and writes it into both records (`:1106`, `:1135`). `verify_frozen_identity` does not re-open `FROZEN_PATH`. `_run_oneshot` body contains no `read_bytes` / `json.loads` / `open(`. PROBE 1: after the accepted read, the on-disk frozen file was swapped (including reversed `family_order`); both outputs still recorded the original digest and executed the original selection. |
| T2 (verified plan object is the object executed; no post-preflight plan reload) | CLOSED | `verify_frozen_identity:489-494` reads `PLAN_PATH` once (`plan_raw = PLAN_PATH.read_bytes()`), hashes that buffer, `verified_plan = json.loads(plan_raw)`, returns it. `cmd_oneshot:1063-1066` passes that object into `_run_oneshot`. `trade_bearing_gate:948` calls `driver._profile(trial, frame, modules, plan)` with that same object. `load_plan()` exists at `:388-389` and is called only from `build_freeze:616` (freeze path). Static scan of `_run_oneshot` (PROBE 7): no `load_plan(` / `open(` / `read_text` / `read_bytes`. Real driver `_load_plan` (`run_bounded_benchmark.py:85-92`) is called only from driver `main:671` (`--validate-plan` / `--run`), which this path never invokes; real `_profile:430-438` uses the passed `plan` argument. PROBE 2: plan file mutated to `POST_PREFLIGHT` at reservation time; every `_profile` call saw `PREFLIGHT`. |
| T3 (commit failure → both reserved files `ABORTED`; handles stay open; nothing deleted) | CLOSED | `ReservedOutputs.commit:557-570` writes and flushes both payloads while both handles remain in `self.handles`; they are popped and closed only in `finally` after success, or by `abort` on failure. `except BaseException` calls `abort:572-586` which `seek(0)` / `truncate(0)` / writes `ABORTED` / `flush` / close for every remaining handle. No `unlink` / `os.remove` / `Path.unlink` anywhere in `preselect_profile.py`. PROBES 3–5: first-write, second-write, and flush failures each left **both** files as `ABORTED` with `error=OSError`, neither deleted, no mixed real-payload + `ABORTED` pair. |
| T4 (runbook + prereg split outcomes by phase) | CLOSED | `PRESELECT_RUNBOOK.md:164-172` table: before any reservation / partial reservation failure / post-both-reservations transaction failure, with file residue. Normal recorded outcomes at `:174-179`. `PRESELECTION_PREREG_V1.md:510-516` states the same three-phase split. |
| S1 (single `--oneshot` transaction, no inter-command file) | CLOSED | `main:1163-1171`: only `--freeze` / `--oneshot`. `cmd_calibrate` / `cmd_eligibility` / `refuse_existing_output` absent. `_run_oneshot:1084-1131` builds the matrix in memory, `lexicographic_first_matching` on that set (`:1103`), `verified_selection` on the in-memory record (`:1112`), then the 15 trials. No file read between matrix and trials. |
| S2 (exclusive-create reservation, ABORTED records, no overwrite path) | CLOSED | `ReservedOutputs.reserve:549-555` `open(path, "xb")`; `reserve_outputs:597-602` both paths; called at `cmd_oneshot:1064` after identity preflight and before `_run_oneshot` / `load_driver` / any `simulate_slice`. Final payloads through `commit:557-570` / `:1147`. `except BaseException` → `abort` (`:1067-1069`, `:572-586`). Residual: Windows shared `open("w")` into the empty reserved file — see findings table and (f). |
| S3 (one read per dataset) | CLOSED | `verify_frozen_identity:516-526` reads each dataset once with `read_bytes()` and returns those bytes. `dataset_lines:858-870` opens no file. `_run_oneshot:1079-1082` builds `lines_by_timeframe` from those bytes. |
| S4 (`len(trades)` only, never iterate) | CLOSED | `trade_bearing_gate:963-967`: `hasattr(trades, "__len__")` then `trade_count = len(trades)`. No `list(trades)` / `float(value) for value in trades`. |
| S5 (runbook wording) | CLOSED | Tightened by T4. Dual-sided codes named at `PRESELECT_RUNBOOK.md:184-187`. BLOCKED trials are a recorded outcome (`status=BENCHMARK_PROFILE_BLOCKED`, exit 2) at `:174-179`; no-matching is ABORTED (post-both-reservations). `PRESELECT_REFUSED_NO_CALIBRATION` absent. |
| NIT-1 (assert_disjoint at consumption) | CLOSED | `calibration_frame:876-878` calls `assert_disjoint(window["start_row"], window["end_row"])` before slicing window bytes. Also still in `plan_calibration_window:251`. |
| NIT-4 (`procedure_sha256` recorded and re-checked) | CLOSED | `build_freeze:752-755` records `procedure_sha256 = sha256_path(PROCEDURE_PATH)` last. `verify_frozen_identity:484-487` hashes `PROCEDURE_PATH.read_bytes()` once and refuses `PRESELECT_REFUSED_SOURCE_DRIFT` with detail `preselect_profile.py`. Frozen value matches live file. |
| R1 (shared binary gate, clauses of `_execute_trial:459-493`) | CLOSED | `trade_bearing_gate:909-977` is the only predicate; both stages call it (`:1093`, `:1126`). See specific (a) for the two intentional substitutions at driver `:459` / `:485`. |
| R2 (selection re-derived, never trusted) | CLOSED | Handoff file is gone (S1). `verified_selection:980-1030` is still applied to the in-memory record about to be written (`:1112`) before the 15 trials. |
| R3 (one-shot mechanical) | CLOSED | Superseded and tightened by S2 + T3: exclusive-create reservation and two-output commit, not `exists()` + later `write_text`. Residual unchanged in kind: an operator who deletes the artifacts outside the tool can run again. |
| R4 (only isolated rows parsed) | CLOSED | `frame_from_lines:843-855` parses given bytes via `io.StringIO`. `pd.read_csv(path)` of a whole dataset does not appear on any execution path. Calibration uses window rows (`:873-882`); measurement uses prefix bytes (`:885-906`). |
| R5 (counts only; no R / extra stats) | CLOSED | Gate body has no `float(`, `asdict`, `json.dumps`, `sha256`, `print(`, `trade_series`. Only `stats.num_trades` is read from `SliceStats` (`:968`). `--calibrate` / `--eligibility` do not exist. |
| R6 (frozen pins re-verified before driver load) | CLOSED | `cmd_oneshot:1062-1066`: token → `verify_frozen_identity` (HEAD, `procedure_sha256` from one byte read, plan from one byte read, compatibility, manifest, every remaining `source_pins` entry, five dataset SHA-256s) → reserve → `_run_oneshot` which is the first `load_driver()` (`:1075`). |

---

## Specific checks (a)–(f)

### (a) `trade_bearing_gate` vs `_execute_trial:459-493`

Compared to `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py:459-493`.

Present, in order, with the same refusal texts and `driver.BenchmarkProfileBlocked` type:

| driver line | clause | gate |
| --- | --- | --- |
| 459 copy | `frame.copy()` | `:935` |
| 460-463 | OHLC-only schema | `:936-939` |
| 464-466 | null OHLC | `:940-944` |
| 467-468 | `timestamp` / `date` | `:945-946` |
| 469 | `before_ohlc` `copy(deep=True)` | `:947` |
| 470 | `driver._profile(...)` | `:948` |
| 471-473 | `build_signals` | `:949-951` |
| 474-477 | mutation check | `:952-955` |
| 478 | `signals, stop = result[:2]` | `:956` |
| 479-483 | identical `simulate_slice` kwargs (`return_trades=True`, `return_trade_events=True`, `direction="long"`, `exit_mode="fixed_2R"`, `p020_profile=profile`, `p020_semantics_id="2.1.0"`) | `:957-961` |
| 484 | `event_list = list(events)` | `:962` |
| 486-489 | `num_trades <= 0 or not event_list or len(event_list) != trade_count` | `:968-972` |
| 490-493 | `projection_source == "COMMITTED_TRANSITION_LEDGER"` | `:973-977` |

Missing or substituted (none reordered; same two substitutions as V1.3):

1. **`:459` `pd.read_csv(data_path).iloc[:N]`** is not in the gate. The frame is already isolated by `frame_from_lines` (R4). The gate still copies it.
2. **`:485` `trade_list = [float(value) for value in trades]`** is **absent** (R5/S4). Replaced by `hasattr` + `len(trades)` (`:963-967`). Count-parity still uses that length.
3. **Extra clause** between `:484` and `:486`: unsized series → `BENCHMARK_PROFILE_BLOCKED` (`:963-966`).

Frozen `eligibility_predicate.implemented_by` still says “reproduced clause-identically, binary-only”. The substitutions are the binary-only / S4 design, not a silent weakening. R1 remains CLOSED.

### (b) Selection-rule change V1.3 → V1.4?

No. `REPORT_R5.md` claims T1–T4 only (fail-closure / documentation). Compared the V1.3 frozen artifact still held at `C:/tmp/GROK_SCRATCH_GK20B_20260913/pkg/PRESELECTION_FROZEN.json` against V1.4:

| rule | V1.3 | V1.4 |
| --- | --- | --- |
| family ordering | `(registered grid size, strategy_id) ascending` | identical (`preselect_profile.py:166-169`, frozen `family_ordering_rule`) |
| canonical bytes | `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=True)` | identical (`:154-156`, frozen `canonicalization`) |
| windows | 15m/1h/2h/4h 2049–4096; 1D 2049–2409 | identical, including per-window `sha256` |
| matching | lexicographically first complete matching of five distinct families | identical (`lexicographic_first_matching:319-350`, frozen `selection_rule`) |
| one-shot 15-trial | 5 timeframes × 512/1024/2048; `second_selection: FORBIDDEN` | identical (`MEASUREMENT_SIZES:49`; `eligibility_run.trials: 15`) |
| family records | nine families, 359 records, same `fixed_parameter_record_sha256` | `family_order EQUAL` |
| measurement prefixes | all 15 prefix hashes | EQUAL |
| limitations / owner_decision | D1 Option A, 161 usable 1D bars | EQUAL |

`CALIBRATION_WINDOWS:106-118` still 2049+2048 / 1D 2049+361. The freeze LIMITATION line at `cmd_freeze:765-778` is still

`LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13`

(as printed in `REPORT_R5.md`). What changed is `artifact_version` (`v1.3` → `v1.4`), `procedure_sha256` (the repaired procedure), and the T1–T4 enforcement / docs. Not the selection rule.

### (c) Swapped `PRESELECTION_FROZEN.json` between token read and execution

No. The token is compared to `sha256(raw)` of the single `read_bytes` buffer, that buffer is parsed, and `accepted_digest` is what both outputs record. PROBE 1 swapped the on-disk file (reversed family order) during that one read; execution used the original bytes and both output records carried the original digest. A swap after `require_t0_authorization` returns cannot change execution either: `verify_frozen_identity` and `_run_oneshot` never re-open `FROZEN_PATH`.

### (d) Mutated `BENCHMARK_PLAN.json` after preflight reaching `_profile`

No on this package’s execution path. PROBE 2 mutated the plan file to `POST_PREFLIGHT` inside a replacement `reserve_outputs` (after `verify_frozen_identity`, before `_run_oneshot`). All 45 `_profile` calls received `marker=PREFLIGHT`. The real driver’s `_profile` consumes `plan["p020_profile"]["records"]` from the passed object (`_records` at `run_bounded_benchmark.py:312`); it does not re-read `PLAN_PATH`. Driver `_load_plan` is not on the `--oneshot` path.

### (e) After a commit exception: mixed payload/`ABORTED`, or a deleted reserved file?

Not on the three specified failure modes. PROBES 3–5 (first write, second write, flush) each left **both** files present as `ABORTED` / `error=OSError`. Second-write failure overwrote the already-flushed calibration payload with `ABORTED` rather than leaving a mixed pair. No delete path exists in the procedure. Residual: if `abort` itself raises mid-loop, `commit`’s `finally` may close remaining handles without writing `ABORTED` (see NOT VERIFIED). That nested failure was not in the T3 specification and was not observed.

### (f) V1.3 NIT (Windows shared write into a reserved empty file)

**UNCHANGED.** Reservation is still `open(path, "xb")` (`:551`): exclusive create, not an exclusive lock. PROBE 6: after reservation both files exist at size 0; a later `open(path, "x")` raised `FileExistsError`; a later `open(path, "w")` wrote `SENTINEL_W` into both empty reserved files while the handles were still held; `ReservedOutputs.commit` then overwrote both with the real payload. Same observation as V1.3 PROBE 2 / GROK_V13 NIT-1. T3’s seek/truncate-on-abort does not close this reservation-window shared write. Not worse.

---

## Findings table

| # | severity REQUIRED / NIT | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | NIT | `preselect_profile.py:551` (`ReservedOutputs.reserve`) | `open(path, "xb")` is an exclusive create, not an exclusive lock. PROBE 6: after reservation, `open(path, "w")` wrote `SENTINEL_W` into both empty reserved files while the handles were still held; the later `commit` overwrote them with the payload. | S2’s original attack (exclusive-create after an `exists()` check) is closed, and T3’s mixed-payload commit failure is closed. A concurrent shared write can still occupy the reserved empty file until the handle writes. A crash in that window spends the one shot on sentinel bytes. Not a second-run overwrite path in the tool itself. Unchanged from V1.3. |

No REQUIRED findings.

---

## RED probes (scratch copy, synthetic only)

Scripts: `C:/tmp/GROK_SCRATCH_GK20C_20260914/pkg/probes/red_probes.py`.
Pinned interpreter. No CLI token matching the real V1.4 digest. `observed_impl_head` stubbed via the synthetic environment so git is not invoked.

### PROBE 1 — swap frozen file after the accepted `read_bytes` (T1)

Monkeypatched `Path.read_bytes` so the one `FROZEN_PATH` read returned the original bytes and then overwrote the file with a reversed `family_order`.

```
OBSERVED oneshot_returncode=0
OBSERVED frozen_read_calls=['C:\\tmp\\GROK_SCRATCH_GK20C_20260914\\tmppdrfkb4a\\PRESELECTION_FROZEN.json']
OBSERVED original_digest=3dfa36103b3a940b08b9aaf88383c0776ac39fd786d8fefad1735063e468bce5
OBSERVED swapped_digest=f524f56b45bee2eef4b7b2b3d40240e723d8edef7b313830e197b1c138dfb52e
OBSERVED on_disk_digest=f524f56b45bee2eef4b7b2b3d40240e723d8edef7b313830e197b1c138dfb52e
OBSERVED cal_frozen_sha256=3dfa36103b3a940b08b9aaf88383c0776ac39fd786d8fefad1735063e468bce5
OBSERVED elig_frozen_sha256=3dfa36103b3a940b08b9aaf88383c0776ac39fd786d8fefad1735063e468bce5
OBSERVED selection={'15m': 'GEN_A', '1D': 'GEN_E', '1h': 'GEN_B', '2h': 'GEN_C', '4h': 'GEN_D'}
OBSERVED PROBE1_PASS: swap after token read did not change executed frozen bytes or recorded digest
```

### PROBE 2 — mutate `BENCHMARK_PLAN.json` after preflight (T2)

Plan marked `PREFLIGHT` and pinned. `reserve_outputs` replaced with a helper that rewrites the plan file to `POST_PREFLIGHT` then reserves. `RecordingDriver._profile` recorded `plan["marker"]`.

```
OBSERVED oneshot_returncode=0
OBSERVED unique_markers=['PREFLIGHT']
OBSERVED on_disk_marker='POST_PREFLIGHT'
OBSERVED plan_read_text_after_patch_count=1
OBSERVED PROBE2_PASS: _profile saw verified preflight plan, not the mutated file
```

(`plan_read_text_after_patch_count=1` is the probe helper’s own `Path.read_text` while mutating the file, not a production reload.)

### PROBE 3 — first `write` raises (T3)

Faulty calibration handle writes `PARTIAL` then raises `OSError`.

```
OBSERVED commit_raised=OSError:synthetic write failure
OBSERVED calibration exists=True deleted=False ... status=ABORTED error=OSError
OBSERVED eligibility exists=True deleted=False ... status=ABORTED error=OSError
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE3_PASS
```

### PROBE 4 — second `write` raises (T3)

Faulty eligibility handle. Calibration write+flush had already succeeded; abort overwrote it.

```
OBSERVED commit_raised=OSError:synthetic write failure
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE4_PASS
```

### PROBE 5 — `flush` raises (T3)

Faulty calibration flush.

```
OBSERVED commit_raised=OSError:synthetic flush failure
OBSERVED both_aborted=True mixed_payload_and_aborted=False files_deleted=False
OBSERVED PROBE5_PASS
```

### PROBE 6 — Windows shared write into reserved empty files (V1.3 NIT)

Temp paths, real `reserve_outputs()`.

```
OBSERVED reserved_handles=['calibration', 'eligibility']
OBSERVED cal_exists=True elig_exists=True
OBSERVED cal_size_after_reserve=0 elig_size_after_reserve=0
OBSERVED exclusive_create_sentinel={'calibration': 'REFUSED_FileExistsError', 'eligibility': 'REFUSED_FileExistsError'}
OBSERVED shared_write_sentinel={'calibration': 'WRITE_SUCCEEDED', 'eligibility': 'WRITE_SUCCEEDED'}
OBSERVED shared_write_contents={'calibration': 'SENTINEL_W', 'eligibility': 'SENTINEL_W'}
OBSERVED after_handle_write cal={"kind":"calibration","probe":true}
OBSERVED after_handle_write elig={"kind":"eligibility","probe":true}
OBSERVED SENTINEL_W_IN_FINAL=False
OBSERVED SENTINEL_X_IN_FINAL=False
OBSERVED PROBE6_PASS: V1.3 Windows shared-write NIT is UNCHANGED
```

### PROBE 7 — static scan of `_run_oneshot`

```
OBSERVED _run_oneshot_forbidden_hits=[]
OBSERVED load_plan_in_module_at_freeze_only=True
OBSERVED PROBE7_PASS: execution path after preflight does not reload plan or frozen file
```

Writes were under temp directories, not the package outputs. After all CLI refusals and probes:
`PRESELECTION_CALIBRATION.json` and `PRESELECTION_ELIGIBILITY.json` do not exist in the scratch package directory.

---

## Commands run with observed output

Pinned interpreter:
`C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`
(present). Cwd for package commands: `C:/tmp/GROK_SCRATCH_GK20C_20260914/pkg`.

Copy of the package into scratch (PowerShell `Copy-Item -Recurse`).

Frozen digest:

```
f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
MATCH
SIZE 18968
```

SHA256SUMS (scratch copy):

```
True PRESELECTION_PREREG_V1.md
True PRESELECTION_FROZEN.json
True PRESELECT_RUNBOOK.md
True REPORT.md
True REPORT_R2.md
True REPORT_R3.md
True REPORT_R4.md
True REPORT_R5.md
True preselect_profile.py
True tests/test_preselect.py
procedure_match True
```

pytest:

```
$ …python.exe -m pytest tests -q -p no:cacheprovider
........................................................................ [ 80%]
..................                                                       [100%]
90 passed in 2.58s
EXIT=0
```

`--oneshot` without a token:

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

RED probes: `…python.exe probes\red_probes.py` — output in the previous section. EXIT=0.

Not run: any `--i-have-t0-review-authorization` token equal to the V1.4 digest; `--oneshot` with a valid token; `run_bounded_benchmark.py --run`; `--freeze`; any git command.

---

## NOT VERIFIED

- **This is not a T0 review and cannot accept.** Exact claude-opus-5 and gpt-5.6-sol have not
  run on these bytes in this lane. V1.3 Sol REQUEST_CHANGES / Opus PASS-WITH-NITS / Gemini
  corroboration do not carry over.
- **Live `git rev-parse HEAD` was not observed** (brief: no git command of any kind). Code
  compares it to frozen `impl_head` `b9b72f858dc830a9389517f79da5ea3c1fa6122c` and to
  `IMPL_HEAD` at freeze time; the live repository was not checked here.
- **Live plan / compatibility / manifest / nine source pins / five dataset files** were not
  re-hashed against frozen values in this lane (except the procedure file and the frozen JSON
  itself). T2’s plan-mutation probe used a synthetic `plan.json`, not the lead `BENCHMARK_PLAN.json`.
- **The real driver/engine path has never been run.** Gate equivalence, T1 swap, T2 plan
  carry-through, T3 commit abort, S2 reservation, S3 single-read and ABORTED records are proven
  on doubles / synthetic CSVs. `_load_engine` / real `_profile` / real `simulate_slice` are
  unexercised. Whether a real `_profile` side-effect could open some other file (economic
  records via `RECORD_PATHS`, not `BENCHMARK_PLAN.json`) is out of T2’s stated scope and untested
  here.
- **No real 45-cell calibration or 15 locked trials.** Eligibility of any matching is unknown.
- **Two-process reservation race was not launched.** Exclusive-create was probed in-process.
  Network-filesystem `O_CREAT|O_EXCL` behaviour was not measured.
- **If `ReservedOutputs.abort` itself fails mid-loop** (disk full, revoked handle after
  `seek`/`truncate`), `commit`’s `finally` may close remaining handles without an `ABORTED`
  record. That nested failure path is untested. The specified first-write / second-write /
  flush failures were tested and closed.
- **Worktree cleanliness** of `C:/P020_IMPL_20260912` is unverified (HEAD-only even in the
  tool; this lane did not run git at all). `check_p020_acceptance.py` was not opened.
- **Bar quality inside windows** (monotonicity, gaps, duplicates) was not audited.
- **The 161 usable 1D bars** remain arithmetic, not an observed trade count.
- **Eligibility-handle flush failure** was not separately injected; it shares the same
  `commit`/`abort` path as PROBE 5 (calibration flush) and PROBE 4 (eligibility write).

---

GROK_V14_VERDICT: NITS
