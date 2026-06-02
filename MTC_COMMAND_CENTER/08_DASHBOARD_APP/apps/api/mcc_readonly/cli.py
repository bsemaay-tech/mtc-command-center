from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .backtest_reader import build_backtest_status
from .health import build_health_report
from .liveops_reader import build_liveops_status
from .optimization_reader import build_optimization_status
from .parity_reader import build_parity_status
from .pine_builder_reader import build_pine_builder_status
from .audit_reader import build_candidate_audit
from .read_model import build_dashboard_snapshot, build_read_model
from .registry_reader import build_strategy_registry
from .server import serve
from .task_lifecycle import build_task_lifecycle
from .writer import process_inbox


def main(argv: list[str] | None = None) -> int:
    _configure_stdout()
    parser = argparse.ArgumentParser(prog="mcc-readonly", description="MCC MVP-1 read-only API tools")
    parser.add_argument("--mcc-root", default=None, help="Path to MTC_COMMAND_CENTER root")
    # command optional: bare `python -m mcc_readonly` defaults to `serve` + opens the dashboard.
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("health", help="Print the MVP-1 health report")
    subparsers.add_parser("read-model", help="Print the read-model diagnostics")
    subparsers.add_parser("snapshot", help="Print the dashboard snapshot payload")
    subparsers.add_parser("task-diagnostics", help="Print read-only task lifecycle diagnostics")
    subparsers.add_parser("liveops-status", help="Print normalized read-only LiveOps dry-run status")
    subparsers.add_parser("parity-status", help="Print normalized read-only parity status")
    subparsers.add_parser("backtest-status", help="Print normalized read-only backtest status")
    subparsers.add_parser("optimization-status", help="Print normalized read-only optimization status")
    subparsers.add_parser("registry-status", help="Print normalized read-only strategy registry")
    subparsers.add_parser("pine-builder-status", help="Print normalized read-only Pine Builder status")
    subparsers.add_parser("audit", help="Print the read-only candidate audit")

    serve_parser = subparsers.add_parser("serve", help="Run the read-only local HTTP API")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", default=8765, type=int)

    writer_parser = subparsers.add_parser("process-inbox", help="Run the MVP-2 controlled task proposal writer")
    writer_parser.add_argument("--owner-ai", default="codex-local")
    writer_parser.add_argument("--task-id", default="MCC-BOOT-010")

    args = parser.parse_args(argv)
    root = Path(args.mcc_root).resolve(strict=False) if args.mcc_root else None

    if args.command is None:
        # No subcommand: launch the dashboard and open it in the browser.
        host, port = "127.0.0.1", 8765
        url = f"http://{host}:{port}/dashboard"
        import threading
        import webbrowser

        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        print(f"MTC Command Center -> {url}  (Ctrl+C to stop)")
        serve(host=host, port=port, mcc_root=root)
        return 0

    if args.command == "health":
        _print_json(build_health_report(root))
        return 0
    if args.command == "read-model":
        _print_json(build_read_model(root))
        return 0
    if args.command == "snapshot":
        _print_json(build_dashboard_snapshot(root))
        return 0
    if args.command == "task-diagnostics":
        snapshot = build_dashboard_snapshot(root)
        _print_json(build_task_lifecycle(snapshot.get("task_queue")))
        return 0
    if args.command == "liveops-status":
        _print_json(build_liveops_status(root))
        return 0
    if args.command == "parity-status":
        _print_json(build_parity_status(root))
        return 0
    if args.command == "backtest-status":
        _print_json(build_backtest_status(root))
        return 0
    if args.command == "optimization-status":
        _print_json(build_optimization_status(root))
        return 0
    if args.command == "registry-status":
        _print_json(build_strategy_registry(root))
        return 0
    if args.command == "pine-builder-status":
        _print_json(build_pine_builder_status(root))
        return 0
    if args.command == "audit":
        _print_json(build_candidate_audit(root))
        return 0
    if args.command == "serve":
        serve(host=args.host, port=args.port, mcc_root=root)
        return 0
    if args.command == "process-inbox":
        _print_json(process_inbox(root, owner_ai=args.owner_ai, task_id=args.task_id))
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
