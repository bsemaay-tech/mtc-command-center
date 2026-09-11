# WP-P0-30 · VEN-E — venue market data: DESIGN DRAFT v1.9 (design only)

**Active version note:** v1.9 is the owner-addendum-31 fold. The v1.8 title is retained below,
collapsed as historical text, so the W290 snapshot comparison remains insertion-only.

<details>
<summary>RETAINED-HISTORICAL — superseded v1.8 title</summary>

# WP-P0-30 · VEN-E — venue market data: DESIGN DRAFT v1.8 (design only)

</details>

- Origin lane: W82. v1 recorded authority repo `C:\WFMERGE54` at HEAD `c18b6f3e`; the v1.1 and v1.2
  folds rechecked the read-only repository on branch `master` at HEAD
  `108ea066a710ff7ef5c09246903fe3d523da1d56`.
- Scope of this document: **design only.** Zero venue contact, zero network reads, zero host/KVM2
  action. No code, no commit. Build is gated on WP-P0-26 + WP-P0-21 acceptance and on
  per-session owner authorization for host-install steps (T0 / gate `G9`, plus `G1-IA`) —
  `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:640`.
- Every build-dependent choice below is labelled **PROVISIONAL**. No invented or owner-selected
  threshold is supplied; every unsettled numeric boundary is **[OPEN]** and blocks the surface it
  governs until the owner ratifies it. Source-fixed limits and ratified cadences remain fixed and
  cited — plan `:642`, `:518`, brief
  `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2332`.

**v1.9 qualification:** the retained v1.8 sentence above no longer describes the six owner-answer
limbs folded here. Owner addendum 31 now supplies the narrowly scoped decisions recorded in §8.1.1
and §8.2.1. Every boundary not expressly closed there remains `[OPEN]`; no unprovided value is
inferred.

## Change log

- **v1.9 (2026-09-02, W290 owner addendum 31 decision 104):** folded the owner's row-23 answer
  at the §8.1 decision site. `OPEN-F1` is now bar interval plus 15 seconds and `OPEN-F2` is now bar
  interval plus 45 seconds. Both are explicitly a **judgement based on illustrative values, not
  measured proof**. `OPEN-F3` remains open because decision 104 does not name per-interval
  overrides; `OPEN-F4` remains `OWNER-DEFERRED-TO-MEASUREMENT` because the owner directed that no
  recovery limit be set yet. Cross-draft echo **X-2** also names P020 build/checklist, P021 and P014,
  but none carries this P030 decision or these values; no sibling draft is changed by decision 104.
- **v1.9 (2026-09-02, W290 owner addendum 31 decision 105):** folded the owner's row-24 answer
  at the §8.2 decision site. The missing worker policy now defaults to stop when the feed falls back
  to slow polling; an explicit frozen strategy instruction remains the only way to choose otherwise.
- **v1.9 (2026-09-02, W290 owner addendum 31 decision 106; decision 54 shape precedent):** folded
  only the owner half of row 25 at the §8.1 decision site: one shared rate-limit coordinator is the
  selected mechanism, and the collector runs as one process until it exists. `OPEN-N7` remains open
  for the engineering-owned batch-size, pacing, coordinator implementation and measured-headroom
  work. Cross-draft echo **X-5** names P020's different shared-capital resource; W271 ungrouped the
  questions, so no P020 draft carries decision 106 and no sibling draft is changed by it.
- **v1.9 (2026-09-02, W290 owner addendum 31 decision 107):** folded the owner's row-26 answer
  at the §8.1 decision site. `OPEN-N9` is closed with calendar-month archive partitions; the Parquet
  substrate, JSON index and backup mechanics remain PROVISIONAL engineering work.
  Cross-draft echo **X-2** also names P020 build/checklist, P021 and P014, but none carries this
  P030 monthly-partition decision; no sibling draft is changed by decision 107.
- **v1.9 (2026-09-02, W290 owner addendum 31 decision 108):** folded only the 15m limb of the
  owner's row-27 answer at the §8.1 decision site: warn when only 40 days of venue history remain.
  Other timeframes remain `OWNER-DEFERRED-TO-MEASUREMENT`. Cross-draft echo **X-2** also names P020
  build/checklist, P021 and P014, but none carries this P030 decision or the 40-day value; no sibling
  draft is changed by decision 108.
- **v1.9 (2026-09-02, W290 owner addendum 31 decision 109):** folded the owner's row-28 answer
  at the §8.1 decision site. `OPEN-N15` is closed: the initial universe is only Hyperliquid BTC
  perpetual on 15m, 1h, 4h and 1d. `OPEN-N2` remains engineering-open for the connection count and
  topology needed to serve that decided universe.
- **v1.9 inventory after the fold:** **17 numeric tags plus 3 PROVISIONAL-question tags = 20 open**.
  The retained v1.8 inventory statements below remain historical measurements, not current counts.
- **v1.8 addendum (2026-09-02, W247 marker-only):** marked the §1.2 F07 residual **OPEN at its
  site** (§1.2 step 3). Marker only: no design text was changed or withdrawn, no numeric boundary
  was selected, no tag was created, and the inventory stays **21 numeric tags plus 4
  PROVISIONAL-question tags = 25** (re-measured from §8.1 and §8.2). v1.8 named the residual in its
  report but was not authorized to touch a line retained character-for-character since v1.6 —
  "Open, unrepaired, and named here so it does not vanish"
  (`C:\tmp\LANE_PROMPTS_20260828\W239_MISREAD_REPAIR_REPORT.md:195-196`) — and an independent pass
  measured it unmarked at the draft site: "DS85-F01 — LOW — job W239 — orphaned-dependent +
  unmarked residual" (`C:\tmp\LANE_PROMPTS_20260828\DETECT_DS85_W239_W240.md:8`). The site now
  carries the marker and the missing pointer to §1.5 and `OPEN-N7`. Recorded as a **v1.8 addendum
  row, not a v1.9 bump**, because this document's own version bumps rewrite retained lines — the
  title (`:1`), the supersession re-tag on the outgoing entry (as at `:50`, `:59`, `:68`), the
  §8.1 namespace label (`:924`) and the §9 limits header (`:986`) all say the version — and this
  change is insertion-only with zero deletions, so nothing it did earns a renumber. Disposition is
  in `C:\tmp\LANE_PROMPTS_20260828\W247_P030_F07_MARK_REPORT.md`.
- **v1.8 (2026-09-02, W239 misread repair):** repaired the three v1.7 conversions whose cited
  authority did not carry what was claimed, each decided from the authority's own words. **F09 —
  REPAIRED (restored, not withdrawn):** §2.4 no longer says WP-P0-04 "explicitly enforces none of
  it (plan `:331`)"; that sentence is the execution-critique-contracts row and does not reach the
  environment-lineage rule, which plan `:328` gates on a bit-identical **WP-P0-11** golden-suite
  re-run. The named gate is restored and marked NOT VERIFIED as running code; the in-scope
  `:331` uses in §6, §6.2 and Appendix A are untouched. **F07 — NARROWED:** the §1.5 withdrawal
  stands, but its sentence no longer claims the addendum specifies no venue rejection behaviour at
  all; the range does state an address-based throttle (`:78-80`), which reserves nothing across
  processes on one IP. **F02-2b — RECORDED:** the §8.2 table row for `[OPEN-P030-3]` stands, and the
  census point v1.7 dropped — that `event_id` had no construction, freeze note or deferral while
  `observation_id` had one — is restored as a §8.2 bullet in the form `[OPEN-P030-2]` already uses.
  No tag was added: the inventory is still **21 numeric tags plus 4 PROVISIONAL-question tags = 25**,
  measured from §8.1 and §8.2. No preimage, default or numeric boundary was selected. Plan and
  addendum were re-read read-only at repo HEAD `4ca0e5e8`; the fifteen retention claims were
  re-read character-for-character against the prior snapshot. Dispositions are in
  `C:\tmp\LANE_PROMPTS_20260828\W239_MISREAD_REPAIR_REPORT.md`.
- **v1.7 (2026-09-02, W228 DS55 repair; RETAINED-HISTORICAL — superseded by v1.8):** recorded dispositions for all nine DS55 findings: 3 MEDIUM
  (DS55-F01/F04/F06) and 6 LOW (DS55-F02/F03/F05/F07/F08/F09). F01 preserves the honest
  producer-observation preimage deferral and tags it BLOCKER `[OPEN-P030-2]`; F02 and F03 add
  the missing sidecar-event and provenance-manifest preimages as BLOCKERS `[OPEN-P030-3]` and
  `[OPEN-P030-4]`, without inventing bytes. F04–F09 name the reconciliation-liveness mechanism,
  correction-chain refusal inputs, fraction computation, observable rate-limit boundary,
  interpolation refusal, and environment-lineage refuser. The listed named-blocker inventory is
  now 21 numeric tags plus 4 PROVISIONAL-question tags = 25; no default or preimage was selected.
  The four DS28 retention groups were rechecked character-for-character against the prior snapshot.
- **v1.6 (2026-09-01, N111 independent-pass closure; RETAINED-HISTORICAL — superseded by v1.7):** closed the non-zero DS28 pass against the
  post-W157 body. **DS28-F01 — REPAIRED:** retained the corrected P2-seed pointers to §1.5 and
  Appendix A. **DS28-F02 — REPAIRED:** retained A13 on the defined §2.5 response and §3.3
  producer/enforcer contracts, and A15 on the executable-root inventory without an undefined route
  registry. **DS28-F03 — REPAIRED WITHOUT INVENTION:** replaced the generic current-state `[OPEN]`
  tag with `[OPEN-P030-1]` and added its one-sentence owner question in §8.2; no default was selected.
  **DS28-F04 — REPAIRED:** retained the pre-merge pointer to §1.5.1 and the producer-local gate in
  §4.2. The current-state header and limits labels now say v1.6; the v1.5 record remains tagged as
  historical. No acceptance or build authority is claimed.
- **v1.5 (2026-08-31, W157 DS28 fold; RETAINED-HISTORICAL — superseded by v1.6):** folded all four DS28 findings. **DS28-F01 — FOLDED:**
  corrected both stale P2-seed `§4` references to §1.5 / Appendix A. **DS28-F02 — FOLDED by
  narrowing to existing contracts:** removed the undefined route-registry operand from A13/A15;
  A13 now uses the §3.3 producer/enforcer registry plus §2.5 response contract, and A15 derives its
  complete import/call/route inventory from the executable roots without inventing another registry.
  **DS28-F03 — FOLDED:** tagged the DEGRADED per-worker default `[OPEN]` in §6.3 and §8.2.
  **DS28-F04 — FOLDED:** corrected the pre-merge quality pointer from §1.5.4 to §1.5.1 and §4.2.
  No acceptance or build authority is claimed.
- **v1.4 (2026-08-31):** folded all eight N101 findings into the acceptance-evidence chain:
  narrowed M1 to the reconnect-trigger measurement, completed DEGRADED entry/precedence rules,
  defined the validator projection and producer grouping, bound verdicts to canonical dataset
  content, removed downstream acceptance cycles, specified discriminating freshness/no-resize
  modified copies, inventoried two native plus one proxy producer, and made the zero-order/
  zero-credential boundary a finite reachability proof. Dispositions and the repeat/count sweep are
  in `C:\tmp\LANE_PROMPTS_20260828\W148_FOLD_REPORT.md`.
- **v1.3 (2026-08-31):** folded every stated DS20 finding (DS20-F01–F06): completed the
  DEGRADED-policy inventory, recorded the unused OPEN-N1/OPEN-N16 namespace positions, repaired
  OPEN-N13/F3/F4 tag traces, made the P2 loop apply the closed-bar gate before archive merge, and
  disambiguated the five semicolon-delimited plan `:641` acceptance clauses. The DS20 verdict
  header says five LOW findings, but its Findings section contains four LOW entries; no absent
  seventh correction was invented. Dispositions and the repeat/count sweep are in
  `C:\tmp\LANE_PROMPTS_20260828\W137_FOLD_REPORT.md`.
- **v1.2 (2026-08-30):** folded the deduplicated union of four N83 and two G30 v1.1 detection
  findings. The fold gives byte-identical P2 replays a recorded idempotent no-op disposition,
  makes the active WS connection count `OPEN-N2`, aligns the derived consumer view with the
  interior-native-hole rule, narrows the blanket numeric labels, and repairs Appendix B's ADR
  attribution. It retains the v1.1 DS10-F2 P2 polling branch with explicit provenance: that branch
  was added by the fold, remains design-only and PROVISIONAL, and is blocked on `OPEN-N18` and
  `OPEN-N4`. Individual dispositions, before/after evidence, the N83/G30 census split, and
  provenance are in `C:\tmp\LANE_PROMPTS_20260828\W102_FOLD_REPORT.md`.
- **v1.1 (2026-08-30):** folded all eight N79 detection findings and all six DS10 supplemental
  findings. The fold separates immutable candle observations from append-only reconciliation
  events, gives corrections an explicit version path, repairs the D026 RED/oracle design, restores
  the ratified daily reconciliation and backup cadences, closes missing availability/provenance and
  sole-authority proof contracts, names the DEGRADED polling mechanism, and leaves every new
  numeric discriminator `[OPEN]`. Individual dispositions and before/after evidence are in
  `C:\tmp\LANE_PROMPTS_20260828\W96_FOLD_REPORT.md`.

Authority block read in full: plan `:630-645` (WP-P0-30), `:632` (map #67 fold — collector is
the earliest deliverable), `:633` (retention arithmetic), `:634` (inputs), `:635` (outputs),
`:636` (map #79 — freshness emission), `:637` (map #95 — sole market-data authority), `:638`
(depends on WP-P0-26, WP-P0-21), `:639-640` (protected surfaces, audit tier, `G9`), `:641`
(acceptance gate), `:642` (freshness acceptance addition), `:643-645` (rollback, authority
boundary, non-goals). Retention decision and dual-track rule cross-checked against
`WAYFINDER_DECISION_FOLD_2026-08-23.md:21` (#44) and `:38` (blocks WP-V2A-08). Sole-authority
and provenance-visible rules cross-checked against `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md:19,31,42,52`.

---

## 0. Problem statement (from authority, cited)

The venue serves only a **hard rolling retention window** — empirically ≈ 5000 candles per
interval (plan `:633`; #44 probe `WAYFINDER_DECISION_FOLD_2026-08-23.md:21`):

| Interval | Retention ≈ (plan `:633`) | #44 probe note (`WAYFINDER_DECISION_FOLD_2026-08-23.md:21`) |
|---|---|---|
| 15m | ≈ 52 days | verified empty at 60 days back, full at 40 days back |
| 1h  | ≈ 207 days | — |
| 4h  | ≈ 2.3 years | — |
| 1d  | ≈ 13.7 years | — |

**Consequence:** every day without a running collector permanently loses venue candles at the
15m/1h edge; loss is not recoverable from the venue later (plan `:633`, `:635`). This is why the
map #67 fold makes the continuous native collector "this package's EARLIEST deliverable and the
platform's most time-critical wave-1 candidate" (plan `:632`).

This package owns venue market data **end to end** (plan `:633`): the native historical archive,
the live/shadow feed WP-V2A-08 consumes, the dual-track history rule, provenance stamping, the
one-time divergence study, and the rule that every promotion/eligibility verdict names which
venue's data produced it.

**Authority boundary (plan `:644`):** unauthenticated public reads only; zero orders; zero
credentials. It may warn or block per frozen policy; it **never resizes an order** (plan `:636`,
brief `:2329`).

---

## 1. Collector design

### 1.1 Two native producers plus one proxy producer, one archive

The design has **two independent native producers plus one proxy producer writing into the same
physical append-only archive**. The two native producers are required by plan `:635` and #44's
"continuous native collector + daily `candleSnapshot` cursor reconcile"
(`WAYFINDER_DECISION_FOLD_2026-08-23.md:21`); the proxy producer implements the same authority's
labelled deep-lookback track. Native and proxy observations share the §2 schema and archive root,
but remain distinct by `track`, `venue`, `source_producer`, and labelled segments (§3):

| Producer | Role | Cadence | Source shape |
|---|---|---|---|
| **P1 — live WebSocket subscriber** | primary; captures each bar as it closes | continuous | venue candle WS subscription per (symbol, interval) |
| **P2 — `candleSnapshot` cursor job** | gap-fill + reconciliation + cold-start backfill; bounded polling source while P1 is unavailable | daily (ratified cadence) + on-demand after any P1 outage | venue `candleSnapshot` REST-style cursor endpoint, paginated by time cursor |
| **P3 — proxy downloader** | labelled deep-lookback proxy only; never fills an interior native hole | on requested proxy ingestion | existing Binance-perp ccxt downloader (§3.2) |

**v1.9 decision-109 universe qualification:** the initial collector universe is only Hyperliquid BTC
perpetual on 15m, 1h, 4h and 1d. This selects the market/interval scope; it does not select the
engineering-owned WS connection count or multiplexing topology (`OPEN-N2`).

Rationale for two native producers: P1 alone loses bars across every disconnect; P2 alone cannot keep
pace with the 15m retention edge if it runs once per day and a multi-day outage occurs. P2 is
also the mechanism the D026 forced-disconnect fixture exercises (§5). This mirrors the existing
proven pattern: the ccxt cursor downloader in
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/data/download.py` is a **time-cursor paginator with
exponential backoff** — reused as the P2 seed (§1.5; Appendix A).

### 1.2 Subscribe (P1)

PROVISIONAL, pending WP-P0-30 build and the venue-doc facts that are owner-gated:

1. Open a WebSocket connection to the venue's public market-data endpoint. The design boundary is
   unauthenticated public reads, zero credentials (plan `:644`); whether the exact candle WS and
   `candleSnapshot` endpoints satisfy it is NOT VERIFIED and remains PROVISIONAL. ADR-0021 confirms
   separate testnet/mainnet endpoints and the WS recovery doctrine, but not endpoint authentication
   (`MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0021-hyperliquid-integration-policy.md:47-52`).
2. Subscribe one channel per (symbol, interval) in {15m, 1h, 4h, 1d} (plan `:635`).
3. Respect the shared-connection budget: **max 10 WS connections, 30 new connections/min, 1000
   subscriptions, 2000 messages/min** on one IP/VPS
   (`HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md:76-77`); the collector shares
   the IP-based 1200/min info-weight budget with any other process on KVM2 (`:83-85`). Those
   source-fixed maxima bound but do not select the topology. The active WS connection count and
   connection/subscription split are **[OPEN-N2]**; the subscription topology is blocked until
   that value and the symbol universe are ratified.
   **v1.9 decision-109 qualification:** the symbol-universe limb is now ratified as Hyperliquid BTC
   perpetual on 15m, 1h, 4h and 1d. `OPEN-N2` remains open only for the engineering-owned active
   connection count and connection/subscription topology within that decided universe and the
   source-fixed maxima.
   **Residual F07 (census `DS55-F07`, LOW) — OPEN at this site; marker only, nothing above is
   changed or withdrawn.** "Respect the shared-connection budget" and "the collector shares the
   IP-based 1200/min info-weight budget with any other process on KVM2 (`:83-85`)" above are a
   source-fixed maximum and a sharing fact, both individually true of the cited addendum range;
   neither grants VEN-E a reservable or observable share, and §1.5 records that "a shared-budget
   guarantee is not a VEN-E-held property; OPEN-N7 stays blocked until a coordinating mechanism or
   measured-headroom rule is named" (`:305-306`). This is the un-repaired half of the census F07
   line — "a shared rate budget consumed by processes VEN-E does not own and cannot observe"
   (`DS55_RUN.log:34`), whose two cited sites are this one (`DS55_RUN.log:35`) and §1.5
   (`DS55_RUN.log:36`). The §1.5 half was narrowed in v1.8; this half was named but deliberately
   left unedited as text retained character-for-character since v1.6 — "Open, unrepaired, and named
   here so it does not vanish" (`W239_MISREAD_REPAIR_REPORT.md:195-196`; site confirmed at `:178`,
   retention at `:179`). An independent pass then measured it unmarked here: "DS85-F01 — LOW — job
   W239 — orphaned-dependent + unmarked residual" (`DETECT_DS85_W239_W240.md:8`), "it is named only
   in the report — at the draft site it is unmarked (no `[OPEN-…]` tag, no pointer to §1.5 /
   `OPEN-N7`)" (`DETECT_DS85_W239_W240.md:11-12`). The missing pointer is supplied here: see §1.5
   and `OPEN-N7` (§8.1). **No new tag is created** — the residual is held by the existing
   `OPEN-N7`, so the inventory stays 21 numeric tags plus 4 PROVISIONAL-question tags = 25.
   **v1.9 inventory qualification:** the sentence above is the retained v1.8 marker measurement.
   After owner addendum 31 decisions 104-109, the current inventory is 17 numeric tags plus 3
   PROVISIONAL-question tags = 20 open; `OPEN-N7` remains one of them because decision 106 closes
   only its owner coordination half.
4. Maintain heartbeat / ping per venue protocol; treat missed heartbeats as a disconnect
   (ADR-0021 `:52` — "heartbeat, reconnect/backoff, resubscription, sequence/gap detection,
   stale-data state").
5. Each inbound message carries an interval-bucket open time and an is-final / closed flag
   (PROVISIONAL field names — owner-gated venue-doc read). The collector holds the **currently
   forming bar** in memory and does not write it (§1.4).

### 1.3 Reconnect (P1)

PROVISIONAL:

1. On disconnect (socket close, missed heartbeat, or parse-fatal), enter internal
   `connection_state = RECONNECTING`. This is not an emitted freshness value; emitted freshness
   remains limited to the seven-state vocabulary in §6.
2. Backoff schedule: exponential with jitter, base and ceiling **[OPEN-N3]**. Reuse the shape
   from `download.py:202-210` (`base_delay * (2 ** retry_count)` over
   `RequestTimeout / DDoSProtection / ExchangeNotAvailable / NetworkError`) — the retry classes
   and the escalation curve are proven; only the constants are [OPEN].
3. Cap the number of consecutive failed reconnects before the collector attempts the `DEGRADED`
   fallback. P1 remains the unavailable WebSocket producer; **P2 temporarily changes from
   its daily/on-demand job to bounded repeated `candleSnapshot` polling** at cadence
   **[OPEN-N18]**. This is the named REST recovery mechanism, not a new producer or a claim that P1
   itself polls (ADR-0021 `:52` "REST is a bounded recovery/reconciliation path"; brief freshness
   table `:2324`). The v1.1 fold added this branch as DS10-F2's disposition; it is design-only and
   PROVISIONAL, and it makes no venue-contact or endpoint-capability claim. The failed-reconnect cap
   remains **[OPEN-N4]**. Both unset values block the DEGRADED fallback path. The state is emitted
   only after polling is confirmed active; a reached cap without confirmed polling follows §6.2's
   `UNKNOWN` rule.
4. On reconnect: re-subscribe all channels, then **immediately trigger a P2 gap-backfill** for
   the window `[last_contiguous_closed_bar_open_time, now]` per interval (plan `:635`
   "candleSnapshot gap-backfill on reconnect"). Do not resume `FRESH` until that backfill lands
   and reconciliation passes → `RECOVERING` until then (brief `:2325`, `:2310-2311`).
5. Sequence/gap detection: if P1 delivers a closed bar whose open time is more than one interval
   after the last stored closed bar for that (symbol, interval), record the gap as first-class
   evidence and enqueue a P2 backfill for the missing span (plan `:636` "market-feed health
   emits the common WP-P0-04 freshness states and evidence"; ADR-0021 `:52` sequence/gap
   detection).

### 1.4 Bar-close semantics

Authority: the platform trades **on bar close** on 15m–1D bars (brief `:347`); `taken_at` is a
**bar-close timestamp** (brief `:1203`); evaluation cadence is "bar close on the bucket's
timeframe set" (brief `:1881`); stop revisions apply "at bar close" (brief `:1749`). Acceptance
requires "the feed's bar-close semantics match the #45 time-discipline rows" (plan `:641`); #45
time-discipline is carried as WP-P0-09 rows (`WAYFINDER_DECISION_FOLD_2026-08-23.md:41`).

Design rules:

1. **Only closed bars are written to the archive.** The forming bar is held in memory and
   exposed to live consumers as a separate, explicitly-marked "forming" datum — never persisted,
   never fed to an eligibility/promotion verdict.
2. A bar for interval *T* with open time *t0* is **closed** at *t0 + T* venue time. The
   collector writes it only after it has both (a) the venue's is-final flag (P1) or a
   `candleSnapshot` row whose open time ≤ `now − T` (P2), and (b) passed the write-path quality
    checks (§4.1–§4.3). Section 4.4 is consumer-side divergence evidence and is not a write-path
    gate.
3. **One canonical timestamp convention, recorded in the archive schema:** each row's
   `bar_open_time` is the interval open in UTC epoch ms; `bar_close_time = bar_open_time + T`.
   `download.py` and `io.py` already standardise on a single UTC `timestamp` column
   (`io.py:18`, `download.py:229`); the archive extends that to an explicit open/close pair to
   remove the "is this the open or the close?" ambiguity that the #45 rows exist to settle.
   Exact convention (label open vs close as the primary key) is **[OPEN-N5]** — owner-gated
   because it must match the WP-P0-09 #45 rows, which this lane may not read into as settled.
4. **Venue clock vs host clock:** the collector records the venue-supplied bar open time as
   authoritative for bucketing and separately records host receipt time. A host/venue clock
   skew beyond **[OPEN-N6]** raises the NTP/drift alarm that WP-P0-26 owns (`plan:580` "the host
   NTP/drift-alarm check (#45)").
5. **Late bars / corrections / replay:** `observation_id` is the stable producer-observation
   identity defined in §2.2. If a later P2 pull returns the same identity with byte-identical
   canonical producer bytes, the archive accepts an idempotent no-op: it appends an
   `ARCHIVE_DISPOSITION` event with `IDENTICAL_REPLAY_NOOP` referencing the existing immutable
   observation and appends no second candle row. This is a recorded terminal disposition, not a
   silent collapse. If OHLCV differs for an already-stored
   `(source_producer, symbol, interval, bar_open_time)`, it is accepted only as an explicitly
   versioned `CORRECTION` with a new `observation_id` and a `supersedes_observation_id` naming the
   prior observation (§2.2). Both differing observations remain; a `CORRECTION` event is appended
   and the current-best rule is deterministic (§2.5). Reusing one `observation_id` with different
   canonical bytes, or supplying an unlinked differing repeat, is a defect → FAIL. Nothing
   overwrites (plan `:643` "the archive is append-only and retained"; #44 mismatch handling =
   "stamp / measure / disclose", `WAYFINDER_DECISION_FOLD_2026-08-23.md:21`).

### 1.5 Backfill (P2)

PROVISIONAL. Reuses the `download.py` cursor loop shape directly (Appendix A):

1. For each (symbol, interval) and a target window `[start, end]`:
   - `cursor = start`
   - loop: request `candleSnapshot(symbol, interval, since=cursor, limit=batch)`;
     stop on empty response or on no-cursor-progress (`download.py:178-197`);
     first filter rows to the requested window with `bar_open_time < end` (`download.py:183`),
     then apply the §1.4.2 closed-bar gate before archive merge: only rows with
     `bar_open_time <= now - T` may proceed; hold or discard forming rows with
     `bar_open_time > now - T`;
     advance `cursor = last_row_open_time + 1` (`download.py:197`).
2. Batch size and inter-request pacing are **[OPEN-N7]**. The source-fixed 1200/min IP weight
   maximum is shared on KVM2
   (`HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md:73-85`) and constrains total IP
   traffic; it does not reserve a VEN-E share. VEN-E can meter only its own requests and cannot
   observe other processes on KVM2. The cited addendum states no IP-limit rejection behaviour and no
   cross-process reservation mechanism — its only throttle statement is address-based ("when throttled,
   one request per 10 seconds still allowed", `:78-80`) and reserves nothing across processes sharing
   one IP — so a shared-budget guarantee is not a VEN-E-held property; OPEN-N7 stays blocked until a
   coordinating mechanism or measured-headroom rule is named.
   **v1.9 decision-106 qualification — owner half decided, engineering half open:** one shared
   rate-limit coordinator is the selected coordinating mechanism. Until it exists, the collector
   runs as one process only. This answer does not supply a P2 batch size, inter-request cadence,
   coordinator implementation or measured safe headroom, and it does not convert the source-fixed
   IP maximum into a VEN-E reservation. `OPEN-N7` therefore remains
   `OWNER-ANSWERED-SHAPE, VALUE PENDING`; engineering owner: the WP-P0-30 / VEN-E build lane.
3. Retry classes and backoff identical to §1.3 step 2.
4. **De-dup and sort on merge** (`download.py:232`
   `drop_duplicates(subset=['timestamp']).sort_values('timestamp')`) is reused only inside one
   raw response batch. At the append-only archive boundary, identity is `observation_id`: P1 and
   P2 observations for the same slot are both retained; a first-seen identity appends one candle
   row; a byte-identical replay of an existing stable identity appends only the recorded
   `IDENTICAL_REPLAY_NOOP` disposition; and a valid differing same-producer correction is a new
   explicitly linked observation (§1.4.5, §2.2). No producer observation is silently collapsed.
5. **Cold start:** on first run for a (symbol, interval), P2 backfills the entire venue
   retention window (§0 table) so the archive begins as deep as the venue allows; everything
   older than that is dual-track proxy territory (§3).

### 1.6 Reconciliation (P1 vs P2)

Daily (ratified plan cadence) the collector compares, per (symbol, interval), the P1
closed bars against a fresh P2 `candleSnapshot` pull over the same window:

- **Match:** append a `RECONCILIATION_STATUS` event that identifies both immutable observations and
  sets the derived slot state to `RECONCILED`; the P1 observation is the canonical read and the P2
  observation is retained as corroboration, or a byte-identical P2 replay references the already
  retained P2 observation through its `IDENTICAL_REPLAY_NOOP` disposition.
- **Mismatch (OHLCV differ beyond [OPEN-N8] tolerance):** retain both rows, emit a
  `FEED_DIVERGENCE` evidence record (schema §2.3), append derived status `DIVERGENT`, and expose
  that slot as `UNKNOWN` until an owner-gated rule resolves it — "stamp / measure / disclose",
  never pick a winner silently (`WAYFINDER_DECISION_FOLD_2026-08-23.md:21`; plan `:635`
  divergence study).
- **P1 missing, P2 present:** backfill from P2, append derived status `BACKFILLED`, keep the gap
  record.
- **P1 present, P2 missing:** keep the P1 observation, append derived status `P2_ABSENT`
  (possible retention-edge expiry); do not delete.

All four outcomes are sidecar events keyed by stable slot and observation IDs; reconciliation never
mutates a candle observation (§2.2–§2.5).

This reconciliation is also the watchdog's liveness signal (§6): if the daily reconciliation
job does not run, the WP-P0-26 dead-man watchdog must notice.
The failing component is the daily reconciliation job; the failing input is that job not running
while the collector main loop and its ordinary heartbeat continue. VEN-E therefore gates its
watched-process heartbeat on a completed reconciliation within the ratified cadence; without that
gate, this reconciliation-liveness claim is withdrawn. The external dependency is verified in plan
`:580`: watched processes emit heartbeats and a checker outside the watched host detects silence and
delivers a push to the owner's phone. OPEN-N14 remains the owner-gated detect-to-delivery bound.

---

## 2. Archive + provenance schema

### 2.1 Storage substrate (PROVISIONAL)

Reuse `io.py` conventions: Parquet as the at-rest format (`io.py:43-46`, columnar, `pyarrow`),
CSV export path retained for portability (`io.py:47-54`), one file per
`(symbol, interval, calendar-partition)`. Partition granularity **[OPEN-N9]** (per-month vs
per-year vs rolling). A small JSON index mirrors `cache.py`'s `.cache_index.json` pattern
(`cache.py:39-60`) for fast "what do we hold" queries and for `list_datasets`-style metadata
(`io.py:178-239`).

**v1.9 decision-107 qualification:** `OPEN-N9` is closed: `calendar-partition` is a calendar month,
so the archive stores market data by month. Parquet, the JSON index and the WP-P0-26 backup
mechanics remain PROVISIONAL engineering choices; the owner decision does not settle those limbs.

The archive lives **on disk under WP-P0-26's second-location backup policy** (plan `:635`,
`:638`): automated cross-copy KVM2 ↔ owner PC, text-class metadata also to GitHub, daily backup
with hourly sync during active windows, protected classes never auto-deleted (plan `:580`). The
candle archive is a **protected class** for backup purposes — losing it re-incurs the permanent
retention loss.

### 2.2 Candle row schema (PROVISIONAL field names; append-only)

| Field | Type | Notes / authority |
|---|---|---|
| `observation_id` | str | stable producer-observation identity and archive idempotency key; a byte-identical producer replay reuses it, while differing canonical bytes require a new ID and linked `CORRECTION` |
| `producer_payload_hash` | str | hash of the frozen canonical producer bytes; proves byte identity for replay and makes same-ID/different-bytes refusal executable |
| `symbol` | str | venue-native symbol |
| `interval` | enum {15m,1h,4h,1d} | plan `:635` |
| `bar_open_time` | int (UTC epoch ms) | interval open; bucketing key (§1.4.3) |
| `bar_close_time` | int (UTC epoch ms) | `= bar_open_time + interval` (§1.4.3) |
| `open` `high` `low` `close` `volume` | float | OHLCV; same 5 columns as `io.py:18` |
| `venue` | str | e.g. the venue id — provenance (plan `:635`, `:637`) |
| `track` | enum {`NATIVE`, `PROXY`} | dual-track (plan `:635`; §3) |
| `proxy_source` | str \| null | e.g. `BINANCE_PERP:<symbol>` when `track=PROXY`; null when NATIVE (§3) |
| `source_producer` | enum {`WS_LIVE`, `CANDLE_SNAPSHOT`, `PROXY_DOWNLOAD`} | which producer wrote the row |
| `observation_type` | enum {`INITIAL`,`CORRECTION`} | `CORRECTION` is legal only with `supersedes_observation_id` |
| `supersedes_observation_id` | str \| null | exact prior same-producer observation replaced in the derived view; null for `INITIAL` |
| `ingest_time` | int (UTC epoch ms) | host receipt/write time (§1.4.4) |
| `venue_seq` | int \| null | venue sequence number if provided (gap detection, ADR-0021 `:52`) |
| `env_lineage_id` | str | FK to §2.4 — Python version, lockfile hash, OS of the collector build (WP-P0-04 rule, plan `:328`) |
| `schema_version` | str (semver) | archive schema version |

**Append-only:** rows are never updated or deleted (plan `:643`). Corrections and late bars
land as new, explicitly linked `CORRECTION` observations with a later `ingest_time`; reconciliation
state is never stored on or stamped into a candle row. The derived "current best" view (§2.5)
chooses among immutable observations and append-only status events by documented rule, and that
choice is reproducible. Repeated ingestion of the same stable `observation_id` is accepted only
when its canonical producer bytes are identical; it produces an append-only
`IDENTICAL_REPLAY_NOOP` disposition rather than a second candle row. Same-ID/different-bytes is
refused. A correction chain must stay within the same producer/symbol/interval/slot; a missing
target, cycle, cross-slot link, or two corrections claiming the same successor position is refused.

### 2.3 Evidence / divergence record schema (PROVISIONAL)

Emitted to an append-only sidecar store (not the candle archive):

| Field | Notes |
|---|---|
| `record_type` | enum {`GAP`, `FEED_DIVERGENCE`, `RECONNECT`, `FRESHNESS_TRANSITION`, `BACKFILL_RUN`, `PROXY_NATIVE_DIVERGENCE`, `RECONCILIATION_STATUS`, `CORRECTION`, `ARCHIVE_DISPOSITION`} |
| `event_id` | stable unique identity for the immutable sidecar event |
| `symbol`, `interval` | scope |
| `slot_id` | stable `(venue, symbol, interval, bar_open_time)` identity |
| `observation_ids` | exact immutable candle observations this event identifies, compares, or assigns a disposition to |
| `window_start`, `window_end` | UTC epoch ms |
| `detected_at` | UTC epoch ms |
| `detail` | structured: e.g. `{missing_bars: N}`, `{ohlcv_delta: {...}}`, `{from_state, to_state}` |
| `producer` | which producer / job raised it |
| `env_lineage_id` | §2.4 |
| `deployment_identity_hash` | when the record supports an eligibility/promotion verdict (plan `:518` verdict-record field set) |

The `event_id` byte preimage is **BLOCKER [OPEN-P030-3]** and is frozen through the §8.2
question before an immutable sidecar event contract can be built; this design does not invent it.

### 2.4 Environment-lineage record (WP-P0-04 compensating rule)

WP-P0-04 excludes Python version / lockfile / OS from the identity hashes **but requires every
evidence artifact to additionally record its environment lineage** (plan `:328`). The collector
therefore stamps `env_lineage_id → {python_version, lockfile_hash, os}` on every candle row and
every evidence record. An environment change forces a bit-identical golden re-run before evidence
continues (plan `:328`).
Detector: before every candle-row or evidence-record emission, the collector build compares its
live `env_lineage_id` with the lineage admitted by the most recent bit-identical golden-suite run.
An attempted emission under a differing live lineage is the failing input and is refused until a
new golden run passes and admits that lineage. WP-P0-04 carries this as a decided contract rule and
names the gate: an environment change "must pass a bit-identical golden-suite re-run (WP-P0-11
goldens) before evidence continues; a golden divergence IS a material identity change"
(plan `:328`). The "defines shapes only and enforces none of them" sentence belongs to WP-P0-04's
separate execution-critique-contracts row (plan `:331`) and does not reach this rule, so this
document does not claim WP-P0-04 leaves environment lineage unenforced. Whether the WP-P0-11 golden
suite exists as running code is **NOT VERIFIED** here — plan `:391` and `:1069` describe the package
and its T0 gate only. No WP-P0-04 row (plan `:317-332`) names a VEN-E-side emission refuser, so this
local emission refuser is VEN-E-owned.

### 2.5 Derived "current best" view

A rebuildable, non-authoritative projection over the append-only archive:

- Per `(symbol, interval, bar_open_time)`: resolve each producer's acyclic correction chain first,
  then derive reconciliation state from the latest valid `RECONCILIATION_STATUS` event. Inside the
  native archive's time span, a missing, divergent, or unreconciled native slot stays `UNKNOWN`
  (`NOT BUILT` only when the native read route is absent) with its evidence; the view must not select
  an available `PROXY` observation for that slot. `NATIVE` is preferred over `PROXY` only for a
  native-covered slot; `PROXY` is eligible only before the native earliest bar or in the proxy
  segment of a boundary-straddling request already split per §3.1. Within an eligible NATIVE slot,
  prefer `RECONCILED` P1 over unreconciled. Candle observations remain unchanged.
- Chart/consumer contract (plan `:637`; `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md:19`):
  the consumer receives **the complete retained archive behind a bounded initial window**, plus
  freshness/evidence metadata; **absence is reported honestly** (one of the five availability
  classes `AVAILABLE NOW` / `CAPTURED — READ ROUTE MISSING` / `NOT BUILT` / `UNKNOWN` /
  `NOT APPLICABLE`, `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md:52`) — never reconstructed or
  interpolated.
- The view can be destroyed and rebuilt from the archive with no loss (mirrors plan `:643`
  rollback posture and the WP-P0-31 "derived view can always be rebuilt" pattern, plan `:650`).

---

## 3. Dual-track + labeling rules

Authority: plan `:635` (dual-track history rule; venue-provenance field on every research
artifact; divergence study; "every promotion/eligibility verdict states which venue's data
produced it — no silent proxy evidence"); #44 decision
(`WAYFINDER_DECISION_FOLD_2026-08-23.md:21` — "dual-track history: continuous native collector +
Binance-perp proxy for deep lookbacks, always labeled"); non-goal plan `:645` ("no re-blessing
of proxy-based artifacts — they keep their lineage class and provenance label").

### 3.1 Track selection rule

For a requested `[start, end]` window at interval *T*:

- Span inside the venue retention window (§0 table) **and** covered by the native archive →
  `track = NATIVE`.
- Span older than the native archive's earliest bar for *T* → `track = PROXY`, `proxy_source`
  set to the labelled Binance-perp equivalent.
- A window that straddles the boundary is returned as **two labelled segments**, never a
  blended single series (plan `:637` "no silent data blend").
- A requested slot inside the native archive's time span that is missing, divergent, or not yet
  reconciled is **not silently substituted with proxy data**. It is returned with the appropriate
  native provenance and availability `UNKNOWN` (or `NOT BUILT` only when the native read route is
  absent), plus its gap/divergence evidence. This classifies interior holes explicitly.

### 3.2 Proxy ingestion

The Binance-perp proxy is produced by the **existing** ccxt downloader
(`02_MTC_BACKTEST/src/data/download.py`, `defaultType: future`, `BTC/USDT:USDT` style symbols,
`download.py:41-48,53-76`) — reused as-is for proxy pulls, writing rows with `track = PROXY`,
`source_producer = PROXY_DOWNLOAD`, `venue = BINANCE_PERP`. No new downloader is written for the
proxy track.

### 3.3 Labeling / provenance stamping

- **Every** candle row carries `venue`, `track`, `proxy_source` (§2.2).
- **One authoritative stamp interface (PROVISIONAL downstream contract):**
  `VenueProvenanceStamp` writes an immutable manifest
  `{venue, track, proxy_source, window, native_fraction, proxy_fraction, archive_schema_version,
  env_lineage_id, dataset_content_hash, content_hash_algorithm, canonicalization_version}` and
  returns its content hash. `dataset_content_hash` binds the exact logical dataset/archive slice
  covered by the manifest under the frozen canonical-byte contract in §4.3; it is not the manifest
  hash. Every covered artifact/verdict has a required
  `venue_provenance_manifest_hash`; a missing, unknown, or content-mismatched hash is refused, not
  flagged. No writer may re-declare venue/track fields without binding this manifest.
  The manifest's own serialization, field order, and encoding are **BLOCKER [OPEN-P030-4]**:
  §4.3's canonical-byte contract is scoped to dataset content, not the manifest. They must be
  frozen before a downstream consumer can reproduce or verify the manifest hash; this design does
  not invent them.
  `native_fraction` and `proxy_fraction` are each computed by the VEN-E stamp writer at manifest
  emission as that track's row count within the manifest `window` divided by the total row count in
  the same window. The fixed rounding precision is recorded by `canonicalization_version`. Any
  acceptance threshold for either fraction remains `[OPEN]` and owner-gated.
- **Producer/enforcer registry contract (PROVISIONAL):** VEN-E publishes the machine-readable row
  shape, the VEN-E dataset/export writer row, and verifier-owned accepting-consumer fixtures. VEN-E
  acceptance requires those fixtures to refuse missing, unknown, content-mismatched, and proxy-
  incomplete stamps. It does **not** require a package that depends on accepted VEN-E to exist.
  Each later covered writer/consumer pair is added and proven at that consumer package's own gate:
  WP-P0-21 verdict writer → WP-V2A-10 admission authority; WP-V2A-10 decision writer → its
  loaders/readers; WP-V3-03 promotion-decision writer → its loaders/readers. Future research or
  verdict writers are not admitted by their own gates until registered.
- Those downstream carrier mappings remain **PROVISIONAL and BLOCKED at the downstream package's
  gate**, not at VEN-E acceptance. The checked plan rows for WP-V2A-10 and WP-V3-03 do not yet
  supply that venue-provenance carrier (plan `:769-778`, `:1004`).
- VEN-E's D026 modified copies remove or corrupt the stamp in verifier-owned research-artifact and
  verdict-carrier fixtures; the verifier-owned accepting consumer refuses each. The same modified-
  copy contract travels to each real consumer's gate. A dataset containing any `PROXY` row without
  the proxy-bearing manifest is invalid.

### 3.4 One-time divergence study

Authority: plan `:635` ("one-time divergence study quantifying proxy-vs-native differences on
the overlapping window once enough native history accumulates"); audit tier **T2** for the study
(plan `:640`).

Design:

- Trigger: native archive has accumulated **[OPEN-N10]** of overlap with the proxy series at
  interval *T* (owner-gated — "enough native history").
- Method: over the overlap window, per interval, compute per-bar OHLCV deltas
  (absolute + relative), close-to-close return correlation, volume ratio distribution, and
  count of bars present in one track but not the other.
- Output: a `PROXY_NATIVE_DIVERGENCE` evidence record set (§2.3) + a written T2 study document
  with the measured numbers. **No number is invented here** — if the overlap is insufficient the
  study reports "insufficient overlap" and stays open (C-4; plan `:525`).
- The study informs but does not set the [OPEN-N8] reconciliation tolerance or any promotion
  rule — those remain owner-gated.

---

## 4. Quality-gate reuse map (WP-P0-21 checks — PROVISIONAL)

Authority: plan `:635` ("quality gates reusing WP-P0-21 checks"), `:638` (WP-P0-21 is a declared
dependency), WP-P0-21 block plan `:515-525`.

WP-P0-21 delivers an **executable check suite** for *deterministic replay, lookahead, repaint,
data quality, the basic-failure floor, and unsimulated controls*, each emitting a
machine-readable verdict record `{check id, threshold, measured value, PASS/FAIL/BLOCKED,
dataset hash, deployment_identity_hash, timestamp}` with a D026 fixture per check; **an unset
threshold yields `BLOCKED`, never `PASS`** (plan `:518`, `:522`, `:525`).

### 4.1 Which WP-P0-21 checks VEN-E consumes

| WP-P0-21 check (plan `:518`) | VEN-E use | Applied where |
|---|---|---|
| **data quality** | primary reuse — run on each single-producer interval projection before archive merge; archive-level identity/version checks run separately | write path (§1.4.2) + pre-merge backfill/proxy ingestion (§1.5.1, §3.2), through the producer-local projection and gate in §4.2 |
| **deterministic replay** | the derived "current best" view (§2.5) must replay identically from the append-only archive | archive rebuild test |
| **lookahead** | forming bar must never reach a consumer or a verdict (§1.4.1); a check that the feed cannot serve a bar whose `bar_close_time > now` | feed read path |
| **repaint** | a stored closed bar's canonical value must not change; corrections are new rows, and the derived view's choice is deterministic (§1.4.5, §2.5) | archive invariant |
| **basic-failure floor** | not VEN-E's to run (it is a strategy-evidence floor); VEN-E only guarantees the data it serves is labelled and quality-checked | n/a — consumer side |
| **unsimulated controls** | n/a to the feed itself | n/a |

### 4.2 Local write-path quality checks (`io.py:validate_dataset`, `io.py:108-175`, through an explicit projection)

VEN-E does not pass mixed archive rows directly to `io.py:validate_dataset`. Before archive merge,
it groups incoming observations by
`(venue, track, source_producer, symbol, interval)`, requires one candidate observation per
`bar_open_time` in that group, and projects exactly
`timestamp = UTC(bar_open_time), open, high, low, close, volume`. The projection is ordered by
`timestamp`; before ordering, an explicit unconditional check refuses duplicate `bar_open_time`
members within the group. The projected single-producer interval series is then passed to
`validate_dataset`. P1, P2, and P3 each traverse this contract independently. Cross-producer rows
for one slot never share a validator projection and therefore do not create a false zero-spacing
failure.

The repository validator implements:

- required OHLCV columns present (`io.py:122-124`)
- non-empty (`io.py:130-132`)
- no NaN in `open/high/low/close`; NaN `volume` is a warning (`io.py:135-141`)
- timestamps strictly monotonic increasing; its duplicate diagnostic runs only when the series is
  already non-monotonic (`io.py:143-150`), so VEN-E's unconditional pre-order duplicate check above
  is the build-time duplicate gate
- existing gap heuristic `time_diff > mode * 1.5` (`io.py:152-158`) — implementation fact only;
  VEN-E does **not** adopt `1.5` as an acceptance boundary, because the interval-exact rule below
  governs its archive
- OHLC consistency: reject `high < low`, `high < open`, `high < close`, `low > open`,
  `low > close` (`io.py:161-170`)

VEN-E adds, on top (PROVISIONAL, thresholds [OPEN]):

- **interval-exact spacing:** within each single-producer projection, consecutive
  `bar_open_time` differ by exactly *T* (stricter than the `mode * 1.5` heuristic); any deviation
  → gap record + P2 backfill enqueue (§1.3.5). It is never evaluated across P1/P2/P3 rows.
- **retention-edge watch:** if the oldest `NATIVE` bar for *T* is within **[OPEN-N11]** of the
  venue retention limit and no fresh backfill has landed, raise `DEGRADED` and page via
  WP-P0-26 (falling behind the retention window is a permanent hole — plan `:635`).
  **v1.9 decision-108 qualification:** for 15m only, warn when only 40 days of venue history
  remain. The other timeframes remain `OWNER-DEFERRED-TO-MEASUREMENT`; their retention-edge
  predicate stays `BLOCKED`. This decision supplies no measured proof and does not alter the
  separate no-fresh-backfill input in the retained rule above.
- **price/volume domain:** minimum admissible bounds are **[OPEN-N17]**; this check is `BLOCKED`
  until ratified. Reuse of an existing validator does not ratify a numeric boundary.
- **duplicate/version policy:** observations across `source_producer` are expected and retained.
  Within one producer/slot, a byte-identical replay with the same stable `observation_id` is an
  accepted idempotent no-op with a recorded `IDENTICAL_REPLAY_NOOP` disposition. Reusing that ID
  with different bytes, a second unlinked `INITIAL`, or an unlinked differing repeat is a defect →
  FAIL. A differing repeat is legal only as a `CORRECTION` with a new ID and a valid
  `supersedes_observation_id` chain (§1.4.5, §2.2).

After all producer-local projections pass, the archive boundary applies the observation-identity,
same-ID/same-bytes, correction-chain, and terminal-disposition rules in §1.4.5/§2.2. Those
archive-level rules are not delegated to the single-series validator.

### 4.3 Verdict record binding

Every VEN-E quality result is emitted in the WP-P0-21 verdict-record shape (plan `:518`) with
`dataset_hash` equal to a content hash of the exact logical dataset/archive slice whose quality was
measured, and `deployment_identity_hash` set from the collector build. The frozen, versioned
canonical-byte contract orders rows by stable observation identity after the declared
`(venue, track, source_producer, symbol, interval, bar_open_time)` keys, uses a fixed field order and
type-tagged encodings, and records its `content_hash_algorithm` and `canonicalization_version`.
Unknown versions, duplicate stable identities, or a different byte stream under the same claimed
hash are refused. The §3.3 provenance-manifest hash remains the separate
`venue_provenance_manifest_hash`; the manifest contains and verifies `dataset_content_hash`, but its
own hash is never relabelled `dataset_hash`. The exact algorithm/version is frozen by the build
contract before evidence is accepted; this design invents no owner-gated value. An unset threshold
→ `BLOCKED` (plan `:522`); VEN-E **invents no threshold to make a check pass** (plan `:525`, C-4).

### 4.4 Standing backtest-vs-forward divergence

WP-P0-21 also computes a standing backtest-versus-forward divergence check per
`deployment_identity_hash`, tolerance **[OPEN-N13]**, emitting evidence for WP-V3-03 to enforce
(plan `:519`, `:1004`). VEN-E's role: supply the forward (native) series and its provenance so
that check can run; VEN-E does not compute or enforce it. The "measures and reports; does not
promote, demote or authorize" boundary belongs to WP-P0-21 (plan `:519`); VEN-E's own boundary is
warn/block under frozen policy and never resize (plan `:636`).

---

## 5. D026 forced-disconnect / gap-backfill fixture design (two native producers)

Authority: acceptance gate plan `:641` — "the collector survives a forced disconnect with a
proven gap-backfill (**D026 RED/GREEN on a deliberately dropped window**)". D026 =
`AGENTS.md:46-47`: the regression test must show **RED on the exact pre-fix behaviour or an
equivalent mutation, then GREEN with the fix, with real commands/output recorded.**

### 5.1 Test doubles (no venue contact — C-6)

- **WS event source** (`tests/fixtures/ven_e/ws_events.json`) is independently authored for
  `FakeWsFeed`. It contains the emitted message stream and supports commanded `drop(window)`,
  `close_socket()`, and `reopen()` actions.
- **Snapshot response source** (`tests/fixtures/ven_e/snapshot_pages.json`) is independently
  authored for `FakeSnapshotEndpoint`. It contains cursor pages (`since`, `limit`, empty-response
  stop, no-progress stop) and the full dropped window still held by the modeled venue.
- **Verifier-owned oracle** (`tests/fixtures/ven_e/expected_closed_window.json` plus a pinned hash)
  is authored and frozen independently before the two adapters run. It contains the expected
  closed-bar identities/OHLCV and terminal gap/reconciliation events. Neither fake may import,
  generate, rewrite, or derive this file; the verifier may import neither fake nor collector code.

The three sources share no data file or generator. A build-time dependency check enforces the
forbidden imports/generation edges, and the evidence record pins all three file hashes. This is the
source-correctness oracle; replay of the archive against itself proves determinism only.

### 5.2 The two native producers under test

P1 (live subscriber) consumes only the WS event source through `FakeWsFeed`; P2 (cursor backfill)
consumes only the snapshot response source through `FakeSnapshotEndpoint`. The verifier compares
the resulting archive/evidence only to its separately pinned expected-window oracle. The archive
and reconnect/backfill logic (§1.3–§1.6) are the code under test.

| Assertion | Actual operand producer/source | Expected operand producer/source |
|---|---|---|
| complete closed-bar set and OHLCV | collector archive from P1/P2 fixture adapters | verifier / `expected_closed_window.json` |
| exact `W` gap, reconnect, and terminal reconciliation events | collector evidence sidecar | verifier / expected event rows in `expected_closed_window.json` |
| reconnect-trigger enqueue | collector scheduler/event output, including trigger cause and ordering | verifier / scripted reconnect timeline and expected `cause=RECONNECT` enqueue before the next P1 closed-bar delivery |
| P2 repair provenance | immutable P2 observations + status events | verifier / expected observation IDs and producers |
| forming-bar exclusion | archive from WS events containing a marked forming bar | verifier / expected closed-bar identity set |
| emitted freshness sequence | collector freshness/event output | verifier / expected seven-state sequence; connection-state assertion is separate |
| deterministic replay | first derived view from immutable archive/events | independently rebuilt view from the same pinned bytes (determinism only) |

### 5.3 RED case (mechanism absent / mutated)

The build runs M1 and M2 as separate discriminating checks because they cover independent enqueue
routes; if one is also the exact pre-fix behaviour, that run is labelled the regression closure per
D026. M3 is the separate forming-bar check:

- **M1 — no reconnect-trigger enqueue:** disable only the §1.3.4 "trigger a P2 gap-backfill on
  reconnect" step. This modified copy measures the reconnect-trigger contract; it does not claim
  the archive must remain unfilled because §1.3.5 may later enqueue the same span. Or
- **M2 — no gap detection:** disable §1.3.5 sequence/gap detection so a silent hole is never
  noticed. Or
- **M3 — forming-bar written:** disable §1.4.1 so the collector persists an unclosed bar.

Procedure for M1 (forced reconnect, trigger-specific):

1. Run the collector against both fakes for `N` bars — archive matches the separately pinned
   verifier oracle. Record.
2. Command `FakeWsFeed.drop(window W)` spanning `k` closed bars (`k` chosen so `W` is a
   *deliberately dropped window*), then resume.
3. On re-subscription, the verifier requires exactly one P2 enqueue covering `W`, carrying
   `cause=RECONNECT`, before the next P1 closed-bar delivery. The expected side comes from the
   independently scripted reconnect timeline, not collector output.
4. The M1 modified copy lacks that enqueue and the same trigger-specific invariant refuses it →
   RED. Continue the fixture afterward only to demonstrate that a later §1.3.5 enqueue may still
   fill `W`; any eventual completeness is explicitly **not** evidence that M1 passed.
5. Capture the exact executable command and real failing output.

Procedure for M2 (silent sequence gap, no reconnect route):

1. Keep the socket open and have `FakeWsFeed` omit `W`, then deliver the first later closed bar; no
   reconnect/re-subscribe event occurs in this fixture.
2. Run the same final archive/evidence positive invariant used by GREEN: the closed-bar
   identity/OHLCV set equals the verifier oracle, every bar in `W` is present, the `GAP` event names
   `W`, and terminal P2 provenance/reconciliation evidence exists.
3. With §1.3.5 disabled, no route enqueues `W`; the invariant refuses the modified copy → RED.
   Restore §1.3.5 and the identical input reaches GREEN through P2.
4. Capture the exact executable command and real RED/GREEN output. The missing gap and terminal
   evidence are assertions, not merely diagnostics.

### 5.4 GREEN case (mechanism present)

1. Restore §1.3.4 + §1.3.5 (+ §1.4.1).
2. Repeat the identical drop procedure.
3. **Assertions (expected to PASS → GREEN):**
   - a `GAP` evidence record exists for exactly `W` (§2.3);
   - a `RECONNECT` record exists;
   - P2 backfill ran for `W`; the `k` immutable observations are present with
     `source_producer = CANDLE_SNAPSHOT`, and sidecar events derive state `BACKFILLED` or
     `RECONCILED`;
   - final closed-bar identities/OHLCV equal the verifier-owned oracle byte-for-byte for the pinned
     numeric representation;
   - emitted freshness followed only an allowed sequence such as
     `FRESH → STALE|UNKNOWN → RECOVERING → FRESH`, returning to `FRESH` only after backfill and
     reconciliation; internal `connection_state = RECONNECTING` occurred and was never emitted;
   - the forming bar was never persisted (M3 guard);
   - deterministic replay: rebuilding the derived view from the append-only archive reproduces
     the identical series.
4. Capture real command + output.
5. **Oracle-independence probe:** make a modified copy that shifts one snapshot timestamp or OHLCV
   value while leaving the WS source and verifier oracle untouched. Drive the real P2/collector
   path; the positive invariant must refuse the modified copy. Repeat with only the oracle changed
   to prove neither adapter can rewrite it.

### 5.5 Second native producer explicitly exercised

The fixture is designed so the **only producer that can supply the missing candle observations** is
P2 (`FakeSnapshotEndpoint`) — `FakeWsFeed` never re-sends the dropped bars after resume. Either the
§1.3.4 reconnect trigger or §1.3.5 gap detector may enqueue P2 in the unmodified integration path;
their discriminating proofs are separated in §5.3. This forces the integration test to prove the
two-native-producer design: P1 exposes the outage boundary, P2 supplies `W`, and reconciliation
closes it. A P1-only collector cannot pass §5.4.

### 5.6 Extra D026 fixtures (same shape, one mutation each)

Per WP-P0-21's "a D026 fixture per check" (plan `:518`) and the freshness acceptance addition
(plan `:642`), each of these gets its own RED/GREEN:

- forming-bar exclusion (M3 above, standalone);
- interval-exact spacing check (§4.2);
- three separate archive-disposition modified copies: byte-identical P2 replay with the stable ID →
  accepted no-op plus `IDENTICAL_REPLAY_NOOP`; differing repeat with a new linked correction ID →
  accepted new immutable row; same ID with different bytes → refused (§1.4.5, §2.2, §4.2);
- correction-chain refusal arms, each a modified copy the common positive invariant refuses: a
  correction whose `supersedes_observation_id` targets a missing observation; a correction cycle;
  a cross-slot link (target in a different producer/symbol/interval/slot); two corrections claiming
  the same successor position; a second unlinked `INITIAL` for an existing slot; an unlinked
  differing repeat without a valid `CORRECTION` link (§1.4.5, §2.2, §4.2);
- P1/P2 divergence → both retained + `FEED_DIVERGENCE` record + slot served `UNKNOWN` (§1.6);
- reconciliation status mutation: any attempt to update an immutable candle row is refused; replay
  derives the status solely from sidecar events;
- producer/provenance coverage: P1/`WS_LIVE`, P2/`CANDLE_SNAPSHOT`, and P3/`PROXY_DOWNLOAD` each
  traverse the §4.2 producer-local projection and stamp path. P3 writes into the same archive with
  `track=PROXY`, labelled proxy venue/source, and cannot replace an interior native hole;
- venue-provenance omissions: independently remove or corrupt the stamp in verifier-owned research-
  artifact, eligibility/admission-verdict, and promotion-verdict carrier fixtures; the verifier-
  owned accepting consumer refuses each. The same contract moves to each real downstream gate;
- freshness transitions and no-resize use the discriminating matrix below; an attempted emitted
  `RECONNECTING` or any other eighth value is separately refused.

| Check | Exact fixture input | Actual producer/source | Independent expected producer/source | Modified copy refused by the common positive invariant |
|---|---|---|---|---|
| `AGING` | a reconciled closed stream whose age reaches its injected ratified `[OPEN-F1]` boundary but not `[OPEN-F2]` | VEN-E state machine + transition sidecar | verifier-owned transition table + synthetic clock | suppress the FRESH→AGING transition |
| `STALE` | the same stream advanced beyond injected ratified `[OPEN-F2]` | VEN-E state machine + sidecar | verifier table + synthetic clock | keep emitting `AGING` beyond F2 |
| `UNKNOWN` | collector start, and separately a post-disconnect stream before its first reconciled snapshot | VEN-E state machine + sidecar | verifier timeline oracle | emit `FRESH` before reconciliation |
| `DRIFT` | independently authored P1/P2 rows beyond injected ratified `[OPEN-N8]` for exactly injected ratified `[OPEN-N19]` consecutive reconciliations | reconciliation + VEN-E state machine | verifier row fixtures + transition table | omit the terminal UNKNOWN→DRIFT transition; this check stays `BLOCKED` while either boundary is unset |
| `DEGRADED` (reconnect fallback) | exactly injected ratified `[OPEN-N4]` consecutive reconnect failures followed by confirmed P2 polling at injected ratified `[OPEN-N18]` cadence | reconnect/poll scheduler + state machine | verifier reconnect/poll timeline | suppress DEGRADED after both conditions hold; stays `BLOCKED` while either boundary is unset |
| `DEGRADED` (retention risk) | oldest native bar crosses injected ratified `[OPEN-N11]` with no fresh backfill | retention watcher + state machine | verifier archive-age fixture + transition table | suppress DEGRADED when the independent retention trigger holds; stays `BLOCKED` while N11 is unset |
| `RECOVERING` | reconnect succeeds while P2 gap-backfill/reconciliation remains incomplete | reconnect/reconciliation state machine | verifier reconnect timeline + expected event rows | emit `FRESH` before terminal reconciliation |
| no-resize | every transition fixture also carries sentinel quantity/position/order fields through the reachable consumer test boundary | complete VEN-E entry-point/route graph + before/after records | verifier-owned byte comparison of the sentinel fields | add one reachable transition-handler write that changes a sentinel quantity/size/order field; the same graph-and-byte invariant must refuse it |

**v1.9 fixture-boundary qualification:** the retained `[OPEN-F1]` and `[OPEN-F2]` references in the
matrix now resolve to bar interval plus 15 seconds and bar interval plus 45 seconds, respectively;
the verifier records both as a **judgement based on illustrative values, not measured proof**.
The `[OPEN-N11]` reference resolves only for 15m, to the owner wording "when only 40 days of venue
history remain". The N11 rows for 1h, 4h and 1d remain `BLOCKED` and
`OWNER-DEFERRED-TO-MEASUREMENT`. No per-interval F1/F2 override is supplied because `OPEN-F3`
remains open.

The verifier injects only owner-ratified boundaries. Until a referenced boundary is ratified, that
row emits `BLOCKED`; relative prose such as "reaches F1" is not a substitute numeric default. For
every row the positive invariant requires the exact expected transition/event sequence and unchanged
sentinel economic fields. Each modified copy is run through the same top-level fixture and must be
refused; a state label or static absence scan alone is supplemental.

Every extra fixture records the actual and expected producer/source operands using the §5.2 table
shape. No self-comparison or unpaired assertion counts as closure evidence.

---

## 6. Freshness-state emission map

Authority: plan `:636` (map #79 fold — "market-feed health emits the common WP-P0-04 freshness
states and evidence… This package may warn or block according to the frozen policy; it never
resizes an order"); plan `:642` (deliberate transitions produce shared machine-readable states;
no state silently changes position size; numeric boundaries **[OPEN]**); WP-P0-04 defines the
"shared seven-state freshness vocabulary" as **shapes only, enforces none** (plan `:331`); brief
seven-state table `:2317-2325`, rejections `:2329-2330`, carrier assignment `:2332`
("WP-P0-30 emits market-feed freshness… Numerical boundaries remain `[OPEN]`; no state may
silently resize").

### 6.1 State → VEN-E trigger → emitted behaviour

| State (brief `:2317-2325`) | VEN-E market-feed trigger (PROVISIONAL; thresholds [OPEN]) | Behaviour VEN-E emits (VEN-E never resizes) |
|---|---|---|
| `FRESH` | last closed bar age `< interval + [OPEN-F1]` (brief default 15s) | normal; feed serves closed bars |
| `AGING` | age in `[interval + [OPEN-F1], interval + [OPEN-F2]]` (brief default 15–45s) | **warning badge only — no economic change** (brief `:2320`, `:2329`) |
| `STALE` | age `> interval + [OPEN-F2]` (brief default 45s) | emit `STALE`; consumer policy = hard block on new entries, resting native stops untouched (brief `:2321`). VEN-E only *reports*; the block is the consumer's frozen policy |
| `UNKNOWN` | collector start, or post-disconnect before first snapshot reconciled | emit `UNKNOWN`; consumer hard-block (brief `:2322`) |
| `DRIFT` | mismatch beyond [OPEN-N8] persists for [OPEN-N19] consecutive daily reconciliations; while either value is unset, transition is `BLOCKED` and the slot remains `UNKNOWN` with divergence evidence | emit `DRIFT` + evidence record; signal for halt/disarm/PAGE is the consumer's (brief `:2323`); VEN-E pages via WP-P0-26 channel |
| `DEGRADED` | either (a) P1 has reached [OPEN-N4] consecutive reconnect failures **and** P2 bounded `candleSnapshot` polling is confirmed active at [OPEN-N18] cadence (§1.3.3), or (b) the retention-edge watcher crosses [OPEN-N11] with no fresh backfill (§4.2) | emit `DEGRADED` with every active reason. For reason (a), **per-worker policy declared in the frozen package** decides whether that worker may trade on polled data — not a global constant (brief `:2324`, `:2330`). Reason (b) reports retention risk and pages through WP-P0-26; it does not claim polling is active |
| `RECOVERING` | reconnected, P2 gap-backfill + reconciliation in progress (§1.3.4) | emit `RECOVERING`; consumer inhibits new orders until reconciliation completes (brief `:2325`) |

**v1.9 owner-decision qualification:** `FRESH → AGING` is bar interval plus 15 seconds and
`AGING → STALE` is bar interval plus 45 seconds (decision 104), marked exactly as a **judgement
based on illustrative values, not measured proof**. `OPEN-F3` remains open, so this draft adds no
per-interval override. `OPEN-F4` remains `OWNER-DEFERRED-TO-MEASUREMENT`. For `DEGRADED` reason
(a), a missing strategy instruction defaults to stop (decision 105); an explicit frozen strategy
instruction remains authoritative. For reason (b), the 15m warning is when only 40 days of venue
history remain; 1h, 4h and 1d remain `OWNER-DEFERRED-TO-MEASUREMENT` (decision 108).

### 6.2 Emission mechanism

- One `freshness_state` per `(symbol, interval)` stream, published on the feed alongside the
  data, plus a `FRESHNESS_TRANSITION` evidence record (§2.3) on every change.
- The state machine is VEN-E-local but uses the **WP-P0-04 shape** (plan `:331`) so all
  authoritative domains share one vocabulary; account freshness stays with WP-V2A-04,
  portfolio/order/fill aggregation with WP-V2B-03 (plan `:636`).
- **Hard invariant, tested (§5.6):** no VEN-E code path multiplies, scales, or reduces a
  quantity, position size, or order parameter. VEN-E's only outputs are data + state + evidence
  (plan `:636`, `:644`).
- **DEGRADED precedence and disagreement rule:** the evaluator records the truth value and
  `PASS`/`BLOCKED` status of both independent entry predicates. Retention risk alone is sufficient
  when [OPEN-N11] is ratified and crossed. Reconnect failure is sufficient only when [OPEN-N4] is
  ratified and reached **and** P2 polling is actually active under ratified [OPEN-N18]; reaching the
  reconnect cap without confirmed fallback polling emits `UNKNOWN` plus failure evidence, not a
  false claim that polled data is active. If both predicates hold, emit one `DEGRADED` transition
  with both reasons. An unset boundary blocks only its predicate and cannot suppress the other
  independently proven predicate; if neither predicate is evaluable/true, `DEGRADED` is not emitted.

**v1.9 N11 precedence qualification:** the retained "unset boundary" branch now applies to 1h, 4h
and 1d. The 15m N11 limb is ratified at "when only 40 days of venue history remain" and can be
evaluated with the retained no-fresh-backfill input. This does not make any other timeframe
evaluable and does not change the independent reconnect-fallback predicate.

### 6.3 Boundaries left open

The v1.8 inventory sentence below is retained for traceability. Active v1.9 status follows it.

`[OPEN-F1]` FRESH→AGING age; `[OPEN-F2]` AGING→STALE age; `[OPEN-F3]` per-interval overrides of
both; DRIFT tolerance `[OPEN-N8]`; reconnect-failure count for DEGRADED/fallback `[OPEN-N4]`;
retention-edge DEGRADED boundary `[OPEN-N11]`; DEGRADED per-worker policy field default
`[OPEN-P030-1]`;
`[OPEN-F4]` RECOVERING max duration before escalation; P2 DEGRADED-poll cadence `[OPEN-N18]`;
DRIFT persistence count `[OPEN-N19]`.
All blocked pending owner ratification (plan `:642`, brief `:2332`).

**Active v1.9 status:** `OPEN-F1` and `OPEN-F2` are closed by decision 104 at interval plus 15
seconds and interval plus 45 seconds. `OPEN-P030-1` is closed by decision 105 with default stop.
`OPEN-F3` remains open because no override answer was named. `OPEN-F4` remains
`OWNER-DEFERRED-TO-MEASUREMENT`. `OPEN-N11` is closed only for 15m at the owner wording "when only
40 days of venue history remain"; its 1h, 4h and 1d limbs remain
`OWNER-DEFERRED-TO-MEASUREMENT`. Every other retained tag in the sentence above remains open.

---

## 7. Acceptance mapping

Maps each authority acceptance clause to the design element that satisfies it and the evidence
that will prove it. **Nothing here is executed — this is the plan for the build's acceptance.**

| # | Acceptance clause (authority) | Design element | Evidence at build time |
|---|---|---|---|
| A1 | Collector survives a forced disconnect with proven gap-backfill; **D026 RED/GREEN on a deliberately dropped window** (plan `:641`, first semicolon-delimited acceptance clause) | §1.3 reconnect + §1.5 P2 backfill + §1.6 reconciliation; two-native-producer design §1.1 | §5 fixture: M1 RED/GREEN for the reconnect-trigger measurement, M2 RED/GREEN for the independent silent-gap detector, GREEN integration for completed P2 backfill, with real command/output (`AGENTS.md:46-47`) |
| A2 | Archive rows carry venue provenance (plan `:641`, second semicolon-delimited acceptance clause) | `venue`, `track`, `proxy_source`, `source_producer` on every row (§2.2); provenance manifest §3.3 | schema test: no row writable without `venue`+`track`; manifest emitted on every export |
| A3 | Feed bar-close semantics match the #45 time-discipline rows (plan `:641`, third semicolon-delimited acceptance clause) | §1.4 closed-bars-only, explicit `bar_open_time`/`bar_close_time`, forming bar never persisted | fixture §5.6 forming-bar-exclusion RED/GREEN; cross-check against WP-P0-09 #45 rows (owner-gated read — [OPEN-N5]) |
| A4 | Accepted **before WP-V2A-08 starts** — hard edge; A08 consumes a proven feed (plan `:641`, fourth semicolon-delimited acceptance clause; `WAYFINDER_DECISION_FOLD_2026-08-23.md:38`) | feed infra §1–§2 delivered and accepted as a unit | sequencing note — this lane records the edge; it does not start A08 |
| A5 | Belongs among the earliest G1-IA candidates given retention loss (plan `:641`, fifth semicolon-delimited acceptance clause; plan `:632`) | collector §1 is the first buildable slice | priority note; build still needs `G1-IA` (D-12) |
| A6 | Freshness acceptance: deliberate `AGING/STALE/UNKNOWN/DRIFT/DEGRADED/RECOVERING` transitions produce shared machine-readable states; **no state silently changes position size**; numeric boundaries owner-gated `[OPEN]` (plan `:642`) | §6 emission map + §6.2 mechanism + §6.2 hard invariant; internal `RECONNECTING` is not emitted | §5.6 fixture matrix: exact input/actual/expected producer plus one refused modified copy per transition, both DEGRADED triggers, an eighth-state refusal, and a reachable size-write modified copy; boundary-dependent rows remain `BLOCKED` until ratified |
| A7 | Quality gates reuse WP-P0-21 checks (plan `:635`) | §4 reuse map; `io.py:validate_dataset` reuse; verdict-record shape §4.3 | check suite runs on every write batch; verdict records emitted; unset threshold → `BLOCKED` (plan `:522`) |
| A8 | Watched by the WP-P0-26 dead-man watchdog (plan `:635`) | §6 (§1.6 daily reconciliation is the liveness signal) + heartbeat emission | watchdog fixture: kill the collector heartbeat → push lands on owner phone (plan `:585`) — WP-P0-26's gate, consumed here |
| A9 | Archive under WP-P0-26 second-location backup (plan `:635`) | §2.1 — archive registered as a protected backup class | restore drill RED/GREEN is WP-P0-26's (plan `:585`); VEN-E supplies the store inventory entry |
| A10 | Dual-track rule: native where window suffices, labelled proxy beyond (plan `:635`) | §3.1 track-selection; §3.2 proxy via existing ccxt downloader; straddling window → two labelled segments; interior native hole → explicit `UNKNOWN`, never proxy substitution | tests: boundary-straddling request returns two labelled segments; interior hole returns explicit availability/evidence and never a blend (plan `:637`) |
| A11 | Every research artifact and every promotion/eligibility verdict states which venue's data produced it — no silent proxy evidence (plan `:635`) | §3.3 `VenueProvenanceStamp`, separate dataset/provenance hashes, registry contract; downstream mappings are PROVISIONAL and belong to downstream gates | VEN-E proves its producer contract with verifier-owned accepting-consumer fixtures that refuse missing/corrupt research and verdict carriers. Each real consumer proves its own carrier/refusal at its package gate; no dependent package must exist for VEN-E acceptance |
| A12 | One-time divergence study; audit tier T2 (plan `:635`, `:640`) | §3.4 — triggered at [OPEN-N10] overlap; measured deltas; T2 written study | study document with measured numbers, or "insufficient overlap" — no invented number (C-4) |
| A13 | Sole market-data authority for the execution chart; no second collector / no silent blend; provenance visible; absence reported honestly (plan `:637`, `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md:19,31,42`) | §2.5 derived-view response contract; §3.1 segment/hole rules; five availability classes; §3.3 producer/enforcer registry contract | VEN-E acceptance proves those existing registry/response contracts with verifier-owned chart-consumer fixtures: exactly one VEN-E authority, provenance + availability on every datum, and modified copies adding a second authority path or removing VEN-E are refused. A separate modified copy that returns an interpolated or reconstructed value for a missing or unavailable native slot is refused by the same response invariant. WP-V2B-05 later proves the same invariant over its real built chart caller at its own gate; the dependent chart is not a VEN-E prerequisite |
| A14 | Host-install steps T0 / gate `G9` (+ `G1-IA`), per-session owner auth, nothing authorized (plan `:640`) | all §1 deployment steps flagged host-contact; this document performs none | design records the gate; build stops for owner per session |
| A15 | Authority boundary: unauthenticated public reads only; zero orders; zero credentials (plan `:644`) | §1.2 no-auth WS + public `candleSnapshot`; §6.2 no-resize invariant | finite reachability proof rooted at every VEN-E executable entry point. Derive the complete import/call/route inventory from those roots, including every resolved import, call, and configured dispatch edge; unknown or opaque edges are refused. The same top-level check separately refuses modified copies that make a signer, a credential read, and an order call reachable |
| A16 | Rollback: stop the collector; archive append-only and retained (plan `:643`) | §2.1/§2.2 append-only; §2.5 derived view rebuildable | test: stop collector → archive intact; destroy derived view → rebuild with no loss |

**v1.9 A6 qualification:** the authority wording in A6 is retained, but F1 and F2 are now ratified
by decision 104 and the missing DEGRADED-policy default is ratified by decision 105. The 15m N11
limb is ratified by decision 108. A transition row stays `BLOCKED` only for a boundary it still
requires that remains open; §5.6 and §6 carry the per-row status.

---

## 8. [OPEN] owner-gated items (every unsettled numeric boundary is here)

All are blockers, not defaults (plan `:642`, `:518`/`:522`, brief `:2332`; C-4). "PROVISIONAL"
design choices depending on WP-P0-26/WP-P0-21 build or on owner-gated venue-doc facts are listed
after the numerics.

**v1.9 reading rule:** the v1.8 tables are retained as the before-state. Their active dispositions
are in §8.1.1 and §8.2.1. Closed rows are not blockers; partial rows retain only the expressly named
engineering or measurement limb.

### 8.1 Numeric boundaries — all `[OPEN]`, all blocking

**RETAINED-HISTORICAL v1.8 table label:** the active v1.9 count and dispositions follow the table
in §8.1.1.

| Tag | Boundary | Governs | Notes |
|---|---|---|---|
| OPEN-F1 | FRESH → AGING bar-age offset | §6 freshness | brief illustrative default 15s (`:2319-2320`) — not ratified |
| OPEN-F2 | AGING → STALE bar-age offset | §6 freshness | brief illustrative default 45s (`:2321`) — not ratified |
| OPEN-F3 | per-interval overrides of F1/F2 (15m vs 1d differ) | §6 | — |
| OPEN-F4 | RECOVERING max duration before escalation | §6 | — |
| OPEN-N2 | active WS connection count and connection/subscription topology | §1.2 | source-fixed 10-connection / 1000-subscription maxima bound but do not select the count (`ADDENDUM:76`) |
| OPEN-N3 | reconnect backoff base + ceiling + jitter | §1.3 | shape reused from `download.py:208`; constants open |
| OPEN-N4 | consecutive-reconnect-fail count → DEGRADED / REST fallback | §1.3.3 | — |
| OPEN-N5 | canonical bar timestamp convention (key on open vs close) | §1.4.3, §2.2 | must match WP-P0-09 #45 rows — owner-gated, this lane may not settle it |
| OPEN-N6 | host/venue clock-skew alarm threshold | §1.4.4 | feeds WP-P0-26 NTP/drift alarm (`plan:580`) |
| OPEN-N7 | P2 batch size + inter-request pacing | §1.5 | 1200/min is the source-fixed total IP maximum shared on KVM2, not a reserved VEN-E share (`ADDENDUM:73-85`); blocked pending a named coordination or measured-headroom rule |
| OPEN-N8 | P1/P2 OHLCV reconciliation / DRIFT tolerance | §1.6, §6 | informed (not set) by §3.4 study |
| OPEN-N9 | archive partition granularity (month/year/rolling) | §2.1 | storage-cost tradeoff |
| OPEN-N10 | "enough native history" to trigger the divergence study | §3.4 | plan `:635` leaves it qualitative |
| OPEN-N11 | retention-edge proximity that raises DEGRADED | §4.2 | permanent-hole risk margin |
| OPEN-N12 | data-quality check thresholds inherited from WP-P0-21 that are still unset | §4 | each yields `BLOCKED` until set (plan `:522`) |
| OPEN-N13 | backtest-vs-forward divergence tolerance | §4.4 | WP-P0-21-owned; VEN-E supplies the series only |
| OPEN-N14 | detect-to-delivery time bound for the watchdog on this collector | §6 A8 | WP-P0-26-owned and itself `[OPEN]` (plan `:578`, `:580`, `:585`) |
| OPEN-N15 | symbol universe for the collector (which markets, how many) | §1.2 | interacts with rate-limit budget; universe policy is VEN-A scope (`WAYFINDER_DECISION_FOLD_2026-08-23.md:25`) |
| OPEN-N17 | minimum admissible price and volume bounds | §4.2 | affected domain check is `BLOCKED`; no zero boundary is presumed |
| OPEN-N18 | P2 `candleSnapshot` polling cadence while DEGRADED | §1.3.3, §6 | bounded-recovery cadence; no default |
| OPEN-N19 | consecutive beyond-tolerance reconciliations required for DRIFT | §6 | until ratified, mismatch remains `UNKNOWN` with evidence and DRIFT transition is `BLOCKED` |

#### 8.1.1 v1.9 owner-addendum-31 decision records (active status)

The v1.8 table rows above are retained verbatim for zero-deletion traceability. A copied row struck
below is closed by the appended decision. A struck limb closes only that limb; the unstruck
engineering or measurement limb remains open with its owner stated.

**Decision 104 — one site for owner row 23**

~~| OPEN-F1 | FRESH → AGING bar-age offset | §6 freshness | brief illustrative default 15s (`:2319-2320`) — not ratified |~~

~~| OPEN-F2 | AGING → STALE bar-age offset | §6 freshness | brief illustrative default 45s (`:2321`) — not ratified |~~

**DECIDED - owner addendum 31 decision 104 (2026-09-02): Use "bar interval plus 15 seconds" for
aging and "bar interval plus 45 seconds" for stale data. Do not set a recovery limit yet. Mark
these as a judgement based on illustrative values, not measured proof.** Consequence: the F1 and
F2 blockers are closed with those exact offsets and that exact evidence marking. `OPEN-F3` remains
open because the decision does not name per-interval overrides. `OPEN-F4` remains open as
`OWNER-DEFERRED-TO-MEASUREMENT`; no recovery-limit value is minted.

> Owner verbatim: Use "bar interval plus 15 seconds" for aging and "bar interval plus 45 seconds" for stale data. Do not set a recovery limit yet. Mark these as a judgement based on illustrative values, not measured proof.

**Decision 106 — one site for the owner half of owner row 25**

~~Owner limb of the retained `OPEN-N7` row: "blocked pending a named coordination or
measured-headroom rule".~~

**DECIDED - owner addendum 31 decision 106 (2026-09-02): Create one shared rate-limit
coordinator. Until it exists, run the collector as one process only.** Consequence: the mechanism
choice is closed, following the decision-54 shape precedent. The `OPEN-N7` row itself remains open
as `OWNER-ANSWERED-SHAPE, VALUE PENDING`: P2 batch size, inter-request pacing, coordinator
implementation and measured safe headroom remain engineering work. Engineering owner: the
WP-P0-30 / VEN-E build lane. A source-fixed IP maximum is still not a reserved VEN-E share.

> Owner verbatim: Create one shared rate-limit coordinator. Until it exists, run the collector as one process only.

**Decision 107 — one site for owner row 26**

~~| OPEN-N9 | archive partition granularity (month/year/rolling) | §2.1 | storage-cost tradeoff |~~

**DECIDED - owner addendum 31 decision 107 (2026-09-02): Store market data by month.**
Consequence: `OPEN-N9` is closed and `calendar-partition` means calendar month; storage substrate,
index and backup implementation remain PROVISIONAL engineering work.

> Owner verbatim: Store market data by month.

**Decision 108 — one site for owner row 27's 15m limb**

~~15m limb of: | OPEN-N11 | retention-edge proximity that raises DEGRADED | §4.2 |
permanent-hole risk margin |~~

**DECIDED - owner addendum 31 decision 108 (2026-09-02): For 15-minute data, warn when only 40
days of venue history remain. Measure the other timeframes before setting their limits.**
Consequence: the 15m limb is closed at the owner's exact 40-day wording. The 1h, 4h and 1d limbs
remain open as `OWNER-DEFERRED-TO-MEASUREMENT`; no value or conversion is minted for them.

> Owner verbatim: For 15-minute data, warn when only 40 days of venue history remain. Measure the other timeframes before setting their limits.

**Decision 109 — one site for owner row 28**

~~| OPEN-N15 | symbol universe for the collector (which markets, how many) | §1.2 | interacts with rate-limit budget; universe policy is VEN-A scope (`WAYFINDER_DECISION_FOLD_2026-08-23.md:25`) |~~

**DECIDED - owner addendum 31 decision 109 (2026-09-02): Start only with Hyperliquid BTC
perpetual on 15m, 1h, 4h, and 1d intervals.** Consequence: `OPEN-N15` is closed with exactly one
market and the four named intervals. Connection count/topology remains engineering-owned
`OPEN-N2`; the decision does not select that value.

> Owner verbatim: Start only with Hyperliquid BTC perpetual on 15m, 1h, 4h, and 1d intervals.

**Current count:** 17 numeric tags remain open. The closed numeric rows are F1, F2, N9 and N15;
N7 remains open after its owner half closed, and N11 remains open for non-15m timeframes.

`OPEN-N1` and `OPEN-N16` are explicitly unused namespace positions in v1.8: no boundary in this
document is assigned either tag, and neither position implies an omitted default or owner decision.
Why earlier versions skipped those positions is NOT VERIFIED, so this draft does not invent a
historical explanation or renumber the stable tags above.

**v1.9 namespace label:** `OPEN-N1` and `OPEN-N16` remain explicitly unused; the retained v1.8
sentence above is historical only. No new numeric tag was created by the fold.

### 8.2 PROVISIONAL choices (depend on WP-P0-26 / WP-P0-21 / owner-gated venue facts)

| Tag | Open question | Status |
|---|---|---|
| OPEN-P030-1 | What default should a worker use when its frozen package does not declare the DEGRADED polled-data policy field? | BLOCKED pending owner ratification |
| OPEN-P030-2 | Which bytes compose `observation_id` and `producer_payload_hash`, in what order, and encoded how? | BLOCKED pending the frozen producer-observation identity contract |
| OPEN-P030-3 | Which bytes compose `event_id`, in what order, and encoded how? | BLOCKED pending the frozen immutable-sidecar-event identity contract |
| OPEN-P030-4 | Which bytes compose the provenance manifest, in what field order, and encoded how? | BLOCKED pending the frozen manifest-hash contract |

#### 8.2.1 v1.9 owner-addendum-31 decision record (active status)

The v1.8 row is retained verbatim above and copied here with its closed text struck.

~~| OPEN-P030-1 | What default should a worker use when its frozen package does not declare the DEGRADED polled-data policy field? | BLOCKED pending owner ratification |~~

**DECIDED - owner addendum 31 decision 105 (2026-09-02): If data falls back to slow polling and
the strategy gives no instruction, stop.** Consequence: `OPEN-P030-1` is closed. The missing-field
default is stop; a strategy's explicit frozen instruction remains authoritative. Three
PROVISIONAL-question tags remain open: `OPEN-P030-2`, `OPEN-P030-3` and `OPEN-P030-4`.

> Owner verbatim: If data falls back to slow polling and the strategy gives no instruction, stop.

- Storage substrate = Parquet + JSON index (reuse `io.py`/`cache.py`) — PROVISIONAL, pending
  archive size reality and WP-P0-26 backup mechanics.
  **v1.9 decision-107 qualification:** calendar-month partitioning is decided. The substrate,
  index and backup-mechanics portions of this bullet remain PROVISIONAL.
- WS connection count and multiplexing topology — PROVISIONAL and BLOCKED on OPEN-N2, pending venue
  WS protocol facts (owner-gated read) and final symbol universe (OPEN-N15).
  **v1.9 decision-109 qualification:** the final initial universe is Hyperliquid BTC perpetual on
  15m, 1h, 4h and 1d. `OPEN-N2` and the venue-protocol facts remain engineering-open; `OPEN-N15`
  does not.
- No-auth public reads for both producers — PROVISIONAL on the venue serving candle WS +
  `candleSnapshot` without signing. The design authority is plan `:644`; ADR-0021 `:47-52` does
  not establish endpoint authentication. Exact endpoint capability remains owner-gated and
  NOT VERIFIED.
- P2 bounded `candleSnapshot` polling under DEGRADED — a design-only branch added by the v1.1 fold
  as DS10-F2's disposition, not a claim that the two detector censuses agreed on whether venue/
  network content was added. It remains a PROVISIONAL recovery mechanism per ADR-0021 `:52`;
  cadence OPEN-N18 and failed-reconnect cap OPEN-N4 both block it until ratified.
- DEGRADED per-worker policy field default `[OPEN-P030-1]` — PROVISIONAL and BLOCKED. The field is declared per
  worker by the frozen package (§6.1; brief `:2324`, `:2330`), but this design selects no default;
  the owner must ratify one before a consumer can rely on default behaviour.
  **v1.9 decision-105 qualification:** the retained v1.8 blocker statement above is closed. If the
  strategy gives no instruction when data falls back to slow polling, the worker stops; an explicit
  frozen strategy instruction remains authoritative.
- Stable producer-observation identity/canonical-byte construction — PROVISIONAL; the build must
  freeze and hash the construction so identical replay is reproducible and same-ID/different-bytes
  is refused before archive acceptance.
  **BLOCKER [OPEN-P030-2].** Question: which bytes compose `observation_id` and
  `producer_payload_hash`, in what order, and encoded how, before the idempotency backbone can be
  built?
- Sidecar `event_id` byte-preimage construction — PROVISIONAL; before v1.7 this document gave
  `event_id` no construction, no freeze note and no deferral, while `observation_id` already carried
  the deferral above (v1.6 `:336` was its only occurrence; census `DS55_RUN.log:15`). v1.7 named the
  blocker (§2.3) but did not record that asymmetry; it is recorded here.
  **BLOCKER [OPEN-P030-3].** Question: which bytes compose `event_id`, in what order, and encoded
  how, before an immutable sidecar-event contract can be built?
- Reuse of `02_MTC_BACKTEST/src/data/download.py` for the proxy track and as the P2 cursor
  seed — PROVISIONAL on that module staying the canonical downloader (it is REUSE-FIRST per the
  lane spec and plan `:634`); **this lane does not modify it** (C-5).
- WP-P0-21 check IDs and record field names in §4 are taken from the plan description
  (`:518`); exact identifiers land when WP-P0-21 is built — PROVISIONAL.
- `VenueProvenanceStamp`, its separate dataset-content/provenance hashes, and the registry contract
  are PROVISIONAL. VEN-E acceptance proves verifier-owned consumer fixtures; adoption/refusal by
  each real downstream consumer is BLOCKED at that consumer package's own gate (§3.3), not here.
- Watchdog heartbeat protocol — PROVISIONAL on WP-P0-26's chosen technology (plan `:580`
  "technology chosen inside this package").

### 8.3 Missing input (see report §Discrepancies)

- `wayfinder_research/HYPERLIQUID_CANDLE_DATA_2026-08-23.md` (named in plan `:634` and the lane
  spec) is **not present** at current HEAD `108ea066a710ff7ef5c09246903fe3d523da1d56`
  (and v1 recorded it absent at `c18b6f3e`). Retention arithmetic in §0 therefore stays sourced
  from plan `:633` and `WAYFINDER_DECISION_FOLD_2026-08-23.md:21`; candle-shape detail remains
  PROVISIONAL / owner-gated.

---

## 9. v1.9 limits (what this draft deliberately does not settle)

1. **Owner-selected values are narrow, not blanket defaults.** Decisions 104-109 select F1/F2,
   the missing DEGRADED-policy default, the shared-coordinator shape, monthly partitions, the 15m
   retention warning and the initial universe only. `OPEN-F3` remains open; `OPEN-F4` and non-15m
   N11 remain `OWNER-DEFERRED-TO-MEASUREMENT`; N7 retains its engineering value/implementation limb.
2. **Evidence status is explicit.** The 15-second and 45-second offsets are a **judgement based on
   illustrative values, not measured proof**. The 15m 40-day wording is a judgement, not a measured
   limit for another timeframe.
3. **No venue-protocol detail is settled.** WS message shapes, `candleSnapshot` parameter names,
   endpoints, final flags and sequence availability remain PROVISIONAL; `OPEN-N2` remains open.
4. **No code or schema file is authorized.** This remains design-only. The build, host-contact and
   acceptance gates remain exactly as stated in §7.
5. **Bar-close convention remains open** (`OPEN-N5`) pending WP-P0-09; WP-P0-21 and WP-P0-26
   interfaces remain consumed dependencies rather than locally invented contracts.
6. **Storage implementation remains PROVISIONAL.** Decision 107 fixes monthly partitioning only;
   Parquet/index sizing, backup mechanics and measured storage behavior remain engineering work.
7. **The initial symbol universe is settled narrowly.** Decision 109 selects only Hyperliquid BTC
   perpetual on 15m, 1h, 4h and 1d; it does not settle connection topology, future expansion or
   venue-protocol facts.
8. **Nothing is authorized.** Owner addendum 31 supplies design decisions, not permission to build,
   contact a venue, run on a host, or bypass `G1-IA` / per-session `G9`.

<details>
<summary>RETAINED-HISTORICAL — superseded v1.8 limits</summary>

## 9. v1.8 limits (what this draft deliberately does not settle)

1. **No invented or owner-selected threshold.** Every unsettled numeric boundary is `[OPEN]`
   (§8.1); source-fixed limits and ratified cadences remain fixed and cited (plan `:642`, C-4).
2. **No venue-protocol detail.** WS message shapes, `candleSnapshot` parameter names, exact
   endpoints, is-final flags, sequence-number availability are all PROVISIONAL pending an
   owner-gated verification read that this lane is forbidden to perform (lane spec; C-6).
3. **No code, no schema files.** Field names in §2 are a design sketch, not a committed schema;
   the real schema is WP-P0-04-adjacent contract work and lands with the build.
4. **Bar-close convention not finalised** (OPEN-N5) — it must be reconciled against the WP-P0-09
   #45 time-discipline rows, which this lane treats as not-yet-readable-as-settled.
5. **WP-P0-21 interface assumed from prose.** If the built WP-P0-21 check suite differs from the
   plan `:518` description, §4 must be re-mapped.
6. **WP-P0-26 interface assumed from prose.** Backup class registration, heartbeat protocol and
   the detect-to-delivery bound are all WP-P0-26-owned and partly `[OPEN]` themselves.
7. **Divergence study is design-only here** — trigger, method and output format are sketched;
   the actual T2 study runs post-build once native history exists.
8. **Symbol universe undefined** (OPEN-N15) — the collector's scale, rate-limit headroom and
   storage footprint all depend on it; universe policy is VEN-A's, not this package's.
9. **No dashboard / chart UI** — VEN-E supplies the data + provenance + freshness + availability
   contract for the chart (§2.5); the chart itself is WP-V2B-05 (plan `:840`,
   `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md:31`).
10. **Nothing is authorized.** This is a design-ahead draft under owner addendum 9; build needs
     WP-P0-26 + WP-P0-21 accepted, `G1-IA`, and `G9` per session for any host step (plan `:640`).

</details>

## v1.4 change log — W148 fold

- **N101-F01 (HIGH) — FOLDED:** M1 now measures the reconnect-trigger enqueue before any later P1
  delivery; it no longer claims the archive must remain unfilled. M2 uses a separate no-reconnect
  silent-gap input so the shared completeness invariant discriminates the gap detector.
- **N101-F02 (MEDIUM) — FOLDED:** §6.1/§6.3 enumerate both DEGRADED entry predicates and all
  three numeric boundaries; §6.2 defines conjunction, independent-trigger, blocked-boundary, and
  simultaneous-reason precedence.
- **N101-F03 (HIGH) — FOLDED:** §4.2 defines `bar_open_time` → `timestamp`, single-producer
  grouping for P1/P2/P3, unconditional duplicate refusal, producer-local interval spacing, and
  separate archive-level identity/version checks. The duplicate claim is narrowed to repository
  behaviour.
- **N101-F04 (HIGH) — FOLDED:** §3.3/§4.3 separate the provenance-manifest hash from a canonical
  dataset-content hash; WP-P0-21 `dataset_hash` binds the exact measured logical slice.
- **N101-F05 (HIGH) — FOLDED:** VEN-E proves verifier-owned consumer contracts. Real research,
  admission, promotion, and chart consumers prove their carrier/route refusal at their own gates,
  removing the dependency cycle.
- **N101-F06 (MEDIUM) — FOLDED:** §5.6 now names each transition's input, actual producer,
  independent expected producer, and refused modified copy, plus a reachable size-write modified
  copy. Unratified numeric boundaries remain `BLOCKED`.
- **N101-F07 (MEDIUM) — FOLDED:** every architecture/fixture count now says two native producers
  plus one proxy producer where global, or explicitly two native producers where the disconnect
  fixture is scoped; P3 shares the physical archive and has producer/provenance coverage.
- **N101-F08 (MEDIUM) — FOLDED:** A15 is a finite proof rooted at every VEN-E executable entry
  point and a complete route/import inventory, with unknown edges refused and separate reachable
  signer, credential-read, and order-call modified copies.
- **Repeat/count sweep:** swept version labels, producer counts, validator-reuse labels,
  downstream-consumer acceptance wording, dataset/provenance hash labels, DEGRADED inventories,
  freshness/no-resize evidence, and authority-boundary proof wording. Historical v1.1–v1.3 change
  logs remain labelled with their original versions.

## v1.3 change log — DS20 fold

- **DS20-F01 (MEDIUM):** added the DEGRADED per-worker policy field default to §8.2 as a
  PROVISIONAL, blocking owner choice; §6.3 remains an exhaustive list of open boundaries.
- **DS20-F02 (MEDIUM):** recorded `OPEN-N1` and `OPEN-N16` as unused namespace positions without
  inventing a historical reason or renumbering stable tags.
- **DS20-F03 (LOW):** changed §4.4's unqualified `[OPEN]` tolerance to `[OPEN-N13]`.
- **DS20-F04 (LOW):** added `[OPEN-F3]` and `[OPEN-F4]` to their §6.3 body occurrences.
- **DS20-F05 (LOW):** made §1.5's P2 loop apply §1.4.2's `bar_open_time <= now - T` closure gate
  before archive merge, so a target ending at `now` cannot admit a forming bar.
- **DS20-F06 (LOW):** identified A1–A5 as the first through fifth semicolon-delimited clauses of
  plan `:641`, respectively, preserving the single source line while making sub-attribution exact.
- **Census discrepancy:** DS20's verdict header reports five LOW findings, but its Findings section
  contains only the four LOW entries F03–F06. This fold covers all six stated findings and does not
  fabricate an unprovided F07.

---

## Appendix A — reuse map (REUSE-FIRST)

| Need | Existing asset (cited) | Reuse mode |
|---|---|---|
| P2 cursor backfill loop | `02_MTC_BACKTEST/src/data/download.py:97-240` (time-cursor paginate, `since`/`limit`, empty + no-progress stop, `< end_ms` filter, dedupe+sort) | pattern seed; not modified by this lane |
| Retry classes + backoff curve | `download.py:202-210` (`RequestTimeout/DDoSProtection/ExchangeNotAvailable/NetworkError`, `base_delay * 2**n`) | pattern seed |
| Proxy (Binance-perp) ingestion | `download.py:26-50` (`defaultType: future`), `_convert_symbol` `:53-76` | used as-is for `track=PROXY` |
| Write-path data-quality checks | `io.py:validate_dataset` `:108-175` (columns, NaN, conditional duplicate diagnostic, gaps, OHLC consistency) | reused through the explicit producer-local `timestamp` projection; unconditional duplicate and archive identity/version checks added in §4.2 |
| At-rest format + load/save | `io.py:21-106` (Parquet/CSV, UTC timestamp normalisation) | reused |
| Dataset metadata / listing | `io.py:list_datasets` `:178-239`, `get_dataset_info` `:242-299` | reused for the archive index |
| Archive index pattern | `cache.py:CacheManager` `:23-248` (JSON index, key hashing, get-or-fetch, stale-entry prune) | pattern seed for the archive index |
| WS heartbeat/reconnect/gap doctrine | `ADR-0021:52` | design constraint |
| Backup / second-location / watchdog | WP-P0-26 (plan `:577-588`) | consumed dependency |
| Quality-gate check suite + verdict records + D026 fixtures | WP-P0-21 (plan `:515-525`) | consumed dependency |
| Shared freshness vocabulary (7 states) | WP-P0-04 (plan `:331`), brief `:2317-2325` | consumed contract |

## Appendix B — source lines read (evidence index)

- Plan `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`: `:317-332` (WP-P0-04),
  `:515-525` (WP-P0-21), `:527-537` (WP-P0-22, context), `:577-588` (WP-P0-26), `:630-645`
  (WP-P0-30), `:748-750` (WP-V2A-08 dependency), `:1004` (WP-V3-03 provenance/verdict posture).
- Brief `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`: `:196` (R7 context),
  `:202` (R13 — WP-P0-21 origin), `:347` (bar-close system), `:1203` `:1749` `:1881`
  (bar-close usages), `:2297-2332` (seven freshness states, rejections, carrier assignment),
  `:3098` `:3391` (freshness on the dashboard, no silent resize).
- `WAYFINDER_DECISION_FOLD_2026-08-23.md`: `:21` (#44 resolution — retention probe, dual-track,
  collector on KVM2, one package owns collector + feed), `:38` (blocks WP-V2A-08), `:41`
  (letter names; #45 time discipline → WP-P0-09 rows), `:59` (findings ≠ requirements).
- `WAYFINDER_OPERATOR_SURFACE_FOLD_2026-08-23.md`: `:19` (chart scope, VEN-E sole authority),
  `:31` (no second collector), `:42` (chart never a data authority), `:52` (five availability
  classes), `:64` `:88` (read-only indicators; thresholds `[OPEN]`).
- `AGENTS.md`: `:30-31` (research/execution trust separation), `:46-47` (D026 definition).
- `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0021-hyperliquid-integration-policy.md`: `:14`, `:47-57`,
  `:79`, `:94-100` (adapter boundary, separate environments/endpoints, WS recovery doctrine,
  validation; these lines do not establish endpoint authentication). The unauthenticated-public-
  read design boundary is plan `:644`.
- `HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md`: `:73-85` (rate limits, WS caps,
  shared-IP constraint on one VPS).
- `02_MTC_BACKTEST/src/data/download.py` (full), `io.py` (full), `cache.py` (full).
