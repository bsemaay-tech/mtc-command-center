# LEAD_TERMINAL — WP-P0-28 read-only own-account ELIGIBILITY capture, run `p028-eligibility-20260915-r1` — 2026-09-15 08:31-08:33Z

**Authority:** `OD-20260915-P028-READ-GO-1` (owner "P028 read go", ~08:29Z). **Result: attempt 1 REFUSED by the tool (by design), attempt 2 CAPTURE_OK + CAPTURE_VERIFY_OK. Evidence class: NONACCEPTING real observation** (the wrapper is Lead-written today and unreviewed; it reuses the reviewed capture tool `af921d75` for every custody primitive; roster review pending).

## Ownership evidence
Owner signed the fixed message (address lower-cased + `run_id: p028-eligibility-20260915-r1`) with his wallet on the reviewed page (`b43dbe39…`, served on `127.0.0.1:8791` for the signing minutes, server stopped after). Signature `sig_r1.txt` (132 bytes, sha256 `86c0110f…`, public data). Verified by the tool BEFORE any network object: `OWNERSHIP_EVIDENCE: VERIFIED`, recovered `0x1E26…AC49`.

## What ran (wrapper `capture_own_account_eligibility.py`, sha256 `d817b141…`; reviewed tool sha256 `00b3b8f6…` asserted before use; `HL_API_WALLET_KEY` removed from the child environment)
Four public Info reads for the owner's mainnet address, each twice: `subAccounts`, `userFees`, `userRole`, `clearinghouseState` (`https://api.hyperliquid.xyz`, SDK 0.24.0); original bytes write-once + sha256 sidecars + manifest (`raw_bytes_source: http_response_content` on all 8). No key, no order, no sub-account creation, no transfer.
- **Attempt 1 (`r1/`, 08:31:52-59Z): REFUSED `CAPTURE_REFUSED_REQUERY_MISMATCH user_fees`** — the two `userFees` passes differed ONLY in `dailyUserVlm[2026-09-15].exchange` (the exchange-wide daily volume: `1957883672.14` → `1957932162.61`); every user-scoped field was identical. Correct refusal under the strict rule; 16 page files kept as evidence, no manifest written.
- **Wrapper amended** (re-query comparison masks the venue-wide `exchange` field only; both passes' bytes still stored; rule recorded in the derived view as `requery_rule`). **Attempt 2 (`r1_attempt2/`, 08:32:41-45Z): CAPTURE_OK**, `--verify-existing` → `CAPTURE_VERIFY_OK`; `SHA256SUMS_r1_attempt2.txt`.

## Evidence (derived view `DERIVED_ELIGIBILITY_VIEW.json`; every value re-locatable in the original bytes)
| Field | Value (2026-09-15 08:32Z) |
|---|---|
| `userRole.role` | `user` (a master account, not a sub-account) |
| `subAccounts` | `null` → **0 sub-accounts** |
| `dailyUserVlm` rows returned | 15 (2026-09-01 … 2026-09-15) |
| user volume in the returned window | **$91.28** = `userCross` $78.74 + `userAdd` $12.54, all on 2026-09-14 (matches the Path 1 fills: taker 0.00042 BTC ≈ $33 + close 0.00058 ≈ $45.8; maker 0.00016 ≈ $12.5); every other day 0.0 |
| fee tier | `userCrossRate 0.00045` (4.5 bps taker), `userAddRate 0.00015` (1.5 bps maker), `activeReferralDiscount 0.04`, staking discount 0, `trial` null |
| account state | `assetPositions` 0, `withdrawable 0.0` |

## Lead reading against the rule (`hyperliquid-docs/trading/sub-accounts`, accessed 2026-09-15: "Up to 10 sub-accounts can be created after reaching $100,000 in volume")
**NOT ELIGIBLE today** for sub-accounts: 0 sub-accounts exist and the account's volume in the 15-day window the API returns is $91.28 — ~0.09 % of the $100,000 threshold. The API's `userFees` exposes only the trailing daily window, not a lifetime cumulative figure; the account shows no volume before 2026-09-14 in that window, and the owner declared Sunday's fills as his first. A lifetime figure above $100k is therefore implausible but not proven by this read — recorded as `UNKNOWN (lifetime)`, `NOT ELIGIBLE (windowed evidence)`.

**Material consequence (the owner's follow-up note asked to be told only if capacity creates a material choice):** it does. The Q6 default topology (one sub-account + own agent wallet per risk bucket) cannot be instantiated on this account now; the binding spec's **virtual-book fallback** (one account, bucket accounting in the Bridge's ledger) is the applicable mode until the account reaches the venue threshold — no re-decision of the policy is needed, the spec already defines the fallback. The owner may still choose to route future volume through this account to reach the threshold, but that is a trading/volume decision outside this packet.

**Side evidence for WP-P0-12 C-10 (fee tier):** this capture is the first dated, owner-attested fee-rate evidence for the real account (`0.00045` / `0.00015` with a 4 % referral discount). `OD-20260914-P012-ADMISSION-Q3` ("Wait") stands: the Lead records it, declares nothing; the P0-12 Lead lane decides how it enters C-10 with the funding-interval coverage.

## Records and next
- This dir → CT13 `QUEUED_PACKAGES_20260915/P028_ELIGIBILITY_CAPTURE_20260915/` (both attempts, wrapper, log, checksums, signature, this record).
- Roster: the wrapper + capture join the P1CAP tool's review chain (exact Opus Wed queue may take it as an addendum; exact Sol Sep 19; Gemini delta of the wrapper when convenient). Row `s` of the 2026-08-25 venue record moves from EXCLUDED to "captured 2026-09-15, NOT ELIGIBLE (windowed), NONACCEPTING" once reviewed.

Recorded by Claude Opus 5 Lead (743291).
