# RUNID minting review — Codex, 2026-08-11

## Verdict

**NEEDS WORK before Stage 1 mints anything.** A concretely generated compact identifier of
the apparent intended form is accepted by the real predicate, and the seven advertised
refusal values are specific inputs rather than adjectives. The design is nevertheless not
ready to mint because `<UTCSTAMP>` has no exact grammar or length, the literal template is
itself refused, the finite examples are called “the refusal set”, duplicated values are not
mechanically proven equal at every consumer, the Windows runner creates a RUNID-derived
record root without applying the component predicate, and the design has no durable global
allocation/burn ledger.

No host or network contact was made. The checks in this review sourced only the pinned local
library and called the string predicate.

## 1. Authoritative predicate identity

The draft wrappers do not accept an arbitrary function with this name. Both pin
`RP0_LIB_SHA` to the same full digest, hash
`$EXTRACT_DIR/RP0-LIB.sh`, and only then source it (`run_p0.sh:27,89,96` and
`run_ro.sh:21,96,103`). The skeleton independently records the same byte count and abbreviated
digest. The source read for this review is the carried-forward runkit member matching that
binding:

| Field | Value |
|---|---|
| Path read | `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\01_RUNKIT\RP0-LIB.sh` |
| Bytes | `18968` |
| SHA-256 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` |

`07_RUNKIT_B/RP0-LIB.sh` is a second byte-identical repository copy (same 18,968 bytes and
same SHA-256); it was not used as an unproved substitute. At execution, the authoritative
object is the extracted runkit member whose bytes must match the digest above.

The predicate at `RP0-LIB.sh:85-94` is:

```bash
rp0_require_safe_component() {
    local name="$1" val="$2"
    case "$val" in
        ""|"."|"..")       rp0_fail "component_reserved name=$name value=[$val]";     return 1 ;;
        -*)                rp0_fail "component_leading_dash name=$name value=[$val]"; return 1 ;;
        *[!A-Za-z0-9._-]*) rp0_fail "component_charset name=$name value=[$val]";      return 1 ;;
    esac
    rp0_note "component_ok name=$name value=$val"
    return 0
}
```

Both wrappers set `LC_ALL=C` before sourcing the library. In that actual composition, the
accepted language is therefore:

```text
one or more ASCII characters from [A-Za-z0-9._-],
with the first character not '-',
and with the complete value not equal to '.' or '..'.
```

Equivalently, it is `^[A-Za-z0-9._][A-Za-z0-9._-]*$` minus the two complete strings `.`
and `..`. Leading dots are otherwise allowed (`.a` and `...` pass); trailing or embedded
hyphens pass. There is **no length check**.

Exact consequences:

| Input class | Result and code arm |
|---|---|
| Empty | Refused, `component_reserved`, rc 1. |
| Leading `-` | Refused even if every later byte is otherwise allowed, `component_leading_dash`, rc 1. |
| `.` / `..` | Each refused exactly, `component_reserved`, rc 1. Other leading-dot forms are accepted. |
| `/` or `\` | Refused as outside the allowlist, `component_charset`, rc 1. `/` is the relevant remote path separator; `\` is also refused. |
| Space or other whitespace | Refused as outside the allowlist, rc 1. |
| Representable control character | Refused as outside the allowlist, rc 1. A NUL cannot exist in a Bash variable or argv element, so it cannot reach this function as a character. |
| Non-ASCII | Refused in the wrappers' `LC_ALL=C` domain, rc 1. |
| Glob metacharacters such as `*`, `?`, `[` | Refused as outside the allowlist, rc 1. |
| Length | No predicate limit. A locally tested 4,096-byte string of `a` returned rc 0. Downstream `mkdir`/filesystem component limits can still STOP, so predicate acceptance alone does not establish allocatability. |

## 2. Proposed and implied identifier forms

The following table distinguishes the literal draft notation from concrete values. The
local checks used the exact pinned function above under `LC_ALL=C`.

| Form | Example or literal tested | Predicate verdict | Assessment |
|---|---|---:|---|
| Skeleton base template | `WPI-<UTCSTAMP>Z-<8hex>` | rc 1 | The literal placeholder is refused because `<` and `>` are outside the allowlist. This is expected before filling, but Stage 1 must never test the template and infer that the concrete value passed. |
| Intended compact base | `WPI-20260811T120000Z-deadbeef` | rc 0 | Accepted. This depends on choosing a compact digits-plus-`T` timestamp and an ASCII hex nonce. |
| P0 RUNID | `WPI-20260811T120000Z-deadbeef-P0` | rc 0 | Accepted. Appending `-P0` preserves the language. |
| RO RUNID | `WPI-20260811T120000Z-deadbeef-RO` | rc 0 | Accepted. Appending `-RO` preserves the language. |
| P0 stage ID | `p0` | rc 0 | Accepted. |
| RO stage ID | `ro` | rc 0 | Accepted. |
| Remote-base leaf | `wpi_staging_WPI-20260811T120000Z-deadbeef` | rc 0 | Accepted. `remote_setup_wpi.sh` actually strips `/home/gatea/wpi_staging_` and validates the base suffix, not this whole displayed leaf. |
| Operator-record leaf | `WPI_TRANSPORT_WPI-20260811T120000Z-deadbeef` | rc 0 | It would pass if tested, but `transport_runner.ps1` does not apply this predicate to it. |
| Confirmation token | `WPI-20260811T120000Z-deadbeef-EXECUTE` | rc 0 | Safe by derivation if the base is safe, but it is an interlock token rather than an evidence identifier and is not predicate-checked. |

The skeleton says only `<UTCSTAMP>`; it does not define the generator or grammar. A common
compact spelling such as `20260811T120000` happens to pass. An equally ordinary ISO-8601
spelling such as `2026-08-11T12:00:00` fails because of `:`. Therefore the proposed base is
**conditionally accepted and currently fragile**, not accepted by specification. The
`8hex` fragment is safe if Stage 1 really emits exactly eight ASCII hex digits, but that too
should be an executable grammar rather than prose.

There is also no length contract. The apparent compact form is comfortably short, but the
placeholder permits an arbitrarily long “timestamp”; the predicate would return 0 while the
Linux remote-base leaf or evidence-directory leaf could exceed the filesystem's component
limit and fail during allocation. Stage 1 must pin the exact widths or an explicit maximum.

## 3. Refusal demonstration

The skeleton's seven values are not adjectives. Each is a concrete shell value and each has
an expected rc 1:

| Skeleton value | Actual arm |
|---|---|
| `../escaped` | charset (`/`) |
| `a/b` | charset (`/`) |
| `.` | reserved |
| `..` | reserved |
| `-lead` | leading dash |
| empty (`''`) | reserved |
| `bad name` | charset (space) |

They are therefore executable representatives, but the skeleton has not supplied the
literal invocation/transcript yet. Empty input in particular must be passed as an explicit
empty second argument, not omitted. Also, seven samples do not demonstrate the complete
refusal set. The code defines that set; the run demonstrates named cases. The successor
should call these “refusal representatives” unless it performs an exhaustive byte-domain
test under the pinned shell and locale.

For the semantic claims required here, the minimal explicit matrix is:

| Refusal class | Exact shell input expression | Exact value | Expected result |
|---|---|---|---|
| empty | `''` | empty | rc 1, `component_reserved` |
| dot | `'.'` | `.` | rc 1, `component_reserved` |
| dot-dot | `'..'` | `..` | rc 1, `component_reserved` |
| leading dash | `'-lead'` | `-lead` | rc 1, `component_leading_dash` |
| POSIX separator | `'a/b'` | `a/b` | rc 1, `component_charset` |
| backslash | `'a\b'` | `a\b` | rc 1, `component_charset` |
| whitespace | `'bad name'` | `bad name` | rc 1, `component_charset` |
| control | `$'bad\x01name'` | includes byte `0x01` | rc 1, `component_charset` |
| non-ASCII | `$'caf\xC3\xA9'` in a UTF-8 shell | `café` bytes | rc 1, `component_charset` |
| glob metacharacter | `'bad*name'` | `bad*name` | rc 1, `component_charset` |

Run each as the second argument to the exact pinned function, capture stdout, stderr and rc,
and fail the self-QA unless the rc is exactly 1 and the reason token names the expected arm.
The same transcript must include rc 0 for the one concrete base, both derived RUNIDs, and
both stage IDs. This review executed those cases locally and observed the expected results.

## 4. Boundary trace

`<base>` below means the one concrete Stage-1 base, not the placeholder text.

| Boundary | Value/path | Validation or trust at this boundary | Does the gap matter? |
|---|---|---|---|
| Stage-1 mint | `<base>`, `<base>-P0`, `<base>-RO`, `p0`, `ro` | Skeleton requires calls to `rp0_require_safe_component`, but supplies no exact timestamp grammar, generator command, or completed transcript. | **Yes.** This is the only proposed validation before several local path consumers. Validate the concrete values from the exact pinned source and bind the transcript to them. |
| Stage-1 fan-out into files | The same base is copied into runner constants, both wrappers, many plan fields and derived paths. | No current per-consumer equality proof. Marker replacement and hashes prove bytes, not that every duplicate contains the same tested base. | **Yes.** A safe value can be tested while a different or malformed value is frozen in one consumer. Use a fill manifest and equality checks. |
| `transport_runner.ps1` constants | `$BASE_RUN`, `$CONFIRM_TOKEN`, `$RECORD_ROOT` (`transport_runner.ps1:66-76`) | `Assert-MarkerFree` only proves placeholder strings are absent (`:358-382`). It does not apply the RP0 component predicate. | **Yes.** In execute mode the runner checks existence and creates `$RECORD_ROOT` at `:390-409` before any remote validator runs. A bad fill can therefore select/create the wrong operator path. |
| Plan parse | RUNID-derived remote and local paths in `TRANSPORT_PLAN.tsv` ops 01-03 and 07-12 | Whole plan is SHA-pinned. Each argv token must match `^[A-Za-z0-9._@:/\\=-]+$` (`transport_runner.ps1:275-278,456-459`), a deliberately broader path/option grammar that permits separators, colon, backslash, equals and leading dash. | **Yes.** Plan integrity and `Test-SafeArg` are not component validation. They are adequate only if Stage 1 proves that the embedded base/runids equal the already accepted concrete values. |
| Remote op 01 | `/home/gatea/wpi_staging_<base>` passed to `remote_setup_wpi.sh` | Revalidated independently: exact prefix, then suffix rejects empty, `.`, `..`, leading dash and outside charset (`remote_setup_wpi.sh:103-119`); exact parent checked at `:317-320`. | This closes the remote-base component boundary before remote creation. It does not protect the earlier operator record-root creation. |
| Remote setup allocation | Remote base, `evidence`, `evidence/runkit`, `kit` | Base must be absent before non-recursive create-once allocation (`remote_setup_wpi.sh:325-336`). | Enforces one-use while the base survives. |
| Ops 02-03 | Archive and extraction paths below remote base | Trusted as frozen plan paths; extractor checks absolute paths, parent bindings, archive identity and member grammar, but does not re-run the RUNID predicate because no RUNID is passed. | Equality to the validated op-01 base matters. A mismatched but individually absolute plan path is not repaired by op 01's suffix check. |
| Wrapper constants | `BASE_RUN`, `REMOTE_BASE`, `EXTRACT_DIR`, `RUNID`, `EV_STAGE_ID`, `EV_PARENT`, `EV_RUNKIT` in `run_p0.sh:14-22` and `run_ro.sh:8-17` | Wrappers hash the sourced blocks but do not validate `BASE_RUN`, `REMOTE_BASE`, or `RUNID` before using `EXTRACT_DIR` to hash/source them. They pass no RUNID argv; the values are frozen literals inside stdin bytes. | Equality to the Stage-1 manifest matters. The first component validation occurs only after the library has been found through the filled extraction path. |
| `RP0-BOOTSTRAP.sh` | `RUNID`, `EV_STAGE_ID` | Revalidated with the authoritative predicate at `:18-19`; parent roots are independently canonical/owner/mode checked. | This is the first same-shell component check in each stage. |
| Bootstrap derivation | `EV_DIR=$EV_RUNKIT/$RUNID`; `EV_LOG=$EV_DIR/${EV_STAGE_ID}.log` | Each derived leaf is proved a direct child with `rp0_require_leaf_inside`; `EV_DIR` is create-once and `EV_LOG` is opened with noclobber. | Strong relative containment, provided the frozen `EV_RUNKIT` itself is the intended root. |
| `RP6-P0.sh` | `RUNID`, `EV_STAGE_ID`, `EV_DIR`, `EV_LOG` | Checks set/nonempty, re-runs the safe-component predicate on both identifiers (`:403-415`), then later binds stdout's object identity to `EV_LOG`. It does not require `EV_STAGE_ID == p0` and does not independently reconstruct `EV_DIR` from a frozen absolute root. | It trusts the same-shell bootstrap/frozen wrapper for stage identity and absolute-root provenance. This is material to the composite path proof; block-only analysis cannot close it. |
| `RP7-WPI-RO.sh` | Same four values | Re-runs both component checks, requires `EV_STAGE_ID == ro`, requires absolute `EV_DIR`, requires descent below the frozen evidence root, and requires `EV_LOG` below `EV_DIR` (`:688-712`). | Revalidation is stronger here, but still relies on the frozen root being correctly filled and equal to the wrapper/plan root. |
| Close ops 07-08 | `EV_DIR`, stage RUNID and `WORK_ROOT` passed as plan argv | Intended close script independently checks RUNID with the same three refusal arms and requires `basename(EV_DIR) == RUNID`. | ~~**Current composition does not reach that check:** plan rows 07/08 pass two arguments, while the current script requires three (`EV_DIR RUNID WORK_ROOT`). It exits FAIL on argc first.~~ **CORRECTED 2026-08-12 — this row was stale in TWO respects and both are now fixed.** (1) The argv mismatch no longer exists: plan rows 07/08 pass three arguments (`TRANSPORT_PLAN.tsv:8-9`) and the script requires exactly three (`remote_close_tree_wpi.sh:282-286`). (2) The failure mode was mis-stated: an argv-count violation returns **rc 3 STOP**, not rc 1 FAIL — an operator-side composition input is explicitly "an inability to evaluate, never a host finding" (`remote_close_tree_wpi.sh:282`). What actually blocks the close boundary today is different: `EXPECT_UID`/`EXPECT_GID` are still `<PIN-AT-FREEZE>`, so execution STOPs at `:288-291` *before* the RUNID/`EV_DIR` grammar checks at `:295-306`. Sources: `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md` §Blocker 8 (Codex gpt-5.5), independently confirmed and extended by `WPI_BLOCKS_DRAFT/TRANSPORT_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` (GLM-5.2), which caught the second staleness the ledger only half-flagged. |
| Retrieval ops 09-10 | Remote evidence leaf and local destination containing `<base>-P0/-RO` | Runner uses the frozen, hash-bound plan and broad argv grammar; it does not re-run the component predicate. | Equality to the close/stage RUNID matters. A successful scp transfer is transport evidence, not identifier validation. |
| Local bind ops 11-12 | `evidence\<base>-P0/-RO` | `Invoke-LocalBind` joins the frozen relative path to `$RECORD_ROOT`, derives `expectedRunId` from its leaf, and requires every parsed remote close record's runid to equal it (`transport_runner.ps1:811-822,745-805`). It does not apply the safe-component predicate to that leaf. | It detects disagreement between retained close output and local directory spelling, but trusts the plan/record-root path grammar and cannot compensate for a malformed fill created earlier. |

The important trust chain is therefore not “validated once everywhere.” Remote setup,
bootstrap, both blocks, and the intended close script do revalidate at different depths;
the Windows runner, wrapper pre-source paths, extraction paths, retrieval and local binding
trust frozen equality with an earlier Stage-1 validation. That trust is acceptable only if
Stage 1 mechanically proves the same concrete value reached every consumer. Today the
skeleton asks for testing and filling but does not specify that conservation proof.

This is the concrete continuation of prior gap 4: `RUNID`, `EV_STAGE_ID`, `EV_DIR` and
`EV_LOG` cannot be closed by a block-only analyzer because their safety is established by
the wrapper + pinned RP0-LIB + RP0-BOOTSTRAP + block composition. The current analyzer's
opaque/unpinned report is therefore honest; substituting a static safe-looking value is
diagnostic only, not freeze evidence.

## 5. One-use discipline

Three surviving objects currently act as reuse barriers:

1. `transport_runner.ps1` refuses execute mode if
   `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<base>` already exists, then creates it once.
2. `remote_setup_wpi.sh` requires `/home/gatea/wpi_staging_<base>` to be absent before
   creating it and its children.
3. Within that remote base, `RP0-BOOTSTRAP.sh` uses plain non-recursive `mkdir` for
   `evidence/runkit/<RUNID>`; a repeated P0 or RO stage RUNID STOPs and is marked burned.

The skeleton additionally says a failed allocation burns the RUNID and names collision
checks against two existing operator roots. These mechanisms prevent reuse only while the
relevant directory/record survives and while every consumer carries the same base. They do
not form a global, append-only allocation registry. Deleting or losing the operator and
remote roots makes the same spelling allocatable again; checking only two named historical
roots does not prove global novelty.

After the fact, reuse is detectable from evidence **only if evidence from both uses is
retained and compared**: the RUNID appears in wrapper headers, evidence paths, close records,
retrieved directory names and local bind records. A single evidence package can establish
its own spelling and internal consistency, but cannot prove there was no earlier deleted,
failed-before-evidence, or separately stored use. The committed successor history may expose
a duplicate if every allocation/burn is committed and history is searched, but the skeleton
does not define that search or an append-only ledger, so evidence-alone uniqueness is not
established.

## Stage 1 must change before minting

1. Define and execute an exact generator grammar and width, for example
   `UTCSTAMP := [0-9]{8}T[0-9]{6}` and nonce `:= [0-9a-f]{8}`, plus an explicit maximum
   component length. Do not rely on the prose word “UTCSTAMP”.
2. From the one generated base, derive—do not independently type—the two RUNIDs, stage IDs,
   remote suffix, confirmation token and operator record leaf. Run the exact pinned
   predicate on every path component before any consumer is written.
3. Add a per-consumer fill/equality manifest covering both wrappers, runner constants and
   every plan occurrence. Prove each frozen occurrence equals the one tested value before
   commit or execution. Because the runner creates `$RECORD_ROOT` before remote validation,
   either add equivalent local component validation (with the required re-audit) or make
   this pre-commit conservation proof an explicit hard gate.
4. Record literal commands plus stdout, stderr and rc for concrete acceptance and the
   refusal matrix above. Rename the finite claim to “refusal representatives”; do not call
   seven examples the complete refusal set.
5. Reconcile ops 07/08 with the current close script's required third `WORK_ROOT` argument;
   until then, the promised close-boundary RUNID revalidation is not executable.
6. Create a committed append-only allocation/burn ledger and check the candidate base and
   both stage RUNIDs against the complete ledger as well as all retained local/remote roots.
   Evidence retention alone is not a uniqueness proof.
