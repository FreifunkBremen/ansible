fastd
=========================

Install fastd


Configuration
-------------------------

This role creates three instances of fastd:

* `/etc/fastd/{{ site_code }}` listening on port 50000 (IPv4 and IPv6)
* `/etc/fastd/{{ site_code }}-legacy` listening on port 10000 (IPv4 only)
* `/etc/fastd/{{ site_code }}-backbone` listening on port 50001 (IPv4 and IPv6) for only known peers


Usage
-------------------------

    - hosts: servers
      roles:
         - fastd


License
-------------------------

GPLv3
