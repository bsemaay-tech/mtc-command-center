#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# static leaf identity=/safe/fixture/library.sh
/bin/cat "$ROOT/$RUNID/input.txt"
bin/verify_marker
