# ADR-0013 - manual input drop-folder

Status: Accepted

Context: The user provides transcripts, exports, compile output, and approvals.

Decision: Use `00_INBOX/from_user/<input_id>/` with manifests and hashes.

Consequences: AI agents do not scan arbitrary user folders.
