# Owner authorization — V6 §3 installation sentence SIGNED — 2026-08-16

The owner approved in chat, verbatim: "I approve the V6 §3 sentence.
ssh-agent is loaded."

This adopts the single authoritative sentence of
`KVM2_DEPLOYMENT_PLAN_V6_2026-08-16.md` §3 (plan bytes 7342 B sha256
`c41b4cab97f460be3ac5e5fcd24f47b308819e97169c513c65a87b33bb4d16a5`; annex
31980 B sha256
`5a3f92e68514681dd94a913bc00a7f6964ab8efa98a6904be8c507f738761d7a`) for
exact release `acdf4e379fb60ee319854acae19fd3eaf7db71a2` on `srv1856225`.

Scope exactly as the sentence enumerates: one attempt; masked, never-started,
credential-free DISARMED install; read-only operational evidence; the listed
objects and nothing else. No service start, no enable, no secret, no firewall
change, no TESTNET/mainnet, no broker, no ARM, no orders, no retry without a
new sentence. First start and D3 remain separately gated.

Execution begins immediately after this record is committed.

## Supplementary authorization — python3.12-venv — 2026-08-16

Dry run failed closed at the venv preflight (as designed): KVM2 lacks
`python3.12-venv`. Owner approved in chat: install the standard Ubuntu
package `python3.12-venv` (with required dependencies) via apt, then continue
the approved V6 §3 execution. No mutation had occurred; the one bounded
install attempt was unspent.

## Supplementary authorization — UFW comment-normalization repair — 2026-08-16

Second dry-run stop (fail-closed, correct): live UFW rows carry Ubuntu's
trailing `# SSH` comments; the parser models no trailing comment → UNMODELLED.
Owner authorizes ONLY: the one-line trailing-comment normalization repair,
focused fixtures + RED/GREEN proving (1) `22/tcp ALLOW IN Anywhere # SSH`
accepted, (2) a commented rule exposing 8790 still rejected, (3) unknown/
malformed forms remain fail-closed; confirmation-only closure by both
reviewers; rebuild/re-pin of candidate, payload, plan, annex, sentence.
NOT yet authorized: continuing installation or contacting KVM2 with changed
bytes — new pins + corrected sentence go to the owner for signature first.

## Execution-record correction (owner-directed)

KVM2 current state: the uploaded OLD payload `~/payload-acdf4e37` is present
in /home/baris; the separately authorized `python3.12-venv` package (with
dependencies) is installed and is the new authorized baseline. NO Bridge
installation occurred; no service was created or started; the bounded
installation attempt remains UNSPENT. The updated plan must account for
removal or replacement of the old payload.

## OVERNIGHT COMPLETION AUTHORIZATION — 2026-08-16 night (owner, verbatim)

1. If both reviewers CONFIRM the exact UFW-repair closure with nothing else
   changed, the owner signs the corrected V6 §3 installation sentence with the
   new candidate/payload/annex pins, old payload replaced by the new one.
2. If the install, verification, rollback rehearsal, backup/restore check,
   and re-inventory all pass exactly per the plan, the owner authorizes
   exactly one first DISARMED start of that installed release —
   credential-free, loopback-only — the D3 dashboard verification matrix
   including the temporary auditd package and single audit rule with their
   recorded removal, and leaving the service running DISARMED overnight.
3. Any failure, anomaly, or deviation: stop fail-closed, change nothing
   further, report for morning. No secrets, no TESTNET keys, no ARM, no
   orders, no mainnet, no firewall changes, no retry without a new sentence.
