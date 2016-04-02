#! /usr/bin/env sh
# {{ ansible_managed }}

exec /sbin/ip route add default via 172.31.240.1 dev "$1" table {{ ffhb_routing_table }}
