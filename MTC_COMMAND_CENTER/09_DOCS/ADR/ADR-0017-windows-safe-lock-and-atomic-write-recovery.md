# ADR-0017 - Windows-safe lock and atomic write recovery

Status: Accepted

Context: Windows file sharing can block rename/replace operations.

Decision: Use bounded retries, corrupt-lock recovery, copy-not-rename backups, and single-line JSONL appends inside the lock.

Consequences: Controlled writes fail recoverably instead of corrupting status files.
