"""Assemble a Section-16 receipt DRAFT for P012 G5 from reviewer-owned envelopes.

Inputs (all Lead-extracted copies with filenames disjoint from reviewer outputs, R10):
  --packet   packet root (HUNK_INVENTORY.json supplies mechanical hunk fields)
  --item N=path  JSON file holding {"review_disposition":..,"disposition":..,"evidence_paths":[..],"notes":..}
                 for N in 1,3,4,5,6 (extracted verbatim from the reviewer's fenced envelope)
  --hunks path   one or more JSON files, each a list of reviewer-owned hunk classifications:
                 {"index": int, "terminal_class": "DEF"|"SECTION18_SHARED"|"UNDOCUMENTED",
                  "def_ids": [...] | "section18_row": "S18-xx" | "reason": "..."}
  --item2 path   JSON with disposition/evidence_paths/notes for Item 2 (no hunk_coverage; built here)
  --identities path  JSON with the nine reviewed identities (from the R29 request)
  --reviewer path    JSON reviewer block {identity, family, independent_of:[{role,basis},{role,basis}]}
  --out path

The assembler NEVER assigns a semantic class. It refuses on: missing/duplicate hunk index, unknown
class, section18 row whose module pattern does not own the hunk path, served_def_ids not equal to the
design row's served set, unsorted/duplicate def_ids, empty reason, item disposition REFUSED, or any
item with nonempty required_scope_unread. Output carries owner_ratification.ratified=false so it is
structurally INVALID for the gate until an owner act flips it (rule R7).
"""
from __future__ import annotations
import argparse, json, sys, fnmatch
from pathlib import Path, PurePosixPath

VALID_DISP = {"ACCEPTED", "ACCEPTED_WITH_RESIDUAL_RISK"}
CHAIN = ["#5","#6","#7","#8","#9","#10","#11","#12","#12b","#13","#14","#14b","#15","#16","#17","#18","#19","#20","#21","#22","#23","#24","#25","#26","#27","#28","#29","#30","#31","#32","#33","#34","#35","#36","#37","#38","#39"]

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--item", action="append", default=[], help="N=path")
    ap.add_argument("--item2", required=True)
    ap.add_argument("--hunks", action="append", required=True)
    ap.add_argument("--identities", required=True)
    ap.add_argument("--reviewer", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    packet = Path(a.packet)
    inv = load(packet / "HUNK_INVENTORY.json")
    assert inv["total_physical_hunks"] == len(inv["hunks"]) == 218, "inventory hunk count drift"
    rows = {r["row"]: r for r in inv["section18_design_bindings"]}
    errors: list[str] = []

    # reviewer-owned hunk classes
    classes: dict[int, dict] = {}
    for hp in a.hunks:
        for rec in load(hp):
            i = int(rec["index"])
            if i in classes: errors.append(f"duplicate class for hunk {i} ({hp})"); continue
            classes[i] = rec
    missing = [i for i in range(218) if i not in classes]
    if missing: errors.append(f"unclassified hunks: {missing}")

    hunks_out = []
    for h in inv["hunks"]:
        i = h["index"]; rec = classes.get(i)
        if rec is None: continue
        base = {"path": h["path"], "old_start": h["old_start"], "old_count": h["old_count"],
                "new_start": h["new_start"], "new_count": h["new_count"], "hunk_sha256": h["raw_hunk_sha256"]}
        tc = rec.get("terminal_class")
        if tc == "DEF":
            ids = rec.get("def_ids")
            if not ids or ids != sorted(set(ids)): errors.append(f"hunk {i}: def_ids must be nonempty sorted unique: {ids}")
            base.update(terminal_class="DEF", def_ids=ids)
        elif tc == "SECTION18_SHARED":
            row = rec.get("section18_row"); r = rows.get(row)
            if r is None: errors.append(f"hunk {i}: unknown section18 row {row}"); continue
            if not any(fnmatch.fnmatch(h["path"], pat) or h["path"] == pat for pat in r["module_patterns"]):
                errors.append(f"hunk {i}: row {row} does not own path {h['path']} (patterns {r['module_patterns']})")
            served = rec.get("served_def_ids", r["served_def_ids"])
            if served != r["served_def_ids"]: errors.append(f"hunk {i}: served_def_ids {served} != design row {row} set {r['served_def_ids']}")
            base.update(terminal_class="SECTION18_SHARED", section18_row=row, served_def_ids=r["served_def_ids"])
        elif tc == "UNDOCUMENTED":
            if not rec.get("reason"): errors.append(f"hunk {i}: UNDOCUMENTED without reason")
            base.update(terminal_class="UNDOCUMENTED", reason=rec.get("reason", ""))
            errors.append(f"hunk {i}: UNDOCUMENTED class refuses acceptance by design")
        else:
            errors.append(f"hunk {i}: unknown terminal_class {tc}")
        hunks_out.append(base)

    s18 = []
    for row, r in sorted(rows.items()):
        idx = [h_["hunk_sha256"] for h_ in hunks_out]  # placeholder to keep order stable
        indices = [inv["hunks"][k]["index"] for k, h_ in enumerate(hunks_out) if h_.get("section18_row") == row]
        s18.append({"row": row, "served_def_ids": r["served_def_ids"], "hunk_indices": indices})

    changed_paths = [{"path": c["path"], "hunk_count": c["hunk_count"], "hunk_indices": c["hunk_indices"], "hunk_sha256s": c["raw_hunk_sha256s"]} for c in inv["changed_paths"]]

    def abs_evidence(paths, label):
        # The gate resolves evidence_paths as absolute paths or relative to the source root; reviewer
        # envelopes cite packet-relative paths. Rewrite each to the absolute packet path (the bytes the
        # reviewer actually read) and refuse if it does not exist. Never invents a path.
        out = []
        for p in paths:
            q = Path(p)
            cand = q if q.is_absolute() else (packet / Path(*PurePosixPath(p).parts))
            if not cand.exists(): errors.append(f"{label}: evidence path missing in packet: {p}")
            out.append(str(cand.resolve()).replace("\\", "/"))
        return out

    items = {}
    for spec in a.item:
        n, p = spec.split("=", 1); e = load(p)
        disp = e.get("review_disposition") or e.get("disposition")
        if disp not in VALID_DISP: errors.append(f"item {n}: disposition {disp} does not accept")
        if e.get("required_scope_unread"): errors.append(f"item {n}: required_scope_unread nonempty: {e['required_scope_unread']}")
        items[n] = {"disposition": disp, "evidence_paths": abs_evidence(e["evidence_paths"], f"item {n}"), "notes": e["notes"]}
    e2 = load(a.item2)
    disp2 = e2.get("review_disposition") or e2.get("disposition")
    if disp2 not in VALID_DISP: errors.append(f"item 2: disposition {disp2} does not accept")
    items["2"] = {"disposition": disp2, "evidence_paths": abs_evidence(e2["evidence_paths"], "item 2"), "notes": e2["notes"],
                  "hunk_coverage": {"schema": "P012_KERNEL_HUNK_COVERAGE_V2", "base_commit": inv["base_commit"], "reviewed_head": inv["reviewed_head"],
                                    "diff_command": inv["diff_command"], "diff_sha256": inv["diff_sha256"], "total_changed_paths": inv["total_changed_paths"],
                                    "total_changed_files": inv["total_changed_files"], "changed_paths": changed_paths, "section18_coverage": s18, "hunks": hunks_out}}
    for n in "123456":
        if n not in items: errors.append(f"item {n} missing")

    receipt = {"schema": "P012_SEMANTIC_COVERAGE_REVIEW_V2", "reviewer": load(a.reviewer), "reviewed_identities": load(a.identities),
               "items": {n: items[n] for n in "123456" if n in items}, "unresolved_items": [],
               "owner_ratification": {"chain": CHAIN, "ratified": False}, "signed_at": "UNSIGNED_DRAFT_NOT_A_DATE_TIME"}
    Path(a.out).write_bytes((json.dumps(receipt, indent=2, ensure_ascii=False) + chr(10)).encode("utf-8"))  # LF only, final LF, no BOM (gate load_json_exact)
    print(f"wrote {a.out}; hunks classified {len(hunks_out)}/218; errors {len(errors)}")
    for e in errors: print("REFUSE:", e)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
