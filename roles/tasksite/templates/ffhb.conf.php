<?php

# {{ ansible_managed }}

return array(
  'mysql.host' => 'localhost',
  'mysql.user' => 'phabric',
  'mysql.pass' => '{{ mysql_password_base64["content"] | b64decode }}',
  'phabricator.timezone' => 'Europe/Berlin',
  'phabricator.base-uri' => 'https://{{ tasks_domain }}/',
  'repository.default-local-path' => '/home/{{ tasks_user }}/.var/repo',
  'storage.local-disk.path' => '/home/{{ tasks_user }}/.var/storage',
);
