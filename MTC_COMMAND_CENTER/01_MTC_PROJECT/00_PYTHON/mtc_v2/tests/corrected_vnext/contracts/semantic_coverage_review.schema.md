# Semantic coverage review receipt

`semantic_coverage_review.schema.json` is the closed receipt contract for the mandatory design
section-16 review. The receipt-level `schema` value is fixed to
`P012_SEMANTIC_COVERAGE_REVIEW_V2`. V1 and unknown members are invalid.

## Review items

The keys `1` through `6` preserve the design order. The text below is verbatim from the live
`P012_FRESH_DESIGN_V1.md` section 16:

1. Re-derive every formula in sections 7-14 from this design and its named authority; compare it with both code and expected tables, inspect the exact `CONTRACT_TABLES` authoring path/import graph and `IMPLEMENTATION_ANCHOR` ancestry, and confirm the named author is independent from the kernel implementer.
2. Review every kernel diff hunk of the exact ordered raw bytes from `git diff --relative --unified=0 --no-ext-diff --no-textconv --no-renames --diff-algorithm=myers --no-indent-heuristic 5e8e579410ee55008bfd2d2d85054fd1d782f32c..<reviewed-head> -- core`; embed one V2 `hunk_coverage` object in Item 2. It carries base/head, exact canonical command, whole-diff SHA-256, changed path/file totals, per-path hunk counts and identities, all S18-01..S18-12 assignment/coverage rows, and one ordered record per physical hunk. The gate derives served DEF sets and exact module-to-Section-18-row bindings from exact design bytes and SHA-256 pinned by `CONTRACT_TABLES_MANIFEST.json`, then recomputes all paths, hunks, assignments, ranges, ordering, and digests; every hunk's asserted row must own that hunk's module path in section 18. V1, missing/duplicate/malformed/drifted data, duplicate ownership, and UNDOCUMENTED hunks refuse; external evidence paths never satisfy Item 2.
3. Review scenario catalog boundaries and correction interactions, explicitly looking outside the finite cases.
4. Review the grid/record lineage for every production number and confirm section 19 resolution evidence.
5. Inspect for economic state carried across modules/containers or external consumers that the static shape census could miss.
6. Inspect event/schema additions for missing consumers, overwrite, duplicate identity, or silently dropped members.

Each item has one terminal `disposition`, at least one `evidence_paths` member that exists when the
gate runs, and `notes`. Relative evidence paths are resolved from the `mtc_v2` root supplied to
`verify_bceg.py`; absolute local paths are also accepted. `REFUSED`, `NOT_VERIFIED` in a
disposition or note, a missing item, or a non-empty `unresolved_items` list refuses acceptance.

## Independence and identities

`reviewer.independent_of` has exactly two ordered entries: `KERNEL_IMPLEMENTER`, then
`CONTRACT_TABLES_AUTHOR`, each with a non-empty one-line basis. A Codex- or Claude-family reviewer
is invalid because those are the kernel-implementer and tables-author families for this package.

The signature covers the engine, the answer sheets, the reference and the design as they were;
adding the signature file itself, or a report, does not void it; changing any of those five does.
`worktree_head_commit` is required information that records when the review happened. It must be a
Git OID and an ancestor of the current `HEAD`, but it does not have to equal the current `HEAD`.
The gate compares the content identities with fresh measurements from the run:

- `mtc_v2/core` tree OID at `HEAD`;
- the `mtc_v2/core` tree OID at `worktree_head_commit`, which must equal the current `core` tree
  OID so later core drift refuses;
- computed bundle `EXPECTED_SEAL_SHA`;
- `implementation_anchor.json` SHA-256;
- baseline `BASELINE_BYTES_MANIFEST.json` SHA-256;
- live design-file SHA-256 and the version parsed from its heading.
- `verify_bceg.py` harness SHA-256;
- `scenario_catalog.json` SHA-256.

Item 2 carries an embedded V2 semantic hunk receipt with schema
`P012_KERNEL_HUNK_COVERAGE_V2`; separate evidence files, including the superseded
`P012_KERNEL_HUNK_COVERAGE_V1` ledger, never satisfy Item 2.
Its `base_commit` is fixed to `5e8e579410ee55008bfd2d2d85054fd1d782f32c`, its `reviewed_head` must
equal `reviewed_identities.worktree_head_commit`, and its `diff_command` must equal the exact
canonical command. The gate recomputes the diff from Git and refuses a wrong base, head, command, or
whole-diff SHA-256, binary/rename/submodule/unparsed/no-hunk diffs, empty/extra/missing/duplicate/
reordered/stale hunk records, malformed or mixed class payloads, and any UNDOCUMENTED core hunk.

The `hunk_coverage` object is closed at every nested level. `changed_paths` records require exactly
`path`, `hunk_count`, `hunk_indices`, and `hunk_sha256s`. `section18_coverage` requires exactly one
ordered row for each `S18-01` through `S18-12`, with nonnegative integer indices and DEF ids from
`DEF-P012-01` through `DEF-P012-08`. Each hunk is exactly one of `DEF`, `SECTION18_SHARED`, or
`UNDOCUMENTED`, with only its class-specific payload; paths, counts, indices, Git OIDs, and SHA-256
values have fixed types and formats. The Python gate additionally checks recomputed ranges, ordering,
counts, assignments, and digest identity.

`owner_ratification.chain` is exactly `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, `#11`, `#12`,
`#12b`, `#13`, `#14`, `#14b`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`,
`#22`, `#23`, `#24`, `#25`, `#26`, `#27`, `#28`, `#29`, and `#30`, in that order. `ratified` must be true, and `signed_at` must be a timezone-qualified
date-time.
