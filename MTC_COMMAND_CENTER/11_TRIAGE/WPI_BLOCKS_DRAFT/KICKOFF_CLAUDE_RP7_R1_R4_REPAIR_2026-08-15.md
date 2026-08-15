# RP7 R1-R4 owner-authorized repair — 2026-08-15

## Authority and classification

Owner authorization: Barış explicitly authorized everything needed to continue
after `RP7_CAP_OVERRIDE_FINAL_OWNER_BOUNDARY_2026-08-15.md` returned RP7 to the
owner boundary. This opens **one bounded repair candidate** for the four
reproduced findings below and the two fresh mandatory T0 audits that follow.

Gate-1 classification: **T0**. The artifact is a staging-host verification
run-kit. Exact post-repair acceptance requires fresh independent
`claude-opus-5` and `gpt-5.6-sol`, both `xhigh`, after Lead verification and
freeze.

This repair grants no deployment, host contact, credential access, service
mutation, broker/exchange access, ARM/order action, TESTNET/mainnet action,
Pine/parity/MTC/trading change, destructive Git, merge, or release authority.

## Implementer contract

Implementer: one fresh exact `claude-opus-5`, effort `xhigh`, no
resume/continue and no sub-delegation. Work only in `C:\R7FINAL`.

Read in order:

1. root `AGENTS.md`;
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`;
3. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`;
4. `RP7_CAP_OVERRIDE_FINAL_OWNER_BOUNDARY_2026-08-15.md`;
5. both cap-override T0 verdicts and the Codex Lead adjudication;
6. the four frozen artifacts in full or by targeted ranges where large.

Do not modify Git metadata or run checkout/reset/stash/commit/push/worktree
commands. Existing files may have Windows checkout CRLF transport; final owned
artifact bytes must be LF-only and must be tested as such.

Repository writes are limited to these four files:

- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_REPORT_2026-08-13.md`

All dynamic execution evidence must remain in one run-owned temporary tree
outside the repository. Preserve all useful accepted behavior and prior
findings. No broad rewrite.

Frozen baseline subject: `2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b`.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 132886 | `a4af307c34cbc6092676b0838e17090dcadeb1116703773f1dbd42749670b243` |
| `SELF_QA_RP7.md` | 504144 | `72aab351fc9f0d5881bbac995985338dc983777978b1787b4b5abe3bf0fda58f` |
| `STATUS_RP7.md` | 12213 | `df44704c4099459d2860fd6ddbfc0b659b981eb4ecbe06a7f1ef89b99499ad65` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 41843 | `4e5d38d422ab836aca3e2421f0430b4cdb72680c5d34de86e33d14b2c0fd7cde` |

## REQUIRED repairs

### R1 — bind row 9 to the production normalization boundary

The production caller reads effective `Environment` from `systemctl show`.
Systemd accepts a raw mid-name quote spelling and normalizes it to the clean
protected assignment, which the repaired tokenizer accepts. The current D026
injects the raw spelling directly into fake show output and therefore bypasses
the manager boundary.

Repair the real invariant without weakening the existing effective-property
check. If lexical spelling is part of the invariant, bind it to the attested
unit source (drop-ins are already required empty) and prove the raw source form
cannot bypass the production caller. If only effective semantics are intended,
the safety contract and tests must be made truthful and must not claim source
spelling rejection. Do not silently choose a weaker contract. Produce a real
production-path D026 RED against the frozen bytes and GREEN against repaired
bytes, with fully quoted/value-quoted valid controls and an explicit duplicate
policy. Use a live systemd oracle where the claim depends on systemd behavior.

### R2 — reconcile provenance

Remove every contradictory `no Lead run` / `none_yet` statement. The four
artifacts must tell one exact, chronological truth about the Lead and auditor
runs. Do not rewrite history: distinguish frozen-baseline runs from this repair
candidate's implementer self-QA and from later Lead/auditor work not yet run.

### R3 — make the published transcript literally reproducible

The prior contract required exact transcript reproduction but required external
normalization of the run-owned scratch root and excluded a dynamic mount digest.
Repair the harness/report contract so the **raw published transcript** is
deterministic and compares exactly across runs while runtime scratch isolation
and real mount binding remain intact. Canonicalize only presentation fields;
retain and verify the real raw values internally or in run-owned temporary
evidence. The harness itself must fail closed if canonicalization loses binding
or masks a predicate-relevant difference. Demonstrate two fresh sequential
runs whose published transcripts compare byte-for-byte equal with no external
editing or normalization.

### R4 — model systemd bare-CR line termination

The frozen parser uses `text.split("\n")` plus `rstrip("\r")`; systemd 259 also
terminates a line at bare CR. This can return rc 0 `install_section=absent` for a
fragment systemd parses with a real `[Install]` section.

Use an exact systemd-faithful terminator model, not broad `str.splitlines()`.
Add bare-CR and multi-CR production-path D026 pairs against the frozen/round-4
subjects and repaired bytes. Extend the live oracle so it varies terminator
identity. Preserve LF, CRLF, trailing-space-after-backslash, odd/even
backslash, comment bridge, blank termination, malformed header, UTF-8/NUL, and
EOF behavior. Record exact commands and outputs.

## Mandatory self-QA and completion

1. `bash --noprofile --norc -n` on the LF-only repaired script.
2. Run the complete rows-1-9 fence sequentially with a unique scratch root.
3. Run every new R1-R4 D026 RED/GREEN and control against actual named subjects
   in separate processes; no reimplemented block logic.
4. Run the complete fence twice and prove the raw  transcript outputs are
   byte-for-byte identical while real internal scratch/mount identities differ.
5. Require zero harness abort, capture collision, unexpected stderr, ERR-trap
   contamination, or identity drift.
6. Run `git diff --check` and report exact changed paths, bytes, SHA-256, CR
   counts, syntax result, commands, meaningful outputs, and remaining risks.

Stop only after all four files are mutually consistent and the complete fence
passes. Do not write a separate verdict; update `STATUS_RP7.md` and the existing
report with the repair/self-QA record. The Lead will independently inspect,
execute, freeze, commit, and dispatch the fresh auditors.
