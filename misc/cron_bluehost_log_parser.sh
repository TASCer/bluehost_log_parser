#!/bin/bash

# Title:        cron_bluehost_log_parser.sh
# Description:  runs script with no args
# Author:       TASCS LLC
# Date:         2026-11-02
# Version:      1.0
# Usage:        ./cron_bluehost_log_parser.sh 
# Helper:       https://linux.die.net/man/1/keychain


# Load keychain variables
[ -z "$HOSTNAME" ] && HOSTNAME=`uname -n`
. $HOME/.keychain/$HOSTNAME-sh 2>/dev/null

# TRY ONE THEN OTHER UNTIL I CAN SET A PROJECT DIR
cd /home/todd/bluehost_log_parser/src/bluehost_log_parser || cd /home/todd/python_projects/bluehost_log_parser/src/bluehost_log_parser

/home/todd/.local/bin/uv run main.py

