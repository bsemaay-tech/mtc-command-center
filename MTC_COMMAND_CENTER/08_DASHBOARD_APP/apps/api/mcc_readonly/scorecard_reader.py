from __future__ import annotations

import json
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

    # ---- discover run directories (one level below backtest_root) ----
    # A "run" is any directory that contains a scorecard_v2 sub-directory.
    run_dirs: list[Path] = []
    for item in sorted(backtest_root.iterdir()):
        if item.is_dir():
            sc_dir = item / 'scorecard_v2'
            if sc_dir.is_dir():
                run_dirs.append(item)

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
        if match:
            new_row = dict(row)
            new_row['scorecard_v2'] = match.get('display_card')
            new_row['scorecard_v2_cases'] = match.get('cards')
            out.append(new_row)
        else:
            out.append(dict(row))
    return out
