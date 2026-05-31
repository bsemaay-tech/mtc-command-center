# Task Lifecycle State Machine

Allowed states:

```text
TODO
READY
IN_PROGRESS
WAITING_FOR_USER
WAITING_FOR_AI_REVIEW
STALE
FAILED
DONE
ARCHIVED
```

Rules:

- A task must have an owner before `IN_PROGRESS`.
- A task with missing external input moves to `WAITING_FOR_USER`.
- An `IN_PROGRESS` task past `timeout_seconds` moves to `STALE`.
- `DONE` requires expected outputs, report, verification, and no forbidden action.
