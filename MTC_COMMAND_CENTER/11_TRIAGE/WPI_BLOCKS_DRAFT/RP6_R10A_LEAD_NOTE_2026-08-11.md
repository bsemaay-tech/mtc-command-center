# RP6-P0 round 10a — Claude Pro died on its WEEKLY limit mid-round; partial preserved

## What happened

Round 10 was dispatched to Claude Pro at ~10:50. It hit the **weekly** Claude Pro limit
(resets 2026-08-12 23:00 Europe/Chisinau) partway through and stopped. It left `RP6-P0.sh`
and two other files **modified with no report, no round-10 QA section, and the four findings
not confirmed closed**.

This is the "agents crash mid-write" trap, this time from a hard weekly cap rather than a
5-hour window.

## State of the partial

- `RP6-P0.sh` → `a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`, 107252 B,
  zero CR bytes, `bash -n` rc 0.
- Diff vs round-9b: `+73` block lines, `+994` SELF_QA lines, `+176` draft lines.
- **No `RP6_REPAIR_R10_REPORT.md`.**

## What the Lead verified

The whole existing fence set still passes on the partial bytes: `R9_GRAMMAR` 5/5,
`RP6_R4_D026` PASS, `RP6_FULLBLOCK_D026` PASS, `R7_F2`/`R7_F3`/`R7_C3` all PASS, `C13_R4B`
27/27. So the partial did not break anything that was green.

**But that is not evidence round 10 is done.** The four round-9 findings were:
F1 the published `R9_GRAMMAR` command not running the harness; F2 grammar closure; F3
malformed followed-target reaching rc 1; F4 the unreachable relabelled line. None of these
is confirmed closed by the existing fences — they would need the new round-10 arms the report
was supposed to introduce, and there is no report. The green set only proves no regression.

## Disposition

Committed as **round 10a, explicitly not round 10**, to protect the work from loss under the
same reasoning as round 9a: the bytes are syntactically valid, cause no regression, and
reverting would discard real work. But round 10 is **not closed**. A resumed round 10b must:

1. Confirm F1's actual fix — the published command now runs the harness — by running that
   published command **verbatim** and showing the summary line appears.
2. Confirm F2/F3/F4 with new RED/GREEN arms.
3. Write `RP6_REPAIR_R10_REPORT.md`.
4. Re-run every published command verbatim, per the corrected Lead QA practice.

Until then RP6-P0 stays at `REQUEST_CHANGES` from the round-9 review, not re-submitted.

## Routing consequence

Claude Pro is out for ~1.5 days (weekly cap). The two remaining implementer routes are GLM
(returns 13:50) and Codex — but Codex is auditor of record for RP6 and cannot implement its
repairs. So **round 10b waits for GLM at 13:50**, unless the owner authorises Claude Max as
an implementer for this one round.
