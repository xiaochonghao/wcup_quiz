/*
Navicat MySQL Data Transfer

Source Server         : dev
Source Server Version : 50505
Source Host           : 101.251.234.164:3306
Source Database       : wcup_quiz

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-06-08 00:15:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account_user
-- ----------------------------
DROP TABLE IF EXISTS `account_user`;
CREATE TABLE `account_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `employee_no` varchar(255) DEFAULT NULL,
  `id_no` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(50) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `wechat_id` varchar(255) DEFAULT NULL,
  `capital` decimal(12,3) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  `register_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `ext_data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_account_user_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wcup_country
-- ----------------------------
DROP TABLE IF EXISTS `wcup_country`;
CREATE TABLE `wcup_country` (
  `name` varchar(50) NOT NULL,
  `name_zh_cn` varchar(50) NOT NULL,
  `group` varchar(10) NOT NULL,
  `is_out` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wcup_guess_condition
-- ----------------------------
DROP TABLE IF EXISTS `wcup_guess_condition`;
CREATE TABLE `wcup_guess_condition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `odds_a` double NOT NULL,
  `odds_b` double NOT NULL,
  `handicap_num` double NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `schedule_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wcup_guess_condition_schedule_id_4e5b0db1_fk_wcup_schedule_id` (`schedule_id`),
  CONSTRAINT `wcup_guess_condition_schedule_id_4e5b0db1_fk_wcup_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `wcup_schedule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wcup_guess_record
-- ----------------------------
DROP TABLE IF EXISTS `wcup_guess_record`;
CREATE TABLE `wcup_guess_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_for` int(11) NOT NULL,
  `support_odds` double NOT NULL,
  `pay_back` decimal(12,3) DEFAULT NULL,
  `detail` longtext NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `condition_id` int(11) NOT NULL,
  `schedule_id` varchar(36) NOT NULL,
  `support_country_id` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wcup_guess_record_condition_id_2fd06d3b_fk_wcup_gues` (`condition_id`),
  KEY `wcup_guess_record_schedule_id_52cc3568_fk_wcup_schedule_id` (`schedule_id`),
  KEY `wcup_guess_record_support_country_id_c0d0c664_fk_wcup_coun` (`support_country_id`),
  KEY `wcup_guess_record_user_id_590e73be_fk_account_user_user_id` (`user_id`),
  CONSTRAINT `wcup_guess_record_condition_id_2fd06d3b_fk_wcup_gues` FOREIGN KEY (`condition_id`) REFERENCES `wcup_guess_condition` (`id`),
  CONSTRAINT `wcup_guess_record_schedule_id_52cc3568_fk_wcup_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `wcup_schedule` (`id`),
  CONSTRAINT `wcup_guess_record_support_country_id_c0d0c664_fk_wcup_coun` FOREIGN KEY (`support_country_id`) REFERENCES `wcup_country` (`name`),
  CONSTRAINT `wcup_guess_record_user_id_590e73be_fk_account_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wcup_schedule
-- ----------------------------
DROP TABLE IF EXISTS `wcup_schedule`;
CREATE TABLE `wcup_schedule` (
  `id` varchar(36) NOT NULL,
  `start_time` datetime NOT NULL,
  `score_90min` varchar(20) NOT NULL,
  `score_final` varchar(20) NOT NULL,
  `type` varchar(20) NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `country_a_id` varchar(50) NOT NULL,
  `country_b_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wcup_schedule_country_a_id_c3839ca3_fk_wcup_country_name` (`country_a_id`),
  KEY `wcup_schedule_country_b_id_b3131c51_fk_wcup_country_name` (`country_b_id`),
  CONSTRAINT `wcup_schedule_country_a_id_c3839ca3_fk_wcup_country_name` FOREIGN KEY (`country_a_id`) REFERENCES `wcup_country` (`name`),
  CONSTRAINT `wcup_schedule_country_b_id_b3131c51_fk_wcup_country_name` FOREIGN KEY (`country_b_id`) REFERENCES `wcup_country` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wcup_transaction
-- ----------------------------
DROP TABLE IF EXISTS `wcup_transaction`;
CREATE TABLE `wcup_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `out_gold` int(11) DEFAULT NULL,
  `in_gold` decimal(12,3) DEFAULT NULL,
  `detail` longtext,
  `create_time` datetime NOT NULL,
  `schedule_id` varchar(36) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wcup_transaction_schedule_id_9963a72d_fk_wcup_schedule_id` (`schedule_id`),
  KEY `wcup_transaction_user_id_f135384a_fk_account_user_user_id` (`user_id`),
  CONSTRAINT `wcup_transaction_schedule_id_9963a72d_fk_wcup_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `wcup_schedule` (`id`),
  CONSTRAINT `wcup_transaction_user_id_f135384a_fk_account_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
