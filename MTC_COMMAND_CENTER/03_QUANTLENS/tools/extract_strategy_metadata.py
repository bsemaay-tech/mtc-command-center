#!/usr/bin/env python3
"""
extract_strategy_metadata.py — S1 A1a
Extracts trailing_logic, filters_used, known_strengths, known_weaknesses
from 07_deterministic_spec.md for each strategy folder.
Patches producer_spec.json or appends to 01_candidate_metadata.yaml.
"""

import os
import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
STRATEGIES_DIR = ROOT / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "strategies"


def _clean_md(text):
    """Strip markdown formatting: **bold**, *italic*, bullet chars, leading #."""
    t = text.strip()
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)  # bold
    t = re.sub(r"\*(.+?)\*", r"\1", t)  # italic
    t = re.sub(r"^[-*]\s+", "", t)  # bullet
    t = re.sub(r"^#+\s*", "", t)  # heading
    t = re.sub(r"\s+", " ", t)  # collapse whitespace
    # Normalize common Unicode: em-dash, en-dash, smart quotes
    t = t.replace("\u2014", "--").replace("\u2013", "-")
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    return t.strip()


def _parse_md_sections(text):
    """Split markdown into sections keyed by ## header (lowercase)."""
    sections = {}
    current_key = "_preamble"
    current_lines = []
    for line in text.split("\n"):
        m = re.match(r"^##\s+(.+)", line)
        if m:
            if current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = m.group(1).strip().lower().replace(" ", "_")
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections[current_key] = "\n".join(current_lines).strip()
    return sections


def _first_bullet_value(text, key_pattern):
    """Extract value after `**Key**:` in a markdown bullet line."""
    for line in text.split("\n"):
        m = re.search(rf"\*\*{key_pattern}\*\*:?\s*(.+)", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _get_section(sections, *names):
    """Return first matching section content."""
    combined = {}
    for name in names:
        key = name.replace(" ", "_").lower()
        if key in sections:
            combined[key] = sections[key]
    if not combined:
        return ""
    # Return the longest matching section
    return max(combined.values(), key=len, default="")


def _extract_indicator_terms(text):
    """Extract named indicators/MA types from text."""
    text_lower = text.lower()
    terms = set()

    indicator_map = {
        "sma": "SMA",
        "ema": "EMA",
        "vwap": "VWAP",
        "rsi": "RSI",
        "macd": "MACD",
        "bollinger": "Bollinger Bands",
        "atr": "ATR",
        "adx": "ADX",
        "volume": "Volume",
        "relative_strength": "RS",
        "parabolic": "Parabolic SAR",
        "standard_deviation": "StdDev",
        "moving_average": "MA",
        "supertrend": "SuperTrend",
    }

    for keyword, label in indicator_map.items():
        if keyword in text_lower:
            terms.add(label)

    return sorted(terms)


def extract_trailing_logic(text, sections):
    """Extract trailing exit / stop logic."""
    # Collect all text sections for broad search
    all_content = text + "\n".join(sections.values())

    # Check **Exit**: bullet in full text or rules section
    exit_patterns = [
        r"\*\*Exit\*\*:?\s*(.+?)(?:\n|$)",
        r"\*\*exit\*\*:?\s*(.+?)(?:\n|$)",
        r"[-*]\s+\*\*Exit\*\*:?\s*(.+?)(?:\n|$)",
    ]
    for pattern in exit_patterns:
        for source in [text] + list(sections.values()):
            m = re.search(pattern, source, re.IGNORECASE)
            if m:
                exit_val = _clean_md(m.group(1).strip())
                exit_lower = exit_val.lower()
                if any(
                    kw in exit_lower
                    for kw in [
                        "trail",
                        "dynamic",
                        "move",
                        "close",
                        "cross",
                        "sell into strength",
                    ]
                ):
                    return exit_val[:250]
                if "fixed" in exit_lower or exit_lower.startswith("target_r="):
                    return "N_A"

    # Search text for trailing keywords in context
    trail_patterns = [
        r"(trail(?:ing)?\s+(?:the\s+)?(?:whole\s+)?position\s+(?:up|down)[^.]*)",
        r"(trail(?:ing)?\s+(?:exit|stop)[^.]*)",
        r"(dynamic(?:\s+trailing)?\s+(?:exit|stop)[^.]*)",
        r"(close\s*(?:closes\s*)?cross(?:ing|es)?\s*(?:below|above)\s+(?:the\s+)?(?:\d+\s*)?\w+\s*(?:EMA|MA|SMA|line)[^.]*)",
        r"(sell\s+into\s+strength[^.]*)",
    ]
    for pattern in trail_patterns:
        m = re.search(pattern, all_content, re.IGNORECASE)
        if m:
            return _clean_md(m.group(1).strip())[:250]

    return "N_A"

    # Check all sections for trailing keywords
    trail_keywords = [
        "trail",
        "dynamic.*exit",
        "dynamic.*stop",
        "moving.*stop",
        "close.*cross.*(?:below|above)",
        "sell into strength",
    ]
    for section_key, content in sections.items():
        content_lower = content.lower()
        for kw in trail_keywords:
            if re.search(kw, content_lower):
                # Extract the most relevant sentence
                for line in content.split("\n"):
                    if re.search(kw, line.lower()):
                        return line.strip("* -=")[:250]
                return content[:250]

    # Check rules section for exit with trailing
    rules = sections.get("rules", "")
    if rules:
        for line in rules.split("\n"):
            if re.search(r"\*\*Exit\*\*", line, re.IGNORECASE):
                exit_text = _first_bullet_value(rules, r"[Ee]xit")
                if exit_text:
                    if "fixed" not in exit_text.lower():
                        return exit_text[:250]

    return "N_A"


def extract_filters_used(text, sections):
    """Extract filters / regime conditions as comma-separated list."""
    filter_terms = []

    # 1. Explicit filter / gate sections
    filter_section = _get_section(
        sections,
        "filters",
        "filter",
        "conditions",
        "market_environment",
        "market_context",
        "regime",
        "entry_conditions",
    )
    if filter_section:
        terms = _extract_indicator_terms(filter_section)
        filter_terms.extend(terms)

    # 2. Entry bullet → extract condition indicators
    entry_val = _first_bullet_value(text, r"[Ee]ntr[yi]")
    if entry_val:
        terms = _extract_indicator_terms(entry_val)
        filter_terms.extend(terms)

    # 3. Search whole text for explicit filter language
    text_lower = text.lower()
    filter_markers = [
        "regime filter",
        "market filter",
        "trend filter",
        "only when",
        "requires",
        "only if",
        "must be above",
        "gate",
        "screener",
        "environmental",
        "precondition",
    ]
    for marker in filter_markers:
        if marker in text_lower:
            # Extract conceptual filter from context
            for line in text.split("\n"):
                if marker in line.lower():
                    clean = re.sub(r"[*#\-]", "", line).strip()[:120]
                    if clean and clean not in filter_terms:
                        filter_terms.append(clean)

    # 4. Input filters (emulated)
    # Check for "parameter" + condition patterns
    for line in text.split("\n"):
        m = re.search(
            r"(?:Close|Price|Volume|RSI|EMA|SMA|VWAP|ATR|MACD)\s*(?:[><]=?|is)\s*(?:above|below|greater|less)",
            line,
            re.IGNORECASE,
        )
        if m:
            clean = re.sub(r"[*#\-]", "", line).strip()[:120]
            if clean not in filter_terms:
                filter_terms.append(clean)

    # Deduplicate while preserving order-ish
    seen = set()
    unique = []
    for t in filter_terms:
        norm = t.lower()
        if norm not in seen:
            seen.add(norm)
            unique.append(t)

    if not unique:
        return "N_A"

    return ", ".join(unique[:6])  # keep reasonable size


def extract_strengths(text, sections):
    """Summarize strategy strengths in 1-2 lines."""
    # Try Style / Overview sections
    overview = _get_section(sections, "style", "overview", "description", "summary")
    if overview and len(overview) > 30:
        sentences = re.split(r"[.!?]\s+", overview)
        result = ". ".join(sentences[:2])
        cleaned = _clean_md(result)
        if len(cleaned) > 30:
            return cleaned[:300]

    # Try "The 3 setups" or similar list-style sections
    setup_section = _get_section(sections, "the_3_setups", "setup", "strategy")
    if setup_section and len(setup_section) > 30:
        # Take first setup description
        first_item = setup_section.split("\n")[0]
        cleaned = _clean_md(first_item)
        if len(cleaned) > 15:
            return cleaned[:300]

    # Take from preamble (text after # Title, before ##), skip metadata lines
    preamble = sections.get("_preamble", "")
    if preamble and len(preamble) > 15:
        lines = [
            l
            for l in preamble.split("\n")
            if not re.match(r"^[-*>#]\s+", l.strip()) and l.strip()
        ]
        if not lines:
            # Only had title + metadata → skip preamble entirely
            pass
        else:
            clean = _clean_md(" ".join(lines))
            if len(clean) > 15:
                return clean[:300]

    # Fallback: from entry description in the spec
    entry_val = _first_bullet_value(text, r"[Ee]ntr[yi]")
    if entry_val:
        return f"Entry: {_clean_md(entry_val)[:280]}"

    # Fallback: combine entry+stop+target from rules section
    rules = sections.get("rules", "")
    if rules:
        lines = []
        for line in rules.split("\n"):
            m = re.search(r"\*\*(?:Entry|Stop|Target|Exit)\*\*:?\s*(.+)", line)
            if m:
                lines.append(_clean_md(m.group(1)))
        if lines:
            return " | ".join(lines)[:300]

    # Last resort: title line (with Deterministic Spec suffix stripped)
    title = text.split("\n")[0].strip("# ").strip()
    title = re.sub(r"\s*[—\-]+\s*Deterministic\s+Spec\s*$", "", title).strip()
    return title[:300] if title else "N_A"


def extract_weaknesses(text, sections):
    """Summarize risks / limitations in 1-2 lines."""
    weak_section = _get_section(
        sections,
        "risks",
        "risks_for_backtesting",
        "ambiguities",
        "limitations",
        "weaknesses",
        "caveats",
        "readiness",
    )
    if weak_section:
        sentences = re.split(r"[.!?]\s+", weak_section)
        result = ". ".join(sentences[:2])
        if len(result) > 10:
            return result[:300]

    # Search for risk/caveat keywords in full text
    risk_lines = []
    for line in text.split("\n"):
        if re.search(
            r"\b(risk|caveat|limitation|ambiguous|unknown|not tested|unclear)\b",
            line,
            re.IGNORECASE,
        ):
            clean = re.sub(r"[*#\-]", "", line).strip()
            if clean and len(clean) > 10:
                risk_lines.append(clean)

    if risk_lines:
        return ". ".join(risk_lines[:2])[:300]

    # Check disposition for readiness signals
    for key in ["disposition", "rating", "readiness"]:
        if key in sections:
            content = sections[key]
            if any(
                kw in content.lower()
                for kw in ["needs", "review", "low", "medium", "ambiguous"]
            ):
                return content[:300]

    return "N_A"


def extract_all(text):
    """Extract all 4 fields from spec text."""
    sections = _parse_md_sections(text)
    return {
        "trailing_logic": extract_trailing_logic(text, sections),
        "filters_used": extract_filters_used(text, sections),
        "known_strengths": extract_strengths(text, sections),
        "known_weaknesses": extract_weaknesses(text, sections),
    }


def patch_producer_spec(spec_path, fields):
    """Update producer_spec.json in-place with extracted fields."""
    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False, "json_read_error"

    changed = False
    for key, value in fields.items():
        if value and value != data.get(key) and value != "N_A":
            data[key] = value
            changed = True
        elif key not in data:
            data[key] = value
            changed = True

    if changed:
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return True, "updated"
    return True, "unchanged"


def patch_candidate_metadata(meta_path, fields):
    """Append extracted fields to 01_candidate_metadata.yaml under A1 block."""
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False, "yaml_read_error"

    marker = "# --- A1 Extracted (auto) ---"
    if marker in content:
        prefix = content[: content.index(marker)]
    else:
        prefix = content.rstrip() + "\n\n"

    block_lines = [marker]
    for key, value in fields.items():
        # Clean any remaining markdown from values
        clean_val = _clean_md(value) if value and isinstance(value, str) else value

        if not clean_val or clean_val in ("N_A", "None", ""):
            block_lines.append(f"{key}: N_A")
        elif "\n" in clean_val:
            block_lines.append(f"{key}: |")
            for vline in clean_val.replace("\r", "").split("\n"):
                block_lines.append(f"  {vline.strip()}")
        else:
            # Quote if it contains YAML special chars or markdown artifacts
            needs_quote = any(
                c in clean_val
                for c in [
                    ": ",
                    " #",
                    "{",
                    "}",
                    "[",
                    "]",
                    ",",
                    "&",
                    "*",
                    "?",
                    "|",
                    ">",
                    "!",
                    "%",
                    "@",
                    "`",
                    '"',
                    "'",
                ]
            )
            if needs_quote:
                # YAML double-quote escaping: backslash → \\, quote → ""
                # Also avoid leading "- " which YAML treats as list item
                safe = clean_val.replace("\\", "\\\\").replace('"', '""')
                block_lines.append(f'{key}: "{safe}"')
            elif clean_val and clean_val[0] in ("-", "*", "&", "!"):
                block_lines.append(f'{key}: "{clean_val}"')
            else:
                block_lines.append(f"{key}: {clean_val}")

    new_content = prefix + "\n".join(block_lines) + "\n"

    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True, "updated"


def main():
    strategies_dir = STRATEGIES_DIR
    if not strategies_dir.exists():
        print(f"ERROR: strategies dir not found: {strategies_dir}")
        sys.exit(1)

    stats = {
        "total_dirs": 0,
        "with_spec": 0,
        "skipped_no_spec": 0,
        "producer_spec_updated": 0,
        "candidate_meta_updated": 0,
        "errors": 0,
        "details": [],
    }

    for entry in sorted(strategies_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not entry.name.startswith("STG"):
            continue

        stats["total_dirs"] += 1
        stg_name = entry.name
        spec_path = entry / "07_deterministic_spec.md"

        if not spec_path.exists():
            stats["skipped_no_spec"] += 1
            print(f"SKIP   {stg_name} — no 07_deterministic_spec.md")
            continue

        stats["with_spec"] += 1

        try:
            with open(spec_path, "r", encoding="utf-8") as f:
                spec_text = f.read()
        except Exception as e:
            stats["errors"] += 1
            print(f"ERROR  {stg_name} — read failed: {e}")
            continue

        fields = extract_all(spec_text)

        # Determine target file
        producer_path = entry / "producer_spec.json"
        meta_path = entry / "01_candidate_metadata.yaml"

        if producer_path.exists():
            ok, status = patch_producer_spec(producer_path, fields)
            if ok and status == "updated":
                stats["producer_spec_updated"] += 1
                print(f"OK     {stg_name} — producer_spec.json updated")
            elif ok:
                print(f"OK     {stg_name} — producer_spec.json unchanged")
            else:
                stats["errors"] += 1
                print(f"ERROR  {stg_name} — producer_spec.json: {status}")
        elif meta_path.exists():
            ok, status = patch_candidate_metadata(meta_path, fields)
            if ok:
                stats["candidate_meta_updated"] += 1
                print(f"OK     {stg_name} — 01_candidate_metadata.yaml updated")
            else:
                stats["errors"] += 1
                print(f"ERROR  {stg_name} — 01_candidate_metadata.yaml: {status}")
        else:
            print(
                f"SKIP   {stg_name} — no producer_spec.json or 01_candidate_metadata.yaml"
            )

    print(f"\n{'=' * 60}")
    print(f"Total dirs scanned:    {stats['total_dirs']}")
    print(f"With spec file:        {stats['with_spec']}")
    print(f"Skipped (no spec):     {stats['skipped_no_spec']}")
    print(f"producer_spec updated: {stats['producer_spec_updated']}")
    print(f"candidate_meta updated:{stats['candidate_meta_updated']}")
    print(f"Errors:                {stats['errors']}")
    return stats


if __name__ == "__main__":
    main()
