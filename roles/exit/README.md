Exit
============

A role to setup up a OpenVPN, GRE or IPIP connection as exit.


Role Variables
--------------

### GRE Exit

    exit: gre
    exit_gre_interface: Interface name
    exit_gre_address
    exit_gre_address_global
    exit_gre_address_peer
    exit_gre_local
    exit_gre_remote

### IPIP Exit

    exit: ipip
    exit_ipip_interface: Interface name
    exit_ipip_address
    exit_ipip_address_global
    exit_ipip_address_peer
    exit_ipip_local
    exit_ipip_remote

### OpenVPN Exit

    exit: openvpn
    exit_openvpn_host: Openvpn exit host (required)
    exit_openvpn_username: Username for openvpn auth
    exit_openvpn_password: Passwort for openvpn auth


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: exit, exit: "gre" }

License
-------

GPLv3
