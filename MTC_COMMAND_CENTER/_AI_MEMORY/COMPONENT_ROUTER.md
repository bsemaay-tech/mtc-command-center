# COMPONENT_ROUTER

Router contract for the modular-monorepo. Read immediately after root `AGENTS.md` and root `START_HERE.md`, before accessing any volatile memory (GLOBAL_HANDOFF, NEXT_STEPS, ACTIVE_FILES). `SESSION_LOG.md` is retired — historical-only, not a cold-start file.

---

## 1. Path-Based Routing (primary)

Match the task's primary working path prefix to a component, then load that component's local memory chain instead of root histories.

| Path prefix | Component | Local onboarding chain |
|---|---|---|
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/` | **MTC V2** | `01_MTC_PROJECT/AGENTS.md` → `01_MTC_PROJECT/_AI_MEMORY/START_HERE.md` → `CURRENT.md` → `NEXT_STEPS.md` |
| `MTC_COMMAND_CENTER/12_PARITY_PINETS/` | **MTC V2 — protected reference** | Same chain as MTC V2. `12_PARITY_PINETS/` is read-only; never edit any file there. |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/` | **MTC Backtest** | `02_MTC_BACKTEST/AGENTS.md` → `02_MTC_BACKTEST/_AI_MEMORY/START_HERE.md` → `CURRENT.md` → `NEXT_STEPS.md` |
| `MTC_COMMAND_CENTER/03_QUANTLENS/` | **QuantLens Research** | `03_QUANTLENS/AGENTS.md` → `03_QUANTLENS/_AI_MEMORY/START_HERE.md` → `CURRENT.md` → `NEXT_STEPS.md` |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/` | **Dashboard** | `08_DASHBOARD_APP/AGENTS.md` → `08_DASHBOARD_APP/_AI_MEMORY/START_HERE.md` → `CURRENT.md` → `NEXT_STEPS.md` |
| `IBKR_PAPER_BRIDGE/` | **Bridge** | `IBKR_PAPER_BRIDGE/AGENTS.md` → `IBKR_PAPER_BRIDGE/_AI_MEMORY/START_HERE.md` → `CURRENT.md` → `NEXT_STEPS.md` |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/`, `MTC_COMMAND_CENTER/04_SHARED/`, `MTC_COMMAND_CENTER/05_REGISTRY/`, `MTC_COMMAND_CENTER/06_SCHEMAS/`, `MTC_COMMAND_CENTER/07_ADAPTERS/`, `MTC_COMMAND_CENTER/09_DOCS/ADR/`, repo root policy files, or no single component prefix | **Global/Shared** | Root `_AI_MEMORY/AI_RULES.md` → `GLOBAL_HANDOFF.md` → `NEXT_STEPS.md` (`ACTIVE_FILES.md`, `DECISIONS.md`, `PROJECT_MEMORY.md` selective by task; `SESSION_LOG.md` historical-only — never a normal cold-start file) |

---

## 2. Keyword Routing (secondary — when path is ambiguous)

Use these keywords when no clear path prefix identifies the component:

| Keywords in task | Route to |
|---|---|
| MTC V2, Pine strategy, parity, layer, candle pattern, Pine script | MTC V2 |
| backtest engine, parity suite, `parity_compare`, `parity_test`, `mtc_bridge.mjs` | MTC Backtest |
| QuantLens, walk-forward, research run, CPCV, DSR, strategy research, overnight sweep | QuantLens Research |
| dashboard, web UI, `app.js`, `/api/snapshot`, `/api/read-model` | Dashboard |
| bridge, Hyperliquid, paper trade, `bridge.app`, execution, broker, testnet | Bridge |
| ADR, agent protocol, shared prompt, schema, registry, repo policy, `DO_NOT_TOUCH`, sprint workflow | Global/Shared |

---

## 3. Ambiguity Fallback

**Multi-component task** (task touches two or more components):
1. Load each affected component's local chain first: `<component>/AGENTS.md` -> `<component>/_AI_MEMORY/START_HERE.md` -> `CURRENT.md` -> `NEXT_STEPS.md` for each component.
2. Load root volatile files (`GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md`) only when cross-component coordination history is actually required — not unconditionally. `SESSION_LOG.md` is retired historical-only; never load it as a default cold-start file.
3. Document the cross-component scope in the G1 scope contract and follow Section 4 (Cross-Component Behavior).

**No-component task** (repo policy, shared contracts, ADRs, global governance, or no component can be identified from path or keywords):
Use the **Global/Shared** route and load root `_AI_MEMORY/` volatile memory. Document scope in the G1 scope contract.

---

## 4. Cross-Component Behavior

When a task touches two or more components:
1. Use the global G1 prompt with each affected local chain. Load root histories only if cross-component coordination or history is actually needed — not unconditionally.
2. During G7 write-back: update every affected component per the component-scoped G7 rules below, then add one concise root `GLOBAL_HANDOFF.md` coordination entry.
3. Do not duplicate per-component details in the root entry; the root entry is a coordination pointer only.

---

## 5. Gate 7 (Memory Write-Back) — Scoped Contract

This contract overrides any "always update root GLOBAL_HANDOFF" language in older prompts. The applicable rule is determined by the route selected at startup.

### Component-scoped task (single component)

| File | Rule |
|---|---|
| `<component>/_AI_MEMORY/CURRENT.md` | Always update |
| `<component>/_AI_MEMORY/NEXT_STEPS.md` | Always update |
| `<component>/_AI_MEMORY/DECISIONS.md` | Update if a sticky decision was made |
| `<component>/_AI_MEMORY/ACTIVE_FILES.md` | Update if working set changed |
| Root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md` | **Do not touch** |
| Root `SESSION_LOG.md` | **Retired — do not read or write** |

### Cross-component task

Update every affected component per the component-scoped rules above, then add one concise coordination entry to root `GLOBAL_HANDOFF.md`. Root `NEXT_STEPS.md` updated only for cross-component next steps. Root `ACTIVE_FILES.md` updated only if a cross-component working set change occurred.

### Global/policy task (root policy, shared contracts, repo-wide governance, no single component owner)

Use root memory files: `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `ACTIVE_FILES.md`, `PROJECT_MEMORY.md` per the existing write-back contract in `AI_RULES.md`.

---

## 6. Protected Reference

`MTC_COMMAND_CENTER/12_PARITY_PINETS/` is a protected reference owned by the MTC V2 route. Read access only for parity context. Never edit, delete, or create any file there.

---

## 7. Root Historical Files

Root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `ACTIVE_FILES.md` are readable and are the correct source when:
- Performing cross-component coordination
- Investigating repo-wide policy
- Onboarding to historical context spanning multiple components

`SESSION_LOG.md` is **retired historical-only**. Read it only for explicit historical investigation; never as a default cold-start file, cross-component coordination file, or normal volatile state source.

Component-scoped tasks do not require reading root histories.
