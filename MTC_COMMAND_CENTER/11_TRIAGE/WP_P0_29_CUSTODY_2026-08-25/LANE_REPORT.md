# Lane Z Report — WP-P0-29 VEN-C Custody and Treasury Policy

**Date:** 2026-08-25

**Lane:** Z

**Role:** Codex implementer under Claude Lead

**Audit tier:** T2 — owner-signable policy documents

**Status:** IMPLEMENTER DRAFT PACKAGE COMPLETE; OWNER SIGNATURE AND LEAD ACCEPTANCE PENDING

## 1. Scope and authority result

Created only new Markdown policy files under `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/`.

No credential, seed, private key, wallet, account, purchase, deposit, transfer, venue contact, authenticated read, host contact, testnet/mainnet action, trade, deployment, Pine/parity/MTC/Bridge/schema change or push occurred. Public internet research was not needed because merged WP-P0-28 and WP-P0-24 records supplied the required evidence.

## 2. Deliverables

1. `CUSTODY_RUNBOOK_DRAFT.md`
   - hardware master-wallet generation ceremony design;
   - proposed metal storage medium and two owner-filled physical-location placeholders;
   - loss/recovery paths;
   - empty-wallet restore drill design, explicitly not performed and required before first mainnet deposit;
   - preferred and standalone-second-master-account fallback topology;
   - agent-wallet generation/storage/rotation policy;
   - full map-#96 credential-lifecycle boundary;
   - live-gate precondition-11 mapping; and
   - sealed incapacity pointer-sheet template with no keys.
2. `TREASURY_POLICY_DRAFT.md`
   - all five #42 principles with concrete proposed numbers or named procedures;
   - owner-only manual transfer/address-verification procedure; and
   - objective USDC watch/DISARM/emergency/recovery proposals.
3. `VENUE_DUE_DILIGENCE_RECORD.md`
   - all twelve O-16 criteria adapted to Hyperliquid;
   - citations to merged WP-P0-28/WP-P0-24 records;
   - honest PASS/PARTIAL/UNKNOWN/BLOCK dispositions;
   - blocking closure register and 90-day/event-driven refresh proposal.
4. `LANE_REPORT.md`
   - implementer self-QA and handoff evidence.

## 3. Venue facts and proposals carried correctly

- WP-P0-28 verifies a custom agent-wallet expiry no more than 180 days in the future and documents no default. The runbook therefore proposes explicit 120-day expiry, planned rotation by day 90, and warnings at 30/14/7/1 days.
- Agent withdrawal restriction is not primary-source established; the policy treats agent wallets as able to move or economically endanger 100% of reachable funds.
- Customer-configurable IP allowlisting is UNKNOWN. Per-IP rate limiting is not represented as an IP restriction.
- Actual account eligibility and testnet volume-gate behavior remain UNKNOWN/EXCLUDED.
- None of these documentation outcomes is represented as execution evidence or live readiness.

## 4. Implementer self-QA against WP-P0-29 acceptance gate

| Acceptance requirement | Self-QA result |
|---|---|
| Every precondition-11 item maps to a runbook section or explicit venue-mapping difference | **PASS at draft level:** `CUSTODY_RUNBOOK_DRAFT.md` §9 maps all five original items and map-#96 subproofs. Withdrawal-disabled and IP-restricted are explicitly UNSATISFIED venue differences. |
| Five treasury principles each have a concrete proposed number or named procedure | **PASS:** 7-day Operating Float; daily 20:00 UTC check; sweep above 120% down to 100%; Owner Manual Transfer Procedure; 100% least-trust exposure; USDC thresholds; 90-day/1-business-day review cadence. |
| Due-diligence record covers all twelve O-16 criteria | **PASS:** criteria 1–12 are present individually, with evidence, disposition and closure. |
| Custody runbook covers ceremony, medium, two locations, recovery, restore drill, agent lifecycle | **PASS at design level:** all named sections present; two locations remain deliberate owner-filled off-repo placeholders. |
| Restore drill proven before first mainnet deposit | **NOT CLAIMED / CORRECTLY DEFERRED:** design only; first mainnet deposit remains blocked until a separately authorized drill is accepted. |
| Calendar rotation proposed against verified venue expiry | **PASS:** 120-day explicit expiry and day-90 rotation are tied to WP-P0-28's verified 180-day maximum/no-default fact. |
| Credential lifecycle boundary per map #96 | **PASS at policy level:** absolute stage separation, least privilege, one secret road, audited lifecycle, warnings, revocation drill design and compromise response are explicit. |
| Sealed incapacity one-pager and fallback topology carried from full package | **PASS at draft level:** pointer-only no-key template and separately authorized second-master variant are present. |
| Owner-signable | **PASS at draft level:** each policy/record includes initial/amend fields and owner signature block. |
| Owner signature on the set | **PENDING — FINAL ACCEPTANCE ACT.** The implementer cannot perform or claim it. |

## 5. Mechanical QA recorded before commit

- branch/base preflight: `feature/wp-p0-29-custody-policy-20260825` at `6d1136a9108656c7f8bf811a4a5247268452c7a2`;
- `git diff --cached --check`: **PASS**;
- exact-path verification: **PASS** — exactly the four intended new files staged, with no unstaged/untracked remainder;
- local Markdown link-path audit: **PASS**;
- structural scan: **PASS** — 12 due-diligence criterion rows and 5 treasury-principle rows;
- required boundary/expiry/mapping terms scan: **PASS**;
- credential/secret-shaped value scan: **PASS** — no candidate secret value or 64-hex private-key shape found; and
- final commit SHA: intentionally not embedded in the commit that defines it; emitted by Git and handed to the Lead after commit.

## 6. Acceptance handoff

Owner signature is the final package acceptance act. This implementer deliverable is a signable set of drafts, not an owner signature, an independent T2 review, live-gate evidence or permission to execute any procedure.

The Claude Lead owns independent T2 review, acceptance, any repair round, and Gate-7 handoff updates. This implementer report claims only self-QA.

## 7. Exact intended commit paths

1. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md`
