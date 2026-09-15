#!/bin/bash

# https://linux.die.net/man/1/keychain

[ -z "$HOSTNAME" ] && HOSTNAME=`uname -n`
. $HOME/.keychain/$HOSTNAME-sh 2>/dev/null

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SCRIPT_DIR

# TRY ONE THEN OTHER UNTIL I CAN SET A PROJECT DIR
cd /home/todd/bluehost_log_parser/src/bluehost_log_parser || cd /home/todd/python_projects/bluehost_log_parser/src/bluehost_log_parser

/home/todd/.local/bin/uv run main.py

