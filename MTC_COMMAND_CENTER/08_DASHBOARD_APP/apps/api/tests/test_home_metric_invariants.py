"""Home metric invariant guard.

Mirrors the canonical strategy-universe aggregation implemented in
`apps/web/app.js` (canonicalStrategyIds / orphanScorecardIds / strategyMetrics).
There is no JS test harness in this repo, so this Python test re-implements the
same contract over synthetic snapshot data to prevent regressions where Home shows
raw scorecard-row counts as strategy-level counts.

Invariant: no strategy-level count may exceed Total Strategies, and Total Strategies
is the canonical pipeline (fallback registry) universe — scorecard-only ids are NOT
counted as strategies.

If the JS aggregation changes, update this mirror accordingly.
"""

from __future__ import annotations

import unittest


def _base(x) -> str:
    return str(x or "").split("|")[0]


def _is_pass(s) -> bool:
    t = str(s or "").lower()
    return "pass" in t or t in ("ok", "accepted", "certified", "done")


def _is_fail(s) -> bool:
    return "fail" in str(s or "").lower()


def _row_id(r: dict) -> str:
    return r.get("id") or r.get("strategy_id") or r.get("candidate_id") or r.get("base_strategy_id") or ""


def _card_id(c: dict) -> str:
    return _base(c.get("base_strategy_id") or c.get("strategy_id"))


def canonical_ids(snap: dict) -> list[str]:
    rows = (snap.get("candidate_pipeline") or {}).get("rows") or []
    ids = {_base(_row_id(r)) for r in rows if _base(_row_id(r))}
    if not ids:  # fallback: registry candidates only when pipeline unavailable
        reg = snap.get("strategy_registry") or {}
        for r in (reg.get("candidates") or []) + (reg.get("strategies") or []):
            b = _base(_row_id(r))
            if b:
                ids.add(b)
    return sorted(ids)


def orphan_ids(snap: dict) -> list[str]:
    canon = set(canonical_ids(snap))
    cards = (snap.get("scorecards") or {}).get("cards") or []
    return sorted({_card_id(c) for c in cards if _card_id(c) and _card_id(c) not in canon})


def _cards_for(snap, sid):
    return [c for c in ((snap.get("scorecards") or {}).get("cards") or []) if _card_id(c) == sid]


def _row_for(snap, sid):
    for r in (snap.get("candidate_pipeline") or {}).get("rows") or []:
        if _base(_row_id(r)) == sid:
            return r
    return None


def _gate_statuses(snap, sid, key):
    out = []
    r = _row_for(snap, sid)
    st = ((r or {}).get("scorecard_v2") or {}).get("gate_summary", {}).get("statuses", {}) if r else {}
    if st.get(key) is not None:
        out.append(st[key])
    for c in _cards_for(snap, sid):
        s = (c.get("gate_summary") or {}).get("statuses", {}).get(key)
        if s is not None:
            out.append(s)
    return out


def _gate_pass(snap, sid, key):
    return any(_is_pass(s) for s in _gate_statuses(snap, sid, key))


def _gate2_pass(snap, sid):
    if _gate_pass(snap, sid, "gate2"):
        return True
    return any((c.get("gate2") or {}).get("score") is not None and float(c["gate2"]["score"]) >= 80 for c in _cards_for(snap, sid))


def _gate2_failed(snap, sid):
    sts = _gate_statuses(snap, sid, "gate2")
    if not sts or _gate2_pass(snap, sid):
        return False
    return any(_is_fail(s) for s in sts)


def _promotable(snap, sid):
    r = _row_for(snap, sid)
    if r and (r.get("scorecard_v2") or {}).get("gate_summary", {}).get("promotable"):
        return True
    return any((c.get("gate_summary") or {}).get("promotable") for c in _cards_for(snap, sid))


def strategy_metrics(snap: dict) -> dict:
    ids = canonical_ids(snap)
    return {
        "total": len(ids),
        "g1": sum(_gate_pass(snap, i, "gate1") for i in ids),
        "g1b": sum(_gate_pass(snap, i, "gate1B") for i in ids),
        "g2": sum(_gate2_pass(snap, i) for i in ids),
        "g2f": sum(_gate2_failed(snap, i) for i in ids),
        "paper": sum(_promotable(snap, i) for i in ids),
    }


def _snap():
    """Synthetic snapshot: 2 canonical pipeline strategies + 1 orphan scorecard id."""
    return {
        "candidate_pipeline": {"rows": [
            {"id": "QL_A", "scorecard_v2": {"gate_summary": {"statuses": {"gate1": "OK", "gate1B": "OK", "gate2": "FAIL"}}}},
            {"id": "QL_B", "scorecard_v2": {"gate_summary": {"statuses": {"gate1": "OK"}, "promotable": True}}},
        ]},
        "strategy_registry": {"candidates": [{"id": "QL_A"}, {"id": "QL_B"}]},
        "scorecards": {"cards": [
            {"base_strategy_id": "QL_A", "gate_summary": {"statuses": {"gate1": "OK", "gate2": "FAIL"}}, "gate2": {"score": 40}},
            {"base_strategy_id": "QL_B", "gate_summary": {"statuses": {"gate1": "OK"}}, "gate2": {"score": 85}},
            # orphan: present in scorecards, absent from pipeline/registry
            {"base_strategy_id": "QL_ORPHAN", "gate_summary": {"statuses": {"gate1": "OK", "gate2": "OK"}}, "gate2": {"score": 90}},
        ]},
    }


class HomeMetricInvariantTests(unittest.TestCase):
    def test_total_is_canonical_not_unioned(self):
        snap = _snap()
        self.assertEqual(strategy_metrics(snap)["total"], 2)  # QL_A, QL_B only

    def test_orphan_ids_excluded_from_total_listed_separately(self):
        snap = _snap()
        self.assertEqual(orphan_ids(snap), ["QL_ORPHAN"])
        self.assertNotIn("QL_ORPHAN", canonical_ids(snap))

    def test_orphan_gate1_pass_not_counted_as_strategy(self):
        # QL_ORPHAN passes gate1 + gate2 but must not inflate strategy-level counts.
        sm = strategy_metrics(_snap())
        self.assertEqual(sm["g1"], 2)   # QL_A, QL_B (not orphan)
        self.assertEqual(sm["g2"], 1)   # QL_B (benchmark>=80); QL_A fails; orphan excluded

    def test_no_strategy_level_count_exceeds_total(self):
        sm = strategy_metrics(_snap())
        for k in ("g1", "g1b", "g2", "g2f", "paper"):
            self.assertLessEqual(sm[k], sm["total"], f"{k} exceeds total")

    def test_registry_fallback_when_pipeline_empty(self):
        snap = _snap()
        snap["candidate_pipeline"]["rows"] = []
        self.assertEqual(set(canonical_ids(snap)), {"QL_A", "QL_B"})  # from registry


if __name__ == "__main__":
    unittest.main()
