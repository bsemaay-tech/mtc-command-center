# VERDICT: REQUEST_CHANGES

**TIER:** T1  
**APPLIED AUDITOR CONTRACT:** Codex `gpt-5.6-sol`, xhigh per the explicit round-10 kickoff; fresh independent flagship audit; T1 round cap 2.  
**AUDIT SUBJECT:** commit `a0ebac7b`, SEC102 composite pathproof round 10.  
**GIT MUTATION:** none.

## Required findings

1. `SELF_QA_SEC102_R10.md:1647-1654,1841-1852,2608-2617`; `SEC102_R10_REPORT_2026-08-12.md:192-201`; `STATUS_SEC102.md:812-821` — **MEDIUM — Pattern 11, with Patterns 6 and 9 overlays:** the disclosed volume/drive-letter rebind is not guaranteed to be detected. The wrapper samples the pathname identity before `subprocess.run`, waits for the child to exit, and samples the pathname again. A same-session actor can re-point the mutable DOS-device/volume mapping after the pre-launch sample, let the child resolve the same pathname to different bytes, and restore the mapping before the post-run sample. Both samples then match the pinned object and its unchanged bytes, so the alternate child output can reach the published-subset comparison and be accepted. The post-run check detects a rebind that persists until line 2616; it does not detect a transient rebind-and-restore. That contradicts both the core contract (“executed bytes differ from compared bytes without rejection”) and the statements that the residual is terminal and that there is no path on which unproven bytes execute.

   **Minimum required repair:** give the child a path whose volume identity cannot be rebound independently of the pinned object—such as a stable volume-GUID/device path derived and checked from the held object—or use another execution channel that consumes the pinned bytes without mutable name resolution. A post-run snapshot alone is insufficient. Add deterministic D026 RED/GREEN evidence in which the mapping diverges only across the child’s open and is restored before the post-run gate; round 10 must false-accept or otherwise fail to reject the RED, and the repaired wrapper must reject it before interpreting stdout.

2. `SELF_QA_SEC102_R10.md:2514-2533,2557-2605` — **MEDIUM — Patterns 3 and 11, with Pattern 13 overlay:** `for component in [WORK] + list(WORK.parents)` acquires directory handles leaf-to-root, but the wrapper stores only handles and a count. It never records each component’s object identity, proves parent/child adjacency, or re-resolves the completed set as one coherent current chain. While a higher ancestor has not yet reached its turn, it can be renamed and replaced; the later opens can therefore pin a mixture of components from different historical chains. The already-passed lower name in the new live chain remains unpinned. A transient swap of that unpinned live component around the child open, restored before the sole post-run leaf check, has the same accepted-divergence shape as finding 1. `PATH_PIN_HELD=7` proves seven handles were obtained, not that all seven handles bind the pathname later passed to PowerShell.

   **Minimum required repair:** construct and validate one coherent root-to-leaf chain, preferably by opening each child relative to the already pinned parent and carrying a stable identity for every component; otherwise re-resolve and compare every component to its held identity after acquisition and bind execution to a stable volume path. Add deterministic RED/GREEN evidence for an ancestor swap during pin acquisition and for a transient component swap around the child open. Counting handles is supplemental, not closure evidence.

## Independent verification

### Scope and identity

- Commit `a0ebac7b` changes exactly the three declared round-10 evidence-harness files: new `SELF_QA_SEC102_R10.md`, new `SEC102_R10_REPORT_2026-08-12.md`, and modified `STATUS_SEC102.md`. It changes no Pine, parity, MTC, trading, production, host, network, or protected file. `git diff --check a0ebac7b^ a0ebac7b` returned 0.
- The current round-10 files are identical to their `a0ebac7b` versions.
- `composite_pathproof.py` is unchanged from the round-8/round-9 input and from `a0ebac7b`: Git blob `0e00db0ef3324765118f4e313f8e1964d451bd70`, 129658 bytes, SHA-256 `adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`. Round 10 is harness-only.

### Verbatim execution evidence

All detailed fixture output was redirected to temporary files outside the repository. No new attack fixture was authored, and no sensitive fixture body is reproduced here.

1. The exact section-3 PowerShell fence was extracted as bytes and run from outside the repository. Process status was 0 and stderr was empty:

   ```text
   CASES=58 FAILED_COUNT=0
   ```

2. Section 13b was extracted as bytes and run verbatim. The published R9 finding and R10 direct-leaf repair reproduced in both directions with a real sharing-violation result; all six R9 verdicts and M1/M2/M3 were conserved/exercised:

   ```text
   D026 REBIND=rebind_certified R9_HOLD=ACCEPTED/rc0 R10_HOLD=REJECTED/rc1 R10_REASON=MISMATCH REBOUND_UNDER_R9=1 REBOUND_UNDER_R10=0 R10_DENIAL=SHARING_VIOLATION_32/1 R9_ASSERTED_IDENTITY=1
   D026 REBIND=rebind_honest R9_HOLD=REJECTED/rc1 R10_HOLD=ACCEPTED/rc0 R10_REASON=OK REBOUND_UNDER_R9=1 REBOUND_UNDER_R10=0 R10_DENIAL=SHARING_VIOLATION_32/1 R9_ASSERTED_IDENTITY=1
   D026_PIN_PRECONDITION EXISTING_WRITER=1 PIN_TAKEN=0 WINERROR=32 OK
   D026_CARRIED=6 CONSERVED_R9_VERDICTS=6 D026_REBIND=2 FALSE_ACCEPT_UNDER_R9=1 FALSE_REJECT_UNDER_R9=1 REBIND_DENIED_UNDER_R10=2 M1_GATE_FIRED=1 M2_EXCLUSION_MEASURED=1 M3_POST_RUN_GATE_FIRED=1 D026_OFF_EXPECTATION=0
   ```

   The exact block returned 0 with zero stderr. Its own adjudication requires `INPLACE_WRITE=DENIED WINERROR=32` and `ENTRY_REPLACE=DENIED` on both R10 rebinding cases before it can emit `R10_DENIAL=SHARING_VIOLATION_32/1`; that predicate reproduced. `M2` proves share-mode widening is caught before the child. `M3` proves a persistent post-run byte divergence is terminal with stdout unread. Neither arm covers a transient volume or component rebind restored before the post-run sample.

3. The sole section-13c Python fence was extracted as bytes, written outside the repository, and run there against the final self-QA document. The executed wrapper was 19602 bytes with SHA-256 `fa17160a92612c93280ca451b06ad7bf8c1bca008b2d8345c1996bf7c303f1bb`. The wrapper returned 0 with zero stderr; all eleven write/delete exclusion probes returned `WINERROR=32/32`; the complete 36-line transcript matched section 13d exactly:

   ```text
   BLOCKS=11 SCRIPT_BYTES_IDENTICAL_ALL=11 PINNED_ALL=11 NAME_BOUND_ALL=11 POST_NAME_BOUND_ALL=11 POST_BYTES_UNCHANGED_ALL=11 REJECTED_ON_BYTES=0 REJECTED_ON_BINDING=0 STATUS_PROVED_COMPLETE=11 REJECTED_ON_STATUS=0 REJECTED_ON_STDERR=0 COMPARED=11 MISMATCHED=0 REJECTED=0
   OUTER_WRAPPER_RC=0
   OUTER_WRAPPER_STDERR_BYTES=0
   ```

### Core pin attack result

- **Share-mode widening:** caught. M2 makes the measured exclusion fail before any child is launched.
- **Direct leaf replacement/modification:** caught while the leaf pin is held; the operating system returned sharing violation 32.
- **Persistent post-run divergence:** caught. M3 reaches gate 4 and refuses with stdout unread.
- **Handle reuse:** no surviving path found. The leaf handle remains live through child exit and both post-run measurements, and it is not used after `CloseHandle`.
- **Path-component swap:** not closed because the leaf-to-root acquisition does not establish a coherent current chain; required finding 2.
- **Volume/drive-letter rebind:** not honestly closed as “detected” for the full class. A persistent rebind is detected, but a transient rebind restored before the post-run snapshot is silently admitted; required finding 1.

## Thirteen-pattern adjudication

- **Patterns 1-2 and 4-8:** no new module regression. The 58-case matrix passed, the production prover is frozen, and no host or production claim was added.
- **Pattern 3:** required finding 2. The wrapper counts directory handles without proving that they constitute the pathname’s current component chain.
- **Pattern 9:** both required findings invalidate the unconditional executed-byte and terminal-detection sentences.
- **Pattern 10:** literal reproducibility passed: the matrix, section 13b, byte-extracted section 13c, and section 13d transcript all reproduced. The existing D026 arms are nevertheless supplemental for the two untested temporal paths above; they cannot prove closure of a class they do not discriminate.
- **Pattern 11:** both required findings. The declared pinned instrument is still not bound to the real top-level caller across every mutable resolution layer.
- **Pattern 12:** M1/M2/M3 exercise the published byte, direct-share, and persistent post-run branches, but transient path/volume rebinding is absent from the model and disappears between its two samples.
- **Pattern 13:** all eleven clean-run blocks reached terminal dispositions, but `PATH_PIN_COMPONENTS=7` lacks one stable identity and adjacency disposition per component. The pin-set conservation claim is therefore not established.

## Acceptance consequence

Round 10 closes direct same-object modification/replacement while the leaf pin is held and preserves every earlier SEC102 verdict, but it does not close the broader executed-byte binding class. This verdict does **not** close the SEC102 Codex flagship slot. The two original CRITICALs, R3-F2/F3, command-word whitelist fixpoint, round-7 child-completion gate, and round-8 byte-identity gate remain closed; the round-9 executed-byte binding remains open on the two paths above. Because this T1 flagship raised findings and the diff exceeds 300 lines, the policy-required GLM-5.2 second opinion is also required before acceptance, after the Lead adjudicates and repairs the reproduced findings.

## Repository-delta proof

The pre-audit dirty worktree contained only pre-existing untracked logs/scratch artifacts and was preserved. The only repository path created by this audit is this verdict file. No tracked file was modified, and no Git command mutated repository state.
