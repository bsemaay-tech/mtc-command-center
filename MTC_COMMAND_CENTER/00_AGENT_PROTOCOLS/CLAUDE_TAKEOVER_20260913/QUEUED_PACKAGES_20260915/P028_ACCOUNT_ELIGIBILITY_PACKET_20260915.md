# WP-P0-28 — account-eligibility evidence packet (prepared 2026-09-15; NOT executed)

Prepared by the Claude Opus 5 Lead (session 743291) on the owner's 2026-09-12 queue decision (Codex ad-hoc notes `20260912-221906-p028-ai-work-queue.md` / `…-owner-followup.md`). Everything below is preparation; the read described in §4 is the owner-side `G6` / T0 step the venue record excludes — it runs only on the owner's explicit one-line word.

## 1. Existing record — reused, provenance verified
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md` (+ `ACCOUNT_BINDING_AND_FALLBACK_SPEC.md`, `LANE_REPORT.md`), integrated by merge `6d1136a9` ("WP-P0-28 venue-fact verification + Q6 binding specs, doc half (lane T, T2 2026-08-25)"). 16 rows VERIFIED with primary-source quotes; 4 UNKNOWN: `j` (same-asset cross+isolated), `r` (testnet sub-account gate), `s` (this account's eligibility — ACCOUNT-LEVEL-ONLY), `t` (customer-configurable IP restriction). No new review of the documentation half is necessary: the record is T2-accepted and its facts are re-read today (§2) without contradiction.

## 2. Bounded public-source check (2026-09-15, official docs, read-only)
| Question | Result | Source (accessed 2026-09-15) |
|---|---|---|
| Sub-account eligibility rule unchanged? | **VERIFIED, unchanged:** "Up to 10 sub-accounts can be created after reaching $100,000 in volume. Every additional $100M in volume enables the ability to create 1 additional sub-account, up to a maximum of 50 sub-accounts." | https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts |
| Testnet exemption or parity for the $100k gate (row `r`)? | **UNKNOWN (re-confirmed):** the sub-accounts page and the testnet-faucet page contain no testnet statement at all. | same page; https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/testnet-faucet |
| Is there a read-only, credential-free way to see an address's sub-accounts, volume and role? | **VERIFIED:** the public Info endpoint documents `{"type":"subAccounts","user":<address>}` → `name`, `subAccountUser`, `master`, `clearinghouseState`, `spotState`; `{"type":"userFees","user":<address>}` → `dailyUserVlm`, `feeSchedule`, `userCrossRate`, `userAddRate`, `activeReferralDiscount`; `{"type":"userRole","user":<address>}` → `role` (+ `data`). No key, no signature, no authenticated endpoint. | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint |
| Rows `j` (same-asset mixed margin) and `t` (IP allow-listing) | **not revisited** — no supported capability in the current design depends on them (the binding spec fails closed on both); the P0-29 deep-research request (Section D2/D5) carries the same questions to a second pass, so the two records will be reconciled once. | — |

Consequence: the "authenticated account-eligibility read" of the 2026-08-25 record can be performed as a **read-only public-address read with the owner's ownership signature**, exactly like the Path 1 capture of 2026-09-15 — no credential, no order, no venue write. It is still the owner's step (his address, his attestation, his authorization), and it is still T0 for that step.

## 3. What the owner confirms first (one line each)
1. **Account and network:** the same mainnet address used for Path 1 (`0x1E26…AC49`) is the address the Bridge binding would use — YES / another address. (Testnet has no sub-account gate evidence; a testnet read cannot answer the mainnet eligibility question.)
2. **Authorization of the read:** "P028 read GO" authorizes ONE read-only capture of `subAccounts`, `userFees`, `userRole` (+ `clearinghouseState`) for that address, with the ownership signature over a fresh run_id (`p028-eligibility-<date>-r1`), stored write-once with sidecars like the Path 1 capture. Nothing else.

## 4. The read, exactly (prepared; not run)
- Tool: the reviewed capture pattern (`IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` at `af921d75`) extended by a small **read-only sibling** `capture_own_account_eligibility.py` that issues only the three Info calls above (same `CapturingInfo` bytes capture, sidecars, manifest with `raw_bytes_source`, ownership signature verified first, `HL_API_WALLET_KEY` refusal). Building the sibling is a bounded builder task (Codex after Sep 19, or the Lead on an owner "A"); until then the three calls can be captured with the existing tool's `account_state_query` pattern by hand — the Lead prefers the sibling so the evidence has the same custody chain.
- Fields the packet needs, dated: `userRole.role` (master or sub-account), the list of existing sub-accounts (count, names, addresses), `userFees.dailyUserVlm` (per-day volume history → cumulative 14-day and lifetime sums computed in the derived view, both labelled DERIVED), the fee tier (`userCrossRate`, `userAddRate`), `activeReferralDiscount`, and the account state (positions, withdrawable) for context.
- Acceptance condition of the evidence (not of the package): `OWNERSHIP_EVIDENCE: VERIFIED` for the address; two passes byte-identical; the derived cumulative volume compared against the **$100,000** rule with the result stated as one of: ELIGIBLE (≥ $100k, sub-account count < 10), NOT ELIGIBLE (< $100k), or ALREADY PROVISIONED (sub-accounts exist). The number itself is evidence; the eligibility statement is the Lead's reading and stays NONACCEPTING until the roster reviews the capture.
- Date/window: point-in-time read; `dailyUserVlm` history as returned (the API decides the depth — record it).

## 5. Downstream mapping (specification, not implementation)
| Concern | Downstream package | Status |
|---|---|---|
| Registry of bound accounts / sub-accounts and agent wallets (identities, expiry ≤ 180 d, rotation) | WP-V2B-03 (Bridge multi-account binding) — prerequisite: accepted P0-28 spec + this eligibility evidence | spec exists (`ACCOUNT_BINDING_AND_FALLBACK_SPEC.md`); evidence pending |
| Sub-account routing per risk bucket; virtual-book fallback when sub-accounts are not eligible | WP-V2B-03 | design settled (Q6); fallback normative in the spec |
| Virtual-book accounting and reconciliation (one account, several buckets) | WP-P0-12 consumers / reconciliation package | depends on the P0-12 research/paper route |
| Universe enforcement (#48 policy) | WP-V2B-03 admission fixtures + WP-P0-21 | specified, not built here |
Nothing in this packet starts those implementations.

## 6. NOT VERIFIED / open
- Row `r` stays UNKNOWN (no testnet statement exists in the official docs read today).
- Rows `j`, `t` deferred to the P0-29 second pass.
- The actual account numbers — until the owner authorizes the read.
