respondd
=========================

Install respondd from git repo with systemd unit


Role Variables
-------------------------

    respondd_git_root: (default: 'https://github.com/FreifunkBremen/respondd/')


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
