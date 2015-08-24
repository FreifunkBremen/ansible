Ansible Freifunk Bremen
=======================

In this repository are playbooks for deploying services on Freifunk Bremen machines.

### Playbooks

    serviceserver-jabber
    serviceserver-omd
    serviceserver-web
    vpnserver

Playbooks serviceserver* set up 3rd party services on machines defined in hosts. Playbook vpnserver sets up a Freifunk Bremen gateway.

### Site-Conf

Community related variables are defined in `site/site.conf` and `group_vars/all.yml`.
This variables are used by the ansible-tasks.

    pgp_keyserver:        'pool.sks-keyservers.net'
    site_git_root:        'https://github.com/FreifunkBremen'
    site_city:            'bremen'
    site_domain:          'bremen.freifunk.net'
    site_vpn_prefix:      'vpn'
    icvpn_as:             65196
    fastd_peers_limit:    150

Other communities need to modify this variables.

### Hosts

The hosts-file defines all machines where our services are deployed on as well as community related variables. For other communities the variables are to be changed.
Variables:

    ipv6_network_alt   = "2001:bf7:540::/64",
    icvpn_ipv4_network = "10.207.0.196",
    icvpn_ipv6_network = "fec0::a:cf:0:c4/96",

Hosts:

    vpn0*.bremen.freifunk.net

with exit=openvpn/gre and ansible_ssh_port=* (both optional).

### Gateway Playbook

Playbook vpnserver sets up a Freifunk Bremen gateway. When executed additional variabels need to be defined. For example to set up a Freifunk gateway on vpn05 the following command is used:

    ansible-playbook playbooks/vpnserver.yml --limit=vpn05.bremen.freifunk.net -e "exit_openvpn_username=* exit_openvpn_password=* exit_openvpn_host=* exit=openvpn"

Username, host and password can be found by your exit-vpn provider.

The following roles are excecuted in the playbook vpnserver:

    common
    batman-adv-14
    fastd
    alfred-announce
    icvpn
    ipv6-exit
    ntp-chrony
    exit
    dns-unbound
    dhcp-dnsmasq
    system

For detailed information about the roles see README.md inside of the role.
