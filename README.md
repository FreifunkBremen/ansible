Ansible Freifunk Bremen
=======================

In this repository are playbooks for deploying services on Freifunk Bremen machines.

## Dependencies

    apt-get install python-dnspython

## Playbooks

  * services: Generic service host for Freifunk Bremen community.
  * vpnserver: vpnserver sets up a Freifunk Bremen gateway.

## Site-Conf

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

## Hosts

The hosts-file defines all machines where our services are deployed on as well as community related variables. For other communities the variables are to be changed.
Variables:

    ipv6_local_network  = "fd75:3707:b8c2::/64",
    icvpn_ipv4_network  = "10.207.0.196/16",
    icvpn_ipv6_network  = "fec0::a:cf:0:c4/96",

Hosts:

    vpn0*.bremen.freifunk.net

with exit_ipv4=openvpn/gre and ansible_ssh_port=* (both optional).

## Gateway Playbook

Playbook vpnserver sets up a Freifunk Bremen gateway. When executed additional variabels need to be defined. For example to set up a Freifunk gateway on vpn05 the following command is used:

    ansible-playbook playbooks/vpnserver.yml --limit=vpn05.bremen.freifunk.net -e "exit_ipv4_openvpn_username=* exit_ipv4_openvpn_password=*"

Username, host and password can be found by your exit-vpn provider.

The following roles are excecuted in the playbook vpnserver:

    common
    batman-adv-14
    fastd
    alfred-announce
    icvpn
    exit-ipv4
    exit-ipv6
    chrony
    unbound
    dnsmasq
    system

For detailed information about the roles see README.md inside of the role.


## Afterwork
After setting up a vpnserver you have to do something by hand.

### Create DNS-Entries
In Bremen you need a VPN-Entry and NTP-Entry.

### Add fastd-public-key to site.confg
You got your key from running
```
fastd --show-key -c /etc/fastd/{{site_code}}/fastd.conf
```
Then add it to your site.conf - From Bremen you found it [here](https://github.com/FreifunkBremen/gluon-site-ffhb/blob/master/site.conf)

**Do not forget to add NTP-Server either.**

### Add vpn to icvpn
Publish your tinc Public-key to [IC-VPN](https://github.com/freifunk/icvpn).
Your found your one /etc/tinc/icvpn/hosts/{{site_city}}{{id}}.
So other IC-VPN-Servers could create a vpn-Connection to your VPN.


### Add vpn to icvpn-meta
Add your new VPN to the [IC-VPN-Meta](https://github.com/freifunk/icvpn-meta) to get the bgp routing active on other Host from other communitys.

### Add bgp internal routing
Ask to other VPN-Owner to run ansible again.
On this way the other vpns got the new internal routing in ```bird``` and ```bird6```.
[See here](https://github.com/FreifunkBremen/ansible/tree/master/roles/router-bird/templates)
