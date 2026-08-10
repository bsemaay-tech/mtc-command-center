# RP7-WPI-RO repair round 4 - report

Implementer: Claude Opus 5, xhigh, fresh session, 2026-08-10. Owner-authorized
in-session past the recorded T0 cap after the second-flagship Codex xhigh audit
(`RP7_CODEX_T0_AUDIT_2026-08-10.md`) returned **BLOCK on 5**, one of them a
security-relevant false-PASS hole. Standing-authority §1 escalation resolved to
CONTINUE by explicit owner grant.

No host contact, no network, no SSH/SCP, no RUNID, no commit. Local Git Bash
execution only.

## Byte identity

| | bytes | SHA-256 |
|---|---:|---|
| baseline (round 3, audited) | 58012 | `1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e` |
| repaired (round 4) | 70941 | `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad` |

The baseline was verified against the kickoff hash **before** the first edit, and
independently against `git show HEAD:...` (the same 58012 B / `1d118d15…`), from
which the round-3 function bodies were extracted verbatim for the RED arms.
`bash -n` returns 0 at the repaired bytes. Every file written this round is
UNIX LF; no CR byte exists in any of them.

## Files touched

`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, this report, and narrow
edits to `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`. Nothing else.
`RP6-P0.sh`, `SELF_QA_RP6.md` and the transport tree were not written; they are
under concurrent edit by other sessions.

## The five findings

### F1 (BLOCK) - venv `site` startup executes unbound code before both adjudicators

**Closed.** `-I` is not `-S`. The block was using the venv it judges as the
interpreter for two *accepting* adjudicators, so one executable `import` line in
that venv's `site-packages/*.pth`, or a `sitecustomize.py` beside it, ran with
this block's authority before the intended child body.

- **(a) status parser** now runs `"$WPI_PYTHON3" -I -S -c '<parser>'`. It needs
  no venv context: it opens one file and parses JSON with the standard library.
- **(b) lock parity** now runs `"$WPI_PYTHON3" -I -S -c '<driver>' <site>
  <verifier> <lock>`. The driver refuses unless `sys.flags.isolated` and
  `sys.flags.no_site` are set and no `site`/`sitecustomize`/`usercustomize`
  module is loaded; scans the venv's `site-packages` **itself** as an explicit
  bounded path; replaces `importlib.metadata.distributions`,
  `Distribution.discover` and `PathFinder.find_distributions` with exactly that
  enumerated list; and only then compiles and runs the digest-bound
  `verify_lock.py` source under `__main__`. The venv directory is never placed
  on `sys.path`, so no venv module is importable and no venv startup
  configuration is read. `verify_lock.py` is unmodified and its rc, stdout and
  stderr grammar are unchanged, so rows 19/19a keep their preregistered forms.
- The status parser carries the same startup guard, emitting
  `PARSE startup_not_isolated` (parser rc 3) rather than a result.
- **New bound tool.** `python3` is the tenth `WPI_TOOL_PINS` entry, bound with
  the same kind/mode/owner discipline as the other nine, disclosed as
  `attestation=bound_instrument`, and added to the mount projection as the
  twenty-first point path.

**Falsified, executed.** Two real `python -m venv` environments. One carries
`zzforge.pth`, one carries `sitecustomize.py`; each writes a marker file and
prints the exact accepted result line, then `os._exit(0)`.

| arm | round-3 bytes | round-4 bytes |
|---|---|---|
| `.pth` vs status parser, deviant body | `B5_status … flags=expected`, rc 0, marker present | `B5_FAIL reason=flag_mismatch field=state`, rc 1, marker absent |
| `sitecustomize.py` vs parity, deviant universe | `B1_lock_parity result=pass`, rc 0, marker present | `B1_FAIL reason=lock_installed_parity`, rc 1, marker absent |
| same-interpreter control (only `-S` differs) | - | rc 1, marker absent, in both |
| production bytes with ` -S` deleted | - | rc 3, `trusted_startup_unproven` / `parser_rc=3` |
| clean universe control | - | `B1_lock_parity result=pass packages=2 … adjudicator=pinned_system_interpreter`, rc 0 |
| symlinked `python3` pin | - | rc 3, `tool_not_evaluable tool=python3 … kind=symlink` |

The parity arms drive the **real** candidate `verify_lock.py`: the fence
LF-normalises the worktree copy and asserts 3735 bytes /
`d951e0ee…a451e5`, which is exactly `WPI_VERIFY_LOCK_SHA256`.

### F2 (HIGH) - row 22 could FAIL before the complete table was parsed

**Closed.** `wpi_assert_listener_set` is now two-phase. Phase 1 reads to clean
EOF recording only sanitised counters and flags (`total`, `port_rows`,
`wildcard_seen`/`wildcard_addr`, `unexpected_seen`, loopback `count`); a
grammar, read or termination failure is still an immediate STOP, because that is
an inability to evaluate. Phase 2 emits the inventory line and only then applies
the wildcard, unexpected-address and count FAILs, in that unchanged precedence.

**Falsified, executed.** The auditor's two records in both orders. Both files
contain a malformed record, so neither order is evaluable:

```text
LISTENER_ORDER red_wildcard_first_rc=1 red_malformed_first_rc=3 green_wildcard_first_rc=3 green_malformed_first_rc=3 expected_both_stop=3
```

Positive controls prove the fix did not convert every FAIL into a STOP: a
**complete** table containing a wildcard still FAILs rc 1, a complete correct
table still PASSes rc 0, and in both cases
`B6_listener_inventory … parse=complete_before_semantics` precedes the verdict.

### F3 (HIGH) - the preflight omitted metadata formats its verifier consumes

**Closed, by the second route the finding offers** (make the trusted verifier
reject every non-preregistered format/location), composed with the first
(enumerate the whole universe). There is now ONE explicit discovery universe,
enforced twice:

- the preflight enumeration drops `-name '*.dist-info'` and classifies every
  direct child; the only admissible object is a `*.dist-info` **directory** with
  `METADATA` and `RECORD`;
- `*.egg-info`, `*.egg-link`, `*.egg`, `*.zip`, `*.whl`, `sitecustomize.py`,
  `usercustomize.py` and a non-directory `*.dist-info` are
  `B1_STOP reason=metadata_universe_unexpected stage=preflight … format=<f>`;
- the trusted driver re-derives the same universe from its own `os.listdir`
  scan and STOPs on the same set as `stage=verifier`, with the entry name
  content-suppressed to `name_sha256=<h>`;
- because `sys.path` never names the venv under `-I -S` and
  `PathFinder.find_distributions` is neutralised, the zip and extension-finder
  routes are structurally unreachable rather than merely unlisted.

**Falsified, executed.** The auditor's own fixture - a `ghost.egg-info` beside
two `*.dist-info` directories - runs both bodies. The round-3 body returns rc 0
and prints `dist_info_dirs=2 complete=yes readable=yes`, declaring complete
readability of a universe it never enumerated; the round-4 body returns rc 3
with `format=egg_info`. The requested readable / unreadable / malformed /
unexpected-egg-info cases are all present, plus `pth`, `startup_hook`, `zip`,
`dist_info_kind_regular`, and the driver-side `stage=verifier` pair.

### F4 (MEDIUM) - the semantic B5/B6 order was inverted beyond the authorised preflight

**Closed.** `wpi_main` now calls `wpi_assert_netns_binding`,
`wpi_assert_status`, `wpi_assert_listener_set`. Only the preregistered row-22
preflight inversion survives.

**Falsified, executed.** The QA does not re-declare the GREEN order; it
**extracts** it from the frozen `wpi_main` body at run time, so the arm cannot
pass if the block's call order is wrong. A two-deviation host state (HTTP 500
*and* a `10.0.0.5:8790` listener) is driven through both orders:

```text
red_first_result=[B6_FAIL reason=listener_set_unexpected observed=non_preregistered_address expected=1x127.0.0.1:8790]
green_first_result=[B5_FAIL reason=status_endpoint_unexpected_http code=500]
```

### F5 (LOW) - residual row/result grammar

**Closed, all four items.**

1. `wpi_lstat` takes the caller's row-specific unreadable reason (3rd argument),
   and `wpi_walk_components` threads it through the root check, every component
   and the leaf (10th argument). Rows 17, 19 and 19a now emit
   `installed_lock_unreadable`, `metadata_unreadable` and `verifier_unreadable`.
2. A bound **leaf** with deviant numeric ownership emits the row's own
   `installed_lock_owner_unexpected` / `verifier_owner_unexpected` (11th
   argument, derived from the row label). Deviant **intermediate** components
   keep `path_metadata_mismatch`, and rows 17/19a now preregister that form
   explicitly, so every form the walk can emit is a form the row records.
3. `installed_lock_object_unexpected` drops the extra `path=` via the new
   `kind_only` field style (12th argument); row 19a keeps `path=<p> kind=<k>` as
   its table records.
4. The two remaining raw `%F` sites (`dist_info_kind_$WPI_META_KIND`,
   `kind_$WPI_META_KIND`) are routed through `wpi_kind_token`.

**Falsified, executed** against a stat that really errors (`Permission denied`,
real nonzero exit) and against a multi-word object kind, five RED/GREEN pairs
plus the two `%F` pairs. RED is the round-3 call contract.

## Draft edits (narrow)

The kickoff scopes draft edits to "the §8.2 rows the fixes name". Four of the
five findings also name a binding paragraph as a location, and F1's new pinned
tool makes the §4 projection enumeration factually wrong if left alone. The
edits are therefore:

- **§4** - the point-path list becomes the **ten** tool pins and **twenty-one**
  records; a new paragraph preregisters `WPI_TRUSTED_PYTHON` as a freeze-gate
  input and states why it is not `<venv>/bin/python` and why the resolved
  `/usr/bin/python3.<minor>` must be pinned.
- **§8.2 rows 17, 19, 19a, 21, 22** - the new and corrected result forms above.
- **Instrument-attestation disclosure** - "the other five" becomes six, with
  `python3` named.
- **Metadata-readability adjudication rule** - the one explicit discovery
  universe, and why "every object the verifier consumes" is not a synonym for
  "every `*.dist-info` directory".
- **Probe execution-environment rule** - `-I -S` rather than `-I`, and the rule
  that no process may adjudicate its own state.
- **General probe-output precedence** - the precedence extends past the tool's
  status to the whole table.
- **Namespace-binding paragraph** - the row-22 preflight is the **only**
  authorised departure from display order; the executed order after it is
  `netns -> 20-21 -> 22-23`.

Nothing outside those surfaces was touched. Row 23, row 24, rows 10-16, 18 and
20 are unchanged.

## Self-QA

`SELF_QA_RP7.md` carries the exact fence, its complete real transcript, and a
per-finding coverage interpretation. Every round-3 arm is retained and still
holds. Per the kickoff, the published fence was **re-extracted** from the
markdown and **re-run**: the extraction is byte-identical to the file that ran,
and the re-run ended `QA_PASS all_assertions=yes` at exit status 0.

Substitutions are disclosed in full in the QA fixture table. The one new
substitution this round is `forge_capture`, which replaces the MSYS
`env -i`/`timeout` exec plumbing (it rewrites POSIX-looking argv for a native
Windows child) and normalises the Windows CRLF terminator. It honours the
interpreter and the flag words the production or mutant body chose, so nothing
about interpreter selection - the subject of finding 1 - is simulated.

## Freeze-gate inputs (two, unchanged in kind)

1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` - `<PIN-AT-FREEZE>`. The v2
   digest now covers 21 point paths.
2. `WPI_FIXED_TRUSTED_PYTHON` - `<PIN-AT-FREEZE>`, new this round.

Both must come from the deploy channel. Until they do, `wpi_validate_inputs`
necessarily STOPs and no end-to-end RP7 PASS can or should exist.

## What this round does not establish

No staging execution, no real bind or overlay mount, no `shellcheck` result (not
installed), and no accepting `wpi_validate_inputs` arm. The `.pth` and
`sitecustomize` behaviour was executed on local CPython 3.14.2; the relevant
semantics are documented for the target Python 3.12 in the primary sources the
audit cites, and the block's own runtime guard (`sys.flags.isolated` and
`sys.flags.no_site`) makes the requirement self-checking on the target rather
than assumed.

Acceptance belongs to a fresh independent cross-model re-audit.
