Exit
============

A role to setup up a OpenVPN, GRE or IPIP connection as exit.


Role Variables
--------------

### GRE or IPIP Exit

    exit: Tunnel mode (GRE or IPIP)
    exit_address
    exit_address_global
    exit_address_peer
    exit_local
    exit_remote

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
