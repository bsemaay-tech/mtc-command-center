---
name: quantlens-parity-promoter
description: Use when turning a successful QuantLens backtest candidate into a parity-first MTC_V2 integration preparation package.
---

# QuantLens Parity Promoter

## Purpose

Convert a `BACKTEST_PASSED` or `BACKTEST_PROMISING` candidate into a feature contract, Python reference note, Pine integration plan, PineTS parity plan, and Go/No-Go decision.

## When to use

Use after bounded validation when a candidate is ready for parity preparation.

## Inputs

- Candidate metadata.
- Backtest result folder.
- Risk and unknowns notes.

## Outputs

- `06_PROMOTED_TO_PARITY/<CandidateID>` package.
- Feature contract YAML.
- Python reference logic note.
- Pine integration plan.
- PineTS parity test plan.
- Expected risks and Go/No-Go file.

## Safety rules

- Do not modify `01_PINE/MTC_V2.pine`.
- Do not modify production Python runner files.
- Do not claim PineTS lifecycle parity unless lifecycle rows exist.
- TradingView export remains final release audit.

## Feature contract requirement

Define feature type, inputs, outputs, defaults, gate, warmup behavior, and deterministic close-bar or intrabar rules.

## Pine/Python parity requirement

Pine and Python must implement the same semantics before promotion. Existing behavior must remain unchanged unless explicitly scoped.

## PineTS requirement

Use PineTS for local L0-L3 feature/indicator/signal checks where comparable. Mark unsupported lifecycle surfaces as not comparable.

## Go/No-Go rules

Block on repaint, lookahead, unresolved parity ambiguity, missing data, weak OOS evidence, or feature-gate/default-OFF gaps.
