"""Builds the NON-ACCEPTING T-A drill PREVIEW lane on the WP-P0-26 candidate bytes (d81b07f6).
Copies the candidate files from the P026 worktree (file copies only; no git while agy runs) and records their
sha256 so they can be checked against `git show d81b07f6:<path>` once the Gemini chain has ended."""
import hashlib, json, pathlib, shutil
LANE = pathlib.Path("C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
WT_SRC = pathlib.Path("C:/tmp/P026_REPAIR_20260915")
OLD = pathlib.Path("C:/tmp/P026_DRILLS_TA_20260914")
FILES = [
    "p030_closed_partition_backup_adapter.py", "p030_opsa_heartbeat_adapter.py", "p030_market_data_contracts.py",
    "market_data_collector.py", "p030_opsa_backup_config.json",
    "MTC_COMMAND_CENTER/tools/opsa/backup.py", "MTC_COMMAND_CENTER/tools/opsa/restore.py",
    "MTC_COMMAND_CENTER/tools/opsa/opsa_common.py", "MTC_COMMAND_CENTER/tools/opsa/heartbeat.py",
    "MTC_COMMAND_CENTER/tools/opsa/watchdog.py", "MTC_COMMAND_CENTER/tools/opsa/config.example.json",
    "MTC_COMMAND_CENTER/tools/opsa/README.md",
]
wt = LANE / "wt"
if wt.exists():
    shutil.rmtree(wt)
sums = []
for rel in FILES:
    src = WT_SRC / rel; dst = wt / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    sums.append(f"{hashlib.sha256(dst.read_bytes()).hexdigest()}  {rel}")
(wt / "COPIED_SOURCES_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii", newline="\n")
fx = LANE / "fixtures"
if fx.exists():
    shutil.rmtree(fx)
shutil.copytree(OLD / "fixtures" / "contract_partition", fx / "contract_partition")
(fx / "config").mkdir()
(fx / "backup_root").mkdir()
cfg = {"backup_root": str(fx / "backup_root").replace("/", "\\"), "schema": "mtc.opsa_backup_config/v1",
       "stores": [{"class": "protected", "id": "p030_closed_partition",
                   "path": str(fx / "contract_partition" / "stable_prefix" / "drill_3").replace("/", "\\")}]}
(fx / "config" / "intended_config_d4.json").write_text(json.dumps(cfg, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
(LANE / "tmp").mkdir(exist_ok=True)
for d in ("D-4", "D-5", "D-6", "D-7"):
    (LANE / "drills" / d).mkdir(parents=True, exist_ok=True)
print("\n".join(sums))
print("fixtures:", sorted(p.relative_to(fx).as_posix() for p in fx.rglob("*") if p.is_file()))
