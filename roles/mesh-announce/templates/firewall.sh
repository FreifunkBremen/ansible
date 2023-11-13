# batman
ipt6 -A INPUT -i '{{ main_bridge }}' -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i 'vpn-{{ site_code }}-legacy' -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i 'vpn-{{ site_code }}' -p udp --dport 1001 -j ACCEPT

# babel
ipt6 -A INPUT -i babel-ffhb -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i mmfd0 -p udp --dport 1001 -j ACCEPT
