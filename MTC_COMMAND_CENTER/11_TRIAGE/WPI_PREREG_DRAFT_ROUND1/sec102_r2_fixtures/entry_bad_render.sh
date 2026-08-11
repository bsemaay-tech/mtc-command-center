#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WRONG-REPRESENTATION'
# source identity=/safe/fixture/library.sh
source "$LIBRARY_PATH"
cat "$ROOT/$RUNID/input.txt"
