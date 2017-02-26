ipt6 -A INPUT -i {{ batman_dummy_interface }} -p udp --dport 16962 -j ACCEPT
ipt6 -A INPUT -i {{ main_bridge }} -p udp --dport 16962 -j ACCEPT
