# r2 ownership message — the EXACT signed bytes (no display file; lesson of r1)

The signed string is `ownership_message(address, run_id)` from `capture_own_account_evidence.py` at `af921d75` (`:107-112`): three lines joined by LF, address lower-cased, no trailing newline — 135 bytes, sha256 `81a0c120690bbe2ec1be9fbd233e6888fd3044c97317cfaa468892e119f586d6`.

base64 of the exact bytes (decode to reproduce byte-for-byte):
`UDAxMiBQYXRoIDEgb3duLWFjY291bnQgZXZpZGVuY2UgY2FwdHVyZQphZGRyZXNzOiAweDFlMjY1ZjVlMzk5NTdlMDhlZDAyYTEyMGNlZmEzM2E5YmQ0NmFjNDkKcnVuX2lkOiBwMDEyLXBhdGgxLTIwMjYwOTE3VDA3MDBaLTExMDBaLXIy`

Signature: `sig_r2.txt` (132 hex chars, sha256 `b7f17449dcccccd2…`), EIP-191 `personal_sign`. Verification (no network): `Account.recover_message(encode_defunct(text=base64decode(...).decode()), signature=open("sig_r2.txt").read().strip())` → the owner address (`0x1E26…AC49`, checksum form). Verified by the Lead offline and by the tool before its first network call (manifest `OWNERSHIP_EVIDENCE: VERIFIED`).

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
