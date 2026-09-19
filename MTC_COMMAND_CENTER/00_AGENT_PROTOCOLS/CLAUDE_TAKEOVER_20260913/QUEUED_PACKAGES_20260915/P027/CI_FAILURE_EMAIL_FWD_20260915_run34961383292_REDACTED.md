# GitHub Actions failure e-mail — forwarded copy (tokens redacted)

```json
{
 "record": "github_actions_failure_email_artifact",
 "purpose": "WP-P0-27 R5 / Gemini NIT F-02: an immutable artifact that GitHub's native Actions failure e-mail reaches the owner",
 "gmail_account_read": "bsemaay3@gmail.com (the connector account; the GitHub notifications land in bsemaay@gmail.com and were forwarded by the owner)",
 "gmail_message_id": "1a0a4d879a3c386d",
 "gmail_thread_id": "1a0a4d879a3c386d",
 "gmail_internal_date_utc": "2026-09-15T11:33:45Z",
 "forwarded_by": "bsemaay@gmail.com",
 "original_sender": "notifications@github.com",
 "original_date_local": "Tue, Sep 15, 2026 at 2:06 PM (Europe/Istanbul = 11:06Z)",
 "original_subject": "[bsemaay-tech/mtc-command-center] PR run failed: Research gates - ci(research-gates): P0-30 checkers, contracts tests, Ruff light lint (WP-P0-27; T1 review before merge) (55ab90b)",
 "workflow_run": "34961383292 (PR #193 first run; P0-30 checkers (Windows) failed at checkout)",
 "note": "This is the PR-run failure mail of 2026-09-15 11:06Z, not the D026 demo mail of 08:18Z (run 34946092493, confirmed by the owner in chat). It proves the delivery channel with an immutable artifact; the demo mail can be attached the same way if forwarded. Personal notification tokens (email_token=...) redacted before storage.",
 "captured_by": "Claude Opus 5 Lead (743291) via the Gmail connector, read-only, 2026-09-15 11:48Z"
}
```

```text
---------- Forwarded message ---------
From: bsemaay-tech <notifications@github.com>
Date: Tue, Sep 15, 2026 at 2:06 PM
Subject: [bsemaay-tech/mtc-command-center] PR run failed: Research gates -
ci(research-gates): P0-30 checkers, contracts tests, Ruff light lint
(WP-P0-27; T1 review before merge) (55ab90b)
To: bsemaay-tech/mtc-command-center <mtc-command-center@noreply.github.com>
Cc: Ci activity <ci_activity@noreply.github.com>

[image: GitHub] [bsemaay-tech/mtc-command-center] Research gates workflow
run

  Research gates: Some jobs were not successful

View workflow run
<https://github.com/bsemaay-tech/mtc-command-center/actions/runs/34961383292?email_source=notifications&email_token=[REDACTED]>

Status Job Annotations
[image: Contracts tests and Ruff (Python 3.12)]

*Research gates* / Contracts tests and Ruff (Python 3.12)
Succeeded in 29 seconds
[image: Research gate checkers (Python 3.12)]

*Research gates* / Research gate checkers (Python 3.12)
Succeeded in 17 seconds
[image: P0-30 checkers (Python 3.12, Windows)]

*Research gates* / P0-30 checkers (Python 3.12, Windows)
Failed in 22 seconds
[annotations: 6]

—
You are receiving this because you are subscribed to this thread.
Manage your GitHub Actions notifications <https://github.com/settings/notifications?email_source=notifications&email_token=[REDACTED]>
GitHub, Inc. ・88 Colin P Kelly Jr Street ・San Francisco, CA 94107
```
