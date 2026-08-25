# WP-P0-29 VEN-C — Custody Runbook Draft

**Status:** DRAFT FOR OWNER SIGNATURE · policy design only · T2

**Date:** 2026-08-25

**Owner:** Barış

**Hard boundary:** This document creates, stores, reads, prints, transmits, imports, approves, revokes or handles no seed, private key, API credential or authenticated account value. It authorizes no purchase, wallet creation, deposit, transfer, venue contact, host contact, testnet action, mainnet action or trading action. Every later execution act requires its own scope, tier and authorization.

**Acceptance boundary:** Signing this draft accepts the procedure and proposed policy values. It does not prove a ceremony or drill occurred, satisfy a live-readiness row, or authorize execution.

## 1. Governing records and verified venue facts

This runbook implements the WP-P0-29 contract in the [master work-package plan](../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md#wp-p0-29--ven-c--wallet-custody-and-treasury-policy-new-2026-08-23-wayfinder-fold-tickets-42-and-48), the #42/#48 decisions in the [wayfinder decision fold](../WAYFINDER_DECISION_FOLD_2026-08-23.md), and the credential doctrine in brief §12.6.3.

The merged [WP-P0-28 venue record](../WP_P0_28_VENUE_FACTS_2026-08-25/VENUE_VERIFICATION_RECORD_2026-08-25.md) establishes only the facts used here:

- a master account may approve agent/API wallets for itself or subaccounts; subaccounts have no private keys (rows `d` and `e`);
- nonces are per signer, supporting dedicated signer isolation (row `f`);
- a custom agent-wallet expiry may be set no more than **180 days** in the future, while the default duration is undocumented (row `g`);
- actual account eligibility and testnet gate behavior remain UNKNOWN (rows `r` and `s`);
- customer-configurable venue IP allowlisting remains UNKNOWN; documented per-IP rate limiting is not an allowlist (rows `n` and `t`); and
- no independent agent-withdrawal safety boundary is established by WP-P0-28's [binding specification](../WP_P0_28_VENUE_FACTS_2026-08-25/ACCOUNT_BINDING_AND_FALLBACK_SPEC.md#3-preferred-subaccount-mode).

Therefore this policy treats every agent wallet as capable of moving or economically endangering its accessible funds until a later primary-source record proves a narrower boundary.

## 2. Roles and records

| Role | Permitted policy role | Forbidden under this package |
|---|---|---|
| Owner | Signs/amends this policy; later authorizes each separately gated ceremony, provisioning, transfer, revocation and recovery act | Delegating master-seed knowledge or master-signing authority to software, an AI agent or an ordinary operator |
| Ceremony observer, optional | On a later authorized date, checks the non-secret checklist without viewing seed words or PINs | Recording, photographing, reading back or retaining any secret |
| Worker/process | After later authorization, uses only its own stage- and bucket-scoped credential through restricted OS storage | Reading, printing, exporting or sharing a secret; using a master key |
| AI/automation | Verifies non-secret presence, permission metadata, public address, expiry and audit-record completeness | Receiving seed words, private keys, credentials, screenshots of secrets or secret-bearing logs/prompts |

Only non-secret metadata may enter the permanent audit record: ceremony/drill date, device model and firmware version, public address, public signer address, stage, risk bucket/worker ID, explicit expiry timestamp, approver, lifecycle event, result, and evidence pointer. A seed, private key, PIN, recovery phrase, QR code, encrypted secret blob or credential value is never audit evidence.

## 3. Approved custody topology

### 3.1 Preferred topology

1. One dedicated, freshly generated **hardware-signer master wallet** is the custody root for this project.
2. The master signer remains offline, off KVM2 and outside all dashboard, research, AI, notification and execution paths.
3. The master account may govern venue subaccounts, but each active risk bucket or worker receives its own dedicated agent wallet under the accepted WP-P0-28 binding.
4. A live agent wallet is never shared across risk buckets/workers and never reused in testnet.
5. Public addresses and lifecycle metadata may be registered; secrets may not.

### 3.2 Standalone-second-master-account fallback

This is a recorded fallback topology, not an authorization or automatic failover:

- It may be selected only by a separate written owner decision after accepted evidence shows the preferred master/subaccount topology cannot supply the required isolation or capacity.
- It uses a **separate freshly generated hardware master wallet, separate seed, separate two-location backups, separate restore drill and separate audit lineage**. The first master seed, signer or agent wallets are never reused.
- It must have an explicit purpose and risk-bucket allocation; funds and positions are never silently moved between masters.
- Activation, funding, migration and retirement each require their own authorization, reconciliation and no-orphan disposition.
- A second master account is not a workaround for UNKNOWN eligibility, UNKNOWN IP restriction or an unproven withdrawal boundary.

## 4. Hardware master-wallet generation ceremony — design

### 4.1 Preconditions for any future ceremony

The Lead must freeze a separate execution contract that names the hardware signer model, trusted acquisition path, firmware verification source, compatible recovery device, date/location, authorized participants, evidence fields and rollback/abort rules. The owner must approve that exact contract. This draft neither selects nor purchases a device.

The ceremony aborts if packaging, firmware identity, entropy generation, display integrity, device state, room privacy or participant authorization is uncertain. No improvised workaround is allowed.

### 4.2 Proposed ceremony sequence

1. Owner confirms the signer is dedicated to this project, reset to the verified factory state and running owner-verified firmware.
2. Owner performs setup in a private room with cameras, phones, microphones, remote-desktop tools and screen capture removed or disabled. The optional observer cannot see the device display or backup words.
3. The hardware signer generates the seed internally. The owner records it **by hand directly onto two numbered physical backup media**; no computer keyboard, printer, photograph or digital note is used.
4. The owner verifies every word/order using the signer's own confirmation flow.
5. The owner sets a unique device PIN/passphrase according to the separately approved device procedure. The PIN/passphrase is not written in this repository or on the seed medium.
6. The owner displays the first public receive address on the hardware signer and records only that public address plus device/firmware metadata in the audit record.
7. Before any mainnet deposit, the empty-wallet restore drill in §6 must pass. Failure voids the ceremony result and triggers a separately authorized restart with a fresh seed.
8. After a passing drill, the owner seals and distributes the two backups under §5. No deposit or venue approval is part of the ceremony.

## 5. Storage medium and two physical backup locations

### 5.1 Proposed medium

- Two separately numbered, tamper-evident, fire- and water-resistant **metal mnemonic backup media**, each holding the complete recovery material needed by the selected signer procedure.
- No split that makes recovery depend on improvised reconstruction; no photo, scan, cloud copy, password manager, email, ordinary backup, repo entry or AI prompt.
- The hardware signer is stored separately from both seed backups when not in use.
- Tamper seals and inspection dates are recorded without recording their secret contents.

### 5.2 Owner-filled location placeholders

The owner fills the exact names/addresses **only on the printed, sealed signature copy**. The repository copy keeps placeholders.

| Item | Named placeholder for sealed owner copy | Separation rule |
|---|---|---|
| Seed backup A | `[LOCATION A NAME / CUSTODIAN / ACCESS METHOD — OWNER FILLS OFF-REPO]` | Not in the same building, fire/flood zone or access-control dependency as Location B |
| Seed backup B | `[LOCATION B NAME / CUSTODIAN / ACCESS METHOD — OWNER FILLS OFF-REPO]` | Not in the same building, fire/flood zone or access-control dependency as Location A |
| Hardware signer | `[SIGNER STORAGE LOCATION — OWNER FILLS OFF-REPO]` | Not stored with either complete seed backup |

Proposed inspection cadence: the owner checks seal/inventory condition **every 90 days** and after any access, move, disaster warning or suspected exposure. Inspection never requires exposing the words unless a separately authorized recovery or drill requires it.

## 6. Empty-wallet restore drill — design only

**Mandatory timing:** completed and accepted after the master ceremony and **before the first mainnet deposit**. This section designs the drill; no drill has been run.

### 6.1 Preconditions

- The wallet is proven empty by public-address inspection; no asset, approval, position or venue relationship exists.
- A compatible recovery signer has been separately selected and authorized.
- The exact seed-handling room, participants, evidence fields and wipe-verification method are approved.
- No camera, remote access, clipboard, printer, digital note or AI tool is present.

### 6.2 Drill sequence

1. Record the original signer's public receive address from its trusted display.
2. Power off and physically isolate the original signer.
3. Owner retrieves **one** seed backup through its logged access procedure and restores it into the separately authorized empty recovery signer, entering words only on that hardware device.
4. Display the same derivation/account public receive address on the recovery signer's trusted display.
5. Pass only if the complete displayed address matches the ceremony record exactly and the public chain view remains empty.
6. Record only pass/fail, devices, firmware, public address, date, participants and backup identifier A/B. Record no secret.
7. Wipe the recovery signer using the device's verified reset procedure; prove it no longer displays or derives the wallet before it leaves the room.
8. Reseal and return the used backup; inspect the other backup's seal without opening it.

Any mismatch, uncertain wipe, exposed word, damaged seal or unlogged access is a failure. The wallet remains ineligible for funding; the owner decides under a new scope whether to repeat, destroy or replace the seed.

## 7. Loss and recovery paths

| Event | Required response | Return condition |
|---|---|---|
| Signer lost/damaged; both backups believed intact | DISARM affected scopes; notify owner; inventory public addresses and exposure; recover using one sealed backup on an approved replacement signer; verify address; rotate affected agent wallets | Owner accepts recovery evidence, both backup locations are re-inventoried, and reconciliation is clean |
| One backup lost/damaged; signer and other backup intact | DISARM if exposure is uncertain; owner authorizes creation of a replacement backup through a fresh controlled ceremony | Two separated intact backups restored, old medium accounted for or recorded irrecoverable, seals logged |
| Seed or master signer suspected exposed | Treat master as compromised; DISARM; owner chooses KILL/FLATTEN/venue route as needed; preserve evidence; create a wholly fresh master topology only under separate authorization | Funds/positions reconciled, exposed authority revoked or abandoned safely, fresh custody ceremony and restore drill accepted |
| Both backups lost; signer works | No routine use. DISARM; owner authorizes migration to a fresh master while the signer still works | Fresh master ceremony, restore drill, owner-authorized transfer plan and reconciliation accepted |
| Both backups and signer lost | Record custody loss. No technical recovery is claimed or improvised | Only independently proven venue/account recovery options may be considered under a new owner-authorized incident scope |
| Owner incapacitated | Trusted person uses the sealed pointer sheet in §10; it contains no key and grants no signing authority | The separately defined legal/account recovery process determines authority |

There is no automatic transfer, KILL or FLATTEN in any recovery path.

## 8. Credential-lifecycle boundary policy (map #96)

### 8.1 Absolute stage separation

| Stage | Credential rule |
|---|---|
| Simulation | **No exchange credential.** Credential inventory must be zero. |
| `INTERNAL_PAPER` | **No exchange credential.** A venue credential invalidates the environment. |
| `EXCHANGE_TESTNET` | Testnet-only agent wallets/credentials under WP-V2B-07's later authorization. Never reused in live. |
| Live | Distinct live agent wallet per risk bucket or worker. Never reused in testnet or another bucket/worker. |

No credential crosses a stage. Changing stage requires a new identity and separately audited lifecycle.

### 8.2 Least privilege and the one secret road

- Each worker receives only its own scoped credential. The master wallet never signs routine worker actions.
- Dashboard, research surfaces, AI tooling and notification paths hold no exchange key.
- Secrets never enter Git, issues, documents, logs, evidence, ordinary backups, screenshots, terminals captured to logs, or AI prompts.
- Owner-gated provisioning exposes a value only to its required process through restricted operating-system secret storage. The exact mechanism belongs to the later T0/T1 execution design.
- Agents and checks may verify presence, owner, mode/ACL, public signer identity, scope and expiry; they never read or print the value.
- Because withdrawal restrictions are unverified, every agent wallet is treated as able to move or economically endanger all funds reachable through its binding.

### 8.3 Agent-wallet generation and storage design

Any future generation belongs to WP-V2B-07 or another separately authorized execution package; this section defines its custody contract only:

1. The owner-approved package names one stage and one risk bucket/worker before generation. A wallet is never generated “for later” or for a shared pool.
2. Generate the agent secret inside the later-approved restricted execution environment using the approved cryptographic tool. No browser extension, chat, clipboard, ordinary file, shell history or AI tool may receive it.
3. Record the public signer address, intended stage, bucket/worker, creation event and explicit expiry before approval. The secret goes directly into restricted OS secret storage accessible only to the named process.
4. The owner uses the offline master signer to approve only that public agent identity and scope under the later authorized venue procedure. The master seed/private key never enters the execution environment.
5. Verify secret-store owner/mode/ACL, expected public signer, venue-visible scope and explicit expiry without reading or printing the value. A mismatch destroys eligibility; it is not repaired by copying the secret elsewhere.
6. Before activation, prove the credential cannot authenticate in another stage or worker and cannot appear on dashboard, research, AI or notification paths. Actual probes and their tier belong to the later execution package.
7. Store no recoverable agent-secret backup in ordinary backup systems. Recovery means owner-authorized generation of a successor, not restoration from Git, documents, logs or an AI transcript.

### 8.4 Proposed calendar lifecycle

WP-P0-28 row `g` verifies a configurable expiry of at most 180 days and no documented default. The owner is asked to sign or amend this more conservative proposal:

1. Set every agent wallet's explicit `valid_until` to **120 days** from activation; never rely on the venue default.
2. Plan routine replacement by **day 90**, leaving up to 30 days to complete a fail-closed handover before expiry.
3. Warn the owner at **30, 14, 7 and 1 day** before expiry. A missing warning or unrecorded expiry blocks new risk for that credential.
4. Preflight available agent slots. If a successor cannot overlap because of venue capacity, DISARM the affected scope, reach a flat/reconciled state, revoke the predecessor, then activate the successor. Sharing a credential is not a capacity workaround.
5. Activation requires recorded public signer address, stage, bucket/worker, explicit expiry, scope and owner approval. Rotation retires the predecessor only after the successor is permission-checked and reconciliation is clean.
6. Revoke immediately on suspected compromise, personnel/device/access change, unintended disclosure, permission drift, binding change or unexplained signed action. Incident-driven rotation overrides the calendar.
7. Creation, activation, rotation, revocation, expiry and destruction each receive an append-only audit event. Destruction means the authorized secret-storage copy is removed and absence is verified without revealing its former value.

### 8.5 Revocation drill and compromise response

A dated revocation drill must be proven before live and after any material venue/credential-path change. The later authorized drill must show: affected scope auto-DISARMS; owner alert arrives; credential is revoked through the approved path; a deliberate safe probe can no longer authenticate; no other worker credential is affected; and reconciliation is clean. D026 RED/GREEN applies where a regression test is offered as proof.

On suspected compromise:

1. auto-DISARM the affected scope and alert the owner;
2. preserve non-secret evidence and stop new risk;
3. owner revokes and chooses KILL, FLATTEN or the venue-side route as needed;
4. isolate the affected device/process and rotate the credential;
5. reconcile account, positions, orders and lifecycle records; and
6. keep live eligibility blocked until the Lead accepts clean recovery evidence.

There is **no automatic FLATTEN**.

## 9. Live-gate precondition 11 mapping

The canonical [live gate](../../_AI_MEMORY/LIVE_TRADING_GATE.md#hard-preconditions) remains DRAFT/NOT READY. This table maps every original precondition-11 item plus its map-#96 subproofs. A policy mapping is not proof.

| Required item | Runbook section or venue-mapping difference | Draft disposition |
|---|---|---|
| Withdrawal disabled | **Venue difference:** WP-P0-28 does not establish a configurable withdrawal-disabled permission or an agent-withdrawal safety boundary. §§1, 8.2 apply least trust. | **UNSATISFIED / BLOCKING** until primary-source evidence and later permission proof establish the required boundary, or the owner formally changes the gate through its own authority |
| IP restricted | **Venue difference:** WP-P0-28 row `t` says customer-configurable IP allowlisting is UNKNOWN; row `n`'s rate limit is not an allowlist. | **UNSATISFIED / BLOCKING**; private-host controls may reduce risk but do not falsely satisfy the venue restriction |
| Least-privilege permissions | §§2, 3.1, 8.1–8.2 | Policy defined; later implementation and permission evidence required |
| Rotation schedule | §8.4 proposes 120-day explicit expiry, rotation by day 90 and 30/14/7/1-day warnings | Proposed for owner signature; no rotation performed |
| Secrets outside repository | §§2, 5, 8.2 | Policy defined; later storage/permission proof required |
| Stage-separated credentials; no reuse | §8.1 | Policy defined; later inventory evidence required per stage |
| Credential scoped per worker/risk bucket | §§3.1, 8.1–8.2 | Policy defined; later binding evidence required |
| No exchange key on dashboard, research, AI or notification paths | §§2, 8.2 | Policy defined; later absence checks required |
| Master wallet offline and off KVM2 | §§3.1, 4, 8.2 | Policy defined; later custody evidence required |
| Owner-gated provisioning; agents never read/print values | §§2, 8.2 | Policy defined; later G6 mechanism and tests required |
| Audited creation, activation, rotation, revocation, expiry, destruction | §§2, 8.3–8.4 | Event schema described; no lifecycle event claimed |
| Expiry warnings | §8.4 | Proposed warning schedule; later monitoring evidence required |
| Proven revocation drill | §8.5 | Drill design only; **not proven** |
| Compromise auto-DISARMS affected scope and alerts owner | §8.5 | Response defined; later fail-closed implementation and drill required |
| Owner chooses revoke/KILL/FLATTEN/venue route; no automatic FLATTEN | §§7, 8.5 | Policy defined; later emergency-path evidence required |
| Live blocked until clean recovery | §§7, 8.5 | Policy defined; later canonical register evidence required |

## 10. Sealed incapacity pointer sheet — template, no keys

Existence of a completed, sealed copy is required before the first `LIMITED_LIVE` position. It is an additional named requirement alongside the fourteen live-gate preconditions; it satisfies none of them.

The trusted person receives only a sealed paper containing:

- `[TRUSTED PERSON LEGAL NAME — OWNER FILLS OFF-REPO]`;
- owner identity and emergency/legal contact pointers;
- pointer to the hardware signer's storage custodian **without** a PIN, seed, passphrase or exact secret location in the repository copy;
- pointer to Location A and Location B custodians, with the instruction that no one should combine or expose materials absent verified legal authority;
- venue/account public identifiers and support URL/contact pointer, no login or credential;
- pointer to the latest signed treasury/custody policy and legal authority documents;
- instruction: **do not trade, transfer, restore, type, photograph or disclose anything; obtain verified legal authority and qualified legal/tax advice first**; and
- owner-selected first contact: `[NAME / ROLE / CONTACT — OWNER FILLS OFF-REPO]`.

Proposed review cadence: inspect the sealed sheet every **90 days** and after any custodian, location, legal-authority, venue or contact change. The repository records existence/review date only, never its filled contents.

## 11. Owner decision and signature

The owner must initial each proposal or write a replacement before signing:

| Proposal | Accept / amend |
|---|---|
| Two complete metal backups in two separately named physical locations | `[INITIAL / AMENDMENT]` |
| Empty-wallet restore drill before first mainnet deposit | `[INITIAL / AMENDMENT]` |
| Backup/sealed-sheet inspection every 90 days | `[INITIAL / AMENDMENT]` |
| Agent explicit expiry 120 days; planned rotation by day 90 | `[INITIAL / AMENDMENT]` |
| Expiry warnings at 30/14/7/1 days | `[INITIAL / AMENDMENT]` |
| Least-trust treatment until withdrawal boundary is primary-source proven | `[INITIAL / AMENDMENT]` |
| Sealed incapacity pointer sheet exists before first `LIMITED_LIVE` position | `[INITIAL / AMENDMENT]` |

**Owner name:** `[PRINT NAME]`

**Owner signature:** `[SIGNATURE]`

**Signed date/time and timezone:** `[YYYY-MM-DD HH:MM TZ]`

**Effective policy version:** `[VERSION]`

**Amendments, if any:** `[ATTACH SIGNED AMENDMENT; NO SECRETS]`
