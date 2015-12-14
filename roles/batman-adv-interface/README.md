batman-adv-interface
=========================

Install the batman interface


Role Variables
-------------------------

    batman_interface: Interface on which works Batman (default: 'bat-{{ site_code }}' )


Usage
-------------------------

    - hosts: servers
      vars:
        site_code: ffhb
      roles:
         - batman-adv-interface


License
-------------------------

GPLv3
