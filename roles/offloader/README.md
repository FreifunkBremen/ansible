Offloader
============

A role to setup up a OpenVPN-server as offloader service.


Role Variables
--------------

### OpenVPN Offloader

    offloader: openvpn


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: offloader, offloader: "openvpn" }

License
-------

GPLv3
