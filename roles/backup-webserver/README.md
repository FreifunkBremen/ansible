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
    - make sure the password file is only readable for user root (`chmod 400 /root/backup-examplehost.password`)
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
#! /usr/bin/env bash

/usr/local/bin/restic_backup.sh "sftp:examplehost:/data/ffhb/webserver-backup/" /root/examplehost.password
```
In the next night the backup should be sent to the new storage as well.


Also, you should set up a cronjob on the target storage for periodic maintenance of the backup repository, doing:
- `restic prune`
- `restic forget`
- `restic check` (possibly with `--read-data` to actually check backup data for corruption)


## Accessing Backups (using a shell on examplehost):
- list snapshots: `restic -r /data/ffhb/webserver-backup/ snapshots`
- view files in latest snapshot: `restic -r /data/ffhb/webserver-backup/ ls latest`
- restore /home/downloads/ directory from latest snapshot: `restic -r /data/ffhb/webserver-backup/ restore latest -i /home/downloads/ -t ~/ffhb-restore-1/`

Use the `--no-lock` parameter for restic if the repository is read-only.


## Inspecting old InfluxDB data
- restore /var/backups/influxdb/ from backup, eg. to ~/ffhb-restore-1/: `restic -r /data/ffhb/webserver-backup/ restore latest -i /var/backups/influxdb/ -t ~/ffhb-restore-1/`
- install InfluxDB and Chronograf, as described at https://portal.influxdata.com/downloads:
```
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.7.1-static_linux_amd64.tar.gz
tar xvfz influxdb-1.7.1-static_linux_amd64.tar.gz
wget https://dl.influxdata.com/chronograf/releases/chronograf-1.7.3_linux_amd64.tar.gz
tar xvfz chronograf-1.7.3_linux_amd64.tar.gz
```

- start InfluxDB:
    - `cd influxdb-1.7.1-1/`
    - if you like to, edit influxdb.conf and change [meta].dir, [data].dir and [data].wal-dir to some user-writable directories
    - `./influxd run -config ./influxdb.conf`
- start Chronograf:
     - `cd chronograf-1.7.3-1`
     - `./usr/bin/chronograf`
- restore backup data:
    - `cd influxdb-1.7.1-1`
    - `./influxd restore -portable ~/ffhb-restore-1/var/backups/influxdb/`
- open Chronograf in browser: http://localhost:8888/
- configure connection to InfluxDB with default values (localhost:8086, no user/password)
    - skip creating any dashboards or Kapacitor connections
- go to http://localhost:8888/sources/1/chronograf/data-explorer?query=SHOW%20DATABASES to see all databases
- click on the databases to interactively view InfluxDB contents
- example query to show CPU load of vpn01: http://localhost:8888/sources/1/chronograf/data-explorer?query=SELECT%20mean%28%22load%22%29%20AS%20%22mean_load%22%20FROM%20%22ffhb-nodes%22.%22autogen%22.%22node%22%20WHERE%20time%20%3E%20%3AdashboardTime%3A%20AND%20%22hostname%22%3D%27vpn01%27%20GROUP%20BY%20time%28%3Ainterval%3A%29%20FILL%28null%29


License
-------------------------

GPLv3
