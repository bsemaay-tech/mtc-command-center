# S4 — VS Code Copilot: Heartbeat Reader + Forward Paper Queue (D3a / B4)

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard backend: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/`  
Tools dir: `MTC_COMMAND_CENTER/03_QUANTLENS/tools/`  
Backtest results: `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`

This is the MTC Command Center — a trading strategy research + backtesting system.
You have 2 independent sub-tasks. Do them in order: D3a → B4.

---

## Task D3a — Overnight Heartbeat Reader

### Problem

The dashboard has no visibility into whether overnight batch runs are alive or dead.
Overnight runs write `_heartbeat*.json` files to:
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_runs/`

These files are NOT currently read by the dashboard API.

### What to build

**Step 1:** Create new file:
`MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py`

```python
from pathlib import Path
from datetime import datetime, timezone
import json

MCC_ROOT = Path(__file__).resolve().parents[5]
OVERNIGHT_DIR = MCC_ROOT / "03_QUANTLENS" / "tools" / "overnight_runs"
ALIVE_THRESHOLD_MINUTES = 15


def build_overnight_heartbeat() -> dict:
    """
    Reads all _heartbeat*.json files from overnight_runs/.
    Returns the most recent heartbeat's data plus an is_alive flag.
    """
    if not OVERNIGHT_DIR.exists():
        return {"available": False, "reason": "overnight_runs dir not found"}

    heartbeat_files = sorted(OVERNIGHT_DIR.glob("_heartbeat*.json"))
    if not heartbeat_files:
        return {"available": False, "reason": "no heartbeat files found"}

    # Pick most recent by mtime
    latest = max(heartbeat_files, key=lambda p: p.stat().st_mtime)

    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as e:
        return {"available": False, "reason": f"parse error: {e}"}

    # Determine is_alive from timestamp field (try common key names)
    ts_str = data.get("timestamp") or data.get("ts") or data.get("updated_at")
    is_alive = False
    age_minutes = None
    if ts_str:
        try:
            ts = datetime.fromisoformat(str(ts_str).replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_minutes = (now - ts).total_seconds() / 60
            is_alive = age_minutes < ALIVE_THRESHOLD_MINUTES
        except Exception:
            pass

    return {
        "available": True,
        "source_file": latest.name,
        "is_alive": is_alive,
        "age_minutes": round(age_minutes, 1) if age_minutes is not None else None,
        "stage": data.get("stage") or data.get("phase") or data.get("step"),
        "status": data.get("status"),
        "run_id": data.get("run_id"),
        "timestamp": ts_str,
        "raw": data,
    }
```

**Step 2:** Wire into snapshot.

Edit `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`

Find the function that assembles the snapshot dict (look for where keys like
`"backtest_status"` or `"scorecards"` are assembled). Add `"overnight_heartbeat"` key:

```python
from mcc_readonly.heartbeat_reader import build_overnight_heartbeat

# In the snapshot assembly function, add:
snapshot["overnight_heartbeat"] = build_overnight_heartbeat()
```

Keep ALL existing keys unchanged. Only add the new key.

### Validation for D3a

```bash
cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -c "
import sys; sys.path.insert(0, 'MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api')
from mcc_readonly.heartbeat_reader import build_overnight_heartbeat
r = build_overnight_heartbeat()
print('available:', r['available'])
print('is_alive:', r.get('is_alive'))
print('stage:', r.get('stage'))
print('status:', r.get('status'))
"

python -c "
import sys; sys.path.insert(0, 'MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api')
from mcc_readonly.read_model import build_snapshot
s = build_snapshot()
print('overnight_heartbeat key present:', 'overnight_heartbeat' in s)
print(s.get('overnight_heartbeat', {}).get('available'))
"

python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed — must not regress
```

---

## Task B4 — Build Forward Paper Queue

### Problem

No tooling exists to automatically identify which strategies are CPCV-robust, alpha-positive,
and ready for forward paper trading (i.e., Gate2=PASS + strong CPCV + alpha evidence + Gate3 evidence only
missing final paper-trade confirmation).

### What to build

Create new file:
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_forward_paper_queue.py`

```python
"""
build_forward_paper_queue.py

Reads scorecard_v2/*.scorecard.json from all backtest runs.
Identifies FORWARD_PAPER candidates: Gate2=PASS + cpcv_pass_ratio>=0.7 + net_after_slippage_pct > 0
Outputs: MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/FORWARD_PAPER_QUEUE.md
"""

from pathlib import Path
import json
from datetime import datetime

MCC_ROOT = Path(__file__).resolve().parents[3]
BACKTEST_ROOT = MCC_ROOT / "03_QUANTLENS" / "05_BACKTEST_RESULTS"
STATUS_ROOT = MCC_ROOT / "03_STATUS"
OUTPUT_FILE = BACKTEST_ROOT / "FORWARD_PAPER_QUEUE.md"

CPCV_THRESHOLD = 0.70
SLIPPAGE_NET_MIN = 0.0  # must be positive after slippage


def load_scorecards() -> list[dict]:
    """Load all scorecard_v2 JSON files from BACKTEST_ROOT and STATUS_ROOT."""
    cards = []
    search_roots = [BACKTEST_ROOT, STATUS_ROOT]
    for root in search_roots:
        if not root.exists():
            continue
        for sc_file in root.rglob("scorecard_v2/*.scorecard.json"):
            try:
                data = json.loads(sc_file.read_text(encoding="utf-8"))
                data["_source_file"] = str(sc_file.relative_to(MCC_ROOT))
                cards.append(data)
            except Exception as e:
                print(f"[WARN] Could not parse {sc_file}: {e}")
    return cards


def is_forward_paper_candidate(card: dict) -> tuple[bool, list[str]]:
    """
    Returns (is_candidate, reasons_list).
    Candidate if: Gate2=PASS AND cpcv_pass_ratio>=0.7 AND net_after_slippage_pct>0
    """
    reasons = []
    gate2 = card.get("gate2", {})
    metrics = gate2.get("metrics", {})

    gate2_pass = gate2.get("pass", False)
    if not gate2_pass:
        return False, ["Gate2 not PASS"]

    cpcv = metrics.get("cpcv_pass_ratio", {})
    cpcv_val = cpcv.get("value") if isinstance(cpcv, dict) else cpcv
    if cpcv_val is None or cpcv_val < CPCV_THRESHOLD:
        return False, [f"CPCV {cpcv_val} < {CPCV_THRESHOLD}"]

    slip = metrics.get("net_after_slippage_pct", {})
    slip_val = slip.get("value") if isinstance(slip, dict) else slip
    if slip_val is None or slip_val <= SLIPPAGE_NET_MIN:
        return False, [f"Net slippage return {slip_val} <= {SLIPPAGE_NET_MIN}"]

    reasons.append(f"Gate2=PASS, CPCV={cpcv_val:.2f}, NetSlip={slip_val:.1f}%")

    # Bonus: note if gate_summary says promotable
    if card.get("gate_summary", {}).get("promotable"):
        reasons.append("PROMOTABLE=true")
    else:
        reasons.append("Gate3 still incomplete (paper-trade evidence needed)")

    return True, reasons


def build_queue():
    cards = load_scorecards()
    print(f"Loaded {len(cards)} scorecards from {BACKTEST_ROOT} + {STATUS_ROOT}")

    candidates = []
    for card in cards:
        is_cand, reasons = is_forward_paper_candidate(card)
        if is_cand:
            gate2 = card.get("gate2", {})
            metrics = gate2.get("metrics", {})

            def mval(key):
                v = metrics.get(key, {})
                return v.get("value") if isinstance(v, dict) else v

            candidates.append({
                "strategy_id": card.get("strategy_id", "unknown"),
                "symbol": card.get("symbol", ""),
                "timeframe": card.get("timeframe", ""),
                "gate2_score": gate2.get("score"),
                "cpcv": mval("cpcv_pass_ratio"),
                "pbo": mval("pbo"),
                "net_slippage": mval("net_after_slippage_pct"),
                "sharpe": mval("sharpe"),
                "sortino": mval("sortino"),
                "promotable": card.get("gate_summary", {}).get("promotable", False),
                "reasons": reasons,
                "source": card.get("_source_file", ""),
            })

    candidates.sort(key=lambda c: (not c["promotable"], -(c["cpcv"] or 0)))

    lines = [
        "# FORWARD_PAPER_QUEUE",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} — {len(candidates)} candidates_",
        "",
        "## Criteria",
        f"- Gate2 = PASS",
        f"- CPCV pass ratio ≥ {CPCV_THRESHOLD}",
        f"- Net after slippage > {SLIPPAGE_NET_MIN}%",
        "",
        "## Candidates",
        "",
    ]

    if not candidates:
        lines.append("_No candidates meet all criteria._")
    else:
        lines.append("| # | Strategy | Symbol | TF | Gate2 | CPCV | PBO | Net% | Sharpe | Promotable |")
        lines.append("|---|----------|--------|-----|-------|------|-----|------|--------|------------|")
        for i, c in enumerate(candidates, 1):
            promo = "YES" if c["promotable"] else "no"
            lines.append(
                f"| {i} | {c['strategy_id']} | {c['symbol']} | {c['timeframe']} "
                f"| {c['gate2_score']} | {c['cpcv']:.2f} | {c['pbo'] or 'N/A'} "
                f"| {c['net_slippage']:.1f} | {c['sharpe'] or 'N/A'} | {promo} |"
            )
        lines.append("")
        for c in candidates:
            lines.append(f"### {c['strategy_id']} | {c['symbol']} {c['timeframe']}")
            for r in c["reasons"]:
                lines.append(f"- {r}")
            lines.append(f"- Source: `{c['source']}`")
            lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {OUTPUT_FILE}")
    print(f"Total candidates: {len(candidates)}")
    return candidates


if __name__ == "__main__":
    build_queue()
```

### Validation for B4

```bash
cd C:\LAB\Tradingview_LAB_CLEAN
python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_forward_paper_queue.py
# Expected: prints candidate count and "Written: ...FORWARD_PAPER_QUEUE.md"

python -c "
from pathlib import Path
md = Path('MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/FORWARD_PAPER_QUEUE.md')
print('Exists:', md.exists())
print(md.read_text(encoding='utf-8')[:800])
"

python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_forward_paper_queue.py
python -m py_compile MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py
python -m py_compile MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
# Expected: no output (clean compile)
```

---

## HARD SAFETY RULES

- NEVER edit: `*.pine` files, `MTC_V2.pine`, `mega_walk_forward.py`, `mtc_runner.py`
- NEVER edit: `05_REGISTRY/*.json` (generated files — never touch)
- NEVER edit: `apps/web/app.js` or `apps/web/styles.css` (S2's domain)
- NEVER edit: `02_MTC_BACKTEST/src/engine/` (engine files are locked)
- Only write to:
  - `08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py` (NEW file — D3a)
  - `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` (add one import + one dict key only)
  - `03_QUANTLENS/tools/build_forward_paper_queue.py` (NEW file — B4)
  - `03_QUANTLENS/05_BACKTEST_RESULTS/FORWARD_PAPER_QUEUE.md` (generated output)

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S4_COPILOT_REPORT.md`

Report must contain:
- **D3a result**: Did `build_overnight_heartbeat()` return `available: True` or `False`? Why?
  (If no heartbeat files exist yet, `available: False` with reason is a valid/expected result)
- **D3a snapshot**: Is `overnight_heartbeat` key present in `build_snapshot()` output?
- **B4 result**: How many forward-paper candidates found? List them (strategy_id | symbol | tf | CPCV | net%)
- **Dashboard API test result**: Still 35 passed? (must not regress)
- **py_compile** result for all 3 modified/created `.py` files
