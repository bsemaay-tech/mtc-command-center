# S1 — DeepSeek A1: Strategy Metadata Extractor (Fill "review_needed" Fields)

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
This is the MTC Command Center — a trading strategy research + backtesting system.
63 strategy directories exist. Each has a plain-English `07_deterministic_spec.md`
describing entry/exit/stop/trailing rules. The registry generator
(`build_strategy_research_registry.py`) produces `STRATEGY_RESEARCH_REGISTRY.json`
from per-strategy source files but hardcodes several fields as `"review_needed"` —
specifically `trailing_logic`, `filters_used`, `known_strengths`, `known_weaknesses`.
Your task fills those fields from `07_deterministic_spec.md` and patches the generator
to read them from source files.

---

## Task A1a — Write extractor script

Write `MTC_COMMAND_CENTER/03_QUANTLENS/tools/extract_strategy_metadata.py`

The script iterates every dir in `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STGxxx_*/`
and for each:

1. Reads `07_deterministic_spec.md` (main spec — REQUIRED; skip strategy if missing).
2. Extracts these 4 fields with LLM-quality text understanding:
   - `trailing_logic` — trailing exit rule (e.g. "close below 10 EMA → exit next open") OR `"N_A"` if no trailing
   - `filters_used` — regime/MA/volume/indicator filters (comma-separated) OR `"N_A"` if none
   - `known_strengths` — 1-2 line objective summary from the spec
   - `known_weaknesses` — 1-2 line summary of risks/limitations from the spec
3. Writes the 4 fields into the strategy's source file:
   - If `producer_spec.json` exists → update those 4 keys in-place (JSON patch; keep all other keys)
   - Else → append to `01_candidate_metadata.yaml` under block `# --- A1 Extracted (auto) ---` (do NOT overwrite existing YAML keys)
4. Prints a summary line per strategy: `[OK|SKIP|ERROR] STGxxx — reason`

Run: `python MTC_COMMAND_CENTER/03_QUANTLENS/tools/extract_strategy_metadata.py`

---

## Task A1b — Patch registry generator

Edit `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py`

**Find** the `build_strategy_entry()` function. Around line 344-345 you will see:
```python
"trailing_logic": REVIEW,
"filters_used": REVIEW,
```
And around line 354-355:
```python
"known_strengths": REVIEW,
"known_weaknesses": ...
```

**Patch 1** — make these 4 fields read from source files instead of hardcoding REVIEW:
```python
"trailing_logic": spec.get("trailing_logic") or meta.get("trailing_logic") or REVIEW,
"filters_used": spec.get("filters_used") or meta.get("filters_used") or REVIEW,
```

**Patch 2** — in the `explicit` dict (around line 362) add:
```python
"trailing_logic": meta.get("trailing_logic"),
"filters_used": meta.get("filters_used"),
"known_strengths": meta.get("known_strengths"),
"known_weaknesses": meta.get("known_weaknesses"),
```

These patches make the generator prefer source-file values over its hardcoded REVIEW.

---

## Task A1c — Regenerate + validate

```bash
cd C:\LAB\Tradingview_LAB_CLEAN
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/extract_strategy_metadata.py
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py --check
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/validate_research_registries.py
```

Count how many fields changed from `"review_needed"` to real content in
`MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json`.

---

## HARD SAFETY RULES — do NOT violate

- NEVER edit: `*.pine` files, `MTC_V2.pine`, `mega_walk_forward.py`, any file in
  `02_MTC_BACKTEST/src/engine/`, `02_MTC_BACKTEST/src/config/`
- NEVER edit `05_REGISTRY/*.json` directly — they are generated outputs
- Only write to:
  - `03_QUANTLENS/strategies/STGxxx_*/producer_spec.json` (update existing keys only)
  - `03_QUANTLENS/strategies/STGxxx_*/01_candidate_metadata.yaml` (append under `# --- A1 Extracted (auto) ---`)
  - `03_QUANTLENS/tools/extract_strategy_metadata.py` (new file)
  - `03_QUANTLENS/tools/build_strategy_research_registry.py` (surgical patch only)

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S1_DEEPSEEK_A1_REPORT.md`

Report must contain:
- Total strategies found / processed / skipped (and why skipped)
- Count of `producer_spec.json` files updated
- Count of `01_candidate_metadata.yaml` files updated
- Count of fields that changed from `review_needed` → real content (before/after count from registry)
- Output of `--check` command (pass/fail)
- Output of `validate_research_registries.py` (pass/fail)
- Any strategies where extraction was ambiguous or failed
- py_compile result for both modified Python files
