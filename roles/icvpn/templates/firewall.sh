ipt -A FORWARD -i {{ icvpn_interface }} -o {{ main_bridge }} -j ACCEPT
ipt -A FORWARD -o {{ icvpn_interface }} -i {{ main_bridge }} -j ACCEPT

ipt -A INPUT -p tcp --dport {{ icvpn_port }} -j ACCEPT
ipt -A INPUT -p udp --dport {{ icvpn_port }} -j ACCEPT
