# Audit 2 readiness-package coherence review

## Verdict

**NEEDS-UPDATE: 20 items**

Count basis: 9 stale or superseded claim groups plus 11 missing-material packets. Audit
tier: T2 (documentation/evidence coherence), under the kickoff's explicit fresh Codex
high-effort contract. This was a local, analysis-only review. No package file was edited,
no host or network was contacted, and no execution authority is created here.

The package remains directionally correct that Audit 2 cannot precede WP-I closure and
cannot authorize WP-A. It no longer gives an auditor a coherent account of what must close
inside WP-I, which bytes are current, or which evidence is trustworthy.

## Stale or superseded claims (9)

| # | Package statement, verbatim | Current truth |
|---:|---|---|
| 1 | `Audit 2 is the two-flagship T0 round that freezes the pre-WP-A SHA.` (`KICKOFF_AUDIT2_READINESS.md:10`) | Audit 2 reviews an already frozen pre-WP-A checkpoint. `AUDIT2_FREEZE_PREREQUISITES.md` itself requires the checkpoint SHA before dispatch. A separate Stage-1 artifact freeze must also occur before WP-I host invocation. Audit 2 does not create either freeze. |
| 2 | `The unresolved GLM-5.2 supplemental-versus-omitted decision is recorded in OPEN_QUESTIONS_FOR_DISPATCHER.md.` (`AUDIT2_AUDITOR_SESSION_INPUTS.md:17-18`); the assembly kickoff likewise calls this an `unresolved GLM supplemental-vs-omitted` flag (`KICKOFF_AUDIT2_READINESS.md:52-53`). | This is no longer an open dispatcher choice. The permanent audit-tier policy makes Audit 2 T0: exactly `claude-opus-5` and `gpt-5.6-sol`, both fresh and xhigh. GLM is not silently added; only a later explicit owner contract can designate a broader review. `OPEN_QUESTIONS_FOR_DISPATCHER.md` question 1 should be closed or removed. |
| 3 | `WP-I is still draft round 1.2` (`AUDIT2_HANDOFF_PACKAGE.md:28`) and `The same closure record says WP-I is draft round 1.2, F3/F4 remain OPEN` (`AUDIT2_FREEZE_PREREQUISITES.md:10`). | That historical closure record no longer describes the working WP-I package. RP6-P0 is round 6 and has a Codex `REQUEST_CHANGES`; RP7 has round-5 repaired bytes pending independent re-audit after a round-4 Codex BLOCK; transport round 3 has a Claude `PASS-WITH-NITS` and a Codex `REQUEST_CHANGES`. The successor preregistration also has 13 required gaps. WP-I is still open, but not for only the old round-1.2 F3/F4 state. |
| 4 | `Obtain both authorities, execute only the authorized WP-I scope, close it with evidence, and preserve all exclusions.` (`AUDIT2_FREEZE_PREREQUISITES.md:10`) | Authority and budget are not the complete path to execution. Before any WP-I run, final bytes must close the current RP6, RP7, and transport findings; section 8.2 rows 1-9 must be implemented or explicitly deferred by owner-approved scope change; section 10.1 and 10.2 must close; the successor preregistration and two-commit attestation order must close; all required freeze inputs must be filled; and final T0 acceptances must be on the post-repair bytes. |
| 5 | `BLOCKED-UPSTREAM: no exact paths recorded in the permitted inputs` for the WP-I closure and evidence index (`AUDIT2_AUDITOR_SESSION_INPUTS.md:58`), and `No exact artifact path is recorded in the permitted inputs.` (`AUDIT2_HANDOFF_PACKAGE.md:28`) | A WP-I closure record and final evidence index still do not exist, but exact current artifact paths now do: `WPI_BLOCKS_DRAFT/RP6-P0.sh`, `RP7-WPI-RO.sh`, the nine-file transport set, their status/audit records, and `WPI_PREREG_DRAFT_ROUND1/`. The package must distinguish "current artifacts are known but non-accepted" from "final closure/index not yet produced." |
| 6 | `Only R4-5 has an exact RED/GREEN record location in the permitted inputs. Treat every unlocated row as supplemental, not closure.` (`AUDIT2_HANDOFF_PACKAGE.md:20`) and `Treat all rows marked UNLOCATED as supplemental.` (`AUDIT2_HANDOFF_PACKAGE.md:39`) | The Lead correction appended to `AUDIT2_D026_RED_LOCATIONS.md` identifies auditor-executed locations for multiple B3 falsifications and records the round-6 literal paste-and-run. The handoff still repeats the pre-correction conclusion. The register and handoff must be normalized to one non-contradictory classification before dispatch. Genuinely unlocated rows remain supplemental. |
| 7 | The register says `No exact RED location recorded` / `UNLOCATED; supplemental only` for nested-decoy JSON, duplicate-key JSON, symlinked `/etc/mtc-bridge`, name-mapped ownership, ENOENT at the conf-dir boundary, PYTHONPATH/cwd `json` hijack, non-finite JSON constants, unterminated final mount records, and ambiguous multiline diagnostics (`AUDIT2_D026_RED_LOCATIONS.md:15-25`). | The same file's Lead correction (`:55-84`) supplies audit-report locations for those named cases. Leaving the obsolete rows above the correction makes a dispatcher see two incompatible answers. Replace the obsolete classifications with the corrected per-case locations; do not rely on a trailing narrative override. The shared-path-temp and unguarded-`tr` entries are not silently upgraded unless an exact pair is supplied. |
| 8 | `The current ~26.9 h is explicitly provisional pending owner adjustment.` (`AUDIT2_HANDOFF_PACKAGE.md:33`); `WP-I consumption is not yet known.` (`AUDIT2_FREEZE_PREREQUISITES.md:12`). | The package's 26.9-hour remaining figure predates the current WP-I build/audit cycle. The newest record books about 29.3 hours used out of 50 (24.9 ratified plus about 4.4 prospective), leaving about 20.7 hours prospectively; the added amount is still unratified. Audit 2 still needs one owner-ratified freeze-time figure, but 26.9 remaining is no longer a useful current estimate. |
| 9 | `The only recorded description is that the current baseline includes two permitted test_order_state.py gc-referent failures.` (`AUDIT2_AUDITOR_SESSION_INPUTS.md:82-83`) | The package provides no authoritative command, test IDs, output signatures, or frozen-SHA baseline that establishes this as the current accepted anomaly set; the next paragraph correctly marks all of those fields missing. The quoted sentence must not be presented as a current baseline. Replace it only from an authoritative freeze-time source, or state that the anomaly set is wholly unresolved. |

## Missing material (11)

1. **A current per-artifact acceptance matrix.** It must name exact bytes, latest verdict,
   required repairs, and the acceptance still missing for all three executable sets:
   RP6-P0 (`75db028e...`, round 6, Codex `REQUEST_CHANGES`, five repair groups); RP7
   (round-5 `393a16ce...` working bytes, pending independent re-audit after the round-4
   `23e55667...` BLOCK); and transport (`78173bfd` round-3 basis, Claude
   `PASS-WITH-NITS`, Codex `REQUEST_CHANGES: 4`, repair/re-audit still required). The
   package must say plainly that **none of the three has been accepted by both flagships**.

2. **Section 8.2 rows 1-9 disposition.** No current executable or plan operation implements
   these rows. RP6 provides premises, not B2/B4 results; RP7 implements rows 10-23 and
   records row 24 as operator-side. Freeze is blocked until rows 1-9 have an accepted
   executable and first-divergence position, or an owner-approved scope change explicitly
   defers them and narrows every closure/Audit-2 claim.

3. **The section 10.1 delta and access grammar.** The source reconciliation found 20
   bounded families: 8 already covered, 11 needing narrow extensions, and `/dev/null`
   requiring block changes rather than allowlisting. It also found 3 unresolved families:
   RP6's optional/PATH-resolved tool universe, its arbitrary-prefix venv root, and composite
   evidence-root provenance. The package also needs capability-qualified rules
   (`read-exact`, `read-tree`, `read-terminal`, `read-execute-exact`, `write-tree`,
   `connect`) rather than path shape alone.

4. **The section 10.2 prover's non-accepting status.** The T1 audit returned
   `REQUEST_CHANGES: 9`, including four CRITICAL silent-under-reporting cases that can emit
   `PASS rc=0` while a filesystem or network sink disappears. The reproduced RP6 `1/37`
   and RP7 `4/65` outputs are deterministic lower-bound diagnostics from an unsound
   analyzer; they are not unresolved-path counts, closure evidence, or a freeze gate.

5. **The successor-preregistration review.** `SKELETON_REVIEW_CODEX_2026-08-10.md` is
   `NEEDS-WORK: 13 items`. Audit 2 needs the final accepted successor, not the skeleton:
   exhaustive fill manifest, targeted fills, composite path proof, rows 1-9 disposition,
   P0 environment reconciliation, current transport semantics, close-script contract,
   removal of inert pins, and resolved-status cleanup must all be reflected.

6. **The two-commit Stage-1/attestation order.** Before grant-#6 input acquisition, commit
   the exact read-only attestation command and evidence grammar. Run that committed command
   outside the login domain; then fill each consumer, complete and commit the final
   successor/runkit, and only then allow operations 01-12. This Stage-1 freeze precedes
   WP-I execution and is distinct from the later pre-WP-A checkpoint freeze.

7. **A D026 map for the current WP-I work, not only the earlier WP-L/B3 cycle.** Map every
   new RP6, RP7, transport, rows-1-9, and pathscope closure test to exact RED command/output,
   exact pre-fix or mutation identity, exact GREEN command/output, and final accepted
   bytes. Current audit REDs without a repaired GREEN remain open; helper-only or
   non-literal fence evidence remains supplemental.

8. **The final freeze-input ledger and accepting-input evidence.** It must reconcile every
   duplicate consumer: RP6's six embedded pins, RP7's projection/trusted-Python/evidence-root
   pins, both tool maps, five row-8 attestation values and wrapper copies, transport mount,
   OpenSSH configuration and credential digests, close-script identity, archive/member
   digests, block/wrapper hashes, allocation values, and evidence-root provenance. RP6 has
   no end-to-end PASS while its six pins are literals; RP7 requires three values and a
   recorded accepting-input arm; transport remains marker- and target-state-gated.

9. **Actual WP-I execution and closure evidence.** No WP-I host run, concrete RUNID,
   no-clobber evidence tree, rows 1-24 result set, retrieval/binding record, or WP-I closure
   index exists. Audit 2 cannot infer DISARMED state, restart policy/count, MainPID,
   candidate binding, sandbox state, listener state, package parity, or transport chain
   from local QA.

10. **One authoritative frozen-SHA audit bundle.** Supply the pre-WP-A full SHA, exact base
    and diff, frozen file list, candidate/artifact/manifest identities, mandated suite
    command, exact expected rc/counts, exact accepted anomaly IDs/signatures, and isolated
    worktree instructions. None may be inferred from a pre-freeze working tree or an older
    candidate description.

11. **Current authority and ledger closure.** Carry the owner grants and every hard
    exclusion into one final WP-I authority record; separately record any still-required
    go/no-go or budget lift. Book all WP-I work prospectively and obtain one owner-ratified
    freeze-time balance. Neither technical interlocks nor an old provisional balance may
    stand in for authority or ratification.

## Premise inheritance

| Audit 2 stated premise | Unestablished WP-I result | Artifact(s) it waits on |
|---|---|---|
| `WP-I staging-verification closure` | No accepted, executed, closed WP-I result exists. | Final successor preregistration; accepted RP6-P0; accepted rows-1-9 implementation or approved deferral; accepted RP7 rows 10-23; accepted transport; actual run evidence and WP-I closure record. |
| `frozen source, candidate, artifact, and manifest identity` | The current executables are not jointly accepted, required freeze values are unfilled, and the pre-WP-A checkpoint does not exist. | RP6, RP7, transport, rows 1-9, Stage-1 fill manifest/runkit, then the pre-WP-A checkpoint manifest. |
| `WP-I transport chain of custody, preregistration ordering, RUNID accounting, and hashes` | The WP-I transport set has divergent flagship verdicts and has not run; no concrete WP-I RUNID or create-once evidence root exists. | Transport round-4 repair/re-audit, final plan/successor, committed attestation order, and actual transport/evidence records. |
| `WP-I current-state proofs` | Rows 1-9 have no executable; rows 10-23 are not finally accepted or executed; row 24 is operator-side and unexecuted. | New rows-1-9 artifact/operation, final RP7, transport op 06, and host evidence. |
| `D026 RED/GREEN evidence for every new test offered as closure evidence` | The package maps mostly the older WP-L/B3 work and does not map the current repair cycles; several current audits have RED but no accepted GREEN. | Final RP6, RP7, transport, rows-1-9 and pathscope evidence packages. |
| `authority, budget, and sequencing compliance` | The successor is not accepted, the two-commit order has not run, and the current prospective ledger is not owner-ratified. | Final authority record, successor preregistration, attestation/freeze commits, execution record, and freeze-time ledger source. |
| `complete path-scope/security boundary` | Section 10.1 is incomplete and the section 10.2 prover is unsound. | Repaired blocks, amended section 10.1, repaired/accepted pathscope prover, and composite wrapper+library+block proof. |
| `mandated suite result and accepted anomaly set` | No exact authoritative command, baseline, IDs, or signatures are frozen. | Freeze-time baseline source and both auditors' execution in clean worktrees. |

Audit 2 therefore cannot honestly start merely because host-contact and budget authority
arrive. It waits on the artifacts and results named above.

## Ordering

The high-level order remains coherent:

`WP-L Phase 2 closure -> WP-I closure -> pre-WP-A checkpoint freeze/ledger ratification -> Audit 2 acceptance -> WP-A -> Gate B`

Two corrections are required.

First, remove the claim that Audit 2 freezes the SHA; it audits an already frozen SHA.
Second, expand the WP-I segment to show the blockers and the separate Stage-1 freeze:

`repair/design closure -> final artifact acceptances -> committed pre-attestation command -> grant-#6 input acquisition -> targeted fills + final successor/runkit Stage-1 commit -> authorized WP-I execution -> WP-I closure -> pre-WP-A checkpoint freeze + ledger ratification -> Audit 2`

The rows 1-9 gap, section 10.1 changes, and pathscope repair belong before final artifact
acceptance because each can change the bytes or the accepted scope. Transport's remote
interpreter/TMPDIR/STOP/prerequisite defects also belong before Stage-1 freeze. None of
these blockers moves Audit 2 after WP-A or permits WP-A early; they add mandatory work
before WP-I can close.

## Honest-start condition

Audit 2 can honestly begin only when the final post-repair RP6, rows-1-9, RP7, transport,
and successor artifacts have the required accepting reviews on exact frozen identities;
section 10.1 and the composite section 10.2 proof are accepted; every freeze input and D026
pair is mapped; the authorized WP-I run has produced closed, immutable evidence; the
pre-WP-A checkpoint SHA/diff/candidate identities and mandated-suite baseline are frozen;
and the authority record and 50-hour ledger are ratified. Until then, the readiness
package is an obsolete assembly aid, not a dispatchable Audit 2 input bundle.
