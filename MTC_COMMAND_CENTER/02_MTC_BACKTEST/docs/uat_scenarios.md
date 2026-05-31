# UAT Scenarios

## Scope
- Validate end-user critical flows before production go-live.

## Scenario 1: Backtest Run
1. Load a known parity case in UI.
2. Run backtest with parity mode enabled.
3. Confirm trade count and key metrics are produced.

## Scenario 2: Replay Candidates
1. Export candidate set.
2. Replay candidates on two target windows.
3. Confirm ranking file is generated.

## Scenario 3: Optimizer Flow
1. Execute `runbook.ps1 -Mode optimize`.
2. Validate artifact layout under `results/<run_id>/`.
3. Confirm shortlist is generated.

## Scenario 4: Promote Flow
1. Execute `runbook.ps1 -Mode promote`.
2. Confirm `manifest.json` and blessed candidates exist.

## Acceptance
- No runtime errors.
- All artifacts are generated in deterministic paths.
- Health alert output remains `status=OK`.
