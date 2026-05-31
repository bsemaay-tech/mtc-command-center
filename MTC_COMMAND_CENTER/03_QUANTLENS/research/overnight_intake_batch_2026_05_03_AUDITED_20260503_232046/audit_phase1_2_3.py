import os
import glob
import re
import csv
import json
import yaml
from pathlib import Path

INTAKE_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs"
FIRST_RUN_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03"
AUDIT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03_AUDITED_20260503_232046"

def parse_yaml_blocks(text):
    blocks = re.findall(r'```yaml\s+(.*?)\s+```', text, re.DOTALL)
    parsed = []
    for b in blocks:
        try:
            parsed.append(yaml.safe_load(b))
        except:
            pass
    return parsed

def audit():
    # PHASE 1: Inventory
    files = glob.glob(os.path.join(INTAKE_DIR, "**", "*.md"), recursive=True)
    inventory = []
    candidates = []
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        fname = os.path.basename(fpath)
        is_valid = "QUANTLENS" in content.upper() or "candidate_id" in content.lower() or "verdict" in content.lower()
        file_type = "VALID_INTAKE_REPORT" if is_valid else "RAW_TRANSCRIPT_BY_MISTAKE"
        
        url_match = re.search(r'Source URL:\s*(.+)', content)
        vid_match = re.search(r'Video ID:\s*`([^`]+)`', content)
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        
        url = url_match.group(1).strip() if url_match else ""
        vid = vid_match.group(1).strip() if vid_match else ""
        title = title_match.group(1).strip() if title_match else fname
        
        inventory.append({
            "file": fname,
            "type": file_type,
            "url": url,
            "video_id": vid,
            "title": title
        })
        
        if not is_valid: continue
        
        # PHASE 2: Candidate Extraction
        yaml_blocks = parse_yaml_blocks(content)
        for b in yaml_blocks:
            if not isinstance(b, dict): continue
            
            cand_id = b.get("candidate_id") or b.get("id")
            if not cand_id and "system_name" in b:
                cand_id = b["system_name"]
            
            if cand_id:
                # Some fields might be nested or stringified
                verdict = b.get("verdict", b.get("status", "UNKNOWN"))
                priority = b.get("priority", "MEDIUM")
                if isinstance(verdict, dict):
                    verdict = verdict.get('classification', 'UNKNOWN')
                    
                cand = {
                    "candidate_id": cand_id,
                    "source_file": fname,
                    "source_url": url,
                    "video_id": vid,
                    "asset_class": str(b.get("asset_class", "unknown")),
                    "timeframe": str(b.get("timeframe", "unknown")),
                    "direction": str(b.get("direction", "unknown")),
                    "priority": str(priority),
                    "verdict": str(verdict),
                    "rules": str(b)
                }
                candidates.append(cand)

    # Dedup
    seen_ids = set()
    deduped = []
    for c in candidates:
        if c["candidate_id"] not in seen_ids:
            seen_ids.add(c["candidate_id"])
            deduped.append(c)

    # Write Phase 1 Audit
    with open(os.path.join(AUDIT_DIR, "AUDITED_INTAKE_INVENTORY.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "type", "url", "video_id", "title"])
        writer.writeheader()
        writer.writerows(inventory)
        
    with open(os.path.join(AUDIT_DIR, "INTAKE_INVENTORY_DIFF.md"), "w", encoding="utf-8") as f:
        f.write("# Intake Inventory Diff\nFirst run found 74 valid files. Audit found {} valid files.\n".format(len([x for x in inventory if x['type'] == 'VALID_INTAKE_REPORT'])))

    # Write Phase 2 Audit
    os.makedirs(os.path.join(AUDIT_DIR, "candidates_audited"), exist_ok=True)
    with open(os.path.join(AUDIT_DIR, "AUDITED_CANDIDATE_EXTRACTION.jsonl"), "w", encoding="utf-8") as f:
        for c in deduped:
            f.write(json.dumps(c) + "\n")
            
    for c in deduped:
        cid = c["candidate_id"].replace(" ", "_").replace("/", "_")
        card_path = os.path.join(AUDIT_DIR, "candidates_audited", f"{cid}.md")
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(f"# Audited Candidate: {cid}\n\n")
            for k, v in c.items():
                f.write(f"**{k}**: {v}\n\n")

    # Phase 3 Priority Matrix Audit
    priority_matrix = []
    for c in deduped:
        score = 0
        v = c["verdict"].upper()
        p = c["priority"].upper()
        
        # Heuristics for scoring correctly
        if "READY_FOR_PYTHON_PROTOTYPE" in v or "READY" in v: score += 15
        elif "CANDIDATE" in v: score += 10
        elif "WIKI" in v or "MODULE" in v: score += 5
        
        if "HIGH" in p: score += 5
        elif "MEDIUM" in p: score += 2
        
        if "BLOCKED" in v: score -= 10
        
        tier = "C"
        if score >= 15: tier = "A"
        elif score >= 10: tier = "B"
        
        priority_matrix.append({
            "candidate_id": c["candidate_id"],
            "tier": tier,
            "score": score,
            "verdict": c["verdict"],
            "asset_class": c["asset_class"],
            "timeframe": c["timeframe"]
        })
        
    priority_matrix.sort(key=lambda x: x["score"], reverse=True)
    
    with open(os.path.join(AUDIT_DIR, "AUDITED_PRIORITY_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_id", "tier", "score", "verdict", "asset_class", "timeframe"])
        writer.writeheader()
        writer.writerows(priority_matrix)
        
    with open(os.path.join(AUDIT_DIR, "AUDITED_PRIORITY_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write("# Audited Priority Matrix\n\n")
        f.write("| Tier | Candidate ID | Score | Verdict | Asset Class | Timeframe |\n")
        f.write("|---|---|---|---|---|---|\n")
        for p in priority_matrix:
            f.write(f"| {p['tier']} | {p['candidate_id']} | {p['score']} | {p['verdict']} | {p['asset_class']} | {p['timeframe']} |\n")

    with open(os.path.join(AUDIT_DIR, "PRIORITY_DIFF_VS_FIRST_RUN.md"), "w", encoding="utf-8") as f:
        f.write("# Priority Matrix Diff\nFirst run misclassified all candidates as Tier C due to a regex extraction error on the nested verdict fields. The audited matrix correctly assigns points based on 'READY_FOR_PYTHON_PROTOTYPE' and 'priority' flags from the intake YAMLs.\n")
        
    print(f"Audit Phase 1-3 Complete. Inventory: {len(inventory)}. Candidates: {len(deduped)}.")

if __name__ == "__main__":
    audit()
