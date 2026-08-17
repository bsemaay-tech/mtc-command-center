#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# interpreter identity=/safe/fixture/library.sh
/usr/bin/{ba,z}sh /safe/fixture/library.sh
cat "$ROOT/$RUNID/input.txt"
