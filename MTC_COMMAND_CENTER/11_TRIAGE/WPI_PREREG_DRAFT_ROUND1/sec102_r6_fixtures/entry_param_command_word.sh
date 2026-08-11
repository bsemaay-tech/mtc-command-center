#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
# interpreter identity=/safe/fixture/library.sh
A=1 ${SHELL_BIN} /safe/fixture/library.sh
cat "$ROOT/$RUNID/input.txt"
