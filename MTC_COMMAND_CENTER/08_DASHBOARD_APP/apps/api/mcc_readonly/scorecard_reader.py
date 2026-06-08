from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, default_quantlens_root


def build_scorecards(mcc_root: str | Path | None = None) -> dict[str, Any]:
    """Read-only discovery of all scorecard_v2 JSON files under
    ``03_QUANTLENS/05_BACKTEST_RESULTS``.

    Returns
    -------
    dict with keys:
        count, source, runs, cards, by_strategy
    where *by_strategy* maps ``base_strategy_id`` →
    ``{'display_card': ..., 'cards': [...]}``.
    """
    root = canonicalize(mcc_root or default_mcc_root())
    backtest_root = default_quantlens_root(root) / '05_BACKTEST_RESULTS'

    if not backtest_root.exists():
        return {
            'count': 0,
            'source': '03_QUANTLENS/05_BACKTEST_RESULTS',
            'runs': [],
            'cards': [],
            'by_strategy': {},
        }

    # ---- discover run directories ----
    # A "run" is any directory that contains a scorecard_v2 sub-directory.
    run_dirs = _discover_scorecard_run_dirs(backtest_root)

    # Also scan 03_STATUS for readiness-validated scorecard sets
    status_root = root / '03_STATUS'
    if status_root.exists():
        for item in sorted(status_root.iterdir()):
            if item.is_dir():
                sc_dir = item / 'scorecard_v2'
                if sc_dir.is_dir() and item not in run_dirs:
                    run_dirs.append(item)

    runs: list[dict[str, Any]] = []
    all_cards: list[dict[str, Any]] = []
    bad_json_count = 0

    for run_dir in run_dirs:
        sc_dir = run_dir / 'scorecard_v2'
        run_name = run_dir.name
        run_cards: list[dict[str, Any]] = []

        for sc_file in sorted(sc_dir.glob('*.scorecard.json')):
            try:
                raw = json.loads(sc_file.read_text(encoding='utf-8'))
            except Exception:
                bad_json_count += 1
                continue

            # Only accept scorecard_version == 'v2'
            if not isinstance(raw, dict) or raw.get('scorecard_version') != 'v2':
                continue

            card = _normalize_scorecard(raw, run_dir, sc_file, root)
            if card:
                run_cards.append(card)

        if run_cards:
            runs.append({
                'run_name': run_name,
                'run_path': run_dir.relative_to(root).as_posix(),
                'card_count': len(run_cards),
            })
            all_cards.extend(run_cards)

    # ---- deduplicate by strategy across runs: newest run last preferred ----
    by_strategy: dict[str, list[dict[str, Any]]] = {}
    for card in all_cards:
        base = card.get('base_strategy_id', '')
        if not base:
            continue
        by_strategy.setdefault(base, []).append(card)

    # For each base strategy, pick display_card deterministically:
    #   prefer highest gate2.score among cards with numeric gate2 score,
    #   else first sorted card.
    by_strategy_out: dict[str, dict[str, Any]] = {}
    for base_id, cards in by_strategy.items():
        # Since we iterate run_dirs in sorted order, later runs append later.
        # We already have the "newest run last" effect from sorted iteration.
        display = _pick_display_card(cards)
        by_strategy_out[base_id] = {
            'display_card': display,
            'cards': cards,
        }

    return {
        'count': len(all_cards),
        'source': '03_QUANTLENS/05_BACKTEST_RESULTS',
        'runs': runs,
        'cards': all_cards,
        'by_strategy': by_strategy_out,
        'diagnostics': {
            'bad_json_skipped': bad_json_count,
        },
    }


def _discover_scorecard_run_dirs(backtest_root: Path) -> list[Path]:
    """Return directories that directly own scorecard_v2 artifacts."""

    run_dirs: list[Path] = []
    seen: set[Path] = set()
    for sc_dir in sorted(backtest_root.rglob('scorecard_v2')):
        if not sc_dir.is_dir():
            continue
        run_dir = sc_dir.parent
        if run_dir in seen:
            continue
        seen.add(run_dir)
        run_dirs.append(run_dir)
    return run_dirs


def _normalize_scorecard(
    raw: dict[str, Any],
    run_dir: Path,
    sc_file: Path,
    mcc_root: Path,
) -> dict[str, Any] | None:
    """Parse one scorecard JSON into a stable normalised shape."""

    strategy_id = raw.get('strategy_id', '')
    if not strategy_id:
        return None

    parts = strategy_id.split('|')
    base_strategy_id = parts[0].strip() if parts else strategy_id
    symbol = parts[1].strip() if len(parts) > 1 else ''
    timeframe = parts[2].strip() if len(parts) > 2 else ''

    # Normalize gate_summary
    gate_summary_raw = raw.get('gate_summary') or {}
    gate_summary = {
        'statuses': gate_summary_raw.get('statuses') or {},
        'blocking': gate_summary_raw.get('blocking') or [],
        'promotable': gate_summary_raw.get('promotable'),
    }

    return {
        'strategy_id': strategy_id,
        'base_strategy_id': base_strategy_id,
        'symbol': symbol,
        'timeframe': timeframe,
        'run_id': run_dir.name,
        'run_name': run_dir.name,
        'source_path': sc_file.relative_to(mcc_root).as_posix(),
        'updated_at': _timestamp(sc_file.stat().st_mtime),
        'scorecard_version': raw.get('scorecard_version'),
        'gate_summary': gate_summary,
        'gate1': raw.get('gate1'),
        'gate1B': raw.get('gate1B'),
        'gate2': raw.get('gate2'),
        'gate3': raw.get('gate3'),
        'flags': raw.get('flags') or [],
        'notes': raw.get('notes', ''),
    }


def _pick_display_card(cards: list[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic display card selection.

    Prefer highest ``gate2.score`` among cards with a numeric gate2 score,
    else the first card in list order (which is already sorted by run, then
    filename).
    """
    scored = []
    for c in cards:
        g2 = c.get('gate2') or {}
        s = g2.get('score')
        if s is not None and isinstance(s, (int, float)):
            scored.append((s, c))
    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]
    # Fallback: first card (already deterministically sorted)
    return cards[0]


def build_canonical_display_row(
    row: dict[str, Any],
    scorecard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the UI-36 canonical display object for one strategy row.

    Precedence is ``scorecard_v2 > stage > legacy``: scorecard_v2 is the
    authority for backtest status, Gate 2, promotability, blocking, and
    evidence. Pipeline stage fields and legacy audit/MTC_V2 fields stay on the
    raw row for compatibility, but they are not authoritative for these
    canonical display values.
    """
    card = scorecard if isinstance(scorecard, dict) else None
    gate2 = card.get('gate2') if card else None
    if not isinstance(gate2, dict):
        gate2 = {}
    gate_summary = card.get('gate_summary') if card else None
    if not isinstance(gate_summary, dict):
        gate_summary = {}

    defined_tf = _string_value(row.get('timeframe'))
    tested_tf = _tested_timeframe(card)
    gate2_score = _number_value(gate2.get('score'))
    gate2_status = _gate2_status(gate2, gate_summary)
    gate2_band = _gate2_band(gate2_score)
    promotable = _bool_value(gate_summary.get('promotable'))
    blocking = gate_summary.get('blocking') if isinstance(gate_summary.get('blocking'), list) else []

    return {
        'defined_tf': defined_tf,
        'tested_tf': tested_tf,
        'tf_mismatch': bool(
            defined_tf
            and tested_tf
            and defined_tf.strip().lower() != tested_tf.strip().lower()
        ),
        'backtest_status': _canonical_backtest_status(card, gate2_status),
        'gate2_score': gate2_score,
        'gate2_status': gate2_status,
        'gate2_band': gate2_band,
        'promotable': promotable,
        'blocking': blocking,
        'evidence_level': _canonical_evidence_level(card, promotable, gate2_status, gate2_band),
    }


def _tested_timeframe(card: dict[str, Any] | None) -> str:
    if not card:
        return ''
    strategy_id = _string_value(card.get('strategy_id'))
    parts = strategy_id.split('|') if strategy_id else []
    if len(parts) > 2 and parts[2].strip():
        return parts[2].strip()
    return _string_value(card.get('timeframe'))


def _gate2_status(gate2: dict[str, Any], gate_summary: dict[str, Any]) -> str:
    status = _string_value(gate2.get('status'))
    if not status:
        statuses = gate_summary.get('statuses')
        if isinstance(statuses, dict):
            status = _string_value(statuses.get('gate2'))
    return status.upper() if status else 'UNKNOWN'


def _gate2_band(score: float | int | None) -> str:
    if score is None:
        return 'UNKNOWN'
    if score >= 75:
        return 'PASS'
    return 'FAIL'


def _canonical_backtest_status(card: dict[str, Any] | None, gate2_status: str) -> str:
    if not card:
        return 'NO_SCORECARD'
    if gate2_status and gate2_status != 'UNKNOWN':
        return gate2_status
    return 'UNKNOWN'


def _canonical_evidence_level(
    card: dict[str, Any] | None,
    promotable: bool,
    gate2_status: str,
    gate2_band: str,
) -> str:
    if not card:
        return 'no_scorecard'
    if promotable:
        return 'promotable'
    status = gate2_status.upper()
    if status == 'PASS':
        return 'gate2_pass'
    if status == 'FAIL':
        return 'gate2_fail'
    if status in {'INCOMPLETE', 'PENDING'}:
        return 'gate2_incomplete'
    if gate2_band == 'PASS':
        return 'gate2_pass'
    if gate2_band == 'FAIL':
        return 'gate2_fail'
    return 'scorecard_unscored'


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        return value.strip().lower() in {'1', 'true'}
    return False


def _number_value(value: Any) -> float | int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def _string_value(value: Any) -> str:
    return str(value).strip() if value is not None else ''


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def attach_scorecards_to_rows(
    rows: list[dict[str, Any]],
    scorecards: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return new row dicts with **scorecard_v2** and
    **scorecard_v2_cases** attached when the row ``id`` matches a
    ``base_strategy_id`` in *scorecards*.  Input *rows* are never mutated.
    """
    by_strategy = scorecards.get('by_strategy') or {}
    out: list[dict[str, Any]] = []
    for row in rows:
        row_id = row.get('id', '')
        match = by_strategy.get(row_id) if row_id else None
        display_card = match.get('display_card') if match else None
        if match:
            new_row = dict(row)
            new_row['scorecard_v2'] = display_card
            new_row['scorecard_v2_cases'] = match.get('cards')
        else:
            new_row = dict(row)
        new_row['canonical'] = build_canonical_display_row(new_row, display_card)
        out.append(new_row)
    return out
