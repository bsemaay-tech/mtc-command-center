#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/library.sh
test -f /safe/fixture/marker; source "$LIBRARY_PATH"
cat "$ROOT/$RUNID/input.txt"
