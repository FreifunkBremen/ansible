#! /usr/bin/env python3

import sys
import json
import re
import ipaddress
import socket
from urllib.request import urlopen
from time import time
from textwrap import dedent


def str_to_domainlabel(s):
    label = re.sub("[^0-9a-zA-Z-]+", "-", s)
    label = re.sub("^-|-$", "", label)

    if not re.match("^[a-zA-Z][a-zA-Z0-9-]{,61}[a-zA-Z0-9]$", label):
        raise RuntimeError("Not convertable to a domain label: {}".format(s))

    return label


def ipnetwork_reverse_pointer(net):
    if net.prefixlen % 4:
        raise RuntimeError(
            'Cannot generate reverse pointer for network with prefixlen not '
            'divisible by 8: {}'.format(net.compressed))
    return net.network_address.reverse_pointer[int((128-net.prefixlen)/2):]


def get_zone(
        data,
        reverse=False,
        prefix=None,
        nservers=None,
        contact=None,
        refresh='1h',
        retry='30m',
        expire='2d',
        ttl='1h'):

    if not nservers:
        nservers = [socket.getfqdn()]

    zone = dedent("""\
    $TTL {ttl}
    @       IN              SOA     {nservers[0]}. {contact}. (
                                        {serial:.0f} ; serial
                                        {refresh} ; refresh
                                        {retry} ; retry
                                        {expire} ; expire
                                        {ttl} ; ttl
                                    )
    """.format(
        nservers=nservers,
        contact=contact if contact else 'root.{}'.format(nservers[0]),
        refresh=refresh,
        retry=retry,
        expire=expire,
        ttl=ttl,
        serial=time(),
    ))

    for nserver in nservers:
        zone += "{:>26}      {}.\n".format("NS", nserver)
    zone += "\n"

    for node in data['nodes'].values():
        try:
            label = str_to_domainlabel(node['nodeinfo']['hostname'])
            addresses = iter(node['nodeinfo']['network']['addresses'])
        except (RuntimeError, KeyError, TypeError):
            continue

        for address in addresses:
            try:
                address = ipaddress.IPv6Address(address)
            except ValueError:
                continue

            if prefix:
                if address not in prefix:
                    continue
            elif not address.is_global:
                continue

            if reverse:
                rdns = address.reverse_pointer
                if not prefix:
                    rdns += '.'
                else:
                    # truncate network part of reverse pointer address
                    rdns = rdns[:-len(ipnetwork_reverse_pointer(prefix))-1]
                zone += "{} PTR {}.{}\n".format(rdns, label, reverse)
            else:
                zone += "{:<23} AAAA    {}\n".format(label, address)
    return zone


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(
        description="Generate DNS zone file with all nodes' AAAA records",
        usage="%(prog)s URL [options]",
        argument_default=argparse.SUPPRESS)
    p.add_argument('url', metavar='URL', help='''
                   URL to the nodes.json, in meshviewer API v1 format''')

    p.add_argument('--nservers', metavar='SERVER', nargs='+', help='''
                   Nameservers responsible for this zone; the first nameserver
                   specified will also be entered in the SOA as master
                   (default: FQDN of this machine)''')
    p.add_argument('--contact', help='''
                   Contact for the SOA record, with the @ replaced by .
                   (default: root.the_first_nserver)''')
    p.add_argument('--file', default=None, help='''
                   File to write the final zone to when finished. This is
                   better than output redirection because the file is only
                   opened (and thus truncated) when generation has succeeded.
                   (default: output to stdout)''')
    p.add_argument('--prefix', type=ipaddress.IPv6Network, help='''
                   Consider only addresses from this prefix
                   (default: all global addresses)''')
    p.add_argument('--reverse', metavar='DOMAIN', help='''
                   Generate reverse zone instead, with the node names being
                   under DOMAIN. You should probably specify a PREFIX as
                   well''')

    group = p.add_argument_group(
        'expert arguments',
        'These settings probably already have sensible defaults')
    group.add_argument('--refresh', help='Refresh value for the SOA record')
    group.add_argument('--retry', help='Retry value for the SOA record')
    group.add_argument('--expire', help='Expire value for the SOA record')
    group.add_argument('--ttl', help='TTL for the zone')
    args = p.parse_args()

    with urlopen(args.url) as f:
        data = json.loads(f.read().decode('utf-8'))
    func_args = dict(vars(args))
    del func_args['file'], func_args['url']
    zone = get_zone(data, **func_args)

    try:
        # check zone if we have dnspython installed
        import dns.zone
        dns.zone.from_text(zone, origin='nodes.example.freifunk.net')
    except ImportError:
        pass

    if args.file:
        with open(args.file, 'w') as f:
            f.write(zone)
    else:
        sys.stdout.write(zone)
