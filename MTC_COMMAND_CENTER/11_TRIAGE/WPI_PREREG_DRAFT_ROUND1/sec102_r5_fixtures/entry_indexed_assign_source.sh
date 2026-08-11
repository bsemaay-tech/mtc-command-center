#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/library.sh
SEEN[0]=1 source "$LIBRARY_PATH"
cat "$ROOT/$RUNID/input.txt"
