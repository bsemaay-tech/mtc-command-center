# WP-L/B3 record identity sweep — 2026-08-12

Analyst: Codex (the kickoff was explicitly re-routed from GLM after the large-scope
GLM timeout). Scope: identity and provenance only. No WP-L file, Git state, host, or
network was modified or contacted.

## Verdict

**FULL SWEEP COMPLETED.** I parsed all 198 artifact rows under the nine numbered
sections of `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md`, read
each named file from the current working tree, and independently recomputed its byte
count and SHA-256. No indexed path was left pending.

The populated working tree is substantially intact: **197/198 identities match both
indexed fields**. The only mismatch is a **documented post-index append**, not
undocumented drift. There are **zero missing artifacts in this working tree**, but the
three evidence logs are untracked; a fresh clone will omit exactly those three, so the
closure evidence is not clone-complete.

| Measure | Result |
|---|---:|
| Artifacts checked | 198 / 198 |
| Identities matching (bytes and SHA-256) | 197 |
| Documented changes | 1 |
| Undocumented drift | 0 |
| Missing artifacts in this working tree | 0 |
| Indexed artifacts untracked by Git | 3 |
| `PENDING-LEAD-EXECUTION` | 0 |

## Coverage and method

Sweep order was the index order: `01_RUNKIT` (17), `02_PREREG` (15),
`03_TRANSPORT` (38), `04_PREREG_R45B` (6), `05_TRANSPORT_R45B` (16),
`06_B3_REPAIR` (43), `07_RUNKIT_B` (19), `08_PREREG_B3B` (12), then
`09_TRANSPORT_B3B` (32). For every table row matching the index's
`file | bytes | sha256` schema, I resolved the path below the named section, required a
regular file, read its current length, computed SHA-256 from its current bytes, and
compared both values to the row. The parsed row total was exactly 198.

This is a current-working-tree sweep. It does not claim that a fresh Windows checkout
would preserve these bytes; the separate `.gitattributes` durability analysis already
establishes that risk.

## Identity results by section

| Section | Checked | Full match | Documented change | Undocumented drift | Missing here |
|---|---:|---:|---:|---:|---:|
| `01_RUNKIT` | 17 | 17 | 0 | 0 | 0 |
| `02_PREREG` | 15 | 15 | 0 | 0 | 0 |
| `03_TRANSPORT` | 38 | 38 | 0 | 0 | 0 |
| `04_PREREG_R45B` | 6 | 6 | 0 | 0 | 0 |
| `05_TRANSPORT_R45B` | 16 | 16 | 0 | 0 | 0 |
| `06_B3_REPAIR` | 43 | 43 | 0 | 0 | 0 |
| `07_RUNKIT_B` | 19 | 19 | 0 | 0 | 0 |
| `08_PREREG_B3B` | 12 | 12 | 0 | 0 | 0 |
| `09_TRANSPORT_B3B` | 32 | 31 | 1 | 0 | 0 |
| **Total** | **198** | **197** | **1** | **0** | **0** |

## Documented change

File:
`09_TRANSPORT_B3B/STAGE3B_B3B_RECORD.md`

- Indexed identity: **4,488 bytes**;
  `adc9a4947a5475abacf019c2045b6ad90c0c9a829b54c9aa702c82cf9e0b45f7`.
- Recomputed current identity: **4,901 bytes**;
  `f9cf17bf324402f87fc4a6a66513fe55f19d0d4c35006b16b3044cd4ba1a48ea`.
- Classification: **DOCUMENTED CHANGE**.
- Explanation: `INTEGRITY_VERIFICATION_2026-08-10.md`, under “One
  record-keeping gap found and fixed,” says the B3B record omitted the individual
  `b3b.log` digest and that the digest and byte count were then added inline. Git commit
  `9370a1de1ca5b64c5f71b43c74e6c4f6f9c89654` shows exactly that six-line append and
  no other change to this record.
- Index disposition: **not updated**. `EVIDENCE_INDEX.md` still carries the pre-append
  identity, so its claim to describe every current indexed artifact is stale by one row.

There is no undocumented identity drift among the other 197 rows.

## Untracked evidence logs and clone completeness

All three indexed evidence logs exist in this working tree and match their indexed byte
counts and hashes:

| File | Indexed and recomputed identity | Git state |
|---|---|---|
| `03_TRANSPORT/operator_record/evidence/WPLP2-20260809T125940Z-8dc78f08-B3/b3.log` | 1,784 bytes; `079d6ac9f345b10ec333768203887ae52de9d6be89f0c5c4031a68353c4424a1` | untracked |
| `05_TRANSPORT_R45B/operator_record/evidence/WPLP2-20260809T125940Z-8dc78f08-R45B/r45b.log` | 4,521 bytes; `00078e7ea5caeca69a2468226c3fb1ec180153b74000151243335586363c4e0d` | untracked |
| `09_TRANSPORT_B3B/operator_record/evidence/WPLP2B-20260809T210610Z-834380c5-B3B/b3b.log` | 3,329 bytes; `7b383ab5194972fca9511ae7068509929fab652c980953864ae93aa3ae60fa16` | untracked |

`git ls-files` confirms these are the only three untracked paths among the 198 index
rows (195 are tracked). Therefore the current-tree missing count is zero, but a fresh
clone's missing-artifact count is exactly three unless they are supplied separately.
Current `git check-ignore -v` finds no active ignore rule for them; “untracked” is the
durable fact relevant to clone materialization.

The later integrity record does provide useful external binding for these local bytes:
it recomputed all three leaf digests and compared them with host `CLOSE_DIGEST` output.
That does not make the log files Git-durable or present in a clone.

## Closure-record check

`UNIT_CLOSURE_RECORD.md` depends on all nine numbered stage directories for its result
table and specifically on the three transport families for original B3 STOP, R4-5 PASS,
and repaired B3 PASS.

- Every indexed artifact it relies on exists in this populated working tree.
- 197 artifacts retain their exact indexed identities.
- The one changed relied-on record is not unexplained: its later append adds provenance
  for `b3b.log` and does not weaken or reverse the repaired-B3 PASS claim. The current
  file identity is the post-append identity stated above; the evidence index is stale.
- The three relied-on raw logs match here and are bound by the later integrity record,
  but they are not tracked. Consequently, the closure conclusion is supported in this
  populated workspace and by the committed digest/transport records, yet the complete
  raw evidence set cannot be reconstructed from Git alone.

The closure record itself is not an artifact row in `EVIDENCE_INDEX.md`, so this sweep
does not call it one of the 198 identity matches; it was inspected as the consumer of
those artifacts.

## “Mechanically recomputed” provenance claim

The statement in `EVIDENCE_INDEX.md` that every hash was mechanically recomputed is an
**assertion, not retained execution evidence**.

Located records are limited to:

- the statement in `EVIDENCE_INDEX.md` itself;
- commit `6370e1fe6c79a6ccb0d2ebf19cd1a7cf417f570b`, whose message says the index was
  regenerated over all nine stage directories with recomputed hashes; and
- `OVERNIGHT_RESULT_2026-08-09_NIGHT_FULL.md`, which calls it a mechanical index with
  recomputed hashes.

I found no retained generator script, exact recomputation command, console transcript,
exit code, parsed-row count, or mismatch output for the original generation. Under the
standing evidence rule, the historical claim is therefore **supplemental**. This sweep's
independent recomputation supplies current evidence for all 198 rows, but it does not
retroactively prove which command ran at index-generation time.

## Single most consequential finding

**The closed unit is not clone-complete:** its three raw host evidence logs are indexed
and valid in this working tree but untracked, so a fresh clone omits them. This is more
consequential than the sole hash mismatch because that mismatch is a benign, documented
provenance append; the untracked logs create an unavoidable raw-evidence boundary for
Audit 2 unless the Lead explicitly supplies or reclassifies them. Separately, the stale
B3B index row should not be treated as the authoritative current identity.

## Final counts

- **Artifacts checked:** 198.
- **Identities matching:** 197.
- **Documented changes:** 1.
- **Undocumented drift:** 0.
- **Missing artifacts:** 0 in the current populated working tree; 3 from a fresh clone.
- **Single most consequential finding:** the three matching raw evidence logs are
  untracked and therefore not clone-durable.
