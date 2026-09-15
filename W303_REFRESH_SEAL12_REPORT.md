# W303 re-seal #12 in-repo copy refresh report

Date: 2026-09-03
Actor: Codex implementer lane
Status: **COPY COMPLETE; CANONICAL GATE REFUSED BEFORE PROBE EVALUATION**
Finding count: **4** (one observed gate blocker, one additional stale-size finding not reached by
the one run, one receipt-persistence finding, and one stale-provenance-text finding).

## Scope and preflight

The lane authorized a byte-for-byte refresh from `C:\tmp\P012_CONTRACT_TABLES_W127`, one commit
with the prescribed message, one canonical gate run, and a committed receipt/report
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:3-29`). The prerequisite
marker existed, the active branch was `feature/wp-p0-12-corrected-vnext-20260831`, and the initial
worktree was clean; these were measured before the first write as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:4-7`). No other agent or
CLI was invoked (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

The prompt's shortened `mtc_v2/...` path does not exist at `C:\WP012BUILD\mtc_v2`; repository
discovery located the copies under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/`. The copied
manifest identifies the expected bundle at its first three lines
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1-3`).
This repository-path discrepancy is recorded below under C-2
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).

The baseline regeneration had finished: its manifest consumes seal
`83bbe48c51d0acf78b47c7f5891d78a8b6e1a5dabb98c92673dda224a4597fb2`, records 17 completed
scenarios and 36 output files, and names `C:\tmp\P012_BASELINE_RUN\out` as its output root
(`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13-34`). No baseline byte was created or
changed in this lane.

## Byte-for-byte copy evidence

`Get-FileHash -Algorithm SHA256` was run on each source and destination after the copy and again
after the first commit. All three pairs were equal. Each cited file was read from line 1 and hashed
over its complete bytes.

| File | Source SHA-256 | Destination SHA-256 | Equal | Evidence |
|---|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `ee38b33475dde8cfbb01349a524eaca79b7b7690a6f346f4586afc06c5699965` | `ee38b33475dde8cfbb01349a524eaca79b7b7690a6f346f4586afc06c5699965` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1` |
| `scenario_catalog.json` | `2e10819f45648653f3f43655c9ba26556472d782da9c95923af7fac96a6e1000` | `2e10819f45648653f3f43655c9ba26556472d782da9c95923af7fac96a6e1000` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1` |
| `DERIVATIONS.md` | `fe385afbc8edd15696ad6288836a2eac33d44e4316d5f7e465ff80f63d59c135` | `fe385afbc8edd15696ad6288836a2eac33d44e4316d5f7e465ff80f63d59c135` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\DERIVATIONS.md:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:1` |

Independent rehashing of all 19 `files[]` members found zero SHA-256 mismatches and recomputed the
recorded seal exactly. The copied manifest records the re-seal #12 identity and Lead act at
`CONTRACT_TABLES_MANIFEST.json:751-773`, and the appended nine-probe digest table is at
`DERIVATIONS.md:3975-3989`.

Measured `git diff --stat` before the first commit:

```text
 .../contracts/CONTRACT_TABLES_MANIFEST.json        | 38 +++++++++++++--
 .../tests/corrected_vnext/contracts/DERIVATIONS.md | 17 +++++++
 .../contracts/scenario_catalog.json                | 54 +++++++++++-----------
 3 files changed, 77 insertions(+), 32 deletions(-)
```

The three staged Git blobs were also compared with `git hash-object --no-filters` over the source
files and were byte-identical. The prescribed first commit is
`0942683ce5d131aa758df185e5ca8af61e658d62` with message
`chore(mtc-v2): refresh in-repo bundle copies to re-seal #12`; the required message comes from
`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:16-17`.

## Canonical gate — exactly one invocation

The only invocation was:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN --output C:\WP012BUILD\W303_GATE_RECEIPT.json
```

The shell wrapper surfaced a non-zero status as exit 1. The exact child-process exit code is
**NOT VERIFIED**. The persisted receipt is the JSON object printed by that one run
(`W303_GATE_RECEIPT.json:1-8`).

### Full refusal list

The run emitted a singular preflight `refusal` object rather than the later-stage `refusals` array,
so the full observed refusal list contains exactly one item:

1. `EXPECTED_MEMBER_DIGEST_MISMATCH` — `DERIVATIONS.md`
   (`W303_GATE_RECEIPT.json:4-7`).

The cause is a size-field mismatch, not a SHA-256 mismatch. The copied manifest records the current
SHA-256 values but retains the old byte counts (`CONTRACT_TABLES_MANIFEST.json:284-293`). Direct
whole-file measurements produced:

| Member | Recorded bytes | Actual bytes | Recorded SHA-256 equals actual | Gate disposition |
|---|---:|---:|---|---|
| `DERIVATIONS.md` | 277385 | 279613 | yes | observed refusal |
| `scenario_catalog.json` | 46256 | 47759 | yes | not reached by the one run |

These same two stale byte counts were already recorded by W300
(`C:\tmp\LANE_PROMPTS_20260828\W300_BASELINE_REGEN_REPORT.md:130`). The verifier checks the digest
and `st_size` in one condition and emits `EXPECTED_MEMBER_DIGEST_MISMATCH` if either differs
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1984-1995`).
Changing either manifest value was forbidden because W303 required a byte-for-byte source copy
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:7-13`).

## Probe table

The full-gate path calls `validate_catalog`, which first calls `validate_sealed_producers`; only
after that check succeeds does it load and iterate the scenario catalog
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2041-2051,3243-3247`).
Because the sealed-producer check refused on `DERIVATIONS.md`, **0 of 10 probes were evaluated**.
`DETECTED`/`NOT DETECTED` is therefore **NOT VERIFIED** for every row; the refusal is not evidence
that any variant escaped detection.

| Probe | Target | Declared failed check | Canonical-gate observation | Catalog evidence |
|---|---|---|---|---|
| `PROBE-P012-01-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:735-753` |
| `PROBE-P012-01-B` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:756-774` |
| `PROBE-P012-02-A` | KERNEL | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:777-795` |
| `PROBE-P012-03-A` | INPUT | `RECORD_IDENTITY_PREFLIGHT` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:798-816` |
| `PROBE-P012-04-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:819-837` |
| `PROBE-P012-05-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:840-858` |
| `PROBE-P012-05-B` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:861-879` |
| `PROBE-P012-06-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:882-900` |
| `PROBE-P012-07-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:903-921` |
| `PROBE-P012-08-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:924-942` |

The prompt's predicted KERNEL/producer, RULE2-06/RULE2-08 harness, RULE2-01-GREEN provenance, and
semantic-review refusal records were not reached and are **NOT VERIFIED by W303's canonical run**
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:22-25`).

## Findings

1. **F-01 — observed blocker:** `files[DERIVATIONS.md].bytes` is 277385 while the copied file is
   279613 bytes. Its SHA-256 is correct, but the combined digest/size verifier refused on this first
   member (`CONTRACT_TABLES_MANIFEST.json:284-289`;
   `verify_bceg.py:1984-1994`; `W303_GATE_RECEIPT.json:4-7`).
2. **F-02 — additional stale size, not reached:** `files[scenario_catalog.json].bytes` is 46256
   while the copied file is 47759 bytes; its SHA-256 is correct
   (`CONTRACT_TABLES_MANIFEST.json:290-293`;
   `C:\tmp\LANE_PROMPTS_20260828\W300_BASELINE_REGEN_REPORT.md:130`). No second gate run was made.
3. **F-03 — early refusal does not honor `--output`:** normal completion writes `args.output`, but
   the `GateRefusal` handler only writes JSON to stdout and returns
   (`verify_bceg.py:3555-3558,3568-3575`). The required receipt was therefore persisted from the
   observed stdout without rerunning the gate (`W303_GATE_RECEIPT.json:1-8`).
4. **F-04 — stale seal-state text:** the current `seal_state.EXPECTED_SEAL_SHA` is re-seal #12, but
   its adjacent `reason` still says “Sealed by the Lead at re-seal #10”; `seal.set_by` and the last
   history entry say re-seal #12 (`CONTRACT_TABLES_MANIFEST.json:759-773,1040-1059`). This was not
   changed because the lane required an exact source copy.

## Verification and scope result

- `git diff --check` passed before the first commit.
- `MTC_COMMAND_CENTER/tools/repo_guard.ps1` returned `RESULT: PASS` at clean preflight and again
  with exactly the three intended files staged. The lane itself forbids any other MTC/Pine/parity
  byte (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:7-13`).
- No kernel, harness, golden, input, probe, design, baseline, Pine, broker, host, network, or live
  byte was changed. The common clauses permit only local tests/verifiers in addition to the named
  files (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`).
- No push, PR, merge, or destructive Git action was performed
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:30-31`).

## Discrepancies

1. The prompt names `C:\WP012BUILD\mtc_v2/...`, but that path does not exist; the repository copies
   are under `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/...`. Repository routing was used
   per C-2 (`LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:8-10`;
   `N_COMMON_CLAUSES.md:9-13`; `CONTRACT_TABLES_MANIFEST.json:1-3`).
2. The prediction that nine catalog-pin refusals would clear and all ten probes would evaluate was
   not observed. The one allowed run refused before catalog loading on stale `DERIVATIONS.md` size
   metadata (`LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:22-25`;
   `W303_GATE_RECEIPT.json:4-7`; `verify_bceg.py:1984-1994,2041-2044`).
3. The source bundle's `files[].bytes` values for `DERIVATIONS.md` and `scenario_catalog.json` are
   stale even though both stored SHA-256 values are current; W300 had already recorded the same
   mismatch (`CONTRACT_TABLES_MANIFEST.json:284-293`;
   `C:\tmp\LANE_PROMPTS_20260828\W300_BASELINE_REGEN_REPORT.md:130`).
4. On this early `GateRefusal`, the verifier did not create the requested `--output` file because
   the exception handler omits the output-writing branch. The receipt had to be persisted from the
   one run's stdout (`verify_bceg.py:3555-3558,3568-3575`; `W303_GATE_RECEIPT.json:1-8`).
5. The copied manifest's current seal fields/history say re-seal #12 while `seal_state.reason`
   still names re-seal #10 (`CONTRACT_TABLES_MANIFEST.json:759-773,1040-1059`).

No discrepancy was repaired: the only authorized contract action was the exact bundle copy, and
the canonical gate was authorized exactly once (`LANE_W303_MANIFEST_CATALOG_REFRESH_SEAL12.md:7-18`).
