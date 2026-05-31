# Data Lineage Spec

Verified backtest, parity, optimization, and generated-output records require lineage.

Minimum fields:

```json
{
  "execution_id": "BT-2026-0001",
  "git_commit": null,
  "git_dirty": null,
  "config_hash_sha256": null,
  "data_hash_sha256": null,
  "code_hash_sha256": null,
  "engine_version": null,
  "python_version": null,
  "platform": "Windows",
  "command": null,
  "started_at": null,
  "finished_at": null
}
```

A result without lineage may be displayed as exploratory but cannot be marked verified.
