# Manual User Input Protocol

The user provides inputs AI cannot reliably obtain:

- YouTube transcripts
- TradingView exports
- TradingView compile output
- Secret/API token entry
- Approval decisions

Default drop location:

```text
00_INBOX/from_user/<input_id>/
```

Every drop needs a manifest with input type, task ID, expected files, actual files, hashes, and notes. Originals are immutable evidence.
