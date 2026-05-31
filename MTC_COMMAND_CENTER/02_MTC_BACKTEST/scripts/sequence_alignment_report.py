from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.parity.compare_tv_trades import clip_overlap, load_py_trades, load_tv_trades
from src.parity.sequence_alignment import greedy_prefix_alignment


def render_markdown(
    *,
    tv_path: Path,
    py_path: Path,
    mode: str,
    tolerance_min: int,
    alignment: dict,
) -> str:
    lines = [
        "# Sequence Alignment Report",
        "",
        f"- tv_path: `{tv_path}`",
        f"- py_path: `{py_path}`",
        f"- mode: `{mode}`",
        f"- tolerance_min: `{tolerance_min}`",
        f"- matched_prefix_len: `{alignment['matched_prefix_len']}`",
        f"- tv_total: `{alignment['tv_total']}`",
        f"- py_total: `{alignment['py_total']}`",
        "",
        "## Events",
    ]
    for event in alignment["events"][:25]:
        lines.append(
            f"- tv_seq `{event['tv_seq']}` <-> py_seq `{event['py_seq']}` via `{event['mode']}`"
        )

    lines.extend(["", "## Break"])
    lines.append(f"- break_tv_seq: `{alignment['break_tv_seq']}`")
    lines.append(f"- break_py_seq: `{alignment['break_py_seq']}`")
    lines.append(f"- break_tv: `{alignment['break_tv']}`")
    lines.append(f"- break_py: `{alignment['break_py']}`")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnostic sequence alignment report for TV vs Python trades.")
    parser.add_argument("--tv", required=True)
    parser.add_argument("--py", required=True)
    parser.add_argument("--tv-tz", default="Europe/London")
    parser.add_argument("--mode", choices=["raw", "clip"], default="clip")
    parser.add_argument("--tolerance-min", type=int, default=15)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    tv_path = Path(args.tv).resolve()
    py_path = Path(args.py).resolve()

    tv = load_tv_trades(tv_path, tv_tz=args.tv_tz)
    py = load_py_trades(py_path)
    if args.mode == "clip":
        tv, py = clip_overlap(tv, py)

    alignment = greedy_prefix_alignment(tv, py, tolerance_min=args.tolerance_min)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(alignment, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(
        render_markdown(
            tv_path=tv_path,
            py_path=py_path,
            mode=args.mode,
            tolerance_min=args.tolerance_min,
            alignment=alignment,
        ),
        encoding="utf-8",
    )

    print(f"JSON: {out_json}")
    print(f"Markdown: {out_md}")


if __name__ == "__main__":
    main()
