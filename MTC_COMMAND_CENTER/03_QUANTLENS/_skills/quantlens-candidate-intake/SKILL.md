---
name: quantlens-candidate-intake
description: Use when converting a Gemini QuantLens YouTube strategy report into a structured MTC_V2 strategy candidate record without modifying production code.
---

# QuantLens Candidate Intake

## Purpose

Turn a QuantLens YouTube strategy report into a structured MTC_V2 candidate folder, registry row, and next-action note.

## When to use

Use when the user provides a QuantLens report or asks to intake a new YouTube strategy candidate.

## Inputs

- QuantLens report text.
- Optional source URL, market, timeframe, and title.

## Outputs

- Inbox copy in `06_QUANTLENS_LAB/00_INBOX_REPORTS`.
- Candidate folder under triaged, rejected, salvage, or prototype area.
- Metadata, triage, module mapping, experiment plan, risk, and next-action files.
- Updated CSV and JSONL registry.

## Safety rules

- Never modify `01_PINE/MTC_V2.pine`.
- Never modify production Python runner files.
- Do not write Pine/Python/backtest/optimization code.
- Do not run backtests or optimizations.
- Do not write secrets, API keys, webhooks, broker credentials, or exchange keys.
- Read an existing file before deciding whether it is complete; do not overwrite.

## Folder behavior

Create the standard candidate files:

```text
<CandidateID>/
00_raw_quantlens_report.md
01_candidate_metadata.yaml
02_codex_triage.md
03_mtc_module_mapping.md
04_experiment_plan.md
05_risks_and_unknowns.md
06_next_action.md
```

## Registry behavior

Append one CSV row and one JSONL record. Preserve existing rows. Use status values from `_registry/status_legend.md`.

## Candidate ID rules

Use `QL_YYYY-MM-DD_<MARKET>_<TF>_<SHORT_STRATEGY_SLUG>`. If it already exists, append `_V2`, then increment if needed.

## STOP condition handling

Reject or mark salvage-only if rules are incomplete, source is closed, repaint/lookahead risk is unresolved, or the report is mostly marketing.

## Never modify production code rule

Intake is documentation only. `MTC_V2.pine` changes are only allowed in final integration after feature contract and parity planning.
