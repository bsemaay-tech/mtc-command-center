#!/usr/bin/env python3
"""Cross-platform, stdlib-only port of ``generate_index.ps1``.

This mirrors the PowerShell generator's row format, header lines, cell
cleaning rules, date extraction, text-extension handling, heading/body
extraction, and unreadable-file fallback exactly, so the two tools produce
byte-identical ``INDEX.md`` output when pointed at the same tree. It exists
because ``generate_index.ps1`` requires PowerShell, which is unavailable on
Linux/CI, so this tool lets non-Windows environments (and CI) regenerate or
verify the index without it.

Two intentional differences from ``generate_index.ps1``:

1. File set. ``generate_index.ps1`` walks the filesystem with
   ``Get-ChildItem -Recurse`` and indexes every file present on disk. This
   tool instead indexes the git-tracked-or-trackable file set returned by
   ``git ls-files --cached --others --exclude-standard`` run inside
   ``--root`` (i.e. committed files plus untracked-but-not-ignored files,
   excluding anything ``.gitignore``-ignored). This keeps generated,
   ignored, and scratch files out of the index and gives a deterministic,
   git-defined file set instead of a machine-dependent directory listing.
2. Sort order. ``generate_index.ps1`` relies on PowerShell's
   ``Sort-Object FullName``, which performs a culture-aware .NET string
   comparison with no exact, portable Python equivalent. This tool instead
   sorts with an explicit key function, :func:`dotnet_word_sort_key`, that
   reproduces the same relative ordering (see its docstring) so results are
   byte-for-byte identical to the historical PowerShell-generated output.

Row format, header lines, encoding, and CLI behavior:

* Rows: ``| \\`<path>\\` | <date> | <topic> | <summary> |`` with the same
  header block as ``generate_index.ps1`` (title, notice line, table header,
  separator row).
* Output is written UTF-8 without a byte-order mark, with LF line endings
  and exactly one trailing newline.
* Cell cleaning: pipes are escaped as ``\\|``, runs of whitespace collapse
  to a single space, the result is trimmed, and it is truncated to a
  per-column limit (path 180, topic 120, summary 180) with a trailing
  ``...`` when truncated.
* Date extraction: the first ``YYYY-MM-DD``/``YYYY_MM_DD`` or ``YYYYMMDD``
  run (year starting with ``20``) found in the file *name* becomes the date
  cell; otherwise the date cell is ``-``.
* Text extensions (``.md .txt .json .ps1 .py .sh .yaml .yml``) are opened
  and scanned for the first ATX heading (``#`` through ``######`` followed
  by whitespace and a non-whitespace character) to use as the topic, and the
  first non-blank line that is not a heading/blockquote/table/fence/rule to
  use as the summary. A read failure of any kind falls back to a summary of
  ``Unreadable during index generation: <ExceptionType>``.
* Dotfiles (a name starting with ``.`` that contains exactly one ``.``,
  e.g. ``.gitignore``) are treated as having no stem and the *whole* name as
  the extension, matching .NET's ``Path.GetExtension``/
  ``GetFileNameWithoutExtension`` semantics (``.gitignore`` -> topic
  ``.gitignore``, summary ``GITIGNORE file``) rather than Python's default
  ``os.path.splitext``, which would treat ``.gitignore`` as having no
  extension at all.

CLI:

* ``--root PATH``   Directory to index (default: this script's directory).
* ``--output PATH`` Where to write the index (default: ``<root>/INDEX.md``).
* ``--check``       Do not write anything. Regenerate the index in memory,
  compare it byte-for-byte against the existing file at ``--output``, print
  a match/mismatch summary (counts plus up to 20 added/removed/changed row
  paths), and exit 0 if identical or 1 if not (including if the output file
  does not exist yet).
* With neither flag, the tool writes the regenerated index to ``--output``
  and prints ``Indexed N files into <path>``.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

TEXT_EXTENSIONS = {".md", ".txt", ".json", ".ps1", ".py", ".sh", ".yaml", ".yml"}

HEADING_RE = re.compile(r"^#{1,6}\s+\S")
HEADING_STRIP_RE = re.compile(r"^#{1,6}\s+")
SKIP_BODY_LINE_RE = re.compile(r"^(#|>|\||```|---$)")
DATE_HYPHEN_RE = re.compile(r"(20\d{2})[-_](\d{2})[-_](\d{2})")
DATE_PLAIN_RE = re.compile(r"(20\d{2})(\d{2})(\d{2})")
WHITESPACE_RE = re.compile(r"\s+")
ROW_PATH_RE = re.compile(r"^\| `([^`]*)` \|")

HEADER_LINES = [
    "# 11_TRIAGE index",
    "",
    (
        "> Generated search index. Do not read triage history by default; grep "
        "this file, then open at most the relevant record."
    ),
    "",
    "| Path | Date | Topic | One-line summary |",
    "|---|---|---|---|",
]


def clean_cell(value: str | None, limit: int) -> str:
    """Escape pipes, collapse whitespace, trim, and truncate a cell value."""
    if value is None:
        return ""
    cleaned = WHITESPACE_RE.sub(" ", value.replace("|", "\\|")).strip()
    if len(cleaned) > limit:
        return cleaned[: limit - 3] + "..."
    return cleaned


def file_date(name: str) -> str:
    """Extract a YYYY-MM-DD date from a file name, or '-' if none is found."""
    match = DATE_HYPHEN_RE.search(name)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    match = DATE_PLAIN_RE.search(name)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return "-"


def split_stem_and_extension(name: str) -> tuple[str, str]:
    """Split a file name into (stem, extension) using .NET GetExtension rules.

    .NET's ``Path.GetExtension`` takes everything from the last '.' to the
    end of the name as the extension, with no special case for a leading
    dot. That means a dotfile whose only '.' is the leading one (e.g.
    ``.gitignore``) has *no* stem and the entire name as its extension --
    the opposite of Python's ``os.path.splitext``, which treats such names
    as having no extension at all. For every other name (zero dots, or more
    than one dot) .NET's rule agrees with ``os.path.splitext``, so we only
    special-case that one dotfile shape.
    """
    if name.startswith(".") and name.count(".") == 1:
        return "", name
    return os.path.splitext(name)


def build_row(root: str, rel_path: str) -> str:
    """Build one index row for the file at rel_path (relative to root)."""
    full_path = os.path.join(root, rel_path)
    name = os.path.basename(rel_path)
    stem, extension = split_stem_and_extension(name)

    topic = re.sub(r"[_-]+", " ", stem)
    if not topic.strip():
        topic = name
    summary = f"{extension.lstrip('.').upper()} file"

    if extension in TEXT_EXTENSIONS:
        try:
            with open(full_path, encoding="utf-8-sig", errors="strict") as handle:
                content = handle.read().splitlines()
            heading = next((line for line in content if HEADING_RE.match(line)), None)
            if heading is not None:
                topic = HEADING_STRIP_RE.sub("", heading)
            body = None
            for line in content:
                stripped = line.strip()
                if stripped and not SKIP_BODY_LINE_RE.match(stripped):
                    body = line
                    break
            if body is not None:
                summary = body
        except Exception as exc:  # noqa: BLE001 - mirrors PS1's catch-all
            summary = f"Unreadable during index generation: {type(exc).__name__}"

    path_cell = clean_cell(rel_path, 180)
    date_cell = file_date(name)
    topic_cell = clean_cell(topic, 120)
    summary_cell = clean_cell(summary, 180)
    return f"| `{path_cell}` | {date_cell} | {topic_cell} | {summary_cell} |"


def dotnet_word_sort_key(path: str) -> tuple[list[tuple[int, str]], str]:
    """Approximate PowerShell's ``Sort-Object FullName`` (.NET word-sort).

    Ordering rule, most to least significant:

    1. '-' characters are removed from the comparison entirely (ignored,
       not just low-weighted).
    2. Among the remaining characters, '_', '/', '\\\\', and '.' sort before
       digits ('0'-'9'), which sort before every other character (letters
       compared case-insensitively, by lowercasing).
    3. Ties (identical after the above transform) break on the original,
       unmodified path string, so distinct paths never compare equal.
    """
    stripped = path.replace("-", "")
    weighted: list[tuple[int, str]] = []
    for char in stripped:
        if char in "_/\\.":
            weighted.append((0, char))
        elif char.isdigit():
            weighted.append((1, char))
        else:
            weighted.append((2, char.lower()))
    return (weighted, path)


def list_indexable_files(root: str, output: str) -> list[str]:
    """Return the sorted, git-defined file set to index (see module docstring)."""
    try:
        raw = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:
        raise SystemExit(f"Failed to list git-tracked files under {root!r}: {exc}") from exc

    try:
        output_rel = os.path.relpath(output, root).replace(os.sep, "/")
    except ValueError:
        output_rel = None

    files = [line for line in raw.split("\n") if line and line != output_rel]
    files.sort(key=dotnet_word_sort_key)
    return files


def build_index_lines(root: str, output: str) -> tuple[list[str], list[str]]:
    """Return (all output lines, indexed file list) for root/output."""
    files = list_indexable_files(root, output)
    lines = list(HEADER_LINES)
    lines.extend(build_row(root, rel_path) for rel_path in files)
    return lines, files


def render_content(lines: list[str]) -> str:
    """Render output lines as the final file content (LF, single trailing NL)."""
    return "\n".join(lines) + "\n"


def parse_rows(content: str) -> dict[str, str]:
    """Map row path -> full row line (no trailing newline) from index content."""
    rows: dict[str, str] = {}
    for line in content.split("\n"):
        match = ROW_PATH_RE.match(line)
        if match:
            rows[match.group(1)] = line
    return rows


def run_check(output: str, content: str) -> int:
    """Compare regenerated content against the file at output. See CLI docs."""
    generated_bytes = content.encode("utf-8")
    if os.path.exists(output):
        with open(output, "rb") as handle:
            existing_bytes = handle.read()
    else:
        existing_bytes = None

    if existing_bytes == generated_bytes:
        print(f"OK: {output} is byte-identical to the regenerated index.")
        return 0

    existing_text = existing_bytes.decode("utf-8") if existing_bytes is not None else ""
    existing_rows = parse_rows(existing_text)
    new_rows = parse_rows(content)
    existing_paths = set(existing_rows)
    new_paths = set(new_rows)

    added = sorted(new_paths - existing_paths)
    removed = sorted(existing_paths - new_paths)
    changed = sorted(
        path for path in (existing_paths & new_paths) if existing_rows[path] != new_rows[path]
    )

    print(f"MISMATCH: {output} differs from the regenerated index.")
    print(f"added={len(added)} removed={len(removed)} changed={len(changed)}")

    def show(label: str, paths: list[str]) -> None:
        if not paths:
            return
        print(f"{label} ({len(paths)}, showing up to 20):")
        for path in paths[:20]:
            print(f"  {path}")

    show("Added", added)
    show("Removed", removed)
    show("Changed", changed)
    return 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-platform, stdlib-only equivalent of generate_index.ps1.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Directory to index (default: this script's directory).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write the index to (default: <root>/INDEX.md).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the existing output matches the regenerated index; write nothing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(args.root) if args.root else script_dir
    output = os.path.abspath(args.output) if args.output else os.path.join(root, "INDEX.md")

    lines, files = build_index_lines(root, output)
    content = render_content(lines)

    if args.check:
        return run_check(output, content)

    with open(output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    print(f"Indexed {len(files)} files into {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
