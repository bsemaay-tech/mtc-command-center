"""
MTC CLI — agent-native command surface for MTC Command Center.

Usage:
    python -m mtc_cli audit repo [--json]

Commands:
    audit repo   Read-only repo health snapshot.
"""
from __future__ import annotations

import argparse
import sys

from mtc_cli import contract


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m mtc_cli",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", metavar="COMMAND")

    # audit
    audit_p = sub.add_parser("audit", help="repo audit commands")
    audit_sub = audit_p.add_subparsers(dest="audit_target", metavar="TARGET")
    repo_p = audit_sub.add_parser("repo", help="read-only repo health snapshot")
    repo_p.add_argument("--json", action="store_true", help="emit JSON envelope on stdout")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "audit":
        if args.audit_target == "repo":
            as_json = getattr(args, "json", False)
            from mtc_cli.commands import audit
            envelope = audit.run()
            return contract.emit(envelope, as_json=as_json)
        parser.parse_args(["audit", "--help"])
        return contract.EXIT_ERROR

    parser.print_help()
    return contract.EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
