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

  def group(self, group, *hosts):
    self.groups[group] = list(hosts)

  def host(self, id, hostname, port=None):
    vars = {}

    if port != None:
      vars["ansible_ssh_port"] = port

    vars["dhcp"] = {
      "netmask":     str(self.ipv4_network.netmask()),
      "range_begin": str(ipcalc.IP(self.ipv4_network.ip+id*256*10)),
      "range_end":   str(ipcalc.IP(self.ipv4_network.ip+id*256*10+255)),
    }
    vars["batman_ipv4"] = {
      "address": str(ipcalc.IP(self.ipv4_network.ip+id)),
      "netmask": str(self.ipv4_network.netmask()),
    }
    vars["batman_ipv6"] = {
      "address": str(ipcalc.IP(self.ipv6_network.ip+id).to_compressed()),
    }
    vars["batman_ipv6_alt"] = {
      "address": str(ipcalc.IP(self.ipv6_network_alt.ip+id).to_compressed()),
    }
    vars["icvpn_ipv4"] = {
      "address": str(ipcalc.IP(self.icvpn_ipv4_network.ip + (id << 8))),
      "netmask": str(self.icvpn_ipv4_network.netmask()),
    }
    vars["icvpn_ipv6"] = {
      "address": str(ipcalc.IP(self.icvpn_ipv6_network.ip + (id << 16)).to_compressed()),
      "size":    self.icvpn_ipv6_network.subnet(),
    }

    return (hostname, vars)

  def json_dump(self):
    hostvars = {}
    data     = {}

    for group, hosts in self.groups.items():
      data[group] = [hostname for (hostname,_) in hosts]
      for (hostname,vars) in hosts:
        hostvars[hostname] = vars

    data["_meta"] = {"hostvars": hostvars}
    return json.dumps(data, indent=4)
