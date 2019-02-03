# mmfd
{% for ifname in babel_interfaces %}
ipt -A INPUT -i {{ifname}} -p udp --dport 27275 -j ACCEPT
{% endfor %}
