# Transport round-4 Codex audit — Band B (F1 residual only)

Date: 2026-08-11  
Frozen commit: `99f33c33f5fc5e3c8fbaa6141849c7cd6a435280`  
Tier: **T0**  
Applied auditor contract: fresh Codex `gpt-5.6-sol`, xhigh, read-only judgement. This
file is the Codex Band-B slot only; it does not adjudicate F2/F3/F4/T5-T8 or stand in
for the other T0 flagship slot.

## Verdict

**REQUEST_CHANGES**

F1 is **not closed on the composition**. The frozen bytes do enforce a clean, exact
environment for the inner `/usr/bin/bash` child *if `/usr/bin/env` is reached*. They do
not control the earlier server/account shell through which SSH executes the remote
command string. The report itself discloses that shell as outside every attestation.
A server-supplied startup environment can therefore act before `/usr/bin/env -i` runs;
the claimed residual remains reachable and the closure depends on remote good
behaviour.

## Method and holds

I read the report, `SELF_QA_TRANSPORT.md` §R4-4, and the frozen blobs for
`run_p0.sh`, `run_ro.sh`, `transport_runner.ps1`, and `TRANSPORT_PLAN.tsv` directly
from commit `99f33c33`. I constructed and ran no plant, started no process from the
transport set, opened no connection, contacted no host, used no network, and performed
no Git mutation. This is the requested text-and-bytes judgement.

Frozen Git blob identities used:

| File | Git blob |
|---|---|
| `run_p0.sh` | `70272a36fe83ac040ce5dd84df8f18668256542b` |
| `run_ro.sh` | `36d7f000436f29081f6af71ab6e3ae4cd755039e` |
| `transport_runner.ps1` | `26d7993fe4171c937c2ff65cd76535e7098aaddd` |
| `TRANSPORT_PLAN.tsv` | `0e5aeaf2d248de50c8558805486c439655b87d78` |

## Answers to the three required checks

| Check | Judgement |
|---|---|
| Frozen inner launch bytes | **PASS, narrowly.** The plan and runner enforce the intended inner-child domain. |
| Honesty of “closed on the composition” | **FAIL.** The disclosed residual is reachable before that domain starts. |
| Client-side boundary | **FAIL.** Closure requires an unbound server/account-shell and startup-environment property. |

### 1. What the frozen bytes do establish

`transport_runner.ps1:173-180` freezes the route and the ten-element launch suffix:

`/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash --noprofile --norc -s --`

`transport_runner.ps1:584-601` requires the route and every launch-domain element at
the exact positions after the pinned SSH options. `TRANSPORT_PLAN.tsv:2,4-6,8-9`
carries that suffix on all six `ssh_stdin` rows. `transport_runner.ps1:772-816` then
starts the pinned local `ssh.exe`, passes the plan argv, and writes the frozen script
bytes to SSH stdin.

Accordingly, **if `/usr/bin/env` executes**, its `-i` child environment is explicit and
complete for the wrapper contract: exactly `PATH`, `LC_ALL`, and `HOME`. It contains
none of `ENV`, `BASH_ENV`, `SHELLOPTS`, or `PROMPT_COMMAND`. The inner
`/usr/bin/bash` cannot receive any of those variables *through that `env -i`
invocation*. The exact-three-entry sweeps in `run_p0.sh:64-86` and
`run_ro.sh:58-80` consistently attest that narrower fact after the inner interpreter
has started.

### 2. Why the residual is still reachable

The runner does not directly execute remote `/usr/bin/env`. It executes local
`ssh.exe` (`transport_runner.ps1:772-816`) and supplies a remote **command string**.
The report expressly acknowledges at `TRANSPORT_R4_REPORT_2026-08-11.md:380-383`
that the server/account shell used by `sshd` to run that string is outside every
attestation. That shell necessarily exists *before* the first token of the command
string — `/usr/bin/env` — can execute.

If the server supplies `BASH_ENV` to a Bash account shell, Bash processes that startup
file before executing its `-c` command string. An exiting startup file can therefore
emit the expected operation-family record and return rc 0 without ever reaching
`/usr/bin/env -i` or the stdin-delivered wrapper. The same boundary issue applies to
whatever startup controls the unbound account shell actually honors; omitting
`ENV`, `BASH_ENV`, `SHELLOPTS`, and `PROMPT_COMMAND` from the later child does not erase
them from the already-started outer shell.

The runner cannot distinguish that output from the intended program. Its provenance
test at `transport_runner.ps1:1028-1045` accepts a capture when any line begins with a
prefix registered for the stdin leaf, and `transport_runner.ps1:1075-1093` accepts an
in-grammar rc plus that prefix. Those checks bind marker *shape* to a plan row, not the
process that produced it. The report already grants that an exiting startup file can
forge the record; moving that startup file one interpreter earlier leaves the same
accepted rc/marker path.

The self-QA does not close this boundary. Its `F1 GREEN` drives `/usr/bin/env -i ...
/usr/bin/bash` directly, while §R4-4 says the transport round opened no SSH connection.
It proves the inner-child sanitisation, not that the server/account shell cannot execute
startup code before the frozen command string.

### 3. Why the status wording is an overclaim

`TRANSPORT_R4_REPORT_2026-08-11.md:90-100` and
`SELF_QA_TRANSPORT.md:2185-2199` say the exiting-plant case is unreachable because no
plan row can introduce `BASH_ENV`. That statement addresses only variables written into
the command's `env -i` assignment list. A plan row need not introduce the server's
environment, and the runner has no predicate over it.

The report then says both that the login shell is outside every attestation and that it
“cannot select or influence what runs” (`TRANSPORT_R4_REPORT_2026-08-11.md:380-383`).
Those statements do not compose: startup code that runs before `/usr/bin/env` can prevent
the frozen child from running at all and can produce the record in its place. The
disclosure is useful, but it is not a control. This is the exact “sentence outruns the
probe” failure: the bytes establish an inner-child guarantee, while the status claims an
end-to-end transport guarantee.

## Minimum required repair

1. Mark F1 **OPEN** (or “inner child closed; outer SSH account-shell boundary open”) and
   remove every claim that the residual is unreachable or that F1 is closed on the
   composition. Align the report, self-QA status table/§R4-4, runner comments, wrapper
   comments, and any mirrored status text.
2. To claim closure later, bind an enforcement point that acts before the account shell's
   startup processing — for example, an independently frozen and attested server-side
   execution contract that prevents startup-variable/file processing, or a transport
   path that directly executes the pinned helper without an unbound shell. A command
   *inside the same shell string* cannot establish this.
3. Supply D026 evidence at that actual boundary: RED with the pre-control behaviour and
   GREEN with the control, driven through the real top-level transport path (or an
   equivalent faithful SSH-server falsification). A direct local `env -i` invocation is
   supplemental only for this named residual.

No optional nits are recorded. The finding and verdict are scoped to F1 only.
