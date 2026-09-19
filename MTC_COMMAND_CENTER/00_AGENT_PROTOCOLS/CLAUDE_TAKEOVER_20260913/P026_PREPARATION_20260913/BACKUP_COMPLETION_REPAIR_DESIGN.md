# Backup-completion repair design (WP-P0-26 / P030 §4.1)

**Lane:** P26PREP · SuperGrok (grok-4.6) · 2026-09-13
**Authorization:** owner chat "C YES" = read-only preparation. This file is a design. **No code was written. Nothing was executed. Nothing here is an owner decision, acceptance, or authorization.**
**Owner item this answers:** O-9 in `C:/tmp/CLAUDE_P0_RUN_20260913/laneFX30C_fix3/P030_P026_CONFIG_DRILL_CHOICES_V3.md:586` — "An **implementation scope** for the producer/exporter bridge of §4.1". V3's recommended answer is "**Approve the design step first** (a one-page choice between the two shapes), then implement under the normal review path." This is that design step. The owner still answers O-9.

Authoritative current-state packet: `C:/tmp/CLAUDE_P0_RUN_20260913/laneFX30C_fix3/P030_P026_CONFIG_DRILL_CHOICES_V3.md` section 4.1 (`:497-510`). This document does not re-decide C-1..C-13 or O-1..O-10.

---

## 1. The contradiction (verified by re-reading the bytes)

A collector-written monthly partition cannot be captured by `capture_stable_prefix` today. V3 §4.1 names two independent refusals. Both are still present in the hashed sources (this lane re-hashed; see `REPORT.md`).

### 1.1 Serialization: collector does not write sorted-key JSONL; the adapter requires it

Collector write path: `MonthlyArchive.append_bar` serializes `asdict(bar)` through `_append`.

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:325-331`:

```
    def append_bar(self, bar: MarketBar) -> str:
        replay_status = self.classify_bar(bar)
        if replay_status is not None:
            return replay_status
        path = self.bar_path(bar)
        self._append(path, asdict(bar))
        return "APPENDED"
```

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:294-300`:

```
    def _append(path: Path, record: Mapping[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
```

There is no `sort_keys=True`. `asdict(bar)` follows `MarketBar` declaration order, which is not alphabetical:

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:90-111`:

```
class MarketBar:
    observation_id: str
    producer_payload_hash: str
    symbol: str
    interval: str
    bar_open_time: int
    bar_close_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    venue: str
    track: str
    proxy_source: None
    source_producer: str
    observation_type: str
    supersedes_observation_id: None
    ingest_time: int
    venue_seq: int | None
    env_lineage_id: str
    schema_version: str
```

Adapter capture re-serializes every prefix line with `sort_keys=True` and refuses unless the bytes are identical:

`C:/tmp/P030_INTEGRATION_20260913/p030_closed_partition_backup_adapter.py:197-208`:

```
        canonical = (
            json.dumps(
                record,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
            + b"\n"
        )
        if canonical != raw_line:
            raise ValueError("prefix record is not canonical JSONL")
```

Alphabetical key order starts with `bar_close_time`, not `observation_id`. A collector line therefore fails this check on the first row. The adapter test suite already encodes that refusal: `C:/tmp/P030_INTEGRATION_20260913/check_p030_closed_partition_backup_adapter.py:160-171` writes unsorted `json.dumps({"observation_id": …, "close": 10})` (no `sort_keys`) and expects `"prefix record is not canonical JSONL"`.

Check order inside `_prefix_facts`: canonical-byte compare (`:207-208`) runs *before* the observation-id regex (`:212-213`). On unmodified collector output, the first refusal is the serialization check.

### 1.2 Identities: collector emits a bare hexdigest; the adapter and the frozen contract require `p030obs-v1:`

Collector identity function:

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:66-80`:

```
    def digest(self, record: Mapping[str, object]) -> str:
        missing = [field for field in self.fields if field not in record]
        if missing:
            raise CollectionRefused(
                f"identity contract field(s) missing: {', '.join(missing)}"
            )
        payload = json.dumps(
            [record[field] for field in self.fields],
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode(self.encoding)
        digest = hashlib.new(self.algorithm)
        digest.update(payload)
        return digest.hexdigest()
```

The return is a bare hexdigest with no prefix.

`normalize_bar` uses that digest for both hashes:

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:215-223`:

```
    payload_hash = identities.payload.digest(raw)
    observation_fields: dict[str, object] = {
        **raw,
        "venue": "HYPERLIQUID",
        "track": "NATIVE",
        "source_producer": source_producer,
        "producer_payload_hash": payload_hash,
    }
    observation_id = identities.observation.digest(observation_fields)
```

The check-suite factory confirms there is no prefix on the production-shaped `HashContract`:

`C:/tmp/P030_INTEGRATION_20260913/check_market_data_collector.py:69-71`:

```
def contract(*fields: str) -> subject.HashContract:
    # Fixture values exercise the configurable contract; they are not runtime defaults.
    return subject.HashContract(tuple(fields), "sha256", "utf-8", "json-array-compact")
```

and the observation fields hashed are wire fields plus a few stamps, not the frozen observation tuple (`:83-86`): `"t", "s", "i", "venue", "track", "source_producer", "producer_payload_hash"`.

Adapter grammar:

`C:/tmp/P030_INTEGRATION_20260913/p030_closed_partition_backup_adapter.py:47-48`:

```
_DATASET_ID = re.compile(r"^p030ds-v1:[0-9a-f]{64}$")
_OBSERVATION_ID = re.compile(r"^p030obs-v1:[0-9a-f]{64}$")
```

`C:/tmp/P030_INTEGRATION_20260913/p030_closed_partition_backup_adapter.py:209-213`:

```
        require_non_empty_string(
            record.get("observation_id"), "observation_id", "stable-prefix record"
        )
        if not _OBSERVATION_ID.fullmatch(record["observation_id"]):
            raise ValueError("observation_id must match p030obs-v1 identity")
```

The frozen contract computes a *different digest*, not a prefixed copy of the collector hexdigest:

`C:/tmp/P030_INTEGRATION_20260913/p030_market_data_contracts.py:172-180`:

```
def _canonical_id(prefix: str, domain: str, values: Sequence[Any]) -> str:
    try:
        payload = json.dumps(
            [domain, *values], ensure_ascii=False, allow_nan=False,
            separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractRefused(f"{domain} contains a non-canonical value") from error
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()}"
```

`observation_id` hashes `OBSERVATION_FIELDS` under domain `"p030-observation-v1"` with prefix `"p030obs-v1"` (`:39-43`, `:219-222`). `producer_payload_hash` hashes `PAYLOAD_FIELDS` under domain `"p030-payload-v1"` with prefix `"p030payload-v1"` (`:35-38`, `:187-198`).

Those field tuples are not the collector `HashContract` fields. The hashed array also starts with a domain string the collector never includes. **Stamping `p030obs-v1:` onto the existing hexdigest is therefore not a repair.** It would pass the adapter regex and still fail the contract's load-bearing equality:

`C:/tmp/P030_INTEGRATION_20260913/p030_market_data_contracts.py:324-329`:

```
    payload = {field: row[field] for field in PAYLOAD_FIELDS}
    if producer_payload_hash(payload) != row["producer_payload_hash"]:
        raise ContractRefused("dataset row producer_payload_hash does not match payload fields")
    body = {field: row[field] for field in OBSERVATION_FIELDS}
    if observation_id(body) != row["observation_id"]:
        raise ContractRefused("dataset row observation_id does not match row bytes")
```

`capture_stable_prefix` does *not* recompute `dataset_content_hash` from the rows; it only checks the caller-supplied string against `_DATASET_ID` (`:245-249`). The adapter tests themselves use a regex-only fixture (`check_p030_closed_partition_backup_adapter.py:21`: `DATASET_CONTENT_HASH = "p030ds-v1:" + "a" * 64`). The repair is not complete until collector rows survive `dataset_content_hash(...)`, because that is how a honest capture caller binds the prefix to the frozen identity.

### 1.3 Row *shape* already matches (so this is not a schema redesign)

`DATASET_ROW_FIELDS` is the same 21 names in the same order as `MarketBar`:

`C:/tmp/P030_INTEGRATION_20260913/p030_market_data_contracts.py:53-58`:

```
DATASET_ROW_FIELDS = (
    "observation_id", "producer_payload_hash", "symbol", "interval", "bar_open_time",
    "bar_close_time", "open", "high", "low", "close", "volume", "venue", "track",
    "proxy_source", "source_producer", "observation_type", "supersedes_observation_id",
    "ingest_time", "venue_seq", "env_lineage_id", "schema_version",
)
```

V3 §4.1: "the bridge is a re-identification and re-serialization step, not a schema redesign" (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:510`).

### 1.4 The two halves are not wired together

Collector imports (`market_data_collector.py:9-20`) are stdlib only: no `p030_market_data_contracts`, no adapter. A search of `C:/tmp/P030_INTEGRATION_20260913/*.py` for those module names hits only the check suites (`check_p030_closed_partition_backup_adapter.py:15`, `check_p030_market_data_contracts.py:579/675/732`). `check_p030_opsa_heartbeat_adapter.py:12` imports `p030_opsa_heartbeat_adapter`, a third name; `check_market_data_collector.py:27` is `import market_data_collector as subject`. Each suite can pass against its own fixtures. That is why the contradiction is invisible to the current PASS counts (which this lane did not re-run; see NOT VERIFIED).

Collector runtime remains refused, so there is no production archive to migrate:

`C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py:534-538`:

```
    parser.exit(
        2,
        "REFUSED: Decision 187 authorizes building only; collector runtime requires "
        "a future owner-ratified permission protocol and backend\n",
    )
```

Lifting that refusal is O-6 / C-1, not this repair.

### 1.5 What this repair is *not*

- Not a change to P026 `backup.py` / `restore.py`. The adapter is already "over unchanged P026 backup/restore tools" (`p030_closed_partition_backup_adapter.py:1`).
- Not a change to the frozen prefixes, field lists, or `p030-json-array-v1` canonicalization (`p030_market_data_contracts.py:16-18`, `:35-68`).
- Not a host, schedule, or credential act.
- Not package acceptance of WP-P0-26 or WP-P0-30.

---

## 2. Two design options

V3 O-9 names the fork: "collector writes contract rows directly vs. a separate exporter" (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:586`). A third shape — loosen the adapter to accept unsorted keys and unprefixed ids — is recorded only to reject it.

### Option A — collector writes contract-shaped identities and canonical JSONL (recommended)

**Idea.** Make the live archive the backup-facing partition. One identity space. Adapter, contracts, and P026 tools stay frozen.

**Exact change set (file, function, lines). No code is written here.**

| # | File | Function / site | Lines | Change |
|---|---|---|---|---|
| A1 | `C:/tmp/P030_INTEGRATION_20260913/market_data_collector.py` | module imports | 9-20 | Add `import p030_market_data_contracts`. Today those lines are stdlib only. |
| A2 | same | `normalize_bar` | 215-223 | Stop calling `identities.payload.digest(raw)` and `identities.observation.digest(observation_fields)`. After the already-normalized values exist (`open_time`, `close_time`, decimal-checked OHLC, `venue_seq`, frozen `venue="HYPERLIQUID"` / `track="NATIVE"` / `observation_type="INITIAL"` at `:227-248`), build a `PAYLOAD_FIELDS` mapping and call `p030_market_data_contracts.producer_payload_hash(...)`; build an `OBSERVATION_FIELDS` mapping and call `p030_market_data_contracts.observation_id(...)`. Use those two strings as `MarketBar.producer_payload_hash` and `MarketBar.observation_id`. |
| A3 | same | `MonthlyArchive._append` | 297-300 | Add `sort_keys=True` to the existing `json.dumps(...)` so the written line equals the adapter's canonical re-dump (`p030_closed_partition_backup_adapter.py:197-208`). Keep `ensure_ascii=False`, `allow_nan=False`, `separators=(",", ":")`, and the trailing `"\n"`. |
| A4 | same | `HashContract.digest` / `IdentityPolicy` | 59-86, and constructor `MarketDataCollector.__init__` 338-358 | Retire from the production path. Do **not** "fix" `digest` by prefixing `hexdigest()`: that still omits `_canonical_id`'s domain string (`p030_market_data_contracts.py:174-176`) and still hashes the wrong field tuple. Either delete the types in the same change, or leave them unused for one review cycle. Recommendation: delete them in the same change so a second identity cannot come back. |
| A5 | `C:/tmp/P030_INTEGRATION_20260913/check_market_data_collector.py` | `contract` / `identities_for` | 69-92 | Point collector tests at the frozen contract (or at `normalize_bar` without an injected `HashContract`). The current factory hashes `"t","s","i",...` (`:82-86`) and would hide a regression that re-introduces the bare hexdigest. |
| A6 | capture caller (no file today) | caller of `capture_stable_prefix` | n/a | After A2+A3, compute `dataset_content_hash` with `p030_market_data_contracts.dataset_content_hash(slice_descriptor, observations)` (`:334-380`) over the prefix rows, then pass that string in. This is C-5 orchestration, not a third identity algorithm. |

**Files that must not change in this repair**

- `p030_market_data_contracts.py` — frozen prefixes, field lists, chain rules (`:16-18`, `:35-68`, `:262-312`).
- `p030_closed_partition_backup_adapter.py` — frozen input grammar (`:47-48`, `:197-213`) and "unchanged P026" wrapping (`:1`, `:646-648`, `:706-742`).
- `MTC_COMMAND_CENTER/tools/opsa/{backup,restore,heartbeat,watchdog,opsa_common}.py` — P026 tools.

**Consequences of A**

- After the change, a collector-written `<YYYY-MM>.jsonl` is a legal `capture_stable_prefix` input (serialization + `p030obs-v1` grammar) and a legal `dataset_content_hash` input (digest match).
- `classify_bar` continues to key on `observation_id` / `producer_payload_hash` (`market_data_collector.py:311-314`). Those strings change meaning (contract ids instead of HashContract ids). There is no production archive to migrate: `run` is refused (`:534-538`).
- Collector tests that assert on HashContract-shaped ids must be rewritten (A5). Adapter 44 tests and contract tests stay as they are.
- `IdentityPolicy` injection goes away. That is a collector API change inside P030, not a P026 change.
- Does not lift the runtime refusal (O-6). Does not fill `OPEN-N7` / `OPEN-N8` / `OPEN-N13` / `OPEN-N14` / `OPEN-N17` (`market_data_collector.py:32-52`).
- Does not implement the capture cadence (C-5) or write `p030_opsa_backup_config.json` values (C-4 / O-2). Those remain owner/Lead configuration, not this repair.

### Option B — separate exporter / transform (not recommended as the production path)

**Idea.** Leave the collector bytes alone. Add a new module that reads collector JSONL, recomputes contract identities, re-serializes with `sort_keys=True`, and hands *that* file to `capture_stable_prefix`. This is the GREEN half of D-13 (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:439-445`).

**Exact change set**

| # | File | Function / site | Lines | Change |
|---|---|---|---|---|
| B1 | new file, e.g. `C:/tmp/P030_INTEGRATION_20260913/p030_archive_export.py` (does not exist) | new `export_contract_partition(source_jsonl, dest_jsonl)` | n/a | For each collector line: `json.loads`; map to `PAYLOAD_FIELDS` / `OBSERVATION_FIELDS`; call `producer_payload_hash` / `observation_id`; emit `json.dumps(..., sort_keys=True, separators=(",", ":"))+"\n"`. Refuse extra/missing `DATASET_ROW_FIELDS`. Do not invent OHLC or timestamps. |
| B2 | new check file | tests of B1 | n/a | RED: untransformed collector fixture refused by `capture_stable_prefix`. GREEN: exporter output accepted, and `dataset_content_hash` succeeds. |
| B3 | collector / adapter / contracts / P026 | — | — | Unchanged. |

**Consequences of B**

- Live archive and backup partition become two identity spaces: the exporter *rewrites* `observation_id` and `producer_payload_hash`. A restored backup cannot be replayed through `classify_bar` against the live file and match.
- Every capture depends on remembering to run the exporter. A forgotten transform looks like a collector bug at `_prefix_facts` (`"prefix record is not canonical JSONL"` / `"observation_id must match p030obs-v1 identity"`).
- V3 already fences this transform out of the T-A execution scope: "The GREEN half cannot run under an execution scope alone: **the transform itself is new code and needs the O-9 implementation scope**" (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:445`). Option B *is* that new code, and then it stays in the production path forever.
- Useful as a one-time fixture helper while Option A is in review. Not a production archive design, because the collector is still the evidence store WP-P0-30 places "on disk under WP-P0-26's second-location backup policy" (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:635`).

### Rejected: loosen the adapter

Do not drop `sort_keys` equality or the `p030obs-v1` regex in `_prefix_facts`. That would let non-contract rows into a "stable prefix", contradict the frozen prefixes (`p030_market_data_contracts.py:16-18`, `:219-222`), and make the adapter tests at `check_p030_closed_partition_backup_adapter.py:145-197` lie. P026 tools stay unchanged (`p030_closed_partition_backup_adapter.py:1`). The adapter is the consumer of the frozen contract, not a place to weaken it.

---

## 3. Recommended option

**Recommend Option A.** Offer it as the recommended answer to O-9. The owner still decides.

Why A, stated as reasoning (not a repository rule):

1. The row shape already matches (`MarketBar` `:90-111` vs `DATASET_ROW_FIELDS` `:53-58`). The missing pieces are exactly the two refusals in §1.
2. One identity space: live archive, `dataset_content_hash`, stable-prefix receipt `last_observation_id` (`p030_closed_partition_backup_adapter.py:283`), and later `classify_bar` all see the same `p030obs-v1:` strings.
3. No production archive exists to migrate (`run` refused at `:534-538`).
4. Adapter, contracts, and P026 tools remain frozen — the change sits in the producer, which is where V3 §4.1 places the "unstated prerequisite" (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:508`).
5. Option B leaves the live store un-backup-able and splits identities; WP-P0-30's archive *is* the evidence store being backed up (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:635`).

**Recommended answer to owner item O-9 (not in force until the owner answers):** approve Option A as the production repair, under the T1 review named in §5, with the test list in §4. Option B may exist as a fixture-only helper for D-13 while A is in review; it must not become the production archive path.

This recommendation does not lift C-1's runtime refusal, does not fill any `OPEN-N*` tag, does not install a schedule, and does not authorize G9.

---

## 4. Test list (paper — none run)

Authorization to run these is O-8 (T-A fixtures) plus O-9 (the new code). Under O-8 alone, V3 allows only D-13's RED half (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:445, 550`).

### 4.1 Characterization (RED, current bytes — no new code)

| ID | What | Expected |
|---|---|---|
| T-RED-1 | Collector fixture of one `MarketBar` written through `_append` as shipped, then `capture_stable_prefix` | `ValueError: prefix record is not canonical JSONL` (`p030_closed_partition_backup_adapter.py:208`). This is D-13 RED (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:442-443`). |
| T-RED-2 | Same fixture rewritten with `sort_keys=True` but HashContract ids left bare | `ValueError: observation_id must match p030obs-v1 identity` (`:213`). Proves the two refusals are independent. |
| T-RED-3 | Same fixture with `p030obs-v1:` stamped onto the existing hexdigest, then `dataset_content_hash(...)` | `ContractRefused: dataset row observation_id does not match row bytes` (`p030_market_data_contracts.py:329`) and/or payload mismatch (`:326`). Proves prefix-stamping is not the repair. |

### 4.2 Option A GREEN (after the change set)

| ID | What | Expected |
|---|---|---|
| T-A-1 | `normalize_bar` output: `observation_id` matches `^p030obs-v1:[0-9a-f]{64}$`; `producer_payload_hash` matches `^p030payload-v1:[0-9a-f]{64}$` | grammar + prefix |
| T-A-2 | Round-trip: `observation_id({f: row[f] for f in OBSERVATION_FIELDS}) == row["observation_id"]`; same for `producer_payload_hash` vs `PAYLOAD_FIELDS` | `p030_market_data_contracts.py:324-329` would accept the row |
| T-A-3 | `_append` line bytes equal `json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n"` encoded UTF-8 | adapter `_prefix_facts` `:197-208` would accept |
| T-A-4 | Collector-written fixture → `dataset_content_hash(descriptor, rows)` returns a `p030ds-v1:` id | `:334-380` |
| T-A-5 | That file + hash → `capture_stable_prefix` writes `_P030_STABLE_PREFIX.json` with matching `record_count`, `last_observation_id`, `prefix_sha256` | `:276-290`. This is D-13 GREEN / D-3 on real collector shape. |
| T-A-6 | D-3b: `high_water_bytes` on a record boundary GREEN; mid-record RED `"high-water prefix must end with newline"` (`:182-183`); short read RED `"source prefix is truncated below high water"` (`:262-263`) | C-5 precondition (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:369-374`) |
| T-A-7 | D-4 / D-5 / D-6 / D-7 against the collector-shaped prefix | existing adapter guarantees, now on producer bytes rather than `_line()` fixtures (`check_p030_closed_partition_backup_adapter.py:27-36`) |
| T-A-8 | `classify_bar` IDENTICAL_REPLAY still no-ops when the same contract ids re-arrive; different payload bytes with the same id still refuse (`market_data_collector.py:311-314`) | restart semantics, C-12 / O-7, still fail-closed |
| T-A-9 | Existing collector behavioural tests (universe, forming-bar skip, gap fill, `run` refusal) stay GREEN after A5 updates | no behaviour change outside identity + serialization |
| T-A-10 | `check_p030_closed_partition_backup_adapter.py` 44 `test_*` methods, `check_p030_market_data_contracts.py`, `check_p030_opsa_heartbeat_adapter.py` 10 methods, `test_opsa.py` 33 methods — unchanged GREEN | no P026 / contract / heartbeat regression. Counts verified by reading `def test_` lines; PASS results are NOT VERIFIED (not run). |
| T-A-11 | Negative: a HashContract-style unprefixed line still refused by `_prefix_facts` | adapter grammar remains frozen |
| T-A-12 | Import graph: `market_data_collector.py` now imports `p030_market_data_contracts`; it still must not import the backup adapter or any `tools/opsa` module | producer depends on the frozen contract, not on P026 |

### 4.3 If the owner picks Option B instead

| ID | What | Expected |
|---|---|---|
| T-B-1 | Untransformed collector fixture still T-RED-1 | producer unchanged |
| T-B-2 | Exporter output satisfies T-A-1..T-A-5 | backup-facing partition only |
| T-B-3 | Explicit mismatch test: live `observation_id` ≠ exported `observation_id` for the same bar | documents the split identity space so it cannot be papered over |

### 4.4 Out of this repair's test list

D-8..D-10 heartbeat/watchdog, D-16 phone, D-17 host-loss, D-15 real-store, D-14 real-feed gap-backfill. Those are P026/P030 operational drills, not the §4.1 identity bridge. They stay on V3's dependency graph (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:476-489`).

---

## 5. Review tier

- **This repair is T1.** WP-P0-30: "Audit tier: **T1** for the collector/feed code; host-install steps **T0**" (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:640`). The change set is collector identity + serialization. It does not execute on KVM2.
- **It is not T0 and not G9.** Host contact stays behind the owner's per-session authorization (`:640`, and WP-P0-26 `:584`). Implementing A does not install a collector, a schedule, or a backup root.
- **P026 tooling tier is unchanged T1** for local tools (`:584`; `LANE_REPORT.md:12-13`). This repair must not edit those tools.
- **Contracts stay frozen** — no T2 "schema redesign" is opened. If a later change proposed to edit `PAYLOAD_FIELDS` / `OBSERVATION_FIELDS` / prefixes, that would be a different, wider review. Option A does not do that.
- **Implementation may not start without O-9.** V3: "It is new code with a design choice … and needs its own review tier" (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:586`). This document is the design; it is not that authorization.
- **G1-IA still gates collector *runtime*** (WP-P0-30 amendment, `:632`: "G1-IA is still required to start (D-12)"). Option A does not start the collector.

---

## 6. Sequencing against V3 (not re-decided)

```
O-9 owner answer (this design)
  → T1 implementation of Option A (or B if the owner picks it)
    → O-8 T-A: D-13 GREEN, then D-3 / D-3b / D-4 / D-5 / D-6 / D-7
      → C-5 daily high-water + month-end capture remains the plan's ratified cadence
        (MASTER_WORK_PACKAGE…:580, :581(b); V3 C-5). Monthly-only remains an owner departure (O-2).
      → Real-store D-15 and G9 install remain later, separately authorized.
```

C-1's coded refusal, C-8's unratified silence bound, C-10's notifier, and C-11's state-dir transport are not part of this repair.

---

## 7. NOT VERIFIED (this document)

| Ref | Not verified | Why |
|---|---|---|
| NV-D1 | That T-RED-1 actually raises on a collector-written file | Derived from the production modules; this lane executed nothing. D-13 is the empirical close. Same residual as V3 NV-8. |
| NV-D2 | PASS results of any check suite | Methods were counted by reading `def test_`; no test runner was invoked. |
| NV-D3 | That no other importer of the collector exists outside the inspected `C:/tmp/P030_INTEGRATION_20260913/*.py` tree | Search was bounded to that tree. |
| NV-D4 | Any live archive on KVM2 or elsewhere | Collector `run` is refused; deployed host state is `UNVERIFIED` pending G9 (`MASTER_WORK_PACKAGE…:581`). This lane contacted no host. |

---

**End of design.** No code written. No option is in force until the owner answers O-9.
