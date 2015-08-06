#
# You need a recent version of ipcalc. On Debian/Ubuntu you can install it with:
# sudo apt-get install python-pip
# sudo pip install ipcalc
#

import ipcalc
import json

class Inventory:

  hostnames = []
  hostvars  = {}

  def __init__(self, group, ipv4_network=None, ipv6_network=None, ipv6_network_alt=None ):
    self.data  = []
    self.group = group

    self.ipv4_network     = ipcalc.Network(ipv4_network)
    self.ipv6_network     = ipcalc.Network(ipv6_network)
    self.ipv6_network_alt = ipcalc.Network(ipv6_network_alt)

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

    self.hostnames.append(hostname)
    self.hostvars[hostname] = vars

  def json_dump(self):
    return json.dumps(
      {
        self.group: self.hostnames,
        "_meta": {"hostvars": self.hostvars}
      },
      indent=4,
    )
