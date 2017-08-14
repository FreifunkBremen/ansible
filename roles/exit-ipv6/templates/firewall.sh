ipt6 -A FORWARD -i {{ main_bridge }} -o {{ exit_ipv6_interface }} -j ACCEPT
ipt6 -A FORWARD -o {{ main_bridge }} -i {{ exit_ipv6_interface }} -j ACCEPT
ipt6 -A FORWARD -i {{ main_bridge }} -o {{ main_bridge }} -j ACCEPT
##
# babel interfaces:
##
{% for ifname in babel_interfaces %}
# for interface {{ ifname }}
ipt6 -A FORWARD -i {{ ifname }} -o {{ main_bridge }} -j ACCEPT
ipt6 -A FORWARD -o {{ ifname }} -i {{ main_bridge }} -j ACCEPT
ipt6 -A FORWARD -i {{ ifname }} -o {{ exit_ipv6_interface }} -j ACCEPT
ipt6 -A FORWARD -o {{ ifname }} -i {{ exit_ipv6_interface }} -j ACCEPT
{% if babel_bridge != babel_bridge %}
ipt6 -A FORWARD -i {{ ifname }} -o {{ babel_bridge }} -j ACCEPT
ipt6 -A FORWARD -o {{ ifname }} -i {{ babel_bridge }} -j ACCEPT
{% endif %}
{% endfor %}
