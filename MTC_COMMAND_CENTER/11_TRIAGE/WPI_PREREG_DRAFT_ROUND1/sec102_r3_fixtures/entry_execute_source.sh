#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
bash /safe/fixture/library.sh
cat "$ROOT/$RUNID/input.txt"
