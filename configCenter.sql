
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

