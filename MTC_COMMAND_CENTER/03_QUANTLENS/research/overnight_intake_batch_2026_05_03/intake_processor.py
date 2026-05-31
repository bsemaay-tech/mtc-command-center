import os
import glob
import re
import csv
import json
import yaml

INTAKE_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs"
OUTPUT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03"

def parse_yaml_blocks(text):
    blocks = re.findall(r'```yaml\s+(.*?)\s+```', text, re.DOTALL)
    parsed = []
    for b in blocks:
        try:
            parsed.append(yaml.safe_load(b))
        except:
            pass
    return parsed

def process_intakes():
    os.makedirs(os.path.join(OUTPUT_DIR, "candidates"), exist_ok=True)
    
    files = glob.glob(os.path.join(INTAKE_DIR, "**", "*.md"), recursive=True)
    
    inventory = []
    candidates = []
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        fname = os.path.basename(fpath)
        
        # Determine valid intake
        is_valid = "QUANTLENS" in content or "candidate_id" in content.lower() or "verdict" in content.lower()
        file_type = "VALID_INTAKE_REPORT" if is_valid else "UNKNOWN"
        
        # Extract basic info
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
        
        # Extract candidates
        # Many reports have blocks with `candidate_id:` or `verdict:`
        yaml_blocks = parse_yaml_blocks(content)
        
        # Sometimes there's multiple modules. Let's find all candidate_ids
        for b in yaml_blocks:
            if not isinstance(b, dict): continue
            
            cand_id = b.get("candidate_id") or b.get("id")
            if not cand_id and "system_name" in b:
                cand_id = b["system_name"]
            
            if cand_id:
                # Merge info
                cand = {
                    "candidate_id": cand_id,
                    "source_file": fname,
                    "source_url": url,
                    "video_id": vid,
                    "asset_class": b.get("asset_class", "unknown"),
                    "timeframe": b.get("timeframe", "unknown"),
                    "direction": b.get("direction", "unknown"),
                    "priority": b.get("priority", "MEDIUM"),
                    "verdict": b.get("verdict", b.get("status", "UNKNOWN")),
                    "rules": str(b)
                }
                candidates.append(cand)
                
    # Deduplicate candidates
    seen_ids = set()
    deduped_candidates = []
    for c in candidates:
        if c["candidate_id"] not in seen_ids:
            seen_ids.add(c["candidate_id"])
            deduped_candidates.append(c)
            
    # Write Inventory
    with open(os.path.join(OUTPUT_DIR, "INTAKE_INVENTORY.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "type", "url", "video_id", "title"])
        writer.writeheader()
        writer.writerows(inventory)
        
    # Write Candidates
    with open(os.path.join(OUTPUT_DIR, "CANDIDATE_EXTRACTION_RAW.jsonl"), "w", encoding="utf-8") as f:
        for c in deduped_candidates:
            f.write(json.dumps(c) + "\n")
            
    # Write Candidate Cards
    for c in deduped_candidates:
        cid = c["candidate_id"].replace(" ", "_").replace("/", "_")
        card_path = os.path.join(OUTPUT_DIR, "candidates", f"{cid}.md")
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(f"# Candidate: {cid}\n\n")
            for k, v in c.items():
                f.write(f"**{k}**: {v}\n\n")
                
    # Rank & Priority Matrix
    # We will score them heuristically. If verdict contains 'READY_FOR_PYTHON_PROTOTYPE', score high.
    priority_matrix = []
    for c in deduped_candidates:
        score = 0
        v = c["verdict"].upper()
        if "READY_FOR_PYTHON_PROTOTYPE" in v: score += 15
        if "CANDIDATE" in v: score += 10
        if "HIGH" in c["priority"].upper(): score += 5
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
    
    with open(os.path.join(OUTPUT_DIR, "PRIORITY_MATRIX.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_id", "tier", "score", "verdict", "asset_class", "timeframe"])
        writer.writeheader()
        writer.writerows(priority_matrix)
        
    # Priority Matrix MD
    with open(os.path.join(OUTPUT_DIR, "PRIORITY_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write("# Priority Matrix\n\n")
        f.write("| Tier | Candidate ID | Score | Verdict | Asset Class | Timeframe |\n")
        f.write("|---|---|---|---|---|---|\n")
        for p in priority_matrix:
            f.write(f"| {p['tier']} | {p['candidate_id']} | {p['score']} | {p['verdict']} | {p['asset_class']} | {p['timeframe']} |\n")
            
    print(f"Processed {len(inventory)} files. Found {len(deduped_candidates)} candidates.")
    
if __name__ == "__main__":
    process_intakes()
