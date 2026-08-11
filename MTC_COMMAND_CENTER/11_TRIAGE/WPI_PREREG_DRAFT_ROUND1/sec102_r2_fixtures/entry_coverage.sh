#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# source identity=/safe/fixture/library.sh
source "$LIBRARY_PATH"
opaque_sink "$ROOT/$RUNID/input.txt"
