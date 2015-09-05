Role Name
=========

Install alfred-announce from git repo as cronjob


Role Variables
--------------

    alfred_announce_git_root: (default: 'https://github.com/genofire/alfred-announce/')
    batman_interface: Interface on which works Batman (default: 'bat-{{ site_code }}' )
    alfred_interface: Interface on which Listen Batman Nodes(default:'br-{{ site_code }}' )


Example Playbook
----------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - alfred-announce

License
-------

GPLv3
