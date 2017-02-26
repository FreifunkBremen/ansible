ipt -A INPUT -p udp --dport 53 -j ACCEPT
ipt -A INPUT -p tcp --dport 53 -j ACCEPT
