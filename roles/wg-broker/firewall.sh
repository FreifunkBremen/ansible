# broker
ipt -A INPUT -p tcp --dport {{ wgbroker_port }} -j ACCEPT

# wireguard tunnel
ipt -A INPUT -p udp -m multiport --dports {{ wgbroker_wg_startport }}:{{ wgbroker_wg_endport }} -j ACCEPT
