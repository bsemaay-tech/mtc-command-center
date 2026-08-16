Status: P9 KICKOFF REPAIR DRAFT — FOR LEAD REVIEW — dispatch requires Lead sign-off

# Packet 9 / P9-15 producer kickoff repair

Audit tier for this repair draft: **T3** — dispatch/process artifact; self-verification only. The future producer implementation is provisionally **T0** because it implements a cross-cutting security/secret-scan trust boundary and invokes pinned subprocesses. The producer must not dispatch its own audit; the Lead must confirm the tier and own all later acceptance.

## 1. Located contract and authority chain

The relevant current documents are:

1. The governing Packet-9 scope defines P9-15 as the sole missing producing step and requires its exact producer/command/evidence contract to exist before production. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39-45`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:118`
2. The upstream producer contract defines the three-artifact design. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:43-55`
3. The implementable specification inherits those artifact names and roles, declares its normative words to be implementation requirements, and supplies the exact interfaces and evidence grammar. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:11-25`
4. The night index marks both the producer contract and the implementable specification `CURRENT`; it identifies neither as superseded. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:68-69`
5. The blocked attempt record is the disposition of the defective kickoff, not a replacement producer contract. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_IMPLEMENTATION_2026-08-16.md:1-8`

The authority chain for this question is therefore:

```text
AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md
  -> AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md
  -> P9_15_PRODUCER_SPEC_2026-08-15.md
  -> producer kickoff
```

The scope is upstream of the contract; the contract is upstream of the implementable specification; the kickoff must execute the specification without replacing it with a paraphrase.

## 2. Exact contradiction

| Defective kickoff clause | Normative specification clause |
|---|---|
| “Implement it as a single self-contained Python file under<br>`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`, plus its own falsification<br>suite as a second file. No third-party dependencies. Python 3.12-compatible syntax.”<br><br>`C:/tmp/lane_kick/P9IMP.md:22-24` | “The implementation consists of exactly these three Commit-2-tracked artifacts:<br><br>1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1`<br>2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py`<br>3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json`”<br><br>`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:15-19` |

The contradiction is both cardinal and architectural: two Python files versus exactly three production artifacts; `WPI_PREREG_DRAFT_ROUND1/` versus `AUDIT2_READINESS_PACKAGE/`; and a lone Python top-level program versus a PowerShell evidence-envelope owner, Python semantic child, and JSON policy. The defective kickoff's write fence also prohibited two normative artifacts and put the third at the wrong path. `C:/tmp/lane_kick/P9IMP.md:54-58`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:23-25`

**Which side the block record says is authoritative:** the specification. The block record explicitly calls it “The normative specification” and calls the three files the “normative implementation artifacts.” `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_IMPLEMENTATION_2026-08-16.md:30-38` This fact is not `UNKNOWN`.

## 3. Paper resolution

The specification side **should win**. This is derivable without selecting a new design:

- The defective kickoff itself acknowledges that the specification turned the producer contract into the implementable specification. `C:/tmp/lane_kick/P9IMP.md:14-20`
- The upstream producer contract already says that the future executable producer consists of the PowerShell runner, Python inventory child, and JSON policy at the three `AUDIT2_READINESS_PACKAGE` paths. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-53`
- The later specification says those exact names and roles are inherited from that producer contract. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:15-23`
- The night index keeps both documents current. `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_DOCUMENT_INDEX_2026-08-16.md:68-69`

No owner or Lead choice is needed to decide between the defective one-file design and the three-artifact design: the written authority chain converges on the latter. A **Lead call is still required before dispatch**, because the specification is expressly not authorized, the producer author/reviewer identities and final egress-policy bytes remain unknown, and the block record requires the coherent contract, reviewed policy grammar, and P9-06 fixture to be supplied before implementation. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:3`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:532-533`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_IMPLEMENTATION_2026-08-16.md:144-158`

## 4. Corrected producer kickoff — draft for Lead sign-off

The block below is the complete proposed kickoff. Do not dispatch it until every precondition is satisfied and the Lead signs it.

---

# Lane P9IMP2 — implement the normative P9-15 three-artifact producer

## Authority and status

This kickoff implements, but does not amend, `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md`. Read that file in full first, followed by `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md`, `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`, and `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

The entire specification is binding. The verbatim clauses below are included to prevent this kickoff from becoming a substitute specification. If this kickoff conflicts with the specification, **STOP and return the contradiction to the Lead; do not follow the kickoff paraphrase and do not improvise**.

This is a local implementation lane only. It does not authorize P9-15 production, Packet-9 execution, host contact, a gate verdict, merge, push, or acceptance.

## Dispatch preconditions — all mandatory

The Lead must satisfy and record all of these before dispatch:

1. Sign this corrected kickoff and explicitly select the normative three-artifact design. The prior one-file design is rejected.
2. Supply the exact frozen base SHA, a dedicated clean worktree `C:\P9IMP2`, and branch `codex/p9-15-producer-v2-20260816`. The implementer must confirm the supplied SHA and empty `git status --porcelain` before any write.
3. Supply the reviewed exhaustive egress grammar for the canonical `p9_15_policy.json`, including its exact bytes or an exact closed grammar matrix from which those bytes are mechanically produced, reviewer identity, and expected SHA-256. No implementer-selected network/egress semantics are permitted.
4. Supply the canonical P9-06 pin-record test fixture and its independent expected SHA-256, plus the assigned non-placeholder `producer_author` and `reviewer_identity`. The fixture must not authenticate itself.
5. Confirm this exact repository write allowlist:

   - `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1`
   - `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py`
   - `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json`
   - `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_FALSIFICATION_TESTS_2026-08-16.py`
   - `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_IMPLEMENTATION_ATTEMPT2_2026-08-16.md`

6. Confirm the dedicated create-once QA scratch root `C:\tmp\p9_15_qa\P9IMP2_20260816`. It is the only permitted non-repository write location. Record every retained QA path in the implementation report.
7. Confirm that the existing block record remains immutable: do not edit, delete, rename, replace, or overwrite `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_IMPLEMENTATION_2026-08-16.md` or rewrite commit `6ab04e34`.
8. Confirm the implementation audit tier and later independent audit contract. Provisional classification is **T0** because this is a cross-cutting security/secret-scan trust boundary with pinned subprocess execution. The implementer performs Gates 2–4 only; the Lead owns acceptance and any Gate-5/Gate-6 dispatch.

If any precondition is absent, inconsistent, placeholder-bearing, or unverifiable, do not start implementation. Return `BLOCK` to the Lead and identify the missing item. Do not create a replacement design or another speculative policy.

## Binding specification clauses — quoted verbatim

The following are the minimum clauses this kickoff must carry verbatim. They do not narrow the rest of the specification.

### A. Deliverables and trust boundary

> The implementation consists of exactly these three Commit-2-tracked artifacts:
>
> 1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_runner.ps1`
> 2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_inventory.py`
> 3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json`
>
> Those artifact names and their roles are inherited from the producer contract. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:43-53`
>
> The runner is the evidence-envelope owner. It validates the invocation and pins, starts the child, captures raw process streams and rc, classifies wrapper failures, writes the run envelope, hashes the finalized files, and writes `COMPLETE.json` last. The Python child is the semantic producer. It enumerates Git objects, parses the declared dependency sources, performs the content-redacted scan, derives the static egress inventory under the frozen policy, enforces conservation, writes the deterministic core, and emits the four-line child protocol. The policy is data, not executable code.
>
> P9-06 MUST bind the actual PowerShell, Git, Python, runner, inventory producer, and policy bytes before the process is launched. A self-check performed after an untrusted runner starts is supplemental rather than the root binding event; the repository rule requires every declared instrument to be connected to the real production caller. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895`

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:15-25`

### B. Exact runner interface

> The caller MUST invoke the pinned PowerShell executable with the following expanded argv, in exactly this order:
>
> ```powershell
> & '<PINNED_POWERSHELL_EXE>' -NoLogo -NoProfile -NonInteractive `
>   -File '<REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_runner.ps1' `
>   -RepoRoot '<REPO_ROOT>' `
>   -SourceSha '<COMMIT_2_FULL_40_LOWER_HEX_SHA>' `
>   -OutputRoot '<OPERATOR_RECORD_ROOT>\packet9\p9-15' `
>   -GitExe '<PINNED_GIT_EXE>' `
>   -PythonExe '<PINNED_PYTHON_EXE>' `
>   -PinRecord '<ABSOLUTE_P9_06_PIN_RECORD_JSON>' `
>   -PinRecordSha256 '<64_LOWER_HEX_SHA256>'
> ```
>
> The first six substitutions preserve the contract's proposed command surface. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:59-73`
>
> `-PinRecord` and `-PinRecordSha256` are mandatory clarifications. The contract requires comparison against P9-06 but gives the runner no path or expected digest for that evidence. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:75-95` The two added arguments remove that ambiguity: the path locates the record, and the separately supplied digest prevents the located record from authenticating itself.
>
> The runner MUST use advanced-parameter binding with all eight named parameters mandatory. It MUST reject positional arguments, aliases, repeated parameters, unknown parameters, empty strings, wildcard expansion, and trailing operands as `STOP/3/ARGUMENT_ERROR`.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:31-49`

### C. Exact child argv

> After pin and source preflight, the runner MUST invoke the child directly, without a shell, in this exact argv order:
>
> ```text
> <PINNED_PYTHON_EXE>
> -I
> -B
> <REPO_ROOT>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py
> produce
> --repo
> <REPO_ROOT>
> --source-sha
> <COMMIT_2_FULL_40_LOWER_HEX_SHA>
> --policy-ref
> MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json
> --output-root
> <PRIVATE_STAGING_DIRECTORY>
> --git-exe
> <PINNED_GIT_EXE>
> --pin-record
> <ABSOLUTE_P9_06_PIN_RECORD_JSON>
> --pin-record-sha256
> <64_LOWER_HEX_SHA256>
> ```
>
> `--git-exe` and the two pin-record operands are mandatory because the child must use the pinned Git binary and recheck its actual input binding; a bare `git` lookup is forbidden. The original contract requires Git-object reads and pinned-tool verification but its illustrative child argv did not carry those values. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:75-81,90-95`

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:106-130`

### D. Fail-closed policy boundary

> The exhaustive egress grammar matrix—recognized languages, commands, APIs, options, redirections, nested forms, endpoint extractors, and activation-predicate rules—is **UNKNOWN** because the contract names that policy content but does not supply its bytes. What settles it is the actual canonical `p9_15_policy.json`, reviewed and frozen at Commit 2. The generic implementation MUST treat an absent category, unknown policy key, unconsumed network-capable token, unsupported nested form, or non-exhaustive policy declaration as `UNRESOLVED` and `STOP/3/POLICY_COVERAGE_INCOMPLETE`; it MUST NOT guess or silently omit the construct. This is implementable without selecting new semantics: the engine consumes a closed policy grammar and fails closed until that input exists. The contract assigns modeled constructs to the policy at `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51`, and the fail-closed rule is at `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:919-929`.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:160`

### E. Deterministic compared-byte set

> Two completed runs with the same semantic inputs—identical `SourceSha` Git objects, policy blob, producer blob, pin-record bytes, and tool bytes—MUST produce byte-identical deterministic core files even when `RepoRoot`, `OutputRoot`, staging directory, operator, and run time differ.
>
> The compared-byte set is exactly:
>
> ```text
> dependencies.jsonl
> egress.jsonl
> rc.txt
> secret_scan.jsonl
> source.json
> stderr.bin
> stdout.bin
> summary.json
> universe.jsonl
> unresolved.jsonl
> ```
>
> For a PASS or source-derived FAIL, all ten MUST be byte-identical. For a STOP caused before complete source evaluation, determinism is checked only for whichever canonical semantic files were finalized; the STOP reason and missing/invalid `COMPLETE.json` prevent that run from serving as a successful replay.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:428-445`

> `command.json`, `environment.json`, `tools.json`, `elapsed_ms.txt`, `SHA256SUMS.txt`, and `COMPLETE.json` are run-envelope files and are explicitly excluded from cross-run byte comparison. `SHA256SUMS.txt` and `COMPLETE.json` are excluded because they intentionally bind the volatile envelope as well as the deterministic core. They MUST still verify internally for each individual run.
>
> No other nondeterministic field is permitted in the compared-byte set. If an implementation discovers one, it MUST return `STOP/3/EVIDENCE_IO_ERROR`; it MUST NOT add an unreviewed normalization or silently widen the exclusion list.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:465-467`

### F. Fresh replay contract

> From a fresh detached Commit-2 worktree, with the exact §2.4 environment and cwd set to that fresh root, run:
>
> ```text
> <PINNED_PYTHON_EXE> -I -B <FRESH_COMMIT2_WORKTREE>\MTC_COMMAND_CENTER\11_TRIAGE\AUDIT2_READINESS_PACKAGE\p9_15_inventory.py verify --repo <FRESH_COMMIT2_WORKTREE> --source-sha <COMMIT_2_FULL_40_LOWER_HEX_SHA> --policy-ref MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/p9_15_policy.json --evidence-root <ORIGINAL_P9_15_OUTPUT_ROOT> --git-exe <PINNED_GIT_EXE> --pin-record <ABSOLUTE_P9_06_PIN_RECORD_JSON> --pin-record-sha256 <64_LOWER_HEX_SHA256>
> ```
>
> Verifier stdin is closed. It does not alter `evidence-root`; it may use a private temporary directory whose path and metadata are excluded. Its stdout is exactly:
>
> ```text
> P9_15_VERIFY_BEGIN schema=p9-15/v1 source_sha=<40_lower_hex>
> P9_15_VERIFY_CHECK manifest=<PASS|FAIL|STOP> source=<PASS|FAIL|STOP> canonical=<PASS|FAIL|STOP> core=<PASS|FAIL|STOP>
> P9_15_VERIFY_RESULT class=<PASS|FAIL|STOP> rc=<0|1|3> reason=<UPPER_SNAKE_TOKEN>
> ```
>
> Verifier exit 0 means every structural, source, canonical, and compared-byte check passed. Exit 1 means a complete check established a mismatch. Exit 3 means a check could not be completed. The verifier MUST independently regenerate the compared-byte set and compare exact bytes; invoking the original result's claimed hash alone is insufficient.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:502-516`

### G. Mandatory falsification

> Before treating a new implementation's tests as closure evidence, record real RED and GREEN commands/output for all five mutations:
>
> 1. replace or remove one declared executable/artifact and drive the real top-level runner;
> 2. add one secret-signature fixture and prove the category/path is reported while match text never prints;
> 3. add one unknown or nested network sink and prove `UNRESOLVED` plus STOP/3;
> 4. add two dependency members that canonicalize to the same identity and prove STOP/3 rather than overwrite;
> 5. make one admitted blob read fail and prove STOP/3 rather than a reduced-universe PASS.
>
> The repository requires executable RED/GREEN evidence and specifically requires instrument replacement, unknown static forms, and disappearing/duplicate members to turn red. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:617-687,886-895,919-929,957-967`

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:520-528`

### H. Honest unknowns and authorization boundary

> - **Producer author/reviewer identity: UNKNOWN.** Settled by the Lead assignment and canonical P9-06 pin record before Commit 2. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:53-55,266-271`
> - **Final egress policy grammar bytes: UNKNOWN.** Settled by the reviewed Commit-2 `p9_15_policy.json`; until then the engine is implementable but a real PASS is unavailable because unknown coverage must STOP. `18f2c8b645828ec8900fb0e13d9c0f204b5c8763:MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51,101-109`
> - **Actual P9-15 counts, paths, hashes, class, and rc: UNKNOWN.** Settled only by executing the frozen producer against the real Commit-2 objects. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242`
> - **Numeric internal timeout: UNKNOWN and deliberately not invented.** There is no producer-owned timeout in v1; only caught cancellation is classified. What would settle a timeout is a separately frozen duration and clock contract in a pin/policy revision.
> - **P9-15 labour: NO SOURCED ESTIMATE.** The work catalogue supplies no bounded R15/Packet-9/WP-I price. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54,196-198`
>
> This specification does not implement the producer, create evidence, complete Packet 9, accept a result, open a gate, or authorize any action.

`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:532-538`

## Task

Implement the normative design as exactly three production artifacts at the three paths in clause A. The PowerShell runner owns the top-level trust boundary; the Python child owns semantic production and verification; the JSON policy remains data. Do not collapse, embed, relocate, or replace any of them.

Also create the allowlisted falsification suite and attempt-2 implementation report. These two QA/evidence files are not members of the three-artifact P9-06 production set and must never be added to that set.

Use no third-party dependencies. Use Python 3.12-compatible syntax. Follow every exact grammar, file set, ordering rule, canonicalization rule, status mapping, and finalization rule in the full specification. A deviation requires prior written Lead authorization and a specification revision; recording an unauthorized deviation in the report does not make it acceptable.

Before Gate 3, submit a Gate-2 plan to the Lead describing the runner/child/policy data flow, pin-binding path, deterministic-byte boundary, failure precedence, conservation checks, temporary/finalization behavior, RED/GREEN fixture construction, and rollback. Do not write implementation bytes until the Lead accepts that plan.

## Evidence required from the implementer

1. Execute the complete happy-path suite and every relevant negative case. Record exact commands and real stdout/stderr/rc.
2. Run two completed productions over identical semantic inputs in different create-once roots and compare the exact ten-file set in clause E byte-for-byte. Record the command, per-file hashes, and exact comparison output. Do not replace this with one aggregate hash.
3. Execute the exact fresh verifier path from clause F against the real produced evidence. A helper-level or reimplemented comparison is supplemental only.
4. Execute all five clause-G mutations against the real top-level path, recording a real RED and restored GREEN command/output for each. A test claimed as closure evidence does not count until shown RED against pre-fix/reverted behavior or an equivalent deliberate mutation and GREEN with the fix.
5. For every check, answer: **“What would have to be true for this check to fail?”** State where its expected value comes from, what lies outside its universe, and whether the property is enforced or merely asserted. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`
6. Carry this standing sentence exactly: **“State what would make this check fail, and show it failing.”** `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:73-77`
7. Include a force-inclusive enumeration proving that the repository diff contains only the five allowlisted paths and that no hidden cache, fixture, directory, or generated file entered the repository.
8. State honestly what the producer and its tests do not verify. Keep actual counts, results, hashes, policy coverage, timeout, and labour `UNKNOWN` wherever the specified evidence does not establish them.
9. The implementation report must cite `file:line`, list every command actually executed without placeholders or undeclared shell state, include real outputs, identify the independent expected value for each assertion, and distinguish closure evidence from supplemental evidence.

Do not self-accept. Return the plan, final commit ID, exact diff, test evidence, and implementation report to the Lead. The Lead must independently inspect the real files and reproduce proportionate validation; the implementer's report is not acceptance.

## Standard working rules

- Work only in the Lead-provided `C:\P9IMP2` worktree and named branch. Never work on `master`.
- Before writing, confirm the exact Lead-supplied base SHA and an empty `git status --porcelain`. If either differs, STOP.
- Preserve all existing and foreign changes. Do not use `git checkout`, `git reset`, or `git stash` on any tracked file.
- Stage only the five exact allowlisted paths. Never use `git add .` or `git add -A`.
- One ordinary commit is permitted after self-QA. No amend, rebase, merge, push, force operation, hook bypass, branch deletion, or worktree administration.
- Keep repository writes inside the five-file allowlist. Keep transient QA writes inside the dedicated create-once scratch root. Do not create caches in the repository; use isolated/no-bytecode modes where applicable.
- Cite `file:line` for every structural or contract claim.
- If the full specification is wrong, contradictory, underdetermined, or impossible to falsify, STOP and report the exact clauses to the Lead rather than inventing a repair.
- Do not edit the prior block record. Do not rewrite or amend commit `6ab04e34`.

## Hard exclusions

No host, network, SSH, deployment, service, credential store, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, `git commit --amend`, or economic action. Do not run the actual Packet-9 producer against live/future Commit-2 evidence and do not claim Packet 9 exists. Synthetic local fixtures and local Git-object tests are the only execution authorized by this kickoff.

Do not touch anything outside the exact repository allowlist and QA scratch root. Do not access `.env`, API keys, wallet material, broker/exchange credentials, external credential stores, user shell history, registry credentials, or remote-host content. Secret fixtures must be synthetic and must never emit matched text.

## No sub-delegation

Do this yourself. Do not invoke or shell out to `claude`, `claude.ps1`, Claude Code, `glm`, `gemini`, `hermes`, `cline`, or another `codex` process. Do not dispatch an auditor. The Lead owns any later independent audit and acceptance.

## Stop and hand back

Stop after committing the five allowlisted files and returning the evidence package to the Lead. No acceptance, merge, push, production run, Packet-9 closure, or handoff-memory mutation is authorized in this lane.

---

## 5. Lead sign-off record

Dispatch is forbidden until the Lead completes this block:

```text
Lead identity                    : <REQUIRED>
Sign-off UTC                     : <REQUIRED>
Frozen base SHA                  : <REQUIRED 40 lowercase hex>
Three-artifact design selected   : YES / NO
Reviewed policy attachment/hash  : <REQUIRED>
P9-06 fixture attachment/hash    : <REQUIRED>
Producer author                  : <REQUIRED>
Reviewer identity               : <REQUIRED>
Worktree/branch confirmed        : YES / NO
Five-path write allowlist        : YES / NO
QA scratch root confirmed        : YES / NO
Prior block record protected     : YES / NO
Implementation audit tier        : <REQUIRED>
Dispatch decision                : SIGNED / NOT SIGNED
```

Until every required field is concrete and `Dispatch decision` is `SIGNED`, the producer lane remains undispatched.
