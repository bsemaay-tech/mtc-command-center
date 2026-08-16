Status: ADVERSARIAL VERIFICATION — NO ACCEPTANCE, NO AUTHORITY

> **Pathscope disclosure (owner decision 2026-08-16, section 6):** Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.
> Governing record: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md. Identity split: the prover in this repository is the older 137520-byte R5 code; the audited 185272-byte Option C prover is UNMERGED on codex/pathscope-accounting-redesign-20260815. Prerequisite gate 2 is UNKNOWN until the Lead re-derives it at freeze-prerequisite review.
> Note (2026-08-16): the CONFIRMED "sole open gate-2 lane / gate 2 NOT SATISFIED" rows are superseded; REQUIRED-1/2 remain disclosure; gate 2 is UNKNOWN pending Lead re-derivation.


# Night claim verification — 2026-08-15

Scope: hostile, read-only re-derivation of C1–C5 at the owner-supplied frozen worktree. No host, network, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or economic action was performed. No other AI or agent was invoked. The only write is this report.

## Frozen-subject check

```powershell
git -C C:\CLAIMCHK rev-parse HEAD
git -C C:\CLAIMCHK status --porcelain
```

```text
93479b0e5923b8288ba47dd0dcc5cf8ebf0e096f
<no status output>
```

## C1 — `CONFIRMED`

**Claim tested:** Within Audit-2 prerequisite gate 2, Pathscope is the only open sub-item.

**Narrow scope of this verdict:** this says nothing about prerequisite gates 3–6. They remain open. It says only that the other named gate-2 artifact lanes are accepted under their actual recorded authority.

The primary records support the claim:

- RP7 is accepted on candidate `80cbed461d0b0371e6eabbfff0e732e5001affaf`. That commit is an ancestor of this frozen HEAD. `RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md` records fresh Codex `PASS` and Claude `PASS-WITH-NITS`, zero required repairs.
- Transport has dual flagship acceptance. `TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md:1-10` returns `PASS-WITH-NITS` and expressly closes the second slot on the same seven frozen targets as the Codex `PASS`.
- SEC102 did not receive an accepting Codex verdict: its round-11 Codex result is `REQUEST_CHANGES`. But `STATUS_SEC102.md:3-15` records the later binding owner choice of Option 1, `ACCEPTED-WITH-DISCLOSURE`, and explicitly clears freeze blocker #4. This is not an inference from a favorable model verdict; it is an owner adjudication over a disclosed trusted-base boundary.
- RP6 likewise did not reach ordinary dual-flagship acceptance: its Claude round-18 verdict is `REQUEST_CHANGES`. `WPI_OWNER_DECISIONS_2026-08-13.md:7-20` then expressly accepts the unchanged RP6 executable with disclosure, orders no further hardening rounds, and says the decision closes the RP6 acceptance question.
- Pathscope's authorized execution retry really ran and returned `REQUEST_CHANGES`, not a transport block. `PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md` records three required defects with executable counterexamples that return `PASS rc=0`. No Option A–D disposition has been exercised.

Read-only state commands and decisive output:

```powershell
git merge-base --is-ancestor 80cbed461d0b0371e6eabbfff0e732e5001affaf HEAD
Write-Output "rp7_candidate_in_HEAD_rc=$LASTEXITCODE"
rg -n '^#|Verdict|PASS-WITH-NITS|DUAL FLAGSHIP ACCEPTANCE' `
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_REAUDIT_2026-08-13.md
rg -n 'OWNER DECISION|ACCEPTED-WITH-DISCLOSURE|freeze blocker #4|closes the RP6 acceptance' `
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md `
  MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md
```

```text
rp7_candidate_in_HEAD_rc=0
TRANSPORT ... Verdict: PASS-WITH-NITS
TRANSPORT ... The transport set reaches DUAL FLAGSHIP ACCEPTANCE
STATUS_SEC102 ... ACCEPTED-WITH-DISCLOSURE (owner decision 2026-08-12 ~13:10)
STATUS_SEC102 ... freeze blocker #4 ... CLEARED
WPI_OWNER_DECISIONS ... This closes the RP6 acceptance question by owner decision
```

The accepted executable/proof bytes are still the bytes at frozen HEAD. I hashed the Git-object bytes, avoiding this Windows worktree's CRLF materialization:

```text
RP6-P0.sh                         110817  5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
composite_pathproof.py            129658  adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a
run_p0.sh                           13608  4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c
run_ro.sh                           13470  3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c
transport_runner.ps1               71137  4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2
TRANSPORT_PLAN.tsv                   7970  e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c
remote_setup_wpi.sh                 26483  4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5
remote_extract_verify_wpi.sh        23592  5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b
remote_close_tree_wpi.sh            32630  8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf
```

Those values reproduce the acceptance identities, rather than merely repeating their tables.

The attack on “accepted-with-disclosure” does not refute closure. Gate 2 is titled “Repair/design closure and final artifact acceptances”; it does not say that an owner may not adjudicate a disclosed boundary. The two controlling owner records explicitly say the SEC102 blocker is cleared and the RP6 acceptance question is closed. The repository's general audit policy also permits a later explicit owner contract to override the default. Treating these as ordinary flagship PASSes would be false, but treating them as owner acceptances is supported by primary evidence.

Pathscope is therefore the only open gate-2 lane. Gate 2 itself remains `NOT SATISFIED`, and all downstream Stage-1/Audit-2 work remains blocked.

## C2 — `CONTESTED`

**Claim tested:** Gate B is step 9, downstream of WP-I, Audit 2, WP-A and Audit 3, so deployment cannot run in parallel.

### Reading A — the 50-hour active-delivery sequence is controlling

The later 2026-07-30 “50-Hour Accelerated Implementation Plan” targets the same Ubuntu KVM2 DISARMED finish line and calls itself the **Active Delivery Plan** (`:31-40`). Its section 23a says the gates “must be cleared in the exact order” and records:

```text
3 staging action
4 Audit 2 after WP-L Phase 2 + WP-I staging
5 WP-A
7 final exact SHA/artifact freeze
8 Audit 3 + Gate 6
9 Gate B
10 WP-V after separate deployment approval
```

The current handoff repeats this sequence at `GLOBAL_HANDOFF.md:617-620`. The synthesis citation to `:544-549` is stale at this frozen SHA, but the quoted content exists. Under this authority, C2 is correct: production deployment cannot precede WP-I/Audit 2/WP-A/Audit 3.

### Reading B — the KVM2 bridge program has its own unreconciled authority chain

The older KVM2 master plan is not marked superseded. It says:

- `KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:45-47`: the lower-level bridge authority **remains** `BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`, and the master does not bypass or weaken its ten ordered tasks.
- `:217-237`: the KVM2 execution companion is the sole detailed authority for its 85 task blocks; execution/audit/owner/deploy/first-start gates are separate.
- `:241-248`: Phase 3 is bridge release readiness and Phase 4 is separately authorized deploy/cutover. Its predecessor chain is Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4, not WP-I → Audit 2 → WP-A → Audit 3.
- `:466-479`: deploy is P4-01/P4-02 and first DISARMED start is P4-06/P4-07.
- The lower-level deploy list independently says its ten-item checklist must complete before deploy and ends at a separate owner deploy authorization.

No bounded search found a sentence in the KVM2 master plan, execution companion, or bridge deploy task list subordinating P4 deploy to the later 50-hour plan's Audit-2/WP-A sequence. Conversely, the 50-hour plan does not name or reconcile KVM2 P0–P4. Both documents target the same KVM2 bridge and both present themselves as controlling plans.

**Adversarial disposition:** the later 50-hour plan is the stronger current scheduling authority, but the older KVM2 master/lower-level authority was preserved rather than expressly retired. A defensible reader can treat the systems as cumulative (all gates required), or can treat the KVM2 bridge track as its own program. Until the owner or a canonical reconciliation record states which authority dominates, “cannot run in parallel” is not established uniquely. This ambiguity materially affects both schedule and hour count.

## C3 — `CONFIRMED`

**Claim tested:** Candidate `2ce41e34` is not in `origin/master`, and its A-0..A-9 acceptance cannot be carried to a new release candidate.

Ancestry was re-derived locally:

```powershell
git rev-parse '2ce41e34^{commit}'
git rev-parse 'refs/remotes/origin/master^{commit}'
git merge-base --is-ancestor 2ce41e34 origin/master
git merge-base --is-ancestor origin/master 2ce41e34
git branch -a --contains 2ce41e34
git for-each-ref --contains=2ce41e34 --format='%(refname)'
```

```text
candidate=2ce41e34bceb599d80af24c5c33d835820ec321b
origin_master=637307e83951ffe23e768ed8e50ddaf8712b0660
candidate_is_ancestor_of_origin_master_rc=1
origin_master_is_ancestor_of_candidate_rc=0
merge_base=637307e83951ffe23e768ed8e50ddaf8712b0660
refs/heads/codex/gate-a-disarmed-start-mode
refs/remotes/origin/codex/gate-a-disarmed-start-mode
<no containing tag>
```

So the candidate is a descendant of the locally recorded `origin/master`, but was never merged back. No other ref contains it.

The bounded record search found no completed merge, new candidate, or A-0..A-9 rerun that transfers the acceptance. The only later integration record is explicitly `DESIGN ONLY — NO CODE, NO MERGE, NO ACCEPTANCE`. Its section 5 requires every A check to rerun and section 4 requires a new candidate-bound A-0..A-9 verdict under separate host authority.

I attacked the categorical “nothing transfers” wording. Some **procedures and predicates** are reusable: the A-0 manifest method, A-4 seven-condition structure, A-5 restart sequence, A-8 probe contract, and A-9 category list. Historical outputs are useful regression/supplemental evidence. That is not acceptance transfer. Every PASS depends on either candidate/artifact bytes (A-0, A-2 through A-7, A-9) or time-varying host/network state (A-1, A-4 through A-8). No complete A-0..A-9 verdict is byte-independent. The claim is therefore confirmed as an acceptance claim, not as a claim that all prior work is worthless.

## C4 — `CONFIRMED-NARROWER`

**Claim tested:** A1 fails only on Windows and passes on the Linux deploy target.

**Precisely supported narrower form:** A1 fails when `ledger_schema.json` is materialized as CRLF but the ledger records the LF Git-object hash. It passes when the exact LF bytes are materialized. This happened in a recorded Ubuntu run with the same ledger/schema/validator blobs, and the accepted repair forces LF for fresh checkouts. “Windows-only” is not an OS invariant, and a future exact deploy-target run is not yet established.

The raw mechanism at frozen HEAD is:

```powershell
git check-attr -a -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
git config --show-origin --get core.autocrlf
Get-FileHash -Algorithm SHA256 MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
git cat-file -s HEAD:MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
# The Git-object SHA-256/CR/LF census below was computed by piping `git cat-file blob`
# bytes to Python hashlib without creating a file.
```

```text
HEAD .gitattributes: * text=auto
git check-attr:       text: auto
Git blob:             867 bytes, SHA-256 f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e, CR=0, LF=36
ledger expectation:   f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
Windows worktree:     903 bytes, SHA-256 b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a, CR=36, LF=36
local core.autocrlf:  true
```

`validate_ledger.py:88-93,155-162` opens the artifact in binary mode and compares the raw-file SHA-256 to the ledger. `test_linux_deployment.py:407-416` invokes that validation with artifact verification enabled. The mismatch is therefore sufficient to explain A1; no platform branch exists in the validator.

The repair branch adds exactly:

```gitattributes
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

The relevant immutable subjects compare as follows:

```text
ledger_schema.json blob:  ebada020 = ddc8a9c8 = repair branch = 9433294c050b788dfd47064528ca252bc95bc01e
EVIDENCE_LEDGER.jsonl:    ebada020 = ddc8a9c8 = repair branch = 8d48e41b1868737b60c9b5d00b6f38db6f087be3
validate_ledger.py:       ebada020 = ddc8a9c8 = repair branch = 198a75c5b61a28a65d7b2fbe66f6052fffe83b0e
```

`GATE_A_RESULT_2026-08-08.md:153-180` records a real Ubuntu CPython 3.12.3 / pytest 9.1.1 suite run at `ebada020`; the ledger test passed. That candidate carries the same schema, ledger, and validator blobs and the same `eol=lf` rule now restored by the repair. Also, canonical `package.sh:12-14,73-74` exports release bytes through `git archive`, so the intended deploy artifact comes from Git-object bytes rather than a CRLF Windows working file.

Conditions required for A1 to pass on a future deploy target:

1. The frozen candidate retains the ledger, schema, validator and relevant test semantics, or updates their identities consistently.
2. The candidate contains the accepted `eol=lf` rule, or the artifact is otherwise materialized from the exact LF Git blob.
3. The canonical `git archive` package path is used and no later transfer/install step rewrites the file.
4. The test resolves `REPO_ROOT` to that exact artifact and validates the matching ledger row.
5. The locked target environment can import and run the validator/test; no unrelated collection/import failure prevents evaluation.

Conditions 1–3 hold on the **unmerged repair branch** and historical Ubuntu evidence supports the mechanism. They are not established for a future frozen release SHA because it does not exist. Conditions 3–5 are not established on the actual KVM2 target because host access and execution were forbidden. A Windows checkout with LF bytes can pass; a Linux worktree deliberately configured or mutated to CRLF can fail. The trustworthy statement is about bytes, not operating-system name.

## C5 — `REFUTED`

**Claim tested:** Remaining work to one DISARMED KVM2 first start is 55–105 hands-on hours.

The displayed arithmetic is correct:

```text
lower_sum=55.4
upper_sum=105
```

The estimate is nevertheless not established. Row-by-row source checking found stale inputs, unsupported prices, incompatible ordering, and unresolved overlap.

| Synthesis row | Adversarial source check |
|---:|---|
| 1 | **Supported.** Pathscope Option C is explicitly priced at 6–10 h including design, implementation, Lead execution, and one audit. |
| 2 | **Wrong range/source use.** Reconciliation section 3 prices the post-Pathscope Stage-1 steps at **6–12.5 h** (`1–2 + 1–2 + 0.5–1.5 + 2–4 + 1.5–3`). The quoted **7–14.5 h** comes from section 4's Option-B scenario and includes 1–2 h for recording Option B. Row 1 already prices the chosen Pathscope disposition, so row 2 double-counts 1–2 h. |
| 3 | **Unsupported estimate.** The source is admitted as “not separately priced”; no primary record supplies 4–8 h. |
| 4 | **Partly stale and unpriced.** Prerequisite gates 5–6 provide no 2–4 h estimate. More importantly, `WPI_OWNER_DECISIONS_2026-08-13.md:22-27` already ratified the ledger at ~55 h and closed P11-08. Only the checkpoint-freeze work remains, with no sourced range. |
| 5 | **Unsupported hours.** The acceptance matrix and T0 roster establish required models/state, not 6–12 h. The active plan's entire WP-R reserve is 6 h for Audit 2, Audit 3, Gate 6 and all re-audits combined; the synthesis silently estimates well beyond that without identifying new authorization/funding. |
| 6 | **Contradicts the cited plan.** The canonical WP-A budget is exactly **3 h**, not 4–8 h. A larger planning allowance may be prudent, but it is not what the cited authority says and would require budget reconciliation. |
| 7 | **Unsupported hours.** The sequence establishes final freeze, Audit 3 and Gate 6, but gives no 6–12 h row price. It also shares the active plan's 6 h total audit reserve with Audit 2. |
| 8 | **Underpriced against the newer direct design and placed in the wrong order.** The integration design prices candidate integration + local acceptance at **16–32 h**, including 8–16 h of T0 audits, plus **5–9 h** for fresh staging A-0..A-9. The synthesis uses 12–20 h and labels it local. Worse, it puts integration after final-SHA freeze and Audit 3; integrating after Audit 3 changes bytes and invalidates that acceptance. Integration must occur before WP-I staging/Audit 2, or overlap those earlier freeze/matrix/audit rows. |
| 9 | **Numerically traceable but incompletely named.** The Bridge refresh's total owner time is 0.85–1.5 h, so 0.9–1.5 is reasonable rounding. The cited subset does not explicitly enumerate Gate B, separate WP-V approval, merge authority, and all four deploy/first-start gates. |
| 10 | **Supported as arithmetic.** Bridge-refresh host rows 4–5 total 5–10 h. |
| 11 | **Supported as arithmetic.** Bridge-refresh host rows 6–7 total 2.5–5 h. |

### Audit/integration overlap

The release-integration design explicitly includes T0 audit rounds in its 16–32 h subtotal. The synthesis's row 8 uses a compressed 12–20 h value that also says “tier-required audits,” while rows 5 and 7 separately price Audit 2 and Audit 3/Gate 6. These could be three genuinely distinct audit checkpoints: pre-host candidate acceptance, post-WP-I Audit 2, and post-WP-A Audit 3/Gate 6. If so, row 8 is underpriced and the role split wrongly counts its audit labor as local. If the author intended any of them to be the same audit, the hours are double-counted. The document does not say which. The wrong row order prevents resolving the ambiguity by dependency.

### Mandatory work absent or only hidden inside ambiguous rows

- Packet 9/10/11 completion, including the locked-environment frozen-SHA suite baseline and final authority consolidation, remains an explicit Audit-2 dispatch prerequisite. It has no clear row before Audit 2. Row 8's full matrices cannot supply it while row 8 is ordered after Audit 2 and Audit 3.
- Fresh candidate-bound A-0..A-9 staging is explicitly 5–9 h in the integration design. It is not named. It might be intended inside the unsourced 4–8 h “WP-I staging” row, but that is both under the direct estimate and unstated.
- The accepted Gate-A line still needs separate integration/merge authority. No row names or prices the owner merge decision.
- Gate B and the separate WP-V deployment authorization are mandatory in the 50-hour authority chain but are not explicit milestones in the table.
- Under the alternative C2 reading, KVM2 Phase 0 → Phase 1 → Phase 2 → Phase 3 owner/audit close gates also precede Phase 4 deploy. The synthesis neither declares them already complete nor prices them. This alone prevents a single authoritative range until the two plans are reconciled.

Because some defects inflate the range and others omit work, subtracting or adding one correction does not yield an honest replacement total. What is true is only: the eleven displayed numbers sum to 55.4–105. The repository does not establish that those eleven rows are disjoint, complete, correctly ordered, or consistently sourced. Barış should not budget against 55–105 until the authority chain is reconciled and one dependency-ordered, non-overlapping work breakdown maps candidate integration, A-0..A-9, Packet 9/10/11, Audit 2, WP-A, final freeze/Audit 3/Gate 6, Gate B, and WP-V exactly once.

## Trust-least note

Barış should trust **C5 least**. Its arithmetic creates a false impression of precision while its work packages mix two unreconciled programs, reuse the Option-B Stage-1 range under an Option-C assumption, price already-closed ledger ratification, contradict the canonical 3 h WP-A budget, undercut the newer integration estimate, and put byte-changing integration after final-byte Audit 3. C2 is the underlying governance ambiguity, but C5 converts that ambiguity into a spendable number; making an expensive schedule decision from 55–105 would therefore carry the highest immediate risk.
