from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate_walkforward_summary(summary_path: Path) -> dict:
    if not summary_path.exists():
        return {"status": "ALERT", "reason": "missing_summary"}
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    if payload.get("status") != "OK":
        return {"status": "ALERT", "reason": "summary_status_not_ok"}
    if int(payload.get("ok_candidates", 0)) < 1:
        return {"status": "ALERT", "reason": "no_ok_candidates"}
    return {"status": "OK", "reason": "healthy"}


def evaluate_operational_alerts(metrics_path: Path, checksum_report_path: Path | None = None) -> dict:
    if not metrics_path.exists():
        return {"status": "ALERT", "reason": "missing_ops_metrics"}

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    if not bool(metrics.get("overall_pass", False)):
        return {"status": "ALERT", "reason": "parity_nightly_fail"}

    if checksum_report_path and checksum_report_path.exists():
        checksum = json.loads(checksum_report_path.read_text(encoding="utf-8"))
        mismatch_count = int(checksum.get("checksum_mismatch_count", 0))
        if mismatch_count > 0:
            return {"status": "ALERT", "reason": "checksum_mismatch"}

    return {"status": "OK", "reason": "healthy"}


def main() -> None:
    p = argparse.ArgumentParser(description="Health alerts for optimizer/parity operations.")
    p.add_argument("--walkforward-summary", required=False)
    p.add_argument("--ops-metrics", required=False)
    p.add_argument("--checksum-report", required=False)
    p.add_argument("--out", required=False)
    args = p.parse_args()

    if args.ops_metrics:
        result = evaluate_operational_alerts(
            Path(args.ops_metrics),
            Path(args.checksum_report) if args.checksum_report else None,
        )
    else:
        if not args.walkforward_summary:
            raise ValueError("Provide --walkforward-summary or --ops-metrics")
        result = evaluate_walkforward_summary(Path(args.walkforward_summary))
    text = json.dumps(result, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Health result written: {out}")
    else:
        print(text)

    if result["status"] != "OK":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
