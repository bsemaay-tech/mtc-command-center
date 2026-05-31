# Dashboard App

This folder contains the MCC dashboard runtime area.

## MVP-1 State

`apps/api` contains a dependency-free Python read-only API core. It can:

- validate the MVP-1 read model
- report `/healthz`
- serve `/api/read-model`
- serve `/api/snapshot`

`apps/web` remains a placeholder. The first browser UI should consume the read-only snapshot API before any write controls are introduced.

## Reference

command-dash may be studied as a reference architecture, but MCC will be its own independent dashboard.

## Initial Direction

The first dashboard version should read MCC status, task, registry, and report files without modifying MTC_v2 core systems.
