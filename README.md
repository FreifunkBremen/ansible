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
    icvpn_ipv4_network  = "10.207.0.196/16",
    icvpn_ipv6_network  = "fec0::a:cf:0:c4/96",

Hosts:

    vpn0*.bremen.freifunk.net

with exit_ipv4=gre and ansible_ssh_port=* (both optional).

## Gateway Playbook

Playbook vpnserver sets up a Freifunk Bremen gateway. When executed additional variabels need to be defined. For example to set up a Freifunk gateway on vpn05 the following command is used:

    ansible-playbook playbooks/vpnserver.yml --limit=vpn05.bremen.freifunk.net -e "exit_ipv6_remote=*"

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


## Babel

**NAT64**

if installed nat64 maybe extends port pool by reconfigure local range `sysctl net.ipv4.ip_local_port_range`

Or use other address-pool (and firewall)  `/etc/systemd/system/jool.service`:
```
...
ExecStart=/usr/local/bin/jool instance add --iptables --pool6=64:ff9b::/96
ExecStartPost=/usr/local/bin/jool pool4 add --icmp 185.117.213.250 1601-3000
ExecStartPost=/usr/local/bin/jool pool4 add --udp  185.117.213.250 3001-65535
ExecStartPost=/usr/local/bin/jool pool4 add --tcp  185.117.213.250 1601-65535
...
```


### Babel Gateway
A babel gateway is a maschine which allow to exit ipv6 default route and recieve the client and nodes subnet

Such a gateway need some special configuration.
- (A bigger nat64 whould be nice)
- ip routes for exit
	- `post-up  ip -r r add default via 2a06:8782:ff00::1 dev $IFACE proto 159 table default-freifunk`
	- firewall rules /etc/firewall.d/20-exit 
		```
		ipt6 -A FORWARD -o ens3 -i babel-+ -j ACCEPT
		ipt6 -A FORWARD -i ens3 -o babel-+ -j ACCEPT
		```

- maybe run yanic to collect and forward stats data
	- firewall for respondd
	- firewall for yanic
- tunnel to babel vpn
	- add to /etc/babeld.conf
	- to /etc/systemd/system/mmfd.service

### Babel VPN
A babel vpn is a maschine which recieve VPN connection and "forward" them to a gateway.
It could run nat64 at his own and exit ipv4.

TODO: respondd firewall:
```
# babel
ipt6 -A INPUT -i babel-+ -p udp --dport 1001 -j ACCEPT
ipt6 -A INPUT -i mmfd0 -p udp --dport 1001 -j ACCEPT
```

