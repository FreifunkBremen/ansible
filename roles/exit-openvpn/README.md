OpenVPN Exit
============

A role to setup up a openvpn connection as exit.



Role Variables
--------------
    exit_openvpn_hideme: Configuration for a default hide.me exit (default:true)
    exit_openvpn_host: Openvpn exit host (required)
    exit_openvpn_username: Username for openvpn auth (required if exit_openvpn_hideme is true)
    exit_openvpn_password: Passwort for openvpn auth (required if exit_openvpn_hideme is true)


Example Playbook
----------------

    - hosts: servers
      roles:
         - exit-openvpn

License
-------

GPLv3
