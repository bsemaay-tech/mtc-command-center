#!/usr/bin/env python3
"""Convert binary docs (PDF/DOCX/PPTX/XLSX) to LLM-friendly Markdown via MarkItDown.

Companion to ``route_user_intake.py``. That router only *moves* files; agents
still cannot cheaply read a moved PDF/XLSX. This tool produces a sibling ``.md``
so the content becomes low-token, high-quality text for Claude/Codex/DeepSeek.

It is fully self-contained: MarkItDown needs Python 3.10-3.13, but the repo's
system Python may be newer (3.14+), so this wrapper keeps its own isolated venv
under ``03_QUANTLENS/tools/.venvs/markitdown`` (git-ignored) and bootstraps it on
first run using a 3.10-3.13 interpreter found via the ``py`` launcher.

Nothing is ever deleted. Source files are read-only; only new ``.md`` is written.
Default is a DRY RUN (lists what would convert). Pass ``--apply`` to write.

Usage:
    # dry-run over 00_INBOX/USER_INTAKE (default target)
    python 03_QUANTLENS/tools/markitdown_ingest.py
    # convert everything convertible in the intake dir
    python 03_QUANTLENS/tools/markitdown_ingest.py --apply
    # convert specific files / a dir, write .md next to each source
    python 03_QUANTLENS/tools/markitdown_ingest.py path/to/report.xlsx --apply
    # write all .md into one output folder instead of beside sources
    python 03_QUANTLENS/tools/markitdown_ingest.py somedir --apply --out C:/tmp/md
    # just (re)build the venv and exit
    python 03_QUANTLENS/tools/markitdown_ingest.py --bootstrap
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
QUANTLENS_ROOT = TOOLS_DIR.parent
MCC_ROOT = QUANTLENS_ROOT.parent
INTAKE_DIR = MCC_ROOT / "00_INBOX" / "USER_INTAKE"

VENV_DIR = TOOLS_DIR / ".venvs" / "markitdown"
VENV_PY = VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
PIP_SPEC = "markitdown[pdf,docx,pptx,xlsx]"

# Extensions MarkItDown handles well for our use; sources we convert.
CONVERT_EXT = {".pdf", ".docx", ".pptx", ".xlsx", ".xls"}


def _find_compatible_python() -> str:
    """Return a path/launcher invocation for a Python 3.10-3.13 interpreter."""
    # Prefer the Windows 'py' launcher with an explicit supported minor.
    for minor in ("3.13", "3.12", "3.11", "3.10"):
        try:
            out = subprocess.run(
                ["py", f"-{minor}", "-c", "import sys;print(sys.executable)"],
                capture_output=True, text=True, timeout=30,
            )
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip()
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    # Fall back to the running interpreter only if it is in range.
    if (3, 10) <= sys.version_info[:2] <= (3, 13):
        return sys.executable
    raise SystemExit(
        "No Python 3.10-3.13 found. MarkItDown does not support this repo's "
        f"system Python {sys.version_info.major}.{sys.version_info.minor}. "
        "Install 3.13 (e.g. `py -3.13`) and re-run."
    )


def ensure_venv(force: bool = False) -> Path:
    if VENV_PY.exists() and not force:
        return VENV_PY
    base = _find_compatible_python()
    print(f"[bootstrap] creating venv at {VENV_DIR} using {base}")
    VENV_DIR.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([base, "-m", "venv", str(VENV_DIR)], check=True)
    print(f"[bootstrap] installing {PIP_SPEC} (one-time, ~1-2 min)")
    subprocess.run([str(VENV_PY), "-m", "pip", "install", "--quiet",
                    "--upgrade", "pip"], check=True)
    subprocess.run([str(VENV_PY), "-m", "pip", "install", PIP_SPEC], check=True)
    print("[bootstrap] done")
    return VENV_PY


def _collect(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_dir():
            out.extend(sorted(f for f in p.rglob("*")
                              if f.is_file() and f.suffix.lower() in CONVERT_EXT))
        elif p.is_file() and p.suffix.lower() in CONVERT_EXT:
            out.append(p)
    return out


def convert(py: Path, src: Path, out_md: Path) -> bool:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    res = subprocess.run([str(py), "-m", "markitdown", str(src), "-o", str(out_md)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAIL   {src.name}: {res.stderr.strip()[:200]}")
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="files/dirs (default: USER_INTAKE)")
    ap.add_argument("--apply", action="store_true", help="write .md (default: dry-run)")
    ap.add_argument("--out", type=Path, help="output dir (default: beside each source)")
    ap.add_argument("--bootstrap", action="store_true", help="(re)build venv and exit")
    args = ap.parse_args(argv)

    if args.bootstrap:
        ensure_venv(force=True)
        return 0

    targets = [Path(p) for p in args.paths] if args.paths else [INTAKE_DIR]
    missing = [p for p in targets if not p.exists()]
    if missing:
        for p in missing:
            print(f"not found: {p}")
        return 1

    files = _collect(targets)
    if not files:
        print("Nothing convertible (.pdf/.docx/.pptx/.xlsx/.xls) found.")
        return 0

    if not args.apply:
        print("DRY RUN — would convert:")
        for f in files:
            dest = (args.out / (f.stem + ".md")) if args.out else f.with_suffix(".md")
            print(f"  {f}  ->  {dest}")
        print(f"\n{len(files)} file(s). Re-run with --apply to write.")
        return 0

    py = ensure_venv()
    ok = 0
    for f in files:
        dest = (args.out / (f.stem + ".md")) if args.out else f.with_suffix(".md")
        if convert(py, f, dest):
            ok += 1
            print(f"OK     {f.name}  ->  {dest}")
    print(f"\n{ok}/{len(files)} converted.")
    return 0 if ok == len(files) else 2


if __name__ == "__main__":
    raise SystemExit(main())
