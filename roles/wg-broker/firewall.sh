# broker
ipt -A INPUT -p tcp --dport {{ wgbroker_port }} -j ACCEPT

# wireguard tunnel
ipt -A INPUT -p udp -m multiport --dports {{ wgbroker_wg_startport }}:{{ wgbroker_wg_endport }} -j ACCEPT

# forwarding between wireguard interfaces
ipt6 -A FORWARD -o babel-wg+ -i babel-wg+ -j ACCEPT

# babel
ipt6 -A INPUT -i babel-wg+ -p udp --dport 6696 -j ACCEPT

# mmfd
ipt6 -A INPUT -i babel-wg+ -p udp --dport 27275 -j ACCEPT

# respondd
ipt6 -A INPUT -i babel-wg+ -p udp --dport 1001 -j ACCEPT

