
CREATE TABLE `common_cnf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(128) NOT NULL COMMENT '配置key',
  `value` varchar(1024) NOT NULL COMMENT '配置value',
  `active` tinyint(1) NOT NULL COMMENT '是否有效',
  `desc` varchar(1024) DEFAULT NULL COMMENT '配置描述',
  `created` datetime NOT NULL COMMENT '创建时间',
  `updated` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uix_key` (`key`) USING BTREE,
  KEY `ix_key` (`key`,`created`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `env_cnf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env` varchar(128) NOT NULL,
  `key` varchar(128) NOT NULL,
  `value` varchar(1024) NOT NULL,
  `desc` varchar(1024) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_env_key` (`env`,`key`),
  KEY `ix_env_key` (`env`,`key`,`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `srv_cnf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env` varchar(128) NOT NULL,
  `team` varchar(128) NOT NULL,
  `project` varchar(128) NOT NULL,
  `run_level` int(11) NOT NULL,
  `deploy_type` varchar(128) NOT NULL,
  `current_host` varchar(128) DEFAULT NULL,
  `dev_master` varchar(128) DEFAULT NULL,
  `test_master` varchar(128) DEFAULT NULL,
  `process_key` varchar(128) DEFAULT NULL,
  `desc` varchar(1024) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_env_team_project` (`env`,`team`,`project`),
  KEY `ix_env_team_project` (`env`,`team`,`project`,`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#############`common_cnf` fake data###############
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'mobileHeaders', '{\"User-Agent\": \"Mozilla/5.0 (Linux; Android 4.4.4; Python Scripts/KTU84P)     AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0     Chrome/33.0.0.0 Mobile Safari/537.36     MyMoney/10.3.2.5 feideeAndroidMarket\"}', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'pcHeaders', '{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64)     AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/58.0.3029.81 Safari/537.36\"}', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'Server', 'mail.sui.com', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'From', 'jun_liu3@sui.com', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'To', '[\"jun_liu3@sui.com\"]', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'Subject', '测试环境监控预警', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'dbHost', '10.201.5.33', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'dbUser', 'test_group', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'dbPassword', '123456', '', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'memWarning', '100', '小于该值预警(M)', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'loadWarning', '50', '负载大于该值预警', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');
INSERT INTO `common_cnf`( `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ( 'diskWarning', '1', '硬盘容量小于该值后预警(G)', 1, '2018-11-03 14:03:11', '2018-11-03 14:03:13');


#############`env_cnf` fake data###############
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('UAT', 'rootHost', 'https://uat.host.com', 'UAT域名', 1, '2018-11-28 20:05:04', '2018-11-28 20:05:06');
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('Test1', 'redisInfo', '{\"host\":\"10.201.1.1\",\"port\":9201,\"password\":\"password\"}', 'Test1 redis信息', 1, '2019-01-14 20:33:17', '2019-01-14 20:33:20');
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('UAT', 'redisInfo', '{\"host\":\"10.201.2.1\",\"port\":9201,\"password\":\"password\"}', 'UAT redis信息', 1, '2019-01-14 20:33:17', '2019-01-14 20:33:20');
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('Test1', 'dbInfo', '{\"host\":\"10.201.1.1\",\"port\":3306,\"user\":\"root\",\"password\":\"password\"}', 'Test1 db信息', 1, '2019-01-14 20:07:29', '2019-01-14 20:07:29');
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('UAT', 'dbInfo', '{\"host\":\"10.201.2.1\",\"port\":3306,\"user\":\"root\",\"password\":\"password\"}', 'UAT db信息', 1, '2019-01-14 20:07:29', '2019-01-14 20:07:29');
INSERT INTO `env_cnf`(`env`, `key`, `value`, `desc`, `active`, `created`, `updated`) VALUES ('Tester_1', 'srvInfo', '{\"port\":22,\"user\":\"testgroup\",\"password\":\"password\",\"host\":\"10.201.1.1\"}', '测试服务器1信息', 1, '2019-10-15 08:42:17', '2019-10-15 08:42:22');

