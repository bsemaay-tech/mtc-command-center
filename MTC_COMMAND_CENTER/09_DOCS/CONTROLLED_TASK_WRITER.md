# Controlled Task Writer

MVP-2 introduces a local write gate for task proposals. The dashboard HTTP API remains read-only.

## Input

Proposal files are placed under `02_TASKS/inbox/*.json`.

Supported action:

```json
{
  "schema_version": "1.0",
  "proposal_id": "TP-2026-0001",
  "action": "create_task",
  "task": {
    "id": "MCC-BOOT-999",
    "title": "Example task",
    "status": "READY",
    "assigned_ai": "Codex",
    "phase": "Example",
    "requires_user_input": false
  }
}
```

## Command

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly process-inbox
```

## Behavior

- Acquires `02_TASKS/.locks/task_queue.lock`.
- Rejects duplicate task IDs and malformed proposals.
- Validates candidate task queue and task history JSON against schemas.
- Copies existing task files into `03_STATUS/.backups/` before replacing them.
- Atomically replaces `TASK_QUEUE.json` and `TASK_HISTORY.json` for accepted proposals.
- Writes accepted/rejected receipts to `02_TASKS/outbox/`.
- Appends `TASK_PROPOSAL_ACCEPTED` or `TASK_PROPOSAL_REJECTED` to `03_STATUS/status_events.jsonl`.

## Non-goals

- No dashboard write buttons.
- No MTC_v2 changes.
- No backtest execution.
- No webhook or live trading operation.
