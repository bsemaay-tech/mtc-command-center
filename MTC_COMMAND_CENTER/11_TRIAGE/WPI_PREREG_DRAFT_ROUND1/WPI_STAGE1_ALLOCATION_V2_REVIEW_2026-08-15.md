NEEDS-REWORK

Audit tier: **T2 (documentation/evidence review)**. Reviewed object: commit `a4833939b02a60815cfb321287d089cc6fdf8332`, because the detached `C:\RO` worktree and its `HEAD` (`25564449b8a8254eaa75535039acef4993f5f27e`) predate the three named artifacts. No repository write, host/network action, or delegated process was used.

## Per-finding closure status

| Prior finding | Status in v2 | Short reason |
|---|---|---|
| 1. Fields named, record not populated | **NOT CLOSED** | V2 is still explicitly a template and every live value/result is still a STOP placeholder. |
| 2. Exact reason-token grammar | **NOT CLOSED** | Substring matching is gone, but the replacement “exact line” reader accepts embedded and trailing NUL bytes. |
| 3. Collision universe unproved | **NOT CLOSED** | V2 admits completeness is not proved; its proposed authority/manifest gate can self-confirm an incomplete archive, and its commit-identity fields are self-referential. |
| 4. Append-only asserted, not enforced | **PARTIALLY CLOSED — DESIGN ONLY** | V2 specifies meaningful prefix/suffix/chain/blob checks, but supplies no executable verifier or run evidence. |
| 5. Checked predicate not bound to sourced object | **PARTIALLY CLOSED — DESIGN ONLY; ACTUAL BINDING UNKNOWN** | V2 describes a sensible snapshot-and-lock chain and the Bash body sources `$1`, but there is no caller implementation or transcript proving which object was passed and opened. |

## 1. Population: not closed

V2 correctly labels itself “NOT A LIVE ALLOCATION” and says the spendable record will exist only after replacement of the labels (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:1-3`). The allocation table still contains `MUST BE MINTED`, `MUST BE RECORDED`, and `UNKNOWN` in the required live fields (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:27-47`), and every evidence slot remains a commit-time placeholder (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:308-330`). V2's final boundary repeats that it is not the Stage-1 record until steps 1-15 produce and bind literal evidence (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:338-357`). The governing reconciliation requires a **concrete** allocation artifact and says that artifact does not exist (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70`).

The unresolved-token rule is useful: if actually executed, placeholders would make the candidate STOP (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:17-21,351-352`). It prevents this template from being mistaken for a populated record; it does not populate the record. The actual minted values, commands, streams, return codes, ledger rows, and commit bindings are **UNKNOWN**. They are settled only by the literal commit-time record and replayable evidence required by sections 2, 7, and 9.

## 2. Exact reason-token grammar: still bypassable

V2 materially improves the old substring test. `run_case` compares rc, selects the correct stream, constructs a complete expected line, and calls `require_one_exact_line` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:153-180`). Those expected tokens are independently specified by the successor, including the ten refusal representatives and the rule that an incorrect reason token is STOP (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`). The pinned predicate's actual spelling also matches the constructed acceptance/refusal lines (`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/01_RUNKIT/RP0-LIB.sh:11-13,85-93`).

But `require_one_exact_line` parses with Bash `read` and compares the resulting shell string (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:136-151`). Bash discards NUL bytes while reading into a variable. I extracted and invoked the exact function from those lines, without modifying it. Two deviant byte streams both returned acceptance:

```text
input: expected line with NUL embedded inside component_ok
EMBEDDED_NUL_RC=0

input: exact expected newline-terminated line followed by a bare NUL byte
TRAILING_NUL_RC=0
```

Therefore the claim that “any extra byte is rejected” is false (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:204`). The check fails for ordinary text differences, a second newline-terminated line, or a missing final newline; it does **not** fail for all byte differences. This is a concrete false-property/pass construction, not a typo.

Closure requires byte-level comparison of the complete stream (including length and NULs) against independently constructed expected bytes, plus RED evidence for embedded and trailing NUL mutations and GREEN evidence for the exact pinned output.

## 3. Collision completeness: the STOP is stated, but the semantic omission still passes

V2 honestly says it does not prove today's universe complete (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:206-210`). The actual canonical ledger path, authoritative remote snapshot, exhaustive operator archive, and their completeness are therefore **UNKNOWN**. The successor requires complete ledger history, every retained operator root, and the remote allocation ledger; checking two historical roots is explicitly insufficient (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`).

The proposed fail-closed path is textually reachable for a declared mismatch, missing file, bad hash, unreadable member, reparse point, or scan error (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:212-222,224-233`). If implemented, those conditions STOP before “no collision.” The harder case still bypasses it:

1. Let retained operator root `R` exist outside the selected archive.
2. Generate `operator_root_inventory` from that incomplete archive.
3. Commit a record asserting that the same archive and inventory are complete.
4. Hash the archive, inventory, record, and manifest consistently.

The observed enumeration equals the declared inventory, the hashes match, the record is committed, and the two mandatory historical roots can be present; all stated local comparisons pass while `R` remains outside the quantified universe. The remote snapshot has the same defect: a committed record *saying* the snapshot is authoritative/complete is not an independent derivation of completeness (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:214-220`). The expected universe still comes from the same bundle being checked. This is precisely the self-confirming-check defect: the check can pass by not looking (`MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:16-21,45-63`).

There is also a new reachability contradiction. The manifest must contain `parent_commit` equal to the clean `HEAD` from which allocation starts and must contain `manifest_commit`; the manifest and authority records must themselves be contained by that parent commit (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:210-222`). The checklist says to commit that manifest separately and then restart from the new clean parent (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:341-344`). A file cannot prerecord the hash of the Git commit whose identity depends on that file's final bytes. No non-self-referential envelope or post-commit derivation is defined. Thus the advertised compliant manifest pass path is not merely unproved; under the literal fields it is unattainable.

Closure requires (a) a non-self-referential manifest identity scheme, and (b) completeness evidence whose expected member set comes from an independently authoritative source, with an omission mutation such as `R` making the real gate STOP. A self-authored “complete” statement does not settle the fact.

## 4. Append-only: a real algorithm is described, but not yet enforced

V2 now names a meaningful mechanism. It derives expected parent bytes from the immutable Git object at `$ParentCommit:$LedgerRepoPath`, requires the working ledger to equal them, writes one validated LF-terminated row using append mode, and then checks exact length, parent prefix, and exact new-row suffix (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:272-284`). Full-chain validation is intended to reject duplicate/out-of-order row references, bad global links, and illegal identity transitions; post-commit blob checks repeat the prefix/suffix/chain test against committed parent and candidate objects (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:263-270,284-298`).

What would make that mechanism fail is concrete:

- an edit, deletion, truncation, or insertion in prior bytes breaks the parent-prefix/length equation;
- an extra or altered appended byte breaks the exact suffix equation;
- a duplicate, skipped sequence, wrong predecessor, or illegal state change breaks chain validation;
- committing different bytes breaks the recorded candidate blob/post-commit comparison.

That is substantially better than decorative prose because the expected prior bytes come from a separately committed parent object. However, V2 supplies no validator program, exact invocation, output, rc, or RED/GREEN mutation evidence; “validate” remains an imperative (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:274-286,308-330`). The canonical ledger path is itself **UNKNOWN** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:41-43`). Therefore the current artifact specifies enforcement but does not perform or prove it.

V2 also introduces an unresolved failure-recovery contradiction. It commands a `BURNED` append for any commit/order failure and says a failed initial append check “stops and burns” (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:300-304,347-350`). If the append itself left a partial/invalid suffix or the canonical commit/order binding failed, a valid chained `BURNED` row cannot necessarily be appended without first repairing or deleting bytes, which append-only forbids. The recovery operation and durable burn location for that case are **UNKNOWN**. Closure requires an executable verifier with falsified mutations and a preregistered recovery ledger/envelope that remains writable when the primary candidate is invalid.

## 5. Predicate binding: intended chain traced; same executed object not proved

The intended checked object and used object can be traced as follows:

```text
$PinnedRp0Lib (selected source path; actual value UNKNOWN)
  -> open with FileShare.Read
  -> read 18,968 bytes and verify fixed SHA-256
  -> write those verified bytes once to
     $QaDir\RP0-LIB.pinned.sh (actual path UNKNOWN)
  -> keep snapshot open with FileShare.Read
  -> re-read/hash snapshot before Bash
  -> caller is required to pass snapshot path as Bash $1
  -> Bash: lib=$1
  -> Bash: . "$lib"
  -> re-read/hash locked snapshot after Bash
```

The source-to-snapshot steps are specified at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:103-114`; the later consumer is concretely the Bash assignment and source operation at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:118-134`.

So the design intends the object checked immediately before execution to be the snapshot, and the object later sourced to be the pathname supplied as `$1`. But V2 contains no PowerShell caller that creates/holds the handle, launches Bash, passes that exact path, waits, and performs the post-hash. It also contains no transcript identifying the source path, snapshot path, handles/file identity, Bash argv, or hashes; those are deferred evidence slots (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:105-118,316-320`). Consequently, the object actually checked and the object actually opened by Bash are both **UNKNOWN**, and sameness is not proved by this artifact. A mandatory sentence that the caller “must” pass the snapshot is not caller reachability evidence; the declared-instrument pattern requires tracing the real accepting caller to the binding event (`MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895`).

Closure requires the exact executable caller and transcript, with the snapshot's stable filesystem identity/digest tied to the actual Bash argv/open operation, plus a mutation that passes the original or another file and demonstrates `PREDICATE_BINDING_STOP`. The final proof must show one concrete object identity on both sides, not merely the same future variable name.

## Independent new defects/gaps introduced by v2

1. **Required — NUL bypass in the exact-stream checker.** Reproduced above; contradicts the “any extra byte” claim (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:136-151,204`).
2. **Required — collision-manifest self-reference and self-authored completeness.** The manifest cannot honestly embed its own containing commit identity, and a manifest/archive plus a record asserting its completeness can agree while omitting a retained root (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:210-222,341-344`).
3. **Required — post-commit record binding is not defined non-self-referentially.** V2 requires the committed allocation-record blob to equal the completed pre-commit record, then says post-commit evidence must be “inserted or bound” by an unspecified non-self-referential mechanism (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:288-298,353-355`). The location, schema, and identity relation are **UNKNOWN**. Inserting the resulting commit/blob identity into the already committed record would change its bytes. An external preregistered envelope or derivation rule would settle it.
4. **Required — no safe burn path after a ledger append/commit failure.** V2 requires a burn precisely when the primary append chain may be invalid, but gives no append-only-compatible recovery surface (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:300-304,347-350`).
5. **Documentation gap — broken review citation name.** V2 repeatedly cites `W1_ALLOCATION_REVIEW.md` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_ALLOCATION_DRAFT_V2_2026-08-15.md:15,114,222,286`), but the committed artifact is `WPI_STAGE1_ALLOCATION_REVIEW_2026-08-15.md`. Whether `W1_...` was intended as an alias is **UNKNOWN**; replacing it with the real repo-relative path settles provenance.

## Bottom line

V2 is an honest and materially stronger **design template**, but it is not a populated allocation record. More importantly, two checks still pass without proving their claims: the byte grammar loses NULs, and collision completeness is derived from the same archive/authority bundle being checked. Append-only and predicate binding now have plausible designs, but their real executable callers, failure evidence, and concrete object identities do not exist in V2. The five prior findings are therefore not closed.
