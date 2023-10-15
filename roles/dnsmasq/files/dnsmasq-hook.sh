#!/usr/bin/env sh

set -eu

MODE="$1"
MAC="$2"
IP="$3"

if [ -z "${DNSMASQ_INTERFACE:-}" ]; then
    exit 0
fi

case "$MODE" in
    add|old)
        ip neigh replace "$IP" dev "$DNSMASQ_INTERFACE" lladdr "$MAC" nud reachable
        ;;
    del)
        ip neigh delete "$IP" dev "$DNSMASQ_INTERFACE"
        conntrack -D -s "$IP" > /dev/null
        ;;
esac
