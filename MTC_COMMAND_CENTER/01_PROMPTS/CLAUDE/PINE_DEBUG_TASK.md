# Claude Task Template: Pine Debug Task

## Purpose

Analyze Pine compile or behavior issues reported by the user.

## Inputs

- Pine draft path or pasted snippet
- TradingView compile message
- Expected behavior
- Observed behavior

## Workflow

1. Reproduce the issue mentally from the provided compile output.
2. Identify likely syntax or semantic causes.
3. Propose the smallest safe correction.
4. Ask for missing compile output if needed.
5. Produce a diagnostic report.

## Safety

Do not claim a compile pass unless the user observed it or an approved tool verified it.
