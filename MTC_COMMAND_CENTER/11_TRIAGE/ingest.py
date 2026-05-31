"""Ingest manual backfill from 11_TRIAGE/strategies/*.md into QuantLens canonical paths.

Reads each strategies/stgNNN.md and extracts:
  - 'Video Url:' line              -> manual-backfill quantlens_source_map.csv row
  - '## Transcript' body           -> Transcrips/<safe_name>.md (if candidate had no transcript)
  - '## Alternative Source N'      -> Transcrips/<safe_name>_altN.md (always treated as new)
  - '## Notes' block               -> kept inside 11_TRIAGE only, never copied

Defaults to --dry-run. Pass --apply to actually write.
Re-runs are safe: URLs/transcripts already present in canonical locations are
skipped, and a state file (_ingested_state.json) records what was ingested so
subsequent runs only act on deltas.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

THIS = Path(__file__).resolve()
STRATEGIES_DIR = THIS.parent / "strategies"
CODE_MAP_PATH = STRATEGIES_DIR / "_stg_code_map.json"
STATE_PATH = STRATEGIES_DIR / "_ingested_state.json"
EMBEDDED_TRANSCRIPT_MIN_SIZE = 5_000
EMBEDDED_TRANSCRIPT_MIN_TIMESTAMPS = 30

API_ROOT = THIS.parent.parent / "08_DASHBOARD_APP" / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from mcc_readonly.audit_reader import build_candidate_audit  # noqa: E402
from mcc_readonly.paths import default_mcc_root  # noqa: E402

CSV_HEADERS = [
    "candidate_id",
    "source_url",
    "source_title",
    "transcript_path",
    "intake_path",
    "corrected_intake_path",
    "source_quality",
    "rule_clarity_score",
    "mechanical_testability_score",
    "trader_credibility_context_score",
    "data_availability_score",
    "expected_edge_plausibility_score",
    "MTC_compatibility_score",
    "visual_review_priority",
    "final_priority_score",
    "classification",
    "next_action",
    "do_not_test_yet_reason",
]


def safe_filename(name: str, max_len: int = 80) -> str:
    cleaned = re.sub(r"[^\w\- ]+", "", name).strip().replace(" ", "_")
    return (cleaned or "untitled")[:max_len]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def source_map_transcript_links(qlab_root: Path) -> set[tuple[str, str]]:
    links: set[tuple[str, str]] = set()
    for path in (qlab_root / "12_LLM_WIKI").glob("**/quantlens_source_map.csv"):
        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    cid = (row.get("candidate_id") or "").strip()
                    transcript_path = (row.get("transcript_path") or "").strip()
                    if cid and transcript_path:
                        links.add((cid, transcript_path))
        except OSError:
            continue
    return links


def source_map_row(cid: str, parsed: dict, audit_row: dict, transcript_path: str = "") -> dict:
    return {
        "candidate_id": cid,
        "source_url": parsed["url"] or audit_row.get("source_url") or "",
        "source_title": parsed["title"],
        "transcript_path": transcript_path,
        "intake_path": "",
        "corrected_intake_path": "",
        "source_quality": "MANUAL_BACKFILL",
        "rule_clarity_score": "",
        "mechanical_testability_score": "",
        "trader_credibility_context_score": "",
        "data_availability_score": "",
        "expected_edge_plausibility_score": "",
        "MTC_compatibility_score": "",
        "visual_review_priority": "",
        "final_priority_score": "",
        "classification": "MANUAL_BACKFILL_PENDING_REVIEW",
        "next_action": "RE_AUDIT_AFTER_INGEST",
        "do_not_test_yet_reason": "",
    }


def embedded_transcript_body(path: Path, text: str) -> str:
    """Detect pasted transcripts that missed the explicit section heading."""
    if path.stat().st_size <= EMBEDDED_TRANSCRIPT_MIN_SIZE:
        return ""
    if re.search(r"^##\s+Transcript\s*$", text, re.MULTILINE | re.IGNORECASE):
        return ""
    if len(re.findall(r"\d+:\d+", text)) <= EMBEDDED_TRANSCRIPT_MIN_TIMESTAMPS:
        return ""

    url_match = re.search(r"^Video Url:\s*.*?$", text, re.MULTILINE)
    if not url_match:
        return ""
    body_start = url_match.end()
    next_heading = re.search(r"^##\s+", text[body_start:], re.MULTILINE)
    body_end = body_start + next_heading.start() if next_heading else len(text)
    return text[body_start:body_end].strip()


def parse_stg_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    header_match = re.search(r"^#\s+(\S+)\s+—\s+(.+?)\s*$", text, re.MULTILINE)
    stg_code = header_match.group(1) if header_match else path.stem
    candidate_id = header_match.group(2).strip() if header_match else ""
    name_match = re.search(r"^Video name:\s*(.*?)\s*$", text, re.MULTILINE)
    title = name_match.group(1).strip() if name_match else ""
    url_match = re.search(r"^Video Url:\s*(.*?)\s*$", text, re.MULTILINE)
    url = url_match.group(1).strip() if url_match else ""

    sections: list[tuple[str, str]] = []
    for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE):
        heading = m.group(1).strip()
        body_start = m.end()
        next_m = re.search(r"^##\s+", text[body_start:], re.MULTILINE)
        body_end = body_start + next_m.start() if next_m else len(text)
        body = text[body_start:body_end].strip()
        sections.append((heading, body))

    transcript_main = None
    alternatives: list[tuple[str, str, str]] = []  # (label, url, body)
    notes = None
    for heading, body in sections:
        h_lower = heading.lower()
        if h_lower == "transcript":
            transcript_main = body
        elif h_lower.startswith("alternative source"):
            alt_url_m = re.search(r"^Video Url:\s*(.*?)\s*$", body, re.MULTILINE)
            alt_body_m = re.search(r"^Transcript:\s*(.*)", body, re.MULTILINE | re.DOTALL)
            alt_url = alt_url_m.group(1).strip() if alt_url_m else ""
            alt_body = (alt_body_m.group(1) if alt_body_m else body).strip()
            alternatives.append((heading, alt_url, alt_body))
        elif h_lower == "notes":
            notes = body
    if not transcript_main:
        transcript_main = embedded_transcript_body(path, text)
    return {
        "path": path,
        "stg_code": stg_code,
        "candidate_id": candidate_id,
        "title": title,
        "url": url,
        "transcript_main": transcript_main or "",
        "alternatives": alternatives,
        "notes": notes,
    }


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def build_audit_lookup(audit: dict) -> dict[str, dict]:
    return {row.get("id"): row for row in (audit.get("rows", []) or []) if row.get("id")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes; default is dry-run.")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date bucket for manual_backfill CSV (default: today)",
    )
    args = parser.parse_args()

    mcc_root = Path(default_mcc_root()).resolve()
    tpl_root = mcc_root.parent / "01_MASTER TEMPLATE_V2"
    qlab_root = tpl_root / "06_QUANTLENS_LAB"
    transcripts_dir = qlab_root / "00_INBOX_REPORTS" / "Transcrips"
    backfill_dir = qlab_root / "12_LLM_WIKI" / "manual_backfill" / args.date
    backfill_csv = backfill_dir / "quantlens_source_map.csv"

    audit = build_candidate_audit()
    by_id = build_audit_lookup(audit)
    state = load_state()

    new_csv_rows: list[dict] = []
    new_csv_keys: set[tuple[str, str]] = set()
    new_transcripts: list[tuple[Path, str, str]] = []
    skipped_no_change: list[str] = []
    warnings_list: list[str] = []
    notes_only: list[str] = []
    existing_transcript_links = source_map_transcript_links(qlab_root)

    stg_files = sorted(STRATEGIES_DIR.glob("stg*.md"))
    for stg_path in stg_files:
        parsed = parse_stg_md(stg_path)
        cid = parsed["candidate_id"]
        if not cid:
            warnings_list.append(f"{stg_path.name}: no candidate_id header, skipped")
            continue
        audit_row = by_id.get(cid) or {}
        stg_state = state.get(cid, {})

        # URL ingestion
        if parsed["url"]:
            if not audit_row.get("has_source_url"):
                already = stg_state.get("url") == parsed["url"]
                if not already:
                    new_csv_rows.append(source_map_row(cid, parsed, audit_row))
                    stg_state["url"] = parsed["url"]
            elif audit_row.get("source_url") and parsed["url"] != audit_row.get("source_url"):
                warnings_list.append(
                    f"{stg_path.name}: stg URL ({parsed['url']}) differs from canonical ({audit_row.get('source_url')}); ignored"
                )

        # Main transcript ingestion (only if candidate had none in canonical)
        if parsed["transcript_main"] and not audit_row.get("has_transcript"):
            content_sha = sha256_text(parsed["transcript_main"])
            target_name = safe_filename(parsed["title"] or parsed["stg_code"]) + ".md"
            target = transcripts_dir / target_name
            rel_target = target.relative_to(qlab_root)
            rel_transcript = str(rel_target).replace("/", "\\")
            link_key = (cid, rel_transcript)
            if stg_state.get("transcript_main_sha") != content_sha:
                if not target.exists():
                    new_transcripts.append((target, parsed["transcript_main"], cid))
                stg_state["transcript_main_sha"] = content_sha
            # Annotate the CSV row's transcript_path if we queued or need a row for this candidate.
            for r in new_csv_rows:
                if r["candidate_id"] == cid:
                    r["transcript_path"] = rel_transcript
            if link_key not in existing_transcript_links and link_key not in new_csv_keys:
                if not any(r["candidate_id"] == cid and r.get("transcript_path") == rel_transcript for r in new_csv_rows):
                    new_csv_rows.append(source_map_row(cid, parsed, audit_row, rel_transcript))
                new_csv_keys.add(link_key)

        # Alternative sources are always additive
        for i, (label, alt_url, alt_body) in enumerate(parsed["alternatives"], start=1):
            if not alt_body:
                continue
            sha = sha256_text(alt_body + "\n" + alt_url)
            stg_alt = stg_state.setdefault("alternatives", {})
            if stg_alt.get(label) == sha:
                continue
            target_name = safe_filename(f"{parsed['title']}_alt{i}") + ".md"
            target = transcripts_dir / target_name
            if target.exists():
                target_name = safe_filename(f"{parsed['title']}_alt{i}_{parsed['stg_code']}") + ".md"
                target = transcripts_dir / target_name
            new_transcripts.append((target, alt_body, cid))
            stg_alt[label] = sha
            if alt_url:
                warnings_list.append(
                    f"{stg_path.name}: alt source '{label}' URL ({alt_url}) not added to source map (alt-only); add manually if you want it discoverable."
                )

        if parsed["notes"]:
            notes_only.append(f"{stg_path.name}: {len(parsed['notes'])} char note kept in triage only")

        if not any([parsed["url"], parsed["transcript_main"], parsed["alternatives"]]) or (
            parsed["url"] == stg_state.get("url")
            and parsed["transcript_main"] and sha256_text(parsed["transcript_main"]) == stg_state.get("transcript_main_sha")
        ):
            skipped_no_change.append(stg_path.name)

        state[cid] = stg_state

    print(f"=== Ingest plan (date bucket: {args.date}) ===")
    print(f"  New URL rows for source_map: {len(new_csv_rows)}")
    print(f"  New transcript files:        {len(new_transcripts)}")
    print(f"  Warnings:                    {len(warnings_list)}")
    print(f"  Notes (triage-only):         {len(notes_only)}")
    if warnings_list:
        print()
        for w in warnings_list[:10]:
            print(f"  WARN  {w}")
        if len(warnings_list) > 10:
            print(f"  ... +{len(warnings_list) - 10} more warnings")
    if new_csv_rows:
        print()
        print(f"  Would write -> {backfill_csv}")
        for r in new_csv_rows[:5]:
            print(f"    + {r['candidate_id']}  {r['source_url']}")
        if len(new_csv_rows) > 5:
            print(f"    ... +{len(new_csv_rows) - 5} more")
    if new_transcripts:
        print()
        for t, _body, cid in new_transcripts[:5]:
            print(f"    + transcript {t.relative_to(qlab_root)} (for {cid})")
        if len(new_transcripts) > 5:
            print(f"    ... +{len(new_transcripts) - 5} more")

    if not args.apply:
        print()
        print("DRY-RUN: pass --apply to write the changes above.")
        return 0

    if not new_csv_rows and not new_transcripts:
        print("Nothing to apply.")
        return 0

    if new_csv_rows:
        backfill_dir.mkdir(parents=True, exist_ok=True)
        write_header = not backfill_csv.exists()
        with backfill_csv.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            if write_header:
                writer.writeheader()
            for r in new_csv_rows:
                writer.writerow(r)
        print(f"WROTE  {len(new_csv_rows)} rows -> {backfill_csv}")

    if new_transcripts:
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        for target, body, _cid in new_transcripts:
            target.write_text(body.strip() + "\n", encoding="utf-8")
        print(f"WROTE  {len(new_transcripts)} transcript files -> {transcripts_dir}")

    save_state(state)
    print()
    print("Next: python -m mcc_readonly audit  (re-classify with new material)")
    print("      python 11_TRIAGE/generate_worklist.py  (refresh xlsx + .md set)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
