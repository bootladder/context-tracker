#!/bin/bash

# frontend wants a list of rows
# use jq to scan all objevcts and get rows

cat /var/lib/collectord/firefoxcollectordaemonpy.json | \
    jq -s '.[].rows' | jq -s '.[][]' | jq -s
