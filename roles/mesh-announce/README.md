respondd
=========================

Install respondd from git repo with systemd unit


Role Variables
-------------------------

    respondd_announce_git_root: (default: 'https://github.com/ffnord/ffnord-alfred-announce/')


Usage
-------------------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - respondd

License
-------------------------

GPLv3
