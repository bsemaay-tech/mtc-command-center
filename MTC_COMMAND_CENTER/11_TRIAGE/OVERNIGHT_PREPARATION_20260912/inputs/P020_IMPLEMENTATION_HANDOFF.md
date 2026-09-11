# P020 implementation handoff — preparation only
Source baseline: 42f99571e6abb5222744d9345e1c8a9e19c23c15.
Preparation start: 2026-09-11T21:08:59Z. Original hard deadline: 2026-09-12T05:08:59Z.
Coordinator: 01a0924d-2c4b-7da1-99e1-24e2a7c7685c. P012 owner: 01a09241-3ca0-7181-bd51-8f93b447ae44, “Continue WP-P0-12 sprint”, local.

## What this package now supplies
Four source-checked preparation packets, a35-row status/effort matrix, one retained-owner-decision packet, scoped component-check execution, exact source and data snapshots, and a concrete implementation sequence. RUN_STATE.md and VERIFICATION_REPORT.md record final verification and worker state.

No P020 product change, economic/schema implementation, P012 edit, backtest, expensive benchmark, exchange contact, shared Git write, acceptance audit, PR or merge was performed by this task. Proposed functions, filenames and tokens below are NOT shipped implementations.

## Prerequisites and the smallest first authorization
OWNER_DECISIONS.md OD1–OD3 hold the implementation scope, allocator semantic choice and cost-index role. Recommend an isolated research-only candidate with an explicitly approved economic successor. Proposed2.1.0 is not registered or approved. P0122.0.0 remains available source with bounded upstream evidence; full P012 is NONACCEPTED,10production requirements open.

After authorization, first freeze the interface contract, policy references and independently derived fixture expectations. Build from the pinned snapshot in an owned feature/p020-* worktree with exact paths and no live/scheduled dependency. Do not modify the foreign canonical checkout or P012's reviewed worktree. Coordinate any additive semantic registry change with the P012 owner before taking that path.

Missing owner numerical values can remain refused in a synthetic implementation candidate. Applicable P012 record admission, final reviews and actual human ratification are prerequisites for accepting production-dependent evidence. No successful synthetic benchmark upgrades that evidence class.

## Path ownership proposed for the future build
Repo base for every path in this table is C:/LAB/Tradingview_LAB_CLEAN; use an owned worktree, not this checkout.

| Writer | Exact existing paths / proposed additions | Boundaries |
|---|---|---|
| Economic counterpart flagship | shared_risk_calculator.py; NEW MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/p020_economics.py; additive registration ONLY in MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/semantics.py | Owner OD2 and P012-coordinated registry ownership required. Preserve legacy1.0.0 and corrected2.0.0 outputs. Existing core/economics.py, instrument.py, runner.py and record bytes are read-only dependencies under this proposed minimum. |
| Research integration counterpart | NEW p020_simulator.py; NEW portfolio_simulator.py; MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py | One writer owns the entry/sizing/portfolio chain. No independent quantity before or after resolve. No signal/strategy/grid changes. |
| Contract identity writer | MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py; NEW MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py | Add named snapshot/dataset helper functions only after explicit protected-path approval. Existing package/evaluation/deployment hash recipes and field sets remain unchanged. If exact implementation needs a schema alteration, expand the concrete approval packet first. |
| Consumer writer | MTC_COMMAND_CENTER/03_QUANTLENS/tools/multiwindow_oos.py; cpcv_validator.py; finalize_bootstrap_bh.py; reference_producer.py; rigorous_walk_forward.py; rigorous_walk_forward_parallel.py; variant_missing_knobs.py; enrich_gate3_evidence.py, all in that same tools directory | Separate output namespace per new run; preserve all old artifact bytes. probabilistic_pbo.py in the same directory is the additional inline-harvest companion, not a ninth misclassified direct caller. |
| Evidence/verifier writer | control_parity_checklist.py; unsimulated_controls.py; evidence_class.py; cost_model_registry.py; statistical_battery.py; check_allocator_import_identity.py; check_p020_acceptance.py; existing matching check_*.py files listed in qa/RESULTS.json; NEW research_verification/p020/projections.py; NEW research_verification/p020/test_execution_proofs.py | Independent expected relations, not simulator-produced expectations. Root module whitelist means these exact named files, not arbitrary check_*.py. No Bridge or deployment changes. |
| Benchmark writer | NEW p020_benchmark_runner.py; NEW research_verification/p020/test_restart.py; external run output directory | Harness after integrated path exists. No default live data download, no implicit record fallback. Heavy execution requires its later scoped run authority and resource reservation. |
| Integration Lead | .github/workflows/research-gates.yml only if approved CI wiring needs it; MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md and authoritative P020 tracker after acceptance | Local candidate work is not acceptance. Push/PR/merge require their own recorded authority and protected current-head Bridge CI. Do not infer permission from this proposal. |

If a module needs more paths than the table, the Lead must first state why, check ownership and the retained economic/schema boundary. This is a proposed allowlist, not authority to silently extend P012.

## Build sequence and precise interfaces

### 1. Freeze contracts and independent fixtures before product edits
Confirm OD2 and preserve all historical identities. Resolve_semantics_id remains exact/no-default; add a successor only under the approved version. Pin the three raw production record hashes from inputs/P012_RELEASE_RECEIPT.json, but retain their admission refusals. Synthetic profiles use different records, IDs and evidence namespaces.

The independent verifier authors expected values from the accepted design and explicit synthetic input records. Review and freeze these values before comparing implementation output. Select per-control projections, token vocabulary and minimal-trade requirements from packetC; do not compute expected values by importing the control being checked. Import inspection is one check, not proof against a copied oracle.

Engineering recipes (this handoff resolves engineering choices; packets A-D provide supporting detail):
- snapshot_id: SHA256 of UTF8 canonical_json(AccountSnapshot without snapshot_id), sorted keys, no newline, using existing serialization. Bind one snapshot through the full decision. Equivalent Decimal spelling is not silently normalized beyond the existing serializer.
- dataset_manifest_sha: raw original manifest-file digest. ArtifactManifest.dataset_hash: digest of the selected dataset manifest naming the original manifest digest and sorted selected IDs, relative paths, CSV digests, symbol/timeframe, row count and interval. Different tokens, different meanings; proposed helpers must be checked independently.
- Manifest entries retain shipped required_for_promotion:boolean and reason fields. The proposed closed token/reason validator adds semantic validation without inventing a new authoritative economic record format.
- Policy settings bind through allocation_policy_version and the existing deployment identity inputs. Any policy change requires the relevant fresh sizing/guard/identity evidence; relevant evidence is never an empty set.
- Same-bar rejection key is stable across regenerated intent/snapshot IDs: account, bucket, package, instrument, bar and frozen decision slot. Retry within that slot refuses until bar advance. Slots cannot be caller-generated escape hatches.

Engineering control vocabulary for interface freeze: preserve the eight existing checklist IDs risk_allocator, fees, funding, slippage, protective_order_semantics, guardian_authorize_reject, partial_fills and snapshot_staleness. Proposed leaf IDs are risk_allocator.risk_at_stop, risk_allocator.fixed_qty, risk_allocator.fixed_notional, risk_allocator.volatility_target, risk_allocator.contract_multiplier, risk_allocator.minimum_notional, risk_allocator.quantity_step, risk_allocator.minimum_quantity, risk_allocator.risk_cap, risk_allocator.leverage_cap and risk_allocator.gross_exposure_cap; protective_order_semantics.sl_gap, .tp_gap, .multi_tp, .break_even, .trailing, .collision, .close_only, .opposite_signal, .time_bars and .time_eod (each suffix expands under the full parent); portfolio.daily_loss, portfolio.max_trades, portfolio.max_drawdown, portfolio.consecutive_loss, portfolio.equity_filter and portfolio.mae; informational reconciliation_idempotence and correlation_exposure_veto. This is the proposed closed validation vocabulary; unknown IDs refuse. A required parent is verified only when every enabled required child has independent proof. Frozen-package classification controls requiredness; names never silently downgrade a required control, and snapshot binding/refusal remains required for sizing even when the separate execution-staleness model is informational. This naming choice creates no new owner decision or schema field.

Manifest adapter: root ControlEntry(control, classification, reason) maps to existing shared UnsimulatedControl(control_id=control, required_for_promotion=(classification==REQUIRED), reason=reason). Refuse every classification other than REQUIRED/INFORMATIONAL; use the closed reason set NO_KERNEL_MODEL, MODEL_PRESENT_NOT_REACHED, INFORMATIONAL_BY_DESIGN, DEPLOYED_IDENTITY_UNVERIFIED. Hash canonical JSON of the sorted shared-contract records (by control_id), UTF8/no newline; validate unique IDs first. Preserve both shipped carriers; do not invent a classification field on the shared contract. Expected economic values use exact Decimal units. At an unavoidable float API boundary, compare the frozen expected serialized float representation under the pinned runtime; no unsourced epsilon. Restart semantic equality is exact trial IDs and result values, while timing remains diagnostic. These are preparation proposals requiring implementation verification, not shipped proofs.

### 2. Deliver a separate successor with one final quantity authority
The P012 corrected runner already separates corrected and legacy sizing branches (runner.py:1530-1542 and1908-1920). Do not “repair” it by deleting legacy compatibility.

Proposed successor OPEN sequence: validate exact semantic/records/bound intent → determine slipped and valid rounded fill price → compute the requested sizing method inside resolve → floor quantity to the authoritative step → refuse invalid minima or applicable full-rejection caps → apply fees/protection state → emit one atomic EconomicTransition. The PortfolioSimulator commits that transition once. It must not recalculate quantity.

Method coverage to implement from SizingRequest:
- RISK_AT_STOP: frozen risk budget divided by stop distance times contract multiplier.
- FIXED_QTY: declared quantity, followed by the same quantization, minima and caps.
- FIXED_NOTIONAL: declared quote notional divided by final fill price times contract multiplier.
- VOLATILITY_TARGET: declared target and frozen estimator/annualization parameters produce a notional budget, then the same conversion and caps. Missing, nonpositive, nonfinite or insufficient-history estimator output refuses; no implicit estimator or target.

Preserve exact unit conversion: P012 risk_pct is percentage units, while requested_risk_fraction is a fraction. Root arithmetic is Decimal and current transitions use binary64; define one explicit conversion boundary and test it. The3extra methods need calculation dispatch; the risk-at-stop seed alone is not a complete allocator.

A no-drift adapter is an alternative only with a reviewed integration contract. Calling the seed separately cannot establish one authority. The Lead's synthetic function counterexample confirms clamp-versus-reject differs; it is not a proof that every possible adapter architecture is impossible.

### 3. Portfolio state and canonical simulator
Use existing RiskBucket, AllocationPolicy and GuardianPolicy objects from contracts/mtc_contracts/risk.py, their version/source identities and frozen strategy settings. New research wrapper owns equity, positions, margin/exposure, daily state, full-close counters and the bound snapshot. Reuse current guard comparison semantics unless a separately approved economic change says otherwise. Unset required policy values refuse; synthetic test constants do not become defaults.

Preserve daily-loss/max-DD positive-percentage calculations, full-close loss streaks, source day reset, equity/SMA behavior and MAE equality boundary. Guard basis is GROSS-MINUS-FEES, not an invented funding-adjusted alternative. PacketC lists discriminating fixtures.

Canonical simulate_slice delegates the execution phase to p020_simulator while preserving signal generation and configured exit mode. Explicit compatibility profile can retain old behavior for historical reproduction. New acceptance-bearing runs cannot omit semantic version, bind a stand-in, or pass an unauthenticated control-name list.

### 4. Consumer migration in parallel after the interface freezes
PacketB owns all8tool dispositions and writer tests. Four canonical callers require explicit exit_mode and lineage propagation. reference_producer additionally replaces its separate full-history trade replay with projections from the corrected ledger; its lockbox aggregate call does not validate that old CSV replay.

finalize_bootstrap_bh currently rewrites its source results JSON. Create a new immutable finalized artifact instead. All fixed destination paths can overwrite on rerun; use collision refusal/new run namespaces and atomic publication. Preserve old datasets/results under their original identities.

Retire and freeze the2independent simulators; any retained historical screening entry point stays non-promotable. variant_missing_knobs.apply must refuse the corrected path before changing either GRIDS or build_signals. Do not add signal variants under a patcher cleanup. Reporting prose changes only after actual semantics change.

### 5. Execution proof, battery and acceptance evidence
E parses frozen enabled controls; X records actual typed execution claims; V verifies independent state/cash/fill relations; M joins verified claims and computes enabled minus verified-executed. The shipped root set math is reusable, but the full E/X/V/M chain is new work. Remove forged-claim acceptance by requiring bound event/projection evidence. Run-specific reachability and whole-suite coverage are separate: one minimal trade cannot exercise mutually exclusive exits and every account guard.

Build all8battery-row producers and explicit BLOCKED/STOP/PASS handling. Keep current ratified thresholds; CPCV/PBO and sweep ceiling wait for measured owner decisions. Use measured skewness and Pearson kurtosis with declared estimator/annualization; reject insufficient/nonfinite inputs. The seven-element root combiner is not all8producers.

Freeze a candidate, exact parameters, data selection and baseline before CPCV/PBO port harvest. Scope any future protected02_MTC_BACKTEST port separately; its whole directory is not authorized by this handoff. Before/after economic deltas need independent expectations, not a required equality across changed economics.

Update check_p020_acceptance: test actual binding/execution; remove stale kernel-absence wording; replace file-presence/self-declared PERFORMED checks with evidence verification. Research CI is supplementary and its current acceptance reporter is nonblocking; do not confuse it with protected Bridge CI or silently alter repository rules.

### 6. Benchmark and restart proof
Primary engineering data proposal is the frozen historical legacy bundle in inputs/legacy_dataset. All93CSVdigests across85pairs were independently checked and copied; source evidence in qa/LEGACY_DATA_COVERAGE.json. Preserve first-PASS selection order and pin selected dataset_id: BTCUSDT1h has8matching records and2h has2. Data completeness claims are only as strong as the manifest and hash checks; this task did not establish exchange truth.

Grid constructor inventory:20defaultstrategies,1122parameter sets,1700jobs,95370nominal parameter tuples at the default exit mode. Record eligibility skips separately. This is not100000completed trials. Report whole-existing-grid measurements and an explicit100000scale estimate; a requirement for100000distinct new configurations needs a separately approved expansion. Do not pad duplicates.

Full-kernel baseline and two-tier funnel are separate measurements. Throughput is3600*completed_trials/elapsed_seconds; latencyp50/p90 is separate. Owner OD6 supplies the feasibility budget/statistic. Scope the actual run, reserve memory/CPU with P012, calibrate one worker and fail/delay if even one cannot fit. No expensive run was executed during preparation.

Per-trial ledger/checkpoint protocol validates IDs, row digests and checkpoint manifest; restores only validated completed rows. Test interrupt/torn-tail, missing row, duplicate conflicting ID, changed source/data/config and reordered completion. Exact semantic outputs and final ID sets must match an uninterrupted reference; timing is diagnostic. Never execute untrusted pickle as an admission path.

## Independent evidence already reproduced
- Exact accepted design hash matched.
- Git-archive source pin and189initial input hashes matched; qa/SOURCE_FACTS.json records AST call/writer checks and three raw production-record digests.
- Seven existing P020 component checkers passed under Python3.12.12 in qa/source, including their built-in mutations.
- Existing acceptance reporter exited1 at6/13 with the known stale absence message; this remains a limited report, not package acceptance.
- Synthetic function-level clamp/reject counterexample reproduced; no whole-kernel defect-closure claim.
- Grid constructors enumerated without any strategy or backtest execution.
-93legacyCSV files,259839630bytes, matched their manifests; copied bytes reverified.
No policy/research profitability, production readiness, integrated simulator execution or benchmark throughput is claimed.

## Routing, reviews and estimated remaining work
| Work | Proposed included route | Dispatch condition |
|---|---|---|
| Protected economic implementation | Independent exact Claude Opus5 counterpart, prefer isolated Max as this owner request allows | First-party authentication and live quota verified. Current campaign used no Max inference because the reported session was exhausted. |
| Source mapping / bounded unprotected preparation | OpenCodeGo GLM5.3Flash; DeepSeekV4Pro for difficult synthesis | Explicit opencode-go route only. Numerical allowance was unavailable here; successful routed jobs establish availability, not unlimited capacity. |
| T0 acceptance | Fresh claude-opus-5 and gpt-5.6-sol, xhigh, plus gemini-3.7-flash-high corroboration under current exact policy | Frozen candidate/evidence, independent execution, Lead reproduction. Preserve P012 reviewer reservations and Gemini quiet windows. No substitution or quota reset implied. |
| Integration | Lead | Accepted scope, recorded owner authority, current-head required Bridge CI, then authorized PR/merge. |

Planning estimate:40–80engineeringhours across nonduplicated groups (TASK_MATRIX.md), excluding unmeasured compute and external waits. A30–60elapsed-hour window is provisional scheduling capacity, not a measured forecast: it assumes stable approved interfaces, a core writer, consumer/verifier overlap, available exact reviewers and bounded repairs. Semantic redesign, throughput failure or missing admissible records can extend it. The older120hour budget is not converted into a completion percentage.

Critical path: scope/semantic choice → frozen contracts/policy/independent fixtures → successor + allocator + portfolio → canonical integration → full execution proof/candidate comparison → benchmark/restart → exact reviews → authorized integration. Consumer and verifier work can overlap after interface freeze, with exclusive paths. No P016 research-economics co-writer on the same surface.

NEXT ACTION: Owner reviews OD1–OD3 in OWNER_DECISIONS.md; then an authorized Lead freezes the interface and independent fixture packet before assigning product writers.
WAITING FOR OWNER: Nothing for preparation completion. Product work and numerical/measurement gates remain as listed.
