# babeld control
ipt -A INPUT -i lo -p tcp --dport 33123 -j ACCEPT

# babeld routing
ipt6 -A INPUT -i babel-+ -p udp --dport 6696 -j ACCEPT

#forwarding between babel interfaces
ipt6 -A FORWARD -o babel-+ -i babel-+ -j ACCEPT

