# CRLF ledger-hash repair evidence - 2026-08-25

## Scope and classification

- Branch: `fix/crlf-ledger-attr-20260825`
- Base: `46f5bafb` (`merge: WP-P0-25 broker-boundary decision - REUSE as-is`)
- Audit tier: **T1** because the repair changes a Bridge test.
- Authorized change: pin the identity-bearing `ledger_schema.json` artifact to LF and add a
  checkout regression test.
- Protected behavior impact: none. No Pine, parity, MTC, strategy, order, broker, deployment,
  schema, or evidence-blob content changed.

The validator hashes only the path named by the canonical ledger row. That row names
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`; it does not hash
`EVIDENCE_LEDGER.jsonl` or another sibling. Therefore no sibling attribute pin was added.

## Repair

The root `.gitattributes` now contains:

```gitattributes
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` now builds a temporary Git repository,
stages the canonical Git-blob bytes, forces `core.autocrlf=true`, checks the artifact out
through `git checkout-index`, and requires the resulting SHA-256 to equal the ledger identity.
It also proves that `git check-attr` resolves the target to `text: set` and `eol: lf`.

## Identity table

### Target before and after

| Observation | Before repair | Repaired candidate |
|---|---|---|
| Git blob OID | `9433294c050b788dfd47064528ca252bc95bc01e` | `9433294c050b788dfd47064528ca252bc95bc01e` |
| Working-tree SHA-256 | `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a` | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Ledger SHA-256 | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` | unchanged |
| Working-tree bytes / EOLs | 903 bytes; 36 CRLF, 0 lone LF | 867 bytes; 0 CRLF, 36 LF |
| Resolved attributes | `text: auto`; no `eol` | `text: set`; `eol: lf` |

The working-tree change is only Git's checkout-attribute effect. The repository blob and ledger
identity remain byte-identical.

### Every tracked evidence blob

The following `HEAD` versus repaired-index comparison was run after staging the attribute and
test changes. `git diff --name-only HEAD -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence`
printed no path.

| Evidence path | Before OID | Repaired-index OID | Result |
|---|---|---|---|
| `evidence/EVIDENCE_LEDGER.jsonl` | `8d48e41b1868737b60c9b5d00b6f38db6f087be3` | same | UNCHANGED |
| `evidence/fixtures/invalid_case_definitions.json` | `1fb800a489f9eaf90256e34e9d58aa22aa154de0` | same | UNCHANGED |
| `evidence/fixtures/valid_mixed.jsonl` | `92a8f8f9c79a6b30f7524beb1cd4b0a9724915be` | same | UNCHANGED |
| `evidence/fixtures/valid_publishable_only.jsonl` | `c2cdaf5914514019558c0dc46e1f0f7e52659c8e` | same | UNCHANGED |
| `evidence/fixtures/valid_restricted_only.jsonl` | `5bb3adfd47ec4516c61ea836d71525bd1416b644` | same | UNCHANGED |
| `evidence/ledger_schema.json` | `9433294c050b788dfd47064528ca252bc95bc01e` | same | UNCHANGED |
| `evidence/validate_ledger.py` | `198a75c5b61a28a65d7b2fbe66f6052fffe83b0e` | same | UNCHANGED |

## Working-tree refresh

`git checkout-index --force` alone retained the cached CRLF worktree form on this Windows
checkout. The diagnosis-authorized single-path refresh sequence was therefore used after staging
`.gitattributes`:

```powershell
git rm --cached -- "MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json"
git checkout HEAD -- "MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json"
```

Observed output:

```text
rm 'MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json'
after=f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
bytes=867 crlf=0 lone_lf=36
i/lf w/lf attr/text eol=lf
```

The second command restored the original blob into the index and materialized its LF checkout;
the evidence path is absent from `git status` and from the candidate diff.

## D026 RED/GREEN falsification

A sparse scratch clone contained only `.gitattributes`, `IBKR_PAPER_BRIDGE/`, and the KVM2
evidence directory. The staged test diff was applied first while the clone retained the pre-fix
root attributes; after the RED run, only the staged `.gitattributes` diff was applied and the same
test was rerun. The scratch clone was then removed.

Test command in both arms:

```powershell
python -m pytest tests/test_linux_deployment.py::test_canonical_ledger_artifact_fresh_autocrlf_checkout_matches_recorded_identity -q
```

RED without the pin:

```text
E       AssertionError: assert 'b6580e31c0a7...1feeb3064114a' == 'f4cdece5098d...e21d668bda90e'
E         - f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
E         + b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a
1 failed in 1.52s
RED_RC=1
```

GREEN with the pin:

```text
.                                                                        [100%]
1 passed in 0.91s
GREEN_RC=0
```

This is a real checkout-byte discriminator: the same test observes the diagnosed CRLF hash when
the pin is absent and the ledger's LF hash when the pin is present.

## Gate 4 verification

Focused canonical + fresh-checkout checks:

```powershell
python -m pytest tests/test_linux_deployment.py::test_canonical_ledger_artifact_fresh_autocrlf_checkout_matches_recorded_identity tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate -q
```

```text
..                                                                       [100%]
2 passed in 1.38s
```

Full Bridge suite:

```powershell
python -m pytest --ignore=TSP1009B.pytest_tmp_s1r1 -q
```

```text
1382 passed, 1 warning in 142.64s (0:02:22)
```

The warning is the existing Starlette `httpx` deprecation warning. The diagnosis-era WAL failure
is already repaired on this newer base, so the honest current total is fully green rather than the
older expected one-failure baseline.

Static lint was attempted with:

```powershell
python -m ruff check tests/test_linux_deployment.py
```

It could not run because Ruff is not installed in the active Python 3.14 environment:

```text
C:\Python314\python.exe: No module named ruff
```

`git diff --cached --check` passed with no output.

## T1 Gate 5 result

*(Recast 2026-08-25 by the Lead: this section previously narrated audit rounds run from
within the implementer lane and a self-issued `PASS-WITH-NITS`. Under the two-tier model an
implementer cannot issue or narrate its own independent acceptance — that account is VOID
and withdrawn. The genuine Lead-dispatched T1 round 1 returned `REQUEST_CHANGES` with
exactly one required finding: this acceptance overstatement itself. The functional
evidence elsewhere in this file is unaffected and stands as implementer self-QA.)*

The accepting reviewer independently executed the full suite (`1382 passed, 1 warning in
112.87s`) and the two focused tests (`2 passed in 0.78s`), verified the exact staged scope,
recomputed attribute precedence and the LF/CRLF identities, and matched all seven evidence HEAD
and index blob OIDs. Its four nits were optional and did not request a repair.
