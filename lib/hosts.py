#
# You need a recent version of ipcalc. On Debian/Ubuntu you can install it with:
# sudo apt-get install python-pip
# sudo pip install ipcalc
#

import ipcalc
import json


class Inventory:

  groups = {}

  def __init__(self, ipv4_network=None, ipv6_network=None, ipv6_network_alt=None, icvpn_ipv4_network=None, icvpn_ipv6_network=None):
    self.ipv4_network       = ipcalc.Network(ipv4_network)
    self.ipv6_network       = ipcalc.Network(ipv6_network)
    self.ipv6_network_alt   = ipcalc.Network(ipv6_network_alt)
    self.icvpn_ipv4_network = ipcalc.Network(icvpn_ipv4_network)
    self.icvpn_ipv6_network = ipcalc.Network(icvpn_ipv6_network)

  def group(self, name, **options):
    group = Group(self, **options)
    self.groups[name] = group
    return group

  def json_dump(self):
    hostvars = {}
    data     = {}

    for name, group in self.groups.items():
      data[name] = [hostname for (hostname,_) in group.hosts]
      for (hostname,vars) in group.hosts:
        hostvars[hostname] = vars

    data["_meta"] = {"hostvars": hostvars}
    return json.dumps(data, indent=4)

  def calculate_address(self, key, incr):
    origin  = getattr(self, key, incr)
    address = ipcalc.IP(origin.ip + incr)
    return {
      "address": str(address.to_compressed() if origin.v==6 else address),
      "netmask": str(origin.netmask()),
      "size":    origin.subnet(),
    }

class Group:
  def __init__(self, inventory, dhcp=False, icvpn=False):
    self.inventory = inventory
    self.dhcp      = dhcp
    self.icvpn     = icvpn
    self.hosts     = []

  def host(self, id, hostname, port=None):
    vars = {
      "vpn_id":          id,
      "batman_ipv4":     self.calculate_address("ipv4_network", id),
      "batman_ipv6":     self.calculate_address("ipv6_network", id),
      "batman_ipv6_alt": self.calculate_address("ipv6_network_alt", id),
    }

    if port != None:
      vars["ansible_ssh_port"] = port

    if self.dhcp:
      begin = self.inventory.ipv4_network.ip + (id << 8)*10
      vars["dhcp"] = {
        "netmask":     str(self.inventory.ipv4_network.netmask()),
        "range_begin": str(ipcalc.IP(begin)),
        "range_end":   str(ipcalc.IP(begin+255)),
      }

    if self.icvpn:
      vars["icvpn_ipv4"] = self.calculate_address("icvpn_ipv4_network", (id << 8))
      vars["icvpn_ipv6"] = self.calculate_address("icvpn_ipv6_network", (id << 16))

    self.hosts.append((hostname, vars))

  def calculate_address(self, *args):
    return self.inventory.calculate_address(*args)
