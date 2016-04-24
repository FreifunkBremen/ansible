<?php

# {{ ansible_managed }}

return array(
  'mysql.implementation' => 'AphrontMySQLiDatabaseConnection',
  'mysql.host' => 'localhost',
  'mysql.user' => 'root',
  'mysql.pass' => '{{ tasks_mysql_password }}',
);
