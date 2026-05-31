from __future__ import annotations

import argparse
import tarfile
from datetime import datetime, timezone
from pathlib import Path


def create_backup(output_dir: Path, include_paths: list[Path]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive = output_dir / f"mtc_backup_{stamp}.tar.gz"
    with tarfile.open(archive, "w:gz") as tf:
        for p in include_paths:
            if p.exists():
                tf.add(p, arcname=p.name)
    return archive


def restore_backup(archive: Path, dest_dir: Path) -> None:
    if not archive.exists():
        raise FileNotFoundError(f"Backup archive not found: {archive}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tf:
        tf.extractall(path=dest_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Backup/restore helper for MTC artifacts.")
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("backup")
    b.add_argument("--outdir", required=True)
    b.add_argument("--include", action="append", default=[], help="Path(s) to include")

    r = sub.add_parser("restore")
    r.add_argument("--archive", required=True)
    r.add_argument("--dest", required=True)

    args = parser.parse_args()
    if args.command == "backup":
        include_paths = [Path(p) for p in args.include]
        archive = create_backup(Path(args.outdir), include_paths)
        print(f"Backup created: {archive}")
    else:
        restore_backup(Path(args.archive), Path(args.dest))
        print(f"Backup restored to: {args.dest}")


if __name__ == "__main__":
    main()
