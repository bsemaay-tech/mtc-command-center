# WP-P0-10 deterministic golden fixtures

This directory is a new data-only corpus. It does not overwrite or recapture any existing parity corpus.

Each built family has one JSON fixture containing literal configuration, frozen metadata, normalized bars (or an empty list for static validation), cited expected-output assertions, a canonical output SHA-256, a final-state SHA-256, and one GF field-8 source-mutation descriptor. Expected values come from the cited WP-P0-09 row, never from executing A, B, Pine, or future kernel code.

The comparison seam is deliberately narrow: a future subject normalizes its result to an object whose keys are the fixture assertion paths. Canonical bytes are UTF-8 JSON with sorted keys, compact separators, and one LF terminator. The local verifier changes one copied expected-output path and confirms that the fixture comparator detects the mismatch and returns to byte identity after restoration. These are **fixture-contract self-consistency checks only**. They do not execute a producer or the GF field-8 source mutations.

**D026 is UNEARNED for all 23 built families.** It remains unearned until WP-P0-11/WP-P0-12/WP-P0-20 deliver the canonical kernel subjects and each GF field-8 source mutation is demonstrated against the exact pre-fix behaviour (or an equivalent producer mutation) and then with the fix present. The local mismatch/restoration counts must not be cited as D026 evidence.

Run the fixture-local verifier from the repository root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_verify_output
```

The verifier contains no economic implementation. It validates the complete manifest and file set with explicit, optimization-safe checks; resolves all cited line ranges into the exact WP-P0-09 C/GF or cross-cutting rule; verifies the LF-normalized authority hash, per-fixture semantic hash, and authority-binding hash; checks the stored output/state hashes; and checks the named arithmetic and idempotence relationships exercised by the audit tampers. The authority binding covers every expected path/value paired with the exact cited line-fragment hashes, so rehashing a changed fixture does not make it authoritative.

Optimized Python is deliberately forbidden because `-O` strips language-level assertions. The verifier exits nonzero before reading inputs when `__debug__` is false.

Run the committed tamper regression harness from the repository root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
```

It executes the clean corpus and seven isolated temporary tamper copies: GF-08's bug quantity with inverted descriptor polarity and recomputed internal hashes, a fabricated citation range, three cross-field contradictions, and the manifest-count corruption under normal and optimized Python.

`manifest.json` enumerates all 25 binding families. Families 18 and 19 have no JSON fixture because WP-P0-09 explicitly does not decide their required `SNAPSHOT_MISMATCH` and `REFERENCE_DIVERGENCE` semantics. Their blockers and unblock conditions are recorded in the manifest and lane report.

Family 1 references the existing 858-event Bridge/QuantLens corpus as a companion and labels it `ENTRY SIGNAL GOLDEN`; it does not copy, modify, or broaden that corpus.
