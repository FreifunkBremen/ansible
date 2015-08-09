Exit
============

A role to setup up a OpenVPN or GRE connection as exit.


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
