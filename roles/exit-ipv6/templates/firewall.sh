ipt6 -A FORWARD -i {{ main_bridge }} -o {{ exit_ipv6_interface }} -j ACCEPT
ipt6 -A FORWARD -o {{ main_bridge }} -i {{ exit_ipv6_interface }} -j ACCEPT
ipt6 -A FORWARD -i {{ main_bridge }} -o {{ main_bridge }} -j ACCEPT
ipt -A INPUT -p ipv6 -j ACCEPT
