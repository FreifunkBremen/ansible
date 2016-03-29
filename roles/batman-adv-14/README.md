batman-adv-14
=========================

Install batman-adv compat 14 from universe-factory repo


Role Variables
-------------------------

    pgp_keyserver: keyserver for retreiving the repository key (default: 'pgp.surfnet.nl')
    batman-adv-14_repository: (default: 'https://repo.universe-factory.net/debian sid main')
    batman-adv-14_repository_key: (default: '6664E7BDA6B669881EC52E7516EF3F64CB201D9C')
    batman-adv-14_pkg_name: (default: 'batman-adv-dkms')


Usage
-------------------------

    - hosts: servers
      roles:
         - batman-adv-14


License
-------------------------

GPLv3
