# WP-P0-29 VEN-C — Treasury Policy Draft

**Status:** SIGNED/ACCEPTED · policy only · T2
**Signed by owner Barış, 2026-08-25.**

**Date:** 2026-08-25

**Hard boundary:** No purchase, wallet, credential, deposit, transfer, venue contact, account action, testnet/mainnet action or trade is created or authorized here. Proposed numbers are owner-amendable policy values, not live-readiness evidence or financial advice.

## 1. Authority and scope

This policy implements the five treasury principles settled in #42 and carried by the [WP-P0-29 contract](../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md#wp-p0-29--ven-c--wallet-custody-and-treasury-policy-new-2026-08-23-wayfinder-fold-tickets-42-and-48). The [custody runbook](CUSTODY_RUNBOOK_DRAFT.md) governs keys and credential boundaries. The [venue due-diligence record](VENUE_DUE_DILIGENCE_RECORD.md) governs whether a first mainnet deposit may even be considered.

Only the owner may authorize a treasury movement. An AI, worker, dashboard, notification, scheduler or automatic sweep may never initiate or approve one.

## 2. Five principles — signable proposal summary

| # | Required principle | Concrete proposal for owner signature | Current status |
|---:|---|---|---|
| 1 | Minimize venue balance; define sweep threshold | Define the **Operating Float** as the owner-signed capital required for the next **7 calendar days**. Review daily at **20:00 UTC**. When flat and reconciled, if free venue balance exceeds **120%** of Operating Float, owner manually sweeps the excess down to **100%**. No automatic sweep. | Proposed; no balance or transfer exists/was read |
| 2 | Owner-only, master-key-only manual transfers with address verification | Use the **Owner Manual Transfer Procedure** in §4: hardware master signer only; approved address book; full address/network/asset verification in two independent views; first-use test transfer; reconciliation before any remainder. | Named procedure proposed; never executed |
| 3 | Least trust on agent keys | Until a primary source and later permission proof establish a narrower boundary, treat each agent wallet as able to move or economically endanger **100% of funds reachable through its binding**. Keep distinct wallets per bucket/worker and fund no binding above its owner-signed cap. | Binding policy; venue boundary remains unverified |
| 4 | Written USDC-depeg stance | Use the objective watch/DISARM/emergency/recovery thresholds in §6. No automatic sale, transfer or FLATTEN. | Proposed thresholds; no market action authorized |
| 5 | Twelve-criterion venue due diligence | Owner reviews and signs the twelve-criterion record **before first mainnet deposit**, refreshes it every **90 days**, and triggers an event review within **1 business day** of a material incident/change. | Record drafted; current proposed disposition is HOLD |

## 3. Operating Float and venue-balance minimization

### 3.1 Required signed inputs

Before any mainnet deposit, the owner separately signs:

- `Operating Float amount: [AMOUNT AND UNIT]`;
- `Pilot capital cap: [AMOUNT AND UNIT]` — must remain consistent with the separate live-gate capital signature;
- `Loss-at-stop cap: [LOWER AMOUNT AND UNIT]` — never inferred from the pilot cap; and
- `Applicable risk buckets: [IDS]`.

The relative 120% sweep trigger is concrete, but it does not invent the owner's capital amount. An empty amount field blocks funding.

### 3.2 Daily procedure

1. At 20:00 UTC, an authorized read-only process may prepare a redacted balance/reconciliation report; it cannot move funds.
2. No sweep is considered unless all positions are flat, owned orders are absent, reconciliation is clean, the destination is approved, and the owner is present with the hardware master signer.
3. If free venue balance is greater than 120% of the signed Operating Float, the proposed sweep amount is `free balance - 100% of Operating Float`.
4. The owner performs §4 manually. If any check is uncertain, stop; do not reduce the amount to make the check easier.
5. A venue halt, withdrawal restriction, USDC event, unexplained balance or incident suspends routine sweeping and moves to incident handling.

No bot, cron job, worker or agent key may sweep.

## 4. Owner Manual Transfer Procedure

This is a named future procedure, not an executed action.

### 4.1 Preconditions

- owner authorization identifies source, destination, network, asset, exact amount, purpose and evidence record;
- hardware master signer and trusted display are available; no agent wallet signs a treasury transfer;
- source is flat/reconciled and the transfer will not impair margin, protection or a recovery action;
- destination is in the owner-approved address book with provenance and approval date; and
- no incident, depeg hold, stale venue record or failed custody check is open.

### 4.2 Address verification

1. Verify asset and network by their full canonical names, not ticker alone.
2. Display the complete destination on the hardware signer's trusted screen.
3. Compare the **entire address**, character by character, against two independent owner-controlled views of the approved address-book record. First/last-character checks alone are forbidden.
4. Confirm address-book provenance, destination owner, network and any memo/tag requirement.
5. For a first-use or changed destination, impose a **24-hour cooling period**, then send the smallest venue/network-permitted test transfer that is economically reasonable under a separately approved execution scope.
6. Confirm finality and reconcile source/destination before separately authorizing any remainder.
7. Record only public transaction ID, public addresses, amount, network, purpose, timestamps, approvals and reconciliation result. Record no secret.

Any mismatch, clipboard substitution, unsupported network, stale address, uncertain destination control or unexpected fee stops the procedure.

## 5. Least-trust agent-wallet rule

The merged [WP-P0-28 binding spec](../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md#3-preferred-subaccount-mode) explicitly does not claim an agent-withdrawal safety boundary. Therefore:

- every agent wallet is modeled as capable of losing or moving 100% of funds accessible through its account/subaccount binding;
- no claim such as “agents cannot withdraw” may reduce controls until a dated primary-source record and later permission proof establish it;
- a distinct wallet is required per live bucket/worker, with no cross-stage or cross-bucket reuse;
- accessible balance must not exceed the bucket's owner-signed capital cap;
- unexpected permission or binding behavior auto-DISARMS the affected scope, alerts the owner and blocks new risk; and
- owner-controlled master custody remains offline and separated from routine execution.

## 6. USDC-depeg stance

### 6.1 Reference rule

The trigger price is the median USDC/USD price from at least **two independent, liquid public markets** selected in the separately approved monitoring design. A single stale venue, one anomalous print or the project's own venue alone cannot clear or trigger recovery. If fewer than two sources are fresh, status is UNKNOWN and new risk is DISARMED until the owner resolves it.

### 6.2 Proposed thresholds and named actions

| State | Trigger | Required action |
|---|---|---|
| `USDC_WATCH` | Median below **$0.9975 for 15 continuous minutes**, or a credible issuer/reserve/redemption warning | Alert owner; increase checks to every 5 minutes; block treasury deposits and non-essential transfers; prepare reconciled exposure report. Existing risk is not automatically changed. |
| `USDC_DISARM` | Median below **$0.9900 for 5 continuous minutes**, or confirmed redemption/settlement impairment | Auto-DISARM new risk in affected scopes; suspend routine sweeps/deposits; owner reviews venue protection, positions and exit options. No automatic KILL or FLATTEN. |
| `USDC_EMERGENCY` | Any fresh median below **$0.9700**, or issuer redemption halt, venue USDC withdrawal halt, or credible reserve/custody compromise | Page owner immediately. Owner alone chooses KILL, FLATTEN, venue-side action, hold, or a separately authorized manual transfer based on current exposure. Preserve evidence and reconcile. |
| `USDC_RECOVERY_REVIEW` | Median at or above **$0.9975 for 24 continuous hours**, redemption and venue transfer functions publicly reported normal, and reconciliation clean | Owner may begin a written recovery review. No automatic re-ARM; live eligibility returns only through the canonical gate. |

These thresholds manage operational response; they do not predict USDC value or guarantee an exit.

## 7. Venue due-diligence cadence

The owner reviews the [venue record](VENUE_DUE_DILIGENCE_RECORD.md):

- before the first mainnet deposit;
- every **90 calendar days** thereafter while the venue remains in scope;
- within **1 business day** of a security incident, material outage, withdrawal/deposit restriction, terms/jurisdiction change, API/agent-wallet policy change, stablecoin impairment or accepted evidence invalidation; and
- before any venue replacement, additional master-account topology or material capital increase.

An expired or event-invalidated review blocks new deposits and new risk. UNKNOWN is recorded honestly; it is not silently converted to PASS.

## 8. Exceptions, review and evidence

- There are no automatic exceptions. An owner-approved exception states exact scope, reason, duration, compensating control and expiry.
- All treasury movements require post-action reconciliation and an append-only non-secret record.
- A failed address check, unexplained balance, custody uncertainty, depeg state or stale due diligence stops the act.
- This policy is reviewed every 90 days with the venue record. Superseding versions are added; signed history is never edited away.

## 9. Owner decision and signature

| Proposal | Accept / amend |
|---|---|
| Operating Float = next 7 days; daily review 20:00 UTC; sweep above 120% down to 100% | `[INITIAL / AMENDMENT]` |
| Owner Manual Transfer Procedure, including full-address two-view verification, 24-hour first-use cooling and test transfer | `[INITIAL / AMENDMENT]` |
| Agent wallet modeled as able to endanger 100% of reachable funds until proved otherwise | `[INITIAL / AMENDMENT]` |
| USDC thresholds/actions in §6 | `[INITIAL / AMENDMENT]` |
| Venue review every 90 days and event review within 1 business day | `[INITIAL / AMENDMENT]` |

**Owner name:** `[PRINT NAME]`

**Owner signature:** `[SIGNATURE]`

**Signed date/time and timezone:** `[YYYY-MM-DD HH:MM TZ]`

**Effective policy version:** `[VERSION]`

**Amendments, if any:** `[ATTACH SIGNED AMENDMENT; NO SECRETS]`
