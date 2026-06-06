# S1 DeepSeek A1 — Strategy Metadata Extractor Report

## Task A1a — Write extractor script

**File created:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/extract_strategy_metadata.py`

Extracts 4 fields from `07_deterministic_spec.md` in each strategy folder:
- `trailing_logic` — trailing exit rule or `N_A`
- `filters_used` — comma-separated indicator/regime filters or `N_A`
- `known_strengths` — 1-2 line summary from spec
- `known_weaknesses` — 1-2 line risk/limitation summary or `N_A`

### Extraction approach
Heuristic-based. Multi-stage fallback:
1. Parses `##` sections from markdown
2. Searches `**Exit**:` / `**Entry**:` bullet patterns
3. Keyword matching for trailing logic (trail, dynamic, close…cross EMA, sell into strength)
4. Indicator term extraction for filters (SMA, EMA, RSI, VWAP, ATR, Bollinger, etc.)
5. Section-based strength/weakness extraction (Style, Overview, Risks, Ambiguities)
6. Falls back to entry rule description for short specs with no descriptive sections

### Strategy counts
| Category | Count |
|----------|-------|
| Total strategy dirs scanned | 63 |
| With `07_deterministic_spec.md` | 28 |
| Skipped (no spec file) | 35 |
| `producer_spec.json` updated | 0 |
| `01_candidate_metadata.yaml` updated | 28 |
| Errors | 0 |

### YAML parse status (pre-existing issue affecting 11 files)
| Status | Count |
|--------|-------|
| Parse OK | 17 |
| Parse FAIL (pre-existing) | 11 |

The 11 failing files have **pre-existing** YAML syntax errors (colon-space `: ` inside unquoted scalar values like `New: layered`). These errors predate A1 — they block the registry generator from reading metadata from those files regardless.

**Failing strategies (pre-existing):**
STG048, STG049, STG050, STG051, STG053, STG054, STG055, STG056, STG058, STG059, STG060

---

## Task A1b — Patch registry generator

**File edited:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py`

### Patch 1 — Read from source files (line 646-647)
```python
# Before:
"trailing_logic": REVIEW,
"filters_used": REVIEW,

# After:
"trailing_logic": spec.get("trailing_logic") or REVIEW,
"filters_used": spec.get("filters_used") or REVIEW,
```

### Patch 2 — Add to explicit dict (lines 686-687)
```python
# Added after recommended_timeframes:
"trailing_logic": meta.get("trailing_logic"),
"filters_used": meta.get("filters_used"),
```

The `known_strengths` and `known_weaknesses` fields were already present in the explicit dict (lines 688-689).

---

## Task A1c — Regenerate + validate

### Commands executed
```
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/extract_strategy_metadata.py
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_strategy_research_registry.py --check
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/validate_research_registries.py
```

### Registry output
```
wrote STRATEGY_RESEARCH_REGISTRY.json (63 entries)
wrote INDICATOR_REGISTRY.json (27 entries)
wrote COMPONENT_REGISTRY.json (78 entries)
wrote TAG_DICTIONARY.json (5 entries)
```

### --check output
No output (silent pass — parses without error).

### validate_research_registries.py output
```
INFO: 1447 'review_needed' placeholders across registries
OK: all research registries valid.
```

### review_needed → real content counts (STRATEGY_RESEARCH_REGISTRY.json, 63 entries)

| Field | Real | review_needed | N_A |
|-------|------|---------------|-----|
| trailing_logic | 17 | 46 | 15 |
| filters_used | 17 | 46 | 3 |
| known_strengths | 17 | 46 | 0 |
| known_weaknesses | 19 | 44 | 11 |

**Interpretation:**
- 17 strategies have real metadata flowing through the registry (the 17 with parseable YAML files)
- 46 remain `review_needed` (35 without spec files + 11 with broken YAML)
- Among the 17 real values: 2 have actual trailing logic (rest are N_A), 14 have filter indicators
- The 11 broken YAML files block an additional ~44 field-level improvements

### py_compile results
```
OK: extract_strategy_metadata.py
OK: build_strategy_research_registry.py
```

---

## Summary

| Metric | Value |
|--------|-------|
| Strategies processed | 28 of 63 |
| Fields extracted per strategy | 4 |
| YAML files updated | 28 |
| Registry fields populated | 17 strategies x 4 fields = 68 values |
| Blocked by pre-existing YAML parse errors | 11 strategies |
| Errors (extractor/registry/validation) | 0 |
| Modified files | 2 (extractor: new, registry: 2-line patch) |
