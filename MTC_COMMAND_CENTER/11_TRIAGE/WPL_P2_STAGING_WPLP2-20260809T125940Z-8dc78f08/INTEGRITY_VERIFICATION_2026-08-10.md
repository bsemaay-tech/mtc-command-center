# Integrity verification — the night's evidence chain, re-checked after the fact

Performed by the Lead on 2026-08-10, after all execution was complete, as a check on the
claims this unit makes rather than a restatement of them. Read-only: no host contact, no
file modified except this record and the one line noted below.

## Why bother

Every transport record in this unit asserts that its evidence was "closed, retrieved and
bound". Those assertions were produced by the same runner that performed the transfer. A
claim checked only by the thing that made it is worth little, so each binding was
recomputed here from the preserved bytes and compared against what the **host** independently
computed at close time.

## Result: all three evidence logs verify

| Run | Recomputed locally now | Host `CLOSE_DIGEST` at close time | Bytes | Match |
|---|---|---|---:|---|
| B3 (original, STOP) | `079d6ac9f345b10ec333768203887ae52de9d6be89f0c5c4031a68353c4424a1` | identical | 1784 | yes |
| R4-5 (`-R45B`, PASS) | `00078e7ea5caeca69a2468226c3fb1ec180153b74000151243335586363c4e0d` | identical | 4521 | yes |
| B3 repaired (`-B3B`, PASS) | `7b383ab5194972fca9511ae7068509929fab652c980953864ae93aa3ae60fa16` | identical | 3329 | yes |

The host-side values were read from the `CLOSE_DIGEST` lines in each run's own
`operator_record/ops/*.stdout`, which the remote close-tree script emitted on stdout before
anything was retrieved. Local and remote agree for every run, so the retrieved bytes are the
bytes the host hashed.

## Repository state

`repo_guard.ps1` returns **PASS**. The branch is in sync with its upstream — nothing
committed tonight is unpushed. The working tree carries exactly four untracked entries:
the three evidence-log directories, which the repository's own ignore rules exclude by
convention, and one pre-existing scratch file at the repository root that predates this
work and was not touched.

That the logs are gitignored is precisely why this verification matters: the committed
records are the only in-repository statement of what those logs contain, so their digests
must be checkable against something the repository does not control. The host's own
close-time output is that something.

## One record-keeping gap found and fixed

`09_TRANSPORT_B3B/STAGE3B_B3B_RECORD.md` cited the digest *set* (`d572afe7…`) but never
stated `b3b.log`'s individual digest, unlike the equivalent records for the other two runs.
An auditor would have had to re-derive it. The digest and byte count are now stated inline
in that record, with a pointer here.

## What this does not prove

The digests bind the retrieved bytes to what the host computed. They say nothing about
whether the *content* of those logs is a correct account of the host's state — that
question is answered by the checks themselves and by the audits over their designs, not by
hashing. Nor does any of this extend to the three checks B3 defers to `RPD-VERIFY`, which
has never executed.
