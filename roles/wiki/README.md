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

Gollum Logs
-------------------------
Gollum log files are stored in /home/ffhb-wiki/.config/service/gollum/log/main/.
The "current" file contains the most recent log lines.
To display human-readable timestamps, filter the log file through "tai64nlocal", eg. like this:

  tai64nlocal < current | less


License
-------------------------

GPLv3
