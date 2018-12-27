#! /usr/bin/env sh

# Copy default route
if [ "$IFACE" = "{{ ansible_default_ipv4.interface }}" ]; then
  if [ -z "$(ip -4 route list 0/0 table {{ ffhb_routing_table }} | grep '^default')" ]; then
    ip -4 route list 0/0 | xargs ip route add table {{ ffhb_routing_table }}
  fi
fi
