CREATE DATABASE IF NOT EXISTS `unifyiq`;

CREATE TABLE IF NOT EXISTS `unifyiq`.`unifyiq_configs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `connector_type` VARCHAR(45) NOT NULL,
  `url_prefix` VARCHAR(255) NOT NULL,
  `cron_expr` VARCHAR(20) NOT NULL,
  `start_ts` INTEGER NOT NULL,
  `config_json` VARCHAR(2048) NOT NULL,
  `last_fetched_ts` INTEGER NOT NULL,
  `is_enabled` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`), UNIQUE KEY (`name`));


CREATE TABLE IF NOT EXISTS `unifyiq`.`user_otps` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL,
    `otp` VARCHAR(6) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `is_verified` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`email`)
);
