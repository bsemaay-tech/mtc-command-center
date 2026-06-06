#!/usr/bin/env python3
"""Lightweight validator for the Strategy Research Lab registries.

Checks each registry under ``05_REGISTRY/`` that powers the Strategy Research
Lab tab:

  * JSON parses
  * validates against its ``06_SCHEMAS`` JSON Schema (reuses the dashboard
    validator when importable; otherwise skips schema check with a warning)
  * required per-entry fields present
  * no duplicate ids
  * ``source_file`` / ``source_folder`` paths exist on disk
  * ``report_path`` / report links resolve on disk

Hard errors -> exit 1. ``review_needed`` placeholders and empty optional
fields are reported as INFO, not failures (they are expected during gradual
classification).

Usage:
    python 03_QUANTLENS/tools/validate_research_registries.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUANTLENS_ROOT = Path(__file__).resolve().parents[1]
MCC_ROOT = QUANTLENS_ROOT.parent
REGISTRY_DIR = MCC_ROOT / "05_REGISTRY"
SCHEMA_DIR = MCC_ROOT / "06_SCHEMAS"

# (registry filename, schema filename, list key, id field, required fields,
#  path fields to existence-check)
SPECS = [
    ("STRATEGY_RESEARCH_REGISTRY.json", "strategy_research_registry.schema.json",
     "strategies", "strategy_id",
     ["strategy_id", "strategy_name", "source_folder", "strategy_category", "method"],
     ["source_folder", "source_file"]),
    ("INDICATOR_REGISTRY.json", "indicator_registry.schema.json",
     "indicators", "indicator_id", ["indicator_id", "indicator_name"], []),
    ("COMPONENT_REGISTRY.json", "component_registry.schema.json",
     "components", "component_id", ["component_id", "component_type"], []),
    ("TAG_DICTIONARY.json", "tag_dictionary.schema.json", None, None, [], []),
    ("RESEARCH_RUN_REGISTRY.json", "research_run_registry.schema.json",
     "research_runs", "research_run_id", ["research_run_id", "status"], ["report_path"]),
    ("VARIANT_LOG_REGISTRY.json", "variant_log_registry.schema.json",
     "variants", "variant_id", ["variant_id", "research_run_id"], ["report_link_or_path"]),
    ("RESEARCH_BACKTEST_REGISTRY.json", "research_backtest_registry.schema.json",
     "results", "variant_id", ["research_run_id", "variant_id"], []),
    ("TRIAGE_CANDIDATE_REGISTRY.json", "triage_candidate_registry.schema.json",
     "candidates", "stg_code", ["stg_code"], ["transcript_path"]),
]


def _load_validator():
    api = MCC_ROOT / "08_DASHBOARD_APP" / "apps" / "api"
    if api.exists():
        sys.path.insert(0, str(api))
        try:
            from mcc_readonly.schema import validate_json_schema  # type: ignore
            return validate_json_schema
        except Exception:
            return None
    return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    info = 0
    validate = _load_validator()

    for filename, schema_name, list_key, id_field, required, path_fields in SPECS:
        path = REGISTRY_DIR / filename
        if not path.exists():
            errors.append(f"{filename}: missing")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{filename}: JSON parse error: {exc}")
            continue

        schema_path = SCHEMA_DIR / schema_name
        if validate and schema_path.exists():
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                for issue in validate(data, schema):
                    errors.append(f"{filename}: schema {issue.path}: {issue.message}")
            except Exception as exc:
                warnings.append(f"{filename}: schema check skipped ({exc})")
        elif not validate:
            warnings.append(f"{filename}: schema validator unavailable, skipped")

        if list_key is None:
            continue
        entries = data.get(list_key, [])
        seen: set[str] = set()
        for i, entry in enumerate(entries):
            loc = f"{filename}[{i}]"
            for field in required:
                if field not in entry or entry[field] in (None, "", []):
                    errors.append(f"{loc}: missing required field '{field}'")
            if id_field:
                eid = entry.get(id_field)
                if eid in seen:
                    errors.append(f"{loc}: duplicate id '{eid}'")
                elif eid:
                    seen.add(eid)
            for pf in path_fields:
                val = entry.get(pf)
                if val and val != "review_needed" and not str(val).startswith("http"):
                    if not (MCC_ROOT / val).exists():
                        errors.append(f"{loc}: {pf} path not found: {val}")
            # count review_needed as info
            info += sum(1 for v in entry.values() if v == "review_needed"
                        or (isinstance(v, list) and v == ["review_needed"]))

    print(f"INFO: {info} 'review_needed' placeholders across registries")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1
    print("\nOK: all research registries valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
