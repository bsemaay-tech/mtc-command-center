# ADR-0014 - minimal status event ledger

Status: Accepted

Context: Status snapshots need forensic recovery without full event sourcing.

Decision: Append accepted/rejected write events to `03_STATUS/status_events.jsonl`.

Consequences: JSON snapshots remain primary; JSONL supports audit and recovery.
