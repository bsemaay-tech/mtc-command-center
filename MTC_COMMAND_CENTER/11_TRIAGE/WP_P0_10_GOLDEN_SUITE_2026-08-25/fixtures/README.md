# WP-P0-10 deterministic golden fixtures

This directory is a new data-only corpus. It does not overwrite or recapture any existing parity corpus.

Each built family has one JSON fixture containing literal configuration, frozen metadata, normalized bars (or an empty list for static validation), cited expected-output assertions, a canonical output SHA-256, a final-state SHA-256, and one GF field-8 source-mutation descriptor. Expected values come from the cited WP-P0-09 row, never from executing A, B, Pine, or future kernel code.

The comparison seam is deliberately narrow: a future subject normalizes its result to an object whose keys are the fixture assertion paths. Canonical bytes are UTF-8 JSON with sorted keys, compact separators, and one LF terminator. The local verifier changes one copied expected-output path and confirms that the fixture comparator detects the mismatch and returns to byte identity after restoration. These are **fixture-contract self-consistency checks only**. They do not execute a producer or the GF field-8 source mutations.

**D026 is UNEARNED for all 23 built families.** It remains unearned until WP-P0-11/WP-P0-12/WP-P0-20 deliver the canonical kernel subjects and each GF field-8 source mutation is demonstrated against the exact pre-fix behaviour (or an equivalent producer mutation) and then with the fix present. The local mismatch/restoration counts must not be cited as D026 evidence.

Run the fixture-local verifier from the repository root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_verify_output
```

The verifier contains no economic implementation. It validates the complete manifest and file set with explicit, optimization-safe checks; validates that each cited line range exists and has a structurally matching WP-P0-09 C/GF, cross-cutting-rule, or explicit-non-decision label; verifies the LF-normalized authority hash and the two manifest-local hashes for each fixture; checks the stored output/state hashes; and checks the named arithmetic and idempotence relationships for families 4, 5, 22, and 24.

Those two fixture hashes are self-consistency checks, not an external trust anchor: both stored hashes live in `manifest.json`. A coordinated fixture edit plus recomputation of both hashes is therefore not detected unless one of the independent coherence checks rejects it. At audit fixed point `c05e5968`, coherence validation covered 24 of 230 expected values and left 206 unchecked. This repair adds 11 coverage assertions without extending `validate_coherence`, so the current scope is 24 of 241 expected values; a self-consistent rehash outside those 24 values is not detected. Named follow-up `WP-P0-10-COHERENCE-217` covers the 217 current values outside coherence validation.

Likewise, the summary counter `citation_line_ranges_validated` proves only syntax, existence, and the structural label/range checks above. It does not prove that a cited row is relevant to, or decides, the assertion carrying it. The counter was renamed instead of adding a family-to-row binding because the current corpus has no sound machine-readable relevance map from which such a rule could be derived.

Optimized Python is deliberately forbidden because `-O` strips language-level assertions. The verifier exits nonzero before reading inputs when `__debug__` is false.

Run the committed tamper regression harness from the repository root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
```

It executes the clean corpus and seven isolated temporary tamper copies: GF-08's bug quantity with inverted descriptor polarity and recomputed internal hashes, a fabricated citation range, three cross-field contradictions, and the manifest-count corruption under normal and optimized Python.

`manifest.json` enumerates all 25 binding families. Families 18 and 19 have no JSON fixture because WP-P0-09 explicitly does not decide their required `SNAPSHOT_MISMATCH` and `REFERENCE_DIVERGENCE` semantics. Their blockers and unblock conditions are recorded in the manifest and lane report.

Family 1 references the existing 858-event Bridge/QuantLens corpus as a companion and labels it `ENTRY SIGNAL GOLDEN`; it does not copy, modify, or broaden that corpus.
