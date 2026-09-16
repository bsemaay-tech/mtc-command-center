"""WP-P0-31 M2 design half — source-row CENSUS of the five legacy stores on scratch copies (Q1 A).
Measures rows, value distributions, identity vocabularies and joins; pins the scratch copies by sha256 and
the canonical checkout's blob OIDs. Writes census.json (+ .sha256). No repository write."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORES = HERE / "scratch_stores"
CANON = "C:/LAB/Tradingview_LAB_CLEAN"
LABELS_4B = ["TRUE_ALPHA_CANDIDATE", "BENCHMARK_BEATER", "BETA_DISGUISED_AS_ALPHA", "REGIME_SPECIFIC_EDGE",
             "OVERFIT_SUSPECT", "STATISTICALLY_UNCONFIRMED", "INSUFFICIENT_TRADES", "NO_DATA", "REJECTED"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def git(*args) -> str:
    return subprocess.run(["git", "-C", CANON, "-c", "safe.directory=*", *args], capture_output=True, text=True).stdout.strip()


def main() -> int:
    head = git("rev-parse", "HEAD"); branch = git("rev-parse", "--abbrev-ref", "HEAD")
    srr = load(STORES / "STRATEGY_RESEARCH_REGISTRY.json"); vlr = load(STORES / "VARIANT_LOG_REGISTRY.json")
    tcr = load(STORES / "TRIAGE_CANDIDATE_REGISTRY.json"); aqv = load(STORES / "AI_QUANTLENS_VERDICT_REGISTRY.json")
    specs = {p.relative_to(STORES / "producer_specs").as_posix(): load(p) for p in sorted((STORES / "producer_specs").rglob("producer_spec.json"))}
    stg_of = lambda rel: (re.match(r".*/(STG\d+)_", rel) or [None, None])[1]
    srr_ids = {s["strategy_id"] for s in srr["strategies"]}
    tcr_ids = {c["candidate_id"] for c in tcr["candidates"]}
    tcr_stg = {c.get("stg_code") for c in tcr["candidates"]}
    aqv_ids = [e["strategy_id"] for e in aqv["entries"]]
    def ps_value(d):
        v = d.get("promotion_status"); return "|".join(v) if isinstance(v, list) else v
    pairs = Counter()
    for rel, d in specs.items():
        stg = stg_of(rel)
        if stg in srr_ids:
            reg = next(s["current_status"] for s in srr["strategies"] if s["strategy_id"] == stg)
            pairs[f"{reg} <> {ps_value(d)}"] += 1
    # the nine 4b labels live outside the five stores: count the JSON files in the canonical checkout carrying one
    label_files = 0; label_hits = Counter()
    for p in Path(CANON, "MTC_COMMAND_CENTER").rglob("*.json"):
        s = p.as_posix()
        if "_gemini_packets" in s or "/history/" in s or "/05_REGISTRY/" in s:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        found = [lab for lab in LABELS_4B if f'"{lab}"' in txt]
        if found:
            label_files += 1
            for lab in found: label_hits[lab] += 1
    census = {
        "census_kind": "P031_M2_SOURCE_CENSUS_V0",
        "measured_at_canonical": {"branch": branch, "head": head},
        "scratch_copies": {
            "STRATEGY_RESEARCH_REGISTRY.json": {"sha256": sha256(STORES / "STRATEGY_RESEARCH_REGISTRY.json"), "blob_oid_at_head": git("rev-parse", f"{head}:MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json"), "generated_at": srr.get("generated_at"), "generator": srr.get("generator")},
            "VARIANT_LOG_REGISTRY.json": {"sha256": sha256(STORES / "VARIANT_LOG_REGISTRY.json"), "blob_oid_at_head": git("rev-parse", f"{head}:MTC_COMMAND_CENTER/05_REGISTRY/VARIANT_LOG_REGISTRY.json"), "generated_at": vlr.get("generated_at")},
            "TRIAGE_CANDIDATE_REGISTRY.json": {"sha256": sha256(STORES / "TRIAGE_CANDIDATE_REGISTRY.json"), "blob_oid_at_head": git("rev-parse", f"{head}:MTC_COMMAND_CENTER/05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json"), "generated_at": tcr.get("generated_at"), "generator": tcr.get("generator"), "source_worklist": tcr.get("source_worklist")},
            "AI_QUANTLENS_VERDICT_REGISTRY.json": {"sha256": sha256(STORES / "AI_QUANTLENS_VERDICT_REGISTRY.json"), "blob_oid_at_head": git("rev-parse", f"{head}:MTC_COMMAND_CENTER/05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json"), "generated_at": aqv.get("generated_at"), "model": aqv.get("model")},
            "producer_spec.json": {"files": len(specs), "sha256_of_sorted_sha256s": hashlib.sha256("\n".join(sha256(STORES / "producer_specs" / rel) for rel in specs).encode()).hexdigest()},
        },
        "rows": {
            "STRATEGY_RESEARCH_REGISTRY.json": len(srr["strategies"]),
            "producer_spec.json": len(specs),
            "VARIANT_LOG_REGISTRY.json": len(vlr["variants"]),
            "TRIAGE_CANDIDATE_REGISTRY.json": len(tcr["candidates"]),
            "AI_QUANTLENS_VERDICT_REGISTRY.json": len(aqv["entries"]),
        },
        "fold_counts_vs_measured": {"producer_spec filled": f"fold 44/63 -> measured {sum(1 for d in specs.values() if d.get('promotion_status') is not None)}/{len(specs)}",
                                    "TRIAGE candidates": f"fold 172 -> measured {len(tcr['candidates'])}"},
        "values": {
            "STRATEGY_RESEARCH_REGISTRY.current_status": dict(Counter(s.get("current_status") for s in srr["strategies"])),
            "STRATEGY_RESEARCH_REGISTRY.maturity_level": dict(Counter(s.get("maturity_level") for s in srr["strategies"])),
            "producer_spec.promotion_status": dict(Counter(repr(ps_value(d)) for d in specs.values())),
            "VARIANT_LOG_REGISTRY.promotable": dict(Counter(repr(v.get("promotable")) for v in vlr["variants"])),
            "TRIAGE.recommended_next_step": dict(Counter(c.get("recommended_next_step") for c in tcr["candidates"])),
            "TRIAGE.blocked_reason": dict(Counter(repr(c.get("blocked_reason")) for c in tcr["candidates"])),
            "TRIAGE.eligible_for_retriage": dict(Counter(repr(c.get("eligible_for_retriage")) for c in tcr["candidates"])),
            "TRIAGE.source_quality": dict(Counter(c.get("source_quality") for c in tcr["candidates"])),
            "AI_QUANTLENS.decision": dict(Counter(e.get("decision") for e in aqv["entries"])),
        },
        "identity_vocabularies": {
            "STRATEGY_RESEARCH_REGISTRY.strategy_id": {"form": "STG### (upper)", "unique": len(srr_ids), "sample": sorted(srr_ids)[:3]},
            "producer_spec.candidate_id": {"form": "QL_… / free text (NOT the STG code)", "unique": len({d.get('candidate_id') for d in specs.values()}), "in_registry_ids": sum(1 for d in specs.values() if d.get('candidate_id') in srr_ids), "folder_stg_in_registry": sum(1 for rel in specs if stg_of(rel) in srr_ids)},
            "TRIAGE.candidate_id": {"form": "QLR_<youtube id>", "unique": len(tcr_ids)},
            "TRIAGE.stg_code": {"form": "Stg### (mixed case) — a TRIAGE numbering, NOT the registry's STG### strategies", "unique": len(tcr_stg), "in_registry_ids_exact": sum(1 for s in tcr_stg if s in srr_ids), "in_registry_ids_casefold": sum(1 for s in tcr_stg if s and s.upper() in srr_ids)},
            "AI_QUANTLENS.strategy_id": {"form": "CAND_… / GEN_… / QLR_…", "unique": len(set(aqv_ids)), "in_TRIAGE_candidate_ids": sum(1 for i in aqv_ids if i in tcr_ids), "in_registry_ids": sum(1 for i in aqv_ids if i in srr_ids), "orphans": sorted(i for i in aqv_ids if i not in tcr_ids)},
            "VARIANT_LOG.variant_id": {"form": "NEW_… archetype names; no strategy/family identity field", "unique": len({v.get('variant_id') for v in vlr['variants']})},
        },
        "two_writer_pairs_registry_vs_producer_spec": dict(pairs),
        "labels_4b_outside_the_five_stores": {"json_files_carrying_a_4b_label": label_files, "per_label_file_counts": dict(label_hits),
                                              "note": "table 4b labels live in evaluation artifacts (scorecards/classifications), not in the five stores; a host identity join is undefined"},
    }
    raw = (json.dumps(census, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    (HERE / "census.json").write_bytes(raw)
    (HERE / "census.json.sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n", encoding="ascii")
    print(json.dumps({k: census[k] for k in ("measured_at_canonical", "rows", "fold_counts_vs_measured")}, indent=1))
    print("labels_4b files:", label_files, dict(label_hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
