ipt6 -t mangle -A PREROUTING -d {{ jool_pool6 }} -j JOOL
ipt4 -t mangle -A PREROUTING -d {{ jool_pool4 }} -p icmp -j JOOL
ipt4 -t mangle -A PREROUTING -d {{ jool_pool4 }} -p tcp --dport {{ jool_pool4_ports_min }}:{{ jool_pool4_ports_max }} -j JOOL
ipt4 -t mangle -A PREROUTING -d {{ jool_pool4 }} -p udp --dport {{ jool_pool4_ports_min }}:{{ jool_pool4_ports_max }} -j JOOL
