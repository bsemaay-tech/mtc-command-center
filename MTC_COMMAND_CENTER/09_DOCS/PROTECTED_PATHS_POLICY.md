# Protected Paths Policy

Protected targets:

```text
MTC_V2.pine
01_MASTER TEMPLATE_V2/01_PINE/
01_MASTER TEMPLATE_V2/00_PYTHON/
01_MASTER TEMPLATE_V2/05_PARITY/
Existing TradingView export archives
Canonical feature contracts
MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md
```

Modification gate:

1. Diagnosis report exists.
2. Patch plan exists.
3. Risk report exists.
4. User approval is recorded.
5. Commit message contains `APPROVED-PATCH-PLAN: <task_id>`.
6. Verification report is produced.

The hook under `09_DOCS/hooks/protected_paths_hook.py` is the mechanical guard for commits.
