# AUDIT KICKOFF — round 1 adversarial re-audit (Codex, T0)

You are the independent adversarial auditor for an authorized private-repo
test-infrastructure design repair. Your job is to REFUTE the round-1 deliverables, not
to confirm them. This is shell-script and design-document review only; nothing here
touches any host, credential, or service.

## Scope — read ONLY these files (all relative to this file's directory)

- `KICKOFF_B3_GAP_ENV_OPTION1.md` — the implementer's binding brief.
- `round1/RP1-B3.sh`, `round1/RPD-VERIFY.sh`, `round1/DESIGN_NOTES.md`,
  `round1/SELF_QA.md` — the deliverables under audit.
- `../01_RUNKIT/RP1-B3.sh` — the original accepted block (the repair baseline).
- `../01_RUNKIT/RP0-LIB.sh` — the predicate library both blocks source.
- `../03_TRANSPORT/B3_STOP_ADJUDICATION.md` — why the repair exists.

Do not read anything else in the repository. Do not modify any file outside the
`audit1/` directory next to this file. Do not execute anything against any remote host;
local `bash -n` or local fixture runs in a temp directory are allowed.

## Audit questions (answer all, in order)

1. **Spec compliance**: does `round1/RP1-B3.sh` implement the brief exactly — checks
   1-3 + ancillary modes preserved with no weakening, env/manifest checks fully removed
   from the unprivileged path, the EACCES boundary probe with the three-outcome
   discipline the brief demands? Diff old vs new yourself; list every behavioral delta
   and classify each as required-by-brief / justified-addition / unjustified.
2. **Soundness of the boundary probe**: can a host state exist where the probe PASSes
   but the accepted host state does not hold (false pass)? Consider: ACLs granting
   search to a third user, a symlinked /etc/mtc-bridge, a mount over it, capabilities
   (CAP_DAC_READ_SEARCH), the pair-of-names logic, stderr-classification fragility
   across coreutils versions and locales (LC_ALL discipline).
3. **RPD-VERIFY soundness**: as root, are the mode/owner/binding checks sufficient to
   support the admission claim that moved out of B3? Attack the grep-based binding
   (substring collisions, JSON escaping, duplicated keys in the manifest, the hex
   guards), the numeric-identity guards, and the rc contract.
4. **SELF_QA honesty**: pick at least 5 of the 43 QA arms and independently reproduce
   them from the delivered files (local temp fixtures). Report any arm whose claimed
   output you cannot reproduce.
5. **Open items O1-O7** in `round1/DESIGN_NOTES.md` §7: give a verdict on each
   (accept as-is / must change / indifferent), with one-sentence reasoning. The Lead
   flags two for special attention: O1 (ENOENT routed to STOP; the Lead's preliminary
   view is that ENOENT proves the directory was searchable, i.e. the host is MORE open
   than the accepted state, so FAIL is truer) and O2 (rc divergence between the two
   blocks for a missing preregistered input).

## Output

Write exactly one file: `audit1/AUDIT1_REPORT.md`. Structure: verdict first — one of
PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK — then findings ranked most severe
first, each with: the exact file+line, the failure scenario (concrete input/state that
makes it wrong), and the minimal fix. Answer the five questions in order after the
findings. English, ASCII only. A finding without a concrete failure scenario is a nit,
not a finding — label it accordingly.
