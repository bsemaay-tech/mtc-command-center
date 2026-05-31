# Start Here For Codex

## 2026-04-28 Optimization Consolidation

- Read optimization rules under `docs/optimization/` before optimizer work.
- Current optimizer status is research-only: infrastructure ready, data bundle ready, dataset rules ready, big overnight run partial.
- Big run confirmed `168337 / 6615000` split evaluations, `144` robust medium candidates, and `0` robust strict candidates.
- Next action is resume smoke, then exhaustive core grid resume.
- Do not promote medium candidates to Pine defaults.
- Do not include the external optimization data bundle or heavy optimization outputs in portable handoff.
- Optimization output does not claim TradingView release parity.

Read these files in this order before making changes:

1. `03_DOCS/HANDOFF.md`
2. `03_DOCS/MTC_V2_ARCHITECTURE.md`
3. `03_DOCS/DEV_LOOP.md`
4. `03_DOCS/RUNBOOK.md`
5. `docs/CODEX_GENERIC_FEATURE_CHANGE_WORKFLOW.md`
6. `docs/INDEPENDENT_REFERENCE_ORACLE_POLICY.md`
7. `docs/PORTABLE_HANDOFF_PACKAGE_SCOPE.md`
8. `03_DOCS/PLANS/MTC_V2_OPTIMIZATION_LOOP_SCORING_CROSS_MARKET_PLAN.md`

## Hard Rules

- Do not modify canonical `01_PINE/MTC_V2.pine` without an explicit task.
- Do not modify production Python behavior without an explicit task.
- Do not bypass parity gates.
- Do not optimize before feature parity passes.
- Do not treat PineTS as `L4`-`L6` lifecycle authority unless lifecycle rows are explicitly emitted and normalized.
- Do not use TradingView export as the normal development loop.
- Do not use live trading keys or API keys.
- Do not include generated outputs, caches, venvs, or `node_modules/` in the main portable package.

## Current Portable Handoff State

- Inventory verdict: `PLAN_READY_FOR_REVIEW`
- Secret blocker: false
- Architecture was refreshed for prepackage readiness.
- Current approved chart data candidate: `05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv`
- TradingView audit XLSX archives remain review-needed and should not be included automatically.

## Development Order

Use the architecture layer order. For new or changed features, use the Generic Feature Parity Factory first:

1. contract
2. implementation
3. trace
4. parity comparison
5. acceptance gate
6. integration
7. selected local smoke checks
8. TradingView release audit only when promotion is needed
# Dataset And Optimization Data Rule

Before any optimization work, read `docs/optimization/DATASET_AND_REGIME_USAGE_RULES.md` and `docs/optimization/CODEX_OPTIMIZER_DATA_RULES.md`.

Use the external optimization data bundle manifest at `C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.yml`.

Do not hardcode CSV paths, do not scan `ARŞİV` unless creating/updating a manifest, do not use XLSX Strategy Tester workbooks as chart data, and do not claim robustness from a single symbol or single timeframe.
