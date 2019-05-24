/*
Navicat MySQL Data Transfer

Source Server         : KAILIN
Source Server Version : 80013
Source Host           : localhost:3306
Source Database       : information

Target Server Type    : MYSQL
Target Server Version : 80013
File Encoding         : 65001

Date: 2019-05-24 15:56:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('d54e4533da4a');

-- ----------------------------
-- Table structure for info_category
-- ----------------------------
DROP TABLE IF EXISTS `info_category`;
CREATE TABLE `info_category` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_category
-- ----------------------------
INSERT INTO `info_category` VALUES ('2019-05-02 20:05:22', '2019-05-08 20:05:26', '1', '最新');
INSERT INTO `info_category` VALUES ('2019-05-18 20:52:46', '2019-05-18 20:52:51', '2', '科技');
INSERT INTO `info_category` VALUES ('2019-05-18 20:53:04', '2019-05-23 20:54:03', '3', 'AI');
INSERT INTO `info_category` VALUES ('2019-05-16 20:53:23', '2019-05-18 20:53:25', '4', '商品');
INSERT INTO `info_category` VALUES ('2019-05-16 20:53:35', '2019-05-18 20:53:38', '5', '媒体');
INSERT INTO `info_category` VALUES ('2019-05-02 20:53:53', '2019-05-18 20:53:58', '6', '公司');

-- ----------------------------
-- Table structure for info_comment
-- ----------------------------
DROP TABLE IF EXISTS `info_comment`;
CREATE TABLE `info_comment` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `content` text COLLATE utf8mb4_general_ci NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `like_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `news_id` (`news_id`),
  KEY `parent_id` (`parent_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `info_comment_ibfk_1` FOREIGN KEY (`news_id`) REFERENCES `info_news` (`id`),
  CONSTRAINT `info_comment_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `info_comment` (`id`),
  CONSTRAINT `info_comment_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `info_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_comment
-- ----------------------------
INSERT INTO `info_comment` VALUES ('2019-05-22 17:27:50', '2019-05-22 17:27:50', '4', '1', '1', '撒打撒打撒', null, '0');
INSERT INTO `info_comment` VALUES ('2019-05-23 14:08:39', '2019-05-23 14:08:47', '5', '1', '7', 'qweqwe', null, '0');
INSERT INTO `info_comment` VALUES ('2019-05-23 14:08:44', '2019-05-23 14:08:50', '6', '1', '7', 'wqeqwew', null, '0');

-- ----------------------------
-- Table structure for info_comment_like
-- ----------------------------
DROP TABLE IF EXISTS `info_comment_like`;
CREATE TABLE `info_comment_like` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`comment_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `info_comment_like_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `info_comment` (`id`),
  CONSTRAINT `info_comment_like_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `info_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_comment_like
-- ----------------------------

-- ----------------------------
-- Table structure for info_news
-- ----------------------------
DROP TABLE IF EXISTS `info_news`;
CREATE TABLE `info_news` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `source` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `digest` varchar(512) COLLATE utf8mb4_general_ci NOT NULL,
  `content` text COLLATE utf8mb4_general_ci NOT NULL,
  `clicks` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `reason` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `info_news_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `info_category` (`id`),
  CONSTRAINT `info_news_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `info_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_news
-- ----------------------------
INSERT INTO `info_news` VALUES ('2019-05-01 20:13:26', '2019-05-24 15:14:25', '1', 'awdwad', 'awd', 'awd', 'awd', '35', 'http://prsk3m77n.bkt.clouddn.com/FuLsbHma5TAkmyHVyxxvrlUFM1F9', '3', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-01 20:15:05', '2019-05-22 17:23:20', '2', '123', '123', '123', '123', '132', 'http://prsk3m77n.bkt.clouddn.com/FuLsbHma5TAkmyHVyxxvrlUFM1F9', '2', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-08 20:15:28', '2019-05-23 21:07:36', '3', '3', '2', '23', '23', '26', 'http://prsk3m77n.bkt.clouddn.com/FuLsbHma5TAkmyHVyxxvrlUFM1F9', '3', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-21 20:17:28', '2019-05-23 21:07:33', '4', 'hahah ', '个人发布', 'qqq', '哈哈', '9', 'http://prsk3m77n.bkt.clouddn.com/Fo78zVBvfosCm1TBOn2PqxEA5tbd', '3', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-21 21:05:14', '2019-05-22 17:17:08', '5', '777', '个人发布', '111223', '哈哈', '1', 'http://prsk3m77n.bkt.clouddn.com/Fq2ZDv6QOSPGUrCvEi4KkERGl_ay', '3', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-21 21:14:08', '2019-05-24 08:24:05', '6', '123456', '个人发布', 'qeq', '哈哈', '27', 'http://prsk3m77n.bkt.clouddn.com/Fobt3nIegcgKFeW4VJrzuMLW8QCA', '3', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-21 21:32:33', '2019-05-24 08:42:55', '7', '123122222', '个人发布', '1231', '哈哈', '8', 'http://prsk3m77n.bkt.clouddn.com/FuLsbHma5TAkmyHVyxxvrlUFM1F9', '2', '1', '0', null);
INSERT INTO `info_news` VALUES ('2019-05-23 14:07:20', '2019-05-24 13:56:41', '8', '测试新闻', '个人发布', '测试ing', '<ol>\n<li>册谔谔谔谔谔谔谔</li>\n<li>qweqweqwqwes</li>\n</ol>', '16', 'http://prsk3m77n.bkt.clouddn.com/Fo78zVBvfosCm1TBOn2PqxEA5tbd', '2', '1', '0', 'kkkk');
INSERT INTO `info_news` VALUES ('2020-02-01 13:54:20', '2019-05-24 15:11:15', '9', '用户须知', '管理大大', '使用须知', '<h1 style=\"text-align: center;\">用户须知</h1>\n<ul>\n<li>&nbsp;注册时无需输入手机验证码 （如不能注册请使用以下测试账号）:</li>\n</ul>\n<p>&nbsp;</p>\n<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; 测试账号： 账号：18222222222 &nbsp;&nbsp;账号：15737961722 &nbsp;&nbsp;<span style=\"display: inline !important; float: none; background-color: transparent; color: #000000; cursor: text; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;\">账号：17111111111&nbsp;</span></p>\n<p style=\"background-color: transparent; color: #000000; cursor: text; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; orphans: 2; outline-color: transparent; outline-style: none; outline-width: 0px; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;\">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; 密码：123456 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; 密码：123456789 &nbsp; &nbsp; &nbsp; <span style=\"display: inline !important; float: none; background-color: transparent; color: #000000; cursor: text; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;\">密码：123456789 &nbsp; &nbsp;</span></p>\n<p><span style=\"background-color: transparent; color: #000000; cursor: text; display: inline; float: none; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;\">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; 账号：16222222222 &nbsp;&nbsp;账号：15333333333</span></p>\n<p><span style=\"background-color: transparent; color: #000000; cursor: text; display: inline; float: none; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;\">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; 密码：123456789 &nbsp; &nbsp; &nbsp;&nbsp;密码：123456789&nbsp;</span></p>\n<p>&nbsp;</p>\n<ul>\n<li>&nbsp; 一切BUG请反馈呆鹅：2534992864</li>\n</ul>', '11121', null, '2', '1', '0', null);

-- ----------------------------
-- Table structure for info_user
-- ----------------------------
DROP TABLE IF EXISTS `info_user`;
CREATE TABLE `info_user` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nick_name` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `avatar_url` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `signature` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gender` enum('MAN','WOMAN') COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `nick_name` (`nick_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_user
-- ----------------------------
INSERT INTO `info_user` VALUES ('2019-05-21 19:58:15', '2019-05-24 14:26:08', '1', '15737961721', 'pbkdf2:sha256:150000$l0XCx3E6$4645de80a318dfbb227be84c0878022e82a2d00e9d8c8be7386425ce8f05d4fb', '15737961721', 'FuLsbHma5TAkmyHVyxxvrlUFM1F9', '2019-05-24 14:26:08', '1', 'KAILIN', 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-21 19:51:09', '2019-05-24 14:20:35', '2', '18222222222', 'pbkdf2:sha256:150000$Y6yM0c5r$5efbdb7c04cde38e2c1dad585e80c8ab0bfa0cd298fed4ac6cad03cc67bbdfc1', '18222222222', null, '2019-05-24 14:20:35', '0', null, 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-02 14:00:03', '2019-05-02 14:00:06', '3', '18233333333', '$5efbdb7c04cde38e2c1dad585e80c8ab0bfa0cd298fed4ac6cad03cc67bbdfc1', '18233333333', null, '2019-05-13 14:00:40', '0', null, 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-24 08:42:51', '2019-05-24 14:22:05', '4', '15737961722', 'pbkdf2:sha256:150000$tS21hMOu$d12ac23873e47d03485d8c714bf401a5ee14fffd545218b43dd8df0041db44df', '15737961722', null, '2019-05-24 14:22:05', '0', null, 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-24 14:18:14', '2019-05-24 14:18:14', '5', '17111111111', 'pbkdf2:sha256:150000$p6UHi8YA$8189455bdf59eecf28e34f9818f98079da6f62172596b8aa083a6ff5941f90cb', '17111111111', null, '2019-05-24 14:18:14', '0', null, 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-24 14:18:47', '2019-05-24 14:18:47', '6', '16222222222', 'pbkdf2:sha256:150000$U1g2vku9$7459b73a66458dabb3562303295d8efaf1b7c15c0d3dd6c091d5e31f211c514d', '16222222222', null, '2019-05-24 14:18:47', '0', null, 'MAN');
INSERT INTO `info_user` VALUES ('2019-05-24 14:19:51', '2019-05-24 14:19:51', '7', '15333333333', 'pbkdf2:sha256:150000$5KAFAreL$33170839ad4bc5fbf73321dba1a5ce84c130175add8210134883bbad1b543779', '15333333333', null, '2019-05-24 14:19:51', '0', null, 'MAN');

-- ----------------------------
-- Table structure for info_user_collection
-- ----------------------------
DROP TABLE IF EXISTS `info_user_collection`;
CREATE TABLE `info_user_collection` (
  `user_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`news_id`),
  KEY `news_id` (`news_id`),
  CONSTRAINT `info_user_collection_ibfk_1` FOREIGN KEY (`news_id`) REFERENCES `info_news` (`id`),
  CONSTRAINT `info_user_collection_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `info_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_user_collection
-- ----------------------------
INSERT INTO `info_user_collection` VALUES ('1', '1', '2019-05-22 17:27:52');
INSERT INTO `info_user_collection` VALUES ('1', '2', '2019-05-21 20:12:46');
INSERT INTO `info_user_collection` VALUES ('1', '4', '2019-05-22 09:41:57');

-- ----------------------------
-- Table structure for info_user_fans
-- ----------------------------
DROP TABLE IF EXISTS `info_user_fans`;
CREATE TABLE `info_user_fans` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `info_user_fans_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `info_user` (`id`),
  CONSTRAINT `info_user_fans_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `info_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of info_user_fans
-- ----------------------------
INSERT INTO `info_user_fans` VALUES ('2', '1');
INSERT INTO `info_user_fans` VALUES ('4', '1');
