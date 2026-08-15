NEEDS-REWORK

# RB3REV runbook-patch review

Audit tier: **T2 documentation/evidence review, one round**. I reviewed the exact pinned V2 blob named by the patch (`26309967bb141ff45730ee55fb0b293d48a690ef`), because the task documents are absent from the detached worktree. This review performs no action and creates no acceptance, authorization, or operating permission. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:3-9`

## Bottom line

The substantive R1/R2/R3 text is mostly sound. A reader following only the replacement checklist cannot cross the H-WPI boundary without the distinct WP-I authority binding and close-contract result, Gate-A and grant-#6 remain separate, the claim is narrowed to a documentary contract, and the new post-mutation/quarantine states prevent ordinary continuation.

Two required problems remain:

1. Applying the stated replacements to the pinned V2 blob does not produce a coherent V3 artifact. The untouched document continues to identify and freeze itself as V2, while replacement Sections 10 and 11 call it V3. This is an application seam, not a cosmetic nit.
2. The patch's proposed test checks only patched Section 11. It can pass without proving that the Step-14A producing transition was applied or that the integrated document is internally coherent, and no actual RED/mutation execution output is recorded. It is a useful checklist test specification, not yet proof that the whole R1 repair was applied.

## 1. Checklist-only walk

Following only patched Section 11, the path is blocked.

The checklist first says every row is necessary, later rows cannot cure an earlier omission, and absent, `UNKNOWN`, unevaluable, or non-PASS evidence stops the path. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:202-205`

The relevant ordered trace is:

```text
C1 -> C2 -> C3 -> C4
   -> C8 prerequisite for H-A
   -> BEFORE H-A: separate Gate-A authority + close contract
   -> C6/C7 -> C8
   -> BEFORE H-6: grant-#6 bound to exact Commit 1 + capture close
   -> C9: exact verified Commit 2
   -> P9-15 accepted/preflighted
   -> BEFORE H-WPI: Step-14A record with both exact bindings
   -> H-WPI
   -> AFTER H-WPI only
```

At the pre-H-WPI row, the record must name the exact verified Commit-2 object and runkit and contain both `WPI_OPS_AUTHORITY_BOUND=PASS` and `WP_I_ALWAYS_CLOSE_CONTRACT_ACCEPTED=PASS`. Its expectations must come from the independently identified D2 WP-I clause/exclusions and independently accepted close contract; a D2 sentence or tick mark is not a substitute. Any absent, `UNKNOWN`, unevaluable, or mismatched input stops before socket open and op 01. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:215-218`

Therefore no checklist-only compliant trace reaches WP-I host work without the third authority binding. The following `AFTER H-WPI only` row cannot be reached from a non-PASS Step 15 and cannot cure a missing pre-host result. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:217-223`

## 2. Gate-A and grant-#6 did not regress

The replacement structural edge keeps three separately named host nodes and predicates:

- H-A requires `GATE_A_STAGE_AUTHORITY_BOUND` and its own safe-close contract.
- H-6 requires `GRANT6_CAPTURE_AUTHORITY_BOUND` and its own create-once close contract.
- H-WPI requires `WPI_OPS_AUTHORITY_BOUND` and the WP-I always-close contract.

`MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:40-64`

The replacement also expressly forbids a generic authority gate, an edge from D2 to H-A, and a direct edge from D2 prose to H-WPI. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:66-68`

The summaries preserve the same separation: Step 11 can bind grant-#6 but cannot set Gate-A or WP-I authority; Step 14A alone binds the WP-I clause to the exact Commit-2 runkit; Step 15 says its authority is WP-I and never Gate-A. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:134-148,183-190`

The final checklist also places a verified-Commit-1 prerequisite before H-A, requires a separate Gate-A sentence and forbids D2 reuse, then separately binds D2's grant-#6 clause to exact Commit 1. The third authority has its own later row. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:206-218`

No Gate-A/grant-#6 blur was found in any replacement section.

## 3. R2 claim scope and R3 state model

### R2

The revised claim is truthful within its stated universe. The F1 replacement calls the guard a documentary transition contract for a compliant operator and expressly disclaims an executable dispatcher or mechanical interlock. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:13-21`

Replacement Sections 7, 10, and 11 repeat that limitation: a person who ignores the runbook is outside the quantified universe, and the document proves only documentary reachability for an operator following the transitions. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:28-38,66-68,179-194,202-225`

This resolves the V2 review's R2 overclaim, which found that V2 itself established no executable dispatcher/interlock. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V2_REVIEW_2026-08-15.md:65-73`

### R3

The patch now separates pre-create failure from post-create verification failure for both commits. A possible or actual creation followed by failed read-back/identity verification becomes `COMMIT1_CREATED_UNVERIFIED_QUARANTINE` or `COMMIT2_CREATED_UNVERIFIED_QUARANTINE`, with the observed object/current-reference state preserved and destructive recovery forbidden. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:84-115,125-132,163-170`

The terminal record now carries `mutation_attempted` plus the observed object/current-reference value or `UNKNOWN`, first divergence, completed/skipped work, cleanup evidence, safe-state result, and one terminal disposition. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:70-82`

`HOST_STATE_UNKNOWN_QUARANTINE` is operationally terminal, though deliberately not graph-theoretically edge-free. After an H-WPI partial, the only permitted outgoing edge is local closure-only bookkeeping that writes P9-17 `STOP` and `PACKET9_STOP_CLOSED`; it performs no host operation, does not clear quarantine, cannot reach Step 17, and ends the runbook path. H-A and H-6 quarantine have no such edge. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:109-115,145-160`

The checklist independently blocks continuation past a non-PASS Step 15. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:217-219`

## 4. The patch's own test

The proposed test has real strengths:

- Its expected tuple comes from V2's pre-existing H-WPI incoming edge rather than from the checklist under test. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:243-245`; `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:182-188`
- It exercises negative traces for each missing/`UNKNOWN` binding and identity mismatch. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:247-253`
- It names deletion, token-removal, generic-label, reordering, STOP-removal, and prose/tick-substitution mutations, and requires every mutation to make verification fail. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:255-266`

But the test can pass while the complete R1 repair remains unapplied. Step 1 deliberately gives the verifier only Section 11 and excludes Step 14A and Sections 7/10. A correct checklist can therefore pass even if the Steps-14-through-16 replacement was omitted, Step 14A does not exist, or the integrated document retains contradictory identity text. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:247-251`

That does not reopen a checklist-only host path--the row still stops a compliant reader--but it means the test does not prove the patch's full claim that the missing numbered producer and checklist gate were both repaired. The V2 review required both. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V2_REVIEW_2026-08-15.md:28-30`

The patch also records a verification procedure and required RED arms, not their execution. No command, verifier identity, actual output, or RED/GREEN transcript is established; those values are `UNKNOWN`. Calling the section a test "that proves" closure overstates the evidence until the mutations are actually walked and recorded. The recurring-defect rule requires asking what makes a check fail, where the expected value comes from, and whether it is enforced or asserted--and specifically says to show it failing. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63,73-82`

Required repair: make the verification operate on the fully applied document, check the Step-14A producer and all three H-WPI representations, and record the actual negative/mutation outcomes. Keep the Section-11-only arm as a useful subtest.

## 5. Patch mechanics

The stated replacement ranges do fit the pinned V2 text mechanically:

- line 5 is exactly the complete F1 row;
- lines 152-207 are exactly Sections 7 and 8;
- line 289 is exactly Step 10's old terminal bullet;
- lines 315-336 are exactly Steps 14-16;
- lines 382-401 are exactly Section 10; and
- lines 403-422 are exactly Section 11 through end of file.

`MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:13-25,120-176,174-199`; `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:5,152-209,284-292,315-338,382-422`

Adding Step 14A does not renumber Step 15 or later steps. The new checklist and ordered walk refer to the resulting Step 14A, Step 15, Step 16, and Step 17 consistently. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:134-160,183-192,215-218`

However, the application rule says to apply only the listed replacements to the pinned V2 file. It provides no replacement for the document's status, title, self-identity, or output path. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:7-9`

After those replacements, these V2 statements survive unchanged:

- `Status: EXECUTION RUNBOOK V2`;
- `# Stage-1-to-Audit-2 execution runbook -- version 2`;
- V2 supersedes V1 and V2 itself is not accepted/pinned;
- Step 1 runs C1 over the source list "including this V2"; and
- the Step-7 revision rule says "This V2 cannot self-amend."

`MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:1,14,20,211-217,258-265`

The inserted text instead says Section 10 walks "the V3 text," concludes a property of "V3's documentary transitions," and makes checklist C1 require V3. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:179-194,202-206`

Thus a literal application leaves one artifact simultaneously identified as V2 and V3. Step 1 freezes "this V2," while the final checklist requires V3; the exact resulting artifact/path that C1 must bind is `UNKNOWN`. That seam prevents the patch from being a coherent, safely applicable V3 patch.

Required repair: add exact replacements for the status/title and every self-reference that must change, and specify the resulting artifact path/identity; or consistently describe this as a V2 amendment and remove the new V3 references. Then run the integrated verification against the exact resulting bytes.
