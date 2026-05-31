# Error Taxonomy

| Code | Meaning | Typical action |
|---|---|---|
| `ERR-PATH-UTF8` | UTF-8 path read/write failed | Run path validation and fix encoding |
| `ERR-PATH-LENGTH` | Path exceeds safe length | Shorten IDs or use long-path helper |
| `ERR-JSON-SCHEMA` | JSON failed schema validation | Quarantine candidate payload |
| `ERR-TASK-STALE` | Task exceeded timeout | Review before reassignment |
| `ERR-TASK-LOCKED` | Resource lock is active or OS denied access | Retry later or inspect lock |
| `ERR-PROTECTED-PATH` | Protected path touched without approval | Stop and create patch plan |
| `ERR-DATA-MISSING` | Required data is absent | Mark `WAITING_FOR_USER` |
| `ERR-DATA-HASH` | Data hash mismatch | Rebuild manifest |
| `ERR-PARITY-DIVERGENCE` | Parity mismatch | Create diagnosis report |
| `ERR-PARITY-MISSING-TW_EXPORT` | TradingView export absent | Request user export |
| `ERR-BACKTEST-FAILED` | Backtest command failed | Capture lineage and report |
| `ERR-PINE-COMPILE` | TradingView compile failed | Use Handoff Paste Block |
| `ERR-PINE-REPAINT-RISK` | Repaint risk detected | Block promotion |
| `ERR-QUANTLENS-DUPLICATE` | Candidate duplicate | Link existing candidate |
| `ERR-LIVEOPS-DISABLED` | LiveOps action attempted early | Keep dry-run only |
