# Bridge V2 Deferral Backlog — T2 Acceptance Record — 2026-08-17 (overnight)

**Artifact class:** T2 review acceptance record
**Candidate:** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`
**Candidate identity (reviewed bytes):** SHA-256
`026FC5421D1B17BCC4941D623FF88BAD6A2D8BF0E635DD0BC5D0DAB1F97B5004`
(hash of the exact working-copy bytes as reviewed — LF line endings as authored; computed via
`Get-FileHash` and independently reproduced by the reviewer via `certutil`.)
**Pinned git blob OID (unambiguous under `* text=auto`):** `f0115b0a88e7d1c00e7b8cc54c3e9182eba1fab6`
(a future CRLF working-tree checkout will produce a different byte hash; the blob OID is the
durable identity.)
**Verdict:** **ACCEPT**

## Authorization chain

1. First T2 round (fresh `gpt-5.6-sol`, medium) returned REQUEST_CHANGES with 3 required
   findings + 3 optional nits; one-round cap consumed
   (`BRIDGE_V2_DEFERRAL_BACKLOG_T2_STATUS_2026-08-17.md`).
2. Owner, asked directly in chat on 2026-08-17 evening, authorized exactly one narrow fresh T2
   review of a corrected candidate (`OWNER_DECISIONS_BRIDGE_V2_BACKLOG_NIGHT_2026-08-17.md`,
   Decision 1).
3. Both authorized Codex Plus routes proved credit-exhausted at dispatch time; the owner, asked
   again immediately, chose **GLM-5.3 as the official T2 reviewer** (Decision 4; policy basis:
   AGENTS.md GLM supplemental routing — GLM may fill a T2 reviewer slot; documentation-only
   review, no execution required).

## Review identity

- Reviewer: **fresh GLM-5.3 session** (Z.AI Coding Plan via `glm.ps1`; isolated per-invocation
  `CLAUDE_CONFIG_DIR`), read-only, single round, dispatched 2026-08-17 late evening.
- Review specification: `C:\tmp\night\official_t2_review_prompt.md` (hash-pinned candidate;
  findings verification + fresh whole-document pass + citation reproduction required).
- The reviewer computed the candidate hash itself and reported
  `IDENTITY: 026fc542... MATCH` before reviewing.

## Independence disclosure (recorded honestly)

- The corrected candidate was **authored** by a GLM-5.3 session (implementer sub-delegation under
  the Claude Lead; counterpart Codex flagship unavailable — surfaced to owner in real time).
  Author and official reviewer share model/account but ran as separate isolated sessions.
- Cross-provider mitigation before the official round:
  - **DeepSeek `deepseek-v4-pro`** doc-level pre-review: PREREVIEW_PASS (all findings ADDRESSED;
    two trivial wording items, both fixed before the official round; full report at
    `C:\tmp\ds_backlog_prereview_report.md`, transcript included).
  - **Claude Lead (Fable)** independently reproduced the load-bearing code citations
    (`bridge/store/db.py:263-267,523-524`, `bridge/app.py:108`) before accepting the authored text.
  - **Gemini 3.7 Flash read-only route was unavailable**: its owner-accepted launcher hard-pins
    branch `feature/donchian-crypto-ladder` (launcher line 764) and the repo is on
    `codex/bridge-help-wiki`. Not bypassed; recorded as an owner-ask instead.

## Verdict summary (full reviewer output preserved verbatim below)

- FINDING-1 (partial-fill overstatement): **RESOLVED** — row reads as opt-in v5 source capability,
  inert on default v4, migration/activation and acceptance UNKNOWN; every cited line reproduced.
- FINDING-2 (Package 7 before exchange-dependent Package 1 decisions): **RESOLVED** — identical
  conditioned set across Package 1, Package 7, Section 5, and the Section 3 subaccounts row.
- FINDING-3 (Package 5 blanket T1): **RESOLVED** — 5a (T1 observational) / 5b (per-surface,
  T0 escalation, separately owner-gated) consistent across all three locations.
- NITS 1–3: all RESOLVED.
- FRESH-PASS FINDINGS: **none**. 16 citation spot-check groups verified at the pinned HEAD
  `033546fb...` per the candidate's (HEAD) citation convention.
- Non-blocking nits recorded by the reviewer: (1) the "six pages" phrasing is HEAD-accurate but
  the live tree's accepted Help map adds a seventh page — extend the HEAD convention to
  `index.html` in a future revision; (2) rows 72/73 use explained non-taxonomy labels — future
  normalization optional.

## What this acceptance means — and does not mean

The backlog inventory and package sequencing are now an **accepted T2 documentation record**.
It still authorizes **nothing**: no Package 1–8 kickoff, no implementation, schema migration,
activation, merge of protected surfaces, VPS/host contact, credentials, exchange account actions,
TESTNET/MAINNET, ARM/orders, or Pine/parity/MTC changes. Every package start requires its own
owner authorization and Gate-1 scope record.

---

## Full reviewer output (verbatim)

```
IDENTITY: 026fc5421d1b17bcc4941d623ff88bad6a2d8bf0e635dd0bc5d0dab1f97b5004 MATCH

FINDING-1: RESOLVED
Row 54 now reads as opt-in v5 source capability, inert on default v4, with migration/activation
and acceptance UNKNOWN. All cited evidence reproduced read-only, exactly:
- bridge/store/db.py:263-267 — SCHEMA_VERSION_BASELINE = 4 ("Default target"),
  SCHEMA_VERSION_PARTIAL_FILL = 5 ("opt-in, never automatic").
- db.py:523-524 — initialize(target_schema_version: int = SCHEMA_VERSION_BASELINE) (default = 4).
- db.py:620 — if target_schema_version >= SCHEMA_VERSION_PARTIAL_FILL: self._migrate_v4_to_v5()
  (migrated only on explicit target ≥5).
- db.py:3073-3079 — partial_protection_enabled() is version-≥5 and explicitly still true on v6.
- bridge/app.py:108 — store.initialize() with no target argument.
- docs/25:17-18 — "Status: PROPOSED — implemented and self-QA'd offline; pending independent
  audit and owner acceptance. Not deployed"; docs/25:349-354 — "On a v4 database every TS-P1-004
  path is inert… A separate, approved deployment gate must… wire the v5 target".
- docs/26:2-4 ("nothing in this contract is active on a v4 or v5 runtime database"), :395-396,
  :413-415, :427-429 — all support the row verbatim.
UNKNOWN is preserved with anchor citations (T2_STATUS:41,45, both verified). The closing sentence
("not active, not accepted, and not available under the default runtime schema") is fully
evidence-grounded. Not cosmetic.

FINDING-2: RESOLVED
Package 7 now precedes or explicitly conditions every exchange-dependent Package 1 decision,
consistently in all four required locations: Package 1 (§4: worker boundary, feed topology,
subaccount fallback "and every decision that depends on exchange behavior (subaccount
eligibility, agent-wallet behavior, same-symbol netting, margin mode, API limits)" are
"CONDITIONED ON Package 7 output… freeze waits for Package 7's official verification record");
Package 7 (§4: "Package 1's exchange-dependent decisions are explicitly conditioned on this
package's output"); Section 5 (item 1 starts Package 7 first because it "gates every
exchange-dependent decision below"; item 2 restates the identical conditioned subset, including
worker-boundary and feed-topology choices); Section 3 subaccounts row ("Official-document
verification is read-only T2 and must precede any freeze of these decisions (Package 7)"). The
exchange-dependent set is identical across all four locations; no location freezes exchange
behavior from stale assumptions.

FINDING-3: RESOLVED
No blanket T1 remains on Package 5. Package 5a (§4, T1) is purely observational/export/mock-UI
mechanics with all broker/exchange calls mocked; Package 5b carries "Per-surface classification;
separately owner-gated; no blanket tier" with T0 escalation "named per surface and separately
owner-gated" under highest-risk-wins. Consistent in Section 3 observability row ("the
decision-parity gauge is classified per-surface with T0 escalation, separately owner-gated
(Package 5b)") and Section 5 item 3 ("Package 5b starts only after its per-surface classification
and owner gate").

NITS-1/2/3:
- NIT-1 (HEAD-citation convention): RESOLVED — §1 lines 18-26 declare the (HEAD) convention
  pinned to 033546fb… for all docs/30 and NEXT_STEPS.md citations, anchored to T2_STATUS:6 and
  :43; I verified all such citations against git show 033546fb… and none against the dirty
  working copy.
- NIT-2 (direct funding citation): RESOLVED — row 64 now cites docs/26:2-4,46,261-279,374 for
  the FUNDING capture component / append-only funding_events ledger of the opt-in v6 contract
  (all four ranges verified: :46 FUNDING component, :261-279 userFunding capture, :374
  "append-only" ledger), and :421-422,527-530 for "not consumed by risk" (both verified
  verbatim).
- NIT-3 (label normalization): RESOLVED — every §3 classification cell uses an exact §2
  category; the three hybrids/outliers (rows 71, 72, 73) carry explicit explanations rather than
  silent category mixes.

FRESH-PASS FINDINGS: none

Full-document pass found no overstated capability claim, no uncited factual claim, no internal
contradiction, no authorization creep (the Authority banner holds everywhere; Packages 3/4/5a/6-
local stay T1 read-only/mock with no ARM/credential/live-API authority; Package 8 and all
activation/host/TESTNET/MAINNET/economic surfaces stay T0-gated; Package 7 is read-only
official-document verification with no exchange/host/account contact), and no UNKNOWN-erasure
(row 54, row 71 reverification, row 72 re-triage, and Package 7's existence all preserve
uncertainty). All 20 cited docs/30 ranges and both NEXT_STEPS.md ranges verified at the pinned
HEAD (see spot-checks).

CITATION SPOT-CHECKS:
1. docs/30(HEAD):131-164 — "one VPS / one shared release with isolated workers" preferred:
   SUPPORTS (row 56).
2. docs/30(HEAD):203-254 — same-symbol concurrency "stays closed" pending subaccount
   confirmation/virtual-book validation and netting reverification: SUPPORTS (row 57).
3. docs/30(HEAD):376-407 — sizing-ownership contract must be resolved "before any MTC-to-Bridge
   integration, including a single-worker one": SUPPORTS (row 60 "must precede even the first
   MTC-connected worker").
4. docs/30(HEAD):944-973 — "Only frozen, approved packages may be prepared… never ARMs and never
   trades": SUPPORTS (row 68).
5. docs/30(HEAD):1141-1154,1192-1216,1200-1212 — manual read-only package via owner's Codex
   subscription, embedded chat deferred, package format open: SUPPORTS (row 70).
6. docs/01_ARCHITECTURE.md:747-751,755-764 — adopted-into-v1 list, Manual Ticket, shadow mode,
   funding gate, Market Context, Binance, Postgres+Redis+Docker deferral, login/2FA: SUPPORTS
   (rows 52, 59, 62-66, 69).
7. bridge/app.py:158-174,149-154,191-208,98-103,234 — one engine/Keltner/RiskEngine,
   single-runtime exposure thresholds, Mock-or-Hyperliquid-testnet BTC 1x, loopback bind:
   SUPPORTS (rows 51, 58, 66, 69).
8. bridge/engine/engine.py:62,114 + llm_gate.py:29 + config/bridge.yaml:39-50 +
   NEXT_STEPS(HEAD):83-92 — NullLLMGate fallback, LLMGate class, switches OFF,
   dormant-scaffolding truth correction: SUPPORTS (row 55).
9. requirements.in:26-35 — full direct-dependency list contains no Postgres/Redis/Docker:
   SUPPORTS (row 59).
10. docs/05:47-60 + :1-19 — v1.1 deferral table ("not v1"), advanced-proposals line 60,
    IBKR-wording-historical note: SUPPORTS (rows 63, 71, 72).
11. docs/00_PREREG.md:35-40,105-108 + docs/03_STATUS.md:148-156 — P3 ≥30 days post-P2, v1
    out-of-scope list: SUPPORTS (rows 66, 69, 73).
12. docs/27:1-17, docs/28:1-15,44-49, docs/29:1-19 — opt-in v6/v7/v8, default v4, no operational
    migration/activation: SUPPORTS (row 53).
13. docs/30 dirty-edit claim "89 inserted lines plus cross-reference changes" — git diff
    --numstat vs current HEAD: 89 insertions, 11 deletions: SUPPORTS exactly.
14. NEXT_STEPS(HEAD):7-20,68-71 — V2 work only in separate branches/worktrees under normal audit
    tiers: SUPPORTS (§1).
15. T2_STATUS:6,41,43,45 — pinned HEAD, no acceptance record located, dirty docs/30 + AI-memory
    copies, UNKNOWN discipline: SUPPORTS.
16. bridge/static/index.html:12-18,21-106 — six pages + ARM/DISARM controls: SUPPORTS at pinned
    HEAD 033546fb (110-line file); see NIT 1 below for the live-tree caveat.

NITS (non-blocking):
1. Row 67 "Current V1 has six pages and controls" (and row 68's "current six-page UI") is
   accurate at the pinned reviewed HEAD, but the live committed tree has changed since: the
   accepted Help-map feature (commit d71bc073, after 033546fb) adds a seventh nav page ("Help /
   System Map", index.html:18 working copy), and NEXT_STEPS(HEAD):86-87 itself frames the
   dashboard as "six original pages plus Help". The §1 HEAD convention covers only docs/30 and
   NEXT_STEPS.md; a future revision should extend it to index.html (or note the Help page). No
   effect on any classification, tier, or authorization in the document.
2. Rows 72 ("Candidate ideas, not accepted backlog requirements") and 73 ("Pending, not a V2
   feature") use labels outside the §2 taxonomy. Both are explicitly explained and are not
   category mixes, so they satisfy the nit-3 standard; a future normalization could still map
   them to §2 language (e.g., "Separate future gate" / "Explicitly deferred") or add them to §2
   as named non-categories.

VERDICT: ACCEPT
```
