NEEDS-REWORK

## Findings

### MUST-FIX-BEFORE-COMMIT — The required fields are named, but the required allocation record is not populated

Reconciliation row 3 requires a **concrete** `BASE`, P0/RO RUNIDs, stage IDs, `REMOTE_BASE`, confirmation token, operator root, collision/grammar results, and append-only allocation dispositions; it also says that artifact does not yet exist. (`AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-66`)

The identity-field names all appear in the draft: `BASE`/`BASE_RUN`, P0 and RO `RUNID`, P0 and RO `EV_STAGE_ID`, `REMOTE_BASE`, confirmation token, and operator record root. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:15-28`) The reconciliation names are explicitly rendered as `CONFIRM_TOKEN` and `OPERATOR_RECORD_ROOT`; these are renamings, not omissions, because the table and generator map each name to its value. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:26-28,53-55,67-69`) The stage IDs alone are already concrete as `p0` and `ro`; all minted identities and roots remain marked `MUST BE MINTED AT COMMIT TIME`. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:17-28`)

The required **results** are missing: every acceptance result is `MUST BE RECORDED AT COMMIT TIME`, every refusal result is `MUST BE RECORDED AT COMMIT TIME`, and every collision-result cell is `MUST BE RECORDED AT COMMIT TIME`. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:92-123,264-273`) The append-only row is also not concrete: its row reference and identities are placeholders, its initial successor identity is `UNKNOWN`, and the `SPENT` transition trigger is `UNKNOWN`. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:279-298`) The document itself accurately labels its current bytes `DRAFT TEMPLATE — NOT AN ALLOCATION` and says the real record does not yet exist. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:3,7`)

Do not commit these bytes as the spendable allocation record. First replace every commit-time placeholder and `UNKNOWN` with the actual minted value, actual transcript/result, resolved ledger/record identity, and concrete disposition rule required by the draft's own completion gate. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:308-323`)

### MUST-FIX-BEFORE-COMMIT — The grammar matrix does not enforce the successor's exact reason-token rule

The generator grammar and derivations match the successor: both specify the 15-byte UTC stamp, eight-lowercase-hex nonce, 29-byte base, and the same seven derived spellings. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:76-104`; `WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:13,36-55`) The ten refusal representatives also match the successor's input classes and expected return codes/tokens. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`; `WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:107-123,182-191`)

The executable checker diverges from that grammar contract. The successor makes a missing or incorrect reason token a STOP, but `run_case` accepts any output line that merely **contains** the expected token via `*"$expected_token"*`. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:135`; `WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:163-170`) Therefore text such as `not_component_ok` can satisfy the draft's token test even though it is not the exact `component_ok` reason token required by the grammar contract. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:163-180`)

Replace substring matching with a parser that requires the exact reason field/token emitted by the pinned predicate, rejects conflicting or extra reason tokens, and records the literal per-case invocation with stdout, stderr, and rc as required by the successor. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:116-135`)

### MUST-FIX-BEFORE-COMMIT — The collision check is only real over an unproved, potentially incomplete declared universe

The procedure would detect literal occurrences in the two supplied record files, operator-path names, operator content visible to `rg`, and an already-existing exact candidate operator root. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:225-259`) It also states the correct collision disposition: burn the base and both RUNIDs, do not reuse them, and generate fresh identities under a new preregistration. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:275,293-298`; `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

That is not yet a global collision proof. The canonical ledger path and its historical completeness are `UNKNOWN`, and the authoritative retained remote-allocation record and its completeness proof are also `UNKNOWN`. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:204-212`) The code searches only the current contents of the two supplied files with `Select-String`; it contains no operation that traverses or verifies the complete ledger history it claims to cover. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:228-243,266-270`) The operator-content scan uses `rg --hidden` without a no-ignore option, so ignored content is outside that command's declared scan even though the result table claims all retained operator record contents. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:245-254,271-272`) The successor requires the complete ledger history, every later retained operator record root, and the remote allocation ledger, and says two historical roots alone are not a global proof. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-145`)

Before commit, name the canonical ledger and remote-allocation record, prove each is complete for the required history, inventory every retained operator root, make the content scan include ignored files while failing closed on unreadable content, and record the exact inputs, commands, outputs, and return codes. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:208-216,264-275,311-318`)

### MUST-FIX-BEFORE-COMMIT — Append-only is asserted, not enforced

The draft says existing rows are never edited or deleted and that state changes append a row referring to the prior row, but it supplies only a Markdown row template and prose transition table. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:279-298`) Its checklist likewise instructs the operator to append `BURNED` or `RESERVED`, but defines no append operation, no prior-byte/prefix check, no parent-versus-candidate diff rule, no row-reference validator, and no rejection mechanism for edits or deletions. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:318-320`) This does not enforce the successor's committed append-only-ledger requirement. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

Make the property mechanical before commit: resolve the canonical ledger path; pin the parent ledger identity; require the candidate ledger to preserve every prior byte/row and add only valid chained rows; reject duplicate row references, mutation, deletion, or truncation; and emit the verification command, output, and rc into the allocation record. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:137-147`)

### MUST-FIX-BEFORE-COMMIT — The checked predicate object is not bound to the object later sourced

The draft hashes `$PinnedRp0Lib` in one block, then later starts Bash and sources that same pathname, with no second identity check or immutable-copy binding between the hash and the source operation. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:76-88,124-147,194-196`) The successor requires the exact 18,968-byte, pinned-SHA object to be verified before its predicate is sourced. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`) Bind the QA run to immutable bytes or re-verify the exact object immediately around sourcing and preserve that binding in the transcript. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:78-88,194-202`)

### NOTE — The draft does not invent a live minted identity

No concrete live `UTCSTAMP`, nonce, base, RUNID, confirmation token, remote base, or operator root is presented as already minted; those fields are explicitly deferred to the real allocation session. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:3,15-28`) The concrete `p0`/`ro` stage IDs and the root formulas are sourced by the baseline preregistration: it defines `p0`/`ro`, `/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>`, and `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>`. (`WPI_PREREGISTRATION_DRAFT.md:113-129,675-690`) The pinned predicate's byte count and SHA-256 are also stated by the successor, not introduced without a source by this draft. (`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:98-104`; `WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:76-87`)

The honest `UNKNOWN` labels avoid fabricated identities, but they are unresolved blockers rather than acceptable committed values. (`WPI_STAGE1_ALLOCATION_DRAFT_2026-08-15.md:80,210-212,289-298`)
