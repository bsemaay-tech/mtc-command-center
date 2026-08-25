# QuantLens research stage rules

QuantLens means the research/backtest engine and the expert-verdict layer; the Scorecard owns all
numbers. Research outputs are not execution packages, trading approval, or promotion evidence by
default. Never change Pine, parity, MTC, thresholds, strategy behavior, or promotion logic without
explicit scope.

## Any backtest or optimization — mandatory Gate 0

Read `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`,
`11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`, and
`04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md`. The same gates apply to a five-minute
single-strategy run and an overnight sweep. A result without buy-and-hold comparison, DSR, BH-FDR,
rolling walk-forward, bootstrap, and multi-window evidence is not promotable.

Never guess data. Read `03_QUANTLENS/data/README.md`, set `MEGA_BUNDLE_MANIFEST` to the selected
bundle's `manifests/dataset_manifest.json`, then filter with `--symbol`/`--tf`. The engine's
hard-coded default is a legacy crypto archive, not current data. Canonical research runner:

`python MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>`

The primary multi-asset bundle is `native_multiasset_alpaca_2026-06-28`.
`walk_forward_processor.py` is lower-level/custom, not the default.

## Strategy research

Before combining strategies or indicators, read in order:
`_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md`; the four registries named in `INPUTS.md`;
`_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md`; and
`_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md`. Do not hand-edit generated registries.

Log every variant in `VARIANT_LOG_REGISTRY.json`, save runs under
`03_QUANTLENS/research/<run_id>/`, register runs, and verify the Strategy Research Lab view.
User transcripts/screenshots enter only through `00_INBOX/USER_INTAKE/` and
`tools/route_user_intake.py`.

Use the run-progress supervisor/watchdog for long or overnight work. One loop only; verify power
settings before unattended runs. Simulated/reconstructed matrices are not evidence. Regression
claims require RED then GREEN. Opening-range strategies named in D005 are US-session-only; PBO uses
the D008 cap; SciPy work uses the D009-revised clean/shim route.
