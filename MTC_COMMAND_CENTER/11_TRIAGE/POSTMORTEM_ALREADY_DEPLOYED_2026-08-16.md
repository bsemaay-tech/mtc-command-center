# Post-mortem — "why did nobody know the bridge was already deployed?"

Written 2026-08-16 by the Fable 5 Lead, at the owner's request, after
`GATEA_STAGING_OBSERVATION_2026-08-16.md`. It includes a correction to the
Lead's own report to the owner earlier that morning.

## Correction first

The Lead told Barış that the planning documents and the freshly published
dashboard were "wrong" to say the hardened Ubuntu install had never been
performed and that the first disarmed start had not happened.

**That overstated the case.** Those rows describe the **KVM2 / Hostinger VPS**,
which is the actual deployment target. On KVM2 they are accurate: nothing is
installed there and nothing has started. What the Lead observed was
**GATEA-STAGING**, a different machine at an earlier stage. Both of these are
true simultaneously:

- the hardened Ubuntu deployment has been performed and ran for 2 d 13 h — on
  GATEA-STAGING;
- the hardened Ubuntu deployment has never been performed — on KVM2.

The observation was real and valuable. The conclusion drawn from it conflated
two hosts. Rule adopted: `two-hosts-never-conflate`.

## Did the memory system fail?

**Largely, no — on the central fact it worked.** `plan50h-doc-cycle` records,
under "GATE A COMPLETE (2026-08-09)": A-0 through A-9 **ALL PASS** for accepted
candidate `2ce41e34…` at commit `5af8178b`, staging left "DISARMED,
credential-free, single loopback listener `127.0.0.1:8790`", and explicitly
"**staging Gate-A acceptance only** — no master merge, promotion, credential
load, ARM, TESTNET/mainnet authorized."

That is the deployment, correctly recorded, including its limits. The Lead read
that memory at session start.

**Four narrower failures are real:**

1. **The Lead did not connect the memory to the dashboard rows.** The gate
   table was inherited from the previous dashboard and republished without
   re-deriving any row against memory or against the machine. An inherited
   status row is an unverified claim.
2. **Nothing recorded that GATEA-STAGING is a local Hyper-V VM.** Every
   document treats it as a remote host requiring an administrator. That is the
   one genuine record gap, and it cost the most: an entire blocker class
   ("eight facts only an administrator can supply") was built on it.
3. **Nothing recorded the run window or that the install was left intact.**
   Memory captured the Gate-A verdict, not that the service subsequently ran
   2026-08-09 → 2026-08-11 and remains installed. Verdicts were recorded;
   living state was not.
4. **A 26-day-old memory still carried a "🟢 OPEN + ARMED" header** describing
   the retired July Windows-hosted era. Corrected with a stale-header banner.

## Were the last seven days duplicated work?

**No. Nothing was re-deployed.** 535 commits between 9 and 16 August went to
WP-I evidence work — the RP6, RP7, transport and SEC102 block repairs and their
audits, the Pathscope cycles, Stage-1 preregistration, the KVM2 Phase-2
contracts, and the freeze package. That work is not a repeat of the staging
deployment; it is the evidence programme that gates the KVM2 deployment.

**But a large share of it was low-yield, and that is the honest finding:**

- **Pathscope: five full cycles, none accepted.** Each closed its named
  findings and each surfaced the same defect class one step further out. Now
  retired by owner decision §6 as supplemental-with-disclosure.
- **Documentation multi-audits.** Memory already carries this lesson from
  2026-08-09: "4-model audit + xhigh repair loops on *documentation* burned
  ~10 h wall-clock post-Gate — reserve flagship multi-audit for
  code/staging/deploy surfaces." The lesson was recorded and then not applied.
- **Reasoning about unknowns instead of resolving them.** Roughly fifty
  documents were produced about eight facts that twenty minutes of authorized
  observation answered.

So: no duplicated deployment, but real hours lost to an evidence standard
disproportionate to a disarmed paper bridge on a disposable VM, and to
inference where observation was available.

## Precautions adopted

| # | Precaution | Where it now lives |
|---|---|---|
| 1 | Every deployment status row names its host; a row without one is unverified | memory `two-hosts-never-conflate` |
| 2 | When a plan says UNKNOWN, first ask whether it can simply be observed; take the reversible safety step, observe, restore | memory `verify-state-before-planning` |
| 3 | Never inherit a status row from a previous document without re-deriving it or dating it as unverified | memory `verify-state-before-planning` (3) |
| 4 | Record living state — what is installed and running — not only verdicts | this post-mortem; observation record is the first instance |
| 5 | Stale-header banner on the superseded July bridge memory | memory `ibkr-paper-bridge-track` |
| 6 | Report observations with host, timestamp, and what they do **not** establish | memory `verify-state-before-planning` (5) |

## What is genuinely true about remaining work

The deployment *pattern* is proven on Ubuntu 24.04 and demonstrably ran. That
retires technical risk, and it means the KVM2 work is a repeat of a known
procedure rather than an unknown. It does not mean KVM2 is done, and it does
not transfer Gate-A acceptance to a current candidate. Any revised estimate
must be derived against the KVM2 row set, host-labelled, and is not asserted
here.
