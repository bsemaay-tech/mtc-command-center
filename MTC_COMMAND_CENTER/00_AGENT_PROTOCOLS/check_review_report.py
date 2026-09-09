"""Gate a Section-16 review report before its verdicts are allowed near the assembler.

Attempt 7 reached PASS while citing a file absent from the reviewer's sandbox and line
numbers three times beyond another file's length. This checks, mechanically:

  1. a JSON verdict block exists and parses;
  2. no item is CHANGED and overall is not REQUIRES_FRESH_REVIEW (either refuses by design);
  3. every repository-looking path the prose cites resolves INSIDE the packet;
  4. every cited "path:line" actually has that many lines in the packet copy.

Exit 0 only if all four hold. Anything else prints why and exits non-zero.

Usage:  check_review_report.py [--packet <packet dir>] <report.md>
The packet directory defaults to the re-seal #30 packet below, so behaviour is
unchanged for that packet; --packet makes it reusable for later reviews.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PACKET = Path(r"C:\LAB\Tradingview_LAB_CLEAN\_gemini_packets_20260830\P012_R30_20260908")
STRIPPED = "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/"


def extract_verdicts(text: str):
    """Take the last fenced JSON object that has an 'items' key."""
    best = None
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "items" in obj:
            best = obj
    return best


def packet_candidates(rel: str):
    """Every packet location a cited repo-relative path could legitimately live at."""
    rel = rel.lstrip("/")
    short = rel[len(STRIPPED):] if rel.startswith(STRIPPED) else rel
    out = []
    for base in ("CAND", "PRIOR", "KERNEL_BOOKKEEPING", ""):
        for r in {rel, short}:
            out.append(PACKET / base / r if base else PACKET / r)
            out.append(PACKET / base / Path(r).name if base else PACKET / Path(r).name)
    return out


def main() -> int:
    global PACKET
    args = list(sys.argv[1:])
    if "--packet" in args:
        i = args.index("--packet")
        PACKET = Path(args[i + 1])
        del args[i:i + 2]
    if not args:
        print("usage: check_review_report.py [--packet <dir>] <report.md>")
        return 2
    report = Path(args[0])
    print(f"packet = {PACKET}")
    text = report.read_text(encoding="utf-8", errors="replace")
    problems = []

    verdicts = extract_verdicts(text)
    if verdicts is None:
        print("FAIL: no parseable JSON verdict block with an 'items' key")
        return 2

    items = verdicts.get("items", {})
    changed = [k for k, v in items.items() if v.get("disposition") != "UNCHANGED"]
    overall = verdicts.get("overall", "")
    print(f"items={len(items)} changed={changed or 'none'} overall={overall}")
    if changed:
        problems.append(f"item(s) {changed} are not UNCHANGED -> assembler refuses by design")
    if overall != "SUCCESSOR_REVIEW_CAN_CARRY_FORWARD":
        problems.append(f"overall is {overall!r} -> a full fresh review is required")

    # --- citations -------------------------------------------------------------------
    cited = set(re.findall(r"[\w./\\-]*(?:MTC_COMMAND_CENTER|mtc_v2)[\w./\\-]*\.(?:py|json|md|sha256)", text))
    outside, missing = [], []
    for c in sorted(cited):
        rel = c.replace("\\", "/")
        rel = re.sub(r"^.*?(MTC_COMMAND_CENTER|mtc_v2)", r"\1", rel)
        if not any(p.exists() for p in packet_candidates(rel)):
            (outside if "MTC_COMMAND_CENTER" in rel or "mtc_v2" in rel else missing).append(c)
    if outside:
        problems.append(f"{len(outside)} cited path(s) do not resolve inside the packet")
        for c in outside[:12]:
            print(f"  UNRESOLVED CITATION: {c}")

    # --- did it actually read the packet? ---------------------------------------------
    # Attempt 7 cited line numbers that were correct -- because they came from the diff's
    # hunk headers, not from reading any file. So "the numbers are right" proves nothing.
    # What distinguishes a real read is citing the packet trees the bytes actually live in.
    packet_refs = len(re.findall(r"\b(?:CAND|PRIOR|KERNEL_BOOKKEEPING)/", text))
    print(f"packet-tree citations (CAND/ PRIOR/ KERNEL_BOOKKEEPING/) = {packet_refs}")
    if packet_refs == 0:
        problems.append("report never cites CAND/, PRIOR/ or KERNEL_BOOKKEEPING/ -- "
                        "no evidence it read the mirrored bytes rather than the diff alone")

    # Absolute citations into the live repo are invalid by construction: that checkout is
    # the wrong version, and TASK.md forbids reading it.
    repo_abs = re.findall(r"file:///C:/LAB/Tradingview_LAB_CLEAN/(?!_gemini_packets)[\w./#-]+", text)
    if repo_abs:
        problems.append(f"{len(repo_abs)} citation(s) point at the live (stale) checkout "
                        "instead of the packet")
        for c in sorted(set(repo_abs))[:8]:
            print(f"  STALE-CHECKOUT CITATION: {c}")

    # --- path:line claims ------------------------------------------------------------
    for m in re.finditer(r"([\w./\\-]*(?:MTC_COMMAND_CENTER|mtc_v2)[\w./\\-]*\.py)[#:]L?(\d+)", text):
        rel = re.sub(r"^.*?(MTC_COMMAND_CENTER|mtc_v2)", r"\1", m.group(1).replace("\\", "/"))
        line = int(m.group(2))
        for p in packet_candidates(rel):
            if p.exists():
                n = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                if line > n:
                    problems.append(f"cites {rel}:{line} but the packet copy has {n} lines")
                    print(f"  BAD LINE CITATION: {rel}:{line} (file has {n} lines)")
                break

    print()
    if problems:
        print("REPORT REJECTED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("REPORT ACCEPTED: verdicts are all UNCHANGED, overall carries forward, "
          "every cited path resolves inside the packet, and no line citation exceeds its file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
