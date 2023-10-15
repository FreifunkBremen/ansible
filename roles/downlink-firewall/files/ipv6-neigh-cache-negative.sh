#!/usr/bin/env sh

set -eu

# This little script listens to `ip -6 monitor neigh` and adds addresses for
# which IPv6 ND lookups failed to an ipset, which in turn can be used by the
# firewall to drop packets to these addresses.

IPSET_NAME="ND_FAILED"
IPSET_TIMEOUT=60
IPSET_HASHSIZE=4096


ipset -exist create "$IPSET_NAME" hash:net family inet6 hashsize "$IPSET_HASHSIZE" timeout "$IPSET_TIMEOUT"

ip -6 monitor neigh | while read -r LINE; do
    [ "${LINE##* }" = "FAILED" ] || continue
    [ "${LINE#fe80::}" = "$LINE" ] || continue
    printf "add -exist %s %s\nCOMMIT\n" "$IPSET_NAME" "${LINE%% *}"
done | ipset restore
