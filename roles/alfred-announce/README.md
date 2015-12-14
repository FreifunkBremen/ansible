alfred-announce
=========================

Install alfred-announce from git repo as cronjob


Role Variables
-------------------------

    alfred_announce_git_root: (default: 'https://github.com/genofire/alfred-announce/')
    batman_interface: Interface on which works Batman (default: 'bat-{{ site_code }}' )
    main_bridge: Interface on which Listen Batman Nodes(default:'br-{{ site_code }}' )


Usage
-------------------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - alfred-announce

License
-------------------------

GPLv3
