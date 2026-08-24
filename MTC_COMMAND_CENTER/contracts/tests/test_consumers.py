import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SIMULATOR = (
    REPO_ROOT / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "tools" / "mega_walk_forward.py"
)
BRIDGE_TYPES = REPO_ROOT / "IBKR_PAPER_BRIDGE" / "bridge" / "engine" / "types.py"


def class_fields(path: Path, class_name: str) -> set[str]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    node = next(
        item
        for item in module.body
        if isinstance(item, ast.ClassDef) and item.name == class_name
    )
    return {
        item.target.id
        for item in node.body
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
    }


def test_simulator_source_retains_the_read_only_contract_projection_seam():
    module = ast.parse(SIMULATOR.read_text(encoding="utf-8"))
    function = next(
        item
        for item in module.body
        if isinstance(item, ast.FunctionDef) and item.name == "simulate_slice"
    )
    args = {arg.arg for arg in function.args.args}
    source = SIMULATOR.read_text(encoding="utf-8")
    assert {"return_trades", "return_trade_events", "direction", "exit_mode"} <= args
    assert all(
        f'"{field}"' in source
        for field in ("entry_idx", "exit_idx", "entry_price", "exit_price", "is_short")
    )


def test_bridge_source_retains_the_order_projection_and_protection_seams():
    assert {"signal", "qty", "entry_type", "stop_loss", "take_profit"} <= class_fields(
        BRIDGE_TYPES, "OrderPlan"
    )
    assert {"side", "size", "reduce_only", "trigger_px"} <= class_fields(
        BRIDGE_TYPES, "BrokerOrder"
    )
