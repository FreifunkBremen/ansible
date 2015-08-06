#
# You need a recent version of ipcalc. On Debian/Ubuntu you can install it with:
# sudo apt-get install python-pip
# sudo pip install ipcalc
#

import ipcalc
import json

class Inventory:

  groups = {}

  def __init__(self, ipv4_network=None, ipv6_network=None, ipv6_network_alt=None ):
    self.ipv4_network     = ipcalc.Network(ipv4_network)
    self.ipv6_network     = ipcalc.Network(ipv6_network)
    self.ipv6_network_alt = ipcalc.Network(ipv6_network_alt)

  def group(self, group, *hosts):
    self.groups[group] = list(hosts)

  def host(self, id, hostname, port=None):
    vars = {}

    if port != None:
      vars["ansible_ssh_port"] = port

    vars["dhcp_subnetmask"]         = str(self.ipv4_network.netmask())
    vars["dhcp_range_begin"]        = str(ipcalc.IP(self.ipv4_network.ip+id*256*10))
    vars["dhcp_range_end"]          = str(ipcalc.IP(self.ipv4_network.ip+id*256*10+255))
    vars["batman_ipv4_address"]     = str(ipcalc.IP(self.ipv4_network.ip+id))
    vars["batman_ipv6_address"]     = str(ipcalc.IP(self.ipv6_network.ip+id).to_compressed())
    vars["batman_ipv6_address_alt"] = str(ipcalc.IP(self.ipv6_network_alt.ip+id).to_compressed())

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
