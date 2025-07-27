#!/bin/bash

# KEYCHAIN WIP
# Load keychain variables and check for id_dsa
[ -z "$HOSTNAME" ] && HOSTNAME=`uname -n`
. $HOME/.keychain/$HOSTNAME-sh 2>/dev/null
#ssh-add -l 2>/dev/null | grep -q id_dsa || exit 1


# DEBIAN
# cd /home/todd/python_projects/bluehost_log_parser/src/bluehost_log_parser

# RPI4
cd /home/todd/bluehost_log_parser/src/bluehost_log_parser

/home/todd/.local/bin/uv run main.py

# https://linux.die.net/man/1/keychain
