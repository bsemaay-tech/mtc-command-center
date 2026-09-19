# exit=1 from a 429 on the post-report turn; counted by Lead ruling

`launch.exit`: `exit=1 actual_exit=1 start=2026-09-19T09:27:22.4341298Z end=2026-09-19T09:43:27.1023718Z`.
Non-zero because the launcher's `try` block treats any non-zero `claude --print` exit as a
failure, and the CLI's exit here was non-zero due to a rate-limit hit — not because the review
task failed or was cut off.

## Evidence (stream.jsonl, line numbers and timestamps)
- Line 480 (assistant, `ts=2026-09-19T09:43:25.571Z`): `Write` tool call targeting
  `C:\tmp\OPUS_QUEUE_20260916\P1CAP\opus\OPUS_T0_REPORT.md`.
- Line 481 (user/tool_result, `ts=2026-09-19T09:43:25.590Z`): *"The file
  C:\tmp\OPUS_QUEUE_20260916\P1CAP\opus\OPUS_T0_REPORT.md has been updated successfully."* — the
  **final, successful write of the report**.
- Line 482 (`rate_limit_event`) and line 483 (assistant, `ts=2026-09-19T09:43:26.525Z`): the
  session-limit message *"You've hit your session limit - resets 1:40pm (Europe/Chisinau)"*.
- Line 484 (`result`, `"api_error_status":429`, `"terminal_reason":"api_error"`): the run
  terminates here.

**The 429 landed ~0.9 seconds AFTER the report's last successful write**, on the wrap-up turn
that followed it — not before or during report composition.

## Report completeness (independently confirmed)
`OPUS_T0_REPORT.md`: 492 lines, 11 numbered sections (`## 1.` through `## 11.`), ends with the
line `VERDICT: PASS-WITH-NITS`. Every citation the PACKAGE session grep-verified against the
committed `9f1aa532` blob was exact; one factual claim (both real captures' `account_state.json`
carrying `assetPositions`) was independently reproduced by re-parsing the fixture files.

## Ruling
Per the Lead's ruling (message to the P0-12 PACKAGE session, 2026-09-19): **COUNT this as
PASS-WITH-NITS.** Full adjudication: `OPUS_QUEUE_20260916/P1CAP/LEAD_ADJUDICATION_P1CAP_R1_T0.md`.
