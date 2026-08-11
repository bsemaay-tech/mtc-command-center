#!/usr/bin/env bash
ROOT='/safe/fixture'
RUNID='WPI-FIXTURE-FREEZE'
python verifier.py
cat "$ROOT/$RUNID/input.txt"
