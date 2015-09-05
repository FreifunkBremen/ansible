#! /usr/bin/env bash
# {{ ansible_managed }}

PATH=/sbin:/usr/sbin:/bin:/usr/bin

ip route add $trusted_ip via $route_net_gateway
ip route add default via $route_vpn_gateway dev $1 table {{ batman_table }}
