# W188 Kernel Resume Report

## Verdict

**SAFE KERNEL OBLIGATIONS IMPLEMENTED; ACCEPTANCE STOPPED ON TABLE/DESIGN FINDINGS.** The refreshed
v1.9 bundle verifies at seal `1beaca483f0c79201f950c711ee7407cf6bac9e4f149b50039155b84d854fe47`,
the corrected-vNext suite is green, and frozen legacy behavior remains byte-exact. Direct execution
through the repaired harness measures **11/17 MATCH**. The six remaining mismatches contain no
`KERNEL-SHORT`: three are `GOLDEN-OVER` and three are `DESIGN-GAP`, so the lane stopped without
editing sealed tables or inventing a contract.

Finding count: **6 remaining gate mismatches: 3 GOLDEN-OVER and 3 DESIGN-GAP; 2 additional
source/state discrepancies recorded.**

Evidence-path shorthand used below is exact: `core/...` and `tests/...` expand under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/`; `contracts/...` expands under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/`; `P012_FRESH_DESIGN_V1.md` and
`LANE_W188_KERNEL_RESUME.md` expand under `C:\tmp\LANE_PROMPTS_20260828\`.

This was a **T1** product-code lane on
`feature/wp-p0-12-corrected-vnext-20260831`, the branch fixed by the lane specification
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W188_KERNEL_RESUME.md:3-5`); it changed only the explicitly authorized corrected
kernel/harness/tests plus the required Phase-A bundle refresh. Live/scheduled dependency status is
**NOT VERIFIED**: the selected stage handoff is dated and does not describe WP-P0-12
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/HANDOFF.md:3-9`). No trading, host, deployment, credential,
Pine, adapter, schema, or parity scope was used. The repository requires feature-branch work and
explicit staging (`AGENTS.md:38-49`).

## Phase A - sealed bundle refresh

The repository bundle was compared with `C:\tmp\P012_CONTRACT_TABLES_W127` before implementation.
Of 38 mapped bundle members, 33 were byte-identical; the exact five differing source members were
copied: `CONTRACT_TABLES_MANIFEST.json`, `DERIVATIONS.md`, `scenario_catalog.json`,
`implementation_anchor.json`, and `golden/corrected_vnext/RULE2-05-RED.json`. The anchor sidecar was
then updated to the copied anchor's exact SHA-256. This was the refresh authorized before kernel work
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W188_KERNEL_RESUME.md:37-53`).

Independent verification recomputed all **19/19** manifest member digests and byte counts, then
recomputed the manifest-defined sorted `path:sha256` seal. Stored and computed values both equal
`1beaca483f0c79201f950c711ee7407cf6bac9e4f149b50039155b84d854fe47`; the manifest records that
seal and states that all member digests were measured at seal time
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:332-334`).
All **17/17** RED/GREEN catalog `expected_artifacts["2.0.0"].digest` values were also independently
recomputed against their on-disk goldens. The refreshed RULE2-05-RED catalog binding is present at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:347-375`.

Refresh commit: `608494e8` - `chore(mtc-v2): refresh resealed contract bundle`.

## Obligation-by-obligation disposition

The authoritative v1.9 decision schema is flat and closed
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:999-1036`), and its required follow-up kernel
delta is enumerated at `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1237-1265`.

| # | Design authority | Final disposition |
|---:|---|---|
| 1 | Event identity on all six containers (`P012_FRESH_DESIGN_V1.md:1009-1014`) | Already complete; every serializer emits `kernel_semantics_version` (`core/results.py:465-474`, `:506-529`, `:533-551`, `:581-590`, `:625-635`, `:655-669`). |
| 2 | Flat decisions; no `details` wrapper (`P012_FRESH_DESIGN_V1.md:1001-1021`) | Already complete at the surface boundary; payload members are flattened and unknown members refuse (`core/results.py:442-475`). |
| 3 | Common members, conditional timestamp, no lifecycle id (`P012_FRESH_DESIGN_V1.md:1003-1021`) | Already complete in the same closed serializer (`core/results.py:455-474`). |
| 4 | Non-empty trail and section-3 order (`P012_FRESH_DESIGN_V1.md:1045-1050`) | Completed for RULE2-05: sizing is now evaluated and sequenced on both rows, including the owner-ruled RED zero branch (`core/economics.py:633-682`; `contracts/DERIVATIONS.md:2057-2060`). |
| 5 | Closed reason vocabulary and no redundant reasons (`P012_FRESH_DESIGN_V1.md:1023-1050`) | Already complete; removed reasons are filtered and unknown reasons refuse (`core/results.py:388-456`). |
| 6 | `SIZING_COMPUTED` exact payload (`P012_FRESH_DESIGN_V1.md:1026-1030`) | Completed: corrected sizing always derives from final fill, emits the required row, and normalizes zero fee cash without a negative-zero token (`core/economics.py:633-682`, `:307-318`). |
| 7 | Min-notional admit/refuse predicate (`P012_FRESH_DESIGN_V1.md:228-243`, `:1030-1031`) | Tightened to the exact strict comparison, including zero-notional equality admission (`core/economics.py:643-682`). |
| 8 | Kernel-owned instrument validation/refusal (`P012_FRESH_DESIGN_V1.md:1032-1033`) | Completed in `Runner._bind_corrected_instrument`; the harness now routes by owning DEF instead of synthesizing a scenario-id row (`core/runner.py:459-500`; `tests/corrected_vnext/verify_bceg.py:616-630`). |
| 9 | Protective-stop decision members and finite long vocabulary (`P012_FRESH_DESIGN_V1.md:1034`) | Existing long behavior retained; unmapped short tokens are no longer emitted while short execution behavior remains available (`core/economics.py:783-849`). |
| 10 | Collision receipt and conditionals (`P012_FRESH_DESIGN_V1.md:1035`) | Existing DEF-P012-06 receipt retained; only the named long ordering tokens can be serialized (`core/economics.py:850-887`). |
| 11 | Funding eligibility terminal reason (`P012_FRESH_DESIGN_V1.md:1036`) | Already complete (`core/economics.py:1092-1121`). |
| 12 | Closed fill fields and `{GAP_OPEN, STOP_TOUCH}` (`P012_FRESH_DESIGN_V1.md:1088-1115`) | Completed by replacing `INTRABAR_TOUCH` with `STOP_TOUCH`; conditional serializer checks remain intact (`core/exits.py:472-493`; `core/results.py:478-529`). |
| 13 | Closed exit fields and protective-only trigger (`P012_FRESH_DESIGN_V1.md:1117-1126`) | Already complete (`core/results.py:639-670`). |
| 14 | Seven required RESULT keys; unavailable metrics null/empty (`P012_FRESH_DESIGN_V1.md:1130-1139`, `:1228-1234`) | Completed with present `metrics: null`; no marker or populated metrics object is emitted (`core/results.py:937-960`). |
| 15 | Closed conditional RESULT members (`P012_FRESH_DESIGN_V1.md:1141-1154`) | Existing conditions retained; RULE2-08-RED no longer receives invented guard output (`tests/corrected_vnext/verify_bceg.py:673-686`). |
| 16 | Window-scoped realized-equity endpoints (`P012_FRESH_DESIGN_V1.md:1067-1084`) | Already complete and retained (`core/results.py:927-945`). |
| 17 | Guard closed shape and exact hyphenated basis (`P012_FRESH_DESIGN_V1.md:1156-1172`) | Completed: both runner snapshots now emit `GROSS-MINUS-FEES`; RULE2-08-RED guards are omitted (`core/runner.py:296-303`, `:1285-1294`; `tests/corrected_vnext/verify_bceg.py:673-686`). |
| 18 | Structured refusal objects; no free-form detail (`P012_FRESH_DESIGN_V1.md:1174-1185`) | Already complete and retained in the closed refusal/decision serializers (`core/results.py:397-475`, `:951-960`). |

The three GM46 unknowns were checked rather than assumed. Fee rows contain the design's 15 fields
plus common version identity, and funding rows contain the 18 design fields plus common version
identity (`core/results.py:555-635`; design `P012_FRESH_DESIGN_V1.md:374-382`, `:420-429`). Run
manifest identity pins are populated from verified records (`core/results.py:128-189`), and
`net_trade_pnl` is gross plus linked fee and funding cash deltas (`core/results.py:680-725`; design
`P012_FRESH_DESIGN_V1.md:384`). Regression tests lock the fee and manifest member sets
(`tests/corrected_vnext/contracts/selftests/test_results_corrected.py:86-142`).

Implementation commit: `a37db306` - `fix(mtc-v2): complete v1.9 safe kernel obligations`.

## Corrected gate measurement

The repaired harness has landed: its comparison pipeline calls `execute_corrected_scenario()` and
then `compare_scoped_expected()` (`tests/corrected_vnext/verify_bceg.py:1315-1327`). The canonical
command was run first:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
```

It exited 1 with `BOUNDED_CORRECTION_EVIDENCE_REFUSED / BASELINE_SEAL_IDENTITY_MISMATCH` and detail
`1beaca483f0c...`. The check executes before the per-scenario loop
(`tests/corrected_vnext/verify_bceg.py:968`, `:1315-1327`) because the frozen baseline manifest still
consumes `02b47a8e...` (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`). Therefore the
17-row table below was measured by directly invoking the repaired harness's own executor and scoped
comparator for every RED/GREEN catalog row. No unrepaired or golden-as-observed pipeline was used.

Canonical node notation is the harness comparator's exact output: `I` is integer, `S` is a
length-tagged Base64 string, and `O` is an object (`tests/corrected_vnext/verify_bceg.py:717-760`).

| Scenario | Result | First pointer | Observed | Golden | Classification |
|---|---|---|---|---|---|
| RULE2-01-RED | MATCH | - | - | - | MATCH |
| RULE2-01-GREEN | MATCH | - | - | - | MATCH |
| RULE2-02-RED | MATCH | - | - | - | MATCH |
| RULE2-02-GREEN | MATCH | - | - | - | MATCH |
| RULE2-03-RED | MATCH | - | - | - | MATCH |
| RULE2-03-GREEN | MATCH | - | - | - | MATCH |
| RULE2-04-RED | MISMATCH | `/RESULT_SURFACE/trades/0/exit_fill_price` | absent | `I:90` | **DESIGN-GAP** - lifecycle trades are required, but their member set is not closed (`P012_FRESH_DESIGN_V1.md:480`, `:1130-1139`). |
| RULE2-04-GREEN | MATCH | - | - | - | MATCH |
| RULE2-05-RED | MATCH | - | - | - | MATCH |
| RULE2-05-GREEN | MATCH | - | - | - | MATCH |
| RULE2-06-RED | MISMATCH | `/EVENT_SURFACE/decision_events/2/touched_exit_ids/0` | `S:4:U1RPUA==` (`STOP`) | `S:11:VEFSR0VULU5FQVI=` (`TARGET-NEAR`) | **DESIGN-GAP** - the chosen target order is fixed, but the order of the all-touched receipt is not (`P012_FRESH_DESIGN_V1.md:339-353`, `:1035`). |
| RULE2-06-EQUAL-PRICE-RED | MISMATCH | `/EVENT_SURFACE/decision_events/2/touched_exit_ids/0` | `S:4:U1RPUA==` (`STOP`) | `S:11:VEFSR0VULU5FQVI=` (`TARGET-NEAR`) | **DESIGN-GAP** - same unset all-touched ordering (`P012_FRESH_DESIGN_V1.md:339-353`, `:1035`). |
| RULE2-06-GREEN | MATCH | - | - | - | MATCH |
| RULE2-07-RED | MISMATCH | `/RESULT_SURFACE/guards/guard_pnl_basis` | `S:16:R1JPU1MtTUlOVVMtRkVFUw==` (`GROSS-MINUS-FEES`) | `S:16:R1JPU1NfTUlOVVNfRkVFUw==` (`GROSS_MINUS_FEES`) | **GOLDEN-OVER** - v1.9 requires the hyphenated value and directs tables to repair it (`P012_FRESH_DESIGN_V1.md:1164-1167`, `:1228-1234`). |
| RULE2-07-GREEN | MISMATCH | `/RESULT_SURFACE/guards/guard_pnl_basis` | `S:16:R1JPU1MtTUlOVVMtRkVFUw==` (`GROSS-MINUS-FEES`) | `S:16:R1JPU1NfTUlOVVNfRkVFUw==` (`GROSS_MINUS_FEES`) | **GOLDEN-OVER** - same explicit table defect (`P012_FRESH_DESIGN_V1.md:1164-1167`, `:1228-1234`). |
| RULE2-08-RED | MISMATCH | `/RESULT_SURFACE/guards` | absent | `O:4` | **GOLDEN-OVER** - v1.9 directs removal unless a separate threshold amendment is approved (`P012_FRESH_DESIGN_V1.md:1228-1234`). |
| RULE2-08-GREEN | MATCH | - | - | - | MATCH |

Measured summary: **11/17 MATCH, 6/17 MISMATCH; 0 KERNEL-SHORT, 3 GOLDEN-OVER, 3 DESIGN-GAP.**
Per the lane's stop rules, a tables owner must repair/reseal the three GOLDEN-OVER rows, and the
owner must settle the trade-member and `touched_exit_ids` ordering questions before kernel work can
continue (`C:\tmp\LANE_PROMPTS_20260828\LANE_W188_KERNEL_RESUME.md:68-75`).

## Verification

| Measurement | Before implementation | After implementation |
|---|---:|---:|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | **218 passed** | **220 passed** |
| Frozen legacy replay | **17/17 scenarios; 34/34 surfaces exact** | **17/17 scenarios; 34/34 surfaces exact** |

The legacy replay loaded the frozen driver's `prepare_scenario`, `run_legacy`, and `canonical_bytes`
functions and compared the two in-memory surfaces per scenario directly with
`C:\tmp\P012_BASELINE_RUN\out`; it wrote no artifacts. The driver defines the capture and canonical
surface return at `C:\tmp\P012_BASELINE_RUN\run_baseline.py:746-896` and input preparation at
`:899-948`.

Additional checks:

- Focused changed-area tests: **141 passed**.
- Built-in verifier selftest: exit 0, **18 checks** (3 `PASS`, 14 `DETECTED`, 1
  `DETECTED:/a/1`); its comparator excludes only literal expected `BLOCKED-` cells
  (`tests/corrected_vnext/verify_bceg.py:717-760`).
- `git diff --check`: clean before the implementation commit.
- Proving coverage includes zero-quantity economics and STOP_TOUCH
  (`tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:647-680`), kernel-owned instrument
  validation/refusal (`tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:275-311`),
  guard spelling (`tests/corrected_vnext/contracts/selftests/test_runner_corrected.py:99-117`), and
  zero-quantity position application
  (`tests/corrected_vnext/contracts/selftests/test_position_manager_corrected.py:90-119`).

## Discrepancies

1. GM46 says RULE2-05-RED must withhold sizing
   (`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM46_KERNEL_WORKLIST.md:19-21`, `:80-81`). That was
   superseded by owner addendum 28 decision 68: section 7 governs, quantity is zero, and the sizing
   row is derivable (`contracts/DERIVATIONS.md:2057-2060`, `:2424-2442`). The repository authority
   therefore wins, and the implementation emits `SIZING_COMPUTED` on RED.
2. The repaired canonical harness is current, but the supplied frozen baseline manifest still pins
   seal `02b47a8e...`, while the refreshed implementation anchor pins `1beaca483f0c...`
   (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`;
   `contracts/implementation_anchor.json:2-4`). This prevents a canonical per-scenario gate run even
   though the repaired executor/comparator is present.

## Explicitly not performed

- No golden, catalog, manifest, seal, input, or sidecar was edited after the exact Phase-A source
  refresh. The three GOLDEN-OVER findings were not repaired because only the tables family may
  author/reseal them (`LANE_W188_KERNEL_RESUME.md:57-65`; design `P012_FRESH_DESIGN_V1.md:1189-1235`).
- No behavior was invented for the DESIGN-GAP rows; no third pass was attempted
  (`LANE_W188_KERNEL_RESUME.md:68-75`).
- No baseline artifact, observed artifact, probe, backtest, optimization, server, launcher, or result
  artifact was generated.
- No push, pull request, merge, deployment, host contact, credential operation, or live trading action
  was performed.

## Final reconciliation

After the report commit, the worktree was clean and the feature branch was **ahead 28 / behind 1**
relative to `origin/master`. The one master-only commit is `4ca0e5e8`; it changes only the WP-V2A-03
dependency row in the triage delivery plan, outside every W188 path
(`4ca0e5e8:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:695-702`).
It was not merged into this lane: repository policy requires eventual integration through an
up-to-date PR and forbids overwriting foreign work (`AGENTS.md:48-57`). This reconciliation-note
commit makes the final branch state **ahead 29 / behind 1**. Durable claim status remains **NOT
VERIFIED** because `_AI_MEMORY/SESSION_LOCK.md` is only a mirror, not the guard, and the planned
mechanical claim check does not exist (`AGENTS.md:50-56`); no tracker was modified.

## Commits

1. `608494e8` - `chore(mtc-v2): refresh resealed contract bundle`
2. `a37db306` - `fix(mtc-v2): complete v1.9 safe kernel obligations`

The report itself is committed separately below this implementation history.
