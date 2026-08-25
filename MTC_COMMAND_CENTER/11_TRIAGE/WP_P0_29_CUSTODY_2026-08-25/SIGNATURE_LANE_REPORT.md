# WP-P0-29 Owner-Signature Lane Report

**Date:** 2026-08-25

**Audit tier:** T2 — status/attribution-only documentation change; separate Lead acceptance remains required.

**Signature commit:** `0e5791f75ca1140974a125a447c64d9dca035917`

The existing `CUSTODY_RUNBOOK_DRAFT.md` and `TREASURY_POLICY_DRAFT.md` filenames were intentionally retained. Renaming them would break the existing relative references from this package and merged packages.

## `git diff --stat ef380d1c..0e5791f7`

```text
 .../11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md     | 3 ++-
 .../11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md               | 2 +-
 .../11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md     | 3 ++-
 .../WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md          | 3 ++-
 4 files changed, 7 insertions(+), 4 deletions(-)
```

## Full `git diff ef380d1c..0e5791f7`

```diff
diff --git a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md
index 803f682c..755521e0 100644
--- a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md
+++ b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md
@@ -1,6 +1,7 @@
 # WP-P0-29 VEN-C — Custody Runbook Draft
 
-**Status:** DRAFT FOR OWNER SIGNATURE · policy design only · T2
+**Status:** SIGNED/ACCEPTED · policy design only · T2
+**Signed by owner Barış, 2026-08-25.**
 
 **Date:** 2026-08-25
 
diff --git a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md
index aec9e14e..b73fd4f4 100644
--- a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md
+++ b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md
@@ -8,7 +8,7 @@
 
 **Audit tier:** T2 — owner-signable policy documents
 
-**Status:** IMPLEMENTER DRAFT PACKAGE COMPLETE; OWNER SIGNATURE AND LEAD ACCEPTANCE PENDING
+**Status:** OWNER SIGNATURE GIVEN 2026-08-25; LEAD ACCEPTANCE OF THE SIGNATURE COMMIT PENDING
 
 ## 1. Scope and authority result
 
diff --git a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md
index db2e305c..2a6078d6 100644
--- a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md
+++ b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md
@@ -1,6 +1,7 @@
 # WP-P0-29 VEN-C — Treasury Policy Draft
 
-**Status:** DRAFT FOR OWNER SIGNATURE · policy only · T2
+**Status:** SIGNED/ACCEPTED · policy only · T2
+**Signed by owner Barış, 2026-08-25.**
 
 **Date:** 2026-08-25
 
diff --git a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md
index 614c3c58..2030fa71 100644
--- a/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md
+++ b/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md
@@ -2,7 +2,8 @@
 
 **Venue:** Hyperliquid
 
-**Status:** DRAFT FOR OWNER REVIEW AND SIGNATURE · T2 · no authenticated read
+**Status:** SIGNED/ACCEPTED · T2 · no authenticated read
+**Signed by owner Barış, 2026-08-25.**
 
 **Review date:** 2026-08-25
```

## Surviving `DRAFT` occurrences

Command:

```text
grep -rn DRAFT MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/
```

Output (before this evidence report was added):

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md:21:1. `CUSTODY_RUNBOOK_DRAFT.md`
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md:31:2. `TREASURY_POLICY_DRAFT.md`
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md:55:| Every precondition-11 item maps to a runbook section or explicit venue-mapping difference | **PASS at draft level:** `CUSTODY_RUNBOOK_DRAFT.md` §9 maps all five original items and map-#96 subproofs. Withdrawal-disabled and IP-restricted are explicitly UNSATISFIED venue differences. |
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md:85:1. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md`
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/LANE_REPORT.md:86:2. `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md`
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/VENUE_DUE_DILIGENCE_RECORD.md:39:| 8 | **Incident response** | [Custody runbook §8.5](CUSTODY_RUNBOOK_DRAFT.md#85-revocation-drill-and-compromise-response) defines auto-DISARM, owner alert, revoke/choose KILL-FLATTEN-venue route, isolate, rotate, preserve evidence and reconcile; no automatic FLATTEN. [Treasury policy §6](TREASURY_POLICY_DRAFT.md#6-usdc-depeg-stance) defines USDC actions. WP-P0-24 entry 0007 says disarm/disable affected adapter or pin known-safe state first. | **PASS as policy design only.** Later implementation and drills remain required. |
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/CUSTODY_RUNBOOK_DRAFT.md:200:The canonical [live gate](../../_AI_MEMORY/LIVE_TRADING_GATE.md#hard-preconditions) remains DRAFT/NOT READY. This table maps every original precondition-11 item plus its map-#96 subproofs. A policy mapping is not proof.
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_29_CUSTODY_2026-08-25/TREASURY_POLICY_DRAFT.md:12:This policy implements the five treasury principles settled in #42 and carried by the [WP-P0-29 contract](../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md#wp-p0-29--ven-c--wallet-custody-and-treasury-policy-new-2026-08-23-wayfinder-fold-tickets-42-and-48). The [custody runbook](CUSTODY_RUNBOOK_DRAFT.md) governs keys and credential boundaries. The [venue due-diligence record](VENUE_DUE_DILIGENCE_RECORD.md) governs whether a first mainnet deposit may even be considered.
```

Justifications, one per surviving occurrence:

1. `LANE_REPORT.md:21` — unchanged required filename reference.
2. `LANE_REPORT.md:31` — unchanged required filename reference.
3. `LANE_REPORT.md:55` — historical draft-level acceptance qualifier; it is not the top signature status and was outside the authorized status-only edit.
4. `LANE_REPORT.md:85` — unchanged required full-path filename reference.
5. `LANE_REPORT.md:86` — unchanged required full-path filename reference.
6. `VENUE_DUE_DILIGENCE_RECORD.md:39` — two unchanged relative-link targets using the required filenames.
7. `CUSTODY_RUNBOOK_DRAFT.md:200` — intentionally untouched statement about the separate canonical live gate, which remains `DRAFT/NOT READY`.
8. `TREASURY_POLICY_DRAFT.md:12` — unchanged relative-link target using the required custody-runbook filename.

## Relative-link resolution

Every `](` target in the four source files was resolved relative to its containing file after the edit:

```text
CUSTODY_RUNBOOK_DRAFT.md: ../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md#wp-p0-29--ven-c--wallet-custody-and-treasury-policy-new-2026-08-23-wayfinder-fold-tickets-42-and-48 => EXISTS
CUSTODY_RUNBOOK_DRAFT.md: ../WAYFINDER_DECISION_FOLD_2026-08-23.md => EXISTS
CUSTODY_RUNBOOK_DRAFT.md: ../WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md => EXISTS
CUSTODY_RUNBOOK_DRAFT.md: ../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md#3-preferred-subaccount-mode => EXISTS
CUSTODY_RUNBOOK_DRAFT.md: ../../_AI_MEMORY/LIVE_TRADING_GATE.md#hard-preconditions => EXISTS
TREASURY_POLICY_DRAFT.md: ../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md#wp-p0-29--ven-c--wallet-custody-and-treasury-policy-new-2026-08-23-wayfinder-fold-tickets-42-and-48 => EXISTS
TREASURY_POLICY_DRAFT.md: CUSTODY_RUNBOOK_DRAFT.md => EXISTS
TREASURY_POLICY_DRAFT.md: VENUE_DUE_DILIGENCE_RECORD.md => EXISTS
TREASURY_POLICY_DRAFT.md: ../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md#3-preferred-subaccount-mode => EXISTS
TREASURY_POLICY_DRAFT.md: VENUE_DUE_DILIGENCE_RECORD.md => EXISTS
VENUE_DUE_DILIGENCE_RECORD.md: ../WP_P0_24_OSS_LEDGER_2026-08-24/DEPENDENCY_LEDGER.md => EXISTS
VENUE_DUE_DILIGENCE_RECORD.md: ../WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md => EXISTS
VENUE_DUE_DILIGENCE_RECORD.md: ../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md => EXISTS
VENUE_DUE_DILIGENCE_RECORD.md: CUSTODY_RUNBOOK_DRAFT.md#85-revocation-drill-and-compromise-response => EXISTS
VENUE_DUE_DILIGENCE_RECORD.md: TREASURY_POLICY_DRAFT.md#6-usdc-depeg-stance => EXISTS
```

Result: all 15 link occurrences resolve to existing paths; no relative link broke.
