respondd
=========================

Install respondd from git repo with systemd unit and alfred to announce informations


Role Variables
-------------------------

   mesh_announce_git_root: (default: 'https://github.com/ffnord/mesh-announce/')


Usage
-------------------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - mesh-announce

License
-------------------------

GPLv3
