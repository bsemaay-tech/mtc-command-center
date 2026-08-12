# WP-I claim-audit synthesis - 2026-08-12

Audit tier: T2 documentation/evidence synthesis only.

Inputs read:

- `WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`
- `WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`
- `WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md`
- `WPI_SELFQA_CLAIM_AUDIT_SEC102_2026-08-12.md`
- `WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`

No harness was run. No audited file was edited. This synthesis counts only explicit
findings in the five audit reports; clean checks and non-findings are excluded.

## 1. Finding count by class

| Audit report / package | False | Unsupported | Scope-wrong | Total |
|---|---:|---:|---:|---:|
| Transport + Pathscope self-QA audit | 3 | 3 | 0 | 6 |
| RP7 self-QA audit | 3 | 2 | 1 | 6 |
| RP6 self-QA audit | 2 | 4 | 1 | 7 |
| SEC102 self-QA audit | 6 | 6 | 1 | 13 |
| Round-report audit | 2 | 3 | 1 | 6 |
| **Total** | **16** | **18** | **4** | **38** |

Cleanest at the five-report/package level: a three-way tie between
Transport + Pathscope, RP7, and the round-report package, each with 6 findings.

Worst at the five-report/package level: SEC102, with 13 findings.

Individual-target caveat: the first and fifth audit reports cover multiple underlying
documents/reports. On that narrower view, `SELF_QA_PATHSCOPE.md` has only 2 findings
inside the Transport + Pathscope package, while `SELF_QA_TRANSPORT.md` has 4. In the
round-report package, `RP6_R17_REPORT_2026-08-12.md` checked clean on the audited axes,
`RP7_REPAIR_R9_REPORT.md` had 1 unsupported finding, `TRANSPORT_R6_REPORT_2026-08-11.md`
had 2 findings, and `RP6_R16_REPORT_2026-08-11.md` had the problematic unresolved-
placeholder cluster with 3 findings.

## 2. Systemic cause

Yes. The supported systemic cause is:

**Local-evidence overclaiming after late, carried-forward, or externally evidenced authoring.**

That cause is evidenced in four recurring forms. The audit reports do not prove a
specific "recovered session" root cause, so this synthesis does not name recovery itself
as the cause.

1. **Summary text claims final evidence before the final transcript is actually pasted.**

   RP6 is the clearest cluster. The RP6 self-QA audit finds that round-15/16 prose says
   placeholders were resolved and real captured output is present, while eight transcript
   slots remain literal placeholders. The round-report audit independently repeats the same
   pattern for `RP6_R16_REPORT_2026-08-11.md`, `STATUS_RP6_P0.md`, and the report's own
   `@@REPORT_EXEC_BLOCK@@`. This is not a harness-behavior finding; it is a finalization
   failure where prose moved to "resolved/captured" before the evidence lane did.

2. **Carried-forward round prose keeps stale identity or stale scope language.**

   RP7 is the clearest cluster. The audit finds stale or contradictory bytes/hash/body-size
   prose, including claims around `92853 B / e695a67b...`, `20050 B`, and `77179 /
   393a16ce...`, while the pasted transcripts show the current round-9 repaired artifact
   identity `108301 / 0e93f90d...`. The same audit finds carried-fence summaries saying
   GREEN was run against "round-8 bytes" when the transcript identities show current
   repaired worktree bytes. This is carried text outliving the artifact it describes.

3. **External or whole-session claims are worded as if local transcript evidence proves them.**

   SEC102 contributes the largest unsupported cluster: prior-audit verdicts, cross-round
   byte identity, prior-round closure, a `pathscope_prover.py` pin, and final-byte
   re-derivation are all stated without a supporting line inside the document. The
   round-report audit shows the same issue for RP7's extra run count and Transport's
   document identities, which are self-recorded or external to the matching STATUS/SELF_QA
   lane. RP6 also has broad whole-session negatives such as no host/network/Git/write
   activity that the pasted harness output cannot establish.

4. **Hand-written count/scope summaries drift from the rows they summarize.**

   SEC102 has multiple false count or scope summaries: two versus three killed REDs,
   ten newly closed forms explained with a nine-item subcount, "each new RED" overstated
   when one is carried, a claimed all-95-printable-ASCII sweep contradicted by
   `SWEEP_CHARS=101`, and "no form moved" contradicted by a `MOVED` row. The same pattern
   appears in Pathscope's "four CRITICAL findings" claim versus 16 `rc 0 - (no row)` RED
   rows, Transport's J-family execution miscount, and Transport's unsupported "twelve"
   pinned OpenSSH-program execution count.

## 3. Acceptance-impacting candidates

Most findings are documentation repairs: stale prose, unsupported local wording, count
explanations, and scope phrasing. They should be fixed, but they do not by themselves
show that the underlying repaired code or transcript-backed behavioral rows fail.

The conservative acceptance-impacting candidates are limited to these:

| Finding group | Could affect acceptance? | Reason |
|---|---|---|
| RP6 unresolved-placeholder cluster: RP6 self-QA F-1, U-1, U-2; round-report F-01, F-02, U-01 | **Yes, for RP6 round-15/16 evidence acceptance based on those files** | The documents say closure transcripts, guard counts, discriminating-power proof, status head output, and rerun evidence are present, but the evidence slots are placeholders. If acceptance depended on those documents alone, that acceptance is not evidence-grounded. Later or external evidence may still support a narrower acceptance, but it must be cited explicitly. |
| SEC102 channel-contract scope: SEC102 S-1 | **Conditional, probably documentation-scope repair** | The top summary says every block was run both ways; the transcript proves 10/11 plus one self-excluded block, and later prose discloses the self-exclusion. If "every block both ways" was an acceptance criterion, the acceptance statement must narrow to the actual 10/11 contract. Because the self-exclusion is disclosed later, this is not evidence of a hidden harness failure. |
| Transport cleanup contradiction: Transport F-1 | **Conditional, narrow hygiene impact** | The prose says all fixture scratch was removed, but Fixture D cleanup shows an access-denied removal failure and no final `exists=False` line. This could affect acceptance of cleanup/no-residue claims. It does not directly refute the central transport repair counts that the round-report audit found matched. |

All other listed findings are documentation repairs unless the project explicitly made the
unsupported fact an acceptance condition. Examples: RP7 stale identity prose should be
corrected to the transcript-backed current identity; SEC102 count explanations should be
rewritten to match the rows; external prior-audit and byte-identity claims should be cited
as external evidence or removed from local-proof language.

## 4. Authoring rules that would have prevented the largest share

1. **Placeholder finalization gate.** Before writing any "closed", "resolved", "captured",
   "accepted", or "evidence of record" sentence, scan the document and linked status/report
   files for `@@`, `PENDING`, and empty transcript slots. Any hit must be filled with pasted
   output or the prose must say `PENDING` and exclude that section from closure.

2. **Line-evidence rule for absolute and numeric claims.** Every sentence containing
   `all`, `every`, `no`, `none`, `unchanged`, `byte-identical`, a count, `bytes`, `sha`,
   `rc`, or a run count must point to the exact pasted transcript line that proves it. If
   the support is outside the document, label it `External evidence:` and cite the file;
   do not phrase it as locally transcript-proved.

3. **Carry-forward re-derivation rule.** Any carried-forward section must be re-derived
   after the final artifact edit: replace old bytes, hashes, round labels, and denominators
   from a current identity/scope table. Scope wording must use the exact denominator shown
   by the transcript, such as `10/11 plus one self-exclusion` or `seven targets plus the
   harness`, not `every block` or `every document`.
