# Exact T0 review — WP-P0-30 Shape-B archive exporter, candidate `45a7f50eac009646bde1d80bcf66b1d14e6d72e0`

Reviewer: exact `claude-opus-5`, xhigh. Second exact-Opus read (repair round 1 of 3).
Status: IN PROGRESS — this file is written incrementally; the final line is the verdict.

## 1. Verified identities (COMPUTED)

| item | value | how |
| --- | --- | --- |
| HEAD | `45a7f50eac009646bde1d80bcf66b1d14e6d72e0` | `git -c safe.directory=* -C C:/tmp/P030_INTEGRATION_20260913 rev-parse HEAD` |
| `p030_archive_exporter.py` (blob @HEAD) | `1bb9fb66ff94c95c2d19b3ae04137a4afd8514785ab27141420d4a57d9da0d1f`, 494 lines | `git show HEAD:<path> \| sha256sum` |
| `check_p030_archive_exporter.py` (blob @HEAD) | `4e2d291360565754094cc5f61701505a3507a4b199206853960eccfed19bce9e`, 787 lines | same |
| worktree files | byte-identical to the blobs (LF checkout, `Get-FileHash` matches) | `Get-FileHash -Algorithm SHA256` |
| `p030_market_data_contracts.py` | `433db0e6b2f86f8c0b3bd4375a0fbb1112f331a91284a6d4d1744760c2e3fca3`, 470 lines | blob @HEAD |
| `p030_closed_partition_backup_adapter.py` | `2cba917e8b553cb8e6a25da382f84408c6386ffb0a4050e2babc33ee847c5c3b`, 816 lines | blob @HEAD |
| `market_data_collector.py` | `2819b248be23ce3c59c2d97fcb3968fef91966f635585287b292d466ce80018e`, 542 lines | blob @HEAD |
| interpreter | Python 3.12.12 (`C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`) | `python.exe -V` |

(sections filled in below as the review proceeds)

VERDICT: BLOCK
