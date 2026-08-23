Read `AGENTS.md` first.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Use token-efficient workflow.
MANDATORY — launching Codex: always use `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1` (default `-Account secondary`). Never run bare `codex`, and never route to the desktop home `C:\Users\BarışSemaay\.codex`. Routes and snapshot quotas: `MTC_COMMAND_CENTER\_AI_MEMORY\AI_ACCOUNT_AND_MODEL_ROUTING.md`.
Update handoff files before stopping.
Do not scan the full repo unless required.

## Agent skills

### Issue tracker

GitHub Issues via `gh` CLI (`bsemaay-tech/mtc-command-center`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role vocabulary, unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context (`CONTEXT.md` + `docs/adr/` at repo root). See `docs/agents/domain.md`.
