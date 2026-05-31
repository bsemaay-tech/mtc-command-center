# Data Contracts

MCC uses file-based contracts so the dashboard and AI workers can coordinate without hidden state.

## Status JSON

Status files in `03_STATUS` summarize current dashboard state. They should stay concise, valid JSON, and evidence-based.

## Registry JSON

Registry files in `05_REGISTRY` track long-lived objects such as strategies, cases, workers, data sources, and promotions.

## Task JSON

Task files in `02_TASKS` define work that AI workers can pick up and the history of completed or blocked tasks.

## Report Manifest

Report manifests should identify report ID, task ID, type, summary, creation time, and artifact paths. Detailed logs belong under `04_REPORTS`.

## Missing Data

When required input is absent, use `WAITING_FOR_USER` and describe the missing artifact rather than inventing a result.
