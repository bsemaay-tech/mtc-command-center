# Deploy / restore / phone-alert packet (WP-P0-26)

**Lane:** P26PREP · SuperGrok (grok-4.6) · 2026-09-13
**Authorization used to write this file:** owner chat "C YES" = read-only preparation of a packet listing host steps the owner would *later* authorize.
**This packet authorizes nothing. Nothing in it was executed. No host was contacted. No schedule was installed. No message was sent. No credential was created. No collector was started.**

Every host-executing step is **T0 for that step** and is mapped to gate **G9 (host contact)**, in addition to G1-IA, never instead of it. The plan: "the step requires the owner's authorization per session; the deployed state is `UNVERIFIED` and must not be assumed; … nothing here is authorized." (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:584`; same mapping for P030 host-install at `:640`).

A later owner reply that names **this packet, the step ids, the session, and the host** is what would authorize those steps. A reply that only answers O-1..O-10 does **not** authorize G9.

Deployed backup, monitoring, restart and rollback configuration is `UNVERIFIED` pending G9 (`:581`). Treat it as unproven, never as satisfied.

---

## How to read a step row

| Column | Meaning |
|---|---|
| **ID** | Stable id. Quote it in the later authorization sentence. |
| **Host** | `none` / `KVM2` / `owner-PC` / `both`. |
| **Gate** | `—` (paper / T-A, no host) · `G9` (host contact). |
| **Tier** | T1 local tooling · **T0** any step that executes on a host. |
| **Owner authorization required before this step** | The exact sentence the owner would have to give. Until that sentence exists, the step is forbidden. |
| **Evidence artefact** | File(s) a later executing lane must produce. None of them exist yet. |

Placeholders in angle brackets are owner facts (O-1, O-2, O-3, …). They are not paths this lane verified.

---

## 0. Preconditions that are **not** host steps (must precede §A)

These are listed so a later G9 session cannot skip them. They are not authorized by "C YES".

| ID | What | Gate / tier | Owner authorization required before this step | Evidence artefact |
|---|---|---|---|---|
| P-0 | Owner answers O-1..O-10 in V3 §5 (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:573-590`) | — | A written owner reply naming each O-item. Recommended answers stay as V3 wrote them; this packet does not re-decide them. **O-3 ratification is a number, not a schedule.** | Dated owner-answer note |
| P-1 | O-9 implementation of the §4.1 identity bridge | — / T1 | O-9 approval of the design in `BACKUP_COMPLETION_REPAIR_DESIGN.md` (recommended: Option A), then a normal T1 implementation lane | Merged (or at least reviewed) producer change; T-A-1..T-A-12 results |
| P-2 | O-8 T-A fixture drills D-1, D-2, D-13 RED, and D-8, D-9, D-10 (parallel T-A branch, not under D-13/O-9; `P030_P026_CONFIG_DRILL_CHOICES_V3.md:476-489`); then after P-1: D-13 GREEN, D-3, D-3b, D-4, D-5, D-6, D-7 | — / T1 | O-8: "scratch fixtures only, no host, no network, no credential, no schedule, no real evidence store, no send". D-13 GREEN is **out** of O-8 (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:445, 550`) | Per-drill transcripts under a scratch directory |
| P-3 | Notifier *class* added to `NOTIFIERS`, unit-tested against a **local HTTP stub only** | — / T1 | O-8's notifier-stub clause (`NOTIFIER_PROPOSAL.md:90-91`: "unit-tested with a local HTTP stub (no real send in tests)") plus O-5's technology pick. **No real send.** | Stub-test PASS transcript; `watchdog.py` still ships `local_log` as default |
| P-4 | C-11 state-dir transport design written and accepted | — | Owner names the mechanism that makes KVM2's heartbeat directory visible to a checker on the owner PC. Until then D-16/D-17 are not startable: an absent dir is `check_failed` `"state dir does not exist"` (`watchdog.py:131-136`), not process silence. Recommended (reasoning, not a sourced design): owner-PC-local replica *pulled* from KVM2, refresh ≪ silence bound | One-page transport note naming pull vs mount, interval, and failure mode |

P030 `run` stays refused (`market_data_collector.py:534-538`) until O-6 *and* G9. Heartbeat, backup of a *fixture* stable-prefix, and watchdog can be installed and drilled without starting the collector. Backing up a *real* collector archive cannot.

---

## A. Install / config of backup + watchdog + heartbeat

Plan outputs: automated second-location copy, daily backups, checker **outside** the watched host, phone push, host NTP/drift check (#45) (`MASTER_WORK_PACKAGE…:580`). Package installs no schedule (`watchdog.py:1-6`; `README.md:65, 104`: "NO schedule is installed by this package — host installation is gated behind G9").

Cross-copy direction the plan names: "cross-copy VPS ↔ owner PC" (`:580`). For this archive that means: live store on the collector host (KVM2 — V3 C-3 recommended target A, owner binds the path at G9), second location on the owner PC (O-2). Checker on the owner PC.

### A.1 KVM2 — watched host (collector archive + heartbeat emitter)

| ID | Step | Host | Gate | Tier | Owner authorization required before this step | Evidence artefact |
|---|---|---|---|---|---|---|
| S-A1 | Open a G9 session that names KVM2 and this packet's KVM2 steps | KVM2 | **G9** | T0 | Exact sentence: **"G9 this session: contact KVM2 to execute P026 packet steps S-A2..S-A8 only. No credential read. No notifier send. No schedule yet. No collector `run`. No restore onto a live store."** | Session log with start/end UTC-Z, operator name, step ids |
| S-A2 | Confirm (do not assume) Python ≥ 3.12 is present; stdlib only (`README.md:8`) | KVM2 | G9 | T0 | Covered by S-A1 | `python --version` transcript |
| S-A3 | Place the P026 tooling tree `MTC_COMMAND_CENTER/tools/opsa/` and the P030 adapters + collector modules onto KVM2 at an owner-named `<KVM2_TOOL_ROOT>`. Do not git-pull from this packet; copy method is the owner's. | KVM2 | G9 | T0 | Covered by S-A1, plus O-1/O-2 path names | SHA-256 of the ten files matching `REPORT.md`'s source table (that table omits `opsa_common.py`, which `backup.py:37-39` imports, and omits README / `config.example.json`) |
| S-A4 | Create `<ARCHIVE_ROOT>` (O-1) with layout parent only. Do not seed bars. Mode/owner as the host's existing evidence-store practice. Collector still not started. | KVM2 | G9 | T0 | O-1 answer **and** S-A1. Recommended: bind the concrete path in this same session (V3 C-3). | `dir`/`ls` of empty `<ARCHIVE_ROOT>`; free-space figure |
| S-A5 | Create `<KVM2_HB_DIR>` for heartbeat files. Id **not written yet** until C-6 is used. Recommended id (V3 C-6, Lead default): `p030_market_data_collector`. Must be one segment, no comma, no `/` (`heartbeat.py:45`; `watchdog.py:137-138, 276`). | KVM2 | G9 | T0 | S-A1 | Empty directory listing |
| S-A6 | Emit one heartbeat with the P030 adapter (or `heartbeat.py emit`) into `<KVM2_HB_DIR>` as a host smoke, then stop. Interval default 60 s is a shipped CLI default (`heartbeat.py:76`), not a contract. Do **not** leave a `loop` running until S-A8. | KVM2 | G9 | T0 | S-A1. Not a phone send. | `<KVM2_HB_DIR>/<id>.hb.json` bytes; `verify_process_heartbeat` transcript |
| S-A7 | Host NTP / drift check (#45), as the plan's host-side item (`:580`; `README.md:106-108`: "NTP/drift check (#45) — host-side, arrives with the G9-gated host step"). Record offset. Watchdog already classifies far-future stamps as `clock_skew` (`watchdog.py:112-114`). | KVM2 | G9 | T0 | S-A1 | NTP offset record, UTC-Z |
| S-A8 | **Do not** enable a systemd unit, Task Scheduler job, or cron in this first KVM2 session unless the owner *adds* schedule words. The package's `Restart=no` / "no systemd install enablement" line is a **repository record**, not a verified deployed fact (`MASTER_WORK_PACKAGE…:581`). Leave any long-running emitter off until a later sentence names it. | KVM2 | G9 | T0 | A **second** sentence if scheduling is wanted: **"G9 this session: install heartbeat `loop --interval 60 --id <id>` on KVM2 under `<KVM2_HB_DIR>`. No collector `run`. No watchdog on KVM2."** Without that sentence, skip. | If installed: unit/task file copy + `is-enabled` equivalent; if skipped: explicit SKIP record |

Watched process on KVM2; **checker is not installed on KVM2**. Plan: checker outside the watched host (`:580`; `NOTIFIER_PROPOSAL.md:19-21`).

### A.2 Owner PC — second location (backup root + checker + notifier)

| ID | Step | Host | Gate | Tier | Owner authorization required before this step | Evidence artefact |
|---|---|---|---|---|---|---|
| S-A9 | Open a G9 session that names the owner PC and this packet's owner-PC steps | owner-PC | **G9** | T0 | Exact sentence: **"G9 this session: use the owner PC to execute P026 packet steps S-A10..S-A16 only. No KVM2 contact in this sentence. No real phone send yet. No restore onto a live store."** | Session log |
| S-A10 | Place the same tooling tree at `<PC_TOOL_ROOT>`; SHA-256 match S-A3 | owner-PC | G9 | T0 | S-A9 | SHA-256 table |
| S-A11 | Create `<BACKUP_ROOT>` on a **different device or host** from `<ARCHIVE_ROOT>` (plan `:580`; V3 O-2). Create `<BACKUP_ROOT>/configs/` for generated per-capture configs (V3 C-13). Do not put a config inside a capture's own stable-prefix directory (adapter `:256-257, 267`). | owner-PC | G9 | T0 | O-2 answer **and** S-A9 | Empty `<BACKUP_ROOT>` listing; statement that it is not the archive volume |
| S-A12 | Create `<PC_HB_DIR>` — the directory the *checker* will read. Wire the C-11 transport from `<KVM2_HB_DIR>` into it (P-4). Do not mount KVM2 as the checker's only view if host death should still be distinguishable (D-17). | owner-PC | G9 | T0 | S-A9 **and** P-4 | Transport config copy; one successful replica listing of the S-A6 smoke beat (or an honest failure record) |
| S-A13 | Write a **non-scheduled** watchdog invocation file (script or documented command) using V3 C-9's shape, with `<OWNER_RATIFIED_BOUND>` from O-3. If O-3 was "defer", `--notifier local_log` only and **do not schedule**. `--now` must not appear (`watchdog.py:42, 255-256`). `--expect` must list the heartbeat id (`watchdog.py:144-146`). `--state-file` must be set (`:200-235, 280-286`). | owner-PC | G9 | T0 | O-3 **and** S-A9. O-3 does **not** by itself install a schedule (V3 `:590`). | Command file; one manual `local_log` run transcript |
| S-A14 | If O-3 ratified a bound **and** the owner wants a schedule: install the one-shot checker on a cadence the owner names (V3 proposed 5 minutes — **no repository basis**, `P030_P026_CONFIG_DRILL_CHOICES_V3.md:259`). Still `--notifier local_log` until S-C2. | owner-PC | G9 | T0 | Extra sentence: **"G9 this session: schedule watchdog.py on the owner PC every <N> minutes with --silence-seconds <BOUND> --notifier local_log. No phone send."** | Task/cron copy + one scheduled-run log |
| S-A15 | Generate the first per-capture backup config (V3 C-4 draft shape) pointing `backup_root` at `<BACKUP_ROOT>`, store id `p030_closed_partition`, `class` `"protected"`, `path` a directory that **does not exist yet**. Do not run backup against the live archive in this step. | owner-PC | G9 | T0 | O-2 **and** S-A9 | Config file under `<BACKUP_ROOT>/configs/<label>.json` |
| S-A16 | Dry-run backup of a **fixture** stable-prefix only (`backup.py --dry-run`, `backup.py:207-215`). Writes nothing (`:104-109`). | owner-PC | G9 | T0 | S-A9. Fixture may live on the owner PC; if the fixture is created on KVM2 this step also needs S-A1 still open. | Dry-run JSON header/footer; proof no `runs/` directory and no `manifest.jsonl` appeared |

### A.3 Explicitly not in §A

- Collector `run` (O-6 + future permission protocol + G9 of its own; plan `:632, :640`).
- Filling `p030_opsa_backup_config.json` in the repo (shipped nulls are fail-closed; `p030_opsa_backup_config.json:3,6,7`; `opsa_common.py:232-239`). Generated configs live under `<BACKUP_ROOT>/configs/`.
- Phone notifier registration in `NOTIFIERS` for *real* delivery (that is §C, after stub tests in P-3).
- Retention / size-budget deletions (plan `:581(b)`; `README.md:105`).
- Any write to a live evidence store.

---

## B. RED / GREEN restore drill on copies

Plan acceptance: "the restore drill is RED/GREEN per D026 (an un-backed-up loss is shown unrecoverable; the backed-up copy restores byte-identically)" (`MASTER_WORK_PACKAGE…:585`). Protected surfaces: "restore drills run on copies, never the live store" (`:583`).

The 2026-08-25 lane already reported this **on fixtures** (`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md:95-100`): "dry-run-writes-nothing PASS; backup+readback PASS; RED unrecoverable-without-backup PASS (0/3 baseline hashes remain in damaged live tree); GREEN restore PASS (3/3 byte-identical, empty dir preserved); tampered-backup refused PASS (rc 1)". That does not satisfy D-15 against real stores (V3 D-15). This packet is the real-store / copy-store version. **Reconciliation** required by plan `:581(c)` is still unbuilt (V3 NV-5) — D-15 cannot claim a backup "counts" for clock-gating without it.

Prefer T-B (both roots local copies on the owner PC). If either root is on KVM2, the step is T-C / G9.

| ID | Step | Host | Gate | Tier | Owner authorization required before this step | Evidence artefact |
|---|---|---|---|---|---|---|
| S-B0 | Confirm P-1 (O-9) is in: a collector-shaped partition can be captured. If O-9 is not done, run this drill only against adapter `_line()` fixtures and **label it fixture-only**, not D-15. | none | — | T1 | O-9 for collector-shaped data; O-8 already used for fixture D-5 | T-A-5 transcript or an explicit FIXTURE-ONLY banner |
| S-B1 | Create an isolated **copy** of the store-under-test under `<DRILL_LIVE_COPY>`. Never the live `<ARCHIVE_ROOT>`. | owner-PC (or KVM2 if the copy is made there) | G9 only if the copy is taken *from* KVM2 | T0 if host copy; else T1 | If copying off KVM2: **"G9 this session: read-only copy of <ARCHIVE_ROOT> into <DRILL_LIVE_COPY> on the owner PC. No delete on KVM2. No restore onto <ARCHIVE_ROOT>."** If the drill uses a synthetic collector-shaped fixture on the owner PC: O-8 is enough and this row is not G9. | Copy manifest (path, size, SHA-256 per file) = **baseline** |
| S-B2 | Capture stable prefix of the copy (D-3 / D-3b), then `backup_stable_prefix` into `<BACKUP_ROOT>` (D-4). Store path = that capture's directory (C-4). | owner-PC | G9 only if `<BACKUP_ROOT>` creation was G9 (already S-A11) | T0 if those roots are the real host volumes; T1 if both are drill volumes | "Execute P026 packet S-B2..S-B7 on copies under `<DRILL_*>` and `<BACKUP_ROOT>`. No live-store restore." | `_P030_STABLE_PREFIX.json`; `manifest.jsonl` `run_start`/`file`/`run_end` with `status: ok`, `readback=match`; adapter three-way byte compare (`p030_closed_partition_backup_adapter.py:651-678`) |
| S-B3 | **RED — un-backed-up loss.** Damage `<DRILL_LIVE_COPY>` (flip bytes / remove files). Show that the damaged copy no longer matches baseline hashes **and** that recovery *without* the backup is impossible (0/N baseline hashes remain). | same as S-B1 | same | same | Covered by S-B2's sentence | Hash table: 0/N match; commands + output (D026 shape, `RESTORE_DRILL_EVIDENCE.md:15-16`; command block `:93-98`; `:88` is the A3 heading) |
| S-B4 | **GREEN — restore to an empty target.** `restore_verified_prefix` onto `<DRILL_RESTORE_TARGET>` that is empty (`p030_closed_partition_backup_adapter.py:687-688`). Adapter already runs `--check-only` first against an isolated temp copy of the backup root (`:703-742, 560-622`). | owner-PC | G9 if real `<BACKUP_ROOT>` | T0/T1 as above | Covered by S-B2. **Forbidden:** `--to <ARCHIVE_ROOT>` or `--to <DRILL_LIVE_COPY>`. | `_P030_VERIFIED_RESTORE.json`; N/N byte-identical to **baseline** (not to the damaged copy); empty-dir preservation if the fixture had one |
| S-B5 | **RED — tampered backup.** Flip one byte in `runs/<run_id>/<store_id>/` snapshot; run S-B4 against a fresh empty target. Expect check-only failure, nothing written (`restore.py:60-70, 169-174`; adapter `:727-728` `"P026 check-only failed; restore withheld"`). | owner-PC | same | same | Covered by S-B2. Never tamper the only copy of a real backup; tamper a copy of the backup tree. | rc ≠ 0; empty target still empty; error text |
| S-B6 | Optional RED — incomplete-run manifests (D-7) | none | — | T1 | O-8 | Refusals `"restore requires one complete successful P026 run"` (`p030_closed_partition_backup_adapter.py:482-509`) |
| S-B7 | Record what this drill does **not** prove: plan `:581(c)` reconciliation; production recovery procedure; second-device placement as a hardware fact (a config can point both roots at one disk — human check at S-A11). | — | — | — | none | Honest residual paragraph in the drill evidence file |

**Daily cadence** of real captures (C-5) is a *schedule* on the host, not this drill. If the owner later wants daily high-water captures, that is a separate G9 sentence after P-1 and S-A11, naming the cadence the plan already ratified (`:580, :581(b)`). Monthly-only is an explicit O-2 departure.

---

## C. Phone-alert delivery test and detect-to-delivery measurement

Plan acceptance: "the watchdog is proven by **killing a watched heartbeat and receiving the push on the owner's phone** — the functional delivery requirement, which is binding"; "the detect-to-delivery elapsed time is measured on the candidate technology's real behaviour and recorded, and that measurement is put to the owner, whose ratification of an exact bound is required before any time bound is enforceable as acceptance" (`MASTER_WORK_PACKAGE…:585`). Until that drill runs, WP-P0-26 acceptance stays OPEN (`NOTIFIER_PROPOSAL.md:94-96`).

`OPEN-N14` is "What is the maximum allowed time from collector failure detection to owner notification delivery?" (`market_data_collector.py:48`). One measurement is an observation, not a ratified bound (V3 D-16). `--silence-seconds` is a *detection* bound only (V3 C-8 constraint 3); do not write it down as N14.

Phone OS (O-4) first: self-hosted ntfy on iOS needs the upstream APNS relay (`NOTIFIER_PROPOSAL.md:62-67`). V3 C-10 recommended B (public ntfy.sh) for the first measured drill and A (self-hosted ntfy) as steady state — copied, not re-decided. Aug-25 external facts must be re-verified at adoption (`NOTIFIER_PROPOSAL.md:9-11`). This lane did no network.

| ID | Step | Host | Gate | Tier | Owner authorization required before this step | Evidence artefact |
|---|---|---|---|---|---|---|
| S-C0 | O-4 OS answer + O-5 technology answer + P-3 stub tests green | none | — | T1 | O-4, O-5, O-8 stub clause | Those three artefacts |
| S-C1 | Re-verify the chosen candidate's external facts (pricing, limits, iOS relay, topic-as-bearer) | none (docs) / network if the owner later authorizes a lookup | network is **not** G9 but is still not authorized by "C YES" | — | A later sentence if a live lookup is wanted. This packet does not perform it. | Dated re-verification note |
| S-C2 | Install the chosen notifier on the **owner PC checker** (not on KVM2). For ntfy.sh: long random topic, no signup. For self-hosted ntfy: binary on the owner PC (`NOTIFIER_PROPOSAL.md:50-58, 76-79`). Register the class in `NOTIFIERS` (`watchdog.py:91-94`; `README.md:95-99`). Topic/token is a bearer capability (`NOTIFIER_PROPOSAL.md:72-74`) — store it as a host secret, **never** in Git, issues, evidence, or ordinary backups (plan `:621` secret handling is WP-P0-29 policy; this packet still must not write a secret). | owner-PC | **G9** | T0 | Exact sentence: **"G9 this session: install <ntfy.sh \| self-hosted ntfy> on the owner PC and register the notifier in watchdog.py. No send yet except the S-C3 test push I am about to authorize. No KVM2. No credential on KVM2."** | Install record; `NOTIFIERS` key name; **redacted** topic fingerprint (not the topic) |
| S-C3 | One **deliberate** test push to the owner's phone (not a killed-heartbeat yet) so the channel is known to work before the acceptance drill. | owner-PC | G9 | T0 | Extra words in the S-C2 session or a new one: **"Send one test push to my phone now."** | Photo or screenshot of the phone notification + UTC-Z send timestamp. Payload must contain no secrets and no controls (`watchdog.py:28`) |
| S-C4 | Point the scheduled (or manual) checker at `--notifier <chosen>` instead of `local_log`. Keep `local_log` in parallel if wanted (second `--` is not supported; run two invocations or have the notifier also append — do not invent a dual-notifier without a code change). Recommended: one invocation, chosen notifier, plus the existing JSONL if the chosen class also writes a file. | owner-PC | G9 | T0 | **"G9 this session: switch the owner-PC watchdog invocation to --notifier <name>. Silence bound remains <BOUND>."** | Updated command file |
| S-C5 | **Acceptance drill (binding functional test).** With a fresh heartbeat looping (S-A8 or a manual `heartbeat.py loop` on KVM2 under a G9 sentence), **kill** the watched process. Do not write a "stopped" marker (`heartbeat.py:13-15, 105-107`: silence is the signal; Ctrl-C is swallowed). Wait for the next checker run. | KVM2 (kill) + owner-PC (checker) + owner's phone | **G9** | T0 | Exact sentence: **"G9 this session: kill the watched heartbeat <id> on KVM2 and receive the push on my phone. Record detect-to-delivery time. No collector `run`. No live-store restore. No trading."** Checker must already be on the owner PC (S-A12..S-A14). | (1) kill UTC-Z; (2) last `emitted_at` from the heartbeat file; (3) checker stdout JSON with `silent` or `missing` and rc 2 (`watchdog.py:115-118, 288-289`); (4) notifier event JSON; (5) phone-received UTC-Z; (6) elapsed **detect→delivery** (checker alert time → phone time) and elapsed **kill→delivery** (honest extra) |
| S-C6 | Put the measured detect→delivery elapsed time to the owner. **Do not write it into the code as `--silence-seconds` or as `OPEN-N14`.** The owner may ratify an exact bound later; until then the bound stays `[OPEN]` and no `[OPEN]` value counts as satisfied (`MASTER_WORK_PACKAGE…:585`). | none | — | — | A later owner sentence: "I ratify detect-to-delivery bound = <N> seconds" — **not** requested now (V3 `:590`) | Measurement note + owner ratification-or-defer |
| S-C7 | **D-17 host-loss discrimination** (optional in the same session only if P-4's transport is in). Stop the *host* (or unplug the replica), not just the process. Record `silent`/`missing` vs `check_failed` `"state dir does not exist"` (`watchdog.py:131-136`). | KVM2 + owner-PC | G9 | T0 | **"G9 this session: stop KVM2 (or the heartbeat replica) to run D-17. Checker stays on the owner PC."** | Two-outcome table |
| S-C8 | Explicitly **not** proven by S-C5: collector-failure→detection, unless the killed heartbeat was the collector's own (collector `run` is still refused). N14 spans detection to delivery (`market_data_collector.py:48`); S-C5 measures the delivery half after a watchdog-detected silence. | — | — | — | none | Residual paragraph |

---

## D. Order of later owner sentences (cheat-sheet)

Nothing below is requested by this lane. It is the order V3 §4.4 already wrote (`P030_P026_CONFIG_DRILL_CHOICES_V3.md:544-567`), turned into packet ids.

```
O-1..O-10 answers                         → P-0
O-9 design (this lane's Option A) + T1    → P-1
O-8 T-A drills + notifier stub            → P-2, P-3
C-11 transport chosen                     → P-4
G9 KVM2  S-A1..S-A8                       → tooling, archive dir, hb smoke, NTP
G9 PC    S-A9..S-A16                      → backup root, checker, local_log
G9 copies S-B1..S-B7                      → RED/GREEN restore on copies
G9 phone S-C2..S-C6                       → push received + measurement
then, separately, collector runtime O-6   → not this packet
then WP-P0-26 acceptance                  → still OPEN until S-B + S-C5 exist
then any forward clock                    → plan :585, :581(c); not this packet
```

---

## E. Owner-decision items this packet touches (questions + recommended answers, copied)

These are not new numbers.

| Ref | Question | Recommended answer (V3, not re-decided) |
|---|---|---|
| O-1 | Archive volume? | Placeholder now; bind at S-A4 |
| O-2 | Backup volume, per-capture shape, cadence? | Per-capture config; daily high-water + month-end; "monthly-only" only if you say so |
| O-3 | Silence bound? | Propose 300 s / 5 min check / 60 s emit; or defer. Not a schedule |
| O-4 | Android or iOS? | Answer the OS |
| O-5 | Notifier? | ntfy.sh first drill; self-hosted ntfy steady state |
| O-6 | Lift collector refusal? | Keep refused; not in this packet's G9 sentences |
| O-8 | T-A + stub notifier? | Approve with D-13 GREEN carved out |
| O-9 | Identity bridge? | Approve Option A (`BACKUP_COMPLETION_REPAIR_DESIGN.md`) |

---

## F. NOT VERIFIED (this packet)

| Ref | Not verified | Why |
|---|---|---|
| NV-P1 | That KVM2 exists in the assumed shape, its disks, Python, NTP, systemd, current backup/monitoring | Plan `:581` `UNVERIFIED` pending G9. This lane contacted nothing. |
| NV-P2 | Any of S-A* / S-B* / S-C* | None were run. Every evidence artefact is a *future* name. |
| NV-P3 | ntfy / ntfy.sh / Telegram / APNS behaviour in 2026-09 | `NOTIFIER_PROPOSAL.md:9-11` dates facts to 2026-08-25 and requires re-verification. No network here. |
| NV-P4 | Detect→delivery latency | Unmeasured until S-C5. |
| NV-P5 | State-dir transport | V3 NV-4; P-4 is a design hole, not a command. |
| NV-P6 | Reconciliation implementation | V3 NV-5; S-B7 must not claim plan `:581(c)` is met. |
| NV-P7 | 2026-08-25 drill transcripts beyond `LANE_REPORT.md:95-100` and `RESTORE_DRILL_EVIDENCE.md` headings + lines 1-30 | V3 NV-12. |
| NV-P8 | That a daily capture finishes in a day on the real volumes | V3 NV-16. |

---

**End of packet.** No step above has been authorized or executed.
