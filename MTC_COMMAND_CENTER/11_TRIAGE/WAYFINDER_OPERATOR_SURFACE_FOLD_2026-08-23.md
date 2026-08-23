# WAYFINDER OPERATOR-SURFACE FOLD — 2026-08-23 (map #95)

**Status:** owner-decision record reconciled onto `feature/wayfinder-final-red-team-20260824` from current master on 2026-08-24 under the owner's separate acceptance. Planning only — **implementation authorized: NO.** Per D-12, nothing here authorizes trading code, Pine, Bridge behaviour, host contact, credentials, deployment, testnet, live, ARM, KILL, FLATTEN or any work package to start. Git history is authoritative for final merge status.

**What this is.** GitHub map issue [Execution Dashboard & Trading Chart decision map (#95)](https://github.com/bsemaay-tech/mtc-command-center/issues/95) settled what the owner must see, which controls may appear at each stage, what the execution chart may contain, and how mobile access is staged. Two research tickets established reuse options and the brownfield execution-surface facts. Four owner-grilled tickets then recorded the decisions. **Detail lives in each ticket's final resolution comment; this document indexes and assigns the decisions to existing planning carriers.**

**Locked prior art.** Folds #37, #54, #67, #78 and #79 remain binding and are not reopened. In particular: venue data, worker/account isolation, lifecycle and admission doctrine, kernel seams, chart-POC order, Explorer scope, Guardian policy, reconciliation and evidence-window rules are inherited unchanged. This fold specifies the operator surface that reads or requests through those authorities; it does not become a new authority.

**Change-control position.** Amends the planning set based on `origin/master` at `577e36eb4b44657b00e0ebd801bdb0e2b1da569a`. **Owner outcome documents are untouched. Requirement count remains 60 = 44 + 16. Package count remains 76.** No package is added, removed or renumbered. **Materiality: MATERIAL** — the fold tightens T0 command-surface dependencies and acceptance, defines the truth shown to the operator, stages remote safety controls and constrains protected editing. A fresh G1 acceptance round over the amended set is recommended before G1-IA for any affected package; that audit and every implementation authorization remain separate owner decisions.

---

## 1. Owner decisions

| Ticket | Ratified decision |
|---|---|
| [Operator information doctrine (#100)](https://github.com/bsemaay-tech/mtc-command-center/issues/100) | Use three truth groups and four visible checkpoints: strategy intent; Guardian authorization/rejection; bridge/store execution record; venue reality. Home is a fleet cockpit plus exception strip. Missing data uses five honest availability labels. Current protection is always visible, history remains drill-down evidence, and freshness is per source. **Operator Display Doctrine v1** is owner-gated. Numerical thresholds remain `[OPEN]`. |
| [Staged controls and interlocks (#101)](https://github.com/bsemaay-tech/mtc-command-center/issues/101) | ARM/DISARM/KILL/FLATTEN exist at global, bucket and strategy scope; the safer parent wins and global ARM never silently arms children. Controls stay visible with blockers. DISARM is immediate; stronger actions require stronger confirmation/authentication. Success is not a click: the UI distinguishes `REQUESTED`, `ACKNOWLEDGED`, `RECONCILED` and `FAILED`. Protective editing waits for the strict evidence gate and becomes a governed request that cannot increase risk or create an entry. |
| [Execution trading-chart scope (#102)](https://github.com/bsemaay-tech/mtc-command-center/issues/102) | The chart shows execution truth only: candles, selected position/fills, working orders, current/history protection, rejected events, freshness and read-only strategy-owned indicators. VEN-E is the sole market-data authority; native/proxy provenance is visible. A bounded window opens over the complete retained record. Map #78's library verdict is reused across separate trust domains. The #94 canvas is disposable fake-data specification, and a permissive tearsheet/report-library comparison precedes custom analytics. |
| [Mobile and remote access doctrine (#103)](https://github.com/bsemaay-tech/mtc-command-center/issues/103) | Ship one responsive private web app, not a native app initially. Mobile begins as a read-only 60-second incident view; DISARM follows accepted authentication evidence; KILL/FLATTEN follow map-#96 design and local/testnet drills. ARM and protective dragging remain desktop-only unless separately re-decided. Approved devices, private mesh, WebAuthn/FIDO2, fresh-resume reconciliation, stale/offline read-only behaviour and control-free notifications are binding. |

Research inputs, both closed 2026-08-23: [open-source trading dashboards and operator UIs (#98)](https://github.com/bsemaay-tech/mtc-command-center/issues/98) and [execution-surface inventory (#99)](https://github.com/bsemaay-tech/mtc-command-center/issues/99). Visual input: [result-chart screen mock (#94)](https://github.com/bsemaay-tech/mtc-command-center/issues/94), whose latest reviewed hand-coded canvas reference is `2882b3f748e184085f93226f527a964b84439b35`.

---

## 2. Carrier assignments

| Responsibility | Building/owning carrier | Consumer/proof carrier |
|---|---|---|
| Operator truth/history read model | **WP-V2B-03** | WP-V2B-05 renders; WP-V2B-07 supplies paper/testnet acknowledgement/failure evidence |
| Execution-chart market data and provenance | **WP-P0-30 VEN-E** | WP-V2B-05 chart; no second collector |
| Shared chart-library selection | **WP-P0-18** | WP-V2B-05 execution chart and WP-V3-11 research report use the verdict in separate trust domains |
| Fleet cockpit, display doctrine, request-state rendering | **WP-V2B-05** | Reads accepted semantics and feeds only; never decides an economic outcome |
| Command scope, hierarchy and response states | **WP-V2B-10** | WP-V2B-06 protects; WP-V2B-05 renders |
| Private access, approved devices, resume/offline behaviour | **WP-V2B-06** | WP-V4-06 stages mobile access |
| Simulation-only protective editing | **WP-V2B-08** | Waits for the strict evidence/readiness gate; zero broker network path |
| Paper/testnet protective editing | **WP-V3-07** | Governed request path; T0, G3+G4 |
| Live protective editing | **WP-V4-03** | Desktop-only initially; T0 and live gates remain binding |
| Mobile incident view and staged safety commands | **WP-V4-06** | T1 while read-only; T0 once any command is enabled |
| Research result/report surface | **WP-V3-11** | Runs the permissive tearsheet/report-library comparison before custom analytics |

The chart is a view/request surface. It never becomes a broker authority, market-data authority, Guardian, reconciler or lifecycle writer. Reusing a library does not merge the research and execution applications' processes, ports, sessions, credentials or data authority.

---

## 3. Operator Display Doctrine v1

This is an owner-gated definition artifact. Changing the doctrine requires the owner's explicit word; applying the accepted version consistently to screens does not require a new doctrine decision.

1. Separate strategy intent, Guardian outcome, bridge/store record and venue reality.
2. Never infer or fabricate a missing truth.
3. Show source, freshness and one availability class for every material datum: `AVAILABLE NOW`, `CAPTURED — READ ROUTE MISSING`, `NOT BUILT`, `UNKNOWN` or `NOT APPLICABLE`.
4. Put exceptions before routine detail.
5. Keep current expected-versus-venue protection and last verification visible for every open position.
6. Preserve permanent action and protection history with exact request/acknowledgement/reconciliation/failure states.

---

## 4. Reuse and prototype disposition

- The production chart uses the result of the already-planned open-source POC: **Lightweight Charts → ECharts → the gated TradingView library only if the permissive options fail**.
- That verdict is selected once and reused. Separate trust boundaries remain separate.
- The hand-coded #94 canvas is a disposable fake-data visual specification, not production architecture and not a production base.
- The strategy's own indicators may be displayed read-only when source and freshness are known.
- Before custom-building the TradingView-style research analytics report, WP-V3-11 compares permissively licensed tearsheet/report libraries and independently checks their numbers against source artifacts.

---

## 5. Amendments applied by this candidate

| # | File · location | Amendment |
|---|---|---|
| A1 | Technical brief · current counts | Corrects the current package total to 76 while preserving historical counts. |
| A2 | Technical brief · §12.2/§12.4/§12.5/new §12.6 | Records library reuse, strict protective-editing boundary, normative operator surface, chart scope and mobile doctrine. |
| A3 | Technical brief · A-15a/A-20/A-22 | Adds failable operator-display, governed-edit and desktop/mobile acceptance boundaries. |
| A4 | Work-package plan · count/fold notes | Records no new package, no new requirement and materiality. |
| A5 | Work-package plan · WP-P0-18/P0-30/V2B-03 | Assigns shared-library, sole chart-data and operator-read-model responsibilities. |
| A6 | Work-package plan · WP-V2B-05/V2B-06/V2B-10 | Assigns cockpit/chart rendering, access/resume rules and hierarchical command semantics. |
| A7 | Work-package plan · WP-V2B-08/V3-07/V4-03/V4-06 and gate G3 | Applies strict stage gates, governed protective-exit constraints and staged mobile safety access; maps the command-enabled mobile stage to the protected command gate. |
| A8 | Work-package plan · WP-V3-11 | Requires permissive tearsheet/report-library comparison before custom analytics. |
| A9 | Requirements register · scheme/mapping note | Extends O-02/O-29/D-09/D-16 carrier mappings without changing requirement text or counts. |
| A10 | Technical brief §12.5/§12.6 item 7; work-package plan §0/§2/§6/§8 | **Read-only-seam repair (2026-08-23):** splits WP-V2B-05 and WP-V2B-06 into read-only and command-completion milestones under a new plan-wide staged-milestone rule, so WP-V4-06 Stage 1 depends only on the two accepted read-only milestones and no longer inherits WP-V2B-10 or WP-V2B-06's command-authentication completion milestone. Stage 1 intentionally still depends on WP-V2B-06's read-only-private-access milestone. No package, requirement or owner decision changes. |

---

## 6. What remains open

- Every numerical freshness, alert, deduplication, timeout, confirmation and escalation threshold remains `[OPEN]`.
- Map #96 owns the exact authentication, confirmation, notification, retry/idempotency, acknowledgement, reconciliation and incident-response mechanics.
- WP-P0-18 must run before a production chart library is selected; the mobile/touch chart-drilldown result remains empirical.
- WP-V3-11 must run the focused tearsheet/report-library comparison before any custom analytics report is built.
- Screen visual refinement remains implementation work inside the doctrine; it may not weaken the doctrine.
- Fresh G1 acceptance of this material planning amendment and G1-IA for every affected package.
- The owner-authorized fresh T2 audit of the 2026-08-23 read-only-seam repair (A10) returned `REQUEST_CHANGES`: the seam itself passed, but legacy acceptance criterion A-15 still compressed the normative four checkpoints into `desired / accepted / actual`. The owner then explicitly directed the Lead to stop the audit loop, correct A-15 directly and move on. A-15 now names all four checkpoints. No further T2 audit or audit-acceptance claim is made; branch completion proceeds under that explicit owner override.

---

## 7. What this fold does not do

- No source, trading, Pine, Bridge-runtime, schema, migration, host, credential, deployment, testnet or live change.
- No database, service, process, worker, broker or venue is contacted or modified.
- No package starts and no G1-IA/G2–G9 gate is satisfied.
- No settled map is reopened and no owner outcome or safeguard text changes.
- No chart library or tearsheet library is selected here; no numeric value is invented.
- The original fold candidate performed no merge; its current-master reconciliation and merge are separate owner-authorized Git administration.

---

## 8. Verification

- Base: `origin/master` at `577e36eb4b44657b00e0ebd801bdb0e2b1da569a`.
- Branch: `feature/wayfinder-fold-map95-20260823` in isolated worktree `C:\WF104`.
- Current-master reconciliation: `feature/wayfinder-final-red-team-20260824` in `C:\WFREDTEAM_20260824`, starting from `0baea68ee3bd85a3a57068cc3a3c4876b197d690`; later map-#96 and map-#97 text preserved.
- Editing discipline: exact anchored patches only; no broad replacement, protected path or owner outcome document.
- Checks completed on the branch candidate: exact changed-path review, package/requirement recount, marker searches and whitespace check. Repo guard is re-run after the audit repair below.
- Counts: requirements **60 = 44 + 16** unchanged; packages **76** unchanged.
- T2 audit history: the direct DeepSeek route was unavailable (`402` balance) and the preferred free GLM route was unavailable (`429` upstream rate limit), so the documented fallback used fresh read-only Codex `gpt-5.6-sol` sessions at `medium`. The first audit returned `REQUEST_CHANGES` on a mobile carrier conflict, repaired by confining WP-V2B-05 to the shared responsive foundation and laptop/desktop commands while WP-V4-06 alone owns mobile access and commands. An owner-authorized additional fresh audit then found three documentation inconsistencies: package-level dependencies blocked WP-V4-06 Stage 1; the simulation prerequisite table contradicted its strict gate; and two appendices still gave the old dashboard proposal production authority. The owner explicitly authorized the narrow repairs and one final fresh T2 audit. The three repairs are present, but that final audit returned `REQUEST_CHANGES` on one remaining transitive-dependency problem: WP-V4-06 Stage 1 still depends on WP-V2B-05, which itself waits on WP-V2B-10 and WP-V2B-06, so the read-only stage does not yet have a genuine independent seam. **The owner then authorized this fourth narrow repair and one further fresh T2 audit.** WP-V2B-05 and WP-V2B-06 are each split into an independently acceptable read-only milestone and a command-completion milestone under a new plan-wide staged-milestone rule (plan §0); WP-V4-06 Stage 1 now depends only on the two accepted read-only milestones and no longer transitively depends on WP-V2B-10 or WP-V2B-06's command-authentication completion (brief §12.5, §12.6 item 7; plan §2, §6, §8). The fresh audit independently confirmed that the seam is genuine and acyclic, but returned `REQUEST_CHANGES` because legacy brief criterion A-15 still said `desired / accepted / actual`, contradicting the normative four checkpoints. The owner explicitly directed the Lead to stop further audits, fix A-15 directly and move on. A-15 now names strategy intent, Guardian outcome, bridge/store record and venue reality. No further audit ran and no audit-acceptance claim is made; branch completion proceeds under the explicit owner override.
