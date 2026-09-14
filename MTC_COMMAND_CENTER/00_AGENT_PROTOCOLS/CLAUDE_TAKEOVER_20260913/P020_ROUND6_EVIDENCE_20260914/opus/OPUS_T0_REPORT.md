# T0 review report — ROUND 6 — WP-P0-20 preselection procedure V1.6

Reviewer: exact `claude-opus-5`, effort xhigh. Date: 2026-09-14.
Brief: `C:/tmp/P020_PRESELECT_T0_R6_20260914/REVIEW_BRIEF.md` + `opus/BRIEF.md`.
Scope: the frozen artifact `cb756020…` and everything it binds. I ran every mandated command myself
with the pinned interpreter. I did **not** run the real `--oneshot` and did **not** use the real V1.6
token to authorize anything; every transaction-level RED arm below runs with the economic gate
**stubbed** or on a sandbox artifact whose digest differs from the real token.

---

## 0. Verified identities (COMPUTED)

| Item | Expected (brief) | Computed by me | Result |
|---|---|---|---|
| `PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | **MATCH** |
| Repository HEAD | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` | **MATCH** |
| Pinned interpreter | Python 3.12.12 | `Python 3.12.12` at the pinned path | **MATCH** |
| `SHA256SUMS.txt` (13 entries) | all files | `sha256sum -c` → 13 × `OK` | **MATCH** |
| `SHA256SUMS.txt` line endings | LF | 1090 bytes, **CR = 0**, LF = 13 | **LF (N-4 closed)** |
| Instrument record **V3** | `69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9` | identical; `.sha256` sidecar identical | **MATCH** |
| Instrument record V2 (history) | `1a128964…` | `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15` | **UNCHANGED on disk** |
| `BENCHMARK_PLAN.json` | `c6f07afd…` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` | **MATCH (= frozen `source_pins`)** |
| `run_bounded_benchmark.py` | `3d4453cd…` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` | **MATCH (= frozen `source_pins`)** |
| `selected_manifest.json` | `712ddc27…` | re-verified by the tool's own preflight in every arm | **MATCH** |
| Derivation tool package | `SHA256SUMS.txt` | `sha256sum -c` → 5 × `OK` | **MATCH** |
| `--freeze` reproduction | `cb756020…` | scratch rebuild → `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | **BYTE-IDENTICAL** |

The token binds the exact frozen bytes: `require_t0_authorization:921-923` hashes the one buffer it
reads, and `:931` parses **that same buffer**.

---

## 1. Preregistration correctness

Verified against the artifact bytes:

* Nine `GEN_*` families, `registered_record_total` = **359** (`PRESELECTION_FROZEN.json:432`);
  enforced at freeze by `preselect_profile.py:460-465`.
* Ordering `(registered grid size, strategy_id)` ascending (`frozen_family_order:259-262`), records by
  canonical JSON bytes (`frozen_records:265-267`, `canonical_record:157-159`).
* Five timeframes in frozen order `15m,1h,2h,4h,1D` (`:125`, frozen `timeframe_order`).
* Prefixes 512/1024/2048 (`MEASUREMENT_SIZES:52`).
* Calibration windows disjoint from rows 1..2048: 15m/1h/2h/4h rows 2049-4096, 1D rows 2049-2409
  (frozen `calibration_windows`), enforced at freeze (`plan_calibration_window:344`) **and where the
  window is consumed** (`calibration_frame:1000`).
* Binary predicate (`trade_bearing_gate:1031-1099`), lexicographically-first complete matching of five
  distinct families (`lexicographic_first_matching:412-443`), one-shot 15-trial check
  (`_run_oneshot:1241-1253`), `BENCHMARK_PROFILE_BLOCKED` on any failure (`:438-442`, `:1254`).

**No selection rule changed.** I diffed the frozen artifacts V1.1 → V1.2 → V1.3 → V1.4 → V1.5 → V1.6
myself (digests `8b2ed892…`, `8b688d1a…`, `2e67f3f4…`, `f839c960…`, `b7548984…`, `cb756020…`; the
first five recovered from the Lead reproduction directories and re-hashed, and `2e67f3f4…` /
`b7548984…` match the V1.3 and V1.5 tokens named in the brief, which binds their identity):

| Key | V1.1 → V1.6 |
|---|---|
| `family_order`, `selection_rule`, `family_ordering_rule`, `timeframe_order`, `calibration_window_rule`, `registered_record_total`, `datasets`, `canonicalization`, `owner_decision`, `limitations` | **byte-identical** |
| `calibration_windows`, `measurement_inputs` | identical except **added** `first_ts` / `last_ts` on every window and prefix (V1.5, for the record-interval check). No `start_row`, `end_row`, `row_count`, `input_rows`, `sha256` or `dataset_id` changed. |
| `eligibility_predicate` | V1.1 → V1.2 only: the R1 repair made the gate text clause-identical to `_execute_trial` (added `len(trade_events) == len(trades)`, `guards`, `applies_to`, corrected `implemented_by`). **Byte-identical V1.3 → V1.6.** |

V1.5 → V1.6 changed exactly seven keys and nothing else:
`artifact_version`, `supersedes`, `instrument_record_interval` (V2→V3), `prereg_sha256`,
`runbook_sha256`, `procedure_code_sha256`, and two `source_pins`
(`BENCHMARK_PLAN.json`, `run_bounded_benchmark.py`). This is exactly what the brief declares.

---

## 2. Closure table

All evidence is `file:line` against the bytes I hashed, not against `REPORT_R5.md` / `REPORT_R7.md`.

| Finding | Status | Evidence |
|---|---|---|
| **R1/R5** — one shared binary gate, clause-identical to `_execute_trial`, no economic read | **CLOSED** | `trade_bearing_gate:1031-1099` used by both stages (`:1215` calibration, `:1248` trials). Clause-by-clause: `.copy()` :1057, schema :1058-1061, null-OHLC :1062-1066, `before_ohlc` deep copy :1069 + check :1074-1077, identical `simulate_slice` call :1079-1083, `num_trades <= 0 or not event_list or len(event_list) != trade_count` :1090, projection check :1095. Only `len(trades)` is taken (:1089). **ARM 6**: decision-identical to a transcription of `_execute_trial:470-503` on **75/75** probes. |
| **R2** — selection re-derived from the in-memory matrix; `calibration_sha256` recorded | **CLOSED** | `verified_selection:1102-1152` re-runs `lexicographic_first_matching` on the recorded matrix and refuses on any difference; applied at `:1234` to the record about to be written. `calibration_sha256` at `:1236`, carried at `:1258`. |
| **R3** — no overwrite path | **CLOSED** | `ReservedOutputs.reserve:652-658` (`open(path,"xb")`). **ARM 4**: a pre-existing output refuses `PRESELECT_REFUSED_ALREADY_RUN`; the pre-existing file is byte-unchanged. |
| **R4** — frames built from isolated window/prefix bytes; one read per file | **CLOSED** | `frame_from_lines:965-977` (`io.StringIO`), `calibration_frame:995-1004`, `measurement_prefix_frame:1007-1028`. `csv_lines` (the only whole-file parse helper) is called **only** from `build_freeze:754`. |
| **R6** — full identity re-verification before the driver loads; `--freeze` records observed HEAD | **CLOSED** | `verify_frozen_identity:549-629` (HEAD :568, procedure :578-582, prereg/runbook :583-590, plan :591-595, compatibility :597-600, manifest :601-604, every source pin :605-617, five datasets :618-627, record interval :628). `build_freeze:721,783` records the observed HEAD. |
| **N-1** runbook refusal table complete | **CLOSED** | `PRESELECT_RUNBOOK.md:188-205` lists all **18** `PRESELECT_REFUSED_*` codes present in the source plus `BENCHMARK_PROFILE_BLOCKED` (:182). I enumerated the source codes and compared; no code is missing. |
| **N-2** warmup citation lines | **CLOSED** | `preselect_profile.py:80-86` cites the three `ema_200` gates (`mega_walk_forward.py:503`, `:529`, `:580`) and distinguishes materialisation (`:388`) from dependency; prereg `:105`. |
| **N-4** LF `SHA256SUMS` | **CLOSED** | CR count = 0 (computed). |
| **N-3 / N-5** `REPORT.md` banner | **NOT CLOSED (NIT)** | `REPORT.md:1` names `REPORT_R2..R5` only; `REPORT_R6.md` and `REPORT_R7.md` exist and are unlisted. → **N6-5**. |
| **S1** single `--oneshot` transaction | **CLOSED** | `cmd_oneshot:1165-1191`, `_run_oneshot:1194-1279`: calibration :1209-1222, matching from the in-memory matrix :1225, trials :1241-1253, both files written only at :1269. `--calibrate` / `--eligibility` are argparse errors (observed live, exit 2). |
| **S2** atomic exclusive-create reservation of BOTH paths after preflight, before the first simulation | **CLOSED** | preflight `:1185` → `reserve_outputs()` `:1186` → driver loaded at `:1197`. Handles kept; `reserve_outputs:700-714` aborts the first reservation if the second fails. **ARM 4** reproduces the partial-reservation case. |
| **S3** each dataset read exactly once | **CLOSED** | the one read is `:622`; `dataset_lines:980-992` opens nothing. **ARM 1** (instrumented `Path.read_bytes`/`read_text` over a full stubbed transaction): five CSV files, **1 read each**. |
| **S4** `len(trades)` only; unsized refused; never iterated | **CLOSED** | `:1085-1089`. **ARM 5**: a container whose `__iter__` and `__getitem__` raise passes the gate untouched; an unsized container is refused `BENCHMARK_PROFILE_BLOCKED: unsized trade series`. |
| **S5** runbook separates preflight refusals from recorded outcomes | **CLOSED** | `PRESELECT_RUNBOOK.md:170-176` phase table. Reproduced live: token refusals wrote **no** files. |
| **NIT-1** `assert_disjoint` inside `calibration_frame` | **CLOSED** | `:1000`. |
| **NIT-4** `procedure_code_sha256` computed last, re-checked before load | **CLOSED** | computed last at `:875-877`; re-checked at `:578-582`. **ARM E**: one appended comment byte → `PRESELECT_REFUSED_SOURCE_DRIFT: preselect_profile.py`, with a *valid* token, nothing reserved. |
| **T1** one frozen read; same bytes hashed, parsed, carried into both records | **CLOSED** | `:921` read → `:922` hash → `:931` parse, returned as `(frozen, digest)`; `:1184` → `frozen_sha256` `:1200` → `:1228` and `:1257`. **ARM 1**: frozen file read **exactly once**. **ARM 2**: swapping the frozen file for a hostile one (reversed `family_order`) between the token read and execution leaves both output records bound to the accepted digest and the first cell still runs the accepted family order. |
| **T2** the verified plan **object** is executed | **CLOSED** | `plan_raw` `:591` → `verified_plan = json.loads(plan_raw)` `:596` → `:1185` → `:1188` → `:1215`/`:1248` → `driver._profile(...,plan)` `:1070`. `load_plan()` is called **only** from `build_freeze:727`. **ARM 1**: `BENCHMARK_PLAN.json` read **once**; all 60 gate calls received the **same object id**. |
| **T3** commit failure → BOTH files `ABORTED`, handles kept, nothing deleted, no mixed pair | **CLOSED** | `commit:660-675` (both writes/truncates/flushes in one `try`; `abort` on any `BaseException`; handles closed only in `finally`), `abort:677-697` (`seek(0)`, `truncate(0)`, ABORTED record, flush). **ARM 3** × 3 (first write raises / second write raises / flush raises): both files exist, both are `{"status":"ABORTED"}`, neither holds a payload. |
| **T4** phase-split documentation | **CLOSED** | `PRESELECT_RUNBOOK.md:170-176` (before any reservation / partial reservation failure / post-both-reservations failure, with exact residue and exit codes). Residues match ARMs 3 and 4. |
| **N4-1 / Sol-5** line citations | **PARTLY CLOSED (NIT)** | Live `§(a)-(c)`, `§(e)-(i)` self-citations verified correct against the AST line ranges. **Two live citations are stale**: prereg `:251` cites `preselect_profile.py:456-522` for `verify_frozen_identity` (now `:549-629`) and `:839-852` for `dataset_lines` (now `:980-992`). → **N6-7**. Driver citations → **N6-1**. |
| **N4-2 / Sol-2** commit truncate | **CLOSED** | `commit:664` and `:667` call `truncate()` after each write. |
| **N4-3 / Sol-3** per-handle abort recovery + doc | **CLOSED for the documented behaviour** | `abort:680-697` iterates every handle and continues past a per-handle failure; documented at `PRESELECT_RUNBOOK.md:175`. Residual: the swallowed error → **N6-2**. |
| **N4-4 / Sol-1** `prereg_sha256` / `runbook_sha256` + `procedure_code_sha256` | **CLOSED** | written `:875-877`, re-checked `:578-590`. The frozen artifact no longer pairs `procedure` with a mismatched digest field. |
| **Sol-4** runbook pytest flag | **CLOSED** | `PRESELECT_RUNBOOK.md:33`: `& $py -m pytest tests -q -p no:cacheprovider`. |
| **Interval check** (`PRESELECT_REFUSED_RECORD_INTERVAL`) | **CLOSED** | `verify_frozen_record_interval:232-253` (frozen interval equality, per-window and per-prefix timestamp equality, and in-interval assertions). **ARM H**: on a scratch copy with the V1-era interval (`end_exclusive 2025-09-22T08:00:00Z`), `--freeze` refuses `PRESELECT_REFUSED_RECORD_INTERVAL: calibration 15m first_ts outside instrument record interval` and writes no artifact; the same scratch freezes once the interval covers the windows. This is the V1.4 abort, now caught at freeze time. |
| **D5** `_validate_plan` family-set check | **CLOSED** | see §8. |
| **Derivation tool** | **CLOSED with a NIT** | see §9. |
| **D9-A record V3 + sizing floor (item 10)** | **CLOSED** | see §10. |
| **Opus round-3 NIT-A** (`procedure` vs `procedure_sha256` name different files) | **ADDRESSED** | superseded by N4-4; V1.6 carries `procedure_code_sha256` (code), `prereg_sha256` and `runbook_sha256` (documents) as separate, all three re-checked. |
| **Opus round-3 NIT-B** (commit does not truncate) | **ADDRESSED** | `commit:664`, `:667`. |
| **Opus round-3 NIT-C** (failure inside the final write) | **MOOT** | superseded by the two-output `commit`; ARM 3 confirms all three fault points abort both files. |

---

## 3. Leakage — can an economic outcome influence or be exposed by the selection?

**No, on the mechanisms I could test.** Findings:

* **Selection cannot change after results are visible.** The matching is computed from the in-memory
  matrix (`:1225`) and re-derived from the record about to be written (`:1234`) inside one process;
  no file is read between the matrix and the trials (proved by the ARM 1 read counters: after the
  preflight, zero reads of the plan, the frozen artifact or any dataset).
* **Execution cannot run without the digest-bound token.** Observed live: no token →
  `PRESELECT_REFUSED_NO_T0_REVIEW`; dead V1.3 token `2e67f3f4…` →
  `PRESELECT_REFUSED_T0_TOKEN_MISMATCH`; tampered procedure byte with a *valid* token →
  `PRESELECT_REFUSED_SOURCE_DRIFT`. None of the three reserved or wrote anything.
* **No economic value is read, stored or returned.** The gate takes `num_trades` (a comparison) and
  `len(trades)` (a count). ARM 5 proves the trade series is neither iterated nor indexed; ARM 6 proves
  the decision is identical to the reference gate over a 75-case truth grid.
* **`--freeze` runs no simulation.** Verified by reproducing it: it imports the registry only and
  prints the artifact plus the limitation line.

**Prior-round disclosure (recorded, not a defect I can close).** The V1.5 one-shot returned
`BENCHMARK_PROFILE_BLOCKED` and the tool discarded the matrix by design. I confirmed this against the
bytes: the archived outputs of both prior runs contain **only** ABORTED records —
`{"error":"InstrumentRecordRefusal",...}` (V1.4) and `{"error":"BENCHMARK_PROFILE_BLOCKED",...}` (V1.5)
— no matrix, no selection, no economic content, and they were moved, not deleted. The owner-authorized
D7-A/D8-A diagnostics did disclose per-timeframe **aggregate** counts (trade-bearing families per
timeframe; sorted, unattributed signal counts) with family identities withheld. Those aggregates
contain no family↔timeframe mapping, and V3 changes the fill outcome that produced them, so they
cannot determine the V1.6 matching. I record this as the honest residual: it is information the owner
did not hold at the V1.5 freeze. I could not audit the chat channel — see NOT VERIFIED.

**Re-arming the one shot.** The V1.6 run is the third attempt. That is not a violation of
`second_selection: FORBIDDEN` on the bytes: no selection has ever been produced (V1.4 aborted before
the first cell, V1.5 blocked before the trials). The reset is explicitly recorded and attributed —
`PRESELECT_RUNBOOK.md:69-74` names all six dead tokens and states "Owner ruling D9-A resets both spent
shots for this V1.6 repair." The change that re-arms it is an **input** correction, not a selection
rule: the frozen diff in §1 shows no rule, window, prefix or family-order change, and the corrected
value is independently pre-documented — `03_PRODUCTION_CLOSURE_MATRIX.md:32` row I-3 records the
venue's `quantity_step: 0.00001`, and that file is dated **2026-09-11**, three days *before* the D8-A
diagnostic. The fix was therefore not reverse-engineered to unblock the test.

### RED arms — all designed against the V1.6 code, all run

| Arm | Attack | Result |
|---|---|---|
| 1 | instrumented `Path.read_bytes`/`read_text` across a full stubbed transaction | 5 datasets × **1 read**; frozen **1 read**; plan **1 read**; 60 gate calls, all with the **same** plan object |
| 2 | replace `reserve_outputs` so it swaps `PRESELECTION_FROZEN.json` for a hostile artifact (reversed `family_order`) between the token read and execution | both output records stay bound to the **accepted** digest; the first cell runs the **accepted** family order |
| 3a/3b/3c | first `write` raises / second `write` raises / `flush` raises | all three: both files exist, both `ABORTED`, no mixed pair, nothing deleted |
| 4 | pre-create only the **second** output path | `PRESELECT_REFUSED_ALREADY_RUN`; first path kept as an `ABORTED` record; the pre-existing file byte-unchanged |
| 5 | trade container whose `__iter__`/`__getitem__` raise; and an unsized container | accepted without iterating; unsized → `BENCHMARK_PROFILE_BLOCKED: unsized trade series` |
| 6 | 75-case gate-equivalence grid vs a transcription of `_execute_trial` | 75/75 identical decisions |
| E | append one comment byte to `preselect_profile.py`, valid token | `PRESELECT_REFUSED_SOURCE_DRIFT: preselect_profile.py`; nothing reserved |
| H | calibration window outside the instrument record interval (scratch) | `PRESELECT_REFUSED_RECORD_INTERVAL`; no artifact written; positive control freezes |
| I | `--oneshot` without a token / with the dead V1.3 token / `--freeze` with a token / `--calibrate` / `--eligibility` | all refuse, exit 2, no file created |
| 10c | point the V2 (RED) sizing arm at V3 | all five RED cases stop blocking (`DID NOT RAISE` ×5) — the RED arm genuinely depends on the record |
| 8 | `_validate_plan`: outside family / duplicate / wrong sizes / no derivation / non-list `family_order` | all refused; both GREEN cases accepted; never touches the frozen artifact |

I did **not** mutate `BENCHMARK_PLAN.json` on disk (it is a shared pinned input). The equivalent and
stronger proof is ARM 1's combination of a **read counter of 1** and **object-identity** across all 60
gate calls: nothing can be re-read, so nothing can be substituted.

---

## 4. Identity and drift

Every frozen hash recomputed independently (§0). The token binds the exact frozen bytes (T1, ARM 2).
The frozen artifact in turn binds the procedure code, the preregistration, the runbook, the plan, the
compatibility file, the manifest, all nine implementation sources, all five datasets, and the
instrument record interval — all re-verified before the driver is imported (`:549-629`).
I additionally recomputed every frozen `first_ts`/`last_ts` directly from the manifest's CSV bytes:
all 20 windows/prefixes match.

---

## 5. Tests and freeze reproduction

Commands, cwd `C:/tmp/P020_PRESELECT_20260913`, pinned interpreter:

```
$ python -m pytest tests -q -p no:cacheprovider
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 4.60s
```

**106 passed** — matches the count stated in `REPORT_R7.md`. Collection confirms 106 (96 from
`test_preselect.py` + 10 from `test_sizing_floor.py`); `GateEquivalence` is at
`tests/test_preselect.py:578` and `RealInstrumentRecordSmoke` at `:1826`.

Freeze reproduction, cwd `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` (byte-identical copy of
`preselect_profile.py`, prereg and runbook):

```
FROZEN_WRITTEN C:\tmp\P020_T0R6_OPUS_SCRATCH\pkg\PRESELECTION_FROZEN.json sha256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
```

Digest equals the package file and the brief's value. Token refusals, cwd
`C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg`:

```
$ python preselect_profile.py --oneshot
PRESELECT_REFUSED_NO_T0_REVIEW: --i-have-t0-review-authorization <sha256 of PRESELECTION_FROZEN.json> is required   (exit 2)

$ python preselect_profile.py --oneshot --i-have-t0-review-authorization 2e67f3f4ea357b4b974313ddd4a427564860e5618f24d48758f07b599da4b614
PRESELECT_REFUSED_T0_TOKEN_MISMATCH: token does not match the frozen artifact digest                                 (exit 2)

$ python preselect_profile.py --freeze --i-have-t0-review-authorization deadbeef
preselect_profile.py: error: --freeze never takes a T0 authorization token

$ python preselect_profile.py --calibrate      # and --eligibility
preselect_profile.py: error: one of the arguments --freeze --oneshot is required
```

No `PRESELECTION_CALIBRATION.json` / `PRESELECTION_ELIGIBILITY.json` was created by any of these.
I did not pass the real V1.6 token to `--oneshot` and did not run `run_bounded_benchmark.py --run`.

---

## 6. Limitation honesty (1D)

Accurate and printed on every freeze (observed above). The frozen record
(`PRESELECTION_FROZEN.json:272-284`) states 361 window rows, 200-bar warmup, **161** usable bars
against **1848** elsewhere, that 1D eligibility "may therefore be decided wrongly in either
direction", `accepted_by: owner decision D1 Option A, 2026-09-13`, and
`not_mitigated: no BTCUSDT 1D dataset with more rows exists in the frozen manifest`. The arithmetic
checks out: 2409 − 2048 = 361; 361 − 200 = 161; 2048 − 200 = 1848.

Corroborating, not contradicting, the brief's supplemental observation: the Lead's V1.6 per-timeframe
smoke reports 1D BLOCKED with no signal in the 361-row window. That is the accepted weak spot, not a
new defect.

---

## 7. Real-stack input preconditions (the round-4 miss)

Loaded `EconomicRecords.from_record_paths(...)` from `mtc_v2.core.economics` with the **real** pinned
V3/cost/funding records and called
`records.instrument.for_evaluation(ts, records.runtime_instrument_config or {})` — pure calls, no
`_profile`, no `simulate_slice`, no token.

| Precondition | Where enforced | Holds for the frozen inputs? |
|---|---|---|
| evaluation timestamp inside `effective_interval` | `mtc_v2/core/instrument.py:278-279` | **YES — 40/40.** All 5 calibration windows and all 15 measurement prefixes, at **both** bounds. I first recomputed those 40 timestamps from the manifest CSV bytes (they match the frozen annotations). |
| negative control | same | the V1-era interval (`end_exclusive 2025-09-22T08:00:00Z`) **refuses** the 15m calibration start with `REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE` — the exact ELIG14 failure |
| instrument/cost/funding **record digests** vs the digest-pinned plan | `run_bounded_benchmark._records:329-333` (every `_profile` call) | **YES** — `69b6f246…`, `27ee3b0e…`, `fdeab636…` all equal the plan entries |
| instrument **symbol** scope | `_records:334-338` | **YES** — `SYNTH-RULE2-01-GREEN` |
| cost/funding `symbol_scope` | `_records:339-342` | **YES** — both `SYNTH-RULE2-01-GREEN` |
| `provenance.human_reviewer` present | `instrument.py:246-250` | **YES** — `'Baris Semaay'` |
| `quantity_step` positive, `minimum_quantity`/`minimum_notional` non-negative, `point_value`/`contract_multiplier` positive, exactly one of `price_tick`/`price_alignment_policy` | `instrument.py:219-244` | **YES** — `qty_step=1e-05, min_qty=0.0, min_notional=0.0, price_tick=1.0, point_value=1.0, mult=1.0` |
| owner caps == `OD-20260912-P020-VALUES-1` | `_build_profile:412-420` | **YES** — `max_risk_at_stop_fraction 0.015`, `max_leverage 1.0`, `max_total_exposure 0.20` read live from `p020_owner_policy` |
| row-9 fields remain unset | `_build_profile:422-431`, `_validate_plan:201-204` | **YES** |
| `runtime_instrument_config` | `_build_profile:353` | `None` → `{}`; no runtime override exists to exercise |
| the tool's own freeze-time interval check | `verify_frozen_record_interval:232-253` | **YES** — ARM H refuses when a window is moved outside the interval, and the positive control freezes |

**Preconditions that remain unexercised** (stated explicitly, as the brief requires):

1. **Cost and funding `effective_interval` are declared but enforced nowhere.** Both records declare
   `end_exclusive = 2025-09-22T08:00:00Z`, and the entire 15m calibration window
   (2025-09-22T08:00Z … 2025-10-13T15:45Z) lies **outside** them. I grepped
   `mtc_v2/core/economics.py`: it contains no `effective_interval` handling at all; only
   `instrument.py:197` enforces an interval. So this is inert **at this pinned HEAD** — and the HEAD
   is digest-pinned — but it is the last declared-but-unenforced input precondition, i.e. the same
   defect class as the V1.4 abort, one layer down. → **N6-3**.
2. `runtime_instrument_config` non-`None` behaviour — no such configuration exists in the pinned
   records.
3. The full real 45-cell matrix and 15 locked trials under V3 — deliberately not run (see NOT VERIFIED).

---

## 8. D5 driver change — `_validate_plan`

`_validate_plan:181-200`. I ran the arms against the real driver with the real plan:

| Arm | Result |
|---|---|
| current hand-written plan (original five families, **no** `derivation` block) | **validates unchanged** |
| derived plan, `derivation.family_order` = the nine frozen families, trials using the **other** five families (`GEN_RSI_OVERSOLD_REVERSAL`, `GEN_ZSCORE_MEAN_REVERSION`, `GEN_DONCHIAN_BREAKOUT`, `GEN_ATR_PULLBACK_TREND`, `GEN_GOLDEN_CROSS_PULLBACK`) | **validates** |
| a second, differently-ordered five-family assignment | **validates** |
| family **outside** `family_order` | **refused** |
| **duplicate** family (4 distinct) | **refused** |
| wrong per-family sizes `(512,512,2048)` | **refused** |
| out-of-set input size `4096` | **refused** |
| `derivation.family_order` not a list | **refused** |
| non-original five families **without** a derivation block | **refused** |
| acyclicity | `grep` finds **zero** references to `PRESELECT`/`FROZEN` in the driver; an instrumented run of `_validate_plan` opened **no** `PRESELECTION_*` path |

**No other driver semantics changed.** I diffed the V1.5-pinned driver bytes
(`b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3`, recovered from
`C:/tmp/GROK_SCRATCH_GK20D_20260914/benchmark/` and re-hashed to that exact digest) against the
current file: **one line changed**, `RECORD_PATHS["instrument"]` V2 → V3 (`:25`). The V1.4-pinned
driver `4b293de6…` is not on disk and the brief forbids git history inspection, so the V1.4→V1.5 D5
diff was not re-verified by me — see NOT VERIFIED.

---

## 9. Derivation tool

`C:/tmp/P020_PLAN_DERIVE_20260913/` — digests verified (5 × `OK`), **15 tests passed**.

* **Single read per input, digest describes the parsed bytes**: `load_json_once:30-39` — one
  `read_bytes()`, `sha256` of **that** buffer, `json.loads` of **that** buffer, both returned. Used for
  eligibility, calibration, base plan and the frozen artifact (`:151-154`).
* `derivation.eligibility_sha256` / `calibration_sha256` / `base_plan_sha256` (`:162-166`) are those
  parsed-buffer digests.
* **`EXPECTED_FROZEN_SHA256` = `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126`**
  (`:12`) — the V1.6 digest. Re-pin confirmed.
* `derivation.family_order` emitted (`:167`), taken from the frozen artifact's nine families — which is
  exactly what `_validate_plan:189-194` requires.
* Refusals: frozen digest mismatch, eligibility/calibration cross-digest mismatch, status not
  `PROFILE_ELIGIBLE_NOT_ACCEPTED`, selection not five distinct, selection outside `family_order`
  (`verify_inputs:79-100`); exclusive-create output (`write_once:174-179`).
* Swap probe: `derivation.frozen_sha256` (`:165`) is copied from the **eligibility record**, not from
  the tool's own single read. It is safe only because `verify_inputs:80-83` pins *both* to
  `EXPECTED_FROZEN_SHA256`. → **N6-8** covers the stronger gap.

---

## 10. D9-A record V3 and the sizing floor

**(a) V3 vs V2 — I diffed the two JSON files myself.** Exactly three differences:

| Field | V2 | V3 |
|---|---|---|
| `record_id` | `SYNTH-P020-BOUNDED-INSTRUMENT-V2` | `SYNTH-P020-BOUNDED-INSTRUMENT-V3` |
| `quantity_step` | `1` | `1e-05` |
| `provenance.quantity_step_correction` | absent | **added** (cites D8-A, row I-3, `OD-20260914-P020-RECORD-V3-1`, ratified by Baris Semaay, `2026-09-14T12:59:00Z`) |

`minimum_quantity` **0**, `minimum_notional` **0**, `effective_interval`
(`2019-09-08T00:00:00Z` → `2026-05-01T00:00:00Z`), `symbol`, `point_value`, `price_tick`,
`contract_multiplier` — **all unchanged**. Sidecar `SYNTH-P020-BOUNDED-INSTRUMENT-V3.json.sha256`
= `69b6f246…` = the file digest. **Nothing else changed.**

**(b) Plan and driver pin V3 and nothing else changed.** Diffed against the V1.5 bytes:
`run_bounded_benchmark.py` — **1 line** (`:25`). `BENCHMARK_PLAN.json` — **4 lines**: the driver's own
pin (`:27`) and the instrument `path`/`sha256`/`record_id` (`:291-293`). No other field.

**(c) `tests/test_sizing_floor.py`.** For each of the five timeframes a synthetic BTC-scale frame
runs through the **real** `preselect_profile.trade_bearing_gate` → real `driver._profile` → real
engine. V3 GREEN (5 passed); V2 RED asserts the exact clause
`no actual trade-bearing 2.1.0 successor result` (`:109`) — 5 passed, included in the 106.
**Dependency probe (mandated):** I re-pointed the V2 (RED) arm at V3 — path, digest and `record_id` —
and all five RED cases became `Failed: DID NOT RAISE <BenchmarkProfileBlocked>` (`5 failed, 5 passed`).
The RED arm therefore genuinely depends on the instrument record, not on the frame or the parameters.

**(d) No owner-policy value changed.** `requested_risk_fraction=Decimal("0.0001")` and
`initial_equity=Decimal("1000000")` are byte-present in `_build_profile` (`:408`, `:371`); the live
owner policy still returns `0.015 / 1.0 / 0.20`. I reproduced the mechanism arithmetically at the
frozen equity and risk fraction (risk = $100/trade):

| stop distance | raw qty | V2 (step 1) | V3 (step 1e-05) | V3 notional @ $100k |
|---|---|---|---|---|
| $100 | 1.0000 | **1** | 1.00000 | $100,000 |
| $500 | 0.2000 | **0** | 0.20000 | $20,000 |
| $1,000 | 0.1000 | **0** | 0.10000 | $10,000 |
| $5,000 | 0.0200 | **0** | 0.02000 | $2,000 |

This reproduces D8-A exactly: under V2 every stop wider than $100 floors to zero, which is why 8 of 9
families signalled and none filled on 1h/2h/4h. It also settles a realism question: V3 adopts row
I-3's `quantity_step` but not its `minimum_notional: 10`. At these quantities the notionals are
$2k–$100k, three orders of magnitude above a $10 venue minimum, so keeping `minimum_notional: 0` is
numerically immaterial here. I record it as an observation, not a finding — D9-A said "nothing else",
and the deviation has no effect at the frozen profile.

**(e) The V1.5 → V1.6 frozen diff touches no selection rule, window, prefix or family order.**
Confirmed by direct key diff (§1): `family_order`, `selection_rule`, `calibration_windows`,
`measurement_inputs`, `timeframe_order`, `family_ordering_rule`, `calibration_window_rule`,
`eligibility_predicate`, `eligibility_run`, `registered_record_total`, `datasets`, `limitations`,
`owner_decision`, `canonicalization`, `selected_manifest_sha256`, `impl_head` — **all byte-identical**.

---

## Findings

**0 REQUIRED. 9 NITs.** None changes an execution outcome; none blocks the shot.

### N6-1 (NIT — unrepaired from round 5 N5-1, second round) — the driver line citation is wrong in the FROZEN artifact
`_execute_trial` is at `run_bounded_benchmark.py:460-528`; the clause region the gate reproduces is
`:470-503`. The artifacts still say `:459-493`:
`PRESELECTION_FROZEN.json:139`, `preselect_profile.py:814`, `:1035`, the inline annotations
`:1057-1099`, `PRESELECTION_PREREG_V1.md:391-396`. The D5 edit shifted the driver by 11 lines.
Severity NIT only because the equivalence is pinned mechanically (`GateEquivalence`) and I verified it
independently over 75 probes — but a reviewer following the citation in the *frozen* artifact lands in
`_prefix_hash`. Fix: recompute the citations, re-freeze.

### N6-2 (NIT — unrepaired N5-2) — `abort` swallows its own error
`preselect_profile.py:679`, `:691`, `:695`: `first_error` is assigned and never raised, returned or
printed. A persistent I/O failure during abort therefore leaves a **zero-byte** reserved file with no
`ABORTED` record and no signal, which contradicts the unconditional wording at
`PRESELECT_RUNBOOK.md:175`. Fix: surface `first_error` in the exit message.

### N6-3 (NIT — unrepaired N5-3; the last declared-but-unenforced input precondition) — cost and funding records expire before the 15m calibration window
`SYNTH-P020-BOUNDED-COST-V1.json` and `SYNTH-P020-BOUNDED-FUNDING-V1.json` both declare
`effective_interval.end_exclusive = 2025-09-22T08:00:00Z`; the 15m calibration window runs
2025-09-22T08:00Z … 2025-10-13T15:45Z, entirely outside. Inert at this HEAD — I verified
`mtc_v2/core/economics.py` contains no interval enforcement — and the HEAD is digest-pinned. But the
three records now disagree about their own validity, and this is the same class of defect
(declared, unchecked input precondition) that produced the V1.4 abort. Fix: ratify extending both
intervals to `2026-05-01T00:00:00Z` under the same decision, or declare them documentation-only.

### N6-4 (NIT — unrepaired N5-4) — `_validate_plan` reports four different failures with one message
`run_bounded_benchmark.py:195-196`: a family outside `family_order`, a duplicate family, a
non-list `family_order`, and a missing derivation block all produce
`PLAN_INVALID: five families must each have sizes 512, 1024, 2048`. Observed in four of my arms.
Diagnosability only.

### N6-5 (NIT — unrepaired N5-5, now one report further behind) — `REPORT.md` banner
`REPORT.md:1` names `REPORT_R2.md`…`REPORT_R5.md`; `REPORT_R6.md` and `REPORT_R7.md` also supersede it.

### N6-6 (NIT — unrepaired N5-6) — dead parameter in the derivation tool
`derive_benchmark_plan.py:103` `derive_trials(frozen, base_plan, selection)` — `base_plan` is never
used in the body; passed at `:160`.

### N6-7 (NIT — NEW, a fresh instance of N4-1) — two live preregistration self-citations drifted in V1.6
`PRESELECTION_PREREG_V1.md:251` cites `preselect_profile.py:456-522` for `verify_frozen_identity`
(now `:549-629`) and `:839-852` for `dataset_lines` (now `:980-992`). Both ranges now overlap nothing.
This is inside live section §(d), not a historical change-log table. Every other live
`preselect_profile.py:N-M` citation I checked against the AST is correct.

### N6-8 (NIT — NEW) — the derivation tool never re-derives the matching
`derive_benchmark_plan.py:79-100` checks that the eligibility and calibration records agree, that the
selection names five distinct frozen families, and that the digests chain — but it never re-runs
`lexicographic_first_matching` over `eligibility_matrix_binary_only`, which is the check
`preselect_profile.verified_selection:1102-1152` performs at write time. A consistently re-written
output **pair** would therefore be accepted by the tool. The one-shot's exclusive-create reservation
and the "never delete" rule are the only defence. Fix: re-derive the matching from the recorded matrix
and refuse on mismatch — roughly ten lines, reusing the frozen family order the tool already loads.

### N6-9 (NIT — NEW, observability) — record drift is indistinguishable from a non-trade-bearing cell
`_records:329-342` raises `BenchmarkProfileBlocked` on a record-digest or symbol-scope mismatch.
`_run_oneshot:1216-1217` catches `BenchmarkProfileBlocked` and records the cell as simply not eligible.
A drifted cost/funding/instrument record therefore fails **every** cell uniformly and produces
`BENCHMARK_PROFILE_BLOCKED` with the matrix discarded — fail-closed and incapable of skewing a
selection (I confirmed the failure is uniform, so no partial matching can arise), but the operator
sees exactly what a genuine block looks like. This is the opacity that cost rounds 4 and 5. Fix: let
identity-class refusals propagate out of the calibration loop instead of being folded into the matrix.

---

## Commands run

All with `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`.

| cwd | command | observed |
|---|---|---|
| `C:/tmp/P020_PRESELECT_20260913` | `sha256sum PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` |
| — | `git -c safe.directory=* -C C:/P020_IMPL_20260912 rev-parse HEAD` | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` |
| `C:/tmp/P020_PRESELECT_20260913` | `sha256sum -c SHA256SUMS.txt` | 13 × `OK` |
| `C:/tmp/P020_PRESELECT_20260913` | `python -m pytest tests -q -p no:cacheprovider` | `106 passed in 4.60s` |
| `C:/tmp/P020_PRESELECT_20260913` | `python -m pytest tests -q -p no:cacheprovider --collect-only` | `106 tests collected` |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` | `python preselect_profile.py --freeze` | `FROZEN_WRITTEN … sha256=cb756020…` + the `LIMITATION` line |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` | `--oneshot` (no token) | `PRESELECT_REFUSED_NO_T0_REVIEW`, exit 2, no files |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` | `--oneshot … 2e67f3f4…` | `PRESELECT_REFUSED_T0_TOKEN_MISMATCH`, exit 2, no files |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` | `--freeze --i-have-t0-review-authorization deadbeef` | usage error |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH/pkg` | `--calibrate`, `--eligibility` | usage error, exit 2 |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH` | `python arms_core.py` | **34/34 PASS**, `FAILED ARMS: NONE` |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH` | `python arms_inputs.py` | **11/11 PASS**, incl. `for_evaluation` 40/40 |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH` | `python arms_drift.py` | **9/9 PASS** (tamper, interval, 10c probe) |
| `C:/tmp/P020_T0R6_OPUS_SCRATCH` | `python arms_plan.py` | **11/11 PASS** (D5) |
| `C:/tmp/P020_PLAN_DERIVE_20260913` | `sha256sum -c SHA256SUMS.txt` | 5 × `OK` |
| `C:/tmp/P020_PLAN_DERIVE_20260913` | `python -m pytest tests -q -p no:cacheprovider` | `15 passed in 0.27s` |
| `C:/tmp/P020_LEAD_20260912/benchmark` | `diff` vs the V1.5 driver/plan bytes | 1 line / 4 lines, as declared |

Selected raw output:

```
PASS arm1 S3: each dataset read exactly ONCE :: {"…15m…": 1, "…1h…": 1, "…2h…": 1, "…4h…": 1, "…1D…": 1}
PASS arm1 T1: frozen artifact read exactly ONCE on the execution path :: reads=1
PASS arm1 T2: BENCHMARK_PLAN.json read exactly ONCE (preflight only) :: reads=1
PASS arm1 T2: every gate call received the SAME plan object :: distinct ids=1
PASS arm2 T1: calibration bound to ACCEPTED bytes, not the swapped file
PASS arm3[second-write] calibration is an ABORTED record :: {"error": "Boom", "kind": "calibration", "status": "ABORTED"}
PASS arm5 S4: gate accepted a sized trade container WITHOUT iterating or indexing it
PASS arm6 R1: gate decision == _execute_trial decision on all 75 probes :: []
PASS armE tampered preselect_profile.py refuses PRESELECT_REFUSED_SOURCE_DRIFT :: PRESELECT_REFUSED_SOURCE_DRIFT: preselect_profile.py
PASS armH ... :: PRESELECT_REFUSED_RECORD_INTERVAL: calibration 15m first_ts outside instrument record interval
PASS item7 for_evaluation accepted every window/prefix boundary (20 windows+prefixes, 40 timestamps) :: accepted=40 refused=[]
PASS item10c probe: pointing the V2 (RED) arm at V3 makes all five RED cases STOP blocking :: 5 failed, 5 passed in 1.40s
```

I wrote only into `C:/tmp/P020_PRESELECT_T0_R6_20260914/opus/` and `C:/tmp/P020_T0R6_OPUS_SCRATCH/`.
I ran no `git status`/`diff`/`add`/`commit`/`checkout` in any repository.

---

## NOT VERIFIED

1. **The real V1.6 outcome.** I did not run the 45-cell matrix or the 15 locked trials, and nothing in
   this review predicts them. `BENCHMARK_PROFILE_BLOCKED` remains a possible and legitimate result —
   in particular on 1D, where the Lead's disclosed smoke found no signal in the 361-row window.
2. **The V1.4-pinned driver bytes (`4b293de6…`)** are not on disk and the brief forbids git history
   inspection, so I did not re-verify the V1.4 → V1.5 D5 diff. I verified V1.5 (`b8a8f255…`) → V1.6
   exactly: one line.
3. **Whether family identities were genuinely withheld** in the D7-A / D8-A diagnostics. I verified
   that the persisted artifacts contain only ABORTED records and that the tool discards the matrix on
   BLOCKED; the chat channel itself is not auditable by me.
4. **Concurrency.** `open(path, "xb")` is an exclusive *create*, not an exclusive *lock*: a concurrent
   shared `open(path, "w")` could write into a reserved-but-empty file before commit. Not a second-run
   path in this tool; not tested on a network share.
5. **The abort double-fault path (N6-2)** was not driven to a genuinely unwritable handle.
6. **Cost/funding interval semantics (N6-3)** cannot be exercised — no engine check exists to trigger.
7. **`runtime_instrument_config` other than `None`** — the pinned records supply none.
8. **Any future HEAD** that begins enforcing cost/funding intervals would abort the run exactly as
   V1.4 did; the pinned HEAD does not.
9. **The 200-bar warmup bound** is justified by reading the three `ema_200` gates, not measured.
10. **Real-world venue fidelity of the synthetic instrument** beyond `quantity_step` — it remains a
    mix of venue-realistic and synthetic values (see §10(d)); immaterial at the frozen profile, but
    not independently validated against the venue.

---

## Summary

Identities computed and matching; the freeze reproduces byte-for-byte; 106 tests pass. Every prior
finding (R1–R6, N-1..N-5, S1–S5, NIT-1, NIT-4, T1–T4, N4-1..N4-4, Sol-4, the interval check, D5, the
derivation tool) is closed against bytes except the documentation residuals listed above. Item 7 — the
round-4 miss — is green on all 40 timestamps with a working negative control, and the one remaining
declared-but-unenforced precondition (cost/funding intervals) is identified and shown inert at the
pinned HEAD. D9-A is a minimal, independently pre-documented input correction: V3 differs from V2 in
three fields, the plan and driver moved four and one line, no owner-policy value changed, and no
selection rule, window, prefix or family order changed. The re-armed shot is owner-ruled and recorded,
and no selection has ever been produced. Twelve RED arms — including the frozen-file swap, the three
commit-failure paths, the hostile trade container, the tampered procedure byte, the out-of-interval
window and the sizing-record dependency probe — all behaved fail-closed.

Nine NITs, six of them unrepaired carry-overs from round 5. None can change an execution outcome.

VERDICT: PASS-WITH-NITS
