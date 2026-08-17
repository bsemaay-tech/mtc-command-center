#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/library.sh
function reload { source "$LIBRARY_PATH"; }
reload
cat "$ROOT/$RUNID/input.txt"
