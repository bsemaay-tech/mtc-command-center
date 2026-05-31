# Codex Repair Instructions

This document dictates exact repairs Codex must perform to finalize the restart audit.

## 1. Matching Repairs
Codex must resolve missing transcript and missing intake issues as documented in `MATCHING_AUDIT_FINDINGS.csv`. This includes finding/downloading the missing source files, and merging the duplicate entries for `VKNEJA5r8zw`.

## 2. Corrected Intake Repairs
Codex must update the generated intakes to include the missing trader wisdom mapped in `INTAKE_FAITHFULNESS_REVIEW.csv`.

## 3. Wiki Repairs
Codex must append the specific warnings, rules, and contexts listed in `WIKI_REPAIR_REQUESTS_FOR_CODEX.csv` to both the Trader Wiki and LLM Wiki.

## 4. Classification Repairs
Codex must execute the reclassifications explicitly defined in `CANDIDATE_RECLASSIFICATION_REQUESTS_FOR_CODEX.csv`, moving psychology/process videos out of the strategy pipeline.

## 5. Excel Workbook Updates
Codex must regenerate `QUANTLENS_RESTART_CLASSIFICATION_WORKBOOK.xlsx` to reflect the fixed mappings, updated faithfulness metrics, and reclassified candidates.

## 6. Priority Ranking
Codex should adopt Antigravity's priority rankings for the top test candidates when moving to the Phase 3 visual review sandbox.

## 7. MTC Sandbox Architecture
Codex must adhere to the shared external harness architecture decision validated by Antigravity, ensuring no sandbox code touches `MTC_V2.pine`.
