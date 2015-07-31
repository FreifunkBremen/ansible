SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


CREATE TABLE IF NOT EXISTS `prosody` (
  `host` text,
  `user` text,
  `store` text,
  `key` text,
  `type` text,
  `value` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `prosody`
  ADD KEY `prosody_index` (`host`(20),`user`(20),`store`(20),`key`(20));
