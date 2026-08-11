#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/library.sh
command source "$LIBRARY_PATH"
cat "$ROOT/$RUNID/input.txt"
