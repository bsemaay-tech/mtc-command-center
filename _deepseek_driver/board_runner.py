"""MTC AI Boardroom — read-only review board (Phase 1 MVP).

Fans one normalized review task out to several independent worker models (no
cross-talk), then a judge model synthesizes consensus / contradictions / gaps /
unique insights / risks / next action. The whole run is persisted under a
versioned run folder.

READ-ONLY by construction: this module has NO file-editing tools. It only writes
its own run artifacts inside `runs_dir/<timestamp>/`. It never imports or calls
the ds_agent edit/write sandbox, and it refuses to write into protected paths.

Provider calls go through an injected `chat_fn(messages, prov, model) -> str`
(default: provider.chat). Tests inject a deterministic mock, so no network.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import provider

# Never write a run folder into protected scopes (Pine/parity/MTC_V2/.git).
_PROTECTED = re.compile(r"(\.pine$|parity|MTC_V2|\.git[\\/])", re.IGNORECASE)

# Redact obvious secrets before anything is persisted or sent onward.
_SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{8,}"),       # OpenAI/DeepSeek-style keys
    re.compile(r"xai-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"\b[A-Fa-f0-9]{32,}\b"),         # long hex tokens
]

_WORKER_SYS = (
    "You are an independent technical reviewer on the MTC review board. "
    "Review the task on its own merits. You do not see other reviewers' answers. "
    "Be concrete and skeptical. Do not propose file edits; produce a written review only."
)

_JUDGE_SYS = (
    "JUDGE. You are the MTC review-board judge. You receive several independent "
    "worker reviews of the same task. Synthesize them into one verdict with these "
    "sections: Consensus, Contradictions, Coverage gaps, Unique insights, Risks, "
    "Recommended next action. Do not propose file edits."
)


@dataclass
class Worker:
    name: str
    prov: str = "deepseek"
    model: str | None = None


@dataclass
class BoardInput:
    title: str
    task: str
    workers: list[Worker]
    judge: Worker
    context: str = ""


@dataclass
class RunResult:
    run_dir: Path
    worker_outputs: dict[str, str]
    judge_output: str
    metadata: dict
    writes: list[str] = field(default_factory=list)


def redact(text: str) -> str:
    """Replace obvious secret-looking tokens with REDACTED."""
    out = text or ""
    for pat in _SECRET_PATTERNS:
        out = pat.sub("REDACTED", out)
    return out


def _worker_messages(bi: BoardInput) -> list[dict]:
    body = bi.task if not bi.context else f"{bi.task}\n\n## Context\n{bi.context}"
    return [
        {"role": "system", "content": _WORKER_SYS},
        {"role": "user", "content": redact(body)},
    ]


def _judge_messages(bi: BoardInput, worker_outputs: dict[str, str]) -> list[dict]:
    sections = [f"## Worker: {name}\n{redact(out)}" for name, out in worker_outputs.items()]
    user = (
        f"# Task\n{redact(bi.task)}\n\n"
        f"# Independent worker reviews\n" + "\n\n".join(sections)
    )
    return [
        {"role": "system", "content": _JUDGE_SYS},
        {"role": "user", "content": user},
    ]


def _default_chat_fn(messages, prov, model):
    return provider.chat(messages, prov=prov, model=model)


def run_board(
    bi: BoardInput,
    *,
    runs_dir: Path | str,
    chat_fn: Callable[[list, str, str | None], str] | None = None,
    now: Callable[[], _dt.datetime] | _dt.datetime | None = None,
) -> RunResult:
    """Run the read-only board and persist a versioned run folder.

    Args:
      runs_dir: parent folder for run subfolders (e.g. 11_TRIAGE/FUSION/runs).
      chat_fn:  injected provider call; defaults to provider.chat.
      now:      a datetime or zero-arg callable returning one (for deterministic tests).
    """
    runs_dir = Path(runs_dir)
    if _PROTECTED.search(str(runs_dir.resolve())):
        raise ValueError(f"refusing protected runs_dir: {runs_dir}")

    chat_fn = chat_fn or _default_chat_fn
    if callable(now):
        stamp = now()
    elif isinstance(now, _dt.datetime):
        stamp = now
    else:
        stamp = _dt.datetime.now()
    ts = stamp.strftime("%Y-%m-%dT%H-%M-%S")

    run_dir = runs_dir / ts
    (run_dir / "worker_outputs").mkdir(parents=True, exist_ok=True)
    writes: list[str] = []

    def _write(path: Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")
        writes.append(str(path))

    # 1. persist the (redacted) input
    ctx = f"\n\n## Context\n{redact(bi.context)}" if bi.context else ""
    _write(run_dir / "input.md",
           f"# {bi.title}\n\n## Task\n{redact(bi.task)}{ctx}\n")

    # 2. independent fan-out
    worker_outputs: dict[str, str] = {}
    for w in bi.workers:
        out = chat_fn(_worker_messages(bi), w.prov, w.model)
        worker_outputs[w.name] = out
        _write(run_dir / "worker_outputs" / f"{w.name}.md",
               f"# Worker: {w.name} ({w.prov}/{w.model})\n\n{out}\n")

    # 3. judge synthesis
    judge_output = chat_fn(_judge_messages(bi, worker_outputs), bi.judge.prov, bi.judge.model)
    _write(run_dir / "final_report.md",
           f"# Board verdict: {bi.title}\n\n{judge_output}\n")

    # 4. metadata (no raw secrets, no full task body)
    metadata = {
        "title": bi.title,
        "timestamp": ts,
        "workers": [{"name": w.name, "prov": w.prov, "model": w.model} for w in bi.workers],
        "judge": {"name": bi.judge.name, "prov": bi.judge.prov, "model": bi.judge.model},
        "provider_calls": len(bi.workers) + 1,
        "read_only": True,
    }
    _write(run_dir / "metadata.json", json.dumps(metadata, indent=2))

    return RunResult(run_dir=run_dir, worker_outputs=worker_outputs,
                     judge_output=judge_output, metadata=metadata, writes=writes)
