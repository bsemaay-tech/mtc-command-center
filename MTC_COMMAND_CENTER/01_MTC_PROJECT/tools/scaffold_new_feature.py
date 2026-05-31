from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURE_TYPES = {
    "signal_producer",
    "signal_transform",
    "entry_filter",
    "exit_rule",
    "stop_loss",
    "take_profit",
    "break_even",
    "trailing_stop",
    "position_sizing",
    "portfolio_guard",
    "visualization_only",
    "alert_payload",
}
STAMP = "feature_scaffold_backup"


def backup(path: Path) -> None:
    if path.exists():
        backup_path = path.with_name(f"{path.name}.bak_{STAMP}")
        if not backup_path.exists():
            shutil.copy2(path, backup_path)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing scaffold file: {path}")
    path.write_text(content.strip() + "\n", encoding="utf-8")


def python_stub_target(feature_type: str, name: str) -> Path | None:
    if feature_type == "signal_producer":
        return ROOT / "00_PYTHON" / "mtc_v2" / "signals" / f"{name}.py"
    if feature_type == "entry_filter":
        folder = ROOT / "00_PYTHON" / "mtc_v2" / "core" / "filters"
        return folder / f"{name}.py" if folder.exists() else None
    if feature_type in {"exit_rule", "stop_loss", "take_profit", "break_even", "trailing_stop"}:
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"exits_{name}.py"
    if feature_type == "position_sizing":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"position_sizer_{name}.py"
    if feature_type == "portfolio_guard":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"guards_{name}.py"
    if feature_type == "alert_payload":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"alerts_{name}.py"
    return None


def scaffold(feature_type: str, feature_id: str, name: str) -> list[Path]:
    if feature_type not in FEATURE_TYPES:
        raise ValueError(f"Unsupported feature type: {feature_type}")
    created: list[Path] = []
    contract = ROOT / "feature_contracts" / "drafts" / f"{feature_id}.yml"
    adapter = ROOT / "parity_oracles" / "feature_adapters" / "pinets" / f"{feature_id}.pine"
    trace = ROOT / "parity_oracles" / "feature_traces" / "python" / f"{feature_id}_trace.py"
    notes = ROOT / "docs" / "feature_notes" / f"{feature_id}.md"
    write(contract, f"feature_id: {feature_id}\nfeature_name: {name}\nfeature_type: {feature_type}\nstatus: draft\nintegration_rule: Do not integrate into canonical MTC_V2.pine until feature-level parity passes.")
    write(adapter, f"//@version=6\nindicator(\"{feature_id} feature adapter\", overlay=false)\nplot(na, title=\"FEATURE__{feature_id}__data__placeholder\", display=display.none)")
    write(trace, f"from parity_oracles.templates.python_feature_trace_template import main\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())")
    write(notes, f"# {feature_id}\n\n- Feature type: `{feature_type}`\n- Integration rule: Do not integrate into canonical MTC_V2.pine until feature-level parity passes.\n")
    created.extend([contract, adapter, trace, notes])
    target = python_stub_target(feature_type, name)
    if target is None:
        notes.write_text(notes.read_text(encoding="utf-8") + "\nPython implementation target is architecture-dependent; use docs-only stub until owner boundary is confirmed.\n", encoding="utf-8")
    else:
        write(target, f"from __future__ import annotations\n\n\ndef evaluate_{name}(*args, **kwargs):\n    raise NotImplementedError(\"Implement only after contract trace columns are finalized.\")")
        created.append(target)
    test_target = ROOT / "00_PYTHON" / "mtc_v2" / "tests" / f"test_{name}.py"
    write(test_target, f"def test_{name}_contract_placeholder():\n    assert True")
    created.append(test_target)
    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature-type", required=True, choices=sorted(FEATURE_TYPES))
    parser.add_argument("--feature-id", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    created = scaffold(args.feature_type, args.feature_id, args.name)
    for path in created:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
