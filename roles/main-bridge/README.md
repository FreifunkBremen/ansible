main-bridge
=========================

Install the bridge for Freifunk Bremen VPN gateways


Role Variables
-------------------------

    ffhb_routing_table: Routing table for default gateway via VPN and ICVPN (default: default-freifunk)
    batman_interface: Interface on which works Batman (default: 'bat-{{ site_code }}' )


Usage
-------------------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - main-bridge


License
-------------------------

GPLv3
