# Command sheet — later, separately authorized one-attempt install

- Status: **NOT AUTHORIZED. NOT EXECUTED.** This file is a script, in the
  theatrical sense: it says what would be typed, by whom, after which gate. It
  is not permission to type any of it.
- Every block below names the gate that must close *first*. A closed gate
  authorizes exactly its own block and nothing after it.

Conventions used below:

- `<SHA>` — the exact 40-hex release commit accepted at KVM2-P3-05.
- `<PAYLOAD>` — the payload directory produced by `package.sh`.
- `<PAYLOAD_MANIFEST_SHA256>` — the separately recorded SHA-256 of the
  payload's `RELEASE_SHA256SUMS`.
- No command in this file prints, echoes, or accepts a secret value.
- No command in this file adds, removes or changes a firewall rule.

---

## Stage A — build the payload (trusted build host, not KVM2)

Gate: none beyond ordinary repo rules. Produces artifacts only.

```bash
bash ./IBKR_PAPER_BRIDGE/deploy/linux/package.sh \
    --release-sha <SHA> \
    --repo /path/to/clean/checkout \
    --out  /path/to/payload
sha256sum /path/to/payload/RELEASE_SHA256SUMS   # record in the RC manifest
```

`package.sh` refuses a dirty worktree and refuses a HEAD that is not `<SHA>`.

Optional, for a fully offline install — build the wheelhouse on a machine with
the same platform tag as the target:

```bash
python3.12 -m pip download --require-hashes --no-deps --only-binary=:all: \
    -r IBKR_PAPER_BRIDGE/requirements.lock -d /path/to/wheelhouse
```

---

## Stage B — dry run (KVM2, read-mostly)

Gate: **KVM2-P4-01** (installation and configuration authorization).

`--dry-run` prints every mutating action instead of performing it. It creates no
user, no directory, no unit and no venv.

```bash
sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha <SHA> \
    --manifest-sha256 <PAYLOAD_MANIFEST_SHA256> \
    --source <PAYLOAD> --dry-run
```

Read the printed plan in full before Stage C. If anything is unexpected: stop,
report, do not proceed.

---

## Stage C — the one bounded install attempt

Gate: **KVM2-P4-02** (exactly one attempt; a retry needs a new KVM2-P4-01).

```bash
sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
    --release-sha <SHA> \
    --manifest-sha256 <PAYLOAD_MANIFEST_SHA256> \
    --source <PAYLOAD>
# fully offline variant:
# sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh --release-sha <SHA> \
#      --manifest-sha256 <PAYLOAD_MANIFEST_SHA256> --source <PAYLOAD> \
#      --wheelhouse /path/to/wheelhouse
```

Then verify — read-only, safe to repeat:

```bash
sudo bash ./deploy/linux/verify.sh \
    --release-sha <SHA> \
    --manifest-sha256 <PAYLOAD_MANIFEST_SHA256>
```

Expected end state: release sealed read-only, venv hash-locked, unit installed
**masked**, service **not started**, **not enabled**, env file present at
`0600 root:root` with no values, UFW unchanged and SSH-only.

Record from the output: the first-start unit SHA-256 and
`requirements.lock` SHA-256 (also written to
`/etc/mtc-bridge/install_manifest.json`).

---

## Stage D — secret provisioning

Gate: **KVM2-P4-03** — owner-only, separate from P4-01/P4-02, TESTNET only.

Not scripted here on purpose. The values are typed by the owner into
`/etc/mtc-bridge/mtc-bridge.env` (already `0600 root:root`) through an editor on
a trusted session. Names are listed in `env/mtc-bridge.env.template`.

Post-conditions to assert afterwards, values never printed:

```bash
sudo stat -c '%a %U:%G' /etc/mtc-bridge/mtc-bridge.env      # expect: 600 root:root
sudo grep -c '^HL_LIVE_ACK=' /etc/mtc-bridge/mtc-bridge.env # expect: 0
sudo bash ./deploy/linux/verify.sh \
    --release-sha <SHA> \
    --manifest-sha256 <PAYLOAD_MANIFEST_SHA256>
```

---

## Stage E — quiesce and cutover

Gates: **KVM2-P4-04** (tabletop) → **KVM2-P4-04A** (quiesce the Windows writer)
→ **KVM2-P4-05** (ordered single-writer cutover).

Nothing on KVM2 starts during this stage. The state capture runs on the **old**
writer host, under its own authorization:

```bash
set -Eeuo pipefail
BUNDLE_DIR="/path/to/state-bundle"
CAPTURE_REPORT="${BUNDLE_DIR}.capture-report.json"
HASH_RECORD="/separately-held/state-bundle.expected-sha256"

python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create \
    --source "/path/to/quiesced/bridge.db" --out-dir "${BUNDLE_DIR}" \
    > "${CAPTURE_REPORT}"

EXPECTED_BUNDLE_SHA256="$(
    python3.12 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["bundle_db_sha256"])' \
        "${CAPTURE_REPORT}"
)"
EXPECTED_INVARIANTS_SHA256="$(
    python3.12 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["invariants_sha256"])' \
        "${CAPTURE_REPORT}"
)"
ACTUAL_BUNDLE_SHA256="$(sha256sum "${BUNDLE_DIR}/bridge.db" | awk '{print $1}')"
[ "${ACTUAL_BUNDLE_SHA256}" = "${EXPECTED_BUNDLE_SHA256}" ] || exit 1
EXPECTED_MANIFEST_FILE_SHA256="$(
    sha256sum "${BUNDLE_DIR}/bundle_manifest.json" | awk '{print $1}'
)"
for expected_hash in \
    "${EXPECTED_BUNDLE_SHA256}" \
    "${EXPECTED_INVARIANTS_SHA256}" \
    "${EXPECTED_MANIFEST_FILE_SHA256}"; do
    [[ "${expected_hash}" =~ ^[0-9a-f]{64}$ ]] || exit 1
done

umask 077
printf '%s\n' \
    "EXPECTED_BUNDLE_SHA256=${EXPECTED_BUNDLE_SHA256}" \
    "EXPECTED_INVARIANTS_SHA256=${EXPECTED_INVARIANTS_SHA256}" \
    "EXPECTED_MANIFEST_FILE_SHA256=${EXPECTED_MANIFEST_FILE_SHA256}" \
    > "${HASH_RECORD}"
```

Keep `HASH_RECORD` outside the bundle and transfer/record it through the
separately controlled evidence channel. On the receiving host, set
`BUNDLE_DIR` and `HASH_RECORD` to the transferred paths, then fail closed before
the manifest is parsed:

```bash
set -Eeuo pipefail
BUNDLE_DIR="/path/to/transferred-state-bundle"
HASH_RECORD="/path/to/separately-transferred/state-bundle.expected-sha256"
EXPECTED_BUNDLE_SHA256="$(awk -F= '$1=="EXPECTED_BUNDLE_SHA256" {print $2}' "${HASH_RECORD}")"
EXPECTED_INVARIANTS_SHA256="$(awk -F= '$1=="EXPECTED_INVARIANTS_SHA256" {print $2}' "${HASH_RECORD}")"
EXPECTED_MANIFEST_FILE_SHA256="$(awk -F= '$1=="EXPECTED_MANIFEST_FILE_SHA256" {print $2}' "${HASH_RECORD}")"
for expected_hash in \
    "${EXPECTED_BUNDLE_SHA256}" \
    "${EXPECTED_INVARIANTS_SHA256}" \
    "${EXPECTED_MANIFEST_FILE_SHA256}"; do
    [[ "${expected_hash}" =~ ^[0-9a-f]{64}$ ]] || exit 1
done

printf '%s  %s\n' \
    "${EXPECTED_MANIFEST_FILE_SHA256}" "${BUNDLE_DIR}/bundle_manifest.json" \
    | sha256sum --strict --check -
python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py verify \
    --bundle-dir "${BUNDLE_DIR}" \
    --expect-bundle-sha256 "${EXPECTED_BUNDLE_SHA256}" \
    --expect-invariants-sha256 "${EXPECTED_INVARIANTS_SHA256}"
```

Do **not** pass `--allow-live-source`: for a cutover the writer must already be
quiesced, so any source drift during capture is a stop condition, not a warning.

Transfer, then install the accepted destination state (the destination hash from
the manifest must match what P4-05 recorded):

```bash
sudo install -o mtc-bridge -g mtc-bridge -m 0640 \
    "${BUNDLE_DIR}/bridge.db" /var/lib/mtc-bridge/bridge.db
[ "$(sudo -u mtc-bridge sha256sum /var/lib/mtc-bridge/bridge.db | awk '{print $1}')" \
    = "${EXPECTED_BUNDLE_SHA256}" ] || exit 1
```

---

## Stage F — exactly one first DISARMED start

Gate: **KVM2-P4-06** (authorization) then **KVM2-P4-07** (one attempt, no retry).

```bash
sudo systemctl unmask mtc-bridge-first-start.service
sudo systemctl start   mtc-bridge-first-start.service     # the single attempt
```

Immediately capture evidence — all read-only:

```bash
systemctl is-active   mtc-bridge-first-start.service
systemctl show -p NRestarts --value mtc-bridge-first-start.service   # expect 0
ss -ltn | grep 8790                                                   # 127.0.0.1 only
curl -s http://127.0.0.1:8790/api/status                              # expect DISARMED, testnet
sudo logrotate -f /etc/logrotate.d/mtc-bridge                         # forced-rotation test
```

`verify.sh` is the fail-closed installed-but-masked verifier and must not be
wrapped in `|| true`. After the separately authorized unmask/start, its mask
assertion is intentionally no longer applicable; use the bounded P4-07 evidence
checks above and the accepted staging procedure instead of suppressing a
verifier failure.

Monitoring is reached only through an SSH tunnel from the operator's machine:

```bash
ssh -N -L 8790:127.0.0.1:8790 <operator ssh alias>
```

Port 8790 is never published, never reverse-proxied, never added to UFW.

---

## Stage G — rollback (only if Stage C–F must be undone)

Gate: **KVM2-P4-08** (rollback proof). Recovery start is *not* part of it.

```bash
sudo bash ./deploy/linux/rollback.sh \
    --state-manifest-file <STATE BUNDLE MANIFEST FILE> \
    --state-manifest-sha256 <STATE BUNDLE MANIFEST SHA256> \
    --to-release-sha <PRIOR SHA> \
    --to-manifest-sha256 <PRIOR PAYLOAD MANIFEST SHA256>
sudo bash ./deploy/linux/verify.sh \
    --release-sha <PRIOR SHA> \
    --manifest-sha256 <PRIOR PAYLOAD MANIFEST SHA256>
```

State under `/var/lib/mtc-bridge` is preserved, never reset. A post-rollback
recovery start needs **KVM2-P4-08A** authorization and a single **KVM2-P4-08B**
attempt.

---

## Not in this file, on purpose

ARM (KVM2-P5-05/P5-05A), monitoring and backup provider provisioning
(KVM2-P5-01), AI-lab admission (Phase 6), any firewall or network change, any
mainnet action. Each needs its own owner sentence, and none of them is implied
by completing every stage above.
