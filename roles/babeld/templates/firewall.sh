# babeld
ipt -A INPUT -i lo -p tcp --dport 33123 -j ACCEPT
{% for ifname in babel_interfaces %}
ipt -A INPUT -i {{ifname}} -p udp --dport 6696 -j ACCEPT
{% endfor %}

## TEST-Services
## babelweb
# ipt -A INPUT -p tcp --dport 8080 -j ACCEPT
## yanic-webinterface
# ipt -A INPUT -p tcp --dport 8081 -j ACCEPT

## allow yanic recieve respondd from babel network
{% for ifname in babel_interfaces %}
ipt -A INPUT -i {{ifname}} -p udp --sport 1001 -j ACCEPT
{% endfor %}

ipt -A INPUT -i mmfd0 -p udp --sport 1001 -j ACCEPT

## allow yanic recieve respondd from batman-adv network
# ipt -A INPUT -i br-ffhb -p udp --sport 1001 -j ACCEPT
