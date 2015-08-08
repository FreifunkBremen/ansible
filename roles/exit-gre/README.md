GRE exit
============

A role to setup up a GRE connection as exit.



Role Variables
--------------
    gre_exit_hideme: Configuration for a default hide.me exit (default:true)
    gre_exit_host: Openvpn exit host (required)
    gre_exit_username: Username for openvpn auth (required if gre_exit_hideme is true)
    gre_exit_password: Passwort for openvpn auth (required if gre_exit_hideme is true)


Example Playbook
----------------

    - hosts: servers
      roles:
         - exit-gre

License
-------

GPLv3
