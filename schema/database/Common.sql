CREATE DATABASE IF NOT EXISTS `unifyiq`;

CREATE TABLE IF NOT EXISTS `unifyiq`.`unifyiq_configs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `connector_platform` VARCHAR(45) NOT NULL,
  `connector_type` VARCHAR(45) NOT NULL,
  `src_storage_type` VARCHAR(45) NOT NULL,
  `src_path` VARCHAR(255) NOT NULL,
  `dest_storage_type` VARCHAR(45) NOT NULL,
  `dest_path` VARCHAR(255) NOT NULL,
  `url_prefix` VARCHAR(255) NOT NULL,
  `cron_expr` VARCHAR(20) NOT NULL,
  `last_fetched_ts` INTEGER NOT NULL,
  `is_enabled` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`), UNIQUE KEY (`name`));
