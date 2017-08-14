ipt6 -A INPUT -i {{ main_bridge }} -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i vpn-{{ site_code }}-babel -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i vpn-{{ site_code }}-legacy -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i vpn-{{ site_code }} -p udp --dport 1001 -j ACCEPT
