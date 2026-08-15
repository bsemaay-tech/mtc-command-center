NEEDS-REWORK

# W4 adversarial review — R16 and R23 freeze procedures

## Bottom line

The document distinguishes the ceremonies correctly in prose: R16 is the pre-WP-A checkpoint used by Audit 2, while R23 is the later post-WP-A exact-release freeze used by Audit 3/Gate 6; the work catalogue independently places R16 before Audit 2/WP-A and R23 after WP-A. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:10-21`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-63`

The executable contract does not preserve that distinction reliably. R23 repeatedly says to run R16 steps whose code retains R16-only variables, guards, output names, and conclusions, and R23 does not bind the prior R16 manifest or the accepting Audit-2 close that distinguishes its moment. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:223-249,383-386,423-435,467-484,543-565`

## Required findings

### F1 — R23 is not an executable, ceremony-specific procedure

R23-3 says to “Run R16-3,” but literal R16-3 requires `$Packet9Close` and `$Packet9Index` and rejects a scope lacking them; R23’s input block defines neither variable and instead defines `$Audit2Close`, WP-A evidence inputs, a discard record, and a WP-A artifact identity. A fresh literal R23 run therefore lacks required variables; an operator who edits the inherited step must invent the substitutions. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:223-249,423-435,476-484`

R23-6 says to run R16-5 twice, but R16-5 hard-codes `$ResolvedCandidate`, `R16_CANDIDATE_TO_FREEZE.patch`, and R16-specific conclusion text. R23 names two desired comparisons but supplies no exact parameter assignments or standalone code, and it requires “corresponding identity rows” that R16-5 never produces for the before side. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:282-308,543-556`

R23-2 likewise inherits a table whose row label is hard-coded as `R16_BASE_TO_FREEZE`; merely renaming the two files does not change that embedded ceremony identity. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:194-209,467-474`

Required repair: provide standalone R23 commands, or genuinely parameterized helpers with mandatory `freeze_kind`, comparison endpoints, output names, row labels, required-role set, and conclusion text; fail if an R16 role/label is used in R23 or vice versa. This repair is required by the mismatches above. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:194-209,223-249,467-484,543-565`

### F2 — the two moments can be confused despite the prose warning

The clearest confusion point is R23-3: at the R23 moment, a future reader is explicitly told to apply the R16 scope procedure, including its Packet-9 guard, rather than an R23 guard for the accepting Audit-2 close, WP-A evidence, discard record, and final artifact. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:223-249,376-406,476-484`

The second confusion point is the R16 identity itself. R23 accepts `$R16FreezeSha` as a supplied string, resolves it, and proves only that it is an ancestor of R23; it does not take the verified R16 manifest path/identity as an input or recompute that manifest. Any ancestor can therefore satisfy the implemented “R16” check while being the wrong checkpoint. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:423-460,567-579`

The third confusion point is `$Audit2Close`: R23 declares the path, but no command consumes it, no scope guard requires it, and the final-manifest instructions cannot bind a record that no preceding R23 step writes into `$Out`. The procedure can therefore create an R23-shaped bundle without mechanically establishing the accepting Audit-2 boundary that separates R16 from R23. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:383-386,423-435,440-565`

Required repair: bind the prior R16 manifest by explicit path, `RAW_EXTERNAL_FILE` identity, detached-identity verification, and extracted full SHA; bind the accepting Audit-2 close by explicit identity and require it in the R23 manifest before any R23 output is publishable. The upstream contract requires proof that Audit 2 accepted before WP-A, not merely a named path. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:81-83`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:383-386,423-435`

### F3 — not every identity is unambiguous or even present

The procedure states that every frozen identity table must name its derivation mode because `* text=auto` permits different Git-object and Windows working-tree bytes, and the prior defect record says a bare bytes/SHA-256 pair on a repository Markdown file is ambiguous by construction. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:23-37`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27,59-64`

The R16 base-diff identity table violates its own rule: its published header contains `patch_bytes` and `patch_sha256` but no derivation-mode field, even though the transient object used to construct it was labelled `RAW_EXTERNAL_FILE`. R23-2 inherits that table shape. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:194-209,467-474`

R23’s trigger requires its prerequisite records to be identified only by path/bytes/SHA-256, with no derivation mode. The evidence-index and discard rows later gain `RAW_EXTERNAL_FILE`, but the repo-relative `$Audit2Close` receives no byte count, SHA-256, blob OID, or mode anywhere. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:380-386,423-435,486-510`

Whether the future Audit-2 close record is tracked text is **UNKNOWN**; its final path and storage form would settle that. If it is tracked text, the contract must record `GIT_OBJECT` with blob OID and, if consumed from a checkout, `WORKTREE_RAW`; if it is external, it must record `RAW_EXTERNAL_FILE`. The present procedure supplies none of those identities for it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:30-37,380-386,423-435`

R23 reduces both `$WpaEvidenceIndex` and `$DiscardRecord` to basenames in the order-record identity table, losing the source-root/path namespace. Two distinct source paths with the same basename are not distinguishable by the recorded path field. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:502-510`

Required repair: every identity row, including diff records, close records, input TSVs, evidence roots/indexes, order records, and detached manifests, must carry an explicit mode and canonical path namespace; tracked text must carry a blob OID, and external identities must preserve an immutable root identity plus root-relative path. This follows the standing derivation rule and the missing fields above. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:48-64`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:194-209,380-386,502-510`

### F4 — the R16 unchanged statement is narrow; the overall unchanged-bits guarantee can pass after changes

R16’s generated sentence is falsifiable only for Git blobs at the externally listed `artifact`/`manifest` paths: it derives `$candidatePaths` from `$ScopeInput` and runs `git diff --quiet` on those paths. The sentence itself correctly says “listed tracked artifact/manifest Git blobs,” not all scope files and not prior materialized artifact bytes. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:282-308`

The external `R16_SCOPE_AND_IDENTITIES.tsv` is parsed but never copied into `$Out`, hashed, or placed in the freeze manifest; the manifest enumerates only files already in `$Out`. The auditor is told to inspect the “adopted scope input,” but the bundle does not bind which bytes were adopted. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:146-166,223-249,314-328,357-368`

Consequently, R16 can report `UNCHANGED` while an omitted relevant path changed, or while the scope-input bytes presented later to the auditor differ from the bytes used by the freezer. The code proves equality only over the supplied listed set and has no independent authoritative-universe comparison. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:148-154,223-249,282-308,357-363`

R16 also records `WORKTREE_RAW` only at the freeze side; it has no candidate-side `WORKTREE_RAW` baseline. Because the documented repository failure mode permits Git-object LF bytes and Windows working-tree CRLF bytes to differ, a zero Git diff does not prove equality to an earlier materialized raw candidate artifact. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:23-37,238-247,282-308`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27`

Required repair: freeze and manifest the exact scope-input bytes; derive the scope from an independently identified authoritative universe; compare the frozen set against that universe for omissions/extras/duplicate roles; and publish before/after identities in the relevant mode for every path covered by an unchanged conclusion. The upstream Packet-10 contract requires every in-scope file and every final artifact/manifest identity. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-61`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:146-154,282-308`

### F5 — R23 can report the WP-A artifact unchanged by comparing against the freezer’s own assertion

The expected WP-A artifact path, byte count, and SHA-256 are operator-supplied variables; R23-5 compares the current materialized artifact only with those supplied values. No command extracts the expected identity from `$WpaEvidenceIndex`, validates a unique index row, or binds that row to `$WpaArtifactPath`. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:423-435,517-534`

Thus a freezer can set `$WpaArtifactBytes` and `$WpaArtifactSha256` to the current final artifact and obtain `match=True` even if the actual WP-A-tested identity was different. The generated match is a self-consistency check, not proof of continuity from WP-A. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:519-534`

The same temporal gap exists for evidence: R23 enumerates and hashes the evidence root only at freeze time, while the procedure supplies no prior immutable snapshot/root identity against which to prove that the evidence bytes have remained unchanged since capture. Calling the input “immutable read-only” is an input assertion, not a demonstrated transition. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:423-435,486-510`

The trusted WP-A artifact-identity source and its machine-readable extraction rule are **UNKNOWN** in this procedure. A finalized evidence-index schema, exact unique-row selector, immutable capture-time root identity, and reproduction command would settle it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:400-406,423-435,517-534`

Required repair: derive the expected WP-A artifact identity from the independently frozen capture-time evidence/index, reject zero or multiple matching rows, preserve that source row’s identity, and compare it to both the R23 `GIT_OBJECT` and `WORKTREE_RAW` identity appropriate to the artifact. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:476-510,517-541`

### F6 — auditor verification is strong for recomputation but weak for truth and completeness

The auditor sections genuinely require independent worktrees and independent recomputation of commit identities, diffs, trees, blob identities, raw identities, evidence-file hashes, and freeze manifests; those are real verification steps rather than acceptance of the freezer’s arithmetic. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:338-368,567-598`

The auditor cannot independently establish scope completeness from the procedure because the purported authoritative universe is the unbound adopted scope input itself; checking that table for omissions accepts the freezer/Lead’s chosen universe. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:131-138,146-154,357-363,400-406`

The R23 auditor is told to verify chronology “from the frozen order records.” Hashing those records proves their current bytes, not that the recorded events occurred in that order; the procedure defines no independent event source or cross-record ordering calculation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:389-392,486-510,580-589`

The R23 auditor’s independent artifact comparison is also underspecified because the procedure never defines how the auditor derives the trusted WP-A-tested bytes/SHA-256 independently of the supplied values. Without that derivation, the auditor can repeat the freezer’s assertion rather than verify it. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:423-435,517-534,590-594`

Required repair: give the auditor independently identified source roots and manifests, a frozen authoritative scope universe, a bound Audit-2 close, machine-verifiable chronology fields and comparisons, and a normative derivation of the WP-A-tested artifact identity. Copied digest strings alone are already declared insufficient by the audit input contract. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:65-70`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:357-368,580-598`

## Direct answers

1. **Can the two freezes be confused? Yes.** The prose boundary is clear, but R23-2/R23-3/R23-6 instruct the reader to reuse R16 steps with R16-specific state, and the implemented R23 ancestry check does not prove that its supplied base is the verified R16 freeze. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:17-21,194-209,223-249,423-484,543-556`
2. **Is every identity unambiguous? No.** The base-diff table omits its mode; the R23 prerequisite-record contract uses bare path/bytes/SHA-256; the Audit-2 close has no identity; and order-record paths are reduced to basenames. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:194-209,380-386,423-435,502-510`
3. **Is unchanged-bits falsifiable? Only in narrow subchecks.** R16 can falsify equality of listed Git blobs, and R23 can falsify equality to supplied expected values, but neither proves the broader continuity claim when the scope universe is unbound and the WP-A expected identity is operator-supplied. A freeze can pass while omitted, raw-materialized, capture-time evidence, or actually WP-A-tested bits changed. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:146-166,282-308,423-435,486-534`
4. **Does the auditor verify independently? Partly.** It independently recomputes hashes/diffs/trees, but it accepts the freezer/Lead’s scope universe, reads chronology from freezer-bound narrative records, and lacks an independent derivation for the expected WP-A artifact identity. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:338-368,567-598`

## Estimate and boundary

**NO SOURCED ESTIMATE.** The work catalogue and the procedure both state that neither R16 nor R23 has a sourced disjoint estimate; they direct future operators to time the completed procedures. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55,62`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:370-374,600-605`

This review grants no acceptance or authorization; the reviewed procedure likewise states that it creates no verdict, authority, host action, or deployment action. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/FREEZE_PROCEDURES_2026-08-15.md:3-8`
