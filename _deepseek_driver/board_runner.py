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
    fallback: list[str] = field(default_factory=list)


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


def _call_worker(chat_fn, messages, worker: "Worker") -> tuple[str, str, bool]:
    """Call a worker with provider fallback. Returns (output, used_prov, ok).

    Tries worker.prov first, then each fallback provider on any exception
    (e.g. a 402 insufficient-balance). If all fail, returns a captured ERROR
    string so the run continues instead of crashing.
    """
    last_err = None
    for prov in [worker.prov, *worker.fallback]:
        try:
            return chat_fn(messages, prov, worker.model), prov, True
        except Exception as e:  # noqa: BLE001 - intentionally resilient
            last_err = f"ERROR: {type(e).__name__}: {e}"
    return last_err or "ERROR: no provider", (worker.fallback[-1] if worker.fallback else worker.prov), False


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

    # 2. independent fan-out (resilient: per-worker provider fallback, errors captured)
    worker_outputs: dict[str, str] = {}
    worker_meta: list[dict] = []
    for w in bi.workers:
        out, used_prov, ok = _call_worker(chat_fn, _worker_messages(bi), w)
        worker_outputs[w.name] = out
        worker_meta.append({"name": w.name, "prov": w.prov, "model": w.model,
                            "fallback": list(w.fallback), "used_prov": used_prov, "ok": ok})
        _write(run_dir / "worker_outputs" / f"{w.name}.md",
               f"# Worker: {w.name} ({used_prov}/{w.model})\n\n{out}\n")

    # 3. judge synthesis (also resilient — a judge failure must not crash the run)
    try:
        judge_output = chat_fn(_judge_messages(bi, worker_outputs), bi.judge.prov, bi.judge.model)
        judge_ok = True
    except Exception as e:  # noqa: BLE001
        judge_output = f"ERROR: {type(e).__name__}: {e}"
        judge_ok = False
    _write(run_dir / "final_report.md",
           f"# Board verdict: {bi.title}\n\n{judge_output}\n")

    # 4. metadata (no raw secrets, no full task body)
    metadata = {
        "title": bi.title,
        "timestamp": ts,
        "workers": worker_meta,
        "judge": {"name": bi.judge.name, "prov": bi.judge.prov,
                  "model": bi.judge.model, "ok": judge_ok},
        "provider_calls": len(bi.workers) + 1,
        "read_only": True,
    }
    _write(run_dir / "metadata.json", json.dumps(metadata, indent=2))

    return RunResult(run_dir=run_dir, worker_outputs=worker_outputs,
                     judge_output=judge_output, metadata=metadata, writes=writes)


def board_input_from_config(cfg: dict) -> BoardInput:
    """Build a BoardInput from a plain dict (parsed JSON board config)."""
    def _worker(d: dict) -> Worker:
        return Worker(name=d["name"], prov=d.get("prov", "deepseek"),
                      model=d.get("model"), fallback=list(d.get("fallback", [])))

    return BoardInput(
        title=cfg["title"],
        task=cfg["task"],
        context=cfg.get("context", ""),
        workers=[_worker(w) for w in cfg["workers"]],
        judge=_worker(cfg["judge"]),
    )


# Default run location inside the triage tree (read-only artifacts only).
DEFAULT_RUNS_DIR = (
    Path(__file__).resolve().parent.parent
    / "MTC_COMMAND_CENTER" / "11_TRIAGE" / "FUSION" / "runs"
)


def _dry_run_chat_fn(messages, prov, model):
    """No-network chat: deterministic mock reply (for --dry-run)."""
    from mock_provider import MockClient
    mc = MockClient(default=f"[dry-run mock review by {prov}/{model}]")
    return provider.chat(messages, prov=prov, model=model, client=mc)


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Run the read-only MTC AI Boardroom.")
    ap.add_argument("--config", required=True, help="path to board config JSON")
    ap.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR),
                    help="parent folder for run artifacts")
    ap.add_argument("--dry-run", action="store_true",
                    help="use a deterministic mock provider (no network/cost)")
    a = ap.parse_args(argv)

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    bi = board_input_from_config(cfg)
    chat_fn = _dry_run_chat_fn if a.dry_run else None
    res = run_board(bi, runs_dir=a.runs_dir, chat_fn=chat_fn)
    print(f"[board] run saved -> {res.run_dir}")
    print(f"[board] workers ok: "
          f"{sum(1 for w in res.metadata['workers'] if w['ok'])}/{len(res.metadata['workers'])}, "
          f"judge ok: {res.metadata['judge']['ok']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
