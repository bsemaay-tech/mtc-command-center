"""WP-P0-31 Milestone 2 (SEED_IMPORT) — DESIGN DRY RUN on scratch copies of the legacy stores.

Authority: OD-20260916-P031-M2-Q1-Q6-1 (Q1 A: design half only). This script WRITES NO LEDGER RECORD and
touches no repository file: it reads the scratch copies under ./scratch_stores, applies the one-time mapping
table of WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md section 4 (4a ladder, 4b labels, 4c scattered stores) under the
owner's answers (Q2 A `MIGRATED_2026` non-authoritative; Q3 A composite fold; Q4 A lower state on a two-writer
disagreement; Q5 A `UNKNOWN` + listed), and emits the SHAPE of the reconciliation report: one terminal disposition
per source row, balanced against a fresh enumeration, conflicts, and the `UNKNOWN` targets that would block M3.

`--table-extension 4a_prime.json` applies a PROPOSED extension of table 4a (owner question, not ruled) and labels
every output of that run `WHAT_IF_NOT_RULED`. `--plant` adds one synthetic row to a scratch copy of the registry
before enumerating, to show that the balance check detects a source row the census was not told about.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORES = HERE / "scratch_stores"
RULING = "OD-20260916-P031-M2-Q1-Q6-1"
SOURCE_KIND = "MIGRATED_2026"  # Q2 A; authoritative = 0 kept
NO_STATE = None

# --- table 4a as written in the fold (rank = row order; the rules doc's 7-stage ladder order) ---
LADDER_4A = [  # (old value, new state, tag)
    ("REJECTED", "REJECTED", None),
    ("KEEP_AS_RESEARCH_NOTE", "PARKED", "legacy:research_note"),
    ("PROMOTE_TO_SANDBOX", "CANDIDATE", "legacy:sandbox"),
    ("PROMOTE_TO_FORWARD_PAPER_TRADE", "CANDIDATE", "legacy:forward_paper_aspirant"),
    ("MTC_ENGINE_VALIDATED", "CANDIDATE", "legacy:mtc_engine_validated"),
    ("PROMOTE_TO_PARITY_CANDIDATE", "CANDIDATE", "legacy:parity_candidate"),
    ("APPROVED_FOR_MTC_V2_INTEGRATION", "CANDIDATE", "legacy:approved_v2_integration"),
]
RANK_4A = {old: i for i, (old, _, _) in enumerate(LADDER_4A)}
MAP_4A = {old: (state, tag) for old, state, tag in LADDER_4A}
# Q4 A "lower of the two mapped states": ordering assumed for the dry run (owner question Q12 below)
STATE_RANK = {"REJECTED": 0, "PARKED": 1, "CAPTURED": 2, "TRIAGED": 3, "CANDIDATE": 4}
ADVISORY_4C = {
    "NEEDS_CLARIFICATION": "advisory:needs_clarification",
    "RESEARCH_ONLY": "advisory:research_only",
    "SALVAGE": "advisory:salvage",
}
LABELS_4B = {
    "TRUE_ALPHA_CANDIDATE", "BENCHMARK_BEATER", "BETA_DISGUISED_AS_ALPHA", "REGIME_SPECIFIC_EDGE",
    "OVERFIT_SUSPECT", "STATISTICALLY_UNCONFIRMED", "INSUFFICIENT_TRADES", "NO_DATA", "REJECTED",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def components(value) -> list[str] | None:
    """A ladder value as its components: `A|B` strings and JSON lists are composites; None stays None."""
    if value is None:
        return None
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [part for part in value.split("|") if part]
    return [repr(value)]


def map_ladder(parts: list[str], table: dict) -> tuple[str | None, list[str], list[str], list[str]]:
    """(state, tags, mapped components, unmapped components) under table 4a (+ an optional extension)."""
    mapped, unmapped, tags = [], [], []
    for part in parts:
        if part in table:
            mapped.append(part)
            if table[part][1]:
                tags.append(table[part][1])
        else:
            unmapped.append(part)
    if unmapped or not mapped:
        return NO_STATE, tags, mapped, unmapped
    # Q3 A: the highest-ranked component's row decides the state; every component's tag is carried
    best = max(mapped, key=lambda p: RANK_4A.get(p, -1))
    return table[best][0], sorted(set(tags)), mapped, unmapped


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="write-once output directory (under this design folder)")
    ap.add_argument("--table-extension", help="PROPOSED extension of table 4a as JSON {old: [state, tag]}")
    ap.add_argument("--plant", action="store_true", help="plant one synthetic registry row before enumerating")
    ap.add_argument("--census", help="the census JSON to balance against (rows_censused per store)")
    args = ap.parse_args(argv)
    out = Path(args.out)
    if out.exists():
        print("REFUSE: output exists (write-once)", out)
        return 3
    table = dict(MAP_4A)
    label = "DESIGN_DRY_RUN_NOT_A_LEDGER_WRITE"
    if args.table_extension:
        ext = load(Path(args.table_extension))
        for old, (state, tag) in ext.items():
            table[old] = (state, tag)
            RANK_4A.setdefault(old, -1)  # extension rows rank below the ruled ladder unless the owner ranks them
        label = "WHAT_IF_NOT_RULED"
    census = load(Path(args.census)) if args.census else None

    srr_path = STORES / "STRATEGY_RESEARCH_REGISTRY.json"
    srr = load(srr_path)
    if args.plant:
        srr = copy.deepcopy(srr)
        srr["strategies"].append({"strategy_id": "STG999", "current_status": "PROMOTE_TO_SANDBOX", "strategy_name": "PLANTED ROW (dry-run fixture)"})
    vlr = load(STORES / "VARIANT_LOG_REGISTRY.json")
    tcr = load(STORES / "TRIAGE_CANDIDATE_REGISTRY.json")
    aqv = load(STORES / "AI_QUANTLENS_VERDICT_REGISTRY.json")
    specs = {}
    for p in sorted((STORES / "producer_specs").rglob("producer_spec.json")):
        specs[p.relative_to(STORES / "producer_specs").as_posix()] = load(p)

    dispositions: list[dict] = []
    seeds: dict[str, dict] = {}  # candidate_id -> seed record shape

    def dispose(**row):
        dispositions.append(row)

    # ---- STRATEGY_RESEARCH_REGISTRY.current_status (joined with producer_spec.promotion_status by folder STG code)
    ps_by_stg: dict[str, tuple[str, dict]] = {}
    for rel, spec in specs.items():
        m = re.match(r".*/(STG\d+)_", rel)
        if m:
            ps_by_stg[m.group(1)] = (rel, spec)
    seen_ps: set[str] = set()
    for s in srr["strategies"]:
        stg = s.get("strategy_id")
        reg_value = s.get("current_status")
        reg_parts = components(reg_value) or []
        reg_state, reg_tags, reg_mapped, reg_unmapped = map_ladder(reg_parts, table)
        ps_rel, ps_spec = ps_by_stg.get(stg, (None, None))
        ps_value = ps_spec.get("promotion_status") if ps_spec else None
        ps_parts = components(ps_value)
        prov = {
            "source_kind": SOURCE_KIND, "authoritative": 0,
            "STRATEGY_RESEARCH_REGISTRY.json": {"row": stg, "field": "current_status", "value": reg_value},
        }
        if ps_rel:
            seen_ps.add(ps_rel)
            prov[ps_rel] = {"field": "promotion_status", "value": ps_value, "candidate_id_alias": ps_spec.get("candidate_id")}
        tags = list(reg_tags)
        if reg_state is NO_STATE:
            dispose(source="STRATEGY_RESEARCH_REGISTRY.json", row=stg, field="current_status", value=reg_value,
                    disposition="UNKNOWN", reason=f"value outside table 4a: {reg_unmapped or reg_parts}",
                    also=ps_rel, also_value=ps_value)
            continue
        state = reg_state
        conflict = None
        if ps_parts is not None:
            ps_state, ps_tags, ps_mapped, ps_unmapped = map_ladder(ps_parts, table)
            if ps_state is NO_STATE:
                dispose(source="STRATEGY_RESEARCH_REGISTRY.json", row=stg, field="current_status", value=reg_value,
                        disposition="UNKNOWN", reason=f"the second writer's value is outside table 4a: {ps_unmapped or ps_parts}",
                        also=ps_rel, also_value=ps_value)
                continue
            tags = sorted(set(tags) | set(ps_tags))
            if ps_state != state:
                # Q4 A: migrated-conflict, both values retained, the LOWER mapped state
                conflict = {"registry": (reg_value, reg_state), "producer_spec": (ps_value, ps_state)}
                state = min((state, ps_state), key=lambda st: STATE_RANK[st])
                tags.append("migrated-conflict")
        if reg_value == "REJECTED":
            tags.append("migrated-no-identity")
        seed = {"candidate_id": stg, "record": "SEED_IMPORT", "state": state, "tags": sorted(set(tags)),
                "provenance": prov, "conflict": conflict}
        seeds[stg] = seed
        dispose(source="STRATEGY_RESEARCH_REGISTRY.json", row=stg, field="current_status", value=reg_value,
                disposition="SEEDED", state=state, tags=seed["tags"], conflict=bool(conflict), also=ps_rel, also_value=ps_value)
    for rel, spec in specs.items():
        if rel not in seen_ps:
            dispose(source=rel, row=spec.get("candidate_id"), field="promotion_status", value=spec.get("promotion_status"),
                    disposition="UNKNOWN", reason="producer_spec folder has no STRATEGY_RESEARCH_REGISTRY row (no identity join)")

    # ---- VARIANT_LOG_REGISTRY.promotable -> tag only when True
    for v in vlr["variants"]:
        if v.get("promotable") is True:
            dispose(source="VARIANT_LOG_REGISTRY.json", row=v.get("variant_id"), field="promotable", value=True,
                    disposition="UNKNOWN", reason="tag legacy:promotable needs the variant's FAMILY record; no family identity join is defined")
        else:
            dispose(source="VARIANT_LOG_REGISTRY.json", row=v.get("variant_id"), field="promotable", value=v.get("promotable"),
                    disposition="NOT_SEEDED", reason="promotable is not True: no tag, never a state (table 4c)")

    # ---- TRIAGE_CANDIDATE_REGISTRY -> CAPTURED / TRIAGED funnel seeds
    tcr_ids = set()
    for c in tcr["candidates"]:
        cid = c.get("candidate_id"); tcr_ids.add(cid)
        decision_recorded = False  # no field of the store records an extract-or-decline DECISION (census finding)
        state = "TRIAGED" if decision_recorded else "CAPTURED"
        tags = ["legacy:retriage_eligible"] if c.get("eligible_for_retriage") is True else []
        seeds[cid] = {"candidate_id": cid, "record": "SEED_IMPORT", "state": state, "tags": tags,
                      "provenance": {"source_kind": SOURCE_KIND, "authoritative": 0,
                                     "TRIAGE_CANDIDATE_REGISTRY.json": {"row": cid, "stg_code": c.get("stg_code"),
                                                                        "eligible_for_retriage": c.get("eligible_for_retriage"),
                                                                        "recommended_next_step": c.get("recommended_next_step"),
                                                                        "blocked_reason": c.get("blocked_reason")}},
                      "conflict": None}
        dispose(source="TRIAGE_CANDIDATE_REGISTRY.json", row=cid, field="(decision)", value=None,
                disposition="SEEDED", state=state, tags=tags, conflict=False)

    # ---- AI_QUANTLENS_VERDICT_REGISTRY.decision -> advisory tags on the host record
    for e in aqv["entries"]:
        sid = e.get("strategy_id"); tag = ADVISORY_4C.get(e.get("decision"))
        if tag is None:
            dispose(source="AI_QUANTLENS_VERDICT_REGISTRY.json", row=sid, field="decision", value=e.get("decision"),
                    disposition="UNKNOWN", reason="decision outside table 4c")
        elif sid in seeds:
            seeds[sid]["tags"] = sorted(set(seeds[sid]["tags"]) | {tag})
            seeds[sid]["provenance"]["AI_QUANTLENS_VERDICT_REGISTRY.json"] = {"row": sid, "field": "decision", "value": e.get("decision")}
            dispose(source="AI_QUANTLENS_VERDICT_REGISTRY.json", row=sid, field="decision", value=e.get("decision"),
                    disposition="SEEDED", state=None, tags=[tag], conflict=False, host=sid)
        else:
            dispose(source="AI_QUANTLENS_VERDICT_REGISTRY.json", row=sid, field="decision", value=e.get("decision"),
                    disposition="NOT_SEEDED", reason="advisory tag without a host record (no TRIAGE/registry identity carries this id); never a state")

    # ---- balance: fresh enumeration vs census
    measured = {
        "STRATEGY_RESEARCH_REGISTRY.json": len(srr["strategies"]),
        "producer_spec.json": len(specs),
        "VARIANT_LOG_REGISTRY.json": len(vlr["variants"]),
        "TRIAGE_CANDIDATE_REGISTRY.json": len(tcr["candidates"]),
        "AI_QUANTLENS_VERDICT_REGISTRY.json": len(aqv["entries"]),
    }
    disposed = Counter()
    for d in dispositions:
        src = "producer_spec.json" if d["source"].endswith("producer_spec.json") else d["source"]
        disposed[src] += 1
    # producer_spec rows are disposed inside their registry row (joined) or as UNKNOWN when unjoined
    disposed["producer_spec.json"] += len(seen_ps)
    balance = {}
    for store, n in measured.items():
        censused = (census or {}).get("rows", {}).get(store)
        balance[store] = {"measured_now": n, "disposed": disposed[store], "censused": censused,
                          "every_row_disposed": disposed[store] == n,
                          "matches_census": (censused == n) if censused is not None else None}
    totals = Counter(d["disposition"] for d in dispositions)
    unknown_targets = [d for d in dispositions if d["disposition"] == "UNKNOWN"]
    conflicts = [s for s in seeds.values() if s.get("conflict")]
    report = {
        "report_kind": "P031_M2_RECONCILIATION_REPORT_SHAPE_V0",
        "label": label,
        "ruling": RULING,
        "table_4a_extension": args.table_extension,
        "planted_row": bool(args.plant),
        "sources": {
            "STRATEGY_RESEARCH_REGISTRY.json": sha256(srr_path),
            "VARIANT_LOG_REGISTRY.json": sha256(STORES / "VARIANT_LOG_REGISTRY.json"),
            "TRIAGE_CANDIDATE_REGISTRY.json": sha256(STORES / "TRIAGE_CANDIDATE_REGISTRY.json"),
            "AI_QUANTLENS_VERDICT_REGISTRY.json": sha256(STORES / "AI_QUANTLENS_VERDICT_REGISTRY.json"),
            "producer_spec.json": {rel: sha256(STORES / "producer_specs" / rel) for rel in specs},
        },
        "balance": balance,
        "balanced": all(b["every_row_disposed"] for b in balance.values())
        and all(b["matches_census"] in (True, None) for b in balance.values()),
        "totals": dict(totals),
        "seed_count": len(seeds),
        "seed_state_counts": dict(Counter(s["state"] for s in seeds.values())),
        "conflict_count": len(conflicts),
        "unknown_target_count": len(unknown_targets),
        "unknown_targets": unknown_targets,
        "conflicts": conflicts,
        "dispositions": dispositions,
        "seeds": list(seeds.values()),
        "statement": (
            "Design dry run on scratch copies. No ledger record was written; no repository file was read or "
            "changed by this script. The seed records are the SHAPE the M2 build would write, not records."
        ),
    }
    out.mkdir(parents=True)
    raw = (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    (out / "reconciliation_report.json").write_bytes(raw)
    (out / "reconciliation_report.json.sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n", encoding="ascii")
    print(f"{label} balanced={report['balanced']} seeds={len(seeds)} states={report['seed_state_counts']} "
          f"conflicts={len(conflicts)} unknown={len(unknown_targets)} totals={dict(totals)}")
    for store, b in balance.items():
        print(f"  {store}: measured_now={b['measured_now']} disposed={b['disposed']} censused={b['censused']} "
              f"every_row_disposed={b['every_row_disposed']} matches_census={b['matches_census']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
