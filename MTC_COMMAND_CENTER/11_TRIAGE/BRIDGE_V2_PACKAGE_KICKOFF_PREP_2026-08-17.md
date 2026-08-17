# Bridge V2 Package Kickoff-Prep — 2026-08-17

**Artifact class:** UNACCEPTED kickoff-prep draft. Documentation only.
**Authority:** none. This file authorizes nothing — no package start, no code, no
review round, no deployment, no host contact, no credential use, no broker or
exchange action, no TESTNET, no MAINNET, no ARM, no order, no economic action.
Every package start requires its **own explicit owner authorization** plus a
**Gate-1 scope record with tier classification**; neither exists for any package
as of this draft. This file only *prepares* material so those starts can be
decided quickly and safely.

**Status of the source list:** the package list and tiers below are taken from
the corrected backlog, which is now an **accepted T2 documentation record**: the
owner authorized exactly one fresh T2 review on 2026-08-17 evening and it
returned **ACCEPT**
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`;
authorization chain in
`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`).
Acceptance of the backlog still starts no package.

**Process-artifact note:** the dispatch-prompt skeletons in this file are
prompts/dispatch packages, which are T3 process artifacts under the owner tier
policy — implementer/Lead self-check only, never their own model-audit round
(`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §5).

## 0. Sources

- **[BACKLOG]** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`
  — corrected working copy; authoritative package list and tiers **for this
  draft only**. All `docs/30...` references relayed through it follow its HEAD
  citation convention (committed tree `033546fb`, not the dirty B8 working copy;
  [BACKLOG] §1).
- **[T2-STATUS]** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_T2_STATUS_2026-08-17.md`
  — consumed T2 review of the backlog candidate: REQUEST_CHANGES, 3 required
  findings, authorization boundary.
- **[TIERS]** `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md`
  — binding repo-wide audit tier policy: reviewer counts, efforts, round caps,
  cadence, unchanged boundaries.
- **[ADDENDUM-UNACCEPTED]** `MTC_COMMAND_CENTER/11_TRIAGE/HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md`
  — unaccepted supplemental public-docs research; cited **as leads to verify,
  never as facts**.
- **[7WS]** `MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_SEVEN_WORKSTREAM_STATUS_2026-08-17.md`
  — seven-workstream boundaries and prohibited-now lists.

Tier review policy at a glance (from [TIERS] §2–§3, used in every acceptance
section below):

| Tier | Reviewer / rounds / effort |
|---|---|
| T2 (docs) | 1 reviewer, 1 round, medium effort. GLM-5.2 preferred; DeepSeek acceptable; a flagship at medium only if neither is available. |
| T1 (non-economic product) | 1 flagship (alternating Claude/Codex per round), high effort, max 2 rounds; GLM-5.2 second opinion only if findings raised or diff > ~300 lines. |
| T0 (economic/live/protected) | 2 independent flagships (`claude-opus-5` + Codex `gpt-5.6-sol`), xhigh, max 3 rounds; audited **immediately** at each work-package boundary regardless of cadence. |

## 1. Owner decision checklist (plain language)

Nothing below has been decided yet. Each item names the single "yes" from you
that unlocks a package. Until you give that yes, the package stays unstarted,
and every start also needs its own short written scope note naming its tier.

1. **The list itself — DONE tonight.** You authorized one fresh review of the
   corrected text and it returned ACCEPT, so the backlog is now an accepted
   record (`BRIDGE_V2_DEFERRAL_BACKLOG_T2_ACCEPTANCE_2026-08-17.md`). This
   acceptance starts no package by itself.
2. **Package 7 first — official Hyperliquid fact-check (paperwork only).**
   Your "start Package 7" unlocks a read-only check of official exchange
   documentation. Nothing touches your account, keys, or money. Every
   exchange-dependent design decision waits on its result. ([BACKLOG] §5 item 1)
3. **Packages 1 and 2 — design paperwork.** Your "start" unlocks both, and
   they can run while Package 7 runs. Package 1 has two halves: the half not
   depending on exchange facts (worker identity, storage model, Guardian veto
   rules) can start now; the half that does (sub-accounts, API wallets,
   same-symbol netting, margin mode, API limits, worker boundary, feed
   topology) stays unfrozen until Package 7's record exists. ([BACKLOG] §4–§5)
4. **Packages 3, 4 and 5a — safe build work.** Your "start" unlocks each one,
   each in its own separate isolated copy of the repository, using fake or
   fixture data only. ([BACKLOG] §5 item 3)
5. **Package 5b — the parity gauge.** Two steps before any build: first each
   concrete piece is classified (harmless read-only export vs. protected
   decision-logic work), then you separately approve the pieces. Read-only
   export pieces get the normal single review; anything touching protected
   decision logic needs the heaviest review and your separate approval, named
   per piece. ([BACKLOG] §4 Package 5b; [T2-STATUS] finding 3)
6. **Package 6, local half only.** Your "start" unlocks the fake-feed shadow
   mode. Hooking up a real Hyperliquid feed is a different, heavier package
   and a separate future decision. ([BACKLOG] §4 Package 6)
7. **Package 8 — real implementation.** No blanket start. You authorize each
   small work package one at a time; each gets the heaviest review (two
   independent top-tier models) immediately when finished. ([BACKLOG] §4–§5)
8. **Standing rule for everything above:** no VPS/host contact, no
   credentials, no exchange or account actions, no TESTNET/MAINNET, no ARM or
   orders, no changes to Pine/MTC/parity, and no touching the frozen V1
   candidate. Each of those needs its own explicit authorization and is not
   unlocked by anything in this file. ([7WS] §8; [TIERS] §6; [T2-STATUS])

## 2. Per-package sections

General gating that applies to **all** packages ([BACKLOG] §1; [7WS] §8;
[TIERS] §6): eligible V2 work may proceed only in separate branches/worktrees
under the normal audit tiers, never inside the frozen V1 candidate or its soak
lane; and no VPS/Hostinger/KVM2/GATEA-STAGING contact, no credential/secret
access, no broker/exchange/wallet action, no TESTNET/MAINNET, no ARM/DISARM/KILL
or orders, no Pine/MTC/TradingView-parity or strategy-logic changes, and no
trading-state mutation is authorized by this draft.

---

### Package 1 — V2 architecture contract pack

**Scope.** Settle worker identity, store model, and Portfolio Guardian veto
semantics locally. Worker boundary, feed topology, and subaccount fallback —
and every decision that depends on exchange behavior (subaccount eligibility,
agent-wallet behavior, same-symbol netting, margin mode, API limits) — are
CONDITIONED ON Package 7 output: they must not be frozen from stale or
unverified assumptions, and their freeze waits for Package 7's official
verification record. Documentation only; no code or live exchange assumptions
without current official evidence. ([BACKLOG] §4 Package 1)

**Tier.** T2 ([BACKLOG] §4 Package 1; the architecture-contract half of the
multi-strategy/Guardian rows in [BACKLOG] §3).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- The non-exchange-dependent subset (worker identity, store model, Guardian
  veto semantics) may run in parallel with Package 7 ([BACKLOG] §5 item 2).
- The exchange-dependent subset — subaccount eligibility/fallback,
  agent-wallet behavior, same-symbol netting, margin mode, API limits, and the
  worker-boundary and feed-topology choices — must not be frozen before
  Package 7's verification is on record ([BACKLOG] §4 Package 1, §5 item 2;
  [T2-STATUS] finding 2).
- Evidence caveat: the dirty `docs/30` B8 working copy is not committed or
  accepted authority; all `docs/30` citations must be HEAD citations
  ([BACKLOG] §1).
- Separate branch/worktree per the owner roadmap ([BACKLOG] §1).

**Explicit prohibitions.** No code (documentation only). No live exchange
assumptions without current official evidence. No freezing of
exchange-dependent decisions ahead of Package 7. Plus the general gating list
above (no host contact, credentials, exchange/account actions, TESTNET/MAINNET,
ARM/orders, Pine/parity/MTC changes, frozen-V1 mutation).

**Acceptance criteria.** Done means: (a) worker identity, store model, and
Guardian veto semantics are settled in the contract text with citations;
(b) every exchange-dependent decision is explicitly marked CONDITIONED ON
Package 7 with its trigger named; (c) all UNKNOWNs stay UNKNOWN; (d) the pack
passes one T2 review — single reviewer, single round, medium effort
(GLM-5.2 preferred; DeepSeek acceptable; flagship at medium only if neither is
available) per [TIERS] §2.

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 1 (V2 architecture contract pack), tier T2,
      documentation only, read-only repository.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (authoritative scope: §4 Package 1, §5 item 2; HEAD-citation convention §1)
  - IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md
    (HEAD citations only; the dirty B8 working copy is not authority)
  - Package 7 verification record, for the exchange-dependent subset only,
    if it exists at dispatch time; otherwise that subset stays CONDITIONED.
OUTPUT: one contract-pack document at <OUTPUT_PATH assigned by Lead>,
  in a separate branch/worktree (<WORKTREE_PATH>), nothing else written.
CONSTRAINTS:
  - Documentation only; no code, no runtime wiring, no repo mutation outside
    the output file's worktree.
  - Split the pack into (A) non-exchange-dependent decisions (worker identity,
    store model, Guardian veto semantics) and (B) exchange-dependent decisions
    (subaccount eligibility/fallback, agent-wallet behavior, same-symbol
    netting, margin mode, API limits, worker boundary, feed topology).
  - Section B decisions must be written as CONDITIONED ON Package 7 output and
    must NOT be frozen; cite [T2-STATUS] finding 2.
  - UNKNOWN stays UNKNOWN. No invented facts. Every claim cites its source
    (repo path, or the addendum explicitly labeled UNACCEPTED).
  - No VPS/host contact, credentials, exchange/account actions, TESTNET/
    MAINNET, ARM/orders, Pine/parity/MTC changes, or frozen-V1 mutation.
REVIEW: T2 — single reviewer, single round, medium effort (GLM-5.2 preferred;
  DeepSeek acceptable; flagship at medium only if neither available) per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list (exactly one output file);
  (2) per-decision table: decision | settled (A) or conditioned (B) | evidence
  citations | remaining UNKNOWNs; (3) self-verification statement that no
  exchange-dependent decision was frozen and no prohibition was crossed.
```

---

### Package 2 — MTC integration contract pack

**Scope.** Resolve Pine/Python sizing and lifecycle parity; freeze
`OrderIntent`/`ExitIntent`, Multi-TP, basket/add, stop semantics, and
desired/accepted/actual-state schemas. No runtime wiring. ([BACKLOG] §4
Package 2; open items and evidence in [BACKLOG] §3 rows "MTC sizing ownership
and `OrderIntent`" and "MTC exit lifecycle, Multi-TP and basket/add support".)

**Tier.** T2 ([BACKLOG] §4 Package 2; contract/parity design classified T2 in
[BACKLOG] §3).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- May run in parallel with Package 7 ([BACKLOG] §5 item 2).
- Precedence rule from the backlog: the contract must exist before even the
  first MTC-connected worker ([BACKLOG] §3, relaying `docs/30...:376-407`);
  MTC/Pine/risk/order implementation is T0 and separately owner-gated
  ([BACKLOG] §3).
- Separate branch/worktree per the owner roadmap ([BACKLOG] §1).

**Explicit prohibitions.** No runtime wiring of any kind. No edits to MTC,
Pine, TradingView parity surfaces, or strategy logic (design text only). No
orders, broker contact, or exchange actions. Plus the general gating list
above.

**Acceptance criteria.** Done means: (a) `OrderIntent`/`ExitIntent` schemas,
Multi-TP, basket/add, and stop semantics are frozen in contract text;
(b) Pine/Python sizing and lifecycle parity gaps are each resolved or
explicitly listed as open; (c) desired/accepted/actual-state schemas are
defined; (d) the pack passes one T2 review — single reviewer, single round,
medium effort per [TIERS] §2.

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 2 (MTC integration contract pack), tier T2,
      documentation only, read-only repository.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 2; §3 MTC rows for open parity/intent items, HEAD citations)
  - IBKR_PAPER_BRIDGE/bridge/engine/types.py (current Signal/OrderPlan shapes,
    as inventoried in [BACKLOG] §3)
OUTPUT: one contract document at <OUTPUT_PATH assigned by Lead>, in a separate
  branch/worktree (<WORKTREE_PATH>), nothing else written.
CONSTRAINTS:
  - Documentation only; no runtime wiring; no edits to MTC, Pine, TradingView
    parity, or strategy logic.
  - Freeze: OrderIntent/ExitIntent, Multi-TP, basket/add, stop semantics,
    desired/accepted/actual-state schemas.
  - Resolve or explicitly list every Pine/Python sizing and lifecycle parity
    gap; unresolved items stay OPEN, not assumed.
  - UNKNOWN stays UNKNOWN. Every claim cites its source.
  - No orders, broker/exchange contact, host contact, credentials,
    TESTNET/MAINNET, ARM, or frozen-V1 mutation.
REVIEW: T2 — single reviewer, single round, medium effort per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list; (2) schema freeze table (item | frozen
  definition | evidence); (3) parity-gap table (gap | resolved how | still
  open); (4) self-verification statement that no wiring or prohibited surface
  was touched.
```

---

### Package 3 — Dashboard V2 read-only prototype

**Scope.** Use fixture/mock data for an aggregate overview, per-worker
drill-down, Market Context page, desired/accepted/exchange-truth views, and
phone-responsive monitoring. No ARM, order, config, credential, or live-worker
API changes. ([BACKLOG] §4 Package 3; view requirements relayed from
`docs/30...:911-942,975-1037` in [BACKLOG] §3.)

**Tier.** T1 ([BACKLOG] §4 Package 3; read-only mock/fixture UI classified T1
in [BACKLOG] §3).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- Must run in a separate isolated worktree ([BACKLOG] §5 item 3; general
  roadmap rule [BACKLOG] §1).
- Recorded Dashboard boundary: the seven-workstream status directs finishing
  or preserving the B8 documentation decision and defining the
  documentation-only WP-D0 truth/permission/worker contract **before any new
  Dashboard product package** ([7WS] §3). Whether WP-D0 precedes or is folded
  into Package 3's Gate-1 scope record is an owner/Lead determination at
  dispatch.
- The broader Dashboard V2 architecture-gap inventory remains a read-only,
  unaccepted input, not a blueprint ([7WS] §3).

**Explicit prohibitions.** No ARM, order, config, credential, or live-worker
API changes ([BACKLOG] §4 Package 3). No VPS installation, public exposure,
phone control, login or tunnel deployment, worker-control API wiring,
embedded provider credentials, ARM/order controls, or trading-state changes
([7WS] §3). Market Context must remain context-only — any order-trigger use
escalates to T0 ([BACKLOG] §3). Fixture/mock data only; no live feeds.
Plus the general gating list above.

**Acceptance criteria.** Done means: (a) the prototype demonstrates the five
required views with fixture/mock data and zero live hooks (no live-worker
API, no real exchange data, no credential paths); (b) it runs entirely inside
its isolated worktree; (c) it passes one T1 review — single flagship reviewer
(alternating Claude/Codex), high effort, max 2 rounds, GLM-5.2 second opinion
only if findings are raised or the diff exceeds ~300 lines ([TIERS] §2).

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 3 (Dashboard V2 read-only prototype), tier T1,
      fixture/mock data only, isolated worktree only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 3; §3 Dashboard rows, HEAD citations)
  - MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_SEVEN_WORKSTREAM_STATUS_2026-08-17.md
    §3 (Dashboard boundaries and prohibited-now list)
  - MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_ARCHITECTURE_GAP_INVENTORY_2026-08-17.md
    (read-only inventory; unaccepted input, not a blueprint)
  - Existing V1 dashboard at IBKR_PAPER_BRIDGE/bridge/static/ (reference only)
OUTPUT: fixture/mock prototype inside <WORKTREE_PATH> only; nothing written
  outside that worktree.
CONSTRAINTS:
  - Fixture/mock data only. No live-worker API, no real exchange/market data,
    no credential access, no network calls to hosts or providers.
  - Build exactly: aggregate overview, per-worker drill-down, Market Context
    page, desired/accepted/exchange-truth views, phone-responsive monitoring.
  - Market Context is context-only; any order-trigger idea must be escalated
    in the report, not implemented.
  - No ARM/order/config/credential/live-worker API changes; no VPS install,
    public exposure, phone control, login/tunnels, or trading-state changes.
  - Do not touch the frozen V1 candidate or its soak lane.
REVIEW: T1 — one flagship reviewer (alternate Claude/Codex), high effort, max
  2 rounds; GLM-5.2 second opinion only if findings or diff > ~300 lines, per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list (all inside the worktree); (2) view-by-
  view completion table with the fixture source for each; (3) explicit
  statement of every live hook intentionally absent; (4) self-verification
  against the prohibited-now list in [7WS] §3.
```

---

### Package 4 — Owner analysis-package generator

**Scope.** Produce a bounded, redacted, read-only export for manual Codex
subscription analysis. No embedded API, provider credential, or AI authority.
([BACKLOG] §4 Package 4; §3 row "Dashboard AI assistance": initial route is a
manually supplied read-only package to the owner's Codex subscription,
embedded chat is deferred, and the package format is still open —
`docs/30...:1141-1154,1192-1216`, format open at `:1200-1212`, HEAD
citations.)

**Tier.** T1 ([BACKLOG] §4 Package 4; bounded read-only package generator
classified T1 in [BACKLOG] §3).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- Separate isolated worktree ([BACKLOG] §5 item 3).
- Open prerequisite to resolve inside the package: the export format is not
  yet fixed ([BACKLOG] §3, `docs/30...:1200-1212` HEAD citation). The Gate-1
  scope record should fix the format bounds or list format selection as the
  package's first deliverable.

**Explicit prohibitions.** No embedded API, provider credential, or AI
authority ([BACKLOG] §4 Package 4). No network calls to providers; the export
is delivered manually. No host contact. Embedded server chat is deferred and
excluded ([BACKLOG] §3). Plus the general gating list above.

**Acceptance criteria.** Done means: (a) the generator produces a bounded,
redacted, read-only export from local data with explicit size/content bounds
recorded; (b) the output contains no credentials or secrets (redaction
demonstrated on sample data); (c) no embedded API/provider capability exists
in the artifact; (d) passes one T1 review — single flagship, high effort, max
2 rounds, GLM-5.2 second opinion only if findings or diff > ~300 lines
([TIERS] §2).

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 4 (owner analysis-package generator), tier T1,
      bounded/redacted/read-only export, isolated worktree only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 4; §3 "Dashboard AI assistance" row, HEAD citations)
OUTPUT: generator code + one sample export inside <WORKTREE_PATH> only.
CONSTRAINTS:
  - Bounded: record and enforce explicit size and content limits.
  - Redacted: demonstrate secret/credential redaction on sample data.
  - Read-only and manual: no embedded API, no provider credentials, no AI
    authority, no network delivery; output is handed over as a file.
  - First deliverable: fix the package format (currently open per [BACKLOG]
    §3) or list it as the package's open decision with a recommendation.
  - No host contact, exchange/account actions, TESTNET/MAINNET, ARM/orders,
    Pine/parity/MTC changes, or frozen-V1 mutation.
REVIEW: T1 — one flagship reviewer, high effort, max 2 rounds; GLM-5.2 second
  opinion only if findings or diff > ~300 lines, per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list; (2) format-decision record; (3) bounds
  and redaction evidence table (input | bound applied | redaction check);
  (4) self-verification that no credential, API, or provider surface exists.
```

---

### Package 5a — Local observability toolkit (observational)

**Scope.** Audit/export pack, MockBroker chaos drills, and
readiness-checklist UI — purely observational/export/mock-UI mechanics. All
broker/exchange calls remain mocked. ([BACKLOG] §4 Package 5a; items originate
from the legacy roadmap deferrals at `docs/05_AUDIT_RESOLUTION.md:47-60`,
whose IBKR wording is historical (`:1-19`) so each item needs Hyperliquid
reverification — [BACKLOG] §3 row "V1.1 observability/operator tools".)

**Tier.** T1 ([BACKLOG] §4 Package 5a; read-only export/chaos/UI pieces
classified T1 in [BACKLOG] §3).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- Exists only because of the T2-required split of the former blanket-T1
  Package 5: the T2 review found the parity gauge cannot share a blanket T1
  label ([T2-STATUS] finding 3). Package 5a is the observational remainder;
  the gauge is Package 5b.
- Separate isolated worktree ([BACKLOG] §5 item 3).
- Hyperliquid reverification note: legacy roadmap wording predates the
  Hyperliquid migration, so each tool's assumptions must be checked against
  current reality as part of the work ([BACKLOG] §3).

**Explicit prohibitions.** All broker/exchange calls remain mocked — no real
feed, no real exchange, no credentials. Chaos drills run against MockBroker
only. Approvals, flip state machine, and any order-changing tools are
excluded: they are T0 under [BACKLOG] §3 and not part of 5a. Plus the general
gating list above.

**Acceptance criteria.** Done means: (a) the audit/export pack, MockBroker
chaos drill(s), and readiness-checklist UI operate purely
observationally/export/mock-UI with every broker/exchange call mocked;
(b) each tool's legacy assumptions are either confirmed or flagged for
Hyperliquid reverification; (c) passes one T1 review — single flagship, high
effort, max 2 rounds, GLM-5.2 second opinion only if findings or diff > ~300
lines ([TIERS] §2).

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 5a (local observability toolkit,
      observational), tier T1, mocked broker only, isolated worktree only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 5a; §3 "V1.1 observability/operator tools" row)
  - IBKR_PAPER_BRIDGE/docs/05_AUDIT_RESOLUTION.md:47-60 (legacy roadmap
    wording; historical IBKR framing per :1-19)
OUTPUT: toolkit code inside <WORKTREE_PATH> only.
CONSTRAINTS:
  - Scope: audit/export pack, MockBroker chaos drills, readiness-checklist
    UI. Nothing else from the legacy roadmap list.
  - Every broker/exchange call mocked; no real feed, exchange, or credential
    access; chaos drills target MockBroker only.
  - Approvals, flip state machine, and order-changing tools are OUT (T0 under
    [BACKLOG] §3); name them as excluded in the report.
  - Flag every legacy assumption needing Hyperliquid reverification instead
    of silently keeping it.
  - No host contact, TESTNET/MAINNET, ARM/orders, Pine/parity/MTC changes, or
    frozen-V1 mutation.
REVIEW: T1 — one flagship reviewer, high effort, max 2 rounds; GLM-5.2 second
  opinion only if findings or diff > ~300 lines, per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list; (2) tool-by-tool table (tool | purely
  observational? | mocked-call proof | legacy assumptions flagged); (3)
  excluded-T0-items list; (4) self-verification statement.
```

---

### Package 5b — Offline decision-parity gauge

**Scope.** The offline decision-parity gauge separated from the former
Package 5 by the T2-required split: the gauge touches parity semantics and
protected decision-logic inspection. ([BACKLOG] §4 Package 5b; [T2-STATUS]
finding 3.)

**Tier.** Reproduced from [BACKLOG] §4 Package 5b (no other tier may be
substituted in this draft):

> **Per-surface classification; separately owner-gated; no blanket tier.** The
> gauge touches parity semantics and protected decision-logic inspection, so it
> cannot carry a blanket T1 label. Under highest-risk-wins, each concrete
> surface must be classified before work: purely read-only export of
> already-recorded decision evidence may be **T1**; replay or inspection that
> touches parity semantics or protected decision logic is **T0**, named per
> surface and separately owner-gated.

**Depends on / gated by.**
- Per-surface classification must exist **before any work**, then a separate
  owner gate — the package starts only after both ([BACKLOG] §5 item 3;
  [T2-STATUS] finding 3).
- Each T0 surface is additionally gated per the standing rule that
  Pine/parity surfaces require separate owner authorization ([TIERS] §6).
- Separate isolated worktree ([BACKLOG] §5 item 3 with the general roadmap
  rule [BACKLOG] §1).

**Explicit prohibitions.** No work of any kind before the per-surface
classification and owner gate. No blanket T1 treatment. Replay/inspection
surfaces touching parity semantics or protected decision logic must not be
built without their own named T0 classification and separate owner approval.
No mutation of Pine, MTC, TradingView parity baselines, or strategy logic
(offline gauge only). Plus the general gating list above.

**Acceptance criteria.** Done means, per surface: (a) the classification
record names each concrete surface and its tier with the reason; (b) T1
surfaces (purely read-only export of already-recorded decision evidence)
pass one T1 review — single flagship, high effort, max 2 rounds, GLM-5.2
second opinion only if findings or diff > ~300 lines; (c) T0 surfaces pass a
T0 review — two independent flagships (`claude-opus-5` + Codex `gpt-5.6-sol`),
xhigh, max 3 rounds, audited immediately — and each carries its own owner
gate record ([TIERS] §2–§3; [BACKLOG] §4 Package 5b).

**Dispatch-prompt skeleton** (classification step only; build skeletons are
produced per surface after the owner gate).

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 5b STEP 0 (per-surface classification of the
      offline decision-parity gauge), documentation only, read-only repository.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 5b per-surface rule; §3 "V1.1 observability/operator tools" row)
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_T2_STATUS_2026-08-17.md
    (finding 3: no blanket T1)
OUTPUT: one classification record at <OUTPUT_PATH assigned by Lead>: an
  exhaustive list of the gauge's concrete surfaces, each labeled T1 (purely
  read-only export of already-recorded decision evidence) or T0 (replay or
  inspection touching parity semantics or protected decision logic), each
  with the reason and its evidence citations.
CONSTRAINTS:
  - Classification only; build no component of the gauge.
  - Highest-risk-wins: when a surface is mixed or unclear, classify it T0 and
    say why.
  - No mutation of Pine, MTC, parity baselines, or strategy logic.
  - UNKNOWN stays UNKNOWN; every claim cites its source.
  - No host contact, credentials, exchange/account actions, TESTNET/MAINNET,
    ARM/orders, or frozen-V1 mutation.
REVIEW: the classification record is a T2 documentation artifact — single
  reviewer, single round, medium effort per OWNER_DECISION_AUDIT_TIERS_2026-08-09.md
  §2. Each later build surface is reviewed at its own classified tier.
REPORT FORMAT: (1) changed-file list (one output file); (2) surface table
  (surface | T1/T0 | reason | citations | owner gate required?); (3)
  self-verification that no surface was left unclassified and none blanket-
  labeled.
```

---

### Package 6 — Shadow-mode split

**Scope.** First build fixture/file-fed MockBroker shadow mode as T1. Keep
real Hyperliquid feed attachment in a separate T0 package. ([BACKLOG] §4
Package 6; §3 row "Real-data shadow/ghost mode": fixture/local-feed
MockBroker prototype is T1, live Hyperliquid feed attachment is T0, deferral
recorded at `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md:756` and
`docs/05_AUDIT_RESOLUTION.md:47-52`.)

**Tier.** T1 for the local (fixture/file-fed MockBroker) half. The real-feed
half is **not** part of this tier: it is a separate T0 package with its own
authorization ([BACKLOG] §4 Package 6).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- Runs after/alongside Packages 3, 4, 5a in the fastest safe order
  ([BACKLOG] §5 item 4).
- Separate branch/worktree per the owner roadmap ([BACKLOG] §1).
- The real Hyperliquid feed half is separately gated: attaching it is T0 and
  touches TESTNET/exchange surfaces, which require explicit separate owner
  authorization ([BACKLOG] §4; [TIERS] §6).

**Explicit prohibitions.** For the T1 local half: no real Hyperliquid feed,
no live market data, no network calls to exchanges or hosts, no credentials,
no TESTNET/MAINNET, no ARM/orders. Fixture/file input only. The real-feed
attachment is excluded from this package entirely. Plus the general gating
list above.

**Acceptance criteria.** Done means: (a) shadow mode runs against a
fixture/file-fed MockBroker with zero live-data paths reachable; (b) the
real-feed attachment is explicitly documented as a separate future T0 package,
not stubbed into the T1 code path; (c) passes one T1 review — single flagship,
high effort, max 2 rounds, GLM-5.2 second opinion only if findings or diff >
~300 lines ([TIERS] §2).

**Dispatch-prompt skeleton** (T1 local half only).

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 6 LOCAL HALF (fixture/file-fed MockBroker shadow
      mode), tier T1, isolated worktree only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 6; §3 "Real-data shadow/ghost mode" row)
OUTPUT: shadow-mode prototype inside <WORKTREE_PATH> only.
CONSTRAINTS:
  - Fixture/file-fed MockBroker only. No real Hyperliquid feed, live market
    data, exchange/host network calls, or credential access.
  - The real-feed attachment is a SEPARATE future T0 package: do not build,
    stub, or precondition any live path here; record the split explicitly.
  - No TESTNET/MAINNET, ARM/orders, Pine/parity/MTC changes, or frozen-V1
    mutation.
REVIEW: T1 — one flagship reviewer, high effort, max 2 rounds; GLM-5.2 second
  opinion only if findings or diff > ~300 lines, per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list; (2) data-path proof that every input is
  fixture/file and no live path is reachable; (3) the recorded T0 split
  statement for the real-feed half; (4) self-verification statement.
```

---

### Package 7 — Official exchange reverification

**Scope.** Verify current subaccount, agent-wallet, same-symbol netting,
margin-mode, and API-limit facts before V2 architecture relies on them.
Package 1's exchange-dependent decisions are explicitly conditioned on this
package's output. ([BACKLOG] §4 Package 7; §3 row "Subaccounts and
same-symbol isolation": official-document verification is read-only T2 and
must precede any freeze of these decisions; account, wallet, exchange, and
broker work is T0.)

**Tier.** T2, read-only ([BACKLOG] §4 Package 7).

**Depends on / gated by.**
- Owner authorization + Gate-1 scope record (this draft grants neither).
- First in the fastest safe order: its output gates every
  exchange-dependent decision below ([BACKLOG] §5 item 1).
- The unaccepted public-docs addendum exists as input **leads only**; it does
  not replace Package 7 and authorizes nothing
  ([ADDENDUM-UNACCEPTED] "Authority" and §4).

**Explicit prohibitions.** Read-only verification from official public
documentation only (the addendum's method — live public-docs reads with zero
account, API-key, wallet, login, or exchange actions — is the precedent;
[ADDENDUM-UNACCEPTED] header). No account-level checks: exchange verification
through account actions is on the prohibited-now list ([7WS] §1). Where only
an account-level check can answer a question, the record must say so and mark
that part separately owner-gated (see below). No SDK calls, no endpoints, no
credentials, no host contact, no TESTNET/MAINNET, no ARM/orders, and no
freezing of any Package 1 decision (freezing belongs to Package 1, after this
record exists). Plus the general gating list above.

**Acceptance criteria.** Done means: (a) a verification record listing every
required claim (subaccount eligibility and volume gate, agent-wallet
behavior, same-symbol netting/hedge mode, margin mode, API limits) with, per
claim, the official source (URL plus quoted sentence), and a status of
VERIFIED / UNKNOWN / ACCOUNT-LEVEL-ONLY; (b) every UNKNOWN stays UNKNOWN
rather than being filled from third-party or stale sources; (c) every
ACCOUNT-LEVEL-ONLY item is listed under its own future owner gate with the
note that account/wallet/exchange work is T0 ([BACKLOG] §3); (d) the record
passes one T2 review — single reviewer, single round, medium effort
([TIERS] §2).

**Package 7 note — addendum findings are LEADS TO VERIFY, not facts.**
Everything in this subsection comes from the unaccepted addendum
([ADDENDUM-UNACCEPTED]) and must be re-verified by Package 7 from official
documentation before V2 relies on it:

- **Sub-account volume gate (high-impact lead).** The official sub-accounts
  page reportedly states: up to 10 sub-accounts can be created after reaching
  $100,000 in volume; one additional sub-account per additional $100M
  volume, up to 50; sub-accounts share the master's fee tiers without
  referral discounts; API wallets start at 3 per master and increase by 2
  per sub-account ([ADDENDUM-UNACCEPTED] §2.1). Implication recorded in the
  addendum (a consideration, not a decision): a fresh or low-volume account
  has zero sub-accounts until $100k cumulative volume, so Package 1 must
  treat subaccount availability as conditional with an explicit fallback.
- **Same-symbol netting / hedge mode: officially UNKNOWN.** No official
  sentence was found on whether one account can hold simultaneous long and
  short positions on the same asset; third-party sources describe one-way
  netting per account with sub-accounts as the workaround, but that is not
  official. This stays UNKNOWN until Package 7 verifies it from official
  documentation — or, if only an account-level check can settle it, the
  record says so and that part is separately owner-gated
  ([ADDENDUM-UNACCEPTED] §3.1).
- **Agent/API wallets (lead).** Reportedly: masters approve API wallets to
  sign for the master or its sub-accounts; sub-accounts have no private
  keys; nonces are per signer with a 100-highest-nonces window and a
  (T − 2 days, T + 1 day) validity band; separate API wallets per
  sub-account are recommended; wallets can expire, be pruned, or be
  deregistered ([ADDENDUM-UNACCEPTED] §2.2).
- **Margin modes (lead).** Reportedly: cross margin is the default, isolated
  is supported, some assets are strict isolated; leverage is 1 to the
  asset's max (3x–40x per the perpetual-assets page); maintenance margin is
  half of initial at max leverage; HIP-3 DEXs have a no-cross mode. Whether
  cross and isolated positions can coexist on one asset is **not addressed**
  — UNKNOWN ([ADDENDUM-UNACCEPTED] §2.3, §3.3).
- **API rate limits (lead).** Reportedly: IP-based aggregated weight 1200/min
  with per-request weights; WebSocket caps of 10 connections, 30 new
  connections/min, 1000 subscriptions, 2000 messages/min; address-based
  limits treat **sub-accounts as separate users**, with volume-accrued
  request budget and a 10,000-request initial buffer
  ([ADDENDUM-UNACCEPTED] §2.4).
- **TESTNET parity: UNKNOWN.** Whether the sub-account volume gate,
  API-wallet counts, and rate limits apply identically on testnet is not
  stated in the fetched pages ([ADDENDUM-UNACCEPTED] §3.2).
- **The actual account's eligibility: account-level only.** The cumulative
  volume of the account in use is an account fact, not a documentation
  fact; only a separately gated account-level check may establish it, and
  account/wallet/exchange/broker work is T0 ([ADDENDUM-UNACCEPTED] §3.4;
  [BACKLOG] §3).

**Dispatch-prompt skeleton.**

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 7 (official exchange reverification), tier T2,
      read-only, public official documentation only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 7; §3 subaccounts row; §5 item 1)
  - MTC_COMMAND_CENTER/11_TRIAGE/HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md
    (UNACCEPTED supplemental; its findings are LEADS to verify, not facts)
OUTPUT: one verification record at <OUTPUT_PATH assigned by Lead>.
CONSTRAINTS:
  - Verify from current official Hyperliquid documentation only (live public
    page reads). No account, API-key, wallet, login, or exchange actions; no
    SDK calls; no endpoints; no credentials; no host contact.
  - Required claims: subaccount eligibility incl. the $100k volume gate and
    per-$100M scaling; agent/API-wallet behavior incl. nonce rules and
    lifecycle; same-symbol netting / hedge mode; margin modes incl.
    cross+isolated coexistence; API limits incl. IP-based, WebSocket, and
    address-based treatment of sub-accounts; TESTNET parity of all of the
    above where stated.
  - Third-party or stale sources never upgrade a claim to VERIFIED.
  - UNKNOWN stays UNKNOWN. Where only an account-level check could answer,
    mark ACCOUNT-LEVEL-ONLY and list it under a separate future owner gate
    (account/wallet/exchange work is T0 per [BACKLOG] §3).
  - Freeze no architecture decision; Package 1 consumes this record later.
REVIEW: T2 — single reviewer, single round, medium effort (GLM-5.2 preferred;
  DeepSeek acceptable; flagship at medium only if neither available) per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2.
REPORT FORMAT: (1) changed-file list (one output file); (2) claim table:
  claim | status VERIFIED/UNKNOWN/ACCOUNT-LEVEL-ONLY | official source URL |
  exact quoted sentence(s); (3) addendum-lead reconciliation (each §2/§3
  addendum lead: confirmed, corrected, or still unknown); (4) explicit
  owner-gate list for ACCOUNT-LEVEL-ONLY items; (5) self-verification that no
  account or network action beyond public documentation reads occurred.
```

---

### Package 8 — Protected V2 implementation packages

**Scope.** Multi-worker supervisor, Guardian, storage migration, account
routing, sizing validation, Multi-TP/baskets, event/funding gate, additional
broker, and remote authenticated controls may be designed locally, but must
not be merged into or activate the frozen V1 candidate without their normal
contracts and acceptance. ([BACKLOG] §4 Package 8.)

**Tier.** T0, isolated only ([BACKLOG] §4 Package 8).

**Depends on / gated by.**
- Per-work-package owner authorization: no blanket start; the owner
  authorizes each small T0 work package individually (this draft's charter;
  [BACKLOG] §5 item 5 "split into small T0 work packages and audit each
  immediately").
- Each work package must name the accepted upstream artifact it implements —
  the backlog classifies contract design as T2 and official verification
  (Package 7) as preceding protected implementation: multi-worker
  architecture contract T2 before cross-cutting implementation; MTC
  lifecycle/intent contracts T2 before order/broker/risk implementation;
  subaccount/account routing dependent on Package 7 verification
  ([BACKLOG] §3 rows "Multi-strategy workers", "MTC exit lifecycle...",
  "Subaccounts and same-symbol isolation").
- Isolation: separate branches/worktrees; never the frozen V1 candidate or
  its soak lane ([BACKLOG] §1, §4 Package 8, §5 item 6).
- Standing separate authorizations that nothing here waives: WP-V, KVM2
  production deployment, master merge, credential loading, broker/exchange
  access, ARM, orders, TESTNET/mainnet, any economic action ([TIERS] §6).

**Explicit prohibitions.** No merge into or activation of the frozen V1
candidate without the work package's normal contracts and acceptance
([BACKLOG] §4 Package 8). Keep schema activation, deployment, TESTNET
execution, remote exposure, MAINNET, and any economic control off the V1
soak lane ([BACKLOG] §5 item 6). No master merge, credential loading,
broker/exchange access, ARM, orders, TESTNET/mainnet, or economic action
without explicit separate owner authorization ([TIERS] §6). No Pine, MTC,
TradingView-parity, or strategy-logic changes; no VPS/host contact; no
trading-state mutation ([7WS] §8).

**Acceptance criteria.** Done, per work package, means: (a) the work package
was individually owner-authorized with its own Gate-1 scope record naming the
T0 tier and the upstream accepted contract it implements; (b) the work stayed
inside its isolated worktree and did not touch the frozen V1 candidate or
soak lane; (c) it was audited **immediately** on completion — T0: two
independent flagships (`claude-opus-5` + Codex `gpt-5.6-sol`), xhigh effort,
max 3 rounds ([TIERS] §2–§3); (d) no merge, activation, or deployment
occurred — those remain separately authorized steps ([BACKLOG] §4 Package 8;
[TIERS] §6).

**Dispatch-prompt skeleton** (generic template; one per authorized work
package).

```
DRAFT — DO NOT DISPATCH WITHOUT OWNER AUTHORIZATION
ROLE: Implementer for Package 8 WORK PACKAGE <WP-ID: name>, tier T0, isolated
      worktree only.
INPUTS (read-only):
  - MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md
    (§4 Package 8; §5 items 5-6; the §3 rows covering this capability)
  - <UPSTREAM_ACCEPTED_CONTRACT: exact path of the accepted T2 contract or
    Package 7 verification record this work package implements>
  - MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISION_AUDIT_TIERS_2026-08-09.md
OUTPUT: implementation inside <WORKTREE_PATH> only; nothing written outside
  it; no merge, no activation, no deployment.
CONSTRAINTS:
  - Implement only <WP-ID scope> as frozen in its Gate-1 scope record; any
    scope growth stops work and returns to the owner.
  - Isolated worktree only; the frozen V1 candidate and its soak lane are
    untouchable.
  - No master merge, credential loading, broker/exchange access, ARM,
    orders, TESTNET/MAINNET, VPS/host contact, remote exposure, or economic
    action; each requires separate explicit owner authorization
    (OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §6).
  - No Pine/MTC/parity/strategy-logic changes; UNKNOWN stays UNKNOWN; every
    claim cites its source.
REVIEW: T0, immediate on completion — 2 independent flagships
  (claude-opus-5 + Codex gpt-5.6-sol), xhigh, max 3 rounds, per
  OWNER_DECISION_AUDIT_TIERS_2026-08-09.md §2-§3.
REPORT FORMAT: (1) changed-file list (all inside the worktree); (2) scope-
  conformance table (Gate-1 scope item | delivered | evidence); (3) explicit
  statement of what was NOT done (merge/activation/deployment/credential/
  exchange/ARM/order surfaces); (4) self-verification statement.
```

## 3. Fastest safe order recap

Reproduced verbatim from [BACKLOG] §5 — do not reorder:

1. Start **Package 7** first. Its read-only official Hyperliquid verification
   gates every exchange-dependent decision below.
2. Complete **Package 2** and the non-exchange-dependent part of **Package 1**
   (worker identity, store model, Guardian veto semantics) in parallel with
   Package 7. The exchange-dependent subset of **Package 1** — subaccount
   eligibility/fallback, agent-wallet behavior, same-symbol netting, margin
   mode, API limits, and the worker-boundary and feed-topology choices — is
   **CONDITIONED ON Package 7 output** and must not be frozen before that
   verification is on record.
3. Run **Packages 3, 4 and 5a** in separate isolated worktrees; they are the
   highest-value non-economic work that can progress without touching V1.
   **Package 5b** starts only after its per-surface classification and owner
   gate (see Package 5b).
4. Run the local-only half of **Package 6**.
5. Split **Package 8** into small T0 work packages and audit each immediately.
6. Keep schema activation, deployment, TESTNET execution, remote exposure,
   MAINNET and any economic control off the V1 soak lane.

This order uses the VPS testing period productively while preserving a clean
boundary: **V1 proves the frozen candidate; V2 work proceeds separately and
cannot change what is being tested.** ([BACKLOG] §5, closing paragraph.)

## 4. Draft status

- This file is an unaccepted kickoff-prep draft. It prepares but does not
  start any package, and it contains no authorization language by design.
- No package may be dispatched from the skeletons above until the owner has
  given that package its own explicit authorization and a Gate-1 scope record
  with tier classification exists for it.
- All UNKNOWNs cited above remain UNKNOWN; nothing in this draft resolves
  them.
- Exactly one file was produced by this task: this file, written outside the
  repository. The repository was read-only for this task; no repo file,
  branch, commit, stage, push, or worktree state was modified.
