firewall
=========================

Configure firewall


Role Variables
-------------------------

    icvpn_interface: 'icvpn'
    batman_interface: 'bat-{{ site_code }}'
    alfred_mtu_interface: 'br-{{ site_code }}-mtu'
    main_bridge: 'br-{{ site_code }}'
    fastd_interface: vpn-{{ site_code }}

`exit_ipv4_interface` must be set if the `exit_ipv4` role is not included in the playbook.


Usage
-------------------------

    - hosts: servers
      roles:
         - firewall


License
-------------------------

GPLv3
