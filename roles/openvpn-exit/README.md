OpenVPN Exit
============

A role to setup up a openvpn connection as exit.



Role Variables
--------------
    openvpn_exit_hideme: Configuration for a default hide.me exit (default:true)
    openvpn_exit_host: Openvpn exit host (required)
    openvpn_exit_username: Username for openvpn auth (required if openvpn_exit_hideme is true)
    openvpn_exit_password: Passwort for openvpn auth (required if openvpn_exit_hideme is true)


Example Playbook
----------------

    - hosts: servers
      roles:
         - openvpn-exit

License
-------

GPLv3
