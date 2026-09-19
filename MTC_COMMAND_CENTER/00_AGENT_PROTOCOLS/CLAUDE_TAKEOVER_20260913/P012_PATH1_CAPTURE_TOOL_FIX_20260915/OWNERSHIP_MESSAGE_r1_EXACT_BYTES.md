# r1 ownership message — the EXACT signed bytes (record fix, 2026-09-17)

**Why this file exists.** The exact-Opus T0 read of the capture tool (`af921d75`, lane 2, 2026-09-17) observed that `OWNERSHIP_MESSAGE_r1.txt` in this record is NOT the byte string that was signed: the file was produced by redirecting the tool's `--print-ownership-message` output on Windows, so it carries CRLF line endings and a trailing newline (139 bytes, 3 CR). Git's `text=auto` normalisation turns the committed blob into LF + trailing newline (136 bytes) — also not the signed string. A reviewer who recovers the signature over either file form gets `0x1e10…0324`, a different address, and would wrongly conclude the ownership evidence fails. The Lead reproduced all three recoveries on 2026-09-17 (exact bytes → owner `0x1E26…AC49` = manifest `address` = manifest `recovered_address`; CRLF file → `0x1e10…0324`; LF + trailing newline → not the owner).

**The signed string** is exactly `ownership_message(address, run_id)` from `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` at `af921d75` (`:107-112`) — three lines joined by a single LF (`\n`), address lower-cased, NO trailing newline:

```
P012 Path 1 own-account evidence capture
address: <owner address, lower-case, 42 chars>
run_id: p012-path1-20260914T1500Z-1900Z-r1
```

- length: **135 bytes**; CR count 0; trailing newline: none
- sha256 of the exact bytes: `736dadd86bbb4443115534651115a2c51371d237b090ddfeac605b8568c33721`
- base64 of the exact bytes (decode to reproduce them byte-for-byte; this is the durable form because git normalises text files):
  `UDAxMiBQYXRoIDEgb3duLWFjY291bnQgZXZpZGVuY2UgY2FwdHVyZQphZGRyZXNzOiAweDFlMjY1ZjVlMzk5NTdlMDhlZDAyYTEyMGNlZmEzM2E5YmQ0NmFjNDkKcnVuX2lkOiBwMDEyLXBhdGgxLTIwMjYwOTE0VDE1MDBaLTE5MDBaLXIx`
- signature: `sig_r1.txt` (sha256 `2b7a9eb46ccf8b24…` as recorded in `run.log`), 132-character hex string; scheme EIP-191 `personal_sign` (`encode_defunct(text=…)`).

**Verification recipe (no network):**

```
python - <<EOF
import base64; from eth_account import Account; from eth_account.messages import encode_defunct
msg = base64.b64decode("<base64 above>").decode()
print(Account.recover_message(encode_defunct(text=msg), signature=open("sig_r1.txt").read().strip()))
EOF
```
must print the owner address (`0x1E26…AC49`, checksum form). Equivalent: `python capture_own_account_evidence.py --print-ownership-message p012-path1-20260914T1500Z-1900Z-r1 --address <owner address>` prints the same three lines, but `print()` appends a newline (CRLF on a Windows console/redirect) — strip it before recovering.

`OWNERSHIP_MESSAGE_r1.txt` stays in the record as the historical artefact; treat it as display text, never as the signed bytes. Carried tool NIT-7 (lane 2): the tool should copy the exact signed text and the signature into `CAPTURE_MANIFEST.json` so an output directory stands alone.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
