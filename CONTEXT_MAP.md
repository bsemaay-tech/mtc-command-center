# CONTEXT_MAP — choose one stage

Choose the row containing the task's primary deliverable. Read only that row's five files. If a
task spans rows, Gate 1 names one owner stage using the highest-risk primary change; other paths are
dependencies, not extra onboarding stages.

| Primary path or work | One stage |
|---|---|
| `IBKR_PAPER_BRIDGE/**` | `IBKR_PAPER_BRIDGE/` |
| `mtc_cli/**` | `mtc_cli/` |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/**`; Pine modules under `04_SHARED/**` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/` |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/**` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/` |
| `MTC_COMMAND_CENTER/03_QUANTLENS/**`; strategy-research registries or `00_INBOX/USER_INTAKE/**` | `MTC_COMMAND_CENTER/03_QUANTLENS/` |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/**` | `MTC_COMMAND_CENTER/08_DASHBOARD_APP/` |
| `MTC_COMMAND_CENTER/12_PARITY_PINETS/**` | `MTC_COMMAND_CENTER/12_PARITY_PINETS/` |
| Workflow, audit, planning, Git/handoff, migration, triage, or every other repository path | `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/` |

Within the selected stage read, in order: `AGENTS.md`, `INPUTS.md`, `OUTPUTS.md`, `TESTS.md`,
`HANDOFF.md`. Read `CONTEXT.md` only when terminology is unclear. History is grep-on-demand.
