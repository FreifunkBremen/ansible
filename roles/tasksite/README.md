task system site
=========================

Install Phabricator as task management system of Freifunk Bremen.


Configuration
-------------------------

See `defaults/main.yml` for available parameters.


Usage
-------------------------

    - hosts: servers
      roles:
         - tasksite

Note: after installation with Ansible you need to manually add some config options to /var/www/tasks/opt/phabricator/phabricator/conf/local/local.json. This file contains secrets that are not contained in the Ansible role.


Restore Data From Backup
-------------------------

When restoring a backup, any existing Phabricator data will be overwritten by the data from backup.

This procedure assumes that each Phabricator database is backed up into a separate file, with a name like this: daily_phabricator_meta_data_2016-04-17_00h00m_Sunday.sql.gz


Source customized PHP environment:
  source ~/.local/bin/php_env.sh

Disable tasks site:
  echo "Require all denied" >> /var/www/tasks/domains/tasks.bremen.freifunk.net/.htaccess

Shut down Phabricator daemons:
  svc -d ~/.config/service/phabricator/

Check that daemons are actually killed:
  svstat ~/.config/service/phabricator/
(if they are still alive after 20 seconds, run the svc -d command again)

Backups can only really be restored to the same Phabricator version from which they were taken. So you need the original versions (Git hashes) of the three Phabricator repos (they can be found in a Git checkout with "git rev-parse HEAD"), and have to checkout these versions:
  cd /var/www/tasks/opt/phabricator/arcanist
  git checkout -b backup_version <hash of arcanist module>
  cd /var/www/tasks/opt/phabricator/libphutil
  git checkout -b backup_version <hash of libphutil module>
  cd /var/www/tasks/opt/phabricator/phabricator
  git checkout -b backup_version <hash of phabricator module>

Erase any existing database schema, then create new blank database:
  cd /var/www/tasks/opt/phabricator/phabricator
  ./bin/storage destroy
  ./bin/storage upgrade
(when asked "Fix these schema issues?", say yes).

Go into the directory where all database dump files are located, and run this command to restore database contents from backup:
  for f in *.sql.gz; do dbname=$(echo "$f" | cut -d_ -f 2- | awk -F '_20' '{print $1}'); echo "$f=$dbname"; zcat "$f" | mysql -u phabric -p$(cat ~/mysql-password) -D "$dbname"; done

Perform database upgrade (usually there shouldn't be any changes):
  cd /var/www/tasks/opt/phabricator/phabricator
  ./bin/storage upgrade

Restore separate file storage of uploaded files, by copying directory contents from backup to ~/.var/storage/ .
Make sure that the restored files and directories belong to the "tasks" user and group and are writable for the user.

Checkout newest Phabricator version again:
  cd /var/www/tasks/opt/phabricator/arcanist
  git checkout stable
  git branch -d backup_version
  cd /var/www/tasks/opt/phabricator/libphutil
  git checkout stable
  git branch -d backup_version
  cd /var/www/tasks/opt/phabricator/phabricator
  git checkout stable
  git branch -d backup_version

Perform database upgrade
  cd /var/www/tasks/opt/phabricator/phabricator
  ./bin/storage upgrade
(when asked "Fix these schema issues?", say yes).

Clear caches:
  cd /var/www/tasks/opt/phabricator/phabricator
  ./bin/cache purge --purge-all

Restart web server:
  service apache2 restart

Start Phabricator daemons:
  svc -u ~/.config/service/phabricator/

Reenable tasks site, by editing /var/www/tasks/domains/tasks.bremen.freifunk.net/.htaccess and removing the "Require all denied" line.


License
-------------------------

GPLv3
