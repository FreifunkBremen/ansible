Ansible Freifunk Bremen
=======================

In this repository are playbooks for deploying services on Freifunk Bremen machines.

## Dependencies

With PyPI:

    virtualenv pythonenv
    source pythonenv/bin/activate
    pip install -r requirements.txt

Or as Debian/Ubuntu packages:

    apt-get install python-dnspython ca-certificates

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

Hosts:

    vpn0*.bremen.freifunk.net

with exit_ipv4=gre and ansible_ssh_port=* (both optional).

## Gateway Playbook

Playbook vpnserver sets up a Freifunk Bremen gateway. When executed additional variabels need to be defined. For example to set up a Freifunk gateway on vpn05 the following command is used:

    ansible-playbook playbooks/vpnserver.yml --limit=vpn05.bremen.freifunk.net

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


### Add bgp internal routing
Ask to other VPN-Owner to run ansible again.
On this way the other vpns got the new internal routing in ```bird``` and ```bird6```.
[See here](https://github.com/FreifunkBremen/ansible/tree/master/roles/router-bird/templates)
