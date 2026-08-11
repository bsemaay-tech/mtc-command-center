#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
python /safe/fixture/verifier.py
cat "$ROOT/$RUNID/input.txt"
