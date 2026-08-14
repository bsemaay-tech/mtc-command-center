# RP7 cap-override - Codex T0 flagship audit

Verdict: BLOCK

Auditor: fresh independent Codex `gpt-5.6-sol`, effort `xhigh`, T0.  Date:
2026-08-15.  Frozen subject:
`2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b`.

This is only the Codex flagship verdict. It is not a combined T0 acceptance and
does not adjudicate or fill the Claude slot. I did not read the Claude verdict
for this round.

## Blocking condition - mandatory suite could not execute

The exact published rows-1-9 command was attempted sequentially:

```text
wsl.exe -d Ubuntu -- bash -lc "cd /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT && sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p' SELF_QA_RP7.md | bash --noprofile --norc"
```

It returned `MANDATORY_FENCE_RC=-1` before the fence could start:

```text
Wsl/Service/WSL_E_DISTRO_NOT_FOUND
```

`wsl.exe --list --quiet` reports no installed distribution, and neither the
Windows host nor Git Bash exposes `systemd-analyze`. The fence itself requires
that real parser and must abort rather than skip it. Therefore I could not
produce a fresh 156-line transcript, execute the nine systemd oracle arms, or
establish absence of harness abort/capture collision/ERR-trap contamination in
an auditor run. Under the T0 execution rule, non-execution is BLOCK, not
supplemental acceptance.

## REQUIRED-1 - row-9 D026 fixture bypasses the production normalization boundary

The repair does reject the literal test string when that spelling is handed
directly to the embedded tokenizer. That is not the production input boundary:

- `wpi_assert_b4_rows_8_9` obtains `Environment` from bounded `systemctl show`
  output and passes that effective property value to the tokenizer
  (`RP7-WPI-RO.sh:917-946`).
- The repair's own comment states that systemd removes the mid-name quotes and
  stores the spliced name as the protected target (`RP7-WPI-RO.sh:806-815`).
- The fence does not reproduce that manager boundary. `write_b4_show` injects
  the original raw mid-name spelling directly into fake `systemctl` stdout
  (`SELF_QA_RP7.md:282-291`, `:630-655`).

I extracted the actual embedded row-9 parser source from the frozen Git objects
and ran each subject in a separate Python process. The directed results were:

```text
current  raw MTC_BRIDGE"_START_MODE=credential_free_disarmed"  rc=0 OK
repaired raw MTC_BRIDGE"_START_MODE=credential_free_disarmed"  rc=3 environment_token_name_not_literal
repaired normalized MTC_BRIDGE_START_MODE=credential_free_disarmed rc=0 OK
repaired fully quoted assignment                              rc=0 OK
repaired value-quoted assignment                              rc=0 OK
repaired same-value duplicate                                 rc=1 count=2
```

Thus the new test proves only that the tokenizer refuses a quote spelling if
that spelling survives into `systemctl show`. The package's own model says it
does not survive: it normalizes to the exact clean token the repaired parser
accepts. This is a production-fixture fidelity failure (Patterns 9/11), and the
kickoff requirement that the attack can no longer normalize into the protected
target is not established.

Required repair: bind row 9 to an observation that preserves the lexical unit
assignment, or explicitly revise the predicate and evidence contract. The D026
RED/GREEN must traverse the same normalization boundary as the real B4 caller;
directly injecting pre-normalization text into fake manager output is not
closure evidence.

## REQUIRED-2 - frozen evidence contradicts itself about the Lead run

The four frozen artifacts do not carry one coherent provenance state:

- `STATUS_RP7.md:6-9` and the report at `:7-10`, `:814-818` say the Lead ran the
  complete fence against `132886` bytes on 2026-08-15.
- `SELF_QA_RP7.md:10-11` says no independent Lead run exists, and
  `SELF_QA_RP7.md:1050-1053` repeats that claim.
- The report's current identity block still says
  `independent_lead_run=none_yet_against_these_bytes`
  (`RP7_ROWS_1_9_REPORT_2026-08-13.md:80-95`).

These are false, mutually exclusive provenance statements inside the frozen
acceptance package. Reconcile them from the actual Lead record before another
audit dispatch (Patterns 9/10).

## REQUIRED-3 - the kickoff's exact-transcript condition is not met by the package

The kickoff requires exact transcript reproduction. The package instead states
that, after replacing each random scratch root, only 155 of 156 lines match and
that `HARNESS_ATTESTED_MOUNTINFO sha256=` still differs
(`SELF_QA_RP7.md:990-1006`; report `:798-810`). Raw transcripts also necessarily
differ in every run-owned path. That is an explained source of variation, but it
is not exact reproduction under the dispatched contract.

Required repair: either make the published harness emit and verify a
deterministic canonical transcript while retaining run-owned scratch isolation,
or amend the audit contract explicitly to define the allowed normalization and
the exact fields excluded. An auditor may not silently weaken "exact".

## Partial checks completed - supplemental only

- Kickoff completeness: no unfilled `PENDING-FILL-AFTER-REPAIR` field remains.
- Frozen Git-object identities matched exactly:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 132886 | `a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243` |
| `SELF_QA_RP7.md` | 504144 | `72aab351fc9f0d5881bbac995985338dc983777978b1787b4b5abe3bf0fda58f` |
| `STATUS_RP7.md` | 12213 | `df44704c4099459d2860fd6ddbfc0b659b981eb4ecbe06a7f1ef89b99499ad65` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 41843 | `4e5d38d422ab836aca3e2421f0430b4cdb72680c5d34de86e33d14b2c0fd7cde` |

- The committed block and extracted fence both passed `bash --noprofile --norc
  -n` from Git object bytes. `git diff --check` over the four-file candidate
  delta was clean.
- Historical subject identities re-derived: round 4 = `127491` /
  `5b00207aff17a9a9f29e056b9f93fb46b2cf640376659bf75b9f33b9b9b3dbe3`;
  post-round-4 current = `127655` /
  `beacf85b628e419d911416dc1ee51a382f742d90cbabe29602e60c4f52d809a8`.
- Exact embedded row-6 parser source, run in separate local processes, showed
  the intended discrimination: CRLF continuation was rc 1 on `8ec89675` and rc
  0 on the repair; trailing-space-after-backslash remained rc 1; blank-line and
  even-backslash boundaries were rc 1; comment bridging remained rc 0. This is
  supplemental because the real systemd oracle could not execute.
- The embedded transcript has the declared documentary census: 156 lines,
  single-subject `36/36/9`, multi-subject `11/10/27`, nine ORACLE lines, and no
  pasted contamination marker. A pasted transcript is not a fresh auditor run.

## Repository delta

The repository was clean before this verdict write. No Git mutation, host or
network contact, deployment, credential access, service action, ARM/order,
TESTNET/mainnet, Pine, parity, or trading action occurred. The only
audit-attributable repository path is this Codex verdict file.

