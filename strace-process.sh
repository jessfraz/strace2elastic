#!/bin/bash
#
# Add this script as a PostStart Hook in your runc runtime config.

read input
pid=$(echo "$input" | jq --raw-output '.pid')
strace -f -ttt -T -p "$pid" -o strace.log &
exit 0
