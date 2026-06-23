#!/usr/bin/env python
"""DeepSeek autonomous-editor harness (sandboxed subagent).

Drives DeepSeek via the OpenAI-compatible API with a tiny tool-calling loop so it
can read/edit a FIXED allowlist of files, py_compile, and run smoke checks — then
emit a structured completion report. No git, no commit, no network beyond the API.

Usage:
  python ds_agent.py --task task.json
  python ds_agent.py --selftest

task.json schema:
  {
    "title": "Batch B ...",
    "allow": ["abs\\path\\file1.py", "abs\\path\\file2.py", ...],   # writable files
    "read_extra": ["abs\\path\\reference.py", ...],                  # read-only refs
    "prompt": "the full batch prompt text",
    "max_iters": 40,
    "model": "deepseek-chat"
  }

Safety:
  - write/edit ONLY to files in `allow`.
  - DENYLIST regex refuses writes even if allowlisted (pine/parity/schemas/MTC_V2/.git).
  - read_file restricted to allow + read_extra.
  - run_python: runs a snippet with cwd = first allow file's dir, timeout 120s. No git.
  - every write is echoed to stdout.
"""
from __future__ import annotations

import argparse
import ast
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from openai import OpenAI

# Provider routing is the shared layer (single source of truth, reused by board_runner).
from provider import PROVIDERS, resolve_provider

# HARD denylist: NEVER writable, no exception possible (trading/Pine/parity/vcs).
HARD_DENYLIST = re.compile(r"(\.pine$|parity|MTC_V2|\.git[\\/])", re.IGNORECASE)
# SOFT denylist: writable ONLY if the task lists the exact file in `schema_allow`.
SOFT_DENYLIST = re.compile(r"(06_SCHEMAS)", re.IGNORECASE)

API_BASE = PROVIDERS["deepseek"][0]  # legacy default for selftest

# run_python is read-only: edits MUST go through edit_file (where the allowlist guard
# lives). Reject any snippet that imports dangerous modules, opens files for write, or
# calls write/exec/network primitives. Cooperative barrier (not adversarial sandbox).
_BANNED_IMPORTS = {"subprocess", "shutil", "socket", "urllib", "requests", "ctypes",
                   "multiprocessing", "pickle", "marshal"}
_BANNED_NAMES = {"eval", "exec", "compile", "__import__", "open", "input", "breakpoint"}
_BANNED_ATTRS = {"write", "writelines", "write_text", "write_bytes", "unlink", "rename",
                 "replace", "rmtree", "remove", "removedirs", "mkdir", "makedirs",
                 "rmdir", "truncate", "chmod", "system", "popen", "spawn", "fdopen",
                 "remove", "move", "copy", "copyfile", "copytree", "symlink_to"}


def check_run_python(code: str) -> str | None:
    """Return an error string if `code` uses write/exec/network primitives, else None."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"SYNTAX_ERROR: {e}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in _BANNED_IMPORTS:
                    return f"DENIED run_python: import '{a.name}' blocked (read-only). Use edit_file to write."
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in _BANNED_IMPORTS:
                return f"DENIED run_python: from '{node.module}' blocked (read-only). Use edit_file to write."
        elif isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            return f"DENIED run_python: '{node.id}' blocked (read-only). Use read_file/edit_file."
        elif isinstance(node, ast.Attribute) and node.attr in _BANNED_ATTRS:
            return f"DENIED run_python: '.{node.attr}(...)' blocked (read-only). Use edit_file to write files."
    return None


class Sandbox:
    def __init__(self, allow: list[str], read_extra: list[str], schema_allow: list[str] | None = None):
        self.schema_allow = {str(Path(p).resolve()) for p in (schema_allow or [])}
        self.allow = {str(Path(p).resolve()) for p in allow} | self.schema_allow
        self.readable = self.allow | {str(Path(p).resolve()) for p in read_extra}
        first = allow or list(self.schema_allow)
        self.run_cwd = str(Path(first[0]).resolve().parent) if first else os.getcwd()
        self.writes: list[str] = []

    def _check_write(self, path: str) -> str | None:
        rp = str(Path(path).resolve())
        if rp not in self.allow:
            return f"DENIED: {path} not in write allowlist"
        if HARD_DENYLIST.search(rp):
            return f"DENIED: {path} matches protected HARD denylist (Pine/parity/MTC_V2/.git) — never writable"
        if SOFT_DENYLIST.search(rp) and rp not in self.schema_allow:
            return f"DENIED: {path} is in 06_SCHEMAS — add it to task 'schema_allow' to permit"
        return None

    def read_file(self, path: str, offset: int | None = None,
                  limit: int | None = None, **_ignore) -> str:
        rp = str(Path(path).resolve())
        if rp not in self.readable:
            return f"DENIED: {path} not readable (not in allow/read_extra)"
        try:
            text = Path(rp).read_text(encoding="utf-8")
        except Exception as e:
            return f"ERROR reading {path}: {e}"
        if offset is None and limit is None:
            cap = 60000
            if len(text) > cap:
                return (text[:cap] +
                        f"\n\n... [TRUNCATED: file is {len(text)} chars; showing first {cap}. "
                        f"Use offset/limit to page, or read a smaller sample file.]")
            return text
        lines = text.splitlines()
        start = max(0, (offset or 1) - 1)
        end = start + limit if limit else len(lines)
        return "\n".join(f"{i+1}\t{l}" for i, l in enumerate(lines[start:end], start=start))

    def edit_file(self, path: str, old: str, new: str) -> str:
        err = self._check_write(path)
        if err:
            return err
        try:
            txt = Path(path).read_text(encoding="utf-8")
        except Exception as e:
            return f"ERROR reading {path}: {e}"
        cnt = txt.count(old)
        if cnt == 0:
            return f"NO_MATCH: old_string not found in {path}"
        if cnt > 1:
            return f"AMBIGUOUS: old_string appears {cnt}x in {path}; add more context"
        Path(path).write_text(txt.replace(old, new), encoding="utf-8")
        self.writes.append(path)
        print(f"  [WRITE] edit_file {path} (1 replacement)", flush=True)
        return f"OK: replaced 1 occurrence in {path}"

    def write_file(self, path: str, content: str) -> str:
        err = self._check_write(path)
        if err:
            return err
        Path(path).write_text(content, encoding="utf-8")
        self.writes.append(path)
        print(f"  [WRITE] write_file {path} ({len(content)} bytes)", flush=True)
        return f"OK: wrote {len(content)} bytes to {path}"

    def py_compile(self, paths: list[str]) -> str:
        bad = [p for p in paths if str(Path(p).resolve()) not in self.readable]
        if bad:
            return f"DENIED: {bad} not in sandbox"
        r = subprocess.run([sys.executable, "-m", "py_compile", *paths],
                           capture_output=True, text=True)
        return f"returncode={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"

    def run_python(self, code: str) -> str:
        err = check_run_python(code)
        if err:
            print(f"  [BLOCKED] run_python rejected: {err}", flush=True)
            return err
        r = subprocess.run([sys.executable, "-c", code], cwd=self.run_cwd,
                           capture_output=True, text=True, timeout=120)
        return f"returncode={r.returncode}\nstdout={r.stdout[-6000:]}\nstderr={r.stderr[-3000:]}"


TOOLS = [
    {"type": "function", "function": {
        "name": "read_file", "description": "Read a file (allowlist/read_extra only).",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}},
                       "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "edit_file",
        "description": "Exact-match single replacement. old must be unique in the file.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}},
            "required": ["path", "old", "new"]}}},
    {"type": "function", "function": {
        "name": "write_file", "description": "Overwrite full file content (allowlist only). Prefer edit_file.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "py_compile", "description": "python -m py_compile on given paths.",
        "parameters": {"type": "object", "properties": {
            "paths": {"type": "array", "items": {"type": "string"}}},
            "required": ["paths"]}}},
    {"type": "function", "function": {
        "name": "run_python", "description": "Run a python -c snippet (cwd=tools dir, 120s).",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}},
                       "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "finish", "description": "Call when done; pass the full structured report markdown.",
        "parameters": {"type": "object", "properties": {"report": {"type": "string"}},
                       "required": ["report"]}}},
]

SYSTEM = (
    "You are DeepSeek operating as a sandboxed code-editing subagent in the repo "
    "C:\\LAB\\Tradingview_LAB_CLEAN. You can ONLY touch files via the provided tools. "
    "Writes are restricted to an allowlist; protected files (Pine/parity/schemas) are "
    "refused. NEVER attempt git/commit/push. Make the minimal edits the task specifies, "
    "verify with py_compile + run_python, then call finish() with the EXACT report "
    "structure the task asks for. If a write is DENIED, do not work around it — report it."
)


def _dump(out_path: Path, messages: list, report: str, writes: list) -> None:
    try:
        lines = [f"# DeepSeek run report  ({_dt.datetime.now().isoformat(timespec='seconds')})",
                 "", "## Completion report", report, "",
                 f"## Files written: {sorted(set(writes))}", "", "## Full transcript", ""]
        for m in messages:
            role = m.get("role", "?")
            if m.get("content"):
                lines.append(f"### {role}\n{m['content']}\n")
            for tc in (m.get("tool_calls") or []):
                fn = tc.get("function", {})
                lines.append(f"### {role} tool_call {fn.get('name')}\n{fn.get('arguments')}\n")
        out_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n[saved] full report + transcript -> {out_path}", flush=True)
    except Exception as e:
        print(f"[warn] could not write report file: {e}", flush=True)


def run_task(task: dict) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # avoid cp1254 crash
    except Exception:
        pass
    prov, base, key = resolve_provider(task)
    model = task.get("model") or os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    client = OpenAI(api_key=key, base_url=base)
    sb = Sandbox(task.get("allow", []), task.get("read_extra", []), task.get("schema_allow", []))
    slug = re.sub(r"[^a-z0-9]+", "_", task.get("title", "task").lower())[:40]
    report_path = Path(task.get("report_out") or (Path(r"C:\tmp") / f"ds_{slug}_report.md"))
    dispatch = {"read_file": sb.read_file, "edit_file": sb.edit_file,
                "write_file": sb.write_file, "py_compile": sb.py_compile,
                "run_python": sb.run_python}
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": task["prompt"]}]
    print(f"=== task: {task.get('title','(untitled)')} | provider={prov} model={model} ===", flush=True)
    print(f"  allow={list(sb.allow)}", flush=True)
    for it in range(int(task.get("max_iters", 40))):
        resp = client.chat.completions.create(
            model=model, messages=messages, tools=TOOLS, tool_choice="auto", temperature=0)
        msg = resp.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            rep = msg.content or "(no content)"
            print(f"\n--- DeepSeek stopped without finish() (iter {it}) ---\n{rep}", flush=True)
            _dump(report_path, messages, rep, sb.writes)
            return 0
        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            if name == "finish":
                rep = args.get("report", "(empty report)")
                print("\n================ COMPLETION REPORT ================\n", flush=True)
                print(rep, flush=True)
                print(f"\n=== files written: {sorted(set(sb.writes))} ===", flush=True)
                _dump(report_path, messages, rep, sb.writes)
                return 0
            fn = dispatch.get(name)
            print(f"  [iter {it}] {name}({ {k:(v[:60]+'…' if isinstance(v,str) and len(v)>60 else v) for k,v in args.items()} })", flush=True)
            try:
                result = fn(**args) if fn else f"UNKNOWN_TOOL {name}"
            except Exception as e:
                result = f"TOOL_ERROR {name}: {type(e).__name__}: {e}"
                print(f"    -> {result}", flush=True)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    print("\n[ERROR] hit max_iters without finish().", flush=True)
    _dump(report_path, messages, "(hit max_iters without finish)", sb.writes)
    return 1


def selftest() -> int:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("KEY_MISSING"); return 1
    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    client = OpenAI(api_key=key, base_url=API_BASE)
    r = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": "reply with exactly: PONG"}],
        temperature=0)
    print(f"model={model} reply={r.choices[0].message.content!r}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", type=Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    task = json.loads(a.task.read_text(encoding="utf-8"))
    return run_task(task)


if __name__ == "__main__":
    raise SystemExit(main())
