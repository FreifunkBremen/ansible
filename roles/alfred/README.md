Role Name
=========

Install alfred from debian.draic.info repo


Role Variables
--------------

    alfred_repository: (default: 'http://debian.draic.info/ wheezy main')
    alfred_master: Start Alfred-Daemon on Mastermode (default false)
    batman_interface: Interface on which works Batman (default: 'bat-{{ site_code }}' )
    main_bridge: Interface on which Listen Batman Nodes(default:'br-{{ site_code }}' )


Example Playbook
----------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - alfred

License
-------

GPLv3
