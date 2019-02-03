# babeld control
ipt -A INPUT -i lo -p tcp --dport 33123 -j ACCEPT

# babeld routing
{% for ifname in babel_interfaces %}
ipt6 -A INPUT -i {{ifname}} -p udp --dport 6696 -j ACCEPT
{% endfor %}
