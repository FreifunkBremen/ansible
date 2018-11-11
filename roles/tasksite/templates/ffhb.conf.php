<?php

# {{ ansible_managed }}

return array(
  'mysql.host' => 'localhost',
  'mysql.user' => 'phabric',
  'mysql.pass' => '{{ mysql_password_base64["content"] | b64decode }}',
  'phabricator.timezone' => 'Europe/Berlin',
  # Phabricator only supports one single base URI, and we have used the shorter one (tasks.ffhb.de) so far:
  'phabricator.base-uri' => 'https://{{ tasks_subdomain }}.{{ alt_domain }}/',
  'repository.default-local-path' => '/home/{{ tasks_user }}/.var/repo',
  'storage.local-disk.path' => '/home/{{ tasks_user }}/.var/storage',
);
