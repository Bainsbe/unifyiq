-- Slack
CREATE TABLE IF NOT EXISTS `unifyiq`.`fetchers_slack_channel_members` (
  `channel_id` VARCHAR(45) NOT NULL,
  `member_id` VARCHAR(45) NOT NULL,
  `is_active` BOOLEAN NOT NULL,
  PRIMARY KEY (`channel_id`, `member_id`));

CREATE TABLE IF NOT EXISTS `unifyiq`.`fetchers_slack_channel_info` (
    `channel_id` VARCHAR(45) NOT NULL,
    `name` VARCHAR(80) NOT NULL,
    `topic` VARCHAR(256) NOT NULL,
    `purpose` VARCHAR(256) NOT NULL,
    `is_archived` BOOLEAN NOT NULL,
    `is_private` BOOLEAN NOT NULL,
    `is_channel` BOOLEAN NOT NULL,
    `is_group` BOOLEAN NOT NULL,
    `is_im` BOOLEAN NOT NULL,
    `is_mpim` BOOLEAN NOT NULL,
    PRIMARY KEY (`channel_id`));

-- Confluence
CREATE TABLE IF NOT EXISTS `unifyiq`.`fetchers_confluence_page_info` (
    `page_id` VARCHAR(45) NOT NULL,
    `space_key` VARCHAR(80) NOT NULL,
    `topic` VARCHAR(512) NOT NULL,
    `author_email` VARCHAR(80) NOT NULL,
    `last_modified_time` INTEGER NOT NULL,
    `status` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`space_key`, `page_id`));
