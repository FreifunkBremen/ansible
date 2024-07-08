import ipaddress
import json
from slpp import slpp as lua


class Inventory:

    groups = {}

    def __init__(
        self,
        site_conf,
        ipv6_global_network=None,
        ipv6_local_network=None,
        ipv6_uplink_network=None,
    ):

        # read and parse site.conf
        with open(site_conf, 'r') as f:
            self.site = lua.decode(f.read())
            if not isinstance(self.site, dict):
                raise TypeError("Unable to parse site.conf")

        self.ipv4_network = ipaddress.IPv4Network(self.site["prefix4"])
        self.ipv6_uplink_network = ipaddress.IPv6Network(ipv6_uplink_network)
        self.ipv6_global_network = ipaddress.IPv6Network(ipv6_global_network)

        if "prefix6" in self.site:
            self.ipv6_local_network = ipaddress.IPv6Network(self.site["prefix6"])
        else:
            self.ipv6_local_network = ipaddress.IPv6Network(ipv6_local_network)

    def group(self, name, **options):
        group = Group(self, **options)
        self.groups[name] = group
        return group

    def data(self):
        hostvars = {}
        data = {}

        for name, group in self.groups.items():
            data[name] = {
                "hosts":    [hostname for (hostname, _) in group.hosts],
                "children": group.children,
            }
            for (hostname, vars) in group.hosts:
                hostvars[hostname] = vars

        data["_meta"] = {"hostvars": hostvars}
        data["all"] = {"vars": {
            "site":                self.site,
            "site_code":           self.site["site_code"],
            "ipv4_network":        self.attributeString("ipv4_network"),
            "ipv6_local_network":  self.attributeString("ipv6_local_network"),
            "ipv6_uplink_network": self.attributeString("ipv6_uplink_network"),
            "ipv6_global_network": self.attributeString("ipv6_global_network"),
        }}

        return data

    def json_dump(self, **kwargs):
        return json.dumps(self.data(), **kwargs)

    def attributeString(self, key):
        value = getattr(self, key, None)
        if value is not None:
            value = str(value)
        return value

    def calculate_address(self, key, incr):
        try:
            origin = getattr(self, key)
        except AttributeError:
            return

        address = origin[incr]
        return {
            "address": str(address),
            "netmask": str(origin.netmask),
            "size":    origin.prefixlen,
        }


class Group:
    def __init__(self, inventory, dhcp=False, **vars):
        self.inventory = inventory
        self.dhcp = dhcp
        self.vars = vars
        self.hosts = []
        self.children = []

    def host(self, id, hostname, **host_vars):
        vars = self.vars.copy()
        vars.update(host_vars)
        vars.update({
            "vpn_id":             id,
            "batman_ipv4":        self.calculate_address("ipv4_network", id),
            "batman_ipv6_global": self.calculate_address("ipv6_global_network", id),
            "batman_ipv6_local":  self.calculate_address("ipv6_local_network", id),
        })

        if self.dhcp:
            begin = self.inventory.ipv4_network[(id << 8)*10]
            vars["dhcp"] = {
                "netmask":     str(self.inventory.ipv4_network.netmask),
                "range_begin": str(ipaddress.IPv4Address(begin)),
                "range_end":   str(ipaddress.IPv4Address(begin + 256 * 10 - 1)),
            }

        self.hosts.append((hostname, vars))

    def calculate_address(self, *args):
        return self.inventory.calculate_address(*args)

    def child(self, child):
        self.children.append(child)
