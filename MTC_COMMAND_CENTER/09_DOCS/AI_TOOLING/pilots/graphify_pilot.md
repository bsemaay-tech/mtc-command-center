# Pilot — Graphify (code → knowledge graph / impact analysis)

**Date:** 2026-06-21 · **By:** Claude Opus 4.8 · **Verdict:** ✅ KEEP as an **on-demand** impact-analysis tool. NOT auto, NOT whole-repo, graphs never committed. (Confirms the earlier downgrade from "immediate architecture layer" → pilot.)

## What / install
PyPI package **`graphifyy`** (double-y), v0.8.44. Builds a queryable code graph via tree-sitter.
- Code extraction = **fully local, no API key, nothing leaves the machine**. Only doc/PDF/image/video extraction or community-naming needs an LLM key — skipped here.
- Install (isolated, no repo footprint): `uv tool install graphifyy --python 3.13`.
- Windows OK (use `graphify .`, not `/graphify .`).
- Output: `graphify-out/{graph.json, graph.html, GRAPH_REPORT.md}` — **written into the TARGET path's** `graphify-out/`, not CWD. So running on the repo writes into the repo → see caveats.

## How piloted (safe)
1. Copied the 28 `mcc_readonly/*.py` files to `C:\tmp\graphify_pilot\src` (repo read-only; all writes in tmp).
2. `ANTHROPIC_API_KEY= OPENAI_API_KEY= GEMINI_API_KEY= graphify update ./src --no-cluster` (keys blanked, no clustering = 100% local, keyless).
3. Result: **446 nodes, 1597 edges** from 28 files.

## Results (accurate, verifiable)
- `graphify affected "read_model.py"` → **cli.py, health.py, server.py, __main__.py** = exactly the modules that import read_model. Correct reverse-dependency / blast-radius answer.
- `graphify explain "pipeline_reader"` → imported by audit_reader + read_model; imports paths, presentation_reader, …; degree 50. Matches reality.
- `graphify query "what builds the dashboard snapshot"` → starts at `build_dashboard_snapshot()` (read_model.py:323), traverses to the readers it pulls. Correct but verbose (212 nodes; tune `--budget`/`--context`).

## Value judgement
- `affected` / `explain` give clean **transitive** impact answers in one command — a real win over manual grep for "what breaks if I touch X". For a single-file "who imports X", grep is still fine.
- Not essential: this repo already has registries + a compact, well-named codebase. Graphify is a convenience layer, not a missing capability. Hence **on-demand, not always-on**.

## Caveats / rules
- **Never commit graphs.** `.gitignore` now has `graphify-out/` + `**/graphify-out/`.
- **Don't run on the whole MTC repo blind** — thousands of config/JSON files → heavy graph + noise. Scope to a subdir, or copy the target out to tmp (as done here).
- **Did NOT run `graphify install`** — that registers a skill into assistant config dirs (claude/codex/etc.). Defer until we decide whether we want it as an agent skill.
- Doc/PDF/video extraction + community naming need an LLM key → out of scope for code-only use.

## Acceptance — PASS (conditional)
Accurate, keyless, isolated. Keep as a manual impact-analysis helper. Recommended invocation pattern:
```
uv tool install graphifyy --python 3.13          # once
graphify update <path-or-copy> --no-cluster       # build (local, keyless)
graphify affected "<file.py>"  --graph <path>/graphify-out/graph.json
graphify explain  "<symbol>"   --graph <…>/graph.json
graphify query    "<question>" --graph <…>/graph.json --budget 800
```

## Next (optional, approval-gated)
- Decide if `graphify install` (agent skill) is wanted, or keep CLI-only.
- If used regularly, a tiny wrapper (like markitdown_ingest.py) that copies a scoped dir → tmp → builds, so graphs never land in the repo tree.
