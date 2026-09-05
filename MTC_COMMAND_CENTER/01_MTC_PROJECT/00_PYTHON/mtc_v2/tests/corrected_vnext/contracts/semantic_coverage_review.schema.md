# Semantic coverage review receipt

`semantic_coverage_review.schema.json` is the closed receipt contract for the mandatory design
section-16 review. The receipt-level `schema` value is fixed to
`P012_SEMANTIC_COVERAGE_REVIEW_V1`. Unknown members are invalid.

## Review items

The keys `1` through `6` preserve the design order. The text below is verbatim from the live
`P012_FRESH_DESIGN_V1.md` section 16:

1. Re-derive every formula in sections 7-14 from this design and its named authority; compare it with both code and expected tables, inspect the exact `CONTRACT_TABLES` authoring path/import graph and `IMPLEMENTATION_ANCHOR` ancestry, and confirm the named author is independent from the kernel implementer.
2. Review every kernel diff hunk by the shape census in section 18; map it to exactly one DEF or classify/refuse it as undocumented.
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
- computed bundle `EXPECTED_SEAL_SHA`;
- `implementation_anchor.json` SHA-256;
- baseline `BASELINE_BYTES_MANIFEST.json` SHA-256;
- live design-file SHA-256 and the version parsed from its heading.
- `verify_bceg.py` harness SHA-256;
- `scenario_catalog.json` SHA-256.

`owner_ratification.chain` is exactly `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, `#11`, `#12`,
`#12b`, `#13`, `#14`, `#14b`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, and
`#22`, in that order. `ratified` must be true, and `signed_at` must be a timezone-qualified
date-time.
