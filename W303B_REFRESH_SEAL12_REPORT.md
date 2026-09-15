# W303B re-seal #12b in-repo copy refresh report

Date: 2026-09-03
Actor: Codex implementer lane
Status: **COPY COMPLETE; CANONICAL GATE REFUSED BEFORE PROBE EVALUATION**
Finding count: **2** (one observed stale-anchor blocker and one receipt-persistence finding).

## Scope, guards, and tier

The lane authorizes byte-for-byte replacement of the three named in-repository bundle copies, one
canonical gate invocation, one receipt, one report, and one commit with the prescribed message
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:3-17,18-30`). The prerequisite marker
existed, the active branch was `feature/wp-p0-12-corrected-vnext-20260831`, and the initial worktree
was clean; all three guards were measured before the first write as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:4-7`). No other assistant, model, or
CLI was invoked (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

Gate-1 classification was recorded before any audit dispatch: T0 absent (no economic behavior,
live, host, security, or deployment change); T1 primary (the protected local verification contract
manifest); T2 the receipt and report; T3 absent. The repository defines those tiers at
`AGENTS.md:38-40`. No model audit was dispatched because C-1 expressly forbids one in this lane
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

The prompt's shortened `mtc_v2/...` path does not exist at `C:\WP012BUILD\mtc_v2`; repository
routing located the named copies under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/`. The copied
manifest identifies the bundle at its opening lines
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1-3`).
This path discrepancy is recorded below under C-2
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).

The decision-132 baseline was available rather than missing: its manifest consumes
`83bbe48c51d0acf78b47c7f5891d78a8b6e1a5dabb98c92673dda224a4597fb2`
(`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`). No baseline byte was created or
changed, consistent with the lane's explicit fence
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:18-21`).

## Byte-for-byte copy evidence

`Get-FileHash -Algorithm SHA256` was run on each source and destination after all three copies. All
three pairs were equal, and source/destination byte counts were equal. Each cited file was read from
line 1 and hashed over its complete bytes.

| File | Source SHA-256 | Destination SHA-256 | Bytes each | Equal | Evidence |
|---|---|---|---:|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `542461d39dc45119a4db37a2488f303e7da83a221c52df9ea092000bff75dafd` | `542461d39dc45119a4db37a2488f303e7da83a221c52df9ea092000bff75dafd` | 73173 | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1` |
| `scenario_catalog.json` | `2e10819f45648653f3f43655c9ba26556472d782da9c95923af7fac96a6e1000` | `2e10819f45648653f3f43655c9ba26556472d782da9c95923af7fac96a6e1000` | 47759 | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1` |
| `DERIVATIONS.md` | `fe385afbc8edd15696ad6288836a2eac33d44e4316d5f7e465ff80f63d59c135` | `fe385afbc8edd15696ad6288836a2eac33d44e4316d5f7e465ff80f63d59c135` | 279613 | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\DERIVATIONS.md:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:1` |

A separate complete read-only measurement of the manifest's 19 members found zero SHA-256
mismatches and zero byte-size mismatches. The two corrected sizes are 279613 and 47759
(`CONTRACT_TABLES_MANIFEST.json:284-293`). Recomputing the seal from the sorted `path:sha256` lines
produced the recorded value `83bbe48c51d0acf78b47c7f5891d78a8b6e1a5dabb98c92673dda224a4597fb2`
(`CONTRACT_TABLES_MANIFEST.json:770-773`). The #12b history entry says that the size and reason
metadata changed without moving a member byte or the seal digest
(`CONTRACT_TABLES_MANIFEST.json:1061-1067`).

Measured `git diff --stat` immediately after the copies:

```text
 .../contracts/CONTRACT_TABLES_MANIFEST.json | 14 +++++++++++---
 1 file changed, 11 insertions(+), 3 deletions(-)
```

`scenario_catalog.json` and `DERIVATIONS.md` produce no Git delta because their source bytes were
already identical to the in-repository copies; the required copy-and-hash operation nevertheless
covered both files (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:8-16`).

## Canonical gate - exactly one invocation

The only invocation was:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN --output C:\WP012BUILD\W303B_GATE_RECEIPT.json
```

PowerShell measured child-process exit code 2. The persisted JSON is the refusal object printed by
that one run (`W303B_GATE_RECEIPT.json:1-8`); the verifier's early-refusal handler also returns 2
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3568-3575`).

The previous `EXPECTED_MEMBER_DIGEST_MISMATCH` did clear: the gate passed all 19 member digest/size
checks and the computed/recorded seal comparison before reaching the subsequent anchor check. That
ordering is fixed by the verifier at `verify_bceg.py:1984-2003`, and the observed later check is
recorded at `W303B_GATE_RECEIPT.json:4-7`.

### Full refusal list

The run emitted a singular preflight `refusal` object rather than the later-stage `refusals` array,
so the full observed refusal list contains exactly one item:

1. `IMPLEMENTATION_ANCHOR_SEAL_MISMATCH` -
   `83bbe48c51d0acf78b47c7f5891d78a8b6e1a5dabb98c92673dda224a4597fb2`
   (`W303B_GATE_RECEIPT.json:4-7`).

The current in-repository implementation anchor still records seal
`d763f62f9a423d2c3ca0887224d91e520c5bb1849aaa1958df1e3bb1d46dae29`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`),
while the refreshed manifest records `83bbe48c...` (`CONTRACT_TABLES_MANIFEST.json:759-773`). The
verifier requires the anchor seal to equal the computed manifest seal and refuses otherwise
(`verify_bceg.py:1996-2006`). The anchor and its sidecar were outside this lane's permitted bytes
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:7-13`), so neither was changed.

## Probe table

The gate stopped in `validate_sealed_producers` at the anchor check. Catalog loading and probe
iteration occur only after that validation succeeds (`verify_bceg.py:1976-2006,2041-2051,3243-3247`).
Therefore **0 of 10 probes were evaluated**. `DETECTED` or `NOT DETECTED` is **NOT VERIFIED** for
every row; this preflight refusal is not probe evidence (`W303B_GATE_RECEIPT.json:1-8`).

| Probe | Target | Declared failed check | Canonical-gate observation | Catalog evidence |
|---|---|---|---|---|
| `PROBE-P012-01-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:737-749` |
| `PROBE-P012-01-B` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:758-770` |
| `PROBE-P012-02-A` | KERNEL | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:779-791` |
| `PROBE-P012-03-A` | INPUT | `RECORD_IDENTITY_PREFLIGHT` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:800-812` |
| `PROBE-P012-04-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:821-833` |
| `PROBE-P012-05-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:842-854` |
| `PROBE-P012-05-B` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:863-875` |
| `PROBE-P012-06-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:884-896` |
| `PROBE-P012-07-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:905-917` |
| `PROBE-P012-08-A` | KERNEL | `CORRECTED_EXPECTATION` | refused before evaluation; DETECTED not verified | `scenario_catalog.json:926-938` |

The prompt's predicted remaining KERNEL/producer, RULE2-06/RULE2-08 harness,
RULE2-01-GREEN provenance, and review records were not reached and are **NOT VERIFIED by W303B's
one canonical run** (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:22-25`).

## Findings

1. **F-01 - observed stale-anchor blocker:** the implementation anchor records the pre-#12 seal
   `d763f62f...`, but the manifest and completed baseline record `83bbe48c...`. The gate therefore
   refused before catalog/probe evaluation (`implementation_anchor.json:3-5`;
   `CONTRACT_TABLES_MANIFEST.json:759-773`;
   `C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`;
   `W303B_GATE_RECEIPT.json:4-7`).
2. **F-02 - early refusal does not honor `--output`:** normal completion writes `args.output`, but
   the `GateRefusal` handler prints JSON and returns without writing that path
   (`verify_bceg.py:3555-3558,3568-3575`). The required receipt was persisted from the one run's
   exact stdout without rerunning the gate (`W303B_GATE_RECEIPT.json:1-8`).

## Verification and scope result

- The source/destination SHA-256 values and byte counts were rechecked after writing the receipt and
  report; the authoritative copy requirement is at
  `C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:8-16`.
- No kernel, harness, golden, input, probe, design, baseline, Pine, broker, host, network, or live
  byte was changed. The lane fences those paths at
  `C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:7-13`, and the common clauses allow
  only local tests/verifiers in addition to named outputs
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`).
- No push, PR, merge, destructive Git action, or second gate invocation was performed
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:30-31`;
  `C:\tmp\LANE_PROMPTS_20260828\LANE_W303B_REFRESH_SEAL12B.md:18-26`).

## Discrepancies

1. The prompt names `C:\WP012BUILD\mtc_v2/...`, but that path does not exist; the repository copies
   are under `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/...`. Repository routing was used
   per C-2 (`LANE_W303B_REFRESH_SEAL12B.md:8-10`; `N_COMMON_CLAUSES.md:9-13`;
   `CONTRACT_TABLES_MANIFEST.json:1-3`).
2. The prediction that nine catalog-pin refusals would clear and all ten probes would evaluate was
   not observed. The one allowed run refused earlier because the in-repository implementation
   anchor still names `d763f62f...`, not re-seal #12's `83bbe48c...`
   (`LANE_W303B_REFRESH_SEAL12B.md:22-25`; `implementation_anchor.json:3-5`;
   `W303B_GATE_RECEIPT.json:4-7`; `verify_bceg.py:1996-2006`).
3. On this early `GateRefusal`, the verifier did not create the requested `--output` file because
   the exception handler omits the output-writing branch. The receipt had to be persisted from the
   one run's stdout (`verify_bceg.py:3555-3558,3568-3575`; `W303B_GATE_RECEIPT.json:1-8`).

No discrepancy was repaired: the only authorized contract action was the exact bundle copy, and
the canonical gate was authorized exactly once (`LANE_W303B_REFRESH_SEAL12B.md:7-18`).
