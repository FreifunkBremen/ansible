#! /usr/bin/env bash
# {{ ansible_managed }}

# shellcheck disable=SC2154
{
    /sbin/ip route add "$trusted_ip" via "$route_net_gateway"
    /sbin/ip route add default via "$route_vpn_gateway" dev "$1" table '{{ ffhb_routing_table }}'
}
