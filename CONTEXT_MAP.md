# CONTEXT_MAP — choose one stage

Choose the primary deliverable's row. For a cross-stage task, name one owner stage using the
highest-consequence primary change; other paths are dependencies, not extra onboarding stages.

| Primary path or work | Stage |
|---|---|
| `IBKR_PAPER_BRIDGE/**` | `IBKR_PAPER_BRIDGE/` |
| `mtc_cli/**` | `mtc_cli/` |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/**`; Pine modules in `04_SHARED/**` | `MTC_COMMAND_CENTER/01_MTC_PROJECT/` |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/**` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/` |
| `MTC_COMMAND_CENTER/03_QUANTLENS/**`; research registries; `00_INBOX/USER_INTAKE/**` | `MTC_COMMAND_CENTER/03_QUANTLENS/` |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/**` | `MTC_COMMAND_CENTER/08_DASHBOARD_APP/` |
| `MTC_COMMAND_CENTER/12_PARITY_PINETS/**` | `MTC_COMMAND_CENTER/12_PARITY_PINETS/` |
| Workflow, audit, planning, Git/handoff, migration, triage, other paths | `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/` |

Always load the selected stage's `AGENTS.md`. Read its `INPUTS.md` and `TESTS.md` before writes or
execution; relevant `HANDOFF.md` on resumption; `OUTPUTS.md` before delivering. Search only relevant
root `DECISIONS.md` rows. `CONTEXT.md` is a terminology lookup. History is search-on-demand.
