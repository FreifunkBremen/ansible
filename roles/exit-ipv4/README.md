exit-ipv4
=========================

A role to setup up a OpenVPN, GRE or IPIP connection as exit.


Role Variables
------------------------

### GRE or IPIP Exit

    exit_ipv4: Tunnel mode (GRE or IPIP)
    exit_ipv4_address
    exit_ipv4_address_global
    exit_ipv4_address_peer
    exit_ipv4_local
    exit_ipv4_remote

### default (dangerous)

Be aware of the german "Störerhaftung"!

    exit_ipv4: default


Usage
------------------------

    - hosts: servers
      roles:
         - { role: exit-ipv4, exit_ipv4: "gre" }


License
------------------------

GPLv3
