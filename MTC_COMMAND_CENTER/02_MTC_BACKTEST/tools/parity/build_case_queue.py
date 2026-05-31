from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from read_tracker import TrackerCase, read_tracker


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "01_MASTER TEMPLATE_V2" / "05_PARITY" / "_nightly"
QUEUE_PATH = OUTPUT_DIR / "case_queue.json"
STATE_PATH = OUTPUT_DIR / "state.json"


@dataclass(slots=True)
class QueueItem:
    case_no: str
    phase: str
    status: str
    folder: str
    export_file: str
    title: str
    description: str


def build_queue(cases: list[TrackerCase], resume: bool = True) -> list[QueueItem]:
    completed = set()
    if resume and STATE_PATH.exists():
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        completed = set(state.get("completed_cases", []))
    planned = [c for c in cases if c.status.upper() == "PLANNED" and c.case_no not in completed]
    planned.sort(key=lambda c: int(c.case_no.split("_")[1]))
    return [QueueItem(c.case_no, c.phase, c.status, c.folder, c.export_file, c.title, c.description) for c in planned]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    queue = build_queue(read_tracker(), resume=not args.no_resume)
    QUEUE_PATH.write_text(json.dumps([asdict(q) for q in queue], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"queued={len(queue)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
