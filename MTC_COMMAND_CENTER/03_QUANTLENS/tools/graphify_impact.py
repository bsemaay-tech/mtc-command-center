#!/usr/bin/env python3
"""Safe Graphify wrapper for on-demand code impact analysis.

Graphify writes its ``graphify-out/`` into the TARGET path. Pointing it at the
repo would litter the working tree. This wrapper always works on a *copy* of the
scoped source under a temp dir, so graphs never land in the repo. Code extraction
is fully local (tree-sitter); LLM API keys are blanked so nothing can be sent out.

Requires the ``graphify`` CLI: ``uv tool install graphifyy --python 3.13`` (once).

Usage:
    # build a graph for a scoped path (dir or file), then query it
    python 03_QUANTLENS/tools/graphify_impact.py build 08_DASHBOARD_APP/apps/api/mcc_readonly
    python 03_QUANTLENS/tools/graphify_impact.py affected "read_model.py"
    python 03_QUANTLENS/tools/graphify_impact.py explain  "pipeline_reader"
    python 03_QUANTLENS/tools/graphify_impact.py query    "what builds the snapshot"

``build`` caches the scoped copy + graph under a temp workdir; the query
subcommands reuse the last build (pass --path to rebuild for a different scope).
Nothing in the repo is written or modified; sources are read-only.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
QUANTLENS_ROOT = TOOLS_DIR.parent
MCC_ROOT = QUANTLENS_ROOT.parent
REPO_ROOT = MCC_ROOT.parent

WORK = Path(tempfile.gettempdir()) / "mtc_graphify_work"
SRC = WORK / "src"
GRAPH = SRC / "graphify-out" / "graph.json"

CODE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
            ".c", ".h", ".cpp", ".cs", ".kt", ".php", ".swift", ".lua", ".sh"}
# Never copy these into the scan (data/secrets/noise).
SKIP_DIR = {".git", ".venv", ".venvs", "node_modules", "__pycache__",
            "graphify-out", "05_BACKTEST_RESULTS", "data"}


def _blank_key_env() -> dict:
    env = dict(os.environ)
    for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY",
              "AZURE_OPENAI_API_KEY", "OLLAMA_BASE_URL"):
        env.pop(k, None)
    return env


def _resolve(path_arg: str) -> Path:
    p = Path(path_arg)
    if not p.is_absolute():
        # accept paths relative to repo root or MCC root
        for base in (Path.cwd(), REPO_ROOT, MCC_ROOT):
            if (base / p).exists():
                return (base / p).resolve()
    return p.resolve()


def build(path_arg: str) -> int:
    target = _resolve(path_arg)
    if not target.exists():
        print(f"not found: {target}")
        return 1
    if shutil.which("graphify") is None:
        print("graphify not installed. Run: uv tool install graphifyy --python 3.13")
        return 1
    if WORK.exists():
        shutil.rmtree(WORK, ignore_errors=True)
    SRC.mkdir(parents=True, exist_ok=True)

    copied = 0
    if target.is_file():
        if target.suffix.lower() in CODE_EXT:
            shutil.copy2(target, SRC / target.name)
            copied = 1
    else:
        for f in target.rglob("*"):
            if f.is_file() and f.suffix.lower() in CODE_EXT \
                    and not any(part in SKIP_DIR for part in f.parts):
                rel = f.relative_to(target)
                dest = SRC / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                copied += 1
    if copied == 0:
        print(f"no code files found under {target}")
        return 1

    print(f"[graphify] scoped {copied} file(s) -> {SRC}")
    res = subprocess.run(["graphify", "update", str(SRC), "--no-cluster"],
                         env=_blank_key_env(), capture_output=True, text=True)
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        return res.returncode
    print(f"[graphify] graph at {GRAPH}")
    return 0


def query_cmd(sub: str, arg: str, extra: list[str]) -> int:
    if not GRAPH.exists():
        print("No graph yet. Run `build <path>` first.")
        return 1
    cmd = ["graphify", sub, arg, "--graph", str(GRAPH)] + extra
    return subprocess.run(cmd, env=_blank_key_env()).returncode


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build graph for a scoped path")
    b.add_parser if False else b.add_argument("path")

    for name in ("affected", "explain", "query", "path"):
        s = sub.add_parser(name, help=f"graphify {name} on the last build")
        s.add_argument("arg")
        s.add_argument("--path", help="rebuild for this scope first")
        s.add_argument("--budget", help="token budget (query)", default=None)

    args, unknown = ap.parse_known_args(argv)

    if args.cmd == "build":
        return build(args.path)

    if getattr(args, "path", None):
        rc = build(args.path)
        if rc != 0:
            return rc
    extra = []
    if getattr(args, "budget", None):
        extra += ["--budget", args.budget]
    return query_cmd(args.cmd, args.arg, extra)


if __name__ == "__main__":
    raise SystemExit(main())
