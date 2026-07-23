# Task Contracts

## Purpose

Every non-trivial task or task requiring a fresh audit round must have a lead-owned task contract in this directory. The contract captures the complete authorization envelope before implementation begins and is updated by the lead between repair rounds.

## Contract lifecycle

1. **Lead creates** the contract during or after Gate 1 (Scope), before Gate 3 (Implementation) begins.
2. **Lead updates** `gate_state` and `repair_rounds` before each fresh audit at Gate 5.
3. **Lead updates** `updated_at` on every state change.
4. **Maximum 3 repair rounds** total (initial pass counts as round 0; repairs increment the counter).
5. After a final accepting verdict (PASS or PASS-WITH-NITS), the contract file is closed and remains as evidence.

## File naming

`<task_id>.json` where `task_id` is a short kebab-case identifier (e.g., `two-tier-policy-2026-07-22`).

## Schema reference

See `task_contract_v1.example.json` for the canonical schema with inline field documentation.

## Contract contents

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version (`1.0`) |
| `task_id` | string | Unique kebab-case task identifier |
| `objective` | string | One-sentence goal |
| `lead` | string | Lead orchestrator model |
| `implementer` | string | Implementer model + dispatch path |
| `files_allowed` | string[] | Exact whitelist of paths allowed for edits |
| `gate_state` | string | Current gate: `G1_SCOPE`, `G2_PLAN`, `G3_IMPLEMENTATION`, `G4_QA`, `G5_REVIEW`, `G6_SECURITY`, `G7_HANDOFF`, `CLOSED` |
| `repair_rounds` | integer | 0 = initial; 1-3 = repair round count |
| `authorization` | object | Boolean flags: `local_edits`, `commit`, `push`, `pr`, `merge`, `deploy`, `live` |
| `audit` | object | `model` (exact), `effort` (high/xhigh), `session_mode` (fresh) |
| `validation` | string | Validation/acceptance criteria |
| `updated_at` | string | ISO 8601 timestamp of last contract update |
