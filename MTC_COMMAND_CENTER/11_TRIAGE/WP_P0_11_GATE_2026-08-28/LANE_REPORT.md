# WP-P0-11 `P011-LC-GATE-v2` repair round 6 report

Date: 2026-08-29

Branch: `feature/wp-p0-11-kernel-legacy-compatible-20260825`

Worktree: `C:\WPP011_20260825`

Tier: T0 because this evidence gate protects later economic-kernel work. Two independent flagship
audits remain required; the implementer issues no acceptance verdict.

## Outcome

**Gate outcome after stage 2: STOP.** The current disposition is 27 GREEN, 13 STOP, and 2
policy-only rows. Six formerly GREEN rows correctly became STOP when the gate began checking the
exact declared authority set. This is successful discrimination, not disposition conservation. The
gate now requires those current counts and rejects the protected stale row evidence
(`p011_gate.py:1442-1458`). No kernel consolidation, protected implementation edit, subject
comparison, or live/runtime action was performed.

## Premise 1 - authority diff

| Identity | Git blob OID | CRLF SHA-256 |
|---|---|---|
| v1 pinned P0-09 authority | `f96b53258488eb85b0d67509766c3c19f7bdf0bf` | `6464e6f01a05109816a0433b78ac6eccc50260b77b89093f2444773db6c01068` |
| current-master / v2 P0-09 authority | `1c39ab939dfcf5589e5ec8fba4af8966947a67fc` | `7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249` |

`master` at `85c3e17f97efa1ba83ef9c679de319a50ad3be04` resolves the capability-table
path to blob `1c39ab93...a67fc`. Independent byte hashing reproduced both CRLF hashes.

`git diff f96b5325... 1c39ab93...` reports 119 insertions, 100 deletions, and 93 hunks.
Classification of those hunks found 75 citation-only replacements, 16 source-provenance rewrites
around moved or retired WP-P0-23 surfaces, and two added citation-audit metadata blocks. The latter
two state explicitly that no row claim, canonical rule, chosen implementation, fixture oracle, or
expected value was rewritten. Direct inspection found no rule, oracle, or expected-value change.
Premise 1 therefore holds; no substantive authority change was absorbed into this gate version.

## Stage-1 identities and signature

- Committed legacy manifest: `29ecc19947bd5400293709cccd7fe0e46aceeb013cc8fb0f2d7965a16c515ed3`.
  The prior owner-signed v2 anchor still carries
  `1bc01646e9a00a4ee62c22c6ce1416ed03648e97351e792ae82bbbaff95f52d7`; that stale pin is retained
  deliberately for the stage-4/v3 re-publication obligation described below.
- Observation schema: `c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e`.
- Profiles: Supertrend `c1570317e0dd9ffc2eb9d4ad652891bce65e3ff2007cbbcbba1523ddb33b78f0`;
  Range Filter `35d40915d9813265d1cc1f4474a770471d3ea443e5a67b12ccb4f9e7270944d8`.
- Final receipt: `a31128f1e292c6f70c8204847494e40c38edc9af685f72a21486c90027f61bb1`.
- New external anchor `C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json`:
  `5ab2fd766dec878046ade9e35972ace8eea5c6860f47dc8c719a4b7a55059149`.
- Signature basis: `C:\tmp\LANE_PROMPTS_20260828\OWNER_AUTH_P011_GATE_V2.md`, SHA-256
  `d5da5c81df38de31b629605cd972ce3d9df19185573f6d4018782cae8f2b2ef3`, owner words verbatim:
  **"Bump to v2 now"**.
- **The v1 anchor is retained untouched** at
  `C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json`, SHA-256
  `eb6a600ff9609789465118a217845c7cac6f8b09f7ecaee2a93242f1f16ec15c`.

## Caller-supplied byte comparison - ephemeral historical scratch evidence

The prior round recorded outputs at `C:\tmp\p011_gate_v2_run1_20260828` and
`C:\tmp\p011_gate_v2_run2_20260828`. They are outside the repository and were not regenerated in
repair round 5. The counts (48,077 observations per profile; 96,154 total) and hashes below are
therefore historical **ephemeral** claims, not durable acceptance evidence:

| Artifact | Caller input 1 SHA-256 | Caller input 2 SHA-256 |
|---|---|---|
| `mtc_v2_legacy_sequence.jsonl` | `727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e` | same |
| `final_states.json` | `045f11c34e5713dcec97987f14f26b8e9a72011d44b91806b382680fbe1e622a` | same |
| `row_corroboration.json` | `9d6abe9265f8b332db429c6bc3f8144545902bb03fc44fd60de3bf970a195f0e` | same |
| `baseline_manifest.json` | `62d1ef5fc90b36b6c8caec9388a229ec897dca95ca99f2ba9b979f9c20e6cecc` | same |

The prior report characterized the unchanged sequence hash as expected because the authority diff
changed citations, not rules or data. It also recorded 76/76 comparator RED and 76/76 restored
GREEN; matrix SHA-256 is
`1bfa108ed6b547af92af6bf08c70da8a7363598278747f78259f3958c88c3a3d`.

## Complete C01-C42 re-verification

Comparison against recorded branch SHA `9e8a69b32a3460c9a08e8977db99bd7dfe4e5788` did **not** preserve
the old disposition. The current result is **27 GREEN, 13 STOP, and 2 policy-only (C25/C27)**.
All 33 executable producer bindings still produce clean execution plus mutation RED, but six now
stop because the observed authority set does not equal the declared set. The gate is working by
refusing those six rows.

- C28-C30 remain STOP because no executable Pine producer was authorized; no Pine was run.
- C32/C34/C35/C42 remain authority-contradiction STOPs.
- C03/C04/C26/C38/C39/C41 changed from GREEN to STOP on missing declared authority, as itemized
  below.
- The committed row hashes and receipt narrative predate this disposition and are stale v3 pins;
  this repair does not reuse them as current evidence.

## Stage-2 executable binding rule

Every applicable manifest scenario is exact-bound to a verifier-owned typed scenario before its
producer runs. The binding refuses missing, extra, or unequal values. Producer outputs are then
compared with the bound expected observation and final state.

**Contract conservation is not enforced or claimed.** The dead named-consumer ledger and its unit
tests were removed. `BindingLedger` retains declared leaf paths and bound paths for variant
enumeration and binding summaries only (`scenario_binding.py:246-255`, `:366-385`). Exact binding
is performed separately by `_bind_exact` (`scenario_binding.py:334-364`). The generator emits the
typed scenario declarations (`stage1_freeze.py:551-613`); the baseline gate exact-binds them
(`p011_gate.py:566-601`) and the row arm exact-binds its verifier contract (`row_arm.py:2380-2438`).
The row arm separately compares producer output and checks an observed mutation RED path plus
runtime authority identities (`row_arm.py:155-218`, `:2531-2590`, `:3299-3358`).

The six measured disposition changes are:

| Row | Before | After | Missing declared authority |
|---|---|---|---|
| C03 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | PINE_CURRENT_MASTER |
| C04 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | PINE_CURRENT_MASTER |
| C26 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | PINE_CONTROLLER_FREEZE |
| C38 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | A_CURRENT_MASTER |
| C39 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | A_CURRENT_MASTER |
| C41 | GREEN_AFTER_RED | STOP_MISSING_REQUIRED_AUTHORITY | B_BACKTEST_FREEZE |

The current authority check compares a verifier-declared set with runtime import observations and
records missing identities (`row_arm.py:179-218`). Current code emits no `CONSERVED` contract ledger and
makes no terminal-consumption claim. The isolated unit suite uses a per-suite-invocation temporary directory,
not a committed absolute scratch pin (`test_scenario_binding.py:31-32`). It runs 22 tests, including
the producer spy, exact-key variants, identity-bound C32 control, receipt-pin refusal variants, a
counts-only receipt probe, and the complete declared-leaf variant matrix
(`test_scenario_binding.py:151-987`). C42 publishes only the executed producer outputs; the
re-keyed duplicate and self-comparison were deleted (`row_arm.py:3238-3253`). No load-bearing claim in
the repaired disposition or binding sections cites an `N26_VARIANTS` scratch output.

## Cumulative v3 obligations

1. Repin the protected receipt's truthful row-arm counts/reason, code and evidence identities, and
   final receipt hash only after authorized evidence regeneration (`P011_GATE_RECEIPT.json:70-80,
   242-245,312-315`).
2. Regenerate protected row evidence and C41/F3 rather than hand-editing generated pins; the current
   terminal disposition is described at `LANE_REPORT.md:76-89,106-115`.
3. Coordinate the v2 external-anchor repin only after the receipt and protected evidence agree
   (`LANE_REPORT.md:40-49`).
4. Extend M3-07's durable-evidence rule to every acceptance-bearing scratch citation. Publish any
   variant matrix or transcript under an authorized repository evidence path or label it ephemeral.
   Re-cite the caller-supplied byte-comparison observation counts and four artifact hashes to
   durable repository evidence, or retain the explicit ephemeral label in this report
   (`LANE_REPORT.md:57-72`). The
   owner-authorization basis at `LANE_REPORT.md:50-52` is also an external `C:\tmp` citation, not a
   repository artifact.
5. Reconcile the protected receipt's `legacy_manifest.sha256` and
   `observation_schema.sha256` pins with the current frozen files before an anchor-only repin can
   authorize the package (`P011_GATE_RECEIPT.json:138-146`; `row_arm.py:2322-2346`).
6. State and pin the serialization policy for both normalized/LF repository bytes and CRLF working-
   tree bytes. The validator currently hashes exact on-disk bytes (`row_arm.py:120-129,2322-2346`);
   v3 must name the chosen authoritative byte form and publish both identities where both forms are
   retained.
7. Update every authorized receipt/anchor hash for `row_arm.py`, `scenario_binding.py`,
   `p011_gate.py`, and the test only inside the coordinated v3 package.
8. Add full discrimination-matrix producer-act verification to the v3 external-reproduction
   contract. A different actor must execute the producers; this finalizer verifies only matrix
   shape and cross-source identity and must not issue producer-execution status.
9. Verify the producer acts behind the renamed `caller_supplied_byte_comparison` field through the
   v3 external-reproduction contract; the finalizer measures only caller-supplied byte identity.
10. Coordinate honest caller-input labels across the frozen receipt template, protected receipt,
    row-arm verifier, and independent remeasurement script during v3. Replace the comparison-only
    `double_build`, `run_1`/`run_2`, `run1_sha256`/`run2_sha256`, and matching CLI families with
    caller-supplied input terminology; this label-only lane may not edit those surfaces
    (`stage1_freeze.py:723`; `P011_GATE_RECEIPT.json:43-68`; `row_arm.py:3563-3621`;
    `evidence/remeasure.py:44-51,130-146`).

## Repair-round-8 honest caller-input labels

The editable finalizer and comparison-only command now publish `caller_input_1`,
`caller_input_2`, `caller_input_1_sha256`, and `caller_input_2_sha256`; both CLI surfaces bind
the matching `--caller-input-1` and `--caller-input-2` flags
(`p011_gate.py:1029-1051,1312-1355,1505-1525`). The finalizer still measures only the identity of
caller-supplied files and performs no producer act. Frozen and non-whitelisted comparison-only
surfaces remain obligation 10 rather than being hand-edited in this label-only repair.

The observation schema is not a target for the scenario-binding fields: its catalog contains
observation, signal, event, position, gate-readiness, and account fields, but none of the named
scenario-contract fields (`P011_OBSERVATION_SCHEMA_v1.json:165-789`).

## Repair-round-5 inherited evidence boundary

The candidate finalizer now refuses any absent, byte-empty, or logically empty required candidate
artifact. Its discrimination matrix must carry nonempty rows and bind its declared count, catalog
count, ordered paths, schema pin, RED return-code declaration count, and restoration return-code
declaration count to the independently loaded
observation-schema field catalog (`p011_gate.py:1305-1392`). The zero-row/empty-artifact modified
copy is refused, a separately modified 75-row matrix is refused against the schema's 76-row
universe, and the 76-row/nonempty control reaches shape-and-identity acceptance without verifying
producer execution (`test_scenario_binding.py:190-499`).

Row-corroboration wording now derives its applicable, policy-only, and total counts from the rows
actually present (`p011_gate.py:604-655`; `test_scenario_binding.py:500-513`). Missing nested
receipt pins now reach the intended `RowFail` through guarded reads instead of `KeyError`
(`row_arm.py:2322-2346`; `test_scenario_binding.py:514-538`). These checks change evidence
admission and reporting only; they do not change the frozen row dispositions or any producer.

## Repair-round-6 truthful finalizer closure

The finalizer terminal status is now exactly
`SHAPE_AND_IDENTITY_ACCEPTED; producer execution NOT verified by this gate`. The command output,
receipt state, baseline-generator status, observation-adapter status, baseline-output status, and
anchor freeze state all use that same narrowed wording; the overall gate outcome remains `STOP`
(`p011_gate.py:35-39,1393-1438`; `test_scenario_binding.py:225-291,423-461`).

Digest membership is verified across independent sources: the set of paths flagged by the
caller-selected matrix must equal the state-digest path set parsed from the repository observation
schema. Set equality checks missing and unexpected paths in both directions; the count and declared
scalar checks remain separate (`p011_gate.py:1365-1380`). A count-preserving moved-flag modified copy
is refused (`test_scenario_binding.py:377-390`).

The accepted status does not assert matrix producer execution. Finalizer reasons name only checked
artifact-copy identity, declared return-code counts, declared outcome/failures, schema path-set
membership, and the baseline-manifest's declared adapter hash (`p011_gate.py:1320-1392`). Full
producer-act verification remains a cumulative v3 external-reproduction obligation.

## Scope and audit boundary

This repair writes only `p011_gate.py`, `LANE_REPORT.md`, and `test_scenario_binding.py`.
`row_arm.py`, implementation A/B, Pine, `MTC_V2`, backtest, adapters, kernel, schemas, receipts,
evidence, and anchors were not edited; no host, broker, venue, credential, or live/testnet surface
was invoked. No live dependency was present. The package is committed locally only as an
audit candidate and is not pushed; two independent flagship audits decide any later acceptance,
and the gate remains **STOP**.
