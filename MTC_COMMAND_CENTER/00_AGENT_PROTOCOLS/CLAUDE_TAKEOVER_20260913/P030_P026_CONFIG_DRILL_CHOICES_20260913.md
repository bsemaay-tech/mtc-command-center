<!-- LEAD AUDIT NOTE (Claude Fable Lead, 2026-09-13 13:13Z) -->
> **Lead audit of lane P30D deliverable** (source `C:/tmp/CLAUDE_P0_RUN_20260913/laneP30D_luna/P030_P026_CONFIG_DRILL_CHOICES_DRAFT.md`, SHA-256 `19958357ec6964e25f11447130386f350d1a8dc2a85a1aaf04e62afc2a42a9ca`, produced by an independent Claude Max claude-opus-5 xhigh lane, 63 turns, read-only).
> Mechanical citation check: 288 `[KEY]:line` / `[WT] file:line` citations resolved against the named files; 0 out of range, 0 missing files.
> Claim table tally: 21 VERIFIED, 5 PARTLY VERIFIED, 2 CONTRADICTED (in part), 2 CONTRADICTED. Lead re-verified both full CONTRADICTED rows against bytes: row 31 (collector `_append` at `market_data_collector.py:294-306` writes without `sort_keys`; adapter at `p030_closed_partition_backup_adapter.py:197-208` refuses non-`sort_keys` canonical lines) and row 35 (`C:/CT13/DECISIONS.md` has zero matches for P030/P0-30/P026/P0-26/OPS-A/VEN-E/watchdog/heartbeat).
> Status: DRAFT decision packet for owner. Contains no acceptance decision, no host/account/deployment action, no executed drill. Owner items O-1..O-10 are open decisions; nothing acted on. This note is a Lead audit record, not owner ratification.
> Recorded in CT13 working tree only; commit deferred until the Gemini quiet-window guard is idle.

# P030 / P026 — configuration and drill choices (draft), with verification of Luna's decision packet

**Lane:** P30-LUNA · **Role:** independent drafting analyst (`claude-opus-5`, xhigh). Not a reviewer, not an implementer, not the Lead.
**Owner authorization (chat 2026-09-13):** "Use Luna's corrected P030/P026 packet at `C:/tmp/P030_P026_LUNA_PREP_20260913/DECISION_PACKET.md`. Prepare concrete configuration/drill choices and verify unresolved claims. No deployment or host/account actions."

**What was done here.** Read-only inspection of the packet, the two handoffs, the merged P030 worktree, the P026 tooling and the plan/decision indexes. **Nothing was executed**: no test run, no tool invocation, no runtime start, no network, no host, no credential, no Git mutation, no `git status`/`git diff`. Every drill in section 3 is a **paper plan**; none was started.

## Verification basis (identities checked, not assumed)

| Item | Verified value | How |
|---|---|---|
| P030 worktree HEAD | `f42fd5400b2c2ecb805644d406999cb55c8178c8` on `feature/p030-integrated-20260913` | `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD` in `C:/tmp/P030_INTEGRATION_20260913` — matches [HO]:9 and the brief |
| CT13 control checkout | branch `feature/claude-takeover-20260913`, HEAD `70274964fb6b4795754f04eb56d1ce183f61d065`, exactly three docs commits ahead of `fcac0ac67cf2682693ad28138b1a56e15a0846f2` | `git rev-parse`, `git log --oneline fcac0ac6..HEAD` |
| Closeout commit | `d90150ba6978ec5eaa69febd5bfd113282a8aaf1` = "Merge pull request #189 …", and an ancestor of `fcac0ac6` | `git log --oneline -1 d90150ba`, `git log --ancestry-path d90150ba..fcac0ac6` |
| P030 merge | `62a42514793f192ca4f706ca99cc2700b16300fe` = "Merge pull request #187 from bsemaay-tech/feature/p030-integrated-20260913" | `git log --oneline -8 --name-only 62a42514` |
| CT13 copies vs merged worktree | **byte-identical** for all ten inspected files | SHA-256 of both copies (table below) |
| Handoff copies | `C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md` and the CT13 mirror are byte-identical (`fec60cc9…`); same for `START_HERE.md` (`b890d7fc…`) | SHA-256 |

SHA-256 of the inspected sources (identical in `C:/CT13/` and `C:/tmp/P030_INTEGRATION_20260913/`):

| File | SHA-256 |
|---|---|
| `p030_closed_partition_backup_adapter.py` | `57cb9979d787e5049f3123c9e68cbdb4a1742e7890424ef5e088d3aa8cd8d341` |
| `p030_market_data_contracts.py` | `1c2c23933b6650394137074c537b684b3e360d50667e87bb2473cadbf409e185` |
| `p030_opsa_heartbeat_adapter.py` | `bf3c5032cf2d5a1e0464ad8db1645be66546c6578c9d0c995daa5709c6c960a9` |
| `p030_opsa_backup_config.json` | `52d36c953026da678a7a38a2922cfd1ce1db5945ae1e15b82afa1a00176983a9` |
| `market_data_collector.py` | `377c0eb6de7bc8b6a575354d1fc1ec40beed6a3c1ba794cc10979a26f1607b27` |
| `MTC_COMMAND_CENTER/tools/opsa/watchdog.py` | `0d4ba79dc4cedc32128a13943332f7574aa3a459cacaf399b81ee4dbe785376a` |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | `4c4157191a36885274355267cac953347088b973445b0139219831d2025ed778` |
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | `c2aecdacbca41ea5476438da73b4f078382728605cd709b8f8a7cc2f1d0f7996` |
| `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py` | `38b43d72548de0496be40502b98b9ff8e7c019706d467da2a6c109d13ac507e6` |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | `69054441f308851e869a6b2fc68758c5fd92d18931ba3bb77e66e5eca9f48dc1` |

Because the CT13 copies and the merged P030 worktree are byte-identical, the packet's `CT13 …` citations and this draft's `[WT] …` citations address the same bytes, and the line numbers are interchangeable.

---

## 1. Claim verification table for Luna's packet

Verdicts: **VERIFIED** (checked against the named bytes), **CONTRADICTED** (the source says something materially different), **PARTLY VERIFIED** (true as stated but incomplete or imprecise in a way that would mislead a next agent), **UNVERIFIABLE-HERE** (cannot be settled without an action this lane must not take).

| # | Claim (packet line) | Source checked | Verdict | Note |
|---|---|---|---|---|
| 1 | Basis: read-only review of current integrated CT13, `feature/claude-takeover-20260913`, based on `fcac0ac6`; no host/network/provider/deployment/test/Git/memory action ([PKT]:3) | CT13 `git rev-parse --abbrev-ref HEAD`, `git log --oneline fcac0ac6..HEAD` | VERIFIED (identity) / UNVERIFIABLE-HERE (conduct) | Branch and base confirmed; CT13 HEAD is `70274964`, three docs commits above `fcac0ac6`. Whether the preparation itself took no action cannot be checked from here. |
| 2 | Source key: `P021_P030_HANDOFF.md`, `LANE_REPORT.md`, `NOTIFIER_PROPOSAL.md`, `RESTORE_DRILL_EVIDENCE.md`, `watchdog.py`/`restore.py`/`heartbeat.py`, `C:\CT13\p030_*.py` and `market_data_collector.py` ([PKT]:5) | Directory listings of all five locations | VERIFIED | All named files exist at the stated paths. |
| 3 | Same source key, applied to `p021_readiness_rules.py` (cited as `CT13 p021_readiness_rules.py` at [PKT]:23) | `find /c/CT13 -name "*readiness*"` | PARTLY VERIFIED | The file is **not** at the CT13 root implied by the key; it is `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` [RR]. Contents and line numbers are correct; only the implied path is. |
| 4 | Restart handling "classifies identical replay before returning" ([PKT]:9) | [WT] `market_data_collector.py`:416-425 | VERIFIED | `ingest` calls `classify_bar`; on `IDENTICAL_REPLAY_NOOP` it seeds/advances the WS cursor with `max(previous, bar_open_time)` and returns the bar without appending. |
| 5 | Observation, event, correction-chain, provenance and dataset/manifest identities are implemented ([PKT]:9) | [WT] `p030_market_data_contracts.py`:187-198, 219-222, 225-259, 262-312, 334-380, 391-470 | VERIFIED | Six identity/validation entry points exist with the frozen prefixes `p030payload-v1`, `p030obs-v1`, `p030evt-v1`, `p030ds-v1`, `p030prov-v1`. |
| 6 | The P026 heartbeat payload is consumed through a P030 adapter ([PKT]:9) | [WT] `p030_opsa_heartbeat_adapter.py`:12-22, 59-72, 75-115 | VERIFIED | The adapter imports the unchanged `heartbeat`/`opsa_common` modules and re-validates the exact P026 field set `{schema,id,seq,emitted_at,pid}` + optional `note`. P030-only signals go to a separate `*.health.json` sidecar (130-174), so the P026 payload is not extended. |
| 7 | Closed-partition backup/restore is wrapped with stable-prefix and verified-restore receipts ([PKT]:9) | [WT] `p030_closed_partition_backup_adapter.py`:33-34, 220-290, 625-679, 682-816 | VERIFIED | `_P030_STABLE_PREFIX.json` is written at capture (276-290); `_P030_VERIFIED_RESTORE.json` is written after a verified restore (796-816). |
| 8 | The handoff records collector/contracts PASS, backup `44/44`, heartbeat `10/10`, unchanged P026 `33/33` ([PKT]:9) | [HO]:32; [GH]:10; test-method counts in [WT] `check_p030_closed_partition_backup_adapter.py`, `check_p030_opsa_heartbeat_adapter.py`, `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | VERIFIED (record + counts) / UNVERIFIABLE-HERE (results) | The handoff says exactly that. The three suites contain exactly **44**, **10** and **33** `def test_…` methods, so the denominators are real, not rounded. The PASS results themselves cannot be re-established here — no execution is authorized in this lane. |
| 9 | The handoff "explicitly says this is an implementation milestone rather than package acceptance" ([PKT]:9) | [HO]:37 | VERIFIED | "Completed merges are scoped implementation milestones, NOT P021/P030 package acceptance or readiness." Same wording at [GH]:16. |
| 10 | Contracts freeze `sha256`, `p030-json-array-v1`, `mtc.p030_event/v1`, exact field lists and correction-chain rules ([PKT]:9) | [WT] `p030_market_data_contracts.py`:16-18, 35-68, 262-312 | VERIFIED | `ALGORITHM="sha256"` (16), `CANONICALIZATION_VERSION="p030-json-array-v1"` (17), `EVENT_SCHEMA_VERSION="mtc.p030_event/v1"` (18); seven exact field tuples (35-68); chain rules forbid a second INITIAL per slot (281-284), a missing predecessor (293-295), cross-slot corrections (296-299), forks (300-301) and cycles (304-311). |
| 11 | P026's report describes backup copies/hashes, restore verification, payload-time heartbeat checks and checker-level failure events ([PKT]:11) | [LANE]:29-53; [WT] `MTC_COMMAND_CENTER/tools/opsa/watchdog.py`:1-35 | VERIFIED | The watchdog docstring states the six per-id states and the synthetic `_watchdog_check` checker-level event (30-35), implemented at 162-163, 193-196. |
| 12 | The report "reports 23/23 final checks and fixture drills" ([PKT]:11) | [LANE]:112-114 (and :49, :93) | PARTLY VERIFIED | Line 114 does say `(23/23)`. But the same report says "19-test suite" (49) and "Ran 19 tests" (93), and the **current** `test_opsa.py` holds **33** test methods. The `23/23` figure is a 2026-08-25 snapshot that no longer describes the shipped suite; the packet's own conclusion ("the old report cannot establish that no coding remains") is the right one, and this row is the arithmetic behind it. |
| 13 | Acceptance is still open because phone-push and G9-gated host-install evidence have not happened ([PKT]:11) | [LANE]:5-13; [WT] `MTC_COMMAND_CENTER/tools/opsa/README.md`:4-6; [PLAN]:585 | VERIFIED | [PLAN]:585 makes the phone push the acceptance test: "the watchdog is proven by **killing a watched heartbeat and receiving the push on the owner's phone**". |
| 14 | P030 needs a concrete backend, permission/operating policy, archive root and store identities, restart-first-message closure beyond identical replay, P026 monitoring/delivery acceptance and separately authorized host work ([PKT]:15) | [HO]:40 | VERIFIED | Quoted almost verbatim from the handoff. |
| 15 | The shipped watchdog requires an explicit `--silence-seconds`; it has no ratified default ([PKT]:16) | [WT] `MTC_COMMAND_CENTER/tools/opsa/watchdog.py`:241-246 | VERIFIED | The code comment states the former `900.0` "carried a provenance claim citing a plan item that does not ratify any such value"; the argument is now `required=True`. Note the README usage example still shows `--silence-seconds 900` (`README.md`:68) — an example, not a ratified value; a next agent must not mistake it for one. |
| 16 | No runtime start, deploy, credentials, venue contact, TESTNET/mainnet, ARM/order action, or readiness/acceptance authority exists ([PKT]:17) | [HO]:41; [GH]:18; [SH]:48 | VERIFIED | Also enforced in code: the collector's `run` subcommand exits 2 with "REFUSED: … collector runtime requires a future owner-ratified permission protocol and backend" ([WT] `market_data_collector.py`:534-538). |
| 17 | The handoff verifies that P012/P020 acceptance dependencies, four fail-closed P021 limits, B-12 and qualifying forward evidence remain open ([PKT]:21) | [HO]:39; [RR]:166, 232 | VERIFIED | The four named limits are exactly the four open numbers wired into the readiness rules: `gap_ratio_max` ([RR]:166, 202) and `divergence_tolerance` / `divergence_window_length` / `divergence_min_paired_observations` ([RR]:232). |
| 18 | "The exact primary requirement that starts a countable forward-observation clock … was not located in this bounded search; therefore the start prerequisite is **UNVERIFIED**" ([PKT]:21) | [PLAN]:581, 585, 641, 750; [SH]:51 | CONTRADICTED (in part) | A clock **gating** requirement is locatable and explicit: "**no forward clock (WP-V2A-08 shadow window or WP-V2B-07 lane) may start before this package is accepted** — that clock-gating edge is part of this gate, not advice" ([PLAN]:585), plus "A backup counts only after an isolated restore proves integrity, readability and reconciliation; that proof is required **before any forward clock**" ([PLAN]:581(c)), WP-V2A-08's dependency on P026 and P030 ([PLAN]:750) and P030's "accepted before WP-V2A-08 starts" hard edge ([PLAN]:641). What remains genuinely unlocated is a rule naming the **clock-start event itself** (which admitted observation timestamp starts the count). Section 4 uses the located gates and keeps the start event open. |
| 19 | Derived balanced-profile `day_forward_period = 21 days`, day minimum 20 trades, swing 119 days / 12 trades, position 364 days / 12 trades ([PKT]:23) | [RR]:96-101 (20 trades), 102-111 (21 days), 112-124 (119 days / 12), 125-139 (364 days / 12) | VERIFIED | The 21 is `max(T_count 20.1 d, T_cycle 4 d, T_operational 14 d)` rounded to three weeks; the source note itself records that the owner-facing summary table says a four-week median wait ([RR]:106-111). |
| 20 | "That is a profile rule, not evidence that a clock has started, and must not be presented as a measured '21-day requirement'" ([PKT]:23) | [RR]:102-111 | VERIFIED | The field's own justification text is derivational, and two of the four profile periods are flagged `extrapolated=True` ([RR]:130, 138). |
| 21 | "P021's readiness code refuses if forward evidence numbers are not closed" ([PKT]:23) | [RR]:237-245, 288-295 | PARTLY VERIFIED | `validate_catalog` raises if any member of `FORWARD_EVIDENCE_NUMBER_NAMES` is absent from the closed catalogue (288-291) and if any rule "could be presented as ready" (293-295). This is a **catalogue self-validation** run at record build time, not a per-observation admission gate; the wording should not be read as a runtime evidence check. |
| 22 | Archive root / machine: CT13 config has `backup_root: null` and store `id`/`path: null`; no infrastructure value is verified ([PKT]:29) | [WT] `p030_opsa_backup_config.json`:3, 6, 7; `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py`:227-245 | VERIFIED, and stronger than stated | The nulls are not merely "unset": `load_backup_config` calls `require_non_empty_string_field` on `backup_root` and on every store `id`/`path`/`class` (232-239), so the shipped config **cannot load at all** — every backup, restore and adapter entry point fails closed on it today. |
| 23 | Backup store identity: the adapter enforces confined paths and stable-prefix receipts; use closed monthly partitions, then `--check-only` and per-file SHA-256 read-back before replay ([PKT]:30) | [WT] `p030_closed_partition_backup_adapter.py`:220-290, 625-679, 682-758; `MTC_COMMAND_CENTER/tools/opsa/restore.py`:1-17; `opsa_common.py`:170-224 | PARTLY VERIFIED | Confinement and receipts: verified. Two corrections: (a) `restore_verified_prefix` **already** runs `--check-only` and then the restore internally, against an isolated temp copy of the backup root (703-742) — it is not a separate operator step; (b) "closed monthly partitions" is the **collector's** archive layout `bars/<venue>/<symbol>/<interval>/<YYYY-MM>.jsonl` ([WT] `market_data_collector.py`:268-276), not something the adapter knows about — the adapter only sees a caller-supplied `high_water_bytes` prefix and refuses to infer closure ([WT] `p030_closed_partition_backup_adapter.py`:229). |
| 24 | Heartbeat identity: the adapter requires a non-empty caller-supplied ID and writes the exact P026 payload ([PKT]:31) | [WT] `p030_opsa_heartbeat_adapter.py`:59-72; `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py`:43-54 | VERIFIED | Adds a verified constraint the packet does not state: the id becomes a filename component through `resolve_confined_path(state_dir, f"{id}.hb.json")`, and the watchdog only discovers `state_dir/*.hb.json` at the top level ([WT] `watchdog.py`:137-138) and splits `--expect` on commas (276). So the id must be a **single path segment with no `/`, `\`, `..`, URL-escape or comma**. |
| 25 | Watchdog bound: owner ratifies the operational bound, then every scheduled invocation passes it explicitly; N14 detection is separate from phone delivery ([PKT]:32) | [WT] `watchdog.py`:245-246; `market_data_collector.py`:48 | PARTLY VERIFIED / imprecise | The ratification and explicit-pass points are verified. The N14 sentence is imprecise: `OPEN-N14` is "What is the **maximum allowed time from collector failure detection to owner notification delivery**?" — it *spans* detection to delivery. What is genuinely separate is the watchdog's `--silence-seconds` (a detection-side bound) from N14's end-to-end detect→deliver bound; the two must not be conflated in either direction. |
| 26 | Phone channel: the Aug-25 proposal is "a dated candidate comparison, **not a current recommendation**" ([PKT]:33) | [NOTIF]:1-11, 48-59, 76-85, 87-96 | CONTRADICTED (in part) | The document does state a recommendation: "**Primary: self-hosted ntfy on the owner PC**" (50), a fallback ("public ntfy.sh with a long random topic", 76), a contingency (Telegram, 81) and a rejection (Pushover, 83-85). What the document itself qualifies is narrower: external facts are "as-known 2026-08-25 and must be re-verified at adoption time" (9-11) and the latency bound stays `[OPEN]` (5-7, 41). Treating it as "no recommendation exists" would discard a usable owner input; treating its facts as current would be equally wrong. |
| 27 | Latency remains open until a real drill ([PKT]:33) | [NOTIF]:41, 94-96; [PLAN]:585 | VERIFIED | "Until that drill runs, WP-P0-26 acceptance stays OPEN by definition" ([NOTIF]:96). |
| 28 | Event/correction identities: no owner numeric decision is needed now; schema/version and correction predecessor/successor requirements are frozen ([PKT]:34) | [WT] `p030_market_data_contracts.py`:18, 225-259, 262-312 | VERIFIED | A `CORRECTION` event requires exactly two observation ids (248-249); a `CORRECTION` observation must carry a `p030obs-v1`-prefixed predecessor (215-216); an `INITIAL` must carry none (213-214). Nothing numeric is left to choose in this area. |
| 29 | P030 operational tags: keep N8/N13/N17 and delivery latency unset ([PKT]:35) | [WT] `market_data_collector.py`:32-52 | VERIFIED | The module states "exactly these seventeen tags remain open after decisions 104-109" and the dict contains exactly 17 entries, including `OPEN-N8` (43), `OPEN-N13` (47), `OPEN-N14` (48) and `OPEN-N17` (49). |
| 30 | Cannot yet recommend a deployment command, host path, schedule, phone latency bound, endpoint, credentials or restore-to-production procedure ([PKT]:37) | [HO]:40-41; [PLAN]:584, 640; [LANE]:15-22 | VERIFIED | [PLAN]:584 and :640 map the host steps to gate `G9`, "requires the owner's authorization per session", "nothing here is authorized". |
| 31 | Minimal next sequence step 3: "backup closed partitions and record manifest/hash/read-back evidence" ([PKT]:49) | [WT] `market_data_collector.py`:66-80, 90-111, 294-306; `p030_closed_partition_backup_adapter.py`:47-48, 181-217 | **CONTRADICTED** (executability) | The step is not currently executable against a collector-written partition. Two independent, byte-level refusals (details in §4.1): (a) the adapter requires every prefix line to equal `json.dumps(record, …, sort_keys=True, separators=(",",":"))+"\n"` (197-208), while the collector writes `asdict(bar)` in dataclass declaration order with **no** `sort_keys` (294-306 with 90-111); (b) the adapter requires `observation_id` to match `^p030obs-v1:[0-9a-f]{64}$` (47-48, 209-213), while the collector's `HashContract.digest` returns a **bare** hexdigest with no prefix (66-80). |
| 32 | Step 5: "stop if the checker is not external to the watched host" ([PKT]:51) | [PLAN]:580; [NOTIF]:19-21 | VERIFIED | The plan requires "a checker **outside the watched host**" and the proposal's criterion 3 restates it. |
| 33 | Unverified critical claim: no live host, endpoint capability, phone delivery latency, real archive backup, or P021 qualifying forward-observation interval was verified ([PKT]:56) | Whole-lane observation | VERIFIED (and re-affirmed) | This lane verified none of those either, and was not authorized to. |
| 34 | Implied by the packet's Basis line and §4: P021/P030 work may proceed as "existing scope" ([PKT]:3, 41) | [HO]:52-56 | PARTLY VERIFIED | The handoff's standing state is "**remain parked** … Do not resume P021/P030 unless the owner grants a new bounded scope or asks for a status refresh" ([HO]:52-54). The 2026-09-13 owner authorization quoted at the top of this file **is** such a bounded scope — but it is read-only preparation, and it does not reopen the parked implementation lane. Any next agent must cite that authorization, not the packet, as its basis. |
| 35 | Brief's expectation that `C:/CT13/DECISIONS.md` carries rows naming P030 / P026 / decision 6 / decision 7 | [DEC] full-file grep for `P030`, `P026`, `P0-30`, `P0-26`, `OPS-A`, `VEN-E`, `watchdog`, `heartbeat`, `decision 6`, `decision 7`, `1 YES, 2 YES` | **CONTRADICTED** | `DECISIONS.md` contains **no** such row. The owner answers `1 YES, 2 YES, 3 A, 4 YES, 5 YES, 6 A, 7 A` are recorded only in the two handoffs ([HO]:16; [GH]:5), and the substance of decisions 6 and 7 only at [GH]:16 ("Decision 6 keeps unmeasured limits unset and fail-closed. Decision 7 retains WS-only restart continuity; it does not prove every restart-first-message case or a production backend"). **Consequence:** the P021/P030 owner decisions are not in the durable decision index; they live in handoff prose. That is a records gap the owner may want closed, and it is why this draft cites `[GH]:16` rather than a decision id. |

---

## 2. Configuration choices

Scope: every configuration the **P030 runtime** and the **P026 backup/monitoring** need before any host work. Each entry names the decider — **OWNER** (a value or authority no agent may pick) or **LEAD DEFAULT** (a value the Lead may fix inside the existing contracts, which the owner may override) — the options with their consequences, and **one** recommendation.

Concrete candidate values below are **drafting proposals for owner review**, exactly as the packet's §3 anticipates ([PKT]:29-31). None is a repository fact, none has been written into any config file, and none authorizes a host act.

### C-1 · Collector backend and permission protocol — OWNER

The collector's `run` subcommand takes `--permission-packet PATH` and `--owner-approved-start-decision INT` and then refuses unconditionally: "REFUSED: Decision 187 authorizes building only; collector runtime requires a future owner-ratified permission protocol and backend" ([WT] `market_data_collector.py`:524-538). The refusal is not conditional on the arguments — it is reached for every `run` invocation.

| Option | Consequence |
|---|---|
| A. Ratify a permission protocol + backend now | Requires a backend decision, a `PublicMarketSource` implementation ([WT] `market_data_collector.py`:139-155) and a code change to lift the refusal — a new implementation lane with its own review. The venue is already hard-coded `HYPERLIQUID`, track `NATIVE` (215-249), so "backend" means the transport/client, not the venue. |
| B. Leave the refusal in place; use only the offline `gap-report` path | Keeps the collector inert. `gap-report --archive <root> [--symbol BTC] [--interval …]` is the only executable subcommand and touches no network (496-533). Costs one retention day per day of delay ([PLAN]:633: the venue serves ≈5000 candles per interval; 15m ≈ 52 days). |

**Recommendation: B for this lane; put A to the owner as a separate scope request (§5, O-6).** Lifting a coded refusal is an implementation act with its own review; it must not ride along on a configuration draft. The retention cost of waiting is real and belongs in the owner's decision, not in an agent's discretion.

### C-2 · Collector operating policy (universe, cadence, gap-fill) — LEAD DEFAULT inside a frozen universe

The universe is frozen in code: `INITIAL_SYMBOLS = ("BTC",)` and intervals `15m/1h/4h/1d` ([WT] `market_data_collector.py`:23-30); `normalize_bar` refuses anything outside it (198-199).

| Setting | Options | Recommendation |
|---|---|---|
| `BackfillPolicy.batch_size` / `inter_request_seconds` | Any positive int / any finite non-negative float, both validated at construction (128-136); both are `OPEN-N7` — "What snapshot batch size and inter-request pacing should be used?" (42) | **Do not fix them now.** They are venue-pacing values; choosing them before the backend exists would answer an `OPEN` tag. Carry them as C-1's dependants. |
| Bar admission | Fixed by code: a bar whose `close_time > ingest_time` returns `None` (204-205) — forming bars are never archived | Ratify as-is; it is the closed-bar discipline P021 also requires. |
| Gap handling | Fixed by code: `detect_gap` refuses non-increasing or off-interval sequences (252-261); `_fill_gap` pages `candles_snapshot` and refuses if a page returns nothing, if the cursor fails to advance, or if any bar is still missing afterwards (438-479) | Ratify as-is. |

**Recommendation: adopt the coded policy unchanged and leave `OPEN-N7` unset**, because filling it is the same class of act as filling `N8/N13/N17`, which both [PKT]:35 and [WT] `market_data_collector.py`:32-33 forbid.

### C-3 · Archive root — OWNER (Lead drafts the shape)

The archive root is the `MonthlyArchive(root)` argument; the layout under it is fixed: `bars/<venue>/<symbol>/<interval>/<YYYY-MM>.jsonl`, every segment passed through `_SAFE_PART = ^[A-Za-z0-9._-]+$` ([WT] `market_data_collector.py`:264-276, 54, 158-161). Files are opened `O_APPEND|O_CREAT|O_WRONLY` mode `0o600` and fsynced per record (294-306).

| Option | Consequence |
|---|---|
| A. Archive root on the collector host (KVM2) | Matches [PLAN]:635 ("the archive on disk under WP-P0-26's second-location backup policy"), but every path value is a host fact this lane cannot verify, and any write there is a `G9` act ([PLAN]:640). |
| B. Archive root on the owner PC | Removes the host gate for the archive itself but contradicts [PLAN]:635, and the collector would then have to run off-host. |
| C. Leave the root unbound; parameterize per invocation | The archive root is a plain constructor argument with no config file, so this costs nothing today and defers the host fact. |

**Recommendation: C now, A as the ratified target.** Record the target as a named placeholder — `<ARCHIVE_ROOT>/bars/HYPERLIQUID/BTC/<interval>/<YYYY-MM>.jsonl` — and have the owner supply the concrete volume at the moment the `G9` host step is authorized, so no stale path is baked in. **Owner input needed:** volume and free-space budget (§5, O-1).

### C-4 · Backup store configuration (`p030_opsa_backup_config.json`) — OWNER for the values, LEAD DEFAULT for the shape

Verified constraints that bound every possible answer:

1. `backup_root` and every store's `id`, `path`, `class` must be **non-empty strings**; the shipped file has `null` for all four, so it cannot load ([WT] `p030_opsa_backup_config.json`:3, 6, 7; `opsa_common.py`:227-245).
2. The store `id` is a path component at load time (`runs/_config_check/<id>`, `opsa_common.py`:242-243), at backup time (`runs/<run_id>/<store_id>/<rel>`, `backup.py`:149) and at restore time (`<target>/<store_id>/<rel>`, `restore.py`:181). It must be a confined relative component: **one segment, no `/`, `\`, drive letter, `..` or URL-escaped `..`** (`opsa_common.py`:170-224).
3. For the P030 adapter the `class` must be exactly `protected`, exactly one store may match the given `store_id`, and the store's `path` must **resolve equal to the stable-prefix directory** ([WT] `p030_closed_partition_backup_adapter.py`:393-407).
4. `capture_stable_prefix` refuses if the stable-prefix directory already exists, then creates it ([WT] `p030_closed_partition_backup_adapter.py`:256-257, 267). **The store `path` therefore cannot be a fixed directory reused across captures** — it names a directory that must not exist before its own capture.

| Option | Consequence |
|---|---|
| A. One long-lived config with a fixed store `path` | **Impossible** under constraints 3+4: the path must equal a directory that must not pre-exist. The first capture would succeed; the second would refuse. |
| B. One config **generated per capture**, pointing at that capture's stable-prefix directory, all sharing one `backup_root` (hence one append-only `manifest.jsonl` and distinct timestamped `run_id`s, `opsa_common.py`:80-87) | Works with the code as shipped. Restores stay addressable by `run_id`, and `restore_verified_prefix` re-validates only class/uniqueness in the restore direction ([WT] `p030_closed_partition_backup_adapter.py`:685 with 393-407), so an old per-capture config stays usable later. |
| C. Several stores in one config | Legal — ids must be unique (`opsa_common.py`:240-241) — but the adapter requires exactly one match for its `store_id`, and a `--store`-less P026 invocation would widen the blast radius. |

**Recommendation: B, with a fixed store `id` and a per-partition stable-prefix directory.** Draft shape for owner review:

```
{
  "schema": "mtc.opsa_backup_config/v1",
  "backup_root": "<BACKUP_ROOT>",
  "stores": [
    { "id": "p030_closed_partition",
      "path": "<STABLE_PREFIX_ROOT>/HYPERLIQUID/BTC/1h/2026-09",
      "class": "protected" }
  ]
}
```

`backup_root` — OWNER, the second location, not the archive volume. `id` — LEAD DEFAULT, one segment, stable across captures. `path` — per capture, must not exist before capture. `class` — `protected` is required by the adapter. `<BACKUP_ROOT>` must sit on a **different device or host** from `<ARCHIVE_ROOT>`; that is the point of [PLAN]:580 ("automated second-location copy for every evidence store (cross-copy VPS ↔ owner PC)"). **Owner input needed:** both roots (§5, O-1, O-2).

### C-5 · Stable-prefix capture parameters — LEAD DEFAULT with one owner-visible consequence

`capture_stable_prefix(source_jsonl, stable_prefix, *, source_root, high_water_bytes, captured_at_utc, dataset_content_hash)` ([WT] `p030_closed_partition_backup_adapter.py`:220-290) requires:

- `high_water_bytes` — a positive int; exactly that many bytes are read and the read must not come up short (242-243, 260-263). **The adapter refuses to infer closure** (229): the caller supplies the byte count it knows is closed.
- `captured_at_utc` — a caller-supplied `…Z` timestamp with whole seconds (131-139, 244).
- `dataset_content_hash` — must match `^p030ds-v1:[0-9a-f]{64}$` (47, 248-249), i.e. it must come from `p030_market_data_contracts.dataset_content_hash()` ([WT] `p030_market_data_contracts.py`:334-380).
- The source must be a regular file confined to `source_root` with no symlink/junction in its ancestry (168-179, 233-255).

| Option for "which byte count is closed" | Consequence |
|---|---|
| A. Month boundary — capture the whole `<YYYY-MM>.jsonl` after the month rolls over | Matches "closed monthly partitions" ([PKT]:30) and the collector's layout. One capture per interval per month; the "closed" claim is self-evident from the filename. Cost: up to a month of unbacked-up data. |
| B. High-water inside the live month — capture the prefix up to the last closed bar | Backs up sooner; needs a byte offset ending exactly on a record boundary or `_prefix_facts` refuses ("high-water prefix must end with newline", 182-183). Produces many stable-prefix directories and configs. |
| C. Both — periodic high-water captures plus a month-end capture | Best recovery-point objective, most receipts to manage. |

**Recommendation: A as the ratified default; B only after it has its own drill (§3, D-3b) and once the daily cadence in [PLAN]:581(b) is switched on.**

### C-6 · Heartbeat identity and state directory — LEAD DEFAULT

Verified constraints: the id must be a non-empty string ([WT] `p030_opsa_heartbeat_adapter.py`:65-67); it becomes `"<id>.hb.json"` inside a confined state dir (82; `heartbeat.py`:45); it must be discoverable by the watchdog's top-level `state_dir/*.hb.json` glob (`watchdog.py`:137-138); and it must survive `--expect`'s comma split (`watchdog.py`:276). The state dir must not be empty/whitespace and must not be the current working directory ([WT] `p030_opsa_heartbeat_adapter.py`:41-56).

**Recommendation (single choice):** id `p030_market_data_collector`; state dir `<RUNTIME_STATE_ROOT>/hb`, used for nothing else; one id per watched process. The P030 health sidecar lands beside it as `p030_market_data_collector.health.json` ([WT] `p030_opsa_heartbeat_adapter.py`:163) and is deliberately not part of the P026 payload. Consequence of ignoring the single-segment rule: an id containing `/` still writes — confinement permits nested relative paths — but becomes **invisible to the watchdog glob**, a silent monitoring hole. That is why this is a fixed default rather than a free-text field.

### C-7 · Heartbeat emission interval — LEAD DEFAULT (shipped value)

`heartbeat.py loop --interval` defaults to `60.0` seconds ([WT] `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py`:76). It is a shipped default rather than an owner-ratified contract, but unlike `--silence-seconds` it was never withdrawn.

**Recommendation: adopt 60 s.** One atomic write per minute (`heartbeat.py`:46-53), and it makes the silence bound in C-8 expressible as a whole number of missed beats. If the owner ratifies a different bound, keep `interval ≤ bound / 3` so a single missed beat cannot alert.

### C-8 · Watchdog silence bound (`--silence-seconds`) — **OWNER (ratification required)**

This is the one number the code refuses to default: "an unratified number must not be shipped as a contract. The bound is now a required explicit input" ([WT] `MTC_COMMAND_CENTER/tools/opsa/watchdog.py`:241-246). The README's `900` is an example only (`README.md`:68), and the plan withdrew the earlier `~15 minutes` figure as unratified ([PLAN]:580, 585).

Constraints any ratified value must satisfy (all verified):

1. `bound > emission interval`, or a healthy process alerts (`watchdog.py`:115-118 compares `age > silence_seconds`).
2. Future skew up to 60 s is tolerated separately and is not part of the bound (`watchdog.py`:63-64, 112-114).
3. The bound is a **detection** bound only. The end-to-end "failure detection to owner notification delivery" bound is `OPEN-N14` ([WT] `market_data_collector.py`:48) and stays `[OPEN]` until the real drill measures delivery ([PLAN]:585; [NOTIF]:41).
4. Real detection latency is `bound + time to the next scheduled check`: the checker is one-shot and installs no schedule ([WT] `watchdog.py`:1-6; `README.md`:104). A 300 s bound checked every 15 minutes detects in up to 20 minutes.

| Option | Consequence |
|---|---|
| A. Tight — e.g. 300 s ≈ five missed 60 s beats | Fast detection; sensitive to a stalled writer, a paused VM or a slow disk, and false alerts train the owner to ignore the channel. |
| B. Moderate — e.g. 900 s | The README's example value; survives a short stall; up to 15 minutes of silence looks healthy. |
| C. Defer the bound; run `local_log`-only meanwhile | No unratified number enters a scheduled invocation — and no phone coverage either. |

**Recommendation: put option A's concrete candidate — `--silence-seconds 300` with a 60 s emission interval and a 5-minute check cadence — to the owner for ratification (§5, O-3), and run option C until that ratification exists.** Rationale, offered as reasoning and not as a repository fact: five consecutive missed beats is the smallest count a single write stall cannot produce, and 300 s leaves headroom under any plausible N14 once delivery latency is measured. **The number has no repository basis; it is a proposal, and the code will keep refusing to assume it.**

### C-9 · Watchdog invocation shape — LEAD DEFAULT

**Recommendation (single choice) for the eventual scheduled call:**

```
python watchdog.py --state-dir <RUNTIME_STATE_ROOT>/hb \
                   --silence-seconds <OWNER_RATIFIED_BOUND> \
                   --expect p030_market_data_collector \
                   --notifier local_log \
                   --notifier-log <RUNTIME_STATE_ROOT>/hb/_watchdog_alerts.jsonl \
                   --state-file <RUNTIME_STATE_ROOT>/hb/_watchdog_seen.json
```

Grounding per flag: `--expect` turns a vanished heartbeat file into a `missing` **alert** rather than an empty directory (`watchdog.py`:144-146); without it an emptied state dir is only a check-failure (148-150). `--state-file` is what makes recovery events and re-alerting correct — the ledger records every observed state, and `silent → ok → silent` would otherwise suppress the second real incident (`watchdog.py`:200-235, 280-286). `--notifier local_log` is the only registered notifier today (`watchdog.py`:94). `--now` must **never** appear in a scheduled invocation; it is a test hook (`watchdog.py`:42, 255-256).

### C-10 · Alert delivery / notifier technology — **OWNER**

The registry is a one-entry dict and the extension point is explicit: implement `Notifier`, add a factory to `NOTIFIERS`, and `--notifier` picks it up ([WT] `watchdog.py`:70-94; `README.md`:95-99).

| Option | Consequence |
|---|---|
| A. Self-hosted ntfy on the owner PC (the Aug-25 primary, [NOTIF]:50-58) | No signup, no credential, no third party on the Android path; **on iOS instant push needs the upstream ntfy.sh APNS relay** ([NOTIF]:62-67), and away-from-home delivery needs the owner PC reachable ([NOTIF]:68-71). |
| B. Public ntfy.sh with a long random topic ([NOTIF]:76-79) | Zero infrastructure; third-party availability and metadata dependency; the topic name is a bearer capability ([NOTIF]:72-74). |
| C. Telegram bot ([NOTIF]:81-83) | Adds a real secret on the checker and a cloud with periodic regional blocking. |
| D. Defer | No phone coverage, and P026 acceptance stays closed by definition ([NOTIF]:94-96). |

**Recommendation: obtain the phone OS from the owner first, then adopt B for the first measured drill and A as the steady state.** The phone OS decides whether A's headline advantage survives ([NOTIF]:62-67) and is an owner fact no agent can look up. B is the cheapest way to obtain the *measurement* the acceptance gate demands ([PLAN]:585) without standing up a server; A then inherits a known-good latency baseline. All of it depends on re-verifying the Aug-25 external facts at adoption time ([NOTIF]:9-11). Any notifier implementation must be unit-tested against a local stub only ([NOTIF]:90-91) and is a separate scope request (§5, O-8).

### C-11 · Watchdog placement and scheduling — **OWNER + `G9`**

The package installs no schedule and says so twice ([WT] `watchdog.py`:1-6; `README.md`:104). The plan requires the checker to run **outside** the watched host ([PLAN]:580; [NOTIF]:19-21), which for a KVM2 collector means the checker runs on the owner PC and reads a heartbeat directory replicated from KVM2 — and that replication path is itself an unspecified host fact.

**Recommendation: record the placement requirement now and request nothing.** Watched process on the collector host; checker on the owner PC; the transport that makes `state_dir` visible to the checker is an open host-design question that must be answered **before** the drill, because a checker reading a directory that dies with the host reports `check_failed` ("state dir does not exist", `watchdog.py`:131-136) instead of the process-silence alert the gate is testing. This is a design gap, not a configuration value (§6, NV-4).

### C-12 · Restart-first-message policy beyond identical replay — **OWNER (ratification of implemented semantics)**

Decision 7 preserved WS-only restart continuity and explicitly "does not prove every restart-first-message case" ([GH]:16; [HO]:40). What the code does on a restart's first frame ([WT] `market_data_collector.py`:308-323, 361-436):

- same `observation_id` **and** same `producer_payload_hash` → `IDENTICAL_REPLAY_NOOP`; the cursor is seeded to `max(previous, bar_open_time)` and nothing is appended (311-313, 416-425);
- same `observation_id`, **different** payload bytes → `CollectionRefused("same observation_id has different producer bytes")` (312-314);
- same producer slot (`source_producer`, `symbol`, `interval`, `bar_open_time`), different bar → `CollectionRefused("differing same-producer bar requires an approved correction contract")` (315-322);
- on the first WS frame after restart the persisted WS_LIVE history is re-validated — identity match, integer and on-interval `bar_open_time`, UTC-renderable, and **no gap anywhere in the persisted sequence** — or the collector refuses (374-413).

| Option | Consequence |
|---|---|
| A. Ratify the implemented semantics: identical replay is a no-op; everything else refuses and waits for a `CORRECTION` observation under the frozen contract ([WT] `p030_market_data_contracts.py`:212-216, 262-312) | Fail-closed, no new code, no new numbers. Cost: a venue that legitimately restates a bar with different bytes halts ingestion until a human routes it through the correction path. |
| B. Auto-convert a differing same-slot bar into a `CORRECTION` observation | Removes the halt, but lets the collector mint corrections unattended — and the contract deliberately requires a predecessor id and forbids forks and cycles (293-311). Minting that chain automatically crosses the "no new semantics" line. |
| C. Widen the restart path to non-WS producers | Not needed: `CANDLE_SNAPSHOT` ingestion already flows through the same `classify_bar` (416, 461); Decision 7's WS-only wording is about *continuity*, not about which producers are validated. |

**Recommendation: A** (§5, O-7). It ratifies behaviour that already exists and has tests, keeps every refusal fail-closed, and converts "restart-first-message closure" from an open engineering question into a recorded owner policy without a line of new code. What A does **not** close: the persisted-history gap check (374-413) refuses a restart whenever the archive holds any WS_LIVE gap — including one created by a legitimate outage later backfilled by `CANDLE_SNAPSHOT`, because the check filters to `source_producer == "WS_LIVE"` before looking for gaps (378). That interaction needs a fixture drill before any real restart (§3, D-11).

### C-13 · Config-file location, redaction and confinement review — LEAD DEFAULT

The generated per-capture config (C-4) holds only paths, an id and a class; no secret is representable in the schema (`opsa_common.py`:227-245). Two confinement facts to preserve: `resolve_confined_path` rejects absolute, drive-prefixed, `..`-bearing and URL-escaped-`..` components and refuses a resolved path equal to the root (`opsa_common.py`:170-224); and the adapter re-reads and re-compares the config bytes before and after every P026 call, refusing if they changed mid-run ([WT] `p030_closed_partition_backup_adapter.py`:410-436, 439-466).

**Recommendation:** keep generated configs beside the backup root under `configs/<run label>.json`, never inside `<STABLE_PREFIX_ROOT>` (which must not pre-exist at capture time — C-4 constraint 4), and have the freeze step assert that no value resolves outside `<BACKUP_ROOT>` or `<STABLE_PREFIX_ROOT>`. This is the packet's step 2 ([PKT]:48) made concrete.

### Summary of section 2

| Ref | Configuration | Decider | Recommended choice |
|---|---|---|---|
| C-1 | Collector backend + permission protocol | OWNER | Keep the coded refusal; raise backend/permission as a separate scope (O-6) |
| C-2 | Operating policy (universe, cadence, gap-fill) | LEAD | Adopt the coded policy unchanged; leave `OPEN-N7` unset |
| C-3 | Archive root | OWNER | Parameterize now; owner supplies the volume with the `G9` step (O-1) |
| C-4 | Backup root / store id / path / class | OWNER (values), LEAD (shape) | One config **generated per capture**; fixed store id `p030_closed_partition`; class `protected`; shared `backup_root` (O-2) |
| C-5 | Stable-prefix capture parameters | LEAD | Month-boundary capture as the default; high-water capture only after its own drill |
| C-6 | Heartbeat id + state dir | LEAD | `p030_market_data_collector` in a dedicated `hb` directory |
| C-7 | Heartbeat emission interval | LEAD | 60 s (shipped default) |
| C-8 | Watchdog silence bound | **OWNER** | Propose `300` s for ratification; `local_log`-only until ratified (O-3) |
| C-9 | Watchdog invocation shape | LEAD | `--expect` + `--state-file` + `local_log`; never `--now` |
| C-10 | Notifier technology | **OWNER** | Phone OS first; ntfy.sh for the first measured drill, self-hosted ntfy as steady state (O-4, O-5) |
| C-11 | Checker placement + schedule | **OWNER + G9** | Record "checker outside the watched host"; resolve the state-dir transport before the drill |
| C-12 | Restart-first-message policy | **OWNER** | Ratify the implemented refuse-and-require-CORRECTION semantics (O-7) |
| C-13 | Config location / redaction | LEAD | Generated configs under `<BACKUP_ROOT>/configs/`; confinement asserted at freeze time |

---

## 3. Drill plan (paper only — nothing below was started)

Every drill here is described so that a later, separately authorized lane can execute it. **None was run in this lane**, no fixture was created, no tool was invoked. Authorization tiers used below:

- **T-A · offline fixture execution** — runs shipped code against fixtures inside a scratch directory; no host, no network, no credential, no live evidence store. Still requires an explicit execution scope, because this lane is read-only.
- **T-B · real-store execution** — same code against the real archive/backup roots once C-3/C-4 are ratified. If either root lives on KVM2 this becomes T-C.
- **T-C · `G9` host contact** — owner authorization per session ([PLAN]:584, 640), plus whatever the step itself needs (notifier choice, phone, credentials on the owner's side).

The drills the contracts already support, in dependency order.

### D-1 · Backup-config validation drill — T-A

**Steps (paper).** Call `load_runnable_config(config_path, stable_prefix=…, store_id="p030_closed_partition")` ([WT] `p030_closed_partition_backup_adapter.py`:370-375) against (a) the shipped null config, (b) a filled config whose store class is `bulk`, (c) a filled config whose store path differs from the stable prefix, (d) the intended config.
**Evidence.** Four recorded outcomes: (a) refuses — `require_non_empty_string_field` on `backup_root` (`opsa_common.py`:232); (b) refuses "P030 backup store class must be protected" (403); (c) refuses "P030 backup store path must equal the stable prefix" (404-407); (d) returns the parsed config.
**Does NOT prove.** That the paths exist, are writable, are on separate devices, or that the owner ratified them. Config validity is string/shape validity plus confinement, nothing more.
**Authorization.** T-A. This is the cheapest possible first drill and it is the one that converts C-4 from a proposal into a checked artefact.

### D-2 · Backup dry-run drill — T-A, then T-B

**Steps.** `python backup.py --config <config> --dry-run [--store p030_closed_partition]` ([WT] `MTC_COMMAND_CENTER/tools/opsa/backup.py`:207-215).
**Evidence.** A `PLAN` line per file with size and SHA-256 prefix (165), a JSON header and footer (101-103, 201-203), and — verifiable afterwards — **no** run directory and **no** manifest record, because every `append_jsonl` call is guarded by `if not dry_run` (104-109, 135-144, 184-189, 196-200).
**Does NOT prove.** That a real copy would succeed (no write is attempted), that the destination has space, or that read-back would match.
**Authorization.** T-A on fixtures; T-B once real roots exist.

### D-3 · Stable-prefix capture drill (month boundary) — T-A

**Steps.** Build a fixture partition of canonical sorted-key JSONL rows carrying `p030obs-v1:`-prefixed `observation_id`s; compute its `dataset_content_hash` via `p030_market_data_contracts.dataset_content_hash()`; call `capture_stable_prefix(source_jsonl, stable_prefix, source_root=…, high_water_bytes=<file size>, captured_at_utc=<…Z>, dataset_content_hash=<p030ds-v1:…>)`.
**Evidence.** A new stable-prefix directory containing the byte-identical snapshot and `_P030_STABLE_PREFIX.json` carrying `high_water_bytes`, `record_count`, `last_observation_id`, `prefix_sha256`, `captured_at_utc` and `dataset_content_hash` ([WT] `p030_closed_partition_backup_adapter.py`:276-290). The capture re-reads the source after writing and refuses if it changed mid-capture (270-273), and re-reads the snapshot and refuses if it does not match (274-275).
**Does NOT prove.** That the partition was genuinely closed — the adapter refuses to infer closure (229) and trusts the caller's `high_water_bytes`. It also does not prove the rows are the collector's rows (see D-13).
**Authorization.** T-A.

### D-3b · High-water capture variant — T-A

**Steps.** As D-3, but with `high_water_bytes` set to a byte offset inside the file: one run ending exactly on a record boundary, one ending mid-record.
**Evidence.** GREEN for the boundary-aligned offset; RED "high-water prefix must end with newline" for the mid-record offset ([WT] `p030_closed_partition_backup_adapter.py`:182-183); and a short read refused with "source prefix is truncated below high water" (262-263).
**Does NOT prove.** That any particular production offset is the right one — that arithmetic belongs to the caller, which is exactly why C-5 recommends month boundaries as the default.
**Authorization.** T-A. This drill is C-5 option B's precondition.

### D-4 · Backup of a stable prefix — T-A, then T-B

**Steps.** `backup_stable_prefix(config_path, stable_receipt=<…/_P030_STABLE_PREFIX.json>, store_id="p030_closed_partition", source_root=<ARCHIVE_ROOT>)` ([WT] `p030_closed_partition_backup_adapter.py`:625-679).
**Evidence.** The returned `run_id`; new `manifest.jsonl` records (`run_start`, two `file` records, `run_end` with `status: ok`, `errors: []`); `readback=match` on both files (`backup.py`:178-192); and three independent byte comparisons inside the adapter — the receipt/snapshot before the P026 call, after it (651-661), and as archived (672-678). `_complete_p026_run` additionally refuses unless the run contains exactly the two expected members `{_P030_STABLE_PREFIX.json, <snapshot>}` (518-525), all with `readback == "match"` and matching declared file/byte counts (496-509).
**Does NOT prove.** Restorability (that is D-5), second-device placement (a config could point both roots at one disk — a human check), or that the backed-up partition is complete with respect to the venue.
**Authorization.** T-A on fixtures; T-B on the real roots.

### D-5 · Verified restore drill — T-A, then T-B

**Steps.** Create an **empty** target directory, then `restore_verified_prefix(config_path, run_id=<from D-4>, store_id="p030_closed_partition", target=<empty dir>)` ([WT] `p030_closed_partition_backup_adapter.py`:682-816).
**Evidence.** `_P030_VERIFIED_RESTORE.json` at the target root carrying `run_id`, `store_id`, `restored_prefix` and the six identity fields copied from the stable receipt (796-816); the restored tree contains **exactly** the expected members, with symlink/junction/type checks on each (766-790); and the restored bytes equal the archived bytes (791-795). Note the drill exercises `--check-only` and the write path in one call: the adapter runs `restore.run_restore(..., check_only=True)` first and only then the real restore (706-742), both against an **isolated temporary copy** of the backup root (560-622), so the real backup root is never a restore target.
**Does NOT prove.** Reconciliation in the [PLAN]:581(c) sense ("integrity, readability **and reconciliation**") — the adapter proves integrity and readability of one partition; reconciling restored evidence against the ledgers is a separate, unbuilt step. It also does not prove a production recovery procedure ([HO]:40).
**Authorization.** T-A, then T-B. The target must be empty — the adapter refuses otherwise (687-688) and re-checks twice more before writing (729-735).

### D-6 · Tampered-archive falsification (RED) — T-A

**Steps.** After D-4, flip one byte in the archived snapshot under `runs/<run_id>/<store_id>/`, then run D-5.
**Evidence.** Refusal at the manifest hash check — `verify_backup_file` reports `sha256 mismatch` and `run_restore` returns non-zero (`restore.py`:60-70, 169-174, 204-213), so the adapter raises "P026 check-only failed; restore withheld" ([WT] `p030_closed_partition_backup_adapter.py`:727-728) **before** anything is written to the target. A second variant — tamper the `_P030_STABLE_PREFIX.json` instead — fails earlier, at `_verify_stable_receipt`'s field/hash checks (310-349).
**Does NOT prove.** Detection of a coordinated tamper that rewrites the manifest *and* the archived bytes together; the manifest is append-only by discipline (`opsa_common.py`:130-143) but is not itself signed or externally anchored. Worth recording as a residual risk rather than papering over.
**Authorization.** T-A only. Never tamper with a real archive.

### D-7 · Incomplete-run falsification (RED) — T-A

**Steps.** Hand-build manifests that are individually defective: `run_end.status != "ok"`; `errors` non-empty; `files` count disagreeing with the number of `file` records; a `skipped` or `dir` record inside the run; a `file` record for a third member.
**Evidence.** Each refuses with "restore requires one complete successful P026 run" ([WT] `p030_closed_partition_backup_adapter.py`:482-509) or the member-set check (518-525). A malformed JSONL line refuses earlier at `_decode_strict_jsonl` (99-120) — note this is **stricter** than P026's own `read_jsonl`, which returns `{"record": "_malformed"}` and lets the caller report it (`opsa_common.py`:146-162).
**Does NOT prove.** That a real interrupted backup produces exactly these manifests; it proves the acceptance predicate, not the failure population.
**Authorization.** T-A.

### D-8 · Heartbeat emit / verify / health-sidecar drill — T-A

**Steps.** `emit_process_heartbeat(state_dir, "p030_market_data_collector", seq=1)`, then `verify_process_heartbeat(...)`, then `write_health_sidecar(..., observed_at_utc=…, last_accepted_timestamp_utc=…, reconciliation_progress=None)` ([WT] `p030_opsa_heartbeat_adapter.py`:59-72, 75-115, 130-174). Falsifications: an extra field in the payload; a fractional-second `emitted_at`; `reconciliation_progress` non-null; `last_accepted_timestamp_utc` later than `observed_at_utc`.
**Evidence.** A P026-shaped `<id>.hb.json` (`heartbeat.py`:46-53); a verifier that accepts exactly `{schema,id,seq,emitted_at,pid}` plus optional non-empty `note` and rejects anything else (91-107); the emitter's exact UTC-Z grammar enforced by regex (25, 108-110); a `p030.health_sidecar/v1` file with `market_freshness.availability` = `available`/`unavailable` and a non-negative `age_seconds` (146-162); and refusals for each falsification (143-144, 156-157).
**Does NOT prove.** That anything watches the heartbeat, that the beat reaches a checker on another machine, or that a dead process's silence is noticed — that is D-9 and D-17.
**Authorization.** T-A.

### D-9 · Watchdog state-matrix drill (deterministic) — T-A

**Steps.** With `--now` fixed, drive all six states: fresh beat (`ok`), aged beat (`silent`), `--expect` id with no file (`missing`), unparseable file (`unreadable`), missing `emitted_at` (`bad_timestamp`), far-future stamp (`clock_skew`), plus the three directory-level failures: absent state dir, empty state dir with no `--expect`, and an invalid `--now` value.
**Evidence.** Per-id JSON on stdout and process rc: `0` all ok, `2` any alert, `3` any check-failure with no alert ([WT] `watchdog.py`:288-292; `README.md`:71-86); at least one notifier event for every alert/check-failed outcome, including the synthetic `_watchdog_check` event for the directory-level cases (`watchdog.py`:162-163, 193-196); and an invalid `--now` producing a check-failed record rather than a traceback (264-274).
**Does NOT prove.** Any real-world timing. `--now` is a test hook and must never be used in a scheduled invocation (42, 255-256). It also proves nothing about delivery — `local_log` writes a file, it does not reach a phone.
**Authorization.** T-A.

### D-10 · Recovery-transition ledger drill — T-A

**Steps.** With `--state-file` set, run the sequence `silent → ok → silent` over three checks (using `--now` to control age).
**Evidence.** One `silent` event, then exactly one `recovered` event carrying `recovered_from: "silent"`, then a **second** `silent` event ([WT] `watchdog.py`:200-233). This is the regression the code comments call out as a previously-fixed defect (201-205, 280-282); a drill that does not exercise it cannot claim the fix holds.
**Does NOT prove.** Behaviour when the ledger file itself is unreadable — worth adding as a variant, since the code deliberately treats an unreadable ledger as "first sighting" and re-alerts (186-192).
**Authorization.** T-A.

### D-11 · Collector restart drill (identical replay + persisted-gap interaction) — T-A

**Steps.** Against a fixture `MonthlyArchive`: (i) ingest a WS_LIVE bar, construct a fresh `MarketDataCollector` over the same archive, ingest the identical raw frame again; (ii) repeat with one payload field changed; (iii) repeat with a persisted WS_LIVE history that contains a gap later filled by `CANDLE_SNAPSHOT` rows.
**Evidence.** (i) `IDENTICAL_REPLAY_NOOP`, nothing appended, cursor seeded to the replayed bar ([WT] `market_data_collector.py`:311-313, 416-425); (ii) `CollectionRefused("same observation_id has different producer bytes")` or the same-slot correction refusal (312-322); (iii) the outcome of the WS_LIVE-only gap scan (374-413) — this is the case C-12 flags and the reason the drill exists: the scan filters to `source_producer == "WS_LIVE"` (378) before calling `detect_gap`, so snapshot-backfilled bars do not close a WS_LIVE gap and the restart refuses.
**Does NOT prove.** Anything about a real venue's restart behaviour, real reconnect timing, or the missed-decision policy in [PLAN]:377. It is a fixture-level proof of the coded semantics only.
**Authorization.** T-A. This is the drill that makes C-12/O-7 a ratification of *observed* behaviour rather than of a code reading.

### D-12 · Offline gap-report drill — T-A

**Steps.** `python market_data_collector.py gap-report --archive <fixture root> --symbol BTC --interval 1h` ([WT] `market_data_collector.py`:496-533).
**Evidence.** One `GAP …` line per detected hole with first/last missing bar in UTC, and a `GAPS: <n>` total.
**Does NOT prove.** That the archive is complete with respect to the venue — it only compares stored bars against the interval grid, so a uniformly truncated archive reports zero gaps.
**Authorization.** T-A. This is the only collector subcommand that is executable today (C-1).

### D-13 · Producer-to-contract identity bridge drill — T-A · **prerequisite for D-3…D-7 on real data**

**Why it exists.** §4.1 records a verified byte-level incompatibility: collector-written archive lines are not acceptable input to `capture_stable_prefix`.
**Steps.** Take a collector-written fixture partition and attempt D-3 against it unchanged; then attempt it again after a transform step that (a) recomputes each row's identities through `p030_market_data_contracts.producer_payload_hash()` / `observation_id()` and (b) re-serializes each line with `sort_keys=True`.
**Evidence.** RED on the raw partition — either "observation_id must match p030obs-v1 identity" ([WT] `p030_closed_partition_backup_adapter.py`:212-213) or "prefix record is not canonical JSONL" (207-208), depending on which check the first row trips; GREEN after the transform. The GREEN half also yields the `dataset_content_hash` that D-3 requires.
**Does NOT prove.** That the transform is the right design. Whether the collector should write contract-shaped rows directly, or a separate exporter should produce the backup-facing partition, is an engineering decision that needs its own scope and review (§5, O-9).
**Authorization.** T-A for the drill; the transform itself is new code and needs an implementation scope.

### D-14 · Forced-disconnect gap-backfill drill — T-A (fixture) / **T-C for the acceptance gate**

**Steps (fixture).** Implement a stub `PublicMarketSource` ([WT] `market_data_collector.py`:139-155), deliver WS frames with a deliberately dropped window, and let `_fill_gap` page the stub's `candles_snapshot` (438-479).
**Evidence.** The gap is detected (252-261), backfilled through `CANDLE_SNAPSHOT` ingestion (460-461), and the post-fill completeness check passes; the RED variants — a page returning nothing, a non-advancing cursor, a residual missing bar — each refuse (462-479).
**Does NOT prove.** The P030 acceptance gate. That gate reads "the collector **survives a forced disconnect with a proven gap-backfill** (D026 RED/GREEN on a deliberately dropped window)" ([PLAN]:641) against the real feed; a stub proves the algorithm, not the venue interaction, and the real version needs C-1 plus `G9`.
**Authorization.** T-A for the fixture; T-C plus a ratified backend for the gate itself.

### D-15 · RED/GREEN restore drill on real evidence stores — T-B or T-C

**Steps.** The [PLAN]:585 shape: show an un-backed-up loss unrecoverable, then restore the backed-up copy byte-identically. The 2026-08-25 lane already performed this **on fixtures** ([DRILL]:20-170: dry-run writes nothing; backup + read-back; RED 0/3 baseline hashes remain in the damaged tree; GREEN 3/3 byte-identical; tampered backup refused).
**Evidence a real run would add.** The same verdicts against the actual evidence stores and roots, with the manifest, per-file hashes and the verified-restore receipt as artefacts.
**Does NOT prove.** Acceptance on its own — [PLAN]:585 pairs the restore drill with the phone-push proof, and [PLAN]:581(c) additionally requires **reconciliation**, which no shipped tool performs.
**Authorization.** T-B if both roots are local; **T-C** if either touches KVM2. Restore drills must run on copies, never on the live store ([PLAN]:583).

### D-16 · Kill-heartbeat-to-phone drill — **T-C, not startable here**

**Steps.** Owner picks the notifier (C-10); a `NtfyNotifier`-shaped class is added to `NOTIFIERS` and unit-tested against a **local stub only** ([NOTIF]:90-91); `G9` authorizes the host step that installs the server (if self-hosted) and schedules the checker; then a watched heartbeat is killed and the detect and delivery timestamps are recorded ([NOTIF]:92-96).
**Evidence.** The push received on the owner's phone — the binding functional requirement ([PLAN]:580, 585) — plus the measured detect→delivery elapsed time, which is *put to the owner* for ratification; only after that ratification does any time bound become enforceable ([PLAN]:585).
**Does NOT prove.** `OPEN-N14` by itself: one measurement is an observation, not a ratified bound ([WT] `market_data_collector.py`:48). It also proves nothing about the collector-failure→detection half unless the killed heartbeat is the collector's own.
**Authorization.** Owner decision on the notifier + `G9` + owner's phone. **This lane requests none of it and started none of it.**

### D-17 · Checker-external-to-watched-host drill — **T-C**

**Steps.** With the checker on the owner PC and the heartbeat directory sourced from the collector host, stop the *host* (not just the process) and observe.
**Evidence.** Distinguishes the two outcomes the design cares about: a genuine `silent`/`missing` **alert** versus a `check_failed` "state dir does not exist" ([WT] `watchdog.py`:131-136) caused by losing sight of the directory. [PKT]:51's stop condition ("stop if the checker is not external to the watched host") is exactly this.
**Does NOT prove.** Anything until C-11's state-dir transport question is answered; without that answer the drill's most likely outcome is the uninformative check-failure.
**Authorization.** T-C.

### Drill dependency order

```
D-1 config validation
  └─ D-2 dry-run
       └─ D-13 identity bridge  ── prerequisite for real-data captures
            └─ D-3 capture ─ D-3b high-water variant
                 └─ D-4 backup ── D-6 tamper RED ── D-7 incomplete-run RED
                      └─ D-5 verified restore
                           └─ D-15 real-store RED/GREEN            [T-B/T-C]
D-8 heartbeat ── D-9 watchdog matrix ── D-10 recovery ledger
                      └─ D-16 phone drill                          [T-C, owner + G9]
                           └─ D-17 host-loss discrimination        [T-C]
D-11 restart semantics ── D-12 gap report ── D-14 gap-backfill (stub → real) [T-C for the gate]
```

**Status of every drill above: NOT STARTED.** No fixture exists, no command was run, nothing was scheduled.

---

## 4. Prerequisite ordering

### 4.1 A verified gap between the collector's output and the backup adapter's input

This is the single most consequential finding of this lane, and it changes the packet's "minimal next sequence" step 3 ([PKT]:49). It is a **code-reading** conclusion — nothing was executed — but it rests on four exact, quotable facts.

1. **The collector writes archive lines in dataclass declaration order.** `MonthlyArchive._append` serializes with `json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(",", ":"))` — **no `sort_keys`** ([WT] `market_data_collector.py`:294-300) — over `asdict(bar)` (330), where `MarketBar`'s field order is `observation_id, producer_payload_hash, symbol, interval, bar_open_time, …` (90-111), which is not alphabetical.
2. **The adapter requires sorted-key canonical JSONL.** `_prefix_facts` re-serializes each line as `json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",",":")) + b"\n"` and refuses with "prefix record is not canonical JSONL" if the re-serialization does not equal the original bytes ([WT] `p030_closed_partition_backup_adapter.py`:197-208).
3. **The collector's identities carry no contract prefix.** `HashContract.digest` returns a bare `hashlib` hexdigest ([WT] `market_data_collector.py`:66-80); the check suite constructs it as `HashContract(tuple(fields), "sha256", "utf-8", "json-array-compact")` (`check_market_data_collector.py`:69-71). There is no code path by which it can emit a prefix.
4. **The adapter requires the frozen prefixes.** Every prefix record must have an `observation_id` matching `^p030obs-v1:[0-9a-f]{64}$` ([WT] `p030_closed_partition_backup_adapter.py`:47-48, 209-213), and the dataset contract likewise requires `p030obs-v1`/`p030payload-v1` prefixes ([WT] `p030_market_data_contracts.py`:207-208, 316, 325-329).

**Consequence.** A collector-written monthly partition cannot be captured by `capture_stable_prefix` today: it trips (3)/(4) on the first row, and (1)/(2) independently. Both suites pass because each is exercised against its own fixtures — and the module graph confirms the two halves are never wired together: the only importer of `p030_market_data_contracts` is `check_p030_market_data_contracts.py`, the only importer of `p030_closed_partition_backup_adapter` is its own check suite, and `market_data_collector.py` imports neither (verified by `grep -rln` over `*.py` in the merged worktree).

**Not a defect claim against the merged slices.** Each module does exactly what its own contract says, and [HO]:37 already frames the merges as implementation milestones. What is missing is the **producer/exporter step between them**, and no handoff line claims that step exists. It is an unstated prerequisite, and it belongs in the ordering below rather than being discovered mid-drill.

**One encouraging detail.** The row *shape* already matches: `MarketBar`'s 21 fields are exactly `DATASET_ROW_FIELDS` in exactly that order ([WT] `market_data_collector.py`:90-111 against `p030_market_data_contracts.py`:53-58). So the bridge is a re-identification and re-serialization step, not a schema redesign.

### 4.2 What must precede the forward-observation-clock admission

The START_HERE P0-26 row says only "preserve prerequisite before forward-observation clock admission" ([SH]:51). The prerequisites it points at are locatable and explicit, contrary to the packet's "not located" reading ([PKT]:21, table row 18):

| # | Requirement | Source | Status |
|---|---|---|---|
| P-1 | **WP-P0-26 must be accepted** before any forward clock starts: "no forward clock (WP-V2A-08 shadow window or WP-V2B-07 lane) may start before this package is accepted — that clock-gating edge is part of this gate, not advice" | [PLAN]:585 | OPEN |
| P-2 | P026 acceptance itself needs: the D026 RED/GREEN restore drill; **the phone push actually received**; the detect→delivery time **measured, recorded and put to the owner**; and the owner's **ratification** of an exact bound before any bound is enforceable | [PLAN]:585; [NOTIF]:94-96 | OPEN — D-15, D-16 |
| P-3 | "A backup counts only after an isolated restore proves integrity, readability **and reconciliation**"; that proof is required **before any forward clock**, after any backup or schema change, after any failed recovery, and on a recurring interval that is `[OPEN]` | [PLAN]:581(c) | OPEN — D-5 covers integrity/readability; **reconciliation has no shipped implementation** |
| P-4 | WP-P0-30 acceptance: forced-disconnect gap-backfill proven RED/GREEN, archive rows carry venue provenance, bar-close semantics match the #45 rows — and P030 is "**accepted before WP-V2A-08 starts** (hard edge)" | [PLAN]:641 | OPEN — D-14 |
| P-5 | WP-P0-30 depends on WP-P0-26 (watchdog + backup for the archive) **and** WP-P0-21 (its quality gates reuse P021 checks) | [PLAN]:638 | OPEN |
| P-6 | WP-V2A-08 itself depends on WP-V2A-07, WP-V2A-10, WP-P0-30 and WP-P0-26 | [PLAN]:750 | OPEN |
| P-7 | The **local** prerequisite this lane adds: the producer/exporter bridge of §4.1, without which P-3's restore proof cannot be run over real collector output at all | §4.1 | OPEN — D-13 |

**What is genuinely still unlocated** — and what the packet was right to refuse to invent — is the rule that names the **clock-start event**: which admitted observation timestamp begins a countable forward window. `day_forward_period = 21` days is a *profile length*, not a start rule, and its own source note records that the owner-facing summary table says four weeks instead ([RR]:102-111). Until a start rule is located or ratified, no agent should convert an archive's first bar into "day 1".

### 4.3 What stays blocked on P012 / P020 / P021 acceptance

| Blocked item | Blocking dependency | Evidence |
|---|---|---|
| P021 eligibility verdicts of any kind | P012 **accepted corrected-engine evidence** and P020 **accepted evidence** | [HO]:39 |
| Four P021 limits | `gap_ratio_max`, `divergence_tolerance`, `divergence_window_length`, `divergence_min_paired_observations` remain unset and fail-closed under Decision 6 | [HO]:39; [GH]:16; [RR]:166, 202, 232 |
| P021 lookahead admission | `LOOKAHEAD_DECISION_DOMAIN` B-12 open | [HO]:39 |
| P021 forward evidence | "qualifying forward evidence remain open … No real bundle or readiness PASS occurred" | [HO]:39 |
| P020 as a consumable input | P020 `6f7f495a…` "remains NONACCEPTED and cannot be consumed as accepted evidence"; the acceptance reporter stands at 8/16 MET / NOT ACCEPTABLE | [GH]:16; [SH]:34 |
| P012 | Narrowed to a research/engineering scope only: "P0-12 research/engineering scope complete; production admission pending", with the formal Section-16 review and seal ratifications OPEN | [DEC] `OD-20260913-P012-SCOPE-1` |
| P030 quality gates that reuse P021 checks | P030 depends on P021 | [PLAN]:638 |

Note the direction of these edges: **P030/P026 operational work is not blocked by P012/P020/P021.** Configuration, drills D-1…D-15 and the notifier work can all proceed under their own authorizations while the upstream packages remain unaccepted. What is blocked is the **forward clock** and every readiness/eligibility claim downstream of it. Confusing the two would either stall ready work or manufacture a readiness claim; both are failure modes this ordering is meant to prevent.

### 4.4 Ordering, end to end

```
now ─┬─ C-1…C-13 configuration choices (this document)
     │
     ├─ owner decisions O-1…O-8 (§5)
     │
     ├─ [T-A execution scope] D-1 config validation → D-2 dry-run
     │        → D-13 identity bridge  ← §4.1 prerequisite, needs an implementation scope (O-9)
     │        → D-3/D-3b capture → D-4 backup → D-6/D-7 falsifications → D-5 verified restore
     │        → D-8 heartbeat → D-9 watchdog matrix → D-10 recovery ledger
     │        → D-11 restart semantics → D-12 gap report → D-14 gap-backfill (stub)
     │
     ├─ [notifier scope, local stub only] NtfyNotifier-shaped class + unit tests   (O-8)
     │
     ├─ [G9 + owner] host install/schedule → D-16 phone drill → measured latency
     │        → owner ratifies the detect→delivery bound              (P-2)
     │        → D-17 host-loss discrimination                          (C-11)
     │        → D-15 real-store RED/GREEN + reconciliation step        (P-3)
     │
     ├─ WP-P0-26 ACCEPTED                                              (P-1, P-2, P-3)
     ├─ [C-1 backend + permission protocol ratified] collector runtime → real D-14
     ├─ WP-P0-30 ACCEPTED                                              (P-4, P-5)
     └─ only then: forward-observation clock admission                 (P-1, P-6)
                   — and only with a located or ratified clock-start rule
```

Two edges in that chain have no owner in any current handoff and should be assigned explicitly: **the reconciliation half of P-3**, and **the state-dir transport of C-11**.

---

## 5. Consolidated owner approval request

Only decisions that genuinely cannot be made by an agent are listed. Each carries a recommended answer, so the owner can reply with a short line per item. **Nothing here has been acted on.**

| Ref | Decision needed | Why an agent cannot decide it | Recommended answer |
|---|---|---|---|
| **O-1** | `<ARCHIVE_ROOT>` — the volume and path for the market-data archive, plus a free-space budget | It is a host/infrastructure fact; no repository value exists and the config field is `null` ([WT] `p030_opsa_backup_config.json`:3) | Name the target volume now as a placeholder and bind the concrete path at the same moment the `G9` host step is authorized (C-3). Layout is fixed: `<ARCHIVE_ROOT>/bars/HYPERLIQUID/BTC/<interval>/<YYYY-MM>.jsonl` |
| **O-2** | `<BACKUP_ROOT>` — the second location, on a **different device or host** from O-1; plus confirmation of the store shape | Same: a host fact. The "second location" duty is the plan's, the value is the owner's ([PLAN]:580) | Approve the C-4 shape: one config **generated per capture**, fixed store id `p030_closed_partition`, class `protected`, shared `backup_root`, configs under `<BACKUP_ROOT>/configs/` |
| **O-3** | The watchdog silence bound `--silence-seconds`, and the check cadence | The code refuses to ship a default because no such value is ratified ([WT] `watchdog.py`:241-246); the plan withdrew the old `~15 minutes` figure ([PLAN]:580) | **Ratify `300` seconds** with a 60 s heartbeat interval and a 5-minute check cadence (C-7, C-8). This is a proposal with no repository basis; if the owner prefers to wait for measured delivery latency, answer "defer" and the checker runs `local_log`-only |
| **O-4** | Is the owner's phone **Android or iOS**? | A fact about the owner's device; it decides whether self-hosted ntfy delivers instantly or needs the upstream APNS relay ([NOTIF]:62-67) | Answer the OS; no other action follows from this item alone |
| **O-5** | Notifier technology | The plan explicitly leaves the technology to an owner choice ([PLAN]:580; [NOTIF]:89) | **Public ntfy.sh with a long random topic for the first measured drill, self-hosted ntfy on the owner PC as the steady state** (C-10). Revisit if O-4 says iOS. All Aug-25 external facts to be re-verified at adoption ([NOTIF]:9-11) |
| **O-6** | Collector backend + permission protocol: lift the coded runtime refusal, or keep waiting? | Lifting it needs a ratified permission protocol and a backend; the code refuses unconditionally today ([WT] `market_data_collector.py`:534-538) | **Keep the refusal for now**, and note the cost explicitly: every day of delay permanently loses venue candles against the retention window ([PLAN]:632-633). Revisit immediately after O-5/O-8 rather than after full P026 acceptance |
| **O-7** | Restart-first-message policy beyond identical replay | Decision 7 deliberately did not close it ([GH]:16) | **Ratify the implemented semantics** (C-12 option A): identical replay is a no-op; a differing same-slot bar refuses and waits for a `CORRECTION` observation under the frozen contract. No new code, no new numbers |
| **O-8** | A bounded **offline execution scope** (T-A) to run drills D-1…D-14 on fixtures, plus a notifier class unit-tested against a **local stub only** | This lane is read-only; running any code needs its own scope. It is also the packet's own step 3-5 ordering ([PKT]:49-51) | **Approve**, with the explicit fence: scratch fixtures only, no host, no network, no credential, no schedule, no real evidence store, no send |
| **O-9** | An **implementation scope** for the producer/exporter bridge of §4.1 (contract-shaped identities + sorted-key serialization between the collector archive and the backup adapter) | It is new code with a design choice (collector writes contract rows directly vs. a separate exporter) and needs its own review tier | **Approve the design step first** (a one-page choice between the two shapes), then implement under the normal review path. Without it, no real-data backup drill can run |
| **O-10** | Records hygiene: should the P021/P030 owner answers `1 YES, 2 YES, 3 A, 4 YES, 5 YES, 6 A, 7 A` and the substance of decisions 6 and 7 be added to `DECISIONS.md`? | Only the owner can authorize a decision-index row | **Yes** — they exist today only in handoff prose ([HO]:16; [GH]:5, 16) and are absent from `DECISIONS.md` (table row 35). One row, no semantic change |

**Not requested now, and deliberately so:** `G9` host contact, KVM2 installation, any schedule installation, any credential, any real send, any venue contact, any deployment, any acceptance decision. Those follow O-5/O-8/O-9 in the §4.4 order and each needs its own owner authorization at the time it happens ([PLAN]:584, 640).

---

## 6. NOT VERIFIED

Everything in this list is something a next agent must **not** treat as established by this document.

| Ref | Not verified | Why |
|---|---|---|
| NV-1 | The PASS results behind `collector PASS, contracts PASS, backup 44/44, heartbeat 10/10, P026 33/33` ([HO]:32) and P021's `103/103` ([HO]:30) | No execution is authorized in this lane. Only the **test-method counts** (44, 10, 33) were verified by reading the suites |
| NV-2 | The packet's conduct claims — that its preparation performed no host, network, provider, deployment, test, Git or memory action ([PKT]:3) | Not checkable from the artefacts |
| NV-3 | Every host fact: that KVM2 exists in the assumed shape, its disks, paths, schedules, and the deployed backup/monitoring/restart/rollback state | [PLAN]:581 states this is `UNVERIFIED` pending `G9` and that "nothing here authorizes contacting the host to find out". This lane contacted nothing |
| NV-4 | How a checker on the owner PC would see the collector host's heartbeat directory (C-11) | No design exists in the inspected sources; the plan states the requirement ([PLAN]:580) but not the mechanism |
| NV-5 | Whether any **reconciliation** implementation exists for [PLAN]:581(c) ("integrity, readability and reconciliation") | None was found in the inspected scope (`tools/opsa/`, the three P030 modules and their check suites). This is "not located", not "proven absent" — the search was bounded |
| NV-6 | Every external fact in [NOTIF] — ntfy/ntfy.sh/Telegram/Pushover behaviour, pricing, limits, the iOS APNS-relay constraint, regional blocking | The document itself dates them to 2026-08-25 and requires re-verification at adoption ([NOTIF]:9-11). No network access here |
| NV-7 | Detect→delivery latency, and therefore `OPEN-N14` | Unmeasured by definition until D-16 runs ([PLAN]:585; [WT] `market_data_collector.py`:48) |
| NV-8 | That the §4.1 conclusion holds against every fixture in the check suites | §4.1 is derived from the **production** modules (`market_data_collector.py`, `p030_closed_partition_backup_adapter.py`, `p030_market_data_contracts.py`) and the import graph. The 1791-line and 1600-line check suites were inspected structurally (class/test counts, entry points), not read line by line. D-13 is what would settle it empirically |
| NV-9 | The rule that starts a countable forward-observation clock | Gating requirements are located (§4.2 P-1…P-6); the **start event** is not. `day_forward_period = 21` is a derived profile length, not a start rule ([RR]:102-111) |
| NV-10 | That `origin/master` is still `fcac0ac67cf2682693ad28138b1a56e15a0846f2` | No remote refresh was performed (no network). [HO]:7 already warns: "do not assume that ref remains current without a permitted refresh" |
| NV-11 | Anything in the P021 worktree beyond `p021_readiness_rules.py`, and anything in the closeout worktree | Out of this lane's inspection scope |
| NV-12 | The detailed command outputs in [DRILL] | Read as an outline (section headings plus the first 30 lines). The fixture-drill *claims* summarized in table row 12 come from [LANE], not from re-checking [DRILL]'s transcripts |
| NV-13 | That the recommended values in §2 are correct for the real deployment | They are drafting proposals. Every one of them is either a shipped default (C-7), a coded constraint (C-4, C-6, C-9), or an explicit owner request (C-3, C-8, C-10) |

---

## 7. Citation index

Source keys used throughout. All paths are absolute; line numbers refer to these exact files as read on 2026-09-13.

| Key | Path | What was read |
|---|---|---|
| [PKT] | `C:/tmp/P030_P026_LUNA_PREP_20260913/DECISION_PACKET.md` | whole file (1-57) |
| [HO] | `C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md` (byte-identical to `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md`, SHA-256 `fec60cc9…`) | whole file (1-57) |
| [SH] | `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md` (byte-identical to the CT13 mirror, SHA-256 `b890d7fc…`) | whole file (1-78); P0-26 row at 51, P0-21/P0-30 row at 48 |
| [GH] | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md` | whole file (1-23) |
| [PLAN] | `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` | `### WP-P0-26` (577-589), `### WP-P0-30` (630-646), plus 377, 746-750, 905-911 by targeted search |
| [LANE] | `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md` | 1-125 |
| [NOTIF] | `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/NOTIFIER_PROPOSAL.md` | whole file (1-97) |
| [DRILL] | `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md` | headings outline + 1-30 only (see NV-12) |
| [DEC] | `C:/CT13/DECISIONS.md` | header 1-40, tail 25 lines, and full-file grep for P030/P026/OPS-A/VEN-E/watchdog/heartbeat/"decision 6"/"decision 7"/"1 YES, 2 YES" |
| [RR] | `C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` | 88-147, 166, 172-235, 230-305 |
| [WT] | `C:/tmp/P030_INTEGRATION_20260913/` at HEAD `f42fd5400b2c2ecb805644d406999cb55c8178c8`, branch `feature/p030-integrated-20260913` | files below |

Files read inside [WT] (each byte-identical to its `C:/CT13/` copy — SHA-256 table at the top of this document):

| File | Lines read |
|---|---|
| `market_data_collector.py` | whole file (1-543) |
| `p030_market_data_contracts.py` | whole file (1-471) |
| `p030_closed_partition_backup_adapter.py` | 1-340, 340-639, 639-817 (whole file, 816 lines) |
| `p030_opsa_heartbeat_adapter.py` | whole file (1-175) |
| `p030_opsa_backup_config.json` | whole file (1-11) |
| `MTC_COMMAND_CENTER/tools/opsa/watchdog.py` | whole file (1-297) |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | whole file (1-239) |
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | whole file (1-220) |
| `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py` | whole file (1-113) |
| `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` | whole file (1-246) |
| `MTC_COMMAND_CENTER/tools/opsa/README.md` | whole file (1-111) |
| `MTC_COMMAND_CENTER/tools/opsa/config.example.json` | whole file (1-17) |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | structure only: class list and 33 `def test_…` methods |
| `check_p030_closed_partition_backup_adapter.py` | structure only: single `unittest` class, 44 `def test_…` methods |
| `check_p030_opsa_heartbeat_adapter.py` | structure only: single `unittest` class, 10 `def test_…` methods |
| `check_p030_market_data_contracts.py` | structure only: entry points and `EVENT_FAMILIES` assertion at 922 |
| `check_market_data_collector.py` (read in `C:/CT13/`) | 69-71, 87-92, 921-928 by targeted search |

Read-only Git commands used (no `status`, no `diff`, no mutation): `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`, `git log --oneline -1 <sha>`, `git log --oneline <a>..<b>`, `git log --oneline --ancestry-path <a>..<b>`, `git log --oneline -8 --name-only <sha>`.

---

**End of draft.** Prepared by lane P30-LUNA as an independent drafting analyst. It contains no acceptance decision, no readiness claim, no host or account action, and no executed drill.
