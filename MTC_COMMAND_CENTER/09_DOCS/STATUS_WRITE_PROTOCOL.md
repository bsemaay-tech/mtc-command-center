# Status Write Protocol

MVP-0 and MVP-1 are read-only for the dashboard. Controlled writes begin in MVP-2.

Current MVP-2 entry point:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly process-inbox
```

Task proposals flow from `02_TASKS/inbox` to accepted/rejected receipts in `02_TASKS/outbox`.

Write sequence:

1. Acquire the canonical resource lock.
2. Build candidate payload in memory.
3. Validate against the matching schema.
4. Copy the current live file into `.backups/`.
5. Write a same-directory temp file.
6. Flush and close the temp file.
7. Re-read and validate the temp file.
8. Atomically replace temp over live.
9. Append one JSONL status event while still holding the lock.
10. Release the lock.

Never rename the live file out of place as a backup. On Windows sharing violations, retry briefly and then fail with `ERR-TASK-LOCKED`.
