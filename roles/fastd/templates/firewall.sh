ipt6 -A INPUT -p udp --dport {{ fastd_port }} -s 2002::/16 -j REJECT --reject-with icmp6-adm-prohibited
ipt -A INPUT -p udp --dport {{ fastd_port }} -j ACCEPT
