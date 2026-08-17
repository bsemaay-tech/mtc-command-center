# Package 7 — Official Exchange Reverification Record (T2, read-only)

**Date:** 2026-08-17 (night) · **Implementer:** GLM-5.3 (sub-delegated; per Gate-1 scope record)
**Artifact:** Package 7 verification record — T2, read-only, documentation only.
**Gate-1 scope:** `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE7_EXCHANGE_REVERIFICATION_2026-08-17.md`
(owner-authorized start 2026-08-17 night, Decision 5).
**Accepted demand:** `BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` §4 Package 7, §3 row
"Subaccounts and same-symbol isolation".
**T2 review slot (per Gate-1):** one reviewer, one round, medium effort — DeepSeek (`deepseek-v4-pro`).

**Method:** official Hyperliquid documentation pages, live-fetched by the Claude Lead on
2026-08-17 (two collection passes). The evidence is the Lead's preserved quote dump at
`C:\tmp\night\p7_official_quotes_dump.md` — the ONLY source of official-page evidence used here.
The implementer performed ZERO account, API-key, wallet, login, SDK, endpoint, or host actions,
and no web/network access of any kind. Repositories were read-only. Third-party sources NEVER
upgrade a claim to VERIFIED; none were used (the dump's explicitly forbidden third-party
netting consensus is nowhere cited as evidence).

## 0. Conventions used in this record

- Statuses are exactly the three mandated values: **VERIFIED** (official evidence exists in the
  dump), **UNKNOWN** (the official pages fetched do not establish it), **ACCOUNT-LEVEL-ONLY**
  (only an account action could answer; separately owner-gated, T0).
- Evidence levels, tagged on every quote (all evidence text below is copied character-exact
  from the dump — never paraphrased):
  - **[V]** = sentence the dump marks as a verbatim quote from the official page (quoted text
    inside the dump's bullets).
  - **[E]** = the dump's page-extraction text (the Lead's fetch-tool extraction of the official
    page, not marked verbatim in the dump).
- VERIFIED requires dump evidence from an official page. Where a row's only evidence is [E]
  (no [V] sentence exists in the dump), the row says so explicitly; a verbatim-sentence
  confirmation pass (still T2, docs-only) is recommended before any Package 1 freeze that leans
  on those exact numbers.
- Where a single claim bundles sub-scopes with different evidence (c, r — and one residual note
  in l), the status is given per sub-scope; no fourth status is introduced.

## 1. Claim table

| # | Claim | Status | Official source | Evidence (exact dump text; [V] = verbatim official sentence, [E] = dump page-extraction) |
|---|---|---|---|---|
| a | Sub-account creation eligibility (volume gate, counts, scaling) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts | [V] "Up to 10 sub-accounts can be created after reaching $100,000 in volume" · [V] "Every additional $100M in volume enables the ability to create 1 additional sub-account, up to a maximum of 50 sub-accounts" |
| b | Sub-account fee treatment | **VERIFIED** | same page (D1) | [V] "Sub-accounts share the same fee tiers as the master account, but referral discounts do not apply to sub-accounts" |
| c | Sub-account clearinghouse/margin treatment (incl. under portfolio margin) | **VERIFIED** (sub-scope: under portfolio margin) · **UNKNOWN** (general clearinghouse/margin treatment of sub-accounts outside portfolio margin) | portfolio-margin page (D7); sub-accounts page (D1) | [V] "Sub-accounts are still treated separately under portfolio margin." · Negative evidence [E] (D1): "Page does NOT address: technical creation steps, transfer rules, margin/clearinghouse treatment, testnet vs mainnet differences." Dump gap 5: "Sub-account margin/clearinghouse treatment details beyond D7's 'treated separately': limited." |
| d | API-wallet counts per master and per sub-account | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts (D1) | [V] "The number of API wallets available starts at 3 for all master accounts and increases by 2 per sub-account" · [E] (D2): "No explicit total API-wallet limit stated ON THIS PAGE (but see D1's count rule)." The quote expresses a master-account quota that grows +2 per sub-account; no separate independently-sized per-sub-account quota is stated. |
| e | API-wallet signing authority for sub-accounts (no private keys, vaultAddress) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets (D2) | [V] "A master account can approve API wallets to sign on behalf of the master account or any of the sub-accounts" · [V] "It's recommended to use separate API wallets for different subaccounts" · [E] "Sub-accounts do not have private keys; actions for a sub-account are signed by the master (or an approved API wallet) with the vaultAddress field set to the sub-account address." |
| f | API-wallet nonce rules (per-signer tracking, 100-nonce window, validity band) | **VERIFIED** | same page (D2) | [V] "Nonces are tracked per signer, which is the user address if signed with private key of the address, or the agent address if signed with an API wallet" · [V] "The 100 highest nonces are stored per address" · [E] validity band: "nonces must fall within (T - 2 days, T + 1 day) of block timestamp" |
| g | API-wallet lifecycle (expiry, pruning, deregistration, regeneration guidance) | **VERIFIED** | same page (D2) | [V] regeneration guidance: "Generate a new agent wallet on future use to avoid unexpected behavior" · [E] "Removal scenarios: unnamed wallet deregistered when a new unnamed one is approved; wallets can expire; wallets pruned when the registering account no longer has funds." |
| h | Same-symbol netting / hedge mode (simultaneous long+short on one asset) | **UNKNOWN** | pages fetched that fail to establish it: margining (D4), perpetual-assets (D5) | Negative evidence [E] (D4): "Page does NOT address: cross+isolated coexistence on one asset; simultaneous long and short (hedge mode)." · [E] (D5): "Page does NOT discuss position netting, one-position-per-asset, opposing orders reducing positions, or hedge mode." · Dump gap 1: "Same-symbol netting / hedge mode: no official sentence found (third-party consensus says one-way netting per account; NEVER cite that as VERIFIED)." No official sentence exists in the dump; the third-party consensus is NOT evidence and is NOT cited as such. |
| i | Cross vs isolated margin defaults and strict-isolated assets | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining (D4) | [V] "Cross margin is the default, which allows for maximal capital efficiency by sharing collateral between all other cross margin positions." · [V] "Isolated margin is also supported, which allows an asset's collateral to be constrained to that asset." · [V] "Some assets are strict isolated, which functions the same as isolated margin with the additional constraint that margin cannot be removed." |
| j | Cross+isolated coexistence on the same asset | **UNKNOWN** | margining page (D4) | Negative evidence [E] (D4): "Page does NOT address: cross+isolated coexistence on one asset; simultaneous long and short (hedge mode)." Dump gap 2: "Cross+isolated coexistence on the same asset: not addressed." |
| k | Account abstraction modes and their operational limits (50k actions/day etc.) | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes (D6) | [V] Unified Account: "single balance for each asset. This balance collateralizes all cross margin positions in that asset and is unified with spot balance in that asset" · [V] Portfolio Margin: "single portfolio unifying all eligible assets, which are currently HYPE, BTC, USDC, USDT" · [V] Manual/Standard: "separate perp and spot balances, separate DEX balances. Cross margin applies to each DEX separately" · [V] "Builder code addresses must be in standard mode to accrue builder fees" · [V] "Portfolio margin and unified account are limited to 50k user actions per day. Standard mode has no such restrictions." · [V] API note (on unified/portfolio-margin modes): "all balances and holds in the spot clearinghouse state. Individual perp dex user states are not meaningful." · [E] "DEX Abstraction (discontinued)" |
| l | Portfolio margin status, eligibility thresholds, sub-account treatment | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/portfolio-margin (D7) | [V] "Under portfolio margin, a user's spot and perps trading are unified for greater capital efficiency." · [V] "Sub-accounts are still treated separately under portfolio margin." · [V] described as "a generalization of cross margin" · [V] access fragments: ">$5M in weighted volume or account value >$10k" and "<$25M" · [E] "plus supply/borrow caps" · Residual UNKNOWN (noted, not a row split): "No explicit alpha/live designation on the page." |
| m | Leverage ranges and maintenance-margin rule | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/perpetual-assets (D5) + margining (D4) | [V] "Max leverage varies by asset, ranging from 3x to 40x. Maintenance margin is half of the initial margin at max leverage." · [V] "Leverage can be set by a user to any integer between 1 and the max leverage. Max leverage depends on the asset." |
| n | IP-based REST rate limits and weights | **VERIFIED** | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits (D3) | [V] "aggregated weight limit of 1200 per minute" · [E] "exchange request weight `1 + floor(batch_length / 40)`; info weights 2 / 20 / 60 by type; per-item surcharges ("additional rate limit weight per 20 items returned"; candleSnapshot per 60 items); explorer weight 40" (the fragment "additional rate limit weight per 20 items returned" is [V]) |
| o | WebSocket connection/subscription/message limits | **VERIFIED** (evidence level: [E] only — no verbatim sentence preserved in the dump) | same page (D3) | [E] "max 10 connections; 30 new connections/min; 1000 subscriptions; 10 unique users across user-specific subscriptions; 2000 messages/min sent; 100 inflight posts" |
| p | Address-based limits and sub-accounts-as-separate-users treatment | **VERIFIED** | same page (D3) | [V] "sub-accounts treated as separate users" · [V] "1 request per 1 USDC traded cumulatively" · [V] "initial buffer of 10000 requests" · [E] "throttled to one request per 10 seconds when limited" |
| q | Open-order and cancel allowances | **VERIFIED** (evidence level: [E] only — no verbatim sentence preserved in the dump) | same page (D3) | [E] "cancels `min(limit + 100000, limit * 2)`; open orders 1000 + 1 per 5M USDC volume, cap 5000" |
| r | TESTNET parity of the above (base URL, faucet, whether gates/limits differ) | **VERIFIED** (sub-scope: base URL + faucet mechanics, [E] only) · **UNKNOWN** (whether the sub-account volume gate, API-wallet counts, or rate limits differ on testnet) | https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/testnet-faucet + https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api (D8) | [E] "Testnet faucet requires a mainnet deposit on the same address; claims 1,000 mock USDC at app.hyperliquid-testnet.xyz/drip." · [E] "API: same requests work against testnet base URL `https://api.hyperliquid-testnet.xyz` (mainnet: `https://api.hyperliquid.xyz`)." · [E] "NOT stated anywhere fetched: whether the sub-account volume gate, API-wallet counts, or rate limits differ on testnet." |
| s | The actual trading account's cumulative volume / current sub-account eligibility | **ACCOUNT-LEVEL-ONLY** | n/a — not a documentation fact | Dump gap 4: "The actual trading account's cumulative volume / sub-account eligibility: account fact — ACCOUNT-LEVEL-ONLY by definition." Answerable only by an account-level check under its own future owner gate (T0). No such action was performed. |

**Row tally (19 rows):** VERIFIED 16 · UNKNOWN 2 (h, j) · ACCOUNT-LEVEL-ONLY 1 (s).
Sub-scope caveats inside VERIFIED rows: c general sub-account margin/clearinghouse treatment and
r testnet parity of gates/limits remain UNKNOWN; l carries a noted residual UNKNOWN
(alpha/live designation). Evidence level: 13 of the 16 VERIFIED rows carry at least one
dump-marked verbatim official sentence; rows o and q (and r's VERIFIED sub-scope) rest on
[E] extraction text only.

## 2. Implications for Package 1 (advisory only — freezes nothing)

Package 1's exchange-dependent Section-B subset (backlog §4 Package 1, §5 item 2: subaccount
eligibility/fallback, agent-wallet behavior, same-symbol netting, margin mode, API limits,
worker-boundary and feed-topology choices) is conditioned on this record. This section informs;
all freeze decisions remain with Package 1's own gate.

**Now informed by VERIFIED facts:**
- Subaccount-per-worker isolation is **conditional by design**: sub-accounts are volume-gated
  (10 after $100k; +1 per $100M; cap 50 — row a). The one-risk-bucket-per-subaccount model in
  `docs/30` cannot be assumed available; a fallback (e.g. virtual books under one account) must
  stay a first-class design branch until the actual account's gate status is established (row s).
- Agent-wallet pattern is documentation-aligned (rows d, e, f, g): master-level wallets
  (baseline 3, +2 per sub-account), master-approved signing on behalf of sub-accounts,
  recommended separate API wallets per sub-account, per-signer nonce tracking with a 100-nonce
  window, and a wallet lifecycle (expiry/pruning/deregistration + regenerate-on-reuse) that
  belongs in the worker-identity contract.
- Margin-mode defaults (rows i, m): cross is the exchange default; isolated and strict-isolated
  exist; leverage is 1..asset-max (3x–40x) with maintenance margin = half of initial at max
  leverage — relevant to any per-worker margin-mode and leverage-cap specification.
- Mode ceilings (rows k, l): portfolio margin and unified account are capped at 50k user
  actions/day; standard mode is not; sub-accounts remain separate under portfolio margin; PM
  eligibility is threshold-gated (" >$5M in weighted volume or account value >$10k", "<$25M").
- API-limit topology (rows n, o, p, q): the IP-based 1200/min weight budget and the WebSocket
  10-connection / 1000-subscription caps are shared per IP (a real shared constraint for a
  single-VPS multi-worker topology), while address-based budgets treat sub-accounts as separate
  users — per-worker address-level isolation gains budgets, but the IP-level budget and WS
  connection cap must be shared/planned across workers.

**Still blocked on UNKNOWNs (not freezable from this record):**
- Same-symbol netting / hedge mode (h) — same-symbol concurrency stays closed pending verified
  exchange mechanics and subaccount or virtual-book proof (backlog §3).
- Cross+isolated coexistence on one asset (j).
- General sub-account margin/clearinghouse treatment beyond "treated separately under portfolio
  margin" (c, general sub-scope).
- TESTNET parity of the volume gate, wallet counts, and rate limits (r) — testnet-derived
  evidence cannot be assumed to transfer to mainnet gates/limits.

**ACCOUNT-LEVEL-ONLY (each listed under its own future owner gate, T0):**
- The actual account's cumulative volume → current sub-account eligibility and current wallet
  count (row s).
- Any supervised account-level check of same-symbol behavior (h) should the documentation dig
  stay dry — per the addendum, only such a separately gated check could resolve it.

## 3. Addendum reconciliation (each lead in `HYPERLIQUID_PUBLIC_DOCS_VERIFICATION_ADDENDUM_2026-08-17.md`)

- §2.1 Sub-accounts volume-gated (quotes + conditional-availability implication, testnet-UNKNOWN
  preserved): **confirmed** — all four D1 sentences appear verbatim in the dump; testnet gate
  remains UNKNOWN.
- §2.2 API wallets (signing, nonces, lifecycle, separate-wallet recommendation): **confirmed** —
  D2 verbatim sentences cover signing authority, per-signer nonces, the 100-nonce store and the
  separate-wallet recommendation; the (T − 2 days, T + 1 day) band and the removal scenarios are
  present in the dump at [E] extraction level (substance confirmed, evidence level noted).
- §2.3 Margin modes (cross default, isolated, strict isolated, leverage 1..max, 3x–40x,
  maintenance = half initial at max, HIP-3 no-cross, coexistence/hedge not addressed):
  **confirmed** — D4/D5 verbatim; both "not addressed" notes remain accurate.
- §2.4 API rate limits (1200/min IP weight, request weights, WS limits, address-based treatment,
  accrual/buffer/throttle, cancel and open-order allowances; shared-IP/shared-WS implication):
  **confirmed** — "aggregated weight limit of 1200 per minute" and "sub-accounts treated as
  separate users" verbatim; the remaining numbers confirmed at [E] extraction level.
- §3.1 Same-symbol netting / hedge mode UNKNOWN: **still unknown** — no official sentence in the
  dump; third-party consensus correctly excluded.
- §3.2 TESTNET parity of gates/counts/limits: **still unknown** — explicitly "NOT stated
  anywhere fetched".
- §3.3 Cross+isolated coexistence on one asset: **still unknown** — D4 explicitly does not
  address it.
- §3.4 Current account's own eligibility: **still unknown** from documentation; classified
  ACCOUNT-LEVEL-ONLY in this record (account fact; own future T0 owner gate).

## 4. Self-verification

- Every VERIFIED claim above carries dump evidence text copied character-exact from
  `C:\tmp\night\p7_official_quotes_dump.md`, never paraphrased. 13 of the 16 VERIFIED rows are
  anchored by at least one dump-marked verbatim official sentence; the rows that rest on dump
  page-extraction text only (o, q, and r's VERIFIED sub-scope) are explicitly flagged as such
  inline.
- Every claim not backed by dump text is labeled UNKNOWN or ACCOUNT-LEVEL-ONLY (rows h, j, s;
  plus the flagged sub-scopes of c and r and the residual note in l). UNKNOWN stays UNKNOWN.
- Third-party material (the one-way-netting consensus) appears only as a forbidden non-source
  named in negative evidence; it never upgrades any claim to VERIFIED.
- No account, API-key, wallet, login, SDK, endpoint, host, or network action of any kind was
  performed by the implementer; repositories were treated as read-only; the only file written is
  this record.
