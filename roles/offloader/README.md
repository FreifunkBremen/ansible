Offloader
============

A role to setup up a OpenVPN-server as offloader service.


Role Variables
--------------

### OpenVPN Offloader

    offload: openvpn


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: offloader, offload: "openvpn" }

License
-------

GPLv3
