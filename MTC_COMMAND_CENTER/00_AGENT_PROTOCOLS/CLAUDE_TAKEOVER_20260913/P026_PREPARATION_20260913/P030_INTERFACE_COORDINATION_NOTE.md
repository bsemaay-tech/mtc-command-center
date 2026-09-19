# P030 / P026 interface coordination note

**Lane:** P26PREP · SuperGrok (grok-4.6) · 2026-09-13
**Authorization:** owner chat "C YES" = read-only preparation. **Nothing here is a decision, acceptance, or authorization.** Config recommendations are copied from V3 (C-1..C-13, O-1..O-10); they are not re-decided.
**No code written. Nothing executed. No host contact.**

P030 = venue market data (collector, identity contracts, P030-owned adapters).
P026 = OPS-A survivability (backup, restore, heartbeat emitter, dead-man watchdog).

The adapter docstring states the wrapping rule: "P030 stable-prefix adapter over unchanged P026 backup/restore tools." (`C:/tmp/P030_INTEGRATION_20260913/p030_closed_partition_backup_adapter.py:1`). The heartbeat adapter states the sibling rule: "P030-owned adapter over the unchanged P026 heartbeat emitter." (`C:/tmp/P030_INTEGRATION_20260913/p030_opsa_heartbeat_adapter.py:1`).

---

## 1. Ownership map

| Surface | Who writes | Who reads | Frozen? |
|---|---|---|---|
| Live monthly JSONL archive | P030 collector `MonthlyArchive._append` | P030 collector `classify_bar` / `bars`; P030 adapter `_prefix_facts` / `capture_stable_prefix` | row *shape* frozen (`DATASET_ROW_FIELDS`); serialization + identities currently **not** aligned — see repair design / O-9 |
| Contract identities (`p030obs-v1`, `p030payload-v1`, `p030ds-v1`, `p030evt-v1`, `p030prov-v1`) | P030 `p030_market_data_contracts.py` (pure functions) | P030 adapter grammar; intended collector (not wired today) | **Yes** — prefixes, field tuples, algorithm, canonicalization version |
| Stable-prefix snapshot + `_P030_STABLE_PREFIX.json` | P030 `capture_stable_prefix` | P030 `backup_stable_prefix` / `_verify_stable_receipt`; P026 `backup.py` copies whatever is in the store path | P030 receipt schema |
| Backup tree + `manifest.jsonl` | P026 `backup.py` | P026 `restore.py`; P030 `_complete_p026_run` / `restore_verified_prefix` | P026 manifest schema; no-delete; append-only |
| Isolated verified restore + `_P030_VERIFIED_RESTORE.json` | P026 `restore.py` writes files; P030 adapter writes the verified receipt | operator / later drills | P030 receipt schema; restore target must be empty |
| Heartbeat `<id>.hb.json` | P026 `heartbeat.emit`, called by P030 `emit_process_heartbeat` | P026 `watchdog.classify`; P030 `verify_process_heartbeat` | **Yes** — exact field set; P030 must not extend it |
| Health sidecar `<id>.health.json` | P030 `write_health_sidecar` | P030 only (watchdog glob is `*.hb.json`) | P030 sidecar schema; must stay out of the P026 payload |
| Watchdog alert JSONL + dedupe state | P026 `watchdog.py` (`local_log` only today) | operator | notifier registry extension point; phone notifier absent until owner + G9 |
| Backup config JSON | operator / generated per capture (V3 C-4) | P026 `load_backup_config`; P030 `_validate_config_scope` | schema `mtc.opsa_backup_config/v1`; P030 additionally requires `class=="protected"` and `path==stable_prefix` |

---

## 2. Touchpoints (both sides, file:line)

### T1 · Archive JSONL bytes (the §4.1 seam)

| Side | File:line | Quote / duty |
|---|---|---|
| P030 writer | `C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:330` | `self._append(path, asdict(bar))` |
| P030 writer | `…/market_data_collector.py:297-300` | `json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(",", ":"))` — **no `sort_keys`** |
| P030 writer | `…/market_data_collector.py:268-276` | layout `bars/<venue>/<symbol>/<interval>/<YYYY-MM>.jsonl` through `_SAFE_PART` |
| P030 reader | `…/p030_closed_partition_backup_adapter.py:197-208` | re-dumps with `sort_keys=True` and refuses `"prefix record is not canonical JSONL"` |
| P030 reader | `…/p030_closed_partition_backup_adapter.py:181-183` | `"high-water prefix must end with newline"` |
| P030 reader | `…/p030_closed_partition_backup_adapter.py:229` | docstring: "Capture a caller-bounded canonical JSONL prefix without inferring closure." |

**Write owner:** collector. **Must stay frozen after O-9:** adapter canonical-JSONL rule. **Open:** O-9 (how the producer meets that rule). See `BACKUP_COMPLETION_REPAIR_DESIGN.md`.

### T2 · Observation / payload identity grammar

| Side | File:line | Quote / duty |
|---|---|---|
| P030 writer (today) | `…/market_data_collector.py:66-80` | `HashContract.digest` returns `digest.hexdigest()` — no prefix, no domain string |
| P030 writer (today) | `…/market_data_collector.py:215-223` | `identities.payload.digest(raw)` then `identities.observation.digest(observation_fields)` over wire fields plus a few stamps |
| P030 frozen contract | `…/p030_market_data_contracts.py:16-18` | `ALGORITHM="sha256"`; `CANONICALIZATION_VERSION="p030-json-array-v1"`; `EVENT_SCHEMA_VERSION="mtc.p030_event/v1"` |
| P030 frozen contract | `…/p030_market_data_contracts.py:35-43` | `PAYLOAD_FIELDS` / `OBSERVATION_FIELDS` tuples |
| P030 frozen contract | `…/p030_market_data_contracts.py:172-180, 187-198, 219-222` | `_canonical_id` hashes `[domain, *values]` and returns `f"{prefix}:{hexdigest}"`; `producer_payload_hash` / `observation_id` |
| P030 adapter | `…/p030_closed_partition_backup_adapter.py:47-48, 209-213` | `_OBSERVATION_ID = re.compile(r"^p030obs-v1:[0-9a-f]{64}$")`; refuse `"observation_id must match p030obs-v1 identity"` |
| P030 contract load-bearing check | `…/p030_market_data_contracts.py:324-329` | payload hash and observation id must *match* the row bytes, not merely look prefixed |
| P030 adapter dataset grammar | `…/p030_closed_partition_backup_adapter.py:245-249` | caller-supplied `dataset_content_hash` must match `^p030ds-v1:[0-9a-f]{64}$` (grammar only; recomputation is the caller's) |

**Write owner of live ids today:** collector `HashContract` (wrong shape). **Must stay frozen:** contract prefixes, field lists, `_canonical_id`, adapter regex. **Open:** O-9. Prefix-stamping the current hexdigest is not sufficient (`BACKUP_COMPLETION_REPAIR_DESIGN.md` §1.2).

### T3 · Row shape (already aligned)

| Side | File:line | Quote / duty |
|---|---|---|
| P030 collector | `…/market_data_collector.py:90-111` | `MarketBar` 21 fields |
| P030 contracts | `…/p030_market_data_contracts.py:53-58` | `DATASET_ROW_FIELDS` — same 21 names in the same order |

**Write owner:** collector dataclass. **Must stay frozen:** `DATASET_ROW_FIELDS`. No schema redesign is required for O-9.

### T4 · Stable-prefix capture and receipts

| Side | File:line | Quote / duty |
|---|---|---|
| P030 writer | `…/p030_closed_partition_backup_adapter.py:220-290` | `capture_stable_prefix`; refuses if `stable_prefix.exists()` (`:256-257`); writes snapshot then `_P030_STABLE_PREFIX.json` (`:276-290`) |
| P030 writer | `…/p030_closed_partition_backup_adapter.py:33` | `STABLE_RECEIPT_NAME = "_P030_STABLE_PREFIX.json"` |
| P030 frozen receipt fields | `…/p030_closed_partition_backup_adapter.py:35-46` | exact set `{schema,state,source_path,snapshot_rel,high_water_bytes,record_count,last_observation_id,prefix_sha256,captured_at_utc,dataset_content_hash}` |
| P026 | does not know this receipt | copies it as an ordinary file because it sits in the store path |

**Write owner:** P030 adapter. **Must stay frozen:** receipt field set, "must not already exist" (`:256-257`). That last rule is why V3 C-4 forbids a reused store `path` (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:187-188`).

### T5 · Backup config (P026 schema + P030 extra constraints)

| Side | File:line | Quote / duty |
|---|---|---|
| P026 loader | `…/MTC_COMMAND_CENTER/tools/opsa/opsa_common.py:227-245` | schema `mtc.opsa_backup_config/v1`; `backup_root` and every store `id`/`path`/`class` must be non-empty strings; store `id` confined via `resolve_confined_path(..., "runs", "_config_check", store["id"])` |
| P030 extra | `…/p030_closed_partition_backup_adapter.py:393-407` | exactly one matching `store_id`; `class` must be `"protected"`; `path` must resolve equal to the stable prefix |
| Shipped file | `…/p030_opsa_backup_config.json:3,6,7,8` | `"backup_root": null`, store `"id": null`, `"path": null`, `"class": "protected"` |
| P026 example | `…/MTC_COMMAND_CENTER/tools/opsa/config.example.json:1-16` | schema + two example stores (`protected` / `bulk`); placeholder paths |

The three nulls make the shipped file unloadable (`opsa_common.py:232, 238-239`). `class` is already the required `"protected"` — no class choice remains (V3 C-4 constraint 1). Values are O-2. Shape (one generated config per capture, fresh path per capture, fixed id `p030_closed_partition`) is V3 C-4 recommendation — not re-decided here.

**Write owner:** operator / generator. **Must stay frozen:** P026 schema and confinement; P030 `protected` + path-equals-prefix. **Open:** O-1 / O-2 path values (host facts).

### T6 · P026 backup run (unchanged tool, wrapped)

| Side | File:line | Quote / duty |
|---|---|---|
| P026 writer | `…/MTC_COMMAND_CENTER/tools/opsa/backup.py:80-204` | `run_backup`: copy tree, SHA-256, `readback=match`, append-only `manifest.jsonl`; dry-run writes nothing (`:104-109`, `:164-166`) |
| P026 writer | `…/backup.py:149` | dest `resolve_confined_path(run_dir, store_id, rel)` |
| P026 writer | `…/backup.py:7-9` | "**No delete code path.** This tool only creates and overwrites files." |
| P030 wrapper | `…/p030_closed_partition_backup_adapter.py:625-679` | `backup_stable_prefix` binds config, verifies receipt+snapshot before and after, calls `backup.run_backup(..., dry_run=False, store_filter={store_id})` (`:646-648`), requires exactly one new `run_start` (`:669-671`) |
| P030 wrapper | `…/p030_closed_partition_backup_adapter.py:469-527` | `_complete_p026_run`: one `run_start` + one `run_end` with `status=="ok"` and `errors==[]`; only `file` records besides envelope; `readback=="match"`; member set exactly `{_P030_STABLE_PREFIX.json, snapshot_rel}` |

**Write owner of backup bytes:** P026 `backup.py`. **Write owner of the "this run is a P030 stable prefix" predicate:** P030 `_complete_p026_run`. **Must stay frozen:** P026 no-delete, append-only manifest, read-back; P030 two-member set and `readback=="match"`.

### T7 · P026 restore (unchanged tool, wrapped, isolated)

| Side | File:line | Quote / duty |
|---|---|---|
| P026 | `…/MTC_COMMAND_CENTER/tools/opsa/restore.py:13-14` | "`--check-only` performs step 1 over the whole run and writes nothing — the isolated integrity proof" |
| P026 | `…/restore.py:60-70` | `verify_backup_file`: `"sha256 mismatch"` refuses |
| P026 | `…/restore.py:181` | dest `resolve_confined_path(target, record["store_id"], record["rel"])` |
| P030 wrapper | `…/p030_closed_partition_backup_adapter.py:682-816` | `restore_verified_prefix`: empty target (`:687-688`); isolated temp copy of the backup root (`:560-622`); `restore.run_restore(..., check_only=True)` then the real restore (`:706-742`); writes `_P030_VERIFIED_RESTORE.json` (`:796-816`) |
| P030 wrapper | `…/p030_closed_partition_backup_adapter.py:34` | `VERIFIED_RESTORE_RECEIPT_NAME = "_P030_VERIFIED_RESTORE.json"` |

Plan: restore drills run on copies, never the live store (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:583`: "restore drills run on copies, never the live store").

Plan: "A backup counts only after an isolated restore proves integrity, readability **and reconciliation**" (`:581`). The adapter proves integrity and readability of one prefix. **Reconciliation has no shipped implementation in the inspected OPSA/P030 modules** (V3 NV-5). That is not an owner configuration choice; it is a missing function. It is *not* added as a new O-item because V3 already recorded it as NV-5 / P-3 and asked no extra owner number for it.

**Write owner of restored files:** P026 `restore.py`. **Write owner of the verified-restore receipt:** P030 adapter. **Must stay frozen:** check-then-write, isolated copy, empty target, no-delete.

### T8 · Heartbeat payload (exact P026 set)

| Side | File:line | Quote / duty |
|---|---|---|
| P026 writer | `…/MTC_COMMAND_CENTER/tools/opsa/heartbeat.py:43-54` | `emit` writes `{schema, id, seq, emitted_at, pid}` plus optional `note`; path `<id>.hb.json` via `resolve_confined_path` |
| P026 schema | `…/opsa_common.py:38` | `HEARTBEAT_SCHEMA = "mtc.opsa_heartbeat/v1"` |
| P030 wrapper | `…/p030_opsa_heartbeat_adapter.py:59-72` | `emit_process_heartbeat` — "Emit only the exact P026 heartbeat payload."; requires non-empty id; calls `heartbeat.emit` |
| P030 reader | `…/p030_opsa_heartbeat_adapter.py:91-94` | required `{schema,id,seq,emitted_at,pid}`; allowed = required ∪ `{note}` |
| P030 reader | `…/p030_opsa_heartbeat_adapter.py:108-110` | `emitted_at` must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$` |
| P026 checker | `…/MTC_COMMAND_CENTER/tools/opsa/watchdog.py:97-119` | `classify` uses payload `emitted_at`, never mtime (`heartbeat.py:4-6`; `watchdog.py:4-5`) |
| P026 checker | `…/watchdog.py:137-138` | discovers `state_dir.glob("*.hb.json")` at the **top level only** |
| P026 checker | `…/watchdog.py:276` | `--expect` splits on commas |

**Write owner:** P026 `heartbeat.emit` (P030 may only call it). **Must stay frozen:** field set, schema id, UTC-Z whole-second grammar, filename `<id>.hb.json`, no graceful-stop marker (`heartbeat.py:13-15`). Id must be one path segment with no comma (else invisible to the glob or split by `--expect`). V3 C-6 recommended id `p030_market_data_collector` — Lead default, not re-decided.

### T9 · P030 health sidecar (must not enter T8)

| Side | File:line | Quote / duty |
|---|---|---|
| P030 writer | `…/p030_opsa_heartbeat_adapter.py:130-174` | `write_health_sidecar`; schema `"p030.health_sidecar/v1"`; path `<id>.health.json`; `reconciliation_progress` must remain null (`:143-144`) |
| P026 | `watchdog.py:137-138` | glob `*.hb.json` — sidecar is invisible to the checker by construction |

**Write owner:** P030. **Must stay frozen:** sidecar is not a P026 heartbeat; watchdog must not be taught to parse it as liveness. Freshness numbers stay `OPEN` (collector `OPEN-N14` etc.); the sidecar carries observed timestamps, not a ratified bound.

### T10 · Watchdog states, notifier, silence bound

| Side | File:line | Quote / duty |
|---|---|---|
| P026 | `…/watchdog.py:9-15` | six per-id states: `ok` / `silent` / `missing` / `unreadable` / `bad_timestamp` / `clock_skew` |
| P026 | `…/watchdog.py:17-18` | rc 0 all ok · 2 any alert · 3 check-failure and no alert |
| P026 | `…/watchdog.py:115-118` | `silent` when `age > silence_seconds` |
| P026 | `…/watchdog.py:63-64, 112-114` | future skew ≤ 60 s tolerated; beyond that `clock_skew` |
| P026 | `…/watchdog.py:241-246` | `--silence-seconds` **required**, no default: "an unratified number must not be shipped as a contract" |
| P026 | `…/watchdog.py:70-94` | `Notifier` protocol; `NOTIFIERS = {"local_log": ...}` only |
| P026 | `…/watchdog.py:3-4`; `…/README.md:65, 104` | one-shot; "NO schedule is installed by this package" (`watchdog.py:3`; `README.md:65`); host installation "gated behind G9" (`README.md:104`) |
| P026 | `…/watchdog.py:162-163, 193-196` | synthetic `_watchdog_check` event for directory-level failures |
| P026 | `…/watchdog.py:200-235` | recovery event `silent → ok`; ledger records `ok` so a second `silent` re-alerts |
| P030 | no watchdog wrapper | P030 emits heartbeats; it does not schedule or classify them |

Plan: "a checker **outside the watched host** detects silence and **delivers a push to the owner's phone**" (`MASTER_WORK_PACKAGE…:580`). Phone delivery is binding; the detect-to-delivery bound is `[OPEN]` (`:580`, `:585`).

README usage example `--silence-seconds 900` (`README.md:68`) is an example, not a ratified value.

**Write owner of alerts:** P026 watchdog. **Must stay frozen:** six states, rc convention, required `--silence-seconds`, `local_log` as the only shipped notifier, `--now` is a test hook (`watchdog.py:42, 255-256`) and must never appear in a scheduled invocation (V3 C-9). **Open:** O-3 (bound), O-4 (phone OS), O-5 (notifier technology), C-11 / NV-4 (how the owner-PC checker sees KVM2's `state_dir`).

### T11 · Confinement (shared helper, both sides)

| Side | File:line | Quote / duty |
|---|---|---|
| P026 | `…/opsa_common.py:170-224` | `resolve_confined_path`: reject absolute, drive/UNC, `..`, URL-escaped `..`; result must be strictly inside root |
| P030 backup adapter | uses it for snapshot dest (`:269`), archived prefix (`:511`), isolated restore (`:564-588`), restored prefix (`:759`) | |
| P030 heartbeat adapter | `…/p030_opsa_heartbeat_adapter.py:82, 163` | heartbeat and sidecar paths |

**Must stay frozen:** confinement helper; P030 copies and validates backup-config bytes before the P026 backup call (`p030_closed_partition_backup_adapter.py:410-436`) and compares receipt/snapshot bytes after it (`:651-660`); isolated-restore config is re-verified in a `finally` before and after that restore path only (`:439-466`).

### T12 · Collector universe, gap fill, restart (P030-only, consumed by P026 only as "the process that must heartbeat")

| Side | File:line | Quote / duty |
|---|---|---|
| P030 | `…/market_data_collector.py:23-30` | `INITIAL_SYMBOLS = ("BTC",)`; intervals `15m/1h/4h/1d` |
| P030 | `…/market_data_collector.py:204-205` | forming bars (`close_time > ingest_time`) are not archived |
| P030 | `…/market_data_collector.py:416-425` | `IDENTICAL_REPLAY_NOOP` seeds WS cursor, does not append |
| P030 | `…/market_data_collector.py:374-413, 378` | restart re-validates persisted `source_producer == "WS_LIVE"` history and refuses any gap — snapshot-backfilled bars do not close that scan |
| P030 | `…/market_data_collector.py:534-538` | `run` refused until a future owner-ratified permission protocol and backend |

**Must stay frozen until a separate owner scope:** universe, closed-bar rule, identical-replay no-op, coded `run` refusal (O-6 / C-1). **Open, already numbered:** O-7 (ratify those restart semantics; residual persisted-WS_LIVE-gap is in the O-7 cell itself). Not a new owner item.

### T13 · Plan-level coupling

| Side | File:line | Quote / duty |
|---|---|---|
| Plan WP-P0-30 | `MASTER_WORK_PACKAGE…:635` | collector "watched by the WP-P0-26 dead-man watchdog"; "archive on disk under WP-P0-26's second-location backup policy" |
| Plan WP-P0-30 | `:638` | "**Depends on:** WP-P0-26 (watchdog + backup for the archive), **WP-P0-21**" |
| Plan WP-P0-26 | `:580` | "automated second-location copy for every evidence store (cross-copy VPS ↔ owner PC)"; "daily backups"; checker outside the watched host; phone push |
| Plan WP-P0-26 | `:581(b)` | "already-ratified daily all-store … cadence is **preserved unchanged**" |
| Plan WP-P0-26 | `:585` | no forward clock before this package is accepted; restore RED/GREEN; phone push is the watchdog acceptance test; detect-to-delivery bound `[OPEN]` until owner ratifies a measured value |
| Plan both | `:584`, `:640` | host-install steps T0, mapped to **G9**, plus G1-IA; owner's authorization per session; nothing authorized by the plan text |

**Must stay frozen:** daily cadence (unless the owner explicitly takes O-2's monthly-only departure); phone-delivery duty; clock-gating edge; G9 per-session host gate. **Open:** O-3 bound, O-5 notifier, measured N14.

---

## 3. What must stay frozen (checklist)

Copy this into the O-9 / T1 review so a later implementer cannot "fix" the seam by loosening the consumer.

1. `p030_market_data_contracts.py`: `ALGORITHM`, `CANONICALIZATION_VERSION`, all `*_FIELDS` tuples, `_canonical_id` domain+prefix behaviour, correction-chain rules (`:262-312`).
2. Adapter `_prefix_facts` canonical JSONL equality and `p030obs-v1` / `p030ds-v1` regexes.
3. Adapter "stable prefix must not already exist"; store `class=="protected"`; store path equals stable prefix.
4. P026 backup/restore/heartbeat/watchdog **source** (adapter wraps; it does not fork).
5. P026 no-delete construction (`opsa_common.py:5-12`; `backup.py:7-9`; `README.md:24-33`).
6. Heartbeat field set `{schema,id,seq,emitted_at,pid}` + optional `note`; sidecar stays a separate file.
7. Watchdog six states, required `--silence-seconds`, `local_log` as the only shipped notifier, `--now` test-only.
8. Collector `run` refusal until O-6 + G9; `OPEN-N*` tags remain questions (`market_data_collector.py:32-33`).
9. Restore drills on copies, never the live store (plan `:583`).
10. Alerts carry no secrets and no controls (`watchdog.py:28`; plan `:581(f)`).

---

## 4. Open questions — owner items only where genuinely undecidable

No new O-number is invented. If V3 already numbered it, it stays that number. If it is a missing function rather than a value choice, it stays NOT VERIFIED.

| Ref | Question | Why an agent cannot close it | V3 recommended answer (copied, not re-decided) |
|---|---|---|---|
| **O-1** | `<ARCHIVE_ROOT>` volume and free-space budget | Host fact; collector takes `MonthlyArchive(root)` with no config field (`market_data_collector.py:264-266`) | Name a placeholder; bind the concrete path at the G9 step |
| **O-2** | `<BACKUP_ROOT>` (different device/host from O-1), store shape, and whether to depart from the ratified **daily** cadence | Host fact + plan cadence already ratified (`MASTER_WORK_PACKAGE…:580, :581(b)`) | Approve C-4 per-capture config + C-5 daily high-water plus month-end; say "monthly-only" explicitly if departing |
| **O-3** | `--silence-seconds` and check cadence | Code refuses a default (`watchdog.py:241-246`); plan withdrew `~15 minutes` (`:580, :585`) | Ratify `300` s / 60 s emit / 5 min check as a **proposal with no repository basis**; or "defer" and stay `local_log`-only. Ratifying a number is not schedule installation |
| **O-4** | Owner phone Android or iOS? | Device fact; decides whether self-hosted ntfy needs the APNS relay (`NOTIFIER_PROPOSAL.md:62-67`) | Answer the OS |
| **O-5** | Notifier technology | Plan leaves technology to the owner (`MASTER_WORK_PACKAGE…:580`; `NOTIFIER_PROPOSAL.md:89`) | ntfy.sh for the first measured drill; self-hosted ntfy as steady state; re-verify Aug-25 facts |
| **O-6** | Lift collector `run` refusal? | Needs a ratified permission protocol and backend (`market_data_collector.py:534-538`); also behind P030's dependency on P026 (`MASTER_WORK_PACKAGE…:638`) | Keep the refusal; revisit timing after O-5/O-8; any lift still sits behind that dependency and G9 |
| **O-7** | Restart-first-message policy beyond identical replay | Decision 7 did not close it (V3 cites `[GH]:16`; this lane did not re-open that handoff — see NOT VERIFIED) | Ratify implemented refuse-and-require-CORRECTION semantics; D-11 before any real restart; persisted-WS_LIVE-gap residual stays |
| **O-8** | T-A offline execution scope | This lane is read-only | Approve fixtures-only; D-13 GREEN is **out** (that is O-9) |
| **O-9** | Producer/exporter bridge | New code, two shapes | Approve the design step first — this lane's recommended shape is Option A in `BACKUP_COMPLETION_REPAIR_DESIGN.md` |
| **O-10** | Add P021/P030 owner answers to `DECISIONS.md`? | Only the owner authorizes a decision-index row | Yes — they live in handoff prose today (V3 table row 35). This lane did not re-read `DECISIONS.md` |
| **C-11 / V3 NV-4** | How a checker on the owner PC sees KVM2's heartbeat directory | No mechanism in the inspected sources. Plan requires the checker outside the watched host (`:580`) but does not specify transport. Without it, `watchdog.py:131-136` reports `check_failed` `"state dir does not exist"` instead of process silence | Record the placement requirement; request no install until a transport is chosen. Recommended (reasoning, not a sourced design): owner-PC-local replica *pulled* from KVM2, refresh interval ≪ silence bound, and D-17 to distinguish replica-loss from process-silence. The exact mechanism is a host-design owner question, not a new O-number |
| **V3 NV-5 / P-3** | Who implements plan `:581(c)` reconciliation? | Not located in `tools/opsa/` or the P030 adapters. Missing function, not a config value | Do not invent an owner item. Carry as NOT VERIFIED. A backup still does not "count" for clock-gating until this exists |
| **V3 NV-9** | Which observation timestamp starts a countable forward clock? | Gating requirements are located (plan `:585, :581(c), :641`); the start *event* is not | Do not invent a start rule |

---

## 5. What P030 must not do to P026, and vice versa

- P030 must not add fields to `<id>.hb.json`. Extra fields fail `verify_process_heartbeat` (`p030_opsa_heartbeat_adapter.py:91-94`) and are out of the P026 contract. Health goes to `<id>.health.json`.
- P030 must not call `backup.py` / `restore.py` against the live archive path as `store.path`. The store path is the *stable-prefix directory*, not `<ARCHIVE_ROOT>` (`p030_closed_partition_backup_adapter.py:404-407`).
- P030 must not infer month-file closure inside the adapter (`:229`). The caller supplies `high_water_bytes`.
- P026 must not parse `_P030_STABLE_PREFIX.json` or `_P030_VERIFIED_RESTORE.json`. They are ordinary files in the store.
- P026 must not install a schedule, a phone notifier, or a silence-bound default.
- Neither side deletes (`opsa_common.py:5-12`). Deletions remain owner-approved exact lists (plan `:581(b)`, `:588`).
- Neither side trades, holds a venue credential, or contacts a host without a fresh G9 sentence.

---

## 6. NOT VERIFIED (this note)

| Ref | Not verified | Why |
|---|---|---|
| NV-I1 | Handoff lines V3 cites as `[HO]`, `[GH]`, `[SH]`, `[PKT]`, `[DEC]` | Out of this lane's required input list. O-7's "Decision 7" substance and O-10's `DECISIONS.md` gap are carried as V3 recorded them, not re-opened. |
| NV-I2 | Deployed backup / monitoring / restart / rollback on KVM2 | Plan `:581`: repository records, not host observation; state `UNVERIFIED` pending G9. This lane contacted nothing. |
| NV-I3 | That a daily capture-and-copy completes within a day on the real volumes | V3 NV-16; host fact. |
| NV-I4 | Reconciliation implementation anywhere outside the bounded search | V3 NV-5. |
| NV-I5 | PASS results of the 44 / 10 / 33 suites | Method counts were grepped; nothing was run. |
| NV-I6 | Detailed command transcripts in `RESTORE_DRILL_EVIDENCE.md` beyond headings and lines 1-30 | Same bound as V3 NV-12. Fixture-drill *claims* used below come from `LANE_REPORT.md:95-100`, which was read in full. |

---

**End of coordination note.** No interface is changed by this file.
