# Integration audit round 1 — `ebada020` (2026-08-03)

**Result: `ebada020` is NOT ACCEPTED.** One canonical auditor returned **BLOCK**, the second
flagship has not run, and the locked-Linux floor does not exist. This record exists so the BLOCK is
not mistaken for a defect finding, and so the auditor's read-only work is not thrown away.

Companion records: `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`,
`GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`.

---

## 1. Dispatch

| Item | Value |
|---|---|
| Auditor | GLM-5.2 via `Invoke-GlmAudit.ps1` (read-only prefix enforced by the helper) |
| Worktree | `C:\GAAUD_INT_GLM`, detached at `ebada020`, clean |
| Prompt | `C:\tmp\glm_integration_audit_ebada020_prompt.md` |
| Report | `C:\tmp\GLM_AUDIT_INTEGRATION_EBADA020_2026-08-03.txt` |
| Verdict cap | `PASS-WINDOWS-ONLY` — an unqualified PASS was explicitly denied, since no Linux host is in the auditor's reach |

## 2. Verdict: **BLOCK** — environmental, not a candidate defect

The auditor could not execute the test suite: `python -m pytest` and `pytest` were refused on every
invocation with `This command requires approval`, including with the sandbox override, so it is an
allowlist gate rather than a sandbox condition. It also could not read
`C:\WPI_ARTIFACTS\ebada020…`, which lies outside its allowed working directory.

D025 rule 1 makes BLOCK the only permitted verdict when the suite cannot be executed. The auditor
applied it correctly and refused the `PASS-WINDOWS-ONLY` option that was open to it, recording the
Windows floor as *"unreproduced, not confirmed and not refuted."*

**This is the rule working as designed.** GLM-5.2 previously returned PASS-WITH-NITS on a commit
carrying two severe defects while unable to run the suite at all; that event is why the
BLOCK-on-non-execution rule exists. This round it self-blocked instead.

**It reported zero required findings against the candidate and zero optional nits.**

## 3. Read-only findings — every one independently reproduced by the Lead

The auditor's non-executing work is real and was re-derived here from the same tree:

| Auditor claim | Lead reproduction |
|---|---|
| Scope is exactly nine files, each inside one of the four accepted scopes | Confirmed |
| Four merges on the first-parent chain from `637307e8`; `82e92c98`, `7aad0377`, `17402a58`, `ebb750da` all ancestors | Confirmed |
| Test-function counts `637307e8`=41, `7aad0377`=58, `ebb750da`=41, `f6478e53`=58, `ebada020`=58 | Confirmed exactly |
| HEAD's test-name set is **identical** to `f6478e53`; `ebb750da`'s is a strict subset | Confirmed — `diff` empty, `comm -23` empty |
| Base `637307e8` asserted `inv["schema_version"] == "2"` at line 321 | Confirmed |
| Ledger blob and working-tree hashes both `f4cdece5…`, zero CR bytes | Confirmed |

The test-set result matters most: **the merge dropped, duplicated and weakened nothing.** That is
the most concrete silent-merge risk, and it is closed.

The auditor also supplied a fact the Lead record lacked — the base asserted `"2"`, the WAL branch
raised it to the literal `"4"`, and the residual branch derived it from the base. So the merged
derived form **preserves the WAL branch's v2→v4 intent** rather than merely coinciding with it.
That strengthens the conflict-resolution justification already recorded.

### Silent-merge analysis, four axes, no defect found

1. **DISARMED × WAL/state-bundle.** The WAL preflight is pure read-only byte inspection before any
   `sqlite3` connect; the DISARMED path only changes runtime wiring and writes `app_state`. They
   share only the store DB, and the `app_state` write cannot affect WAL/SHM presence.
2. **Build fix × `.gitattributes`.** `package.sh` exports with `core.autocrlf=false core.eol=lf`;
   the added `ledger_schema.json text eol=lf` is consistent with that and with the pre-existing
   `* text=auto`. Git normalizes once on archive — no double normalization, no changed export bytes.
3. **Two branches editing the same test file.** Covered by the test-set comparison above.
4. **Vacuous-pass check.** `test_invariants_preserve_risk_and_history` is a genuine round-trip
   equality against the fixture store's initialized baseline, not a vacuous assertion.

## 4. Lead reproduction of the Windows floor

The auditor could not run it, so the Lead did, in the same fresh detached worktree:

```
cd C:\GAAUD_INT_GLM\IBKR_PAPER_BRIDGE
python -m pytest -q
→ 1359 passed, 1 warning in 130.09s (0:02:10)
```

This matches the `1359 passed, 1 warning` floor claimed for `ebada020` on an independent run in an
independent worktree. **It is Lead evidence, not auditor evidence** — it does not repair the BLOCK
and does not substitute for an executing canonical audit.

## 5. Report-quality nit

The auditor pasted a truncated working-tree hash (`…a0535e21d668bda90e`, missing characters against
the blob's `…a0535e3e21d668bda90e`) and asserted the two were equal. The Lead measured both directly
and they are in fact equal, so nothing is wrong with the candidate — but an auditor asserting
equality over a mangled transcription is worth recording. Treat pasted hashes in auditor reports as
claims to re-measure, never as measurements.

## 6. D025 status — what is still owed

| Requirement | State |
|---|---|
| First canonical executing auditor | **BLOCK** (environmental) — does not count as accepting |
| Second flagship (`gpt-5.6-sol` xhigh) | **not run** |
| Locked-Linux full-suite floor | **does not exist** |
| Required findings outstanding | none reproduced — none were raised |

To convert this to an accepting round, an auditor session needs an allowlist that permits
`python -m pytest` and read access to `C:\WPI_ARTIFACTS\ebada020…`. Everything non-executing is
already verified and clean; only execution-based evidence is missing.

## 7. Boundary

Read-only audit, one test-suite execution, and doc authoring. `origin/master` unchanged,
`codex/gate-a-integration` head unchanged at `ebada020`, artifact bytes untouched. No merge,
deployment, service or runtime change, credential handling, broker call, ARM, order, TESTNET,
mainnet, Pine/parity/MTC/trading change or economic action.
