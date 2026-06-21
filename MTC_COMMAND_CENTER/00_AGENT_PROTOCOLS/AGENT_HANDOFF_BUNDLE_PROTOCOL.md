# Agent Handoff Bundle Protocol

Codex or Claude should prepare a local handoff bundle when ChatGPT Web needs context that GitHub cannot expose.

## Required Bundle Content

- `CHATGPT_HANDOFF.md`
- `git_status_short.txt`
- `git_status_sb.txt`
- `git_log_oneline_20.txt`
- `git_diff_stat.txt`
- `git_cached_diff_stat.txt`
- `protected_scope_diff.txt`
- `api_healthz.json` if available
- `api_snapshot_summary.json` if available
- `api_snapshot_night_artifacts_summary.json` if available
- curated screenshots if available
- selected source files only
- selected reports only
- manifest

## Exclude

- `.env`
- keys
- secrets
- `.git`
- `node_modules`
- raw data dumps
- large full `05_BACKTEST_RESULTS` dumps
- broker, live, or paper credentials

## Manifest Rules

The manifest must list every included file, why it was included, and whether it is committed, ignored, or untracked locally.

## Runtime/API Snapshot Rules

Runtime files are evidence, not source of truth. Include compact summaries instead of full raw payloads whenever possible. If an API endpoint is unavailable, record the exact command attempted and the meaningful error.

## Source Selection Rules

Include only files needed for the review question. Do not zip the whole repo. Do not include protected or sensitive files unless the user explicitly approved that exact inclusion.
