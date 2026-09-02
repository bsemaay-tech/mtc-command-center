# W251 Canonical Gate Report — Seal #8 and Regenerated Baseline

## Verdict

**BOUNDED_CORRECTION_EVIDENCE_REFUSED — `RULE2_DIVERGENCE_MISSING`.**

The canonical gate exited **2** for `RULE2-02-RED` at
`/EVENT_SURFACE/decision_events/3/decision`. The prior
`BASELINE_SEAL_IDENTITY_MISMATCH` refusal is cleared: the verifier reached the later RED-projection
check that raises the measured refusal
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:964-971,1336-1342`).
The lane requires STOP on any refusal, with no flag or manifest edit
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:25-29`). Therefore no direct
17-row substitute, contract self-test, repair, or second gate run was performed.

Finding count: **1 canonical-gate refusal**. It is **not classified as KERNEL-SHORT,
GOLDEN-OVER, or DESIGN-GAP**, because the gate refused its declared cross-version projection before
it returned a complete corrected-expectation table. Repository evidence instead identifies a
gate-projection inconsistency, recorded under `## Discrepancies`.

## Scope, authority, and Git identity

This is a **T2 evidence/report lane**. The owner-authorized worktree and branch are
`C:\WP012BUILD` and `feature/wp-p0-12-corrected-vnext-20260831`; the lane records this as the only
lane in that worktree and forbids `master` and push
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:3-7`). No live or scheduled
dependency was used. No host, broker, venue, credential, deployment, network, Pine, adapter,
schema, parity, backtest, optimization, server, launcher, or artifact-generation action was
performed. The one local verifier run is expressly authorized by the lane and shared clauses
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:3-5,25-29`;
`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

Git identities measured immediately before the canonical run:

```text
branch=feature/wp-p0-12-corrected-vnext-20260831
HEAD=226c18bf6be3efeb99ed1dc5b3fd42b5daf93b2b
status=clean
```

W249 is present and does not say STOPPED. Its ordered-accumulation implementation commit is
`615438452c0958fb7123a441e0347e3eb9c2d9bb`
(`W249_KERNEL_ORDERED_EQUITY_REPORT.md:131,352-355`). The HEAD used for this run is W249's
report-only commit, whose parent is that implementation commit; `git show --stat` measured two
kernel/test files in `61543845` and only `W249_KERNEL_ORDERED_EQUITY_REPORT.md` in `226c18bf`.
The seal-refresh commit is `18dbe5de`, as W246 records
(`W246_GATE_RERUN_REPORT.md:63-65`).

## Measured preconditions

The byte probe used Python `Path.read_bytes()` and SHA-256. The 38 mappings are the same source set
W246 defined and previously measured: manifest, derivations, catalog, anchor, 17 goldens, and 17
inputs; the detached anchor sidecar was checked separately
(`W246_GATE_RERUN_REPORT.md:31-65`). The seal was independently recomputed as SHA-256 over the
LF-joined, ordinally sorted manifest `path:sha256` lines, which is the anchor's declared algorithm
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5`).

| Precondition | Measured result | Evidence source |
|---|---|---|
| Worktree / branch | `C:\WP012BUILD`; `feature/wp-p0-12-corrected-vnext-20260831` | Lane assignment at `C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:6-7`; exact Git output above |
| Worktree HEAD | `226c18bf6be3efeb99ed1dc5b3fd42b5daf93b2b` | Exact `git rev-parse HEAD` output above |
| Initial tracked/untracked state | Clean | Exact `git status --short --branch` and `git ls-files --others --exclude-standard` output summarized above |
| W249 report | Present; no `STOPPED` token | Required handling at `C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:17-20`; measured W249 summary at `W249_KERNEL_ORDERED_EQUITY_REPORT.md:3-13` |
| W249 implementation | `615438452c0958fb7123a441e0347e3eb9c2d9bb` | `W249_KERNEL_ORDERED_EQUITY_REPORT.md:131,352-355` |
| Bundle manifest members | **19/19** hashes and byte sizes valid | Member declarations at `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:143-238` |
| Seal #8 recomputation | `4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461`; equals manifest and anchor | Manifest pin at `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:543-556`; anchor pin at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:3-5` |
| Bundle-to-worktree copies | **38/38 byte-identical** | Required comparison at `C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:11-13`; mapping definition and prior copy set at `W246_GATE_RERUN_REPORT.md:31-65` |
| Anchor sidecar | `343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8` — **MATCH** | Measured against `implementation_anchor.json`; verifier enforces this comparison at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:956-962` |
| Catalog identity | Bundle = worktree = baseline manifest = `f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603` | Bundle at `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:150-152,737-740`; baseline at `C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:10-13` |
| Baseline-consumed seal vs anchor | Both `4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461` | Baseline at `C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:13`; anchor at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:4` |
| Baseline output bytes | **36/36** declared file digests valid; **17** scenarios declared | Manifest count contract in verifier at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:976-980`; baseline summary at `C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:20-21` |

Exact successful precondition summary:

```text
SEALED_MEMBERS=19/19
COMPUTED_SEAL=4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461
MANIFEST_SEAL=4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461
ANCHOR_SEAL=4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461
COPY_MAPPINGS=38/38
ANCHOR_SIDECAR=MATCH|343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8|343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8
CATALOG_BUNDLE=f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603
CATALOG_WORKTREE=f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603
CATALOG_BASELINE_MANIFEST=f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603
BASELINE_CONSUMED_SEAL=4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461
BASELINE_DECLARED_FILES=36/36
BASELINE_SCENARIOS=17
```

## Canonical gate

Working directory:

```text
C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON
```

Exact command, run once:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
```

Exact Python exit code: **2**.

Full output:

```json
{
  "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
  "mode": "full-gate",
  "refusal": {
    "check_id": "RULE2_DIVERGENCE_MISSING",
    "detail": "RULE2-02-RED",
    "pointer": "/EVENT_SURFACE/decision_events/3/decision"
  }
}
```

### Refusal comparison operands

This refusal does not compare two seal identities. It compares two cross-version projection
identities. For `RULE2-02-RED`, the verifier declares the legacy operand as `_absent()` and resolves
the corrected operand from `EVENT_SURFACE.decision_events[3].decision`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1125-1149,1186-1192`).
The measured equality that triggered `RULE2_DIVERGENCE_MISSING` means the two compared operands
were exactly:

```text
legacy   = {"tag": "ABSENT"}
corrected = {"tag": "ABSENT"}
```

The repository's sealed expected artifact contains three decision rows, indices 0–2, and explicitly
records that no extra row was added under owner Reading Y
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json:21-24,69`).
The verifier rejects a RED row when any declared projection is equal, using the first equal
selector as the refusal pointer
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1336-1342`).

## Seventeen-row table and gate summary

**NOT PRODUCED — STOPPED.** The canonical pipeline entered its scenario loop but raised on
`RULE2-02-RED` before returning the seventeen-scenario collection or any gate summary object
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1315-1354`).
The lane's refusal rule requires STOP and forbids flags or manifest edits
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:27-29`). Repeating W246's old
15/17 table or W249's separate direct 17/17 measurement would not be the canonical gate's measured
output, so neither is substituted (`W246_GATE_RERUN_REPORT.md:124-144`;
`W249_KERNEL_ORDERED_EQUITY_REPORT.md:264-324`).

Gate summary object: **NOT PRODUCED**.

## Contract self-tests

**NOT RUN — STOPPED.** The canonical refusal occurred first, and the lane says STOP on refusal
before its later self-test step (`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:25-33`).
No current count is claimed. For provenance only, W246 measured 220 pytest passes and the 18-check
selftest receipt (`W246_GATE_RERUN_REPORT.md:177-186`), while W249 subsequently added one regression
test and measured 221 pytest passes with the same 18-check receipt
(`W249_KERNEL_ORDERED_EQUITY_REPORT.md:330-340`). Those are prior-run evidence, not W251 results.

## Fence verification

Immediately after the refused gate, the same read-only byte probes measured:

```text
POST_GATE_COPY_MAPPINGS=38/38
POST_GATE_BASELINE_FILES=36/36
POST_GATE_SEAL=4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461
```

`git status --short --branch`, `git diff --name-only`, and
`git ls-files --others --exclude-standard` showed no tracked or untracked change before this report
was created. Thus the canonical command changed no golden, catalog, manifest, seal, input,
baseline, or kernel byte, satisfying the explicit fence
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:36-39`). No skip flag was used.

## Discrepancies

1. **The 17/17 prediction was not reached because the gate refused a different contract check.**
   The prompt predicts 17/17 but says the measured number, not the prediction, controls
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:30-32`). The measured result is
   exit 2 with `RULE2_DIVERGENCE_MISSING`, not a 17-row result.
2. **The verifier declares a divergence at a node that the sealed expected artifact says is absent.**
   The verifier compares corrected `decision_events[3].decision` against legacy ABSENT
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1186-1192`),
   while the sealed artifact has only indices 0–2 and says no row was added
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json:21-24,69`).
   This is a gate-projection inconsistency; the lane authorizes no repair.
3. **The refusal instruction asks for two identities, but this is not an identity-mismatch check.**
   The prompt's wording follows its expected seal refusal context
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:27-29`). The actual check is the
   equality-based projection refusal at `verify_bceg.py:1336-1342`. The report therefore quotes the
   two actual projection operands, both `ABSENT`, rather than inventing a seal-identity pair.
4. **The requested self-test count is stale across W246 and W249.** W246 measured 220 pytest passes
   (`W246_GATE_RERUN_REPORT.md:177-184`), but W249 added a regression and measured 221
   (`W249_KERNEL_ORDERED_EQUITY_REPORT.md:330-338`). W251 claims neither because the refusal STOP
   occurred first.
5. **The checked ownership mirror has no W251 row, while the lane prompt grants exclusive ownership
   and the scope fence forbids editing an unnamed path.** The mirror says unlisted workstreams add a
   row before writing (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:58`); the lane says this is the
   only lane in the worktree (`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:6-7`),
   and the shared scope fence forbids touching paths outside those named by the lane
   (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`). The exclusive external lane record
   supplies known ownership; `SESSION_LOCK.md` was left unchanged to preserve the stricter write
   whitelist.

## Commit handoff

Only `W251_CANONICAL_GATE_REPORT.md` is authorized for staging. It must be staged by exact path,
checked with the repository guard without bypass, and committed on
`feature/wp-p0-12-corrected-vnext-20260831`. No push, merge, pull request, or other write is
authorized (`C:\tmp\LANE_PROMPTS_20260828\LANE_W251_CANONICAL_GATE_SEAL8.md:6-7,34,43-45`;
`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`). The report's containing commit SHA
cannot be embedded in its own bytes without changing that SHA; it is reported in the under-10-line
chat close after commit.
