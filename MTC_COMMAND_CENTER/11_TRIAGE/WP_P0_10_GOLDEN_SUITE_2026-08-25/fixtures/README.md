# WP-P0-10 deterministic golden fixtures

This directory is a new data-only corpus. It does not overwrite or recapture any existing parity corpus.

Each built family has one JSON fixture containing literal configuration, frozen metadata, normalized bars (or an empty list for static validation), cited expected-output assertions, a canonical output SHA-256, a final-state SHA-256, and one single-field deliberate mutation. Expected values come from the cited WP-P0-09 row, never from executing A, B, Pine, or future kernel code.

The comparison seam is deliberately narrow: a subject normalizes its result to an object whose keys are the fixture assertion paths. Canonical bytes are UTF-8 JSON with sorted keys, compact separators, and one LF terminator. A mismatch names the exact path, expected value, and candidate value. The mutation proof changes one candidate-output path and must yield exactly one mismatch; restoration must produce byte identity.

Run the fixture-local verifier from the repository root:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_verify_output
```

The verifier contains no economic implementation. It validates the data contract, citation presence, stored hashes, and the one-field comparison sensitivity that future kernel subjects must satisfy.

`manifest.json` enumerates all 25 binding families. Families 18 and 19 have no JSON fixture because WP-P0-09 explicitly does not decide their required `SNAPSHOT_MISMATCH` and `REFERENCE_DIVERGENCE` semantics. Their blockers and unblock conditions are recorded in the manifest and lane report.

Family 1 references the existing 858-event Bridge/QuantLens corpus as a companion and labels it `ENTRY SIGNAL GOLDEN`; it does not copy, modify, or broaden that corpus.
