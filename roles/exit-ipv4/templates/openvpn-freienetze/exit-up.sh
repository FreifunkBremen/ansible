#! /usr/bin/env sh
# {{ ansible_managed }}

exec /sbin/ip route add default dev "$1" table {{ ffhb_routing_table }}
