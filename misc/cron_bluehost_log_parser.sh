#!/bin/bash

# TODO ISSUE WITH USING SSH AGENT KEYCHAIN?
# NO WORKIE
# SSH_AUTH_SOCK="/tmp/ssh-F3EIZbRPwwAu/agent.4956"
# SSH_AGENT_PID=4957
# SSH_AGENT_PID=`pgrep -U $USER ssh-agent`
# for PID in $SSH_AGENT_PID; do
#    let "FPID = $PID - 1"
#    FILE=`find /tmp -path "*ssh*" -type s -iname "agent.$FPID"`
#    export SSH_AGENT_PID="$PID" 
#    export SSH_AUTH_SOCK="$FILE"
# done

# NO WORKIE
# auth=`find /tmp -user $LOGNAME -type s -name "*agent*" -print 2>/dev/null`
# SSH_AUTH_SOCK=$auth
# export SSH_AUTH_SOCK

cd /home/todd/python_projects/bluehost_log_parser/src/bluehost_log_parser

# source /home/todd/python_projects/rsyslog_processor/.venv/bin/activate

/home/todd/.local/bin/uv run main.py
