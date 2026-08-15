# Bridge suite anomaly repairs — independent T1 audit — 2026-08-15

## Verdict

**PASS-WITH-NITS**

Both repairs are correct, correctly scoped, and supported by evidence that
reproduces. The A2 assertion has real discriminating power — I proved that
myself against the real test rather than accepting the implementer's proof.
No finding below is REQUIRED; all four are NITs and none blocks acceptance.

Auditor: Claude (`claude-opus-5`), independent of the implementer
(Codex `gpt-5.6-sol`). Read-only except this file. No Git mutation performed —
no `commit`, `add`, `checkout`, `reset`, `stash`, `merge`, `push`, or
`worktree`. No host, network, deployment, service, credential, broker/exchange,
ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push,
or economic action occurred. No other worktree was touched.

## Subject confirmation

```text
> git rev-parse HEAD
6c746b65411d5e646da407614f95f8a1174f3a5a

> git rev-parse --abbrev-ref HEAD
codex/bridge-suite-anomaly-repairs-20260815

> git status --porcelain
(empty)
```

`git status --porcelain` was empty before I started and empty again after all
audit work — re-checked at the end, still empty. Everything I wrote outside this
file went to a session scratchpad outside the repository.

The repair commit is `6c746b65`, confirmed by `git log`, and its parent is the
declared base `678d4be2`. The line in the kickoff was not trusted on its own.

## Changed-file verification (check 5)

```text
> git diff --stat 678d4be22ddde2201948de0d60343c1edfa85a06 HEAD
 .gitattributes                                     |   1 +
 IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py   |   9 +-
 ...RIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md | 358 +++++++++++++++++++++
 3 files changed, 367 insertions(+), 1 deletion(-)

> git diff --name-status 678d4be22ddde2201948de0d60343c1edfa85a06 HEAD
M       .gitattributes
M       IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py
A       MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md
```

Exactly the declared set. **No undeclared change.** No product code was
modified — `test_wal_state_bundle.py` is a test, `.gitattributes` is repository
configuration, and the third file is a new report. No `WPI_*` file was touched.
Nothing outside the declared set was touched.

## A1 — is the `.gitattributes` pin correct, and does it actually work? (checks 1, 2)

### Root-cause table reproduces exactly

I recomputed both byte identities from the Git object rather than copying the
report's numbers:

```text
LF   bytes= 867 sha256=f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
CRLF bytes= 903 sha256=b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a

LF   claim reproduces: True
CRLF claim reproduces: True
```

Both the report's and Packet 10's root-cause tables are correct. The recorded
`artifact_sha256` in `EVIDENCE_LEDGER.jsonl` is `f4cdece5…`, i.e. the LF form,
confirmed by reading the ledger directly.

### Current worktree state

```text
> git ls-files --eol -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
i/lf    w/lf    attr/text eol=lf        MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json

> Get-FileHash -Algorithm SHA256 ...\ledger_schema.json
Hash : F4CDECE5098D4E915431F9FD916005BBC3D79EA5AF89A0535E3E21D668BDA90E
       (length 867)

> git cat-file -s HEAD:.../ledger_schema.json
867
```

Index LF, working tree LF, attribute applied, working file byte-identical to the
Git object. This worktree is correct.

### Does it hold for a fresh clone, and on Linux?

This is the load-bearing question and I did not want to answer it from
documentation. `git cat-file --filters` applies the same smudge/eol conversion
that checkout applies, without writing anything, so it answers "what would a
fresh checkout put on disk" read-only. Note this repository is configured
`core.autocrlf=true` — the worst case for this bug.

```text
git object (blob, no filters):
  bytes   = 867
  sha256  = f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e

checkout sim, repo config (core.autocrlf=true):
  bytes   = 867
  sha256  = f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
  CRLF    = 0
  bare_LF = 36

checkout sim, forced core.autocrlf=true:
  bytes   = 867   sha256 = f4cdece5…   CRLF = 0

checkout sim, forced core.eol=crlf:
  bytes   = 867   sha256 = f4cdece5…   CRLF = 0

CONTROL - EVIDENCE_LEDGER.jsonl (no eol pin):
  blob bytes     = 708  sha256=873c35adade696eed29f0c56549b0ff51f0a3ad2ec38f827a0bba6c4bcb52652
  checkout bytes = 709  sha256=de6ddaa1658640b4b7f3c5483fc9dcd810a520d166bb58396708fda2c22213c8
  checkout CRLF  = 1
```

The pinned file checks out as LF with the matching hash even when
`core.autocrlf=true` and even when `core.eol=crlf` is forced — `eol=lf` wins.
The unpinned control file checks out CRLF (708 → 709 bytes), which proves the
ambiguity is real, still live for unpinned paths, and genuinely defeated by the
pin. `.gitattributes` is committed, so any fresh clone gets the rule.

**Conclusion: A1 holds for a fresh clone on Windows, holds on Linux (where
`* text=auto` already yielded LF, which is why this test passed there), and
holds in this worktree.** The mechanism is sound.

The one real limitation is stale checkouts — see NIT-1.

### Is the narrow scope right? (check 2)

Yes. I checked rather than assumed:

- `EVIDENCE_LEDGER.jsonl` contains **exactly one row**, and its
  `publishable_artifact_path` is
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`. That
  is the only artifact the ledger byte-hashes, so the single pinned path is
  100 % of current coverage.
- In `validate_ledger.py`, raw-byte hashing (`_sha256_file`) runs only under
  `verify_artifact=True`. In `test_linux_deployment.py:407` that flag is set
  **only** for the canonical ledger; the three row fixtures are validated
  without artifact hashing, so they cannot fail this way.
- I swept the rest of the suite for the same pattern. `test_release_evidence.py`
  and `test_runtime_baseline.py` compute hashes at runtime and compare them to
  themselves (self-consistent), and the `sha256` hits in
  `test_linux_deployment.py` are string assertions about script text. **No other
  recorded-hash-versus-working-tree site exists.**

The narrow rule is the correct scope today. The generic exposure — any *future*
ledger row pointing at a text artifact reintroduces the same ambiguity — is a
standing-rule matter already raised in the Pathscope identity-table finding, not
a defect in this repair.

## A2 — does the repaired assertion still have teeth? (check 3)

I did not take the implementer's proof on trust, and reproducing it mattered:
**the implementer's published proof never executes the test under audit.** It
re-implements the comparison inline (`assert mutated_schema_version ==
source_schema_version`) in a standalone script. That demonstrates the logic, not
the test.

So I drove the real test. I wrapped `wal.main` so that after a successful
`create` the produced manifest's `invariants.schema_version` is rewritten to
`"999"`, then ran
`IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history`
itself. Every bundle the test builds lives under pytest's `tmp_path`; nothing in
the repository was modified.

First attempt was invalid and I discarded it: my instrumentation printed to
stdout, which `create()` parses as JSON, so the test went RED with a
`JSONDecodeError` — red for the wrong reason. Removing the print gave the honest
result:

```text
STEP 1 - mutated manifest, real test must go RED
>       assert inv["schema_version"] == source_schema_row[0]
E       AssertionError: assert '999' == '4'
E         - 4
E         + 999
IBKR_PAPER_BRIDGE\tests\test_wal_state_bundle.py:328: AssertionError
1 failed in 0.67s
RED_EXIT_CODE=1
MUTATED_MANIFESTS=1

STEP 2 - mutation removed, real test must go GREEN
1 passed in 0.14s
GREEN_EXIT_CODE=0

RESULT=DISCRIMINATING (wrong recorded schema_version is detected)
```

RED lands on the intended line 328 with the intended message, and GREEN returns
after the mutation is removed. **The assertion is not vacuous.**

### Is it tautological?

Partly, and the distinction is worth stating precisely. The test reads
`meta.schema_version` from the same source database the product reads, so it
proves *transport fidelity* — the bundle faithfully records what it captured —
and would catch a hardcoded value, a wrong key, a mangled value, or an omission.
It would **not** catch the baseline itself being wrong, because a wrong baseline
moves both sides together and the test stays GREEN. The original literal `"2"`
did pin an absolute expectation.

That loss is acceptable, but only because absolute coverage survives elsewhere,
which I verified: `IBKR_PAPER_BRIDGE/tests/test_order_identity.py:1567`
(`test_fresh_v3_initialization`) asserts `store.get_meta("schema_version") ==
"4"` after a default `initialize()` — the same fixture pattern `source_db` uses.
So the suite as a whole still fails if the baseline drifts. The repair creates
no coverage hole. The report does not mention this dependency — see NIT-3.

I also confirmed the implementer's reasoning against history. Commit
`ebb750da` repaired the identical two anomalies, using
`str(SCHEMA_VERSION_BASELINE)` for A2 — the option this implementer explicitly
rejects as tautological. Both commits start from the same blob `edc02108`. That
commit is **not an ancestor of HEAD** (`git merge-base --is-ancestor` → rc 1),
so this is a genuine recurrence from a divergent lane, not a regression
introduced here.

## Suite runs (check 4)

Run from repository root, twice, both after the repair, both recorded verbatim:

```text
> python -X utf8 -m pytest IBKR_PAPER_BRIDGE/tests -q -p no:cacheprovider

run A: 1021 passed, 1 warning in 75.35s (0:01:15)
run B: 1021 passed, 1 warning in 97.15s (0:01:37)
```

Both exit 0. The single warning in both runs is the installed-dependency
`StarletteDeprecationWarning` from `fastapi/testclient.py` about `httpx`,
exactly as the report and Packet 10 describe. **`1021 passed` twice reproduces
the implementer's claim.**

Two further background runs of the same command earlier in this audit also
exited 0, so the result held four times.

The two repaired tests also pass in isolation:

```text
> python -X utf8 -m pytest .../test_wal_state_bundle.py::test_invariants_preserve_risk_and_history -q -p no:cacheprovider
1 passed in 0.55s

> python -X utf8 -m pytest .../test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate -q -p no:cacheprovider
1 passed in 0.73s
```

**Command deviation, disclosed:** the kickoff specifies `PYTHONUTF8=1`. This
session's command policy refused the environment-variable form, so I used
`python -X utf8`, which is the documented exact equivalent (PEP 540) and sets
the same UTF-8 mode. Everything else — repository-root CWD, `-q`,
`-p no:cacheprovider` — matches the mandated command.

## Environment limitation

```text
Python 3.14.2
pytest 9.0.2
IBKR_PAPER_BRIDGE/requirements.lock: pytest==9.1.1
```

I verified this myself. The local interpreter is Python 3.14.2 with pytest
9.0.2 while the lock pins `pytest==9.1.1`, so **every result in this audit is
provisional against the frozen environment**. The suite must be re-run at the
release SHA under the locked pytest on the intended interpreter before deploy
checklist item 9 can be accepted. The report states this limitation plainly and
does not overclaim, which is correct.

## Report honesty (check 6)

Every reproducible claim I tested reproduced. Specifically verified as accurate:
the starting-state proof, the changed-file set, both byte/SHA-256 forms in the
A1 root-cause table, the attribute and `ls-files --eol` output, the A1 diff, the
A2 diff, the `1021 passed` post-change results, the warning identity, the
version limitation, and the existence and content of the `ebb750da` rule. The
report's refusal to accept its own work and its explicit "provisional" framing
are appropriate.

Four accuracy nits follow. None is a fabrication and none changes the verdict.

## Findings

### NIT-1 — stale checkouts are not covered, and remediation is not documented

`.gitattributes` only takes effect when a file is written to the working tree.
The blob for `ledger_schema.json` is identical in `678d4be2` and `6c746b65`, so
a pre-existing clone that merely fetches this commit will **not** have that file
rewritten and will keep its CRLF working copy — and A1 will recur there. This
affects any already-checked-out Windows copy (for example `C:\P10BASE`, or a
developer machine), though not the Linux deploy target, which clones fresh and
was never affected.

The report does state the principle — "attributes do not retroactively rewrite
an existing checkout" — and records that it refreshed the file here, which is
why I am not raising this as REQUIRED. What is missing is the instruction for
everyone else.

Suggested addition: *"Existing checkouts must run
`git checkout -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`
(or `git add --renormalize .`) once after taking this commit; a plain fetch will
not fix a stale CRLF working copy."*

### NIT-2 — the published A2 proof does not execute the test under audit

The proof in the report builds a bundle, mutates a manifest, and then asserts
with a hand-written copy of the comparison. It never invokes
`test_invariants_preserve_risk_and_history`. It therefore demonstrates that the
comparison logic is sound, not that the repaired test is discriminating — those
are different claims, and the section heading claims the latter.

The conclusion is correct: I proved discriminating power on the real test above.
But this is precisely the "prose outran its evidence" pattern this project has
been bitten by repeatedly, and the proof should be replaced with one that runs
the real test. Recommend adopting the wrap-`wal.main` method used in this audit.

### NIT-3 — the A2 rationale overstates option 3 and omits its dependency

The report says option 3 "tests the real contract" while rejecting option 2 as
tautological. Option 3 still reads the expected value from the same database the
product reads, so it cannot detect a wrong baseline. It is the right choice, but
the honest justification is that absolute baseline coverage lives elsewhere in
the suite (`test_order_identity.py:1567`). Recommend one sentence naming that
test, so a future editor does not delete it without realising this test depends
on it.

### NIT-4 — "independently validated" is unverifiable, and the ancestry phrasing is loose

The claim that the rule "was previously used and independently validated in
commit `ebb750da`" is half-verifiable: the identical rule is genuinely in that
commit, which I confirmed. "Independently validated" cites no audit artifact and
I could not verify it. Separately, "before it was absent from the present base"
understates the situation — `ebb750da` is not an ancestor of HEAD at all, so the
rule was never in this lineage. Recommend stating that plainly.

## What I could not verify

1. **The pre-change baseline `2 failed, 1019 passed`** at commit `678d4be2`.
   Reproducing it requires checking out the base, which this audit forbids. It
   is consistent with my measured 1021 total (1019 + 2) and with Packet 10's
   independent measurement of the same two failures — but Packet 10 measured at
   a different commit (`ddc8a9c8`), so this is corroboration, not confirmation.
2. **`git check-attr` output.** The session's command policy refused that
   command. `git ls-files --eol` reports the same attribute state
   (`attr/text eol=lf`) and I relied on it instead.
3. **Behaviour under the frozen environment** (`pytest==9.1.1`). Not installed;
   all results are provisional.
4. **Any Linux execution.** Not performed — out of scope and excluded. The Linux
   conclusion above is derived from checkout-filter simulation and from the
   documented prior behaviour, not from a run on Linux.
5. **The implementer's focused-run output `2 passed in 0.83s`.** I ran the two
   tests in separate invocations (both passed) rather than as one command, so I
   confirmed the outcome but not that exact line.
6. **That the schema file was refreshed by the exact means described.** No
   transcript exists for it. The end state is verifiably correct regardless.
7. **The `ebb750da` "independently validated" claim** (NIT-4).

## Bottom line

Both anomalies are genuinely repaired. A1's mechanism is verified to survive a
fresh checkout under the worst-case Windows configuration and is correctly
scoped to the only artifact that needs it. A2 is verified discriminating against
the real test, and the suite is green at `1021 passed` across four runs. The
defects I found are all in how the report describes its evidence, not in the
code. **PASS-WITH-NITS**, provisional against the frozen environment.
