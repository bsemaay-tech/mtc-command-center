# AI Dispatch Harness — token-efficient delegation

**Why:** the expensive model (Claude) must spend its tokens on *decisions + specs + audits*,
not on mechanical reading/editing. Cheap models (DeepSeek, Grok, OpenRouter free) do the
read/edit/verify labor. This harness lets ANY OpenAI-compatible model run as a **sandboxed
sub-agent** that edits real repo files, while the orchestrator only writes a task and audits
the result.

**This is the default working mode for SP-004 and any bounded mechanical work.**

## How to dispatch (orchestrator = Claude or Codex)

1. Write a task JSON (see schema below) to `C:\tmp\<name>_task.json`.
2. Run: `python _deepseek_driver/ds_agent.py --task C:\tmp\<name>_task.json`
3. Read the printed completion report (also saved to `C:\tmp\ds_*_report.md`).
4. **Audit it yourself** — never trust the report. Re-run the real validation
   (py_compile / jsonschema / smoke on real data) before accepting.

## Task JSON schema

```json
{
  "title": "short label",
  "provider": "deepseek",          // deepseek | grok | xai | openrouter | openai | ollama
  "model": "deepseek-v4-pro",      // provider-specific model id
  "max_iters": 45,
  "report_out": "C:/tmp/ds_x_report.md",
  "allow":  ["ABS/path/file1.py"], // files the sub-agent may WRITE (exact paths)
  "schema_allow": [],              // 06_SCHEMAS files to permit (SOFT denylist override)
  "read_extra": ["ABS/path/ref"],  // read-only references
  "prompt": "the full spec: exact edits, line refs, validation, mandatory report sections"
}
```

## Providers (keys via env)

| provider | base_url | key env | notes |
|---|---|---|---|
| `deepseek` | api.deepseek.com | `DEEPSEEK_API_KEY` | primary; `deepseek-v4-pro` / `deepseek-chat` |
| `grok`/`xai` | api.x.ai/v1 | `XAI_API_KEY` | `grok-4` solid |
| `openrouter` | openrouter.ai/api/v1 | `OPENROUTER_API_KEY` | `:free` models = rate-limited, use for cheap/parallel/fallback |
| `openai` | api.openai.com/v1 | `OPENAI_API_KEY` | if set |
| `ollama` | localhost:11434/v1 | (none) | local, offline |

Route cheap/bulk work to the cheapest capable model; keep critical correctness gates auditable.
Tool-calling models = fully autonomous (read+edit+verify). Non-tool models = proposer mode
(return code, orchestrator applies).

## Safety rails (enforced in `ds_agent.py`, cannot be prompted away)

- **HARD denylist** (never writable, no override): `*.pine`, `parity`, `MTC_V2`, `.git/`.
- **SOFT denylist**: `06_SCHEMAS` — writable only if the file is listed in `schema_allow`.
- Writes restricted to the task `allow` list; everything else read-only.
- `run_python` is **read-only**: AST-guard blocks `open`/write/`exec`/`subprocess`/`shutil`/
  network — all edits must go through guarded `edit_file`/`write_file`.
- No git/commit capability in the harness. Barış commits.
- `read_file` capped at 60KB (pass a small sample for huge files; don't feed 5MB JSON).
- Every write echoed to stdout; full transcript + report dumped to `C:/tmp/ds_*_report.md`.

## Orchestrator rules (the token contract)

1. **Dispatch by default.** Any bounded mechanical edit (single/few files, known change,
   schema/JSON, script writing, audit run) → write a task, dispatch, audit. Do NOT hand-edit
   it yourself unless the fix is a trivial 1-liner where a dispatch round-trip costs more.
2. **Orchestrator keeps:** the decision, the spec, the skeptical audit. Nothing else.
3. **Always audit on real data.** Sub-agent reports are unverified until you reproduce the
   validation. Accept only on your own green result.
4. **Serialize tasks that touch the same files**; parallelize disjoint ones.
5. **Huge inputs:** pre-extract a small sample (the model can't read 5MB; harness caps at 60KB).
6. Every accepted batch: update handoff (`SESSION_LOG`, `NEXT_STEPS`, `GLOBAL_HANDOFF`).
