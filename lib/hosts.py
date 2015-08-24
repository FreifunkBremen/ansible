#
# You need a recent version of ipcalc. On Debian/Ubuntu you can install it with:
# sudo apt-get install python-pip
# sudo pip install ipcalc
#

import ipcalc
import json
from slpp import slpp as lua

class Inventory:

  groups = {}

  def __init__(self, site_conf, ipv6_local_network=None, icvpn_ipv4_network=None, icvpn_ipv6_network=None):

    # read and parse site.conf
    with open(site_conf,'r') as f:
      self.site = lua.decode(f.read())
      if not isinstance(self.site, dict):
        raise TypeError("Unable to parse site.conf")

    self.ipv4_network        = ipcalc.Network(self.site["prefix4"])
    self.icvpn_ipv4_network  = ipcalc.Network(icvpn_ipv4_network)
    self.icvpn_ipv6_network  = ipcalc.Network(icvpn_ipv6_network)
    self.ipv6_local_network  = ipcalc.Network(ipv6_local_network)

    if "prefix6" in self.site:
      self.ipv6_global_network = ipcalc.Network(self.site["prefix6"])

  def group(self, name, **options):
    group = Group(self, **options)
    self.groups[name] = group
    return group

  def json_dump(self, **kwargs):
    hostvars = {}
    data     = {}

    for name, group in self.groups.items():
      data[name] = [hostname for (hostname,_) in group.hosts]
      for (hostname,vars) in group.hosts:
        hostvars[hostname] = vars

    data["_meta"] = {"hostvars": hostvars}
    data["all"]   = {"vars": {
      "site":                self.site,
      "site_code":           self.site["site_code"],
      "ipv4_network":        self.attributeString("ipv4_network"),
      "ipv6_local_network":  self.attributeString("ipv6_local_network"),
      "ipv6_global_network": self.attributeString("ipv6_global_network"),
    }}

    return json.dumps(data, **kwargs)

  def attributeString(self, key):
    value = getattr(self, key, None)
    if value != None:
      value = str(value)
    return value

  def calculate_address(self, key, incr):
    try:
      origin  = getattr(self, key)
    except AttributeError:
      return
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

  def host(self, id, hostname, **vars):
    vars.update({
      "vpn_id":             id,
      "batman_ipv4":        self.calculate_address("ipv4_network", id),
      "batman_ipv6_global": self.calculate_address("ipv6_global_network", id),
      "batman_ipv6_local":  self.calculate_address("ipv6_local_network", id),
    })

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
