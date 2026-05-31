# Recovery Playbook

Common recovery paths:

- Invalid JSON: leave live file untouched, move candidate to `03_STATUS/quarantine/`, record `ERR-JSON-SCHEMA`.
- Stale lock: rename to `.lock.stale.<ts>`, append task history event, continue.
- Corrupt lock: rename to `.lock.corrupt.<ts>`, append task history event, continue.
- Protected-path exposure: stop work, produce risk report, request user approval.
- Missing user input: mark task `WAITING_FOR_USER` with exact request.

Never delete forensic files during recovery.
