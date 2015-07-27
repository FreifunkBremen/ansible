#!/bin/sh

exec jq -e ".peers | map(select(.key == \"$PEER_KEY\")) | length == 0" \
    "${1:-blacklist.json}" > /dev/null
