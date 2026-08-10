# LEAD PIN RESOLUTION — WP-I preregistration `<PIN-BEFORE-DISPATCH>` values (2026-08-10)

Prepared by the Claude Lead ahead of prereg finalization, while the retroactive
defect-catalogue pass (Codex) runs. Values below are frozen at fill time per the draft's
freeze rule; they go into the draft only AFTER the catalogue pass is consumed and verified.

## R1 — `WPI_UNIT_FRAGMENT_SHA256`

Full value, read from `GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md` lines 44–45:

```
538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd
```

- Matches the matrix's elided form `538c1c60...279bd` (prefix and suffix both check).
- Size cross-check: inventory records 3736 B, equal to the draft's already-pinned
  `WPI_UNIT_FRAGMENT_BYTES = 3736`.

## R2 — `WPI_LOG_DIR`

Value: **`/var/log/mtc-bridge`**

Source (non-circular, source-derived — NOT runtime `systemctl show`): the frozen
candidate's unit-fragment template at the immutable candidate SHA:

```
git show 2ce41e34bceb599d80af24c5c33d835820ec321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template
```

contains, with no substitution placeholder on these lines:

```
StandardOutput=append:/var/log/mtc-bridge/bridge.log
StandardError=append:/var/log/mtc-bridge/bridge.err.log
ReadWritePaths=/var/lib/mtc-bridge /var/log/mtc-bridge
```

Caveat recorded: the installed fragment is NOT byte-identical to the template
(`@RELEASE_SHA@` is substituted by `install.sh`; template blob LF-hash
`8b01ad1510e9bc86e38a813f42e0120312055559bc3d9967135fe49d4a79d163`, 3628 B vs installed
3736 B). The `ReadWritePaths` / log-path lines carry no placeholder, so the log-dir value
is stable across substitution. The installed fragment's identity remains pinned from the
transition inventory (R1), not from this template.

## Disposition

Both named risks R1 and R2 are now resolvable from committed records. The draft's
"No successor is dispatchable with this unfilled" condition can be satisfied at
finalization without any host contact.
