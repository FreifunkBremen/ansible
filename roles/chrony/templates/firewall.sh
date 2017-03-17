ipt -A INPUT -i {{ main_bridge }} -p udp --dport 123 -j ACCEPT
