<?php

# {{ ansible_managed }}

return array(
  'mysql.implementation' => 'AphrontMySQLiDatabaseConnection',
  'mysql.host' => 'localhost',
  'mysql.user' => 'root',
  'mysql.pass' => '{{ tasks_mysql_password }}',
  'phabricator.base-uri' => 'http://{{ tasks_domain }}/',
  'pygments.enabled' => true,
  'repository.default-local-path' => '/home/{{ tasks_user }}/.var/repo',
);
