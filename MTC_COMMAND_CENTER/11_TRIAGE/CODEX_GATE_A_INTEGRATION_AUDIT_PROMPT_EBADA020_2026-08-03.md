# Codex `gpt-5.6-sol` xhigh — final canonical audit of Gate A integrated SHA `ebada020`

This is the **second flagship** audit required by D025. It is the **only** thing blocking acceptance
of `ebada020`. Everything below the horizontal rule is the prompt; paste it verbatim.

Launch Codex only via `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1`
(default `-Account secondary`). Never run bare `codex`, never route to `C:\Users\BarışSemaay\.codex`.

**Known operational hazard — read before dispatching.** Codex CLI has repeatedly run as
`sandbox: read-only` and refused every command as `blocked by policy` outside a trusted project
directory. That is not a quota problem and it has caused prior Gate A auditor BLOCKs. Confirm the
worktree `C:\GAAUD_INT_GLM` is a trusted directory for the session, or the audit is predetermined to
BLOCK and the round is wasted. The same class of failure already cost one GLM round.

---

## PROMPT

You are the canonical Codex `gpt-5.6-sol` xhigh auditor under D025, and you are the **second
flagship**. A first canonical auditor has already run. Your verdict decides whether the Gate A
integrated candidate is accepted.

Your worktree is `C:\GAAUD_INT_GLM`, detached at `ebada020a59edf539f60acfbb3a6bf870c8679e9`, clean.
Do not modify, create, delete or rename files. Do not stage, commit, push, or switch branches. Do
not touch `codex/gate-a-integration` — its head must stay equal to the artifact's build SHA.
Running tests and read-only git/filesystem commands is required and expected.

### What the candidate is

`ebada020` merges four separately audited and accepted product commits onto `origin/master`
`637307e8`:

- `82e92c98` — build determinism: `deploy/linux/lib/common.sh`, `deploy/linux/package.sh`, `tests/test_linux_deployment.py`
- `7aad0377` — WAL/SHM validation before capture: `tools/wal_state_bundle.py`, `tests/test_wal_state_bundle.py`
- `17402a58` — credential-free DISARMED start mode: `bridge/app.py`, `bridge/api/routes.py`, new focused test
- `ebb750da` — residual evidence-test stabilization: `.gitattributes`, `tests/test_wal_state_bundle.py`

Each input was accepted individually. **The merge itself is what you are auditing.**

### D025 rules that bind you

1. If you cannot execute the test suite, you must return **BLOCK**. A verdict from reading alone is
   not evidence and will be discarded. If the sandbox refuses commands, say so plainly and BLOCK —
   do not substitute analysis for execution.
2. Report only what you actually ran. Paste real output. Never paraphrase a count you did not see.
3. State each finding precisely enough for the Lead to reproduce it: exact file, exact line, exact
   command, observed versus expected. A finding binds only after the Lead reproduces it.

### Evidence already on record — verify, do not assume

Treat every line here as a claim to re-measure, not a fact to accept. Pasted hashes in prior reports
are claims; the first auditor once pasted a mangled hash and asserted equality.

| Claim | Recorded value |
|---|---|
| Scope vs `origin/master` | exactly nine files |
| Merge structure | four merges, first-parent chain from `637307e8` |
| Windows full suite | `1359 passed, 1 warning` |
| Locked-Linux candidate | `2 failed, 1357 passed, 1 warning` |
| Locked-Linux parent `637307e8` | `25 failed, 1281 passed, 1 warning` |
| New failure node IDs in candidate | **none**; 23 failures fixed |
| Ledger blob and worktree SHA-256 | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e`, 0 CR bytes |
| Artifact `RELEASE_SHA` | `ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| Artifact manifest SHA-256 | `8FC30864BA342E53DCFC6B2938124F91D005F02671A332580A723F38FD4700C9`, 7059 entries |
| Artifact `deploy/linux/*.sh` | 0 CR bytes on all five — the A-2 defect is absent |

Records: `11_TRIAGE/GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`,
`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md`,
`GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`.

### Mandatory executed checks

1. `git rev-parse HEAD` equals `ebada020a59edf539f60acfbb3a6bf870c8679e9`; `git status` clean at
   start and at end.
2. `git diff --name-status 637307e8..HEAD` — exactly nine files, each inside one of the four scopes.
   A tenth file is FATAL.
3. `git log --format='%h %p %s' -5 HEAD` — four merges, first-parent chain from `637307e8`; confirm
   each product SHA with `git merge-base --is-ancestor <sha> HEAD`.
4. **Windows full suite**, from `C:\GAAUD_INT_GLM\IBKR_PAPER_BRIDGE`: `python -m pytest -q`
   (~3 minutes). Report the exact final line. If yours differs from `1359 passed, 1 warning`, report
   yours — never adjust it to match.
5. Conflict site `tests/test_wal_state_bundle.py:890`. Confirm `SCHEMA_VERSION_BASELINE` is imported
   and resolves to `4` (`bridge/store/db.py:268`); that the base `637307e8` asserted `"2"`, the WAL
   branch the literal `"4"`, and the residual branch the derived form; and that the merged result is
   behaviourally equivalent today and strictly more robust to a future baseline bump.
6. Ledger `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json` — blob and
   working-tree SHA-256 both `f4cdece5…`, zero `0x0D` bytes.
7. Artifact at `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9\`, read-only: `RELEASE_SHA`
   equals the source commit; `RELEASE_SHA256SUMS` hashes to `8FC30864…4700C9`; the five
   `deploy/linux/*.sh` carry zero CR bytes; and the manifest's recorded hashes match actual bytes
   rather than being a stub.

### Optional but valuable — locked-Linux reproduction

The Lead's Linux floor is already on record; reproducing it independently would strengthen the
round. If you attempt it, the host is `GATEA-STAGING` at `172.24.55.233`, user `gatea`, identity
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`. Run suites with the host-locked venv
`/opt/mtc-bridge/venvs/a1dd5b467b12421f632bf3d8462a7244b39b2287/bin/python` (pytest 9.1.1,
root-owned and read-only — install nothing, modify nothing). **Never touch KVM2. Never read, print,
copy, rotate or modify key contents.** If you cannot reach the host, say so and continue; this is
not a BLOCK condition on its own.

### The real question — semantic merge safety

Only one textual conflict occurred, so everything else merged silently. **Find what merged silently
and should not have.** A merge of two individually correct commits can be wrong with no conflict.

- Does any interaction exist between the DISARMED start path and WAL capture or state-bundle
  behaviour that neither branch tested in isolation?
- Do the build fix's `core.eol=lf` export and the new `.gitattributes` rule interact — could the
  rule change what `package.sh` exports, or double-apply normalization?
- Two branches edited `tests/test_wal_state_bundle.py`. Did the merge drop, duplicate or weaken any
  test present on either parent? Compare `^def test_` name sets, not just counts.
- Does any test now pass for a different reason than on its own branch — for instance an assertion
  that became vacuous after the merge?

The first auditor examined all four axes and found no defect. **Do not treat that as a reason to
look less hard.** It executed only on Windows and could not reach Linux.

### Verdict

`PASS`, `PASS-WITH-NITS`, `REQUEST_CHANGES`, or `BLOCK`. Do not qualify a pass by platform: the
locked-Linux floor is on record as Lead evidence, so a Windows-only execution plus your review of
that recorded evidence is sufficient for a full verdict — but say explicitly which floors you
executed yourself and which you are relying on the record for.

### Report format

```
VERDICT: <PASS | PASS-WITH-NITS | REQUEST_CHANGES | BLOCK>
HEAD verified: <sha>   git status start/end: <clean?>
Scope: <n files, list>
Ancestry: <4 merges? each product SHA an ancestor?>
Windows suite: <exact final pytest line>
Linux floor: <executed by me | relied on Lead record | unreachable>
Conflict site: <verified / defect>
Ledger LF: <hashes + CR count>
Artifact: <RELEASE_SHA, manifest hash, CR counts, manifest consistency>
Silent-merge analysis: <what you checked, what you found>
REQUIRED FINDINGS: <numbered, file:line, command, observed vs expected — or "none">
OPTIONAL NITS: <numbered — or "none">
EXECUTED BY ME vs RELIED ON RECORD: <explicit split>
```
