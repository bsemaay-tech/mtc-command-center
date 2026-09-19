import json
import os
import shutil
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

sys.path.insert(0, str((LANE / "wt").resolve()))
from p030_opsa_heartbeat_adapter import (
    emit_process_heartbeat,
    verify_process_heartbeat,
    write_health_sidecar,
)

BASE = LANE / "fixtures"
beat_id = "p030_market_data_collector"


def reset_dir(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def attempt(label: str, fn) -> None:
    try:
        result = fn()
        print(f"{label}: OK {result}")
    except Exception as exc:
        print(f"{label}: ERROR {type(exc).__name__}: {exc}")


# Isolated falsification: extra field
extra_dir = reset_dir(BASE / "heartbeats_extra")
extra_path = emit_process_heartbeat(extra_dir, beat_id, seq=1)
with extra_path.open(encoding="utf-8") as handle:
    extra_payload = json.loads(handle.read())
extra_payload["extra"] = "x"
extra_path.write_text(json.dumps(extra_payload), encoding="utf-8")
attempt("verify-extra", lambda: verify_process_heartbeat(extra_dir, beat_id))

# Isolated falsification: fractional emitted_at only (no extra field)
frac_dir = reset_dir(BASE / "heartbeats_fractional")
frac_path = emit_process_heartbeat(frac_dir, beat_id, seq=1)
with frac_path.open(encoding="utf-8") as handle:
    frac_payload = json.loads(handle.read())
frac_payload["emitted_at"] = "2026-09-14T05:00:00.123Z"
frac_path.write_text(json.dumps(frac_payload), encoding="utf-8")
attempt("verify-fractional", lambda: verify_process_heartbeat(frac_dir, beat_id))

# Isolated falsification: reconciliation_progress non-null
recon_dir = reset_dir(BASE / "heartbeats_recon")
emit_process_heartbeat(recon_dir, beat_id, seq=1)
recon_payload = verify_process_heartbeat(recon_dir, beat_id)
attempt(
    "health-recon",
    lambda: write_health_sidecar(
        recon_dir,
        beat_id,
        observed_at_utc=recon_payload["emitted_at"],
        last_accepted_timestamp_utc=None,
        reconciliation_progress={"slot": 1},
    ),
)

# Isolated falsification: last_accepted later than observed
late_dir = reset_dir(BASE / "heartbeats_late")
emit_process_heartbeat(late_dir, beat_id, seq=1)
late_payload = verify_process_heartbeat(late_dir, beat_id)
attempt(
    "health-late-accepted",
    lambda: write_health_sidecar(
        late_dir,
        beat_id,
        observed_at_utc=late_payload["emitted_at"],
        last_accepted_timestamp_utc="2099-09-14T05:00:00Z",
        reconciliation_progress=None,
    ),
)

# GREEN path last: surviving artefacts under fixtures/heartbeats are P026-shaped
state_dir = reset_dir(BASE / "heartbeats")
hb_path = emit_process_heartbeat(state_dir, beat_id, seq=1)
print(f"emit: path={hb_path}")
payload = verify_process_heartbeat(state_dir, beat_id)
print(f"verify-ok: fields={sorted(payload.keys())}")
health = write_health_sidecar(
    state_dir,
    beat_id,
    observed_at_utc=payload["emitted_at"],
    last_accepted_timestamp_utc=payload["emitted_at"],
    reconciliation_progress=None,
)
print(f"health-available: path={health}")
health_payload = json.loads(health.read_text(encoding="utf-8"))
freshness = health_payload["market_freshness"]
print(
    f"health-available: schema={health_payload['schema']} "
    f"availability={freshness['availability']} age_seconds={freshness['age_seconds']}"
)
hb_on_disk = json.loads(hb_path.read_text(encoding="utf-8"))
print(f"hb-on-disk-fields={sorted(hb_on_disk.keys())}")
print(f"hb-on-disk-emitted_at={hb_on_disk['emitted_at']}")
