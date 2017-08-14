#
# You need a recent version of ipcalc. On Debian/Ubuntu you can install it with:
# sudo apt-get install python-pip
# sudo pip install ipcalc
#

import copy
import ipcalc
import json
import sys
from slpp import slpp as lua

if ipcalc.__version__.startswith("0.5."):
  sys.stderr.write("ipcalc 0.5 ist zu alt, nutze pip es zu aktualisieren (z.B. pip install --upgrade ipcalc)")
  sys.exit(1)

class Inventory:

  groups = {}

  def __init__(self, site_conf, ipv6_batman_global_network=None, ipv6_batman_local_network=None, ipv6_babel_client_network=None, ipv6_uplink_network=None, ipv4_icvpn_network=None, ipv6_icvpn_network=None):

    # read and parse site.conf
    with open(site_conf,'r') as f:
      self.site = lua.decode(f.read())
      if not isinstance(self.site, dict):
        raise TypeError("Unable to parse site.conf")

    self.ipv4_icvpn_network  = ipcalc.Network(ipv4_icvpn_network)
    self.ipv6_icvpn_network  = ipcalc.Network(ipv6_icvpn_network)

    self.ipv4_network        = ipcalc.Network(self.site["prefix4"])

    if "prefix6" in self.site:
      self.ipv6_babel_client_network = ipcalc.Network(self.site["prefix6"])
    else:
      self.ipv6_babel_client_network  = ipcalc.Network(ipv6_babel_client_network)

    self.ipv6_batman_global_network = ipcalc.Network(ipv6_batman_global_network)
    self.ipv6_uplink_network = ipcalc.Network(ipv6_uplink_network)


    if "node_prefix6" in self.site:
      self.ipv6_babel_node_network = ipcalc.Network(self.site["node_prefix6"])
    if ipv6_batman_local_network is not None:
      self.ipv6_batman_local_network = ipcalc.Network(ipv6_batman_local_network)

  def group(self, name, **options):
    group = Group(self, **options)
    self.groups[name] = group
    return group

  def data(self):
    hostvars = {}
    data     = {}

    for name, group in self.groups.items():
      data[name] = {
        "hosts":    [hostname for (hostname,_) in group.hosts],
        "children": group.children,
      }
      for (hostname,vars) in group.hosts:
        hostvars[hostname] = vars

    data["_meta"] = {"hostvars": hostvars}
    data["all"]   = {"vars": {
      "site":                self.site,
      "site_code":           self.site["site_code"],
      "ipv4_network":        self.attributeString("ipv4_network"),
      "ipv6_babel_client_network":  self.attributeString("ipv6_babel_client_network"),
      "ipv6_batman_global_network": self.attributeString("ipv6_batman_global_network"),
      "ipv6_uplink_network": self.attributeString("ipv6_uplink_network"),
      "ipv6_babel_node_network":  self.attributeString("ipv6_babel_node_network"),
      "ipv6_batman_local_network": self.attributeString("ipv6_batman_local_network"),
    }}

    return data

  def json_dump(self, **kwargs):
    return json.dumps(self.data(), **kwargs)

  def attributeString(self, key):
    value = getattr(self, key, None)
    if value != None:
      value = str(value)
    return value

  def calculate_address(self, key, incr):
    try:
      origin = getattr(self, key)
    except AttributeError:
      return

    address = ipcalc.IP(origin.ip + incr)
    return {
      "address": str(address.to_compressed() if origin.v==6 else address),
      "netmask": str(origin.netmask()),
      "size":    origin.subnet(),
    }

class Group:
  def __init__(self, inventory, dhcp=False, icvpn=False, **vars):
    self.inventory = inventory
    self.dhcp      = dhcp
    self.icvpn     = icvpn
    self.vars      = vars
    self.hosts     = []
    self.children  = []

  def host(self, id, hostname, **host_vars):
    vars = self.vars.copy()
    vars.update(host_vars)
    vars.update({
      "vpn_id":      id,
      "ipv4":        self.calculate_address("ipv4_network", id),
      "ipv6_babel_client":  self.calculate_address("ipv6_babel_client_network", id),
      "ipv6_batman_global": self.calculate_address("ipv6_batman_global_network", id),
      "ipv6_babel_node":  self.calculate_address("ipv6_babel_node_network", id),
      "ipv6_batman_local": self.calculate_address("ipv6_batman_local_network", id),
    })

    if self.dhcp:
      begin = self.inventory.ipv4_network.ip + (id << 8)*10
      vars["dhcp"] = {
        "netmask":     str(self.inventory.ipv4_network.netmask()),
        "range_begin": str(ipcalc.IP(begin)),
        "range_end":   str(ipcalc.IP(begin+256*10-1)),
      }

    if self.icvpn:
      vars["ipv4_icvpn"] = self.calculate_address("ipv4_icvpn_network", (id << 8))
      vars["ipv6_icvpn"] = self.calculate_address("ipv6_icvpn_network", (id << 16))

    vars["ipv6_uplink_own_gateway"] = self.calculate_address("ipv6_uplink_network", (id << 16*4)+1)
    vars["ipv6_uplink_own_vpnserver"] = self.calculate_address("ipv6_uplink_network", (id << 16*4)+2)

    self.hosts.append((hostname, vars))

  def calculate_address(self, *args):
    return self.inventory.calculate_address(*args)

  def child(self, child):
    self.children.append(child)
