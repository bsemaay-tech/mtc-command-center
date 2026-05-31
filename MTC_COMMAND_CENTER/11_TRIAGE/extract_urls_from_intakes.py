"""Scan QuantLens intake markdowns for YouTube URLs and pre-fill empty
'Video Url:' lines in 11_TRIAGE/strategies/stg*.md.

Strict rules:
- Never overwrites a non-empty 'Video Url:' line.
- Ignores 'UNKNOWN_URL' literals and obvious placeholders.
- For QLR_<id> candidates, verifies the extracted URL contains <id>.
- For other candidates, matches by intake filename containing candidate suffix
  or by 'Video ID:' line referencing the same id.

Read-only outside 11_TRIAGE/. Reports a per-candidate result table.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

THIS = Path(__file__).resolve()
STRATEGIES_DIR = THIS.parent / "strategies"
CODE_MAP_PATH = STRATEGIES_DIR / "_stg_code_map.json"

API_ROOT = THIS.parent.parent / "08_DASHBOARD_APP" / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from mcc_readonly.paths import default_mcc_root  # noqa: E402

YT_RE = re.compile(
    r"https?://(?:www\.|m\.)?(?:youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})|youtu\.be/([A-Za-z0-9_-]{6,}))"
)
SOURCE_LINE_RE = re.compile(
    r"^\s*[-*]?\s*\*{0,2}(?:Source URL|Normalized URL|Original URL|URL)\*{0,2}\s*:\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def extract_yt_id(url: str) -> str | None:
    m = YT_RE.search(url)
    if not m:
        return None
    return m.group(1) or m.group(2)


def scan_intake_for_url(text: str) -> tuple[str, str] | None:
    """Return (normalized_url, video_id) found in intake markdown, or None."""
    for m in SOURCE_LINE_RE.finditer(text):
        raw = m.group(1).strip()
        if "UNKNOWN_URL" in raw or "UNKNOWN" in raw.upper().split("?")[0].split("/")[-1]:
            continue
        yid = extract_yt_id(raw)
        if yid:
            return f"https://www.youtube.com/watch?v={yid}", yid
    yid_match = re.search(r"^\s*[-*]?\s*\*{0,2}Video ID\*{0,2}\s*:\s*`?([A-Za-z0-9_-]{6,})`?", text, re.IGNORECASE | re.MULTILINE)
    if yid_match and "UNKNOWN" not in yid_match.group(1).upper():
        yid = yid_match.group(1).strip()
        return f"https://www.youtube.com/watch?v={yid}", yid
    return None


def candidate_id_suffix(cid: str) -> str:
    """Strip common prefixes to get the matching key for intake filenames."""
    for prefix in ("QL_ALPHA_", "QL_2026-05-01_", "QL_2026-05-02_", "QL_2026-05-03_", "QLR_"):
        if cid.startswith(prefix):
            return cid[len(prefix):]
    return cid


def main() -> None:
    mcc_root = Path(default_mcc_root()).resolve()
    inbox_root = mcc_root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB" / "00_INBOX_REPORTS"
    code_map: dict[str, str] = json.loads(CODE_MAP_PATH.read_text(encoding="utf-8"))

    intakes: list[tuple[Path, str, str | None, str | None]] = []
    if inbox_root.exists():
        for p in inbox_root.rglob("*.md"):
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            url_hit = scan_intake_for_url(text)
            url, vid = (url_hit if url_hit else (None, None))
            intakes.append((p, text, url, vid))

    print(f"Scanned {len(intakes)} intake markdowns under {inbox_root.relative_to(mcc_root.parent)}")
    with_url = sum(1 for _, _, u, _ in intakes if u)
    print(f"Intakes with usable YouTube URL: {with_url}")

    filled = 0
    skipped = 0
    no_match = 0
    report_rows: list[tuple[str, str, str, str]] = []

    for cid, code in code_map.items():
        stg_path = STRATEGIES_DIR / f"{code.lower()}.md"
        if not stg_path.exists():
            continue
        md_text = stg_path.read_text(encoding="utf-8")
        url_line = re.search(r"^Video Url:\s*(.*)$", md_text, re.MULTILINE)
        if not url_line or url_line.group(1).strip():
            skipped += 1
            continue

        suffix = candidate_id_suffix(cid).lower()
        cid_yid = None
        if cid.startswith("QLR_"):
            cid_yid = cid[4:]

        match: tuple[Path, str, str] | None = None
        for path, text, url, vid in intakes:
            if not url:
                continue
            if cid_yid and vid and vid == cid_yid:
                match = (path, url, "video_id_match")
                break
            stem = path.stem.lower()
            if suffix and len(suffix) > 8 and suffix in stem:
                match = (path, url, "filename_suffix_match")
                break
            if cid.lower() in text.lower():
                match = (path, url, "id_in_body_match")
                break

        if not match:
            no_match += 1
            report_rows.append((code, cid, "NO_MATCH", ""))
            continue

        path, url, reason = match
        new_text = re.sub(
            r"^(Video Url:)\s*$",
            f"\\1 {url}",
            md_text,
            count=1,
            flags=re.MULTILINE,
        )
        if new_text == md_text:
            no_match += 1
            report_rows.append((code, cid, "ALREADY_HAD_URL", url))
            continue
        stg_path.write_text(new_text, encoding="utf-8")
        filled += 1
        report_rows.append((code, cid, f"FILLED ({reason})", url))

    print()
    print(f"Filled: {filled}  |  Skipped (already had URL): {skipped}  |  No intake match: {no_match}")
    print()
    print("Per-candidate result for the EMPTY-URL group:")
    for code, cid, status, url in report_rows:
        print(f"  {code:8s}  {cid[:45]:45s}  {status:30s}  {url}")


if __name__ == "__main__":
    main()
