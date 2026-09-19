# Independent T0 review — P20-PRE V1.6

Reviewer: exact `gpt-5.6-sol`, xhigh  
Date: 2026-09-14  
Scope: the frozen package at `C:/tmp/P020_PRESELECT_20260913`, the pinned implementation and benchmark/derivation support named by the review brief. All repositories and the package were treated as read-only. Reviewer-only probes and the freeze reproduction were written under `C:/tmp/P020_T0R6_SCRATCH_20260914`.

## Result

I found no REQUIRED defect. The preregistered selection logic, economic-data firewall, identity chain, real-record interval preconditions, D5 plan validation, derivation input binding, and D9-A sizing-floor change are supported by the reviewed bytes and by the required executions. The package test suite passed 106/106 and a scratch freeze reproduced the frozen artifact byte-for-byte.

Three NITs remain: an exclusive create is not an exclusive lock or post-commit integrity check; a second storage failure during ABORTED recovery can still leave a mixed pair despite absolute documentation; and one human-readable benchmark-plan sentence still says the quantity step is `1` although the pinned V3 record says `0.00001`. None changes the executable selection, record pin, requested risk, or gate result.

I did not pass the current frozen digest as an authorization argument, did not execute `--oneshot`, and did not run the benchmark driver with `--run`.

## Verified identities (COMPUTED)

| Identity | Computed value | Result |
| --- | --- | --- |
| `PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | exact expected digest |
| `selected_manifest.json` | `712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a` | exact frozen/brief digest |
| implementation HEAD | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` | exact required HEAD |
| `SHA256SUMS.txt` | 13/13 entries matched; 0 CR bytes; terminal LF present | valid LF manifest |
| scratch freeze | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | byte-identical to package |

The execution preflight independently returned these 19 identities:

| Name | Computed SHA-256 / value |
| --- | --- |
| `BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` |
| `PRESELECTION_PREREG_V1.md` | `39f52ed0fc01bcc1017b36b9f2071ee59a66ecb46a07e89a60b0890c4a605d4c` |
| `PRESELECT_RUNBOOK.md` | `53faa45e583617be11f80cbc1550a3ee806175daa684e8f1620d288e03aab344` |
| `STRATEGY_INPUT_COMPATIBILITY.json` | `3820d859b25a7b8cb1a0b746fc9f0d106d56d13e191d1324390f3bdd2e783c5d` |
| dataset 15m | `472462faf3081027e9fbc791d1d62aeab424481a78860eb4bc5d786d8e50f372` |
| dataset 1h | `888297ddba58206e2bcedece50198c917297b3f514a66e0137a700d78f18f384` |
| dataset 2h | `bf161b20c6f82beb0c3848170198d55e88dadd710ad079e437558f540b1c62bd` |
| dataset 4h | `0181cc1231957e914889ebaabef40e48ae6aca55bd55ce3fe0202fc3fd1287a8` |
| dataset 1D | `9371bc43b8b6f19c3727ef8f4aedde9375e30e6443f01fd5855d56b356a765bc` |
| implementation HEAD | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` |
| `mega_walk_forward.py` | `91a7db44c5cdfbefa31efc44aecc3e6db66f4f0dfb6e8c1aa1d4146a258d1a00` |
| `p020_benchmark_runner.py` | `46b6ce21be52629e0845fef7fd88e5b62ea2e6e03937fa2365ff81f9f7efded2` |
| `p020_economics.py` | `e23a167647fc09b8f226e439d7cbf067dbd53729616d6348f605383cabe08266` |
| `p020_owner_policy.py` | `11237077d555b9267711fef02161c9d228b42fe4c298ec9ec458a8332afc56c7` |
| `p020_simulator.py` | `bfe62a327c1b9af0f4b4543a6064ee8bbc20c102d10a1263caa0b1e2a9752edf` |
| `package.py` | `be9a7a29ceb774205d53048d8367b2cb47339b93b5d7ac26de8f492acbf94d56` |
| `preselect_profile.py` | `c82693d492268944a7b3ed42aebe57a03ce033c3e9e23b4ccc24a60d6931c8d5` |
| `run_bounded_benchmark.py` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` |
| `selected_manifest.json` | `712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a` |

All five calibration-window hashes and all 15 measurement-prefix hashes recomputed from the retained dataset bytes matched the frozen values:

| Timeframe | Window | N=512 | N=1024 | N=2048 |
| --- | --- | --- | --- | --- |
| 15m | `5a9482928bace2dd4eb0b8d9b3d8ecfa2eeabb315fc74438bed21fa4fea73cec` | `de7d720d0bfea6f21d886388085326a7921463e25d4f4926354aa769eb0410ab` | `38f94e7b1284d8f5c435ec6a658721d499f206a4f05027ca07139cf2e6c176c1` | `06da7286af00f6d4d69ae40caa0bf96c2072da35db0f5f95c5669e9ca4b0a21d` |
| 1h | `ec8aa0bda18f554482695c6bbac7aa7cd69a435ad1db13343336526a447e7bd8` | `bce37cff96da136d8b2d4375aecbc197ed19241cd66f4c3965c1c746bf7f3fd2` | `8b0fd23dc69f0aa68c4faf882f459f6948b921a23153bae05714845a979b7466` | `385143699bccdc9301279b54bd73a6b26c12ff96549c260b4358f5ee79143f39` |
| 2h | `dc5876bb085c6e91c7647930b6fc36f37eacecc27a4544ee28c0f73c1f476763` | `7041c16c8908b3640e3ef3c700e5f4ba1f4919bc5cdb2492689aa300b2600051` | `d4e68844e15cc0afa6e37cdd49d924edb2909dea4bf80940a3a209d43b48eb6d` | `d5d67c8cf43cd37f812f2705751e26aa5924fd623a14e3ecdf1a902c9ed7f669` |
| 4h | `d80a4bedfb93f33c9f9d2266fe1b2a70a7c2ce155ff5da935f4e5d4afc61894c` | `2d80d8af4b765f5afc62fa383ab57fd44fdf3b9fd96318ab989ceeb12eff8223` | `2150669eba6952f873835b762dc9fd4a630fb047798a83a64615ae57dfb94e02` | `1c314ef7670d40bd87313dc290ff24ddd18f463e604983637522a110b5c154a0` |
| 1D | `bc763cd09634fa2477310f6b4818916b00a19ac9cd12c7b73d41d662043046c8` | `6302f2d729f90adb20d42f956b6128e7b0edc10a42a45cb2b3e015372a475a1a` | `86d5b2d0bf941321e3040c3fd5e038d8901e60f6374a6daa9c81e57a24078223` | `9de0ef1c165c900936dd12c996e1641c644d63119204dee3a3ae711c12a93c12` |

## T0 decision

### Preregistration and leakage

The live registry contains exactly nine OHLC-compatible `GEN_*` families and 359 records. The frozen order is the required `(grid size, strategy_id)` order, each parameter record is canonical JSON, and the five timeframes, 512/1024/2048 prefixes, windows 2049–4096 (15m/1h/2h/4h) and 2049–2409 (1D), binary predicate, distinct-family lexicographic matching, and 15-trial all-pass rule are implemented at `preselect_profile.py:145-163,259-286,303-443,946-1152,1206-1269`. The corresponding preregistration is at `PRESELECTION_PREREG_V1.md:145-242,358-480,482-542`.

No economic value can select a family: `trade_bearing_gate` reads only `stats.num_trades`, the length of the sized trade container, event count parity, and the literal `projection_source` marker (`preselect_profile.py:1031-1099`). It neither iterates the trade series nor reads/serializes an R, PnL, return, or other statistic. Both calibration and eligibility call that same function (`preselect_profile.py:1213-1216,1246-1249`). Matching is computed from the in-memory Boolean matrix before the measurement trials; neither result files nor an editable handoff are read (`preselect_profile.py:1206-1269`). The no-token and dead-token RED arms refused before reservation.

The current V1.5→V1.6 structural diff leaves `selection_rule`, `family_order`, `calibration_windows`, and `measurement_inputs` equal. The earlier V1.1/V1.3 continuity is recorded in `REPORT_R3.md:258` and `REPORT_R4.md:328`; the current implementation and frozen values agree with those recorded rules. Therefore no selection rule changed from V1.1 through V1.6.

### Real-stack input preconditions and interval check

Using the pinned interpreter, actual V3/cost/funding records, actual manifest CSV bytes, and `EconomicRecords.from_record_paths`, I called `records.instrument.for_evaluation(ts, records.runtime_instrument_config or {})` on the first and last timestamp of each of five calibration windows and 15 prefixes: 20 regions and 40 accepted calls. The accepted range endpoints are included in the transcript below.

Other input conditions were checked as follows:

- `_records` reads all three plan-pinned record paths, checks their SHA-256 values, requires the instrument symbol expected by the plan, and requires cost/funding symbol scopes to contain it (`run_bounded_benchmark.py:311-343`). All three digests and scopes matched.
- `_build_profile` calls `instrument.for_evaluation` with the first frame timestamp and `runtime_instrument_config or {}`, obtains the verified quantity/tick/minimum/interval fields, binds the synthetic provenance and owner policy, and requests `Decimal("0.0001")` (`run_bounded_benchmark.py:346-432`). `_profile` uses that path at `run_bounded_benchmark.py:441-449`.
- `InstrumentRecord.for_evaluation` enforces record text, positive/nonnegative numeric fields, human-review state, interval, and immutable runtime overrides (`C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/instrument.py:197-321`). Actual metadata was symbol `SYNTH-RULE2-01-GREEN`, quantity step `0.00001`, minimum quantity `0`, and minimum notional `0`; runtime config is `None`.
- The raw instrument, cost, and funding JSON records all say `test_only: true`; the cost/funding scopes match the instrument symbol. `test_only` is not carried into or enforced by the `_records`/`_build_profile`/`_profile` branch, so its truth is a byte inspection rather than an exercised engine refusal. Synthetic-only provenance is enforced separately by profile construction.
- A scratch mutation placing the 1D calibration start outside the record interval refused exactly `PRESELECT_REFUSED_RECORD_INTERVAL`.

Positive preconditions for the frozen inputs are exercised. Remaining unexercised input-precondition arms are the individual negative variants of every text/numeric/human-review/runtime-override check, and there is no `test_only` engine branch here to exercise. These omissions do not weaken the positive boundary proof, but are recorded under NOT VERIFIED.

### 1D limitation

The 1D calibration window remains rows 2049–2409: 361 rows and 161 usable rows after the maximum 200-bar warmup. It is recorded and explained at `PRESELECTION_PREREG_V1.md:314-348`, frozen under `limitations[0]`, and printed on the reproduced freeze as accepted under owner decision D1 Option A. The limitation is honest and selection rules remain fixed even if eligibility fails.

### D5 driver and derivation tool

`_validate_plan` validates current hand-written selections and, when present, a derivation `family_order`; it requires exactly five distinct selected families in the allowed family set and sizes 512/1024/2048 (`run_bounded_benchmark.py:95-205`). Its five tests passed, including acceptance of the original plan and a derived order and refusal of outsider, duplicate, and wrong-size cases. The driver contains no `PRESELECTION_FROZEN` read. Reconstructing the V1.4 driver by reversing the documented D5 family-validation block produced `4b293de6c26ae61ffec22c8205b81a1bad0c6561c0c642e19a37596b5fd62736`; the subsequent V1.5→V1.6 driver diff is only the V2→V3 record-path line.

The derivation implementation reads each of eligibility, calibration, base plan, and frozen artifact once and hashes/parses the same buffer (`derive_benchmark_plan.py:30-39,150-170`), validates inputs (`:79-100`), emits `derivation.family_order` and 15 trials (`:67-76,103-147`), and exclusively creates its output (`:174-179`). All 15 tests passed. A swap probe observed one read per input and proved all four emitted digests describe the parsed original buffers. `EXPECTED_FROZEN_SHA256` is the current computed frozen digest (`derive_benchmark_plan.py:12`).

### D9-A record V3 and sizing floor

The parsed V2→V3 diff has exactly three leaf changes: `record_id`, `quantity_step` from `1` to `0.00001`, and the added `provenance.quantity_step_correction`. `minimum_quantity=0`, `minimum_notional=0`, and the effective interval are unchanged. The V3 sidecar digest matches the V3 file: `69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9`.

Compared with the V1.5 pins, `BENCHMARK_PLAN.json` changes only its driver source digest and the instrument record path/id/digest; `run_bounded_benchmark.py` changes only its V2→V3 `RECORD_PATHS` line. The owner-policy source pin is equal and `requested_risk_fraction` remains `0.0001`.

The ten official sizing tests passed. For every timeframe, the real driver/engine/gate produced trade-bearing with V3 and the exact `no actual trade-bearing 2.1.0 successor result` block with V2. Repointing each RED fixture from V2 to V3 made it GREEN, establishing dependence on the record rather than another fixture difference.

## Prior-finding closure table

| Item | Status | Byte/test evidence |
| --- | --- | --- |
| R1 — one shared binary gate | CLOSED | One gate at `preselect_profile.py:1031-1099`, called at `:1213-1216,1246-1249`; full `GateEquivalence` cases passed. |
| R2 — re-derived selection and calibration binding | CLOSED | `verified_selection` re-derives and rejects mismatch at `preselect_profile.py:1102-1152`; `_run_oneshot` uses the in-memory matrix and records the exact calibration payload SHA at `:1224-1269`. |
| R3 — no tool overwrite path | CLOSED | `open(path, "xb")` and `PRESELECT_REFUSED_ALREADY_RUN` at `preselect_profile.py:652-658`; final writes stay on retained handles at `:660-675`. See NIT 1 for external writers. |
| R4 — isolated frames | CLOSED | `io.StringIO` receives only isolated bytes at `preselect_profile.py:965-1028`; wording matches `PRESELECTION_PREREG_V1.md:229-242` and `PRESELECT_RUNBOOK.md:104-112`. |
| R5 — no economic-value read/return | CLOSED | Only count/parity/projection marker at `preselect_profile.py:1031-1099`; hostile non-iterable trade-container test passed. |
| R6 — frozen identity before driver load | CLOSED | HEAD, procedure, prereg/runbook, plan, compatibility, manifest, source pins, datasets and interval at `preselect_profile.py:570-629`; `_run_oneshot` preflight/reservation precede driver load at `:1184-1197`; freeze records observed values at `:720-878`. |
| N-1 — complete refusal table | CLOSED | Complete table at `PRESELECT_RUNBOOK.md:184-205`; source/test refusal inventory agrees. |
| N-2 — warmup citations | CLOSED | `PRESELECTION_PREREG_V1.md:314-348`; implementation maximum warmup commentary/constants at `preselect_profile.py:80-105`. |
| N-3 — no whole-file frame parse | CLOSED | Dataset bytes are read once at `preselect_profile.py:618-628`, then sliced at `:980-1028`; no path-based pandas read on execution path. |
| N-4 — LF checksums | CLOSED | Computed 13/13 entries, zero CR bytes, terminal LF. |
| N-5 — historical report banner | CLOSED | `REPORT.md:1` explicitly marks the V1 report historical and superseded through `REPORT_R5.md`. |
| S1 — single transaction | CLOSED | Matrix, in-memory matching, 15 trials, final paired write at `preselect_profile.py:1165-1279`; CLI exposes only freeze/oneshot at `:1283-1310`. |
| S2 — pre-simulation exclusive reservation | CLOSED | Both paths reserved before simulation and never deleted at `preselect_profile.py:632-714,1184-1197`; ordinary failure tests passed. See NITs 1–2 for adversarial/shared-writer and nested-recovery limits. |
| S3 — one dataset read | CLOSED | Sole reads at `preselect_profile.py:618-628`; reviewer counter saw exactly one per dataset. |
| S4 — `len(trades)` only | CLOSED | Unsized refusal and one length read at `preselect_profile.py:1084-1090`; no iteration/materialization; hostile iterator test passed. |
| S5 — refusal/outcome phases | CLOSED | `PRESELECT_RUNBOOK.md:167-179` and `PRESELECTION_PREREG_V1.md:531-537`. See NIT 2 concerning an absolute nested-failure residue claim. |
| NIT-1 — disjointness at consumption | CLOSED | `assert_disjoint` runs in `calibration_frame` before extraction at `preselect_profile.py:995-1004`. |
| NIT-4 — procedure digest recorded/rechecked | CLOSED | Computed last during freeze at `preselect_profile.py:873-877`, checked before driver load at `:576-590`; source-tamper RED passed. |
| T1 — same frozen bytes hashed and parsed | CLOSED | Exactly one `read_bytes`, digest, comparison, then `json.loads(raw)` at `preselect_profile.py:908-931`; accepted digest is used in both result records in `_run_oneshot`; frozen-swap test passed. |
| T2 — verified plan object executed | CLOSED | Preflight reads/hashes/parses once at `preselect_profile.py:591-629`; returned object passes through `_run_oneshot` to both gate stages; plan-swap test passed. |
| T3 — ordinary commit faults produce two ABORTED records | CLOSED | Commit catches first/second write/truncate/flush faults and calls per-handle recovery at `preselect_profile.py:660-697`; mandated second-write and flush tests produced two ABORTED records. See NIT 2 for a second fault inside recovery. |
| T4 — phase-specific documentation | CLOSED | `PRESELECTION_PREREG_V1.md:531-537,562-575`; `PRESELECT_RUNBOOK.md:167-179`. |
| Opus NIT-A — token did not bind prereg/runbook | ADDRESSED | Both digests are frozen last and rechecked at `preselect_profile.py:583-590,873-877`. |
| Opus NIT-B — exclusive create is not a lock | UNCHANGED NIT | Explicitly disclosed at `PRESELECT_RUNBOOK.md:110`; independently reproduced. See NIT 1. |
| Opus NIT-C — abort failure could skip later handle | ADDRESSED, residual NIT | Per-handle try/close/finally at `preselect_profile.py:677-697` prevents one recovery failure from skipping later handles. A failed recovery write can still leave that file normal/malformed. See NIT 2. |
| N4-1 — stale line citations | CLOSED | Historical locations are explicitly labelled stale and current function names authoritative at `PRESELECTION_PREREG_V1.md:58-59,68-71,89-94`. |
| N4-2 — successful commit did not truncate | CLOSED | Both successful writes truncate before flush at `preselect_profile.py:660-668`. |
| N4-3 — per-handle abort recovery | CLOSED | Independent per-handle recovery/close/finally at `preselect_profile.py:677-697`; later handle recovered in the double-fault probe. |
| N4-4 — prereg/runbook/procedure digest binding | CLOSED | `preselect_profile.py:576-590,873-877`; computed frozen/preflight digests match. |
| Sol-4 — cache-free pytest command | CLOSED | `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` are prescribed at `PRESELECT_RUNBOOK.md:31-36`; all reviewer test commands used them. |
| Instrument interval check | CLOSED | Frozen interval verification occurs at `preselect_profile.py:449-568,628`; 40 real boundary calls passed and an out-of-interval scratch window refused. |
| D5 driver change | CLOSED | Family-set/shape validation at `run_bounded_benchmark.py:95-205`; five tests and current `--validate-plan` passed; no frozen-artifact dependency; reconstructed V1.4 digest matched. |
| Derivation tool | CLOSED | Same-buffer read/hash/parse and emitted family order at `derive_benchmark_plan.py:12,30-39,67-100,103-179`; 15 tests and swap probe passed. |
| D9-A V3 + sizing floor | CLOSED | Exactly three V2→V3 leaf diffs; V3 sidecar/pins match; ten official tests and per-timeframe record-swap probe passed; risk policy and selection fields unchanged. |

## Findings

1. **NIT — Reserved outputs are not locked or verified after commit.** `ReservedOutputs.reserve` uses `open(path, "xb")`, but the retained handle does not deny a shared writer and `commit` does not re-hash/re-read the committed paths (`C:/tmp/P020_PRESELECT_20260913/preselect_profile.py:652-668`). The runbook accurately calls this “not an exclusive lock” (`C:/tmp/P020_PRESELECT_20260913/PRESELECT_RUNBOOK.md:110`), but its nearby statement that a file created after the check cannot be silently replaced (`:129-131`) is broader than the mechanism. On Windows, a reviewer probe opened the already-reserved calibration path after its flush and replaced its contents; eligibility then committed normally. This is not a second-run path in the tool and cannot feed economic results back into matching, but it weakens output integrity against an external same-path writer. Suggested repair: use an OS lock/deny-share primitive for the transaction, or verify both path bytes through independently opened handles after flush and fail closed on mismatch.

2. **NIT — A second storage failure during ABORTED recovery can leave a mixed pair.** `commit` calls `abort` after a final write/flush failure, and `abort` now correctly continues per handle, but it swallows each recovery failure after remembering an unused `first_error` (`C:/tmp/P020_PRESELECT_20260913/preselect_profile.py:660-697`). With an eligibility final-write failure plus a calibration abort-seek failure, the probe left a normal calibration object and an ABORTED eligibility object. That contradicts the unconditional “both ... receive ABORTED” / “both ... contain ABORTED records” language at `PRESELECT_RUNBOOK.md:129-135,171-175` and `PRESELECTION_PREREG_V1.md:503-512,531-537`. This needs no selection-rule change. Suggested repair: make documentation explicitly conditional on successful best-effort recovery and specify malformed/mixed residue under recovery failure; optionally surface `first_error` while retaining the primary exception.

3. **NIT — One benchmark-plan annotation still describes the V2 quantity step.** The executable plan pins the correct V3 path/id/digest, and the engine derives quantity facts from that verified record, but `C:/tmp/P020_LEAD_20260912/benchmark/BENCHMARK_PLAN.json:323` still says “quantity step and lot size Decimal('1')”. V3 is `0.00001`, as the adjacent executable mechanism effectively recognizes (`:324`). This is an audit/documentation inconsistency only; the real driver/engine tests prove the used quantity step comes from V3. Update the sentence and re-pin/re-freeze in a later documentation-only version if desired.

## Commands and exact observed outputs

All Python commands below used `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`, `PYTHONDONTWRITEBYTECODE=1`, and pytest `-p no:cacheprovider`. Git safe-directory configuration was command-local only.

### Hashes, checksum manifest, and HEAD

CWD: `C:/tmp/P020_T0R6_SCRATCH_20260914`

```text
FROZEN_SHA256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
MANIFEST_SHA256=712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a
SHA256SUMS_MATCH=13/13 CR_BYTES=0 TERMINAL_LF=True
b9b72f858dc830a9389517f79da5ea3c1fa6122c
```

The only Git command was exactly:

```text
git -c safe.directory=* -C C:/P020_IMPL_20260912 rev-parse HEAD
```

### Package suite

CWD: `C:/tmp/P020_PRESELECT_20260913`

```text
python -m pytest tests -q -p no:cacheprovider
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 4.01s
```

The targeted authorization/swap/equivalence/no-economic-iteration/tamper/write/flush/one-read tests also ran as a 17-case selection:

```text
17 passed in 0.96s
```

### Freeze reproduction

CWD: `C:/tmp/P020_T0R6_SCRATCH_20260914/freeze_repro`

```text
python preselect_profile.py --freeze
FROZEN_WRITTEN C:\tmp\P020_T0R6_SCRATCH_20260914\freeze_repro\PRESELECTION_FROZEN.json sha256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
EXIT=0
SHA256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
BYTE_EQUAL=True
```

### Authorization RED arms

CWD: `C:/tmp/P020_PRESELECT_20260913`

```text
python preselect_profile.py --oneshot
PRESELECT_REFUSED_NO_T0_REVIEW: --i-have-t0-review-authorization <sha256 of PRESELECTION_FROZEN.json> is required
NO_TOKEN_EXIT=2

python preselect_profile.py --oneshot --i-have-t0-review-authorization 2e67f3f4ea357b4b974313ddd4a427564860e5618f24d48758f07b599da4b614
PRESELECT_REFUSED_T0_TOKEN_MISMATCH: token does not match the frozen artifact digest
DEAD_TOKEN_EXIT=2
```

PowerShell additionally wrapped each native stderr line in a `RemoteException`; the application messages and exits above are exact.

### Real-record interval/precondition probe and interval RED arm

CWD: `C:/tmp/P020_T0R6_SCRATCH_20260914`

```text
python real_preconditions_probe.py
REAL_INTERVAL_ACCEPT 15m calibration 2025-09-22T08:00:00Z .. 2025-10-13T15:45:00Z
REAL_INTERVAL_ACCEPT 15m prefix-512 2025-09-01T00:00:00Z .. 2025-09-06T07:45:00Z
REAL_INTERVAL_ACCEPT 15m prefix-1024 2025-09-01T00:00:00Z .. 2025-09-11T15:45:00Z
REAL_INTERVAL_ACCEPT 15m prefix-2048 2025-09-01T00:00:00Z .. 2025-09-22T07:45:00Z
REAL_INTERVAL_ACCEPT 1h calibration 2024-07-02T17:00:00Z .. 2024-09-26T00:00:00Z
REAL_INTERVAL_ACCEPT 1h prefix-512 2024-04-08T09:00:00Z .. 2024-04-29T16:00:00Z
REAL_INTERVAL_ACCEPT 1h prefix-1024 2024-04-08T09:00:00Z .. 2024-05-21T00:00:00Z
REAL_INTERVAL_ACCEPT 1h prefix-2048 2024-04-08T09:00:00Z .. 2024-07-02T16:00:00Z
REAL_INTERVAL_ACCEPT 2h calibration 2024-10-06T18:00:00Z .. 2025-03-26T08:00:00Z
REAL_INTERVAL_ACCEPT 2h prefix-512 2024-04-19T02:00:00Z .. 2024-05-31T16:00:00Z
REAL_INTERVAL_ACCEPT 2h prefix-1024 2024-04-19T02:00:00Z .. 2024-07-13T08:00:00Z
REAL_INTERVAL_ACCEPT 2h prefix-2048 2024-04-19T02:00:00Z .. 2024-10-06T16:00:00Z
REAL_INTERVAL_ACCEPT 4h calibration 2020-08-15T00:00:00Z .. 2021-07-22T04:00:00Z
REAL_INTERVAL_ACCEPT 4h prefix-512 2019-09-08T16:00:00Z .. 2019-12-02T20:00:00Z
REAL_INTERVAL_ACCEPT 4h prefix-1024 2019-09-08T16:00:00Z .. 2020-02-26T04:00:00Z
REAL_INTERVAL_ACCEPT 4h prefix-2048 2019-09-08T16:00:00Z .. 2020-08-14T20:00:00Z
REAL_INTERVAL_ACCEPT 1D calibration 2025-04-17T00:00:00Z .. 2026-04-12T00:00:00Z
REAL_INTERVAL_ACCEPT 1D prefix-512 2019-09-08T00:00:00Z .. 2021-01-31T00:00:00Z
REAL_INTERVAL_ACCEPT 1D prefix-1024 2019-09-08T00:00:00Z .. 2022-06-27T00:00:00Z
REAL_INTERVAL_ACCEPT 1D prefix-2048 2019-09-08T00:00:00Z .. 2025-04-16T00:00:00Z
REAL_BOUNDARY_CALLS_ACCEPTED=40
RECORD_DIGESTS_MATCH=True
SYMBOL_SCOPE_MATCH=True TEST_ONLY_ALL_TRUE=True RUNTIME_CONFIG=None
METADATA symbol=SYNTH-RULE2-01-GREEN qty_step=1e-05 min_qty=0.0 min_notional=0.0
INTERVAL_RED=PRESELECT_REFUSED_RECORD_INTERVAL: calibration 1D first_ts outside instrument record interval
FROZEN_BYTES_SHA256=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
PLAN_BYTES_SHA256=c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7
```

### Benchmark-driver and derivation tests

CWD: `C:/tmp/P020_LEAD_20260912/benchmark`

```text
python -m pytest tests -q -p no:cacheprovider
.....                                                                    [100%]
5 passed in 0.05s

python run_bounded_benchmark.py --validate-plan
PLAN_VALID: frozen manifest, selections, hashes, and 15-trial shape verified
```

CWD: `C:/tmp/P020_PLAN_DERIVE_20260913`

```text
python -m pytest tests -q -p no:cacheprovider
...............                                                          [100%]
15 passed in 0.20s
```

Derivation swap probe, CWD `C:/tmp/P020_T0R6_SCRATCH_20260914`:

```text
DERIVATION_SWAP_PARSED_ORIGINAL=True
DERIVATION_INPUT_READ_COUNTS={'eligibility.json': 1, 'calibration.json': 1, 'base.json': 1, 'frozen.json': 1}
DERIVATION_DIGESTS_MATCH_PARSED_BYTES eligibility=True calibration=True base=True frozen=True
DERIVATION_FAMILY_ORDER=['GEN_A', 'GEN_B', 'GEN_C', 'GEN_D', 'GEN_E', 'GEN_F']
DERIVATION_TRIALS=15
EXPECTED_FROZEN_SHA256_CURRENT=cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126
```

### D9-A structural and sizing tests

CWD: `C:/tmp/P020_PRESELECT_20260913`

```text
python -m pytest tests/test_sizing_floor.py -q -p no:cacheprovider
..........                                                               [100%]
10 passed in 1.45s
```

Structural/record-swap probe, CWD `C:/tmp/P020_T0R6_SCRATCH_20260914`:

```text
V2_V3_DIFF_COUNT=3
V2_V3_DIFF provenance.quantity_step_correction: '<MISSING>' -> {'from': 1, 'to': 1e-05, 'reason': 'the V1/V2 step of one whole contract floored every risk-sized order on 1h/2h/4h/1D to zero under the owner risk fraction 0.0001 (D8-A diagnostic, LEAD_TERMINAL_ELIG15.md); venue-realistic Hyperliquid BTC step per 03_PRODUCTION_CLOSURE_MATRIX.md:32 row I-3; owner ratification OD-20260914-P020-RECORD-V3-1 (chat: D9 A)', 'ratified_by': 'Baris Semaay', 'ratified_at_utc': '2026-09-14T12:59:00Z'}
V2_V3_DIFF quantity_step: 1 -> 1e-05
V2_V3_DIFF record_id: 'SYNTH-P020-BOUNDED-INSTRUMENT-V2' -> 'SYNTH-P020-BOUNDED-INSTRUMENT-V3'
V3_SIDECAR_MATCH=True 69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9
V15_V16_FROZEN_DIFF_COUNT=9
V15_V16_FROZEN_DIFF artifact_version: 'p020-preselection-frozen-v1.5' -> 'p020-preselection-frozen-v1.6'
V15_V16_FROZEN_DIFF instrument_record_interval.record_id: 'SYNTH-P020-BOUNDED-INSTRUMENT-V2' -> 'SYNTH-P020-BOUNDED-INSTRUMENT-V3'
V15_V16_FROZEN_DIFF instrument_record_interval.sha256: '1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15' -> '69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9'
V15_V16_FROZEN_DIFF prereg_sha256: '3f2ae546cd3a78111bb3eeb05e3a5f69163711b7515e8a664cd8620f28b62eab' -> '39f52ed0fc01bcc1017b36b9f2071ee59a66ecb46a07e89a60b0890c4a605d4c'
V15_V16_FROZEN_DIFF procedure_code_sha256: '54f35c8c82aea844637710eb74d490381dc0aeb071588100e76923ec3c31c877' -> 'c82693d492268944a7b3ed42aebe57a03ce033c3e9e23b4ccc24a60d6931c8d5'
V15_V16_FROZEN_DIFF runbook_sha256: '63874fc578579b4ae5ce2debfa39fbd453739e912d1740f9686584e83eae138d' -> '53faa45e583617be11f80cbc1550a3ee806175daa684e8f1620d288e03aab344'
V15_V16_FROZEN_DIFF source_pins.BENCHMARK_PLAN.json: '8cf52e3d2a91cccdb1e36661f4f97c2b0f165725d4cf3841d4d252fe6fd5b448' -> 'c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7'
V15_V16_FROZEN_DIFF source_pins.run_bounded_benchmark.py: 'b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3' -> '3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324'
V15_V16_FROZEN_DIFF supersedes: 'p020-preselection-frozen-v1.4' -> 'p020-preselection-frozen-v1.5'
V15_V16_STABLE selection_rule=True
V15_V16_STABLE family_order=True
V15_V16_STABLE calibration_windows=True
V15_V16_STABLE measurement_inputs=True
V15_V16_PLAN_DIFF_COUNT=4
V15_V16_PLAN_DIFF implementation_sources.run_bounded_benchmark.py.sha256: 'b8a8f2552aa138d60847d48bbc328436e11c6bbee11c8b1668553e79e4a332f3' -> '3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324'
V15_V16_PLAN_DIFF p020_profile.records.instrument.path: 'C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json' -> 'C:/tmp/P020_LEAD_20260912/benchmark/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json'
V15_V16_PLAN_DIFF p020_profile.records.instrument.record_id: 'SYNTH-P020-BOUNDED-INSTRUMENT-V2' -> 'SYNTH-P020-BOUNDED-INSTRUMENT-V3'
V15_V16_PLAN_DIFF p020_profile.records.instrument.sha256: '1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15' -> '69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9'
V15_V16_DRIVER_CHANGED_LINES=['    "instrument": ROOT / "SYNTH-P020-BOUNDED-INSTRUMENT-V2.json",', '    "instrument": ROOT / "SYNTH-P020-BOUNDED-INSTRUMENT-V3.json",']
RECONSTRUCTED_V14_DRIVER_SHA256=4b293de6c26ae61ffec22c8205b81a1bad0c6561c0c642e19a37596b5fd62736
OWNER_POLICY_STABLE requested_risk_fraction=0.0001 source_pin_equal=True
SIZING_RED 15m=BENCHMARK_PROFILE_BLOCKED: no actual trade-bearing 2.1.0 successor result for sizing-floor-15m
SIZING_RECORD_SWAP_GREEN 15m=TRADE_BEARING
SIZING_RED 1h=BENCHMARK_PROFILE_BLOCKED: no actual trade-bearing 2.1.0 successor result for sizing-floor-1h
SIZING_RECORD_SWAP_GREEN 1h=TRADE_BEARING
SIZING_RED 2h=BENCHMARK_PROFILE_BLOCKED: no actual trade-bearing 2.1.0 successor result for sizing-floor-2h
SIZING_RECORD_SWAP_GREEN 2h=TRADE_BEARING
SIZING_RED 4h=BENCHMARK_PROFILE_BLOCKED: no actual trade-bearing 2.1.0 successor result for sizing-floor-4h
SIZING_RECORD_SWAP_GREEN 4h=TRADE_BEARING
SIZING_RED 1D=BENCHMARK_PROFILE_BLOCKED: no actual trade-bearing 2.1.0 successor result for sizing-floor-1D
SIZING_RECORD_SWAP_GREEN 1D=TRADE_BEARING
```

### Residual robustness RED probes

CWD: `C:/tmp/P020_T0R6_SCRATCH_20260914`

```text
python residual_output_probe.py
CONCURRENT_EXTERNAL_WRITE=SUCCEEDED
CONCURRENT_FINAL_CALIBRATION=b'EXTERNAL_AFTER_FLUSH'
CONCURRENT_FINAL_ELIGIBILITY=b'{"kind":"eligibility"}\n'
DOUBLE_FAULT_RAISED=synthetic final write failure
DOUBLE_FAULT_CALIBRATION={'kind': 'calibration'}
DOUBLE_FAULT_ELIGIBILITY={'error': 'OSError', 'kind': 'eligibility', 'status': 'ABORTED'}
DOUBLE_FAULT_HANDLES_LEFT={}
```

## NOT VERIFIED

- The full 45 real calibration cells, their matching, and the 15 real measurement-prefix trials were not run. This was required: the current digest was never supplied to `--oneshot`. Their economic/trade-bearing outcomes remain unknown.
- The benchmark driver was not run with `--run`; interrupted/resumed equivalence and any measurement outputs were not re-evaluated here.
- I verified the Lead reproduction document reports family-order[0] trade-bearing on 15m/1h/2h/4h and blocked on 1D, but I did not independently rerun that real-simulation smoke because the mandated reviewer precondition probe expressly used no `_profile` or `simulate_slice`. In particular, whether any V3 family makes 1D trade-bearing remains unknown.
- I did not execute every negative `InstrumentRecord.for_evaluation` branch (bad record text, each invalid numeric field, human-review failure, and every runtime override mutation). Positive first/last boundary calls and actual record facts all passed. `test_only` is true in all three records but is not an engine branch in `_records`/`_build_profile`/`_profile`.
- The output-lock and nested recovery findings were demonstrated on reviewer scratch paths. I did not attempt an external write against the package's real output paths.

VERDICT: PASS-WITH-NITS
