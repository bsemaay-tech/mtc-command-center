from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, default_quantlens_root


def _jsonable(obj: Any) -> Any:
    """Deep-coerce parsed YAML to JSON-native types.

    PyYAML turns unquoted dates (e.g. ``created_at: 2026-05-01``) into
    ``datetime.date`` objects, which are not JSON-serializable and would break
    the read-only dashboard snapshot. Convert date/datetime to ISO strings.
    """
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj

try:
    import yaml
except Exception:
    yaml = None

DECISION_LABELS = {
    'SALVAGE': 'Salvage ideas only',
    'GARBAGE': 'Garbage',
    'CLOSED_SOURCE_STOP': 'Closed-source / paid indicator — analysis stopped',
    'COMPLEXITY_OVERLOAD': 'Too complex — simplification required',
}

SALVAGE_KIND_LABELS = {
    'producer': 'Signal producer',
    'entry_gate': 'Entry gate',
    'guard': 'Guard / filter',
    'confirmation': 'Confirmation',
    'exit_rule': 'Exit rule',
    'sl_tp_method': 'Stop-loss / take-profit method',
    'trailing_be_method': 'Trailing / break-even method',
    'money_management': 'Money management',
}

REFERENCE_BASENAMES = [
    '00_raw_quantlens_report.md',
    '01_candidate_metadata.yaml',
    '02_codex_triage.md',
    '03_mtc_module_mapping.md',
    '04_experiment_plan.md',
    '05_risks_and_unknowns.md',
    '06_next_action.md',
]


def _safe_int(val: Any) -> int | None:
    try:
        return int(val)
    except Exception:
        return None


def _commercial_band(score: int | None) -> str:
    if score is None:
        return 'Unknown'
    if score == 0:
        return 'Rejected'
    if score <= 2:
        return 'Weak'
    if score <= 4:
        return 'Plausible but unproven'
    if score <= 6:
        return 'Interesting'
    if score <= 8:
        return 'Strong evidence'
    return 'Strong evidence'


def _stop_state(decision: Any, closed_source_risk: Any, complexity_score: Any) -> str | None:
    if str(closed_source_risk).upper() == 'HIGH':
        return 'CLOSED_SOURCE_STOP'
    if complexity_score is not None and int(complexity_score) >= 8:
        return 'COMPLEXITY_OVERLOAD'
    if str(decision).upper() == 'GARBAGE':
        return 'GARBAGE'
    return None


def _testability(closed_source_risk: Any, decision: Any, risk_management_quality: Any) -> str:
    # Heuristic until structured rule-completeness data exists
    if str(closed_source_risk).upper() == 'HIGH':
        return 'Blocked by closed-source dependency'
    if str(decision).upper() == 'GARBAGE':
        return 'Not testable'
    if str(risk_management_quality).upper() in ('FULL', 'COMPLETE', 'GOOD'):
        return 'Fully testable'
    return 'Partially testable'


def read_quantlens_candidate(candidate_dir: Path) -> dict:
    meta_path = candidate_dir / '01_candidate_metadata.yaml'
    raw = None
    if yaml is not None and meta_path.exists():
        try:
            raw = yaml.safe_load(meta_path.read_text(encoding='utf-8'))
            if isinstance(raw, dict):
                raw = _jsonable(raw)
            else:
                raw = None
        except Exception:
            raw = None

    y = raw or {}
    cid = y.get('candidate_id') or candidate_dir.name
    decision = y.get('quantlens_decision')
    cscore = _safe_int(y.get('commercial_value_score'))
    cxscore = _safe_int(y.get('complexity_score'))
    cs_risk = y.get('closed_source_risk')
    rmq = y.get('risk_management_quality')

    kinds = y.get('candidate_kind') or {}
    if isinstance(kinds, list):
        salvageable = [
            {'category': str(k), 'label': SALVAGE_KIND_LABELS.get(str(k), str(k))}
            for k in kinds if k
        ]
    elif isinstance(kinds, dict):
        salvageable = [
            {'category': k, 'label': SALVAGE_KIND_LABELS.get(k, k)}
            for k, v in kinds.items() if v
        ]
    else:
        salvageable = []

    ref_files = {}
    for bn in REFERENCE_BASENAMES:
        fp = candidate_dir / bn
        if fp.exists():
            ref_files[bn] = fp.relative_to(default_mcc_root()).as_posix()

    return {
        'candidate_id': cid,
        'video_title': y.get('video_title'),
        'source_url': y.get('source_url'),
        'quantlens_decision': decision,
        'stop_state': _stop_state(decision, cs_risk, cxscore),
        'quantlens_verdict': {
            'decision_label': DECISION_LABELS.get(str(decision).upper(), decision),
            'strategy_type': y.get('strategy_type'),
            'instrument_fit': y.get('market_type') or 'UNKNOWN',
            'primary_timeframe': y.get('primary_timeframe') or 'UNKNOWN',
            'commercial_value': {'score': cscore, 'band': _commercial_band(cscore)},
            'complexity': {'score': cxscore, 'overload': bool(cxscore is not None and cxscore >= 8)},
            'testability': _testability(cs_risk, decision, rmq),
            'risks': {
                'repaint': y.get('repaint_risk'),
                'lookahead': y.get('lookahead_risk'),
                'overfit': y.get('overfit_risk'),
                'closed_source': cs_risk,
                'risk_management_quality': rmq,
            },
            'recommended_next_step': y.get('recommended_next_step'),
        },
        'salvageable_ideas': salvageable,
        'human_next_action': y.get('recommended_next_step'),
        'reference_files': ref_files,
        'raw': raw,
    }


def build_quantlens(mcc_root: str | Path | None = None) -> dict:
    root = canonicalize(mcc_root or default_mcc_root())
    ql_root = default_quantlens_root(root)
    seen: dict[str, dict] = {}
    sources: list[str] = []

    salvage_root = ql_root / '03_SALVAGE_IDEAS'
    if salvage_root.exists():
        sources.append('03_QUANTLENS/03_SALVAGE_IDEAS')
        for d in sorted(salvage_root.iterdir()):
            if d.is_dir() and (d / '01_candidate_metadata.yaml').exists():
                c = read_quantlens_candidate(d)
                seen[c.get('candidate_id', '')] = c

    strategies_root = ql_root / 'strategies'
    if strategies_root.exists():
        sources.append('03_QUANTLENS/strategies')
        for d in sorted(strategies_root.iterdir()):
            if d.is_dir() and (d / '01_candidate_metadata.yaml').exists():
                c = read_quantlens_candidate(d)
                cid = c.get('candidate_id', '')
                if cid not in seen:
                    seen[cid] = c

    cands = sorted(seen.values(), key=lambda x: x.get('candidate_id', ''))
    return {
        'candidates': cands,
        'count': len(cands),
        'source': ', '.join(sources) if sources else '03_QUANTLENS',
    }
