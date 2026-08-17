# Section 10.2 composite-input design

Date: 2026-08-10  
Scope: design analysis only; no block, wrapper, prover, draft, fixture, host, or Git action

## Binding requirement

Section 10.2 currently requires, verbatim:

> Stage 1 must emit, per frozen block, the sorted set of every host path that can reach a
> filesystem or network primitive after constant and variable expansion, and must show
> every entry inside section 10.1. A literal-string scan is supplemental only: it misses
> concatenated variables, command substitutions, arrays, sourced values and dynamically
> constructed prefixes. The accepted proof therefore parses the complete shell input,
> rejects unresolved/dynamic path construction, proves every path-bearing argument is
> derived only from preregistered constants, expands those constants, and checks the
> resulting closed set against section 10.1. It also falsifies a forbidden path assembled
> from separately harmless tokens and must reject it. The proof is recorded in the Stage
> 1 record with the exact command and real RED/GREEN output, and the archive is not frozen
> until it passes. This is a static check over frozen bytes, so it cannot be satisfied by
> a run-time guard and cannot be skipped by a run-time branch.

The unit of analysis cannot be `RP6-P0.sh` or `RP7-WPI-RO.sh` alone. The unit is the
stage entrypoint plus every source unit and executable source unit reachable from it,
with the dispatch allocation and freeze-time bindings applied. A proof over fewer bytes
is a lower-bound diagnostic, not the section 10.2 proof.

There is also a necessary semantic boundary. A static source proof can enumerate
source-controlled path operands, redirections, endpoints, and closed derived families. It
cannot enumerate undocumented internal opens performed by Bash, the dynamic loader, libc,
systemd clients, Python, or other pinned binaries. Recursive walks and the installed
distribution scan likewise select concrete descendants from runtime host state. Therefore
the current phrase "every host path" is satisfiable only if section 10.2 explicitly means:

1. every filesystem or network operand produced by the frozen wrapper, reachable sourced
   shell, inline program, and executed source file; and
2. every runtime-selected operand proved to remain in a named, allowlisted closed family.

If it instead means every concrete file internally opened by every executable, or requires
the exact runtime descendant list rather than a closed family, the present static gate is
unsatisfiable and Stage 1 must STOP. It must not silently adopt the narrower meaning.

## Measured composite inventory

All byte counts and SHA-256 values below were measured from the current working tree except
the verifier, which was measured from the exact candidate Git object. The current Windows
worktree rendering of `verify_lock.py` is not the executed candidate byte stream and must
not substitute for it.

| Role | Exact local identity | Bytes | SHA-256 |
|---|---|---:|---|
| P0 entrypoint | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh` | 5215 | `e4ddf87b0869ba0fadcb9750e65f4f276c90667e788e489c5921923b0d3e1f80` |
| RO entrypoint | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh` | 5933 | `cd659ee9e1edceb496a5ed08707abd283e3cf5f70a3872ab6f1fdc616ac3f4e8` |
| Shared library | `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP0-LIB.sh` | 18968 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` |
| Shared bootstrap | `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP0-BOOTSTRAP.sh` | 1937 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` |
| P0 block | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh` | 103071 | `fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd` |
| RO block | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` | 77179 | `393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee` |
| RO executed verifier source | Git object `2ce41e34bceb599d80af24c5c33d835820ec321b:IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` (blob `8ccd6f329154422a85b8e7663e6a079dbd47b4fd`) | 3735 | `d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5` |

The two RP0 files were located at the exact `07_RUNKIT_B` paths above. Their measured
identities match both wrapper pins and the preregistration table. They are not present as
same-named files in `WPI_BLOCKS_DRAFT`; substituting a similarly named or reconstructed
copy would change the composite.

### P0 load and value flow

| Order | Component | Mechanism and path contribution |
|---:|---|---|
| 0 | Remote Bash launch | The transport executes `bash -s --` and sends `run_p0.sh` on stdin. The launch environment and any Bash startup source are pre-input dependencies; they must be closed as described below. |
| 1 | `run_p0.sh` | Executed as the shell input. It contains the dispatch allocation, derives `EXTRACT_DIR`, hashes three extracted files, and therefore contributes the paths of `RP0-LIB.sh`, `RP0-BOOTSTRAP.sh`, and `RP6-P0.sh`. |
| 2 | `RP0-LIB.sh` | Sourced in the same shell after its remote bytes pass the wrapper hash gate. Sourcing defines functions. Only functions reachable from the bootstrap or block belong to the reachable sink graph; unused definitions are not executions. |
| 3 | Evidence inputs | The wrapper exports `RUNID`, `EV_STAGE_ID`, `EV_PARENT`, `EV_RUNKIT`, and their owner/mode fields. These exports are the interface into the bootstrap. |
| 4 | `RP0-BOOTSTRAP.sh` | Sourced in the same shell. It calls RP0-LIB functions, derives `EV_DIR` and `EV_LOG`, creates the evidence directory and log, and redirects the shell's stdout/stderr to that log. |
| 5 | P0 inputs | The wrapper exports the P0 identity, venv-root, and tool-pin inputs. |
| 6 | `RP6-P0.sh` | Sourced in the same shell. Its path operands are composed from its literals, the wrapper exports, the bootstrap's `EV_DIR`/`EV_LOG`, and the complete tool-pin table. |

### RO load and value flow

| Order | Component | Mechanism and path contribution |
|---:|---|---|
| 0-4 | Remote Bash through `RP0-BOOTSTRAP.sh` | Same mechanisms as P0, using `run_ro.sh`, `RUNID=...-RO`, and `EV_STAGE_ID=ro`. |
| 5 | RO inputs | The wrapper exports release, venv, unit, state, log, config, endpoint, PID, interpreter, mount-projection, verifier, and tool-pin inputs. |
| 6 | `RP7-WPI-RO.sh` | Sourced in the same shell. It derives evidence leaves, candidate descendants, procfs operands, the loopback endpoint, and runtime-bounded descendant families. Its two inline Python `-c` programs are part of these frozen bytes and must be parsed as executable nested source, not treated as opaque argv. |
| 7 | Candidate `verify_lock.py` | Its path is passed as argv to the pinned trusted Python. The inline driver opens the file, reads its bytes, compiles it with that path as filename, sets `sys.argv`, and executes it as `__main__`. Its source therefore can affect later path use and is part of the RO composite, even though it is not shell-sourced. |

`requirements.lock`, distribution `METADATA`/`RECORD`, mountinfo, and the HTTP response are
data subjects, not additional source components. They still appear as path operands or
closed runtime families. The external executable objects and Python standard library are
trusted-runtime dependencies, not analyzable shell input; their internal opens are outside
the bounded static claim and must be named as such.

## Where the unresolved values become determinate

| Value | Classification | Point of determination | Static consequence |
|---|---|---|---|
| `RUNID` | Dispatch-time allocation, materialized into the Stage-1 wrapper | The Lead allocates the one-use safe component before the wrapper is frozen. P0 and RO receive distinct `-P0` and `-RO` values. | Not genuinely runtime. After allocation it is a literal input and `EV_DIR`/`EV_LOG` can be reduced. A placeholder is an unconditional Stage-1 STOP. |
| `EV_STAGE_ID` | Frozen constant | `p0` in `run_p0.sh`; `ro` in `run_ro.sh`. | Fully static before dispatch. Its safe-component check is validation, not the source of the value. |
| `REMOTE_BASE` | Dispatch-time allocation, with an ordering constraint | The create-once base is allocated before the wrappers and the RO evidence-root pin are frozen. | Not genuinely runtime. The allocation token must be replaced everywhere by one byte-identical literal before analysis. |
| `EV_DIR` | Runtime assignment with a dispatch-determinate lexical value | RP0-BOOTSTRAP assigns `EV_RUNKIT/RUNID` after validating the components and existing parents. | The filesystem object's existence is runtime, but the lexical path is statically reducible after allocation. Treating it as an arbitrary runtime variable is wrong; defaulting it is equally wrong. |
| `EV_LOG` | Runtime assignment with a dispatch-determinate lexical value | RP0-BOOTSTRAP assigns `EV_DIR/EV_STAGE_ID.log`. | Same distinction as `EV_DIR`: runtime object, statically closed path expression. |
| `P0_TOOL_PINS` | Stage-1 freeze fill | A finite twelve-entry table must be supplied from deploy-channel pins and agree one-for-one with RP6's `P0_FIXED_*` constants. | The path strings must be exact at freeze. Runtime PATH fallback is forbidden. Current round 7 has moved RP6 in this direction by requiring all twelve entries and comparing every entry with a frozen literal. |
| `WPI_TOOL_PINS` | Stage-1 freeze fill | A finite ten-entry table is filled in `run_ro.sh`; RP7 requires and binds all ten. | The path strings are static after freeze. The trusted Python leaf is also tied to `WPI_FIXED_TRUSTED_PYTHON`. |
| Bootstrap helper executables | **Genuinely runtime in the current design** | Reachable RP0-LIB functions call bare `mktemp`, `stat`, `tr`, `rm`, `readlink`, and `mkdir` before RP6/RP7's pin gates. Their resolution comes from the inherited shell environment. | The current composite is not closed. Later P0/RO pin tables cannot retroactively prove which programs the bootstrap already executed. |
| Recursive/distribution descendants | Genuinely runtime, but capable of family confinement | `find` results and venv distribution entries depend on host contents. | A static proof can prove only a closed root/family unless Stage 1 also freezes an exact member manifest and the block enforces conservation against it. It cannot invent a concrete descendant set. |

## Options

| Option | Cost | Residual risk | Assessment |
|---|---|---|---|
| Raw textual concatenation | Low initial implementation cost. | It can change shell semantics around stdin, `source`, `exit`, scope, and `$BASH_SOURCE`; it also misses the separately executed verifier and launch/startup inputs. | Reject as a literal byte-concatenation design. |
| Whole-program analysis from the wrapper entrypoint, resolving includes and nested executed source | Moderate. It needs a frozen component manifest, a source/load graph, cross-file environment/function propagation, nested-source parsing, and fail-closed command grammars. | Parser unsoundness remains the dominant risk; the current prover's four CRITICAL silent-sink classes show that deterministic output does not establish coverage. Runtime descendants still require family semantics. | **Recommend**, with the closures below and a fresh T1 audit of the repaired analyzer. |
| Per-component proofs composed through handwritten interface contracts | Moderate at first and attractive for reuse. | An asserted but unchecked contract can omit a function sink, export, overwrite, or executed member. Patterns 11-13 apply directly; conservation can fail while every local proof passes. | Do not use handwritten contracts as acceptance evidence. Machine-derived summaries may be an internal optimization only when checked against both producer and consumer bytes. |
| Blocks declare their reachable set and the prover checks the declaration | Low declaration cost, high completeness-proof cost. | The declaration is the claim, not proof. Without independent whole-program coverage it is circular and can silently omit the same sink as the code. | Useful output schema and review aid only. |
| Narrow section 10.2 to exact literals only and accept the rest as a limitation | Low. | It would no longer satisfy the quoted requirement and would hide the wrapper/bootstrap and runtime-family risks. | Reject. A narrowly clarified source-visible/family semantic is necessary, but every excluded layer must be named and the gate must STOP when a family cannot be proved closed. |

### Single recommendation

Build one **entrypoint-driven whole-program composite proof per stage**, not one proof per
file and not a raw concatenation. Stage 1 should generate a frozen manifest containing the
ordered component identities above, all allocated/fill values, the exact source edges, and
the bounded proof semantics. The analyzer starts at `run_p0.sh` or `run_ro.sh`, follows
only hash-bound source/exec edges, propagates assignments and exports across those edges,
parses inline and file-backed executed source, and emits:

1. the sorted exact source-derived operands;
2. the sorted closed runtime families with the derivation and access class for each;
3. the external-runtime boundary; and
4. a coverage/conservation record proving every reachable component, command, option,
   redirection, nested source unit, and path-bearing value received exactly one terminal
   disposition.

Any unknown command grammar, unconsumed option, unbound source edge, unresolved value,
unclosed runtime family, component hash mismatch, or startup source outside the manifest is
rc 3 and prevents freeze. The current prover cannot perform this role until its nine audit
findings are repaired with RED/GREEN evidence and a fresh T1 review accepts it.

## Changes required before the composite is analysable

1. **Allocate, render, then freeze.** Allocate `REMOTE_BASE` and both one-use RUNIDs first;
   render them into both wrappers and into RP7's frozen evidence-root constant; fill all
   block hashes and tool pins; then hash and analyze the final bytes. Analysis of angle-
   bracket placeholders is a STOP, not a diagnostic value to default.
2. **Close the Bash-entry boundary.** The remote interpreter identity, argv, environment,
   working directory, shell options, and startup-file behavior must be fixed. In particular,
   an inherited `BASH_ENV`, imported function, alias, or PATH-dependent startup source must
   not be able to add executable text before `run_p0.sh`/`run_ro.sh`. A first-line `unset`
   is too late if Bash has already sourced the file. The transport must either establish a
   startup-free pinned interpreter domain or section 10.2 must STOP at this boundary.
3. **Replace or harden the reachable RP0 bootstrap helpers.** The accepted RP0-LIB is not
   path-neutral when RP0-BOOTSTRAP calls it: `rp0_probe_path` uses `mktemp`, `stat`, `tr`, and
   `rm`; other reachable functions use bare `readlink` and `mkdir`. This creates a temporary
   path outside the evidence tree under the default environment and executes PATH-resolved
   tools before either block's pin validation. Prefer a new frozen WP-I bootstrap helper
   with temp-free probes and absolute, pre-bound tools. Do not widen section 10.1 to `/tmp`.
4. **Remove wrapper `/dev/null` opens.** Both wrappers redirect tool and source stdin/stderr
   through `/dev/null`. The complete-input proof will see those opens even though the
   block-only reconciliation did not. Use closed descriptors or create-once evidence leaves
   inside the frozen evidence root, with explicit read/write classification.
5. **Bind bootstrap tools before use.** The finite RP6 and RP7 pin tables occur after the
   bootstrap. The wrapper/bootstrap boundary needs its own exact tool inventory and binding,
   including every reachable helper, with declared = bound = executed conservation.
6. **Bind RP6's venv root exactly.** The current RP6 check accepts any absolute path whose
   basename is the candidate SHA. It must require exactly
   `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b` before the first
   probe. The existing section 10.1 venv rule must not be widened to arbitrary prefixes.
7. **Finish `/dev/null` removal in RP6.** RP7 round 5 already replaced its prerequisite
   redirections with non-overridable `builtin type -t` checks and closed the noclobber
   diagnostic fd. Current RP6 still uses `2>/dev/null` on its two prerequisite type checks;
   those writes remain outside the allowlist and must be removed without weakening the
   function-type predicate.
8. **Keep the finite pin-table direction.** RP6 round 7 now requires twelve tool pins and
   compares them with twelve frozen literals; RP7 requires and binds ten. Preserve this
   one-to-one rule and derive the analyzed executable inventory from the real top-level call
   graph. A table that is complete only by assertion is not evidence.
9. **Keep and extend the round-5 evidence-root direction.** RP7 now refuses an unfilled
   `WPI_FIXED_EVIDENCE_ROOT` and requires `EV_DIR` below it before allocating capture leaves.
   The wrapper/bootstrap proof must establish the same root derivation for both stages, not
   merely rely on the later RP7 runtime guard.
10. **Account for executed Python source and runtime families.** Include the exact candidate
    `verify_lock.py` blob and both inline Python bodies in the RO source graph. Either define
    closed descendant-family semantics for the release walk and distribution universe, or
    freeze exact manifests and make the blocks enforce one terminal disposition per member.

## What would make the proof worthless

- Omitting the wrapper, RP0-LIB, RP0-BOOTSTRAP, the selected block, an inline program, or
  `verify_lock.py` from the composite.
- Treating a hash check as proof of a component whose hash placeholder was not filled, or
  analyzing local bytes different from the candidate bytes executed remotely.
- Letting Bash startup text, imported functions, aliases, inherited PATH, cwd, or TMPDIR add
  a component or path outside the manifest.
- Asserting an interface contract without mechanically checking both its producer and
  consumer, including every export, assignment, function call, overwrite, and source edge.
- Defaulting `RUNID`, `REMOTE_BASE`, `EV_DIR`, `EV_LOG`, a tool path, PID, or pin during
  analysis. A missing value is rc 3; a diagnostic substitution is not proof.
- Reporting only literals while ignoring concatenation, arrays, redirections, command
  substitutions, `find -exec`, option-valued paths, traps, nested interpreters, or implicit
  endpoints. The current prover audit demonstrates that zero reported facts plus PASS can
  be a silent coverage failure.
- Calling lexical normalization a host-object proof. Intermediate symlinks and mount
  crossings require the separate runtime binding predicates; the static result must say
  lexical/family scope.
- Calling an unenumerated runtime descendant an exact path, or accepting a family without
  proving that every selected member remains inside it.
- Counting generic parser issues as unresolved paths, or allowing a member to disappear
  between enumeration, normalization, and terminal disposition.
- Accepting a declared reachable-set table as its own completeness proof.
- Publishing RED/GREEN prose, edited templates, or commands that cannot be pasted and
  rerun against the exact frozen identities.

## Honest Stage-1 claim under the recommendation

After the launch boundary, bootstrap helper surface, fixed values, source graph, and
runtime-family semantics are closed, Stage 1 can honestly claim that, for each exact frozen
stage composite, it completely enumerated every **source-controlled lexical filesystem and
network operand** plus every **closed runtime-derived operand family**, that each has an
access class and an allowlist disposition under section 10.1, and that no modeled or opaque
sink disappeared without a terminal rc-3 coverage record. That claim must be backed by the
frozen manifest, exact command, full output, and RED/GREEN falsifications.

Stage 1 cannot claim the concrete runtime member list of a recursive walk before the host
state exists; the identity behind a lexical path across unchecked symlink/mount changes;
or the undocumented internal opens and side effects of Bash, the loader, libraries, and
pinned external binaries. It also cannot claim anything for the present composites while
the startup environment, bootstrap PATH tools/tempfile, wrapper `/dev/null` opens, RP6 venv
prefix, or any freeze placeholder remains unresolved. Under any of those conditions, the
truthful section 10.2 result is STOP and the archive is not frozen.
