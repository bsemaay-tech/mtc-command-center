#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/evil/library.sh
source "$LIBRARY_PATH"
cat "$ROOT/$RUNID/input.txt"
