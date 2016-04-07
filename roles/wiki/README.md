wiki
=========================

Install gollum
used by Freifunk Bremen
as wiki system


Usage
-------------------------

    - hosts: servers
      roles:
         - wiki


Github SSH Deploy Key
-------------------------
During installation an SSH key will be created for the wiki user.
The key will be created at /home/wiki/.ssh/id_rsa.pub .
It must be added at https://github.com/FreifunkBremen/wiki/settings/keys
as new key (with write access), so that wiki changes can be pushed to Github.


Gollum Logs
-------------------------
Gollum log files are stored in /home/wiki/.config/service/gollum/log/main/.
The "current" file contains the most recent log lines.
To display human-readable timestamps, filter the log file through "tai64nlocal", eg. like this:

  tai64nlocal < current | less


License
-------------------------

GPLv3
