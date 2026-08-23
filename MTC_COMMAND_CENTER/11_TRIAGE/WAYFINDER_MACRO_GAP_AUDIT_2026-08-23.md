# WAYFINDER MACRO GAP AUDIT — WHAT THE MASTER PLAN MAY HAVE FORGOTTEN

**Date:** 2026-08-23
**Task:** owner-dispatched wayfinder pass: treat the accepted architecture/requirements/work-package set as a strong but potentially incomplete hypothesis; search aggressively for missing macro capabilities, workstreams, boundaries, dependencies, lifecycle gaps and incorrect assumptions; propose the best decomposition of the remaining work before implementation.
**Status:** **FINDINGS AND PROPOSALS ONLY.** This document adds **no requirement, no safeguard, no package and no number** to the canonical set. Per `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md` §6, findings never become requirements, new packages need the plan document and the owner's word, and nothing here authorizes anything. The totals remain **60 requirements and 69 packages** unless and until the owner changes them.
**Basis:**
- Document set at commit **`764da27f`** (branch `codex/g1-architecture-c2-r1-20260823` — the accepted candidate `c81aacb8` plus its status record): the technical brief v2.1 (read end-to-end twice by independent extraction passes, plus targeted synonym greps before any ABSENT verdict), the 69-package delivery plan and the 60-row register (read in full by the lead), both owner documents.
- Read-only repository inspection: root and `MTC_COMMAND_CENTER` inventory sweep, `03_QUANTLENS/data` bundle manifests, `IBKR_PAPER_BRIDGE` deploy/ops assets, CI search, watchdog/backup-tool search, Pine confirmation, `_AI_MEMORY/LIVE_TRADING_GATE.md` (all fourteen preconditions), and the 2026-08-17 Bridge V2 deferral backlog.
- **No code was changed, no host contacted, nothing executed beyond read-only git/grep/ls.**

---

## 1. Verdict in three sentences

The accepted plan is unusually sound **where it looks**: identity and evidence binding, the sizing seam, admission staging, emergency-operation separation and the two-lane paper/testnet split all survived adversarial re-reading with no new structural defect found. The holes are **where it does not look**: the infrastructure that keeps evidence alive (backup, hosting, watchdogs, CI, clocks), the venue's physical reality (account binding, custody, treasury, data for the venue actually traded), and a small number of **dangling dependencies inherited from the retired 2026-08-17 package scheme** that the new 69-package plan silently dropped. None of this invalidates the plan; most of it is addable as one to two new workstreams plus amendments to existing packages, and almost none of it lengthens the critical path — but three items must close **before any forward evidence clock starts**, or the clocks themselves are built on sand.

---

## 2. Confirmed macro gaps

Legend: **ABSENT** = zero treatment found in the brief, plan or register (synonyms checked). **PARTIAL** = mentioned, but no design, no owner, or no package. Each row states the consequence in owner terms and the earliest point it must exist.

### Group A — Evidence survivability and operations

**A-GAP-1 · Backup, restore and disaster recovery for evidence stores — ABSENT (highest-severity finding of this audit).**
Zero occurrences of backup/restore/disaster-recovery for any datastore in the 439 KB brief; VPS-host-level DR explicitly not addressed anywhere. Yet the plan's own rules make evidence loss catastrophic by design: D-15 states an absent or incomplete observation ledger yields **zero confirmation evidence**; the paper-soak rule says a stopped window **never resumes**; admission and promotion records are append-only stores nothing copies anywhere. One failed disk erases the trial catalog, the observation ledger, the admission store, the promotion registry and the soak records — resetting every clock the whole program exists to accumulate. *Repo note:* a tested backup/restore tool with a runbook already exists (`02_MTC_BACKTEST/scripts/backup_restore.py` + `docs/backup_restore_runbook.md`) — but it belongs to the engine Q5 retires, and no package carries the pattern forward. **Earliest need: accepted before the first forward clock starts (before WP-V2A-08 / WP-V2B-07).**

**A-GAP-2 · Run-hosting decision, uptime, and a liveness watchdog that reaches the owner — PARTIAL.**
Brief §12.1 splits research (owner PC) from execution (VPS), but never states where `INTERNAL_PAPER` and the shadow fleet physically run, names no uptime requirement, and defines no watchdog that tells a non-technical owner his 8–16-week soak died. The owner's starting-point file says the paper soak runs "on my own machine" — and this repository's own history records that machine killing a soak before: the IBKR paper window of 2026-07-20 died to Windows **sleep** (v1, ~04:27Z). Combined with the never-resume rule, a single sleep, update-reboot or power cut mid-window destroys up to 16 weeks of calendar evidence. Paging exists only as dashboard-side notions (`DRIFT → audible PAGE`, one notification channel); no push/phone path, no process-liveness monitor for shadow/paper, no package. *Repo note:* watchdog patterns exist (`03_QUANTLENS/tools/run_watchdog.py` and the overnight watchdog family, `02_MTC_BACKTEST/scripts/health_alerts.py`), and two LLM research dumps on exactly this topic ("Dashboard & Observability for a Bar-Close Retail Trading Bot", 2026-08-18/20) sit unused in `08_DASHBOARD_APP/apps/Deepreseach*/`. **Earliest need: decided before any clock starts; watchdog live before the soak window opens.**

**A-GAP-3 · Continuous checks have no home: the only CI dies with the component being retired — PARTIAL.**
The brief mandates its parity tests "run in CI" (§9.6) and specifies the Pine alert guard as a CI guard (§8.3), but the only CI in the entire repository is `MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/{parity.yml,tests.yml}` — inside the engine Q5 freezes. There is no repo-root CI, none for the Bridge, and no package that builds one. Every D026 RED/GREEN guard the plan creates (golden suite, contract tests, no-`alert(` guard, admission fixtures) currently has nowhere to run automatically — in the plan's own words, a warning label with no door. **Earliest need: before WP-P0-10's golden suite and WP-P0-23's guard claim continuous protection.**

**A-GAP-4 · Missed-decision policy and live-bar backfill — ABSENT.**
No named policy anywhere for the basic bar-close question: the process was down when the bar closed — on restart, does it act late, skip, or something else? The freshness state machine's `RECOVERING` replays **fills**, not decisions; the live-gate "dropped signal" drill tests plumbing, not policy. Likewise, backfill of candle bars missed while a feed was down is never mentioned. This is kernel-semantics territory: **it belongs as a decided capability row in WP-P0-09** and a consumer obligation in WP-V2A-08, or five implementations will each invent their own answer again.

**A-GAP-5 · Time discipline — ABSENT.**
No treatment of the authoritative bar-close timestamp source (venue clock vs local), timezone/DST handling, or host clock sync (NTP) — while §12.3 measures staleness in seconds and the whole system trades on bar close. One decided paragraph plus a host requirement; cheap now, expensive as a live incident.

**A-GAP-6 · Forward-evidence growth and retention — ABSENT.**
The 20 GB budget with LRU eviction covers research artifacts only. The stores the design itself creates as append-only — shadow observation records, the observation ledger, the admission store, the drag audit log, months of paper/testnet logs — have no retention policy and no growth bound. Needs a policy extension of the §11.2 discipline, with protected classes (the ledger is never evicted — see A-GAP-1).

### Group B — Venue and capital reality

**B-GAP-1 · Two dependencies of the accepted brief point at packages that no longer exist — internal defect, blocking Q6.**
Brief §17.2 lists as Bridge-V2 dependencies: "**Package 7 exchange reverification (Q6)**" and "**Package 1 §A.2 store decision**". Those IDs come from the retired 2026-08-17 scheme (`11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`: Package 7 = *Official exchange reverification*, "start Package 7 first"; Package 1 = *V2 architecture contract pack*, its exchange-dependent decisions "explicitly conditioned on Package 7's output"). The 69-package plan contains **neither** (grep: zero hits for "Package 7", "reverification", "§A.2"). Consequence: **Q6 — subaccounts vs virtual books, i.e. the answer to venue position netting — is waiting on a verification task that no current package owns**, while WP-V2B-03 (multi-worker) and the bucket design proceed without it. The netting question itself is only PARTIAL in the brief: the virtual-books fallback is explicitly "must be specified before it is needed" and never specified; per-strategy-versus-venue-net reconciliation is undesigned. Note that live-gate precondition 10 already assumes a **dedicated sub-account** exists.

**B-GAP-2 · Exchange wallet custody has less design than the dashboard login — PARTIAL.**
D-16 gives the dashboard authenticators a deep, drilled, redundant design. The credential that can actually move money — the Hyperliquid main wallet and its agent/API wallets — has one checklist line (gate precondition 11). No procedure for generation, storage medium, backup, loss recovery, or rotation of the master key; nothing states where the seed lives or what happens if it is lost while a position is open. The Bridge README's rule ("API wallet cannot withdraw; never the main key") is right and remains a rule without a runbook. **Earliest need: before any credential exists at all — i.e., before WP-V2B-07's testnet credentials.**

**B-GAP-3 · Treasury and venue risk — PARTIAL.**
Deposit/withdrawal procedure, how much capital ever sits at the venue, USDC depeg stance, and a due-diligence record on Hyperliquid itself (solvency, bridge risk, ToS/geo access) appear nowhere. O-16's twelve-criterion review discipline covers every open-source dependency but was never applied to the single largest counterparty in the system — the venue. A short written venue-risk and treasury policy, owner-decided, belongs in the same family as the OSS ledger.

**B-GAP-4 · Research data does not come from the venue being traded, and nothing refreshes it — PARTIAL.**
Storage and identity are well designed (bundles hashed, `dataset_manifest_sha` inside `evaluation_run_hash`, data-quality checks in WP-P0-21). But acquisition has no owner: the primary bundle is **Alpaca** (12 crypto symbols; manifests dated 2026-06-28, ~8 weeks stale), secondary crypto data is **Binance futures**; there is **no Hyperliquid historical-data tool anywhere in the repository**, and no package or cadence for refreshing any bundle. The rebuilt simulator will therefore compute venue-grade economics (real fee schedule, funding per interval) **on prices from a different venue** — a mismatch nothing currently names or bounds. The live/shadow feed side is similarly unowned: WP-V2A-08 consumes "real market feeds, read-only" that no package builds or validates. **Earliest need: design in wave 1; live-feed infrastructure proven before WP-V2A-08.**

**B-GAP-5 · Instrument universe governance — PARTIAL.**
Instrument metadata is frozen per package (good). But per-bucket symbol allowlists, a delisting-while-position-open procedure, and handling of venue spec changes (size decimals, tick size) are never mentioned. One policy document plus a kernel/Guardian consumer rule.

**B-GAP-6 · Order-time API failure handling — PARTIAL.**
`PartialRecoveryBroker` handles submitted-but-unacknowledged correctly. Retry/backoff policy, venue maintenance windows, and rate-limit behaviour *at order time* (as opposed to fleet sizing) are undesigned. Fold into the WP-P0-25 boundary decision's required surface.

### Group C — Lifecycle and architecture seams

**C-GAP-1 · What happens to an open position when its identity dies — PARTIAL.**
§6.7 meticulously resets **evidence clocks** on any identity change, and lifecycle step 21 says "scale up / suspend / retire" with zero elaboration — but nothing states what happens to a **position already open** under a superseded identity, a suspended strategy, or a retired package, nor who closes it (operator FLATTEN? adopt-under-new-identity? run-off under old identity?). Same hole for a KILL-latched restart holding exposure. Must be a named policy before the first `LIMITED_LIVE` position exists; natural home: the WP-V2B-10 semantics family plus a lifecycle rule in §6.3.

**C-GAP-2 · Concurrency at the allocator/Guardian seam — ABSENT.**
The centerpiece seam has no serialization design: two workers proposing against the same bucket capital at the same bar close, snapshot binding order, double-spend of bucket headroom. Cheap to fix as a contract rule now (single-writer per bucket per bar, ordered binding through the Decision Orchestrator, or optimistic reject on `snapshot_id` conflict — decided, not implied); expensive to discover live in V2B. Belongs in WP-P0-04 (contract rule) and WP-V2A-03 (enforcement proof).

**C-GAP-3 · Environment identity — ABSENT.**
None of the three identity hashes includes Python version, dependency lockfile or OS; Windows-development-versus-Linux-production float determinism is never discussed, while deterministic replay (O-30) and bit-identical golden reproduction (WP-P0-11) both silently assume it. Either the composite identity carries environment lineage, or the exclusion is an explicit recorded decision with a compensating rule (e.g. goldens re-run per environment). Belongs in WP-P0-04.

**C-GAP-4 · The plan makes every research trial heavier and never asks if 100k-trial sweeps still finish — ABSENT.**
WP-P0-20 rebases every acceptance-bearing trial on the full kernel plus shared allocator at the same moment O-28 keeps 100,000-trial runs as the workload, and no compute location, runtime budget or queue design exists. The two-tier funnel that resolves this (cheap vectorized screening stays legal as `SIGNAL_SCREEN_ONLY`; full-kernel simulation for survivors) is *implied* by the lineage classes but never stated as the intended operating model. WP-P0-20's acceptance should include a measured trials-per-hour figure and that explicit funnel statement.

**C-GAP-5 · Smaller seam notes (fold into existing packages, one line each).** Contract version-skew during staged deploys (kernel and Bridge briefly on different released contract versions) — WP-P0-04. Change management for editing a live `RiskBucket` (who, through what mechanism, with what identity consequence) — WP-V2B-01/05. V1 end-of-life: decommission trigger and archival of V1's accumulated evidence DBs (the VPS instance and the dormant local `bridge.db`, last written Jul 13) — alongside WP-V2B-11. Fill-model calibration loop: measured testnet/live slippage feeding back into the simulator's in-path parameter — extension of WP-V3-05. Scheduled-job infrastructure (the divergence alarm and daily correlation refresh have no scheduler owner; no Task-Scheduler/cron assets exist in-repo) — OPS workstream below.

### Group D — Owner-world gaps

**D-GAP-1 · Tax, accounting export and jurisdiction/ToS review — ABSENT.** All "legal review" language in the doc set is OSS-licence-scoped. Live trading creates tax events and runs against venue terms from the first fill; one owner decision plus a small V4-adjacent export package.

**D-GAP-2 · Owner incapacity — ABSENT.** Every redundancy mechanism protects against a lost device, none against an unreachable owner with an open live position (single-operator design is explicit). A sealed one-page instruction for a trusted person — or the owner's explicit recorded decision **not** to have one — belongs in the same decision family as D-16. Decide it; don't forget it.

**D-GAP-3 · Funding is designed but no package names it — carrier ambiguity, not a gap.** Correcting this audit's own initial hypothesis: perp funding **is** covered at brief §9.2 (line ~1657: applied per funding interval, `funding_events` v6 ledger, same schedule both sides). But WP-P0-12's defect list (multiplier, min-notional, metadata, gap fills, slippage, collision policy, fees) does not name funding, and no package output does. Ensure each §9.2 control-table row has a named package carrier so funding cannot silently fall between WP-P0-12 and WP-P0-20.

---

## 3. What was checked and found sound

So that silence elsewhere is not read as "unexamined": dataset identity inside the hash chain (§6.7/§11.3); Bridge crash-recovery and mid-position kill contracts; the funding design at brief level; the no-retro-blessing rule for historical evidence (§9.1a rule 5); key permission scoping as a gate principle; the zero-trust access path (Tailscale mesh, no public port, WebAuthn step-up); the two-lane INTERNAL_PAPER/EXCHANGE_TESTNET separation with its D026 cross-crediting fixture; the R1/R2 correction passes (every one re-verified here held); and the T0 gate-coverage rule. The repository sweep also confirmed the brief's core factual claims spot-checked: exactly one live Pine controller with `alert()` at lines 2020/2028, the existing three-protocol broker boundary, and the Bridge's deploy kit.

A second kind of finding: **the plan forgot existing assets, not only missing work.** Harvestable today: `backup_restore.py` + runbook and `health_alerts.py` (02_MTC_BACKTEST), the QuantLens watchdog family, the Alpaca/Binance downloaders, the 02_MTC_BACKTEST CI workflows as a template, and the two dashboard/observability research dumps of 2026-08-18/20. Layout corrections for any future plan text: `01_PINE` is nested at `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/` (not top-level); two `reports/` locations exist (`04_REPORTS/` empty vs `01_MTC_PROJECT/reports/` populated); a near-empty legacy `MCC_COMMAND_CENTER/` stub sits at repo root; the `apps/Deepreseach` + `apps/Deepresearc 2` directories are misplaced research notes inside a code tree — all four are WP-P0-01 inventory fodder.

---

## 4. Proposed decomposition of the remaining work — PROPOSAL ONLY

Nothing below exists until the owner says so; adding any package changes the plan document under its own change control, and every addition would need G1-IA like everything else.

**Add Workstream 8 — Operations and evidence survivability** (Phase 0 design, V2A/V2B execution; almost entirely parallel-safe, off the critical path):
- **OPS-A Evidence-store backup/restore and DR** — policy, tooling (harvest `backup_restore.py` pattern), restore drill proven RED/GREEN, protected-class list (observation ledger never evicted, never unrecoverable). Gate: accepted before any forward clock starts.
- **OPS-B Run-hosting decision + watchdog/paging** — one written decision: where soak and shadow run (owner PC hardened vs VPS vs both), uptime target, host-outage-versus-clock rule made explicit; a liveness watchdog with a push path to the owner's phone, live before the soak window opens. Consumes the Deepresearch dumps and the existing watchdog assets.
- **OPS-C CI home** — repo-level CI carrying the golden suite, contract tests, parity set and the Pine guard; the 02_MTC_BACKTEST workflows as template; explicitly survives Q5's freeze of that engine.
- **OPS-D Time-discipline spec** — authoritative bar-clock source, timezone/DST rule, NTP requirement; one decided page consumed by kernel and runtime packages.
- **OPS-E Forward-evidence retention** — extend the §11.2 budget discipline to the append-only stores and forward logs.

**Add Workstream 9 — Venue and capital reality** (Phase 0 decisions on paper; venue-touching parts land with V2B under existing gates):
- **VEN-A Exchange reverification + account-binding design** — rescues old Package 7; closes Q6 (subaccounts vs virtual books **including the fallback spec**), designs per-strategy-versus-venue-net reconciliation. **Must be accepted before WP-V2B-03 (multi-worker) starts** — a dependency the current plan is missing.
- **VEN-B State-store decision** — rescues old Package 1 §A.2 so the brief's dependency line points at something real again.
- **VEN-C Wallet custody and treasury runbook** — main/agent wallet generation, storage, backup, rotation; deposit/withdrawal procedure; capital-at-venue cap; venue due-diligence record (O-16-style, applied to the venue); feeds live-gate preconditions 10/11/12 instead of scrambling at WP-V4-01.
- **VEN-D Instrument universe policy** — allowlists, delisting-with-open-position, spec-change handling.
- **VEN-E Venue market data** — Hyperliquid historical-data source and bundle-refresh cadence for research; the live/shadow feed service with quality gates (reusing WP-P0-21's checks) proven before WP-V2A-08 consumes it.

**Amend existing packages (no new IDs needed):** WP-P0-09 adds decided rows for missed-bar/restart policy (A-GAP-4) and confirms funding/margin semantics rows carry to a named implementer (D-GAP-3); WP-P0-04 adds the concurrency/serialization rule, version-skew rule and the environment-identity decision (C-GAP-2/3, C-GAP-5); WP-P0-20 acceptance adds a measured throughput statement against O-28 plus the explicit two-tier funnel sentence (C-GAP-4); WP-V2B-10/§6.3 add the open-position-on-identity-death policy (C-GAP-1); WP-V2B-01/05 add RiskBucket change management; WP-V2B-11 gains the V1 decommission/evidence-archival note; WP-V3-05 gains the calibration feedback loop.

**Sequencing recommendations (within the existing plan, no new authority implied):**
1. **De-fang Pine early.** The chain WP-P0-01 → WP-P0-02 → WP-P0-19 → (owner G2) → WP-P0-23 is short, independent of the kernel chain, and removes the only live order path in existence — the single most dangerous standing artifact. Put WP-P0-19 in wave 1 and bring the G2 authorization question to the owner early rather than late.
2. **Start OPS-B and VEN-E infrastructure in wave 1.** Feeds, hosting and watchdogs can run and prove themselves for weeks **without any strategy loaded** — pure infrastructure soak produces zero strategy observations, so it creates no D-15 leakage and burns no evidence integrity, while retiring exactly the operational risks that would otherwise kill the first real clock. This partially rescues O-23's calendar-time intent, because the honest critical path to the first *legal* shadow clock is long: P0-04/P0-06 → P0-09 → P0-10 → P0-11 → P0-12 → P0-20 → P0-13/P0-21/P0-22 → V2A-01…07 → V2A-10 → V2A-08.
3. **OPS-A (backup) is a gate, not a chore**: a clock that can be erased by one disk is not evidence. Accept it before the first identity is admitted anywhere.

**Explicitly not proposed:** no new requirement or safeguard text, no renumbering, no change to any owner wording, no early venue contact, no start of anything. The three wave-1 items above are already legal under the existing plan's own dependency rules once G1-IA is given for them; the new workstreams are for the owner to accept, reshape or refuse.

---

## 5. Owner asks, in plain language

1. **Should we add the two missing workstreams** — "keep the evidence alive" (backups, hosting, watchdogs, CI, clocks) and "the venue's real world" (account setup, wallet safekeeping, money-at-exchange policy, exchange data)? They are the two areas your current plan does not look at, and two of them (backups, hosting/watchdog) should be finished **before any evidence clock ever starts**.
2. **Where should your 8–16-week paper soak actually run?** Your own PC has killed a soak before by going to sleep, and the rules say a stopped window starts over from zero. Options: harden your PC, use your VPS, or both. This is one decision, and it should come before the clock ever starts.
3. **Two old prerequisites fell out of the new plan** — the official exchange re-check (old "Package 7") and the storage decision (old "Package 1 §A.2"). The accepted brief still depends on both by name. They need new homes; without the first one, the "one account or many sub-accounts" question can never be answered.
4. **The exchange wallet needs the same care as your dashboard keys.** Right now the plan protects your login keys deeply and your money keys with one checklist line. A written safekeeping procedure (where the master key lives, its backup, what happens if it is lost) should exist before any credential is created.
5. **Small decisions to record once:** what happens to an open position when its strategy is retired or changed; taxes and record exports; whether a sealed instruction for a trusted person should exist in case you are unreachable with a live position open (deciding "no" is fine — deciding is the point).

---

*Prepared read-only under the wayfinder task of 2026-08-23. Verification trail: brief absence verdicts were produced by a full end-to-end read with synonym greps recorded per verdict; every ABSENT above had zero hits under multiple phrasings; every PARTIAL cites its section. Repository claims cite paths checked on 2026-08-23. This document authorizes nothing and changes no canonical count.*
