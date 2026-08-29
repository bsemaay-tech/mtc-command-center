# Owner decisions — 2026-08-29 afternoon (verbatim + mapping)

Owner's message (verbatim): "1. yes / 2. yes / 3. yes / P0-12 kernel approved / try and find
more paralel wor. all paralel work is approved and mandatory"

The numbered answers are to the three questions of
`OWNER_DECISION_P011_HASH_FORM.md` (delivered this morning, hash-verified by G10):

| Q | Decision | Effect |
|---|---|---|
| 1 | **YES — Option 1** | The frozen Git blob identity becomes the acceptance identity for text inputs in the v3 receipt and the future v3 owner-signed anchor; v1/v2 anchors preserved byte-for-byte. Blocker 10 RESOLVED by decision. |
| 2 | **YES** | Machine strings (Python path, build strings, platform) move out of the hashed baseline into a labelled diagnostic record. Blocker 5 treatment APPROVED. |
| 3 | **YES** | A different actor's clean-checkout rebuild + verification is required before the owner signs the v3 anchor. Blocker 11 contract APPROVED. |

Additional decisions:

- **"P0-12 kernel approved"** — WP-P0-12 (`CORRECTED_VNEXT`, T0, protected strategy kernel) has
  its owner G-word. Build starts only after WP-P0-11 acceptance (its stated dependency);
  design work starts now.
- **"All parallel work is approved and mandatory"** — standing G1-IA-style authorization for
  parallelizable Phase-0 work that respects existing gates and protected-surface rules. Lead
  reading, recorded here for audit: this authorizes starting design/paper/prep lanes and
  cap-stopped closures (WP-P0-15 closure, V-Next amendment closure from 2026-08-24), and does
  NOT waive per-package protected-surface gates, host/broker/ARM gates, or the dependency
  chain 11 -> 12 -> 20 -> 13 -> 31M1 -> 14 (verified against the master plan: P0-31 M1's inputs
  include the P0-13 catalog, so it is chain-bound too).

Blocker 2 (code writes the owner's signature) remains OPEN — not covered by these answers; the
v3 design revision must keep the owner-signs-personally boundary.
