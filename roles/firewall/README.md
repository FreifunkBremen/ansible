Role Name
=========

Configure firewall



Role Variables
--------------

    icvpn_interface: 'icvpn'
    batman_interface: 'bat-{{ site_code }}'
    batman_mtu_interface: 'bat-{{ site_code }}_dummy'
    alfred_interface: 'br-{{ site_code }}'
    fastd_interface: vpn-{{ site_code }}

`exit_interface` must be set if the `exit` role is not included in the playbook.

Example Playbook
----------------

    - hosts: servers
      roles:
         - firewall

License
-------

GPLv3
