# `WP_A_TESTED_ARTIFACT_AUTHORITY_V1`

Status: **PROPOSED DESIGN — NOT IMPLEMENTED, NOT EXECUTED, NOT ACCEPTED, AND NOT AUTHORIZATION**  
Audit tier: **T2** (design/evidence document). The lane contract forbids sub-delegation, so no model-audit verdict is claimed (`C:/tmp/lane_kick/WPAID.md:65-68`).

## 1. Decision

`WP_A_TESTED_ARTIFACT_AUTHORITY_V1` is a single, strict JSONL row produced by the **WP-A close operation**, not by the later final-freeze operation. It records the identity of the installed release payload observed immediately before the first WP-A test and immediately after the last WP-A test. WP-A may close only when those two independently derived observations are identical.

The identity of the tested installed release is the tuple:

```text
(git_object_format, tested_release_oid,
 tested_release_manifest_bytes, tested_release_manifest_sha256)
```

`tested_release_manifest_sha256` is the SHA-256 of the exact raw `RELEASE_SHA256SUMS` member bytes in the installed/tested artifact. It is not a working-tree hash and is not a hash of a value copied from the later freeze. This is consistent with the existing artifact discipline: the current candidate derivation binds the frozen commit and the raw payload-manifest digest, and `install.sh` records that digest in `install_manifest.json` (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:12-24`). The derivation reads Git objects rather than a possibly rendered working tree (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:28-40`) and proves byte fidelity against Git blob identities (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:63-74`).

The contract, producer tool, selector, and RED/GREEN fixtures must be implemented, pinned, and audited **before WP-A begins**. The run-specific row cannot truthfully be populated before the run: it is produced at WP-A close from observations made inside that run. Treating “must exist before WP-A runs” as requiring a populated future observation would be impossible and would invite a guessed value; the task requires the authority mechanism to exist before the run and says WP-A must publish the actual value (`C:/tmp/lane_kick/WPAID.md:12-14`).

## 2. Source limits and known sequence

The three task-named records are not present at their literal paths in the detached `C:\RO` snapshot:

- `MTC_COMMAND_CENTER/11_TRIAGE/MISSING_ARTIFACT_WPA_IDENTITY_AUTHORITY_2026-08-16.md`: **UNKNOWN** in this snapshot.
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_V3_2026-08-16.md`: **UNKNOWN** in this snapshot.
- `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`: **UNKNOWN** in this snapshot.

Their requirements are therefore taken only from the supplied lane contract (`C:/tmp/lane_kick/WPAID.md:5-14`, `C:/tmp/lane_kick/WPAID.md:20-46`, `C:/tmp/lane_kick/WPAID.md:53-57`), not attributed to nonexistent repository lines.

Facts the available repository does establish:

- WP-A is an evidence-mapping and verification overlay, not a feature package (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:779-795`). It performs Ubuntu tests and evidence capture on the retained staging host (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:797-805`).
- Audit 2 precedes WP-A; the current prerequisite document requires STOP if WP-A starts before an accepting Audit-2 close (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:22-31`).
- The operative sequence is WP-A step 5, host discard step 6, final artifact freeze step 7, then Audit 3/Gate 6 (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:970-977`). The combined-plan reconciliation repeats that order (`MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:120-129`).
- Group E already says WP-A captures its evidence before host discard and that its cited tests are against the frozen candidate (`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:896-907`).
- Audit 3 is supposed to work later from the frozen artifact plus the captured WP-A package, without the live host (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:860-864`). That makes a recomputable identity record necessary, not optional.

## 3. Exact location and actors

### 3.1 Paths

The normative producer/verifier must be implemented at:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_RUN_KIT/wpa_tested_artifact_authority_v1.py
```

For run ID `R`, the authority row lives at this fixed repository-relative path:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/authority/WP_A_TESTED_ARTIFACT_AUTHORITY_V1.jsonl
```

The four raw identity captures referenced by the row live at:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/identity/pre/install_manifest.json
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/identity/pre/RELEASE_SHA256SUMS
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/identity/post/install_manifest.json
MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/identity/post/RELEASE_SHA256SUMS
```

No current repository source establishes a canonical WP-A run-ID grammar: **UNKNOWN**. V1 therefore defines it, rather than guessing an inherited grammar:

```regex
^WPA-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}$
```

### 3.2 Lifecycle

1. **Precondition, before WP-A:** the tool and this schema are part of the pre-WP-A frozen inputs and their Git blob OIDs are pinned. Packet 10 already requires path/bytes/SHA identities bound to the frozen checkpoint (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:51-67`).
2. **WP-A pre-observation:** after Audit-2 acceptance and immediately before WP-A's first test, WP-A invokes the tool's `observe --phase pre`. The tool reads the installed release's raw `install_manifest.json` and raw `RELEASE_SHA256SUMS`, strictly parses the former, hashes the latter, and verifies their `release_sha`/`release_manifest_sha256` binding. It accepts no caller-supplied expected release OID or digest.
3. **WP-A work:** WP-A performs its bounded invariant tests and evidence capture.
4. **WP-A post-observation:** immediately after the last WP-A test, before the close record and before host discard, WP-A invokes `observe --phase post` through the same pinned tool.
5. **WP-A close:** the tool derives the tested-artifact tuple independently from both observations. A mismatch is an observed deviant state and exits 1; WP-A does not close. If they match, `close` writes the one-row authority file create-once, recomputes its record identity, and WP-A commits the authority row and four captures in its own close commit. WP-A is not closed until this commit succeeds.
6. **Later freezer:** the final-freeze tool has only a read/verify operation. It is not allowed a `create`, `replace`, `repair`, `prefer-latest`, or caller-supplied-expected option. It reads the authority blob from the WP-A close commit, derives the final artifact identity separately, and compares them.

The WP-A close commit must contain these exact trailers:

```text
WP-A-Run-ID: R
WP-A-Authority-Schema: WP_A_TESTED_ARTIFACT_AUTHORITY_V1
WP-A-Authority-Path: MTC_COMMAND_CENTER/11_TRIAGE/WP_A_EVIDENCE/R/authority/WP_A_TESTED_ARTIFACT_AUTHORITY_V1.jsonl
WP-A-Authority-Blob-OID: GIT_BLOB_OID
WP-A-Authority-Record-SHA256: RECORD_SHA256
```

The literal `producer: "WP-A"` field in the row is only an assertion. Production provenance is enforced by the close sequence: both observations and the add-only authority blob are in the WP-A close commit, that commit precedes host discard and final freeze, and the final freeze must descend from it. The existing programme explicitly places capture before discard (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:974-976`).

## 4. Exact record format and grammar

### 4.1 Byte grammar

The candidate file is UTF-8 without BOM and contains zero or more RFC-8785-canonical JSON objects, each followed by exactly one LF byte. CR, blank lines, invalid UTF-8, duplicate JSON keys, non-finite numbers, and unknown fields are invalid. The V1 producer's valid output contains exactly one row. The verifier nevertheless parses the complete candidate file before selection: an empty file reaches the explicit zero-match outcome, and two valid matching rows reach the explicit multiple-match outcome. They are never collapsed into a generic parse error or first-match success.

The following is a grammar template; uppercase angle-bracket terms are metavariables, not claimed values:

```json
{"payload":{"artifact_kind":"installed-release-payload","git_object_format":"<sha1-or-sha256>","observations":[{"install_manifest":{"bytes":<positive-integer>,"identity_mode":"sha256-raw-captured-file-bytes-v1","path":"identity/pre/install_manifest.json","sha256":"<64-lowercase-hex>"},"phase":"pre","release_manifest":{"bytes":<positive-integer>,"identity_mode":"sha256-raw-artifact-member-bytes-v1","path":"identity/pre/RELEASE_SHA256SUMS","sha256":"<64-lowercase-hex>"}},{"install_manifest":{"bytes":<positive-integer>,"identity_mode":"sha256-raw-captured-file-bytes-v1","path":"identity/post/install_manifest.json","sha256":"<64-lowercase-hex>"},"phase":"post","release_manifest":{"bytes":<positive-integer>,"identity_mode":"sha256-raw-artifact-member-bytes-v1","path":"identity/post/RELEASE_SHA256SUMS","sha256":"<64-lowercase-hex>"}}],"producer":"WP-A","production_event":"wp_a_close","record_identity_mode":"sha256-rfc8785-payload-utf8-v1","schema":"WP_A_TESTED_ARTIFACT_AUTHORITY_V1","tested_release_manifest_bytes":<positive-integer>,"tested_release_manifest_identity_mode":"sha256-raw-artifact-member-bytes-v1","tested_release_manifest_sha256":"<64-lowercase-hex>","tested_release_oid":"<lowercase-git-oid>","wp_a_run_id":"<R>"},"record_sha256":"<64-lowercase-hex>"}
```

Normative constraints:

- For each row, the top-level key set is exactly `{payload, record_sha256}`.
- The payload key set is exactly the 12 keys shown above.
- `observations` has length 2 and order `pre`, then `post`; each observation and nested file-identity object has exactly the shown keys.
- JSON integers are in `1..9223372036854775807`; floats are forbidden.
- `git_object_format == "sha1"` requires a 40-lowercase-hex `tested_release_oid`; `"sha256"` requires 64 lowercase hex. No abbreviation is permitted.
- Each recorded byte count and SHA-256 is recomputed from its named raw capture. Paths are fixed literals, relative to the run evidence root, and may not be symlinks or escape that root.
- Each raw `install_manifest.json` must be a finite, duplicate-key-free top-level JSON object with exactly one top-level string `release_sha` and exactly one top-level string `release_manifest_sha256`. Other install-manifest fields may exist; they do not supply identity.
- For both observations, parsed `release_sha` must equal `tested_release_oid`; parsed `release_manifest_sha256`, the corresponding raw release-manifest SHA-256, and `tested_release_manifest_sha256` must all be identical. The two release-manifest byte counts must both equal `tested_release_manifest_bytes`.
- `record_sha256 = lowercase_hex(SHA256(RFC8785(payload)))`, where `RFC8785(payload)` is the canonical UTF-8 serialization of the payload object only, with no LF. This is the record's own recorded semantic identity.
- The full text-file identity is the Git blob OID in the WP-A close commit and its `WP-A-Authority-Blob-OID` trailer. The verifier reads blob bytes, never working-tree bytes.

The last two rules address text normalization explicitly. The root `.gitattributes` says `* text=auto` (`.gitattributes:1-2`), and an existing baseline demonstrates that Git-object LF bytes and Windows working-tree CRLF bytes can have different lengths and SHA-256 values (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET10_PROVISIONAL_BASELINE_2026-08-15.md:90-110`). No hash in this design is an unstated “text hash.”

## 5. Create-once and immutability

### 5.1 Enforced create-once behavior

`close` first writes canonical bytes to a unique temporary file in the same directory, flushes and fsyncs it, then installs the final fixed path with a no-replace primitive (`linkat`/equivalent exclusive creation). It fsyncs the directory after the link. It never uses replacing `rename`, truncating open, append, or delete-and-recreate.

If the final path already exists for any reason, a second write must:

```text
WPAID_STOP reason=authority_already_exists run_id=R path=PATH
exit 3
```

The existing file is not opened for writing, compared-and-replaced, deleted, or “repaired.” An interrupted attempt before the exclusive link leaves no final authority path and may be retried after its unlinked temporary file is adjudicated. An interruption after the exclusive link is a create-once partial-close condition: WP-A remains open and requires adjudication; it does not issue a second write.

### 5.2 Immutability after WP-A close

The WP-A close commit must add the authority path from absent to one Git blob. The final-freeze verifier enforces all of the following:

1. the selected WP-A close commit is an ancestor of the proposed final-freeze commit;
2. the authority path is absent in the close commit's first parent and present in the close commit;
3. the close trailer's blob OID equals the close commit tree's blob OID at that path;
4. every commit on the linear first-parent chain from WP-A close through final freeze carries the same blob OID at that path; any merge in this interval is STOP pending explicit lineage adjudication;
5. there is no modification, deletion, rename, second add, or modify-then-revert of the path in that interval.

A positively observed post-close path change is:

```text
WPAID_FAIL reason=authority_changed_after_wp_a_close run_id=R commit=OID
exit 1
```

Git object content addressing prevents a later ordinary commit from changing the historical blob in the WP-A close commit. The record hash detects semantic corruption; the close-commit blob OID pins the complete text bytes. Thus the sanctioned freezer cannot influence the expected identity without producing an observable lineage or blob mismatch.

One boundary is not established by the available repository: whether WP-A and the freezer run as distinct OS principals, use an append-only external ledger, or have WORM/signature protection is **UNKNOWN**. Therefore this design establishes separation under the repository's content-addressed, non-destructive Git workflow; it does **not** claim resistance to a malicious same-principal actor that deletes Git objects or rewrites all history and every external reference. If that stronger threat model is required, this design is BLOCKED until a separately controlled append-only publication or signature authority is specified. The literal `producer` field, file mode, or `chmod 0444` would not close that stronger gap.

## 6. Unique-row selector

Inputs are the proposed final-freeze commit `F` and the preregistered WP-A run ID `R`. `R` comes from the WP-A dispatch/close chain; the freezer may not mint or substitute it.

The selector must:

1. locate the unique ancestral close commit whose exact trailers name schema V1 and run ID `R`;
2. extract the authority path's exact Git blob bytes from that commit;
3. strict-parse every JSONL row without ignoring malformed rows;
4. calculate `matches = rows where payload.schema == "WP_A_TESTED_ARTIFACT_AUTHORITY_V1" and payload.wp_a_run_id == R`;
5. require `len(matches) == 1` before reading any expected artifact field.

Explicit cardinality outcomes:

```text
0 rows:  WPAID_STOP reason=authority_selector_zero_matches run_id=R count=0     ; exit 3
>1 row:  WPAID_STOP reason=authority_selector_multiple_matches run_id=R count=N ; exit 3
1 row:   continue verification
```

The same zero/one/many rule applies to matching close commits. There is no `first`, `last`, `head -1`, newest timestamp, lexical preference, or duplicate collapse. This is the conservation rule the defect catalogue demands: every admitted member must have one terminal disposition, with missing or duplicate identity stopping the check (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`).

## 7. Exit contract and failure modes

Only these process exits are legal:

| Exit | Terminal prefix | Meaning |
|---:|---|---|
| 0 | `WPAID_PASS` | Authority and final artifact were completely evaluated and identities are equal. |
| 1 | `WPAID_FAIL` | Evaluation completed and observed a deviant state. |
| 3 | `WPAID_STOP` | The authority or final artifact could not be evaluated uniquely and completely. |

An unexpected exception is caught, rendered as `WPAID_STOP reason=unadjudicated_exception`, and exits 3; raw child-process exits never escape. This follows the repository rule that inability to observe is STOP, while an observed mismatch is FAIL (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:52-85`).

| Condition | Exit/reason | Why |
|---|---|---|
| Second create at the fixed path | 3 / `authority_already_exists` | No second write is performed. |
| Zero or multiple close commits/rows | 3 / explicit selector reason | No unique expected value exists. |
| Invalid UTF-8/JSON, BOM/CR, duplicate or unknown key, wrong field type, bad OID/hash grammar, symlink/path escape | 3 / `authority_record_invalid` | Expected identity cannot be safely parsed. |
| Missing Git object, read error, hash tool error, incomplete artifact traversal | 3 / `identity_recompute_unevaluable` | Observation did not complete. |
| Record semantic hash or close-trailer blob OID does not recompute | 3 / `authority_identity_invalid` | The authority is unusable as an expected source. |
| Pre/post WP-A observations both evaluate but differ | 1 / `artifact_changed_during_wp_a` | Deviant state was observed; no authority row or WP-A close is issued. |
| Install manifest, raw release manifest, or tested tuple fully evaluates but bindings differ | 1 / `artifact_binding_mismatch` | The installed artifact is internally divergent. |
| Authority blob changes after WP-A close | 1 / `authority_changed_after_wp_a_close` | Immutability violation was positively observed. |
| Final-freeze artifact tuple differs from selected WP-A tuple | 1 / `tested_artifact_mismatch` | This is the continuity RED. |
| All checks complete and tuples equal | 0 / `WPAID_PASS` | Continuity is established. |

## 8. Auditor verification procedure

The auditor was not present for WP-A and does not need the discarded host.

1. Resolve `F` from the proposed final-freeze record and `R` from the preregistered WP-A dispatch/close chain. If either source is absent or ambiguous, STOP 3.
2. Verify the unique close-commit selector and ancestry/linear-history rules in section 6. Do not accept a close commit supplied only by the freezer.
3. Read the authority with Git object access from the close commit, not from the checkout. Verify its blob OID against the close trailer and tree entry.
4. Strict-parse the JSONL, apply the zero/one/many selector, and recompute `record_sha256` from RFC-8785 canonical payload bytes.
5. Extract each of the four captured files by its pinned Git blob from the WP-A close commit. Recompute its raw byte count and SHA-256 under the identity mode in the row.
6. Strict-parse both captured install manifests. Independently derive both observed identity tuples by combining their top-level `release_sha`/`release_manifest_sha256` fields with the raw captured `RELEASE_SHA256SUMS` byte counts and hashes. Require pre == post == authority tuple.
7. Independently reconstruct the release manifest for `tested_release_oid` from Git objects using the same rules as the artifact producer: Git blob bytes, explicit `RELEASE_SHA` LF member, C-locale member order, and the artifact's actual separator rendering. The existing derivation documents those rules (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:47-61`, `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:76-106`) and its refusal conditions (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:108-119`). Require the rederived manifest bytes/count/hash to equal the authority tuple and captured manifests.
8. Independently derive the proposed final-freeze artifact tuple from the frozen artifact itself. The expected tuple must remain the selected WP-A row; never derive both expected and observed from the final artifact.
9. Compare the tuples and emit exactly one PASS/FAIL/STOP terminal line and the legal rc.
10. Execute the cardinality, create-once, corruption, A-versus-B RED, and A-versus-A GREEN fixtures from section 9. Record the literal resolved commands and real output. A prose recipe is supplemental only: the defect catalogue requires an executable RED and GREEN, not exact-looking tables (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:618-628`, `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:658-684`).

The eventual normative entry point is:

```text
python MTC_COMMAND_CENTER/11_TRIAGE/WP_A_RUN_KIT/wpa_tested_artifact_authority_v1.py verify-freeze --repo ABS_REPO --freeze-commit F --wp-a-run-id R
```

`ABS_REPO`, `F`, and `R` above are grammar operands, not a claim that a literal command was run. Implementation closure requires a dispatch record with concrete values and unedited real output.

## 9. Failure demonstration: the continuity check has a real RED

### 9.1 Concrete world

Use two already identified, different release OIDs:

- Artifact A: release `2ce41e34bceb599d80af24c5c33d835820ec321b`, whose raw payload-manifest identity is `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_DERIVATION.md:12-20`).
- Artifact B: the earlier installed release `ebada020a59edf539f60acfbb3a6bf870c8679e9` (`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RESULT_2026-08-08.md:143-150`). Its full manifest SHA-256 is not established in that record: **UNKNOWN until independently rederived**. That unknown does not prevent the RED because the full release OIDs already differ.

The reproduction world is:

1. The WP-A pre and post observations both bind Artifact A. WP-A closes and publishes the V1 row with A's full tuple.
2. After WP-A closes, the freezer proposes Artifact B as the final release artifact.
3. A defective self-confirming check would derive its expected value from B and compare B to B. This design instead derives expected from the immutable WP-A close blob (A) and observed from the proposed freeze artifact (B).
4. Both identities evaluate, and `2ce41e34...321b != ebada020...79e9`; therefore the check must emit:

```text
WPAID_FAIL reason=tested_artifact_mismatch run_id=R expected_release_oid=2ce41e34bceb599d80af24c5c33d835820ec321b observed_release_oid=ebada020a59edf539f60acfbb3a6bf870c8679e9
```

and exit **1**. This is a real discriminating predicate: changing what the freezer selects, without changing the WP-A authority, turns continuity RED.

### 9.2 Auditor reproduction matrix

| Fixture | Authority | Proposed freeze | Required outcome |
|---|---|---|---|
| RED continuity | A | B | rc 1, `tested_artifact_mismatch` |
| GREEN control | A | A | rc 0, `WPAID_PASS` |
| Missing authority | zero matching row | A | rc 3, `authority_selector_zero_matches` |
| Duplicate authority | two matching A rows | A | rc 3, `authority_selector_multiple_matches count=2` |
| Second create | existing fixed V1 path | any | rc 3, `authority_already_exists`; original blob unchanged |
| Corrupt record | one payload byte changed, old `record_sha256` retained | A | rc 3, `authority_identity_invalid` |

The auditor must run the RED first, the GREEN second, and verify the original authority blob OID before and after all fixtures. The RED uses the exact same verifier entry point as production; no helper-only comparison counts. The record is not implementation evidence until those commands and their real outputs exist. This document constructs the falsifiable world but does not claim it was executed, because the V1 tool does not yet exist in this snapshot.

## 10. Self-confirming-check accounting

| Check | What makes it fail? | Expected value source | Enforced or asserted? |
|---|---|---|---|
| WP-A pre/post stability | Both observations complete and their artifact tuples differ. | Pre-observation tuple, derived from WP-A raw captures; no digest argument. | Enforced by `close`; record is not written and WP-A cannot close. |
| Install-manifest binding | Parsed release OID/digest differs from raw captured release-manifest identity. | Raw captured `install_manifest.json` plus separately hashed raw `RELEASE_SHA256SUMS`. | Enforced. Neither is allowed to supply both sides. |
| Record self-identity | RFC-8785 payload hash differs from `record_sha256`. | Payload bytes in the selected Git blob. | Enforced as corruption detection; by itself it does not prove producer identity. |
| Producer is WP-A | A matching authority add occurs in the WP-A close commit before discard/freeze. | WP-A run/close chain, commit trailers, ancestry, and blob OID. | Enforced at protocol/Git-history level. The JSON `producer` string alone is asserted. Distinct OS-principal enforcement is **UNKNOWN**. |
| Unique selection | Zero or more than one schema+run-ID row/close commit exists. | Preregistered `R` plus literal schema. | Enforced; STOP 3, never first-match. The current source for preregistering `R` must be added; it is presently **UNKNOWN**. |
| Authority immutability | Any descendant commit changes/deletes/re-adds the authority path. | WP-A close commit's tree/blob identity. | Enforced over the linear Git ancestry; destructive all-history rewrite resistance is **UNKNOWN**. |
| Final freeze continuity | Proposed final artifact tuple differs from selected WP-A tuple. | Expected = WP-A close row; observed = independent final-artifact recomputation. | Enforced; this is the A-versus-B rc-1 RED. |

## 11. Required sequence and document amendments

The authority belongs **inside existing step 5, at WP-A close**, after the last WP-A observation and before step 6 may discard the host. Existing step 5 already includes WP-A evidence capture, step 6 conditions discard on completion/capture, and step 7 performs the final freeze (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:970-977`). Step 7 must consume the already published V1 row and run continuity; it must not create or fill the row.

Before any WP-A dispatch, amend these documents:

1. **`MTC_COMMAND_CENTER/11_TRIAGE/MISSING_ARTIFACT_WPA_IDENTITY_AUTHORITY_2026-08-16.md`** — add this exact V1 contract and keep the gap open until the pinned producer/verifier and executed RED/GREEN evidence exist. Literal source is currently **UNKNOWN** in `C:\RO`.
2. **`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_V3_2026-08-16.md`** — add V1 as a mandatory input; unique-select the WP-A close row; require ancestry/add-only/blob checks; independently derive the final artifact; STOP on unavailable/ambiguous authority and FAIL on identity mismatch. Literal source is currently **UNKNOWN** in `C:\RO`.
3. **`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` Group E** — add an `E9 — WP-A tested-artifact identity publication` item after the existing invariant actions, with pre/post observe, exact output paths, close rule, exits, and D026 fixtures. Group E is the current detailed WP-A execution specification (`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:896-902`).
4. **`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md` §19 and §23a/§23b** — make WP-A close conditional on V1 publication; make host discard conditional on the committed blob; make step 7 run the continuity verifier. Add V1 and the continuity result to the Gate-B checklist, alongside the current WP-A evidence/final artifact requirements (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:1018-1026`).
5. **`MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md`** — expand combined-order step 5 so `WP-A close + V1 authority commit` precedes host discard and final freeze (`MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:120-127`).
6. **`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md`** — at the pre-WP-A freeze, pin the V1 contract and tool blob OIDs as future WP-A inputs. The run-specific row is correctly absent at Audit 2 and must not be fabricated there. The package already distinguishes producer steps and requires one authoritative manifest (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-67`).
7. **The eventual WP-A close record/template and final Audit-3/Gate-6 auditor-input document** — names are **UNKNOWN** in the available snapshot. They must carry `R`, the WP-A close commit OID, authority path/blob OID/record SHA-256, continuity command/output/rc, and the RED/GREEN evidence. Audit 3 already depends on the exact frozen artifact and captured WP-A evidence package (`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md:860-866`).
8. **`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`** — cross-reference V1 as the expected-value authority for final-freeze continuity and retain the A-versus-B falsification. Literal source is currently **UNKNOWN** in `C:\RO`.

No amendment may state that V1 exists, is accepted, or closes the gap until the tool, add-only close integration, unique selector, full auditor recomputation, and recorded RED/GREEN runs are real.
