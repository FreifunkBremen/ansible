backup-webserver
=========================

Sets up backup of entire webserver to remote storage, using Restic.


Usage
-------------------------

    - hosts: servers
      roles:
         - backup-webserver

The backup can be stored on multiple remote hosts.
This role does not specify actual target repositories, though (for privacy reasons).
To add a new backup repository:
- generate a password for the new backup repository, eg. with `pwgen 30 1`
- store the password in a new file on the webserver at eg. /root/backup-examplehost.password
    - make sure the password file is only readable for user root (chmod 400 /root/backup-examplehost.password)
- also, store the password in a secure location outside of the webserver, so the backup is accessible when the webserver is gone
- for backup via SFTP:
    - edit /root/.ssh/config on the webserver and add your target host and its connection settings. Example entry:
```
Host examplehost
Hostname storage.example.org
User my-backup-user
IdentityFile /root/.ssh/id_rsa.ffhb-backup
PasswordAuthentication no
# Restic does not perform any compression, so compress backup data during transfer:
Compression yes
# add this line to avoid frequent SSH warnings if the target host has a dynamic IP:
CheckHostIP no
```
    - add the contents of /root/.ssh/id_rsa.ffhb-backup.pub to the authorized_keys on target storage host
- set up a new Restic repository on the target storage (example path: /data/ffhb/webserver-backup/), using the generated password:
```
restic -r sftp:examplehost:/data/ffhb/webserver-backup/ --password-file=/root/examplehost.password init
```
- add a new executable file in /etc/backup.d/
    - its name must be compatible with run-parts(8) tool, ie. no suffix or special characters
    - the file should contain the actual restic_backup.sh call, like this:
```
#!/bin/sh

/usr/local/bin/restic_backup.sh "sftp:examplehost:/data/ffhb/webserver-backup/" /root/examplehost.password
```
In the next night the backup should be sent to the new storage as well.


Also, you should set up a cronjob on the target storage for periodic maintenance of the backup repository, doing:
- restic prune
- restic forget
- restic check (possibly with --read-data to actually check backup data for corruption)

License
-------------------------

GPLv3
