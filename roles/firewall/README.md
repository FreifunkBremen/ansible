Role Name
=========

Configure firewall



Role Variables
--------------

    icvpn_interface: 'icvpn'
    batman_interface: 'bat-{{ site_code }}'
    alfred_mtu_interface: 'br-{{ site_code }}-mtu'
    main_bridge: 'br-{{ site_code }}'
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
