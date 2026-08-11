#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
cat <<'TEXT'
source library.sh
TEXT
cat "$ROOT/$RUNID/input.txt"
