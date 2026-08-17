#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
LIB="$LIBRARY_PATH"
source "$LIB"
cat "$ROOT/$RUNID/input.txt"
