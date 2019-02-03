# l3roamd
ipt -A INPUT -i {{babel_bridge}} -p udp --dport 5523 -j ACCEPT
