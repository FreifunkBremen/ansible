#!/usr/bin/env python2
#
# Requirements:
# apt-get install python-unittest2
#
# Run with:
# unit2 discover
#

from sys import path
path.append("..")

import unittest2
import json
import hosts

class TestHosts(unittest2.TestCase):

    def test_starttls_true(self):

        inv = hosts.Inventory('site.conf',
          ipv6_batman_global_network = "2a06:8782:ffbb:1337::/64",
          ipv6_uplink_network = "2a06:8782:ffbb::/64",
          ipv6_batman_local_network = "fd2f:5119:f2c::/64",
          ipv4_icvpn_network  = "10.207.0.196",
          ipv6_icvpn_network  = "fec0::a:cf:0:c4/96",
        )

        grp = inv.group("vpnservers",
          dhcp=True,
          icvpn=True,
          batman_gateway=True,
        )
        grp.host(1, "vpn01.bremen.freifunk.net", exit="gre", ansible_ssh_port=60023)

        grp = inv.group("services")
        grp.host(10, "service.example.com")

        with open('hosts.json') as data_file:
            data = json.load(data_file)

        # print inv.json_dump(indent=4)

        self.assertEqual(data, inv.data())
