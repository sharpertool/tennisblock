/*
 Navicat Premium Data Transfer

 Source Server         : Bondinorthpro
 Source Server Type    : MySQL
 Source Server Version : 50513
 Source Host           : localhost
 Source Database       : tennisblock

 Target Server Type    : MySQL
 Target Server Version : 50513
 File Encoding         : utf-8

 Date: 08/22/2013 14:44:21 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `availability`
-- ----------------------------
DROP TABLE IF EXISTS `availability`;
CREATE TABLE `availability` (
  `PID` int(8) NOT NULL,
  `date` date NOT NULL,
  `unavailable` tinyint(1) NOT NULL,
  `Reason` text NOT NULL,
  `season` varchar(12) NOT NULL DEFAULT '2008 fall',
  `sid` smallint(11) NOT NULL,
  KEY `date` (`date`),
  KEY `PID` (`PID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `blockmeetings`
-- ----------------------------
DROP TABLE IF EXISTS `blockmeetings`;
CREATE TABLE `blockmeetings` (
  `MEETID` int(8) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `holdout` tinyint(1) NOT NULL,
  `comments` text NOT NULL,
  `season` varchar(12) NOT NULL DEFAULT '2008 fall',
  `sid` smallint(11) NOT NULL,
  PRIMARY KEY (`MEETID`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=2363 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `couples`
-- ----------------------------
DROP TABLE IF EXISTS `couples`;
CREATE TABLE `couples` (
  `coupleid` int(8) NOT NULL AUTO_INCREMENT,
  `couplename` varchar(50) NOT NULL,
  `pa_id` int(8) NOT NULL,
  `pb_id` int(8) NOT NULL,
  `fulltime` tinyint(1) NOT NULL,
  `canschedule` tinyint(1) DEFAULT NULL,
  `blockcouple` tinyint(1) DEFAULT NULL,
  `season` varchar(12) NOT NULL DEFAULT '2008 fall',
  PRIMARY KEY (`coupleid`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `couples`
-- ----------------------------
BEGIN;
INSERT INTO `couples` VALUES ('65', 'Bloomers', '1', '2', '0', '1', '1', '2009 Fall'), ('66', 'Hendersons', '6', '5', '1', '1', '1', '2009 Fall'), ('67', 'Putnams', '7', '8', '0', '1', '1', '2009 Fall'), ('68', 'Millers', '10', '9', '0', '1', '1', '2009 Fall'), ('69', 'Rita & Rod', '13', '17', '0', '1', '1', '2009 Fall'), ('70', 'Holtzs', '15', '16', '0', '1', '1', '2009 Fall'), ('71', 'Grukes', '21', '22', '0', '1', '1', '2009 Fall'), ('72', 'Moorheads', '32', '33', '0', '1', '1', '2009 Fall'), ('73', 'Bettises', '38', '39', '0', '1', '1', '2009 Fall'), ('74', 'Pearces', '44', '45', '0', '1', '1', '2009 Fall'), ('75', 'Coffeys', '52', '53', '0', '1', '1', '2009 Fall'), ('76', 'Dave & Rochelle', '54', '55', '0', '1', '1', '2009 Fall'), ('77', 'Kirbys', '56', '57', '0', '1', '1', '2009 Fall'), ('78', 'Sharps', '58', '59', '0', '1', '1', '2009 Fall'), ('79', 'Raus', '34', '35', '0', '1', '1', '2009 Fall'), ('150', 'Sharps', '58', '59', '0', '1', '1', '2010 Spring'), ('151', 'Dave & Rochelle', '55', '54', '0', '1', '1', '2010 Spring'), ('152', 'Grunkes', '22', '21', '0', '1', '1', '2010 Spring'), ('153', 'Henderson', '5', '6', '1', '1', '1', '2010 Spring'), ('154', 'Kirbys', '56', '57', '0', '1', '1', '2010 Spring'), ('155', 'Pearce', '44', '45', '0', '1', '1', '2010 Spring'), ('156', 'Bloomers', '2', '1', '0', '1', '1', '2010 Spring'), ('157', 'Bettis', '38', '39', '0', '1', '1', '2010 Spring'), ('158', 'Millers', '9', '10', '0', '1', '1', '2010 Spring'), ('159', 'Rod & Rita', '13', '17', '0', '1', '1', '2010 Spring'), ('160', 'Putnams', '8', '7', '0', '1', '1', '2010 Spring');
COMMIT;

-- ----------------------------
--  Table structure for `player_availability`
-- ----------------------------
DROP TABLE IF EXISTS `player_availability`;
CREATE TABLE `player_availability` (
  `pid` int(8) DEFAULT NULL,
  `firstname` varchar(40) DEFAULT NULL,
  `lastname` varchar(60) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `unavailable` tinyint(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `player_unavailable`
-- ----------------------------
DROP TABLE IF EXISTS `player_unavailable`;
CREATE TABLE `player_unavailable` (
  `pid` int(8) DEFAULT NULL,
  `firstname` varchar(40) DEFAULT NULL,
  `lastname` varchar(60) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `players`
-- ----------------------------
DROP TABLE IF EXISTS `players`;
CREATE TABLE `players` (
  `PID` int(8) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(40) NOT NULL,
  `lastname` varchar(60) NOT NULL,
  `gender` varchar(1) NOT NULL DEFAULT 'm',
  `NTRP` float NOT NULL,
  `microNTRP` float NOT NULL,
  `email` varchar(50) NOT NULL,
  `home` varchar(14) NOT NULL,
  `cell` varchar(14) NOT NULL,
  `work` varchar(14) NOT NULL,
  PRIMARY KEY (`PID`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `players`
-- ----------------------------
BEGIN;
INSERT INTO `players` VALUES ('-2', 'Nobody', '', 'f', '0', '0', '', '', '', ''), ('-1', 'Nobody', '', 'm', '3.5', '3.75', '', '', '', ''), ('1', 'Linda', 'Bloomer', 'f', '4', '4', 'lmbloomer@cableone.net', '', '(208) 724-3267', ''), ('2', 'Jonathan', 'Bloomer', 'm', '4', '4.1', 'jtbloomer@cableone.net', '(208) 378-7418', '', ''), ('3', 'Lisa', 'Dekerchove', 'f', '3.5', '3.6', 'dldekerchove@gmail.com', '(208) 853-2878', '', ''), ('4', 'Doug', 'Dekerchove', 'm', '4', '4.1', 'Dougd@pioneertitleco.com', '', '', ''), ('5', 'Ed', 'Henderson', 'm', '3.5', '3.8', 'edhenderseon@cableone.net', '', '(208) 861-5756', '(208) 489-9380'), ('6', 'Vicki', 'Henderson', 'f', '4', '4', 'viquee@cableone.net', '', '(208) 861-5816', ''), ('7', 'Sheryl', 'Putnam', 'f', '3.5', '3.9', 'Sherylp@IHFA.org', '', '', ''), ('8', 'Jake', 'Putnam', 'm', '4', '4.2', 'mjakeputnam@att.net', '', '', ''), ('9', 'Gary', 'Miller', 'm', '4', '4', 'gary.d.miller@hp.com', '', '', ''), ('10', 'Darlene', 'Miller', 'f', '4', '4.05', 'darlene.miller@hp.com', '(208) 724-4474', '', ''), ('11', 'Gayle', 'Stauffer', 'f', '3.5', '3.4', 'stauffers4@cableone.net', '(208) 939-4380', '', ''), ('12', 'Randy', 'Stauffer', 'm', '4', '4.3', '', '', '', ''), ('13', 'Rod', 'Kimerling', 'm', '4', '4.2', 'rodnkime@yahoo.com', '', '', ''), ('14', 'Christa', 'Patton', 'f', '3.5', '3.9', 'Christa@HomesWithChrista.com', '', '(208) 859-8621', ''), ('15', 'Colleen', 'Holtz', 'f', '3.5', '3.4', 'dynamo10_2000@yahoo.com', '', '(208) 869-7319', ''), ('16', 'Kenny', 'Holtz', 'm', '4', '3.8', 'kholtz@quality-comm.net', '', '', ''), ('17', 'Rita', 'Caven', 'f', '3.5', '3.9', 'ritacaven@msn.com', '(208) 938-0734', '(208) 484-2468', ''), ('18', 'Steve', 'Caven', 'm', '4', '4.25', 'slcaven@msn.com', '(208) 938-0734', '(208) 283-7918', ''), ('19', 'Tracey', 'Idoeta', 'f', '3.5', '3.7', 'idoeta@aol.com', '(208) 362-3481', '', ''), ('20', 'Javier', 'Idoeta', 'm', '5', '5', '', '', '', ''), ('21', 'Jenny', 'Grunke', 'f', '4', '4.2', 'jcrlaw2000@yahoo.com', '(208) 672-9254', '', ''), ('22', 'James', 'Grunke', 'm', '3.5', '3.65', 'jwgrunke@hotmail.com', '', '', ''), ('23', 'Jean', 'Russel', 'f', '3.5', '3.85', '', '', '', ''), ('24', 'Mike', 'Merlot', 'm', '3.5', '3.8', '', '', '', ''), ('25', 'Ken', 'Holtz', 'm', '3.5', '3.5', '', '', '', ''), ('26', 'Rosel', 'Holtz', 'f', '3.5', '3.5', '', '', '', ''), ('27', 'Jeff', 'Morrell', 'm', '4', '4.4', 'MELMCBANDT@aol.com', '208 327-0815', '208 284-5240', ''), ('28', 'Kathne', 'Morrell', 'f', '4', '3.9', 'kathne@aol.com', '208 327-0815', '208 371-0325', '208 381-2490'), ('29', 'Nancy', 'Edward-Wong', 'f', '3', '3.49', '', '', '', ''), ('30', 'Gabby', 'Braun-Maude', 'f', '4', '4.1', '', '', '', ''), ('32', 'Russ', 'Moorhead', 'm', '4', '4.2', 'rmoorhead@lcarch.com', '208 376-7038', '208 820-4116', ''), ('33', 'Maryann', 'Moorhead', 'f', '4', '4.1', 'mmoorhead@boisetennis.com', '208 376-7038', '208 850-2901', ''), ('34', 'Josh', 'Rau', 'm', '4', '4', 'josh@7upboise.com', '208 442-8419', '', ''), ('35', 'Shiela', 'Rau', 'f', '3.5', '3.6', 'sheilarau@aol.com', '208 442-8419', '', ''), ('36', 'Kenny', 'Wong', 'm', '4.5', '4.6', 'sludawg@yahoo.com', '', '208-794-8557', ''), ('37', 'Carrie', 'Cornils', 'f', '3.5', '3.4', 'carrie_cornils@hotmail.com', '', '', ''), ('38', 'Dave', 'Bettis', 'm', '3.5', '3.6', 'davebettis@cableone.net', '', '', ''), ('39', 'Lisa', 'Bettis', 'f', '3.5', '3.4', '', '', '', ''), ('40', 'Heather', 'Kolnes', 'f', '3.5', '3.8', 'hkolnes@msn.com', '', '', ''), ('41', 'Katie', 'Stauffer', 'f', '3.5', '3.5', '', '', '', ''), ('42', 'Sue', 'Webster', 'f', '3.5', '3.5', '', '', '', ''), ('43', 'Thad', 'Webster', 'm', '3.5', '3.5', '', '', '', ''), ('44', 'John', 'Pearce', 'm', '4.5', '4.5', 'drjpearce@aol.com', '208 855-2369', '', ''), ('45', 'Corie', 'Pearce', 'f', '4', '4.15', 'pearceelc@aol.com', '208 855-2369', '208 283-0065', ''), ('46', 'Colby', '', 'm', '4', '4.45', '', '', '', ''), ('48', 'Susan', 'Schosshberger', 'f', '4', '4', '', '', '', ''), ('49', 'Dave', 'Surbeck', 'm', '4', '4.2', '', '', '', ''), ('50', 'Terry', 'Rich', 'm', '4', '4.1', '', '', '', ''), ('51', 'Shelly', 'Lane', 'f', '4', '4.2', '', '', '', ''), ('52', 'Tammy', 'Sevieri-Coffey', 'f', '4', '4.2', 'coffeyenterprises@clearwire.net', '327-8822', '761-9550', ''), ('53', 'Ken', 'Coffey', 'm', '4.5', '4.6', 'kencoffey@clearwire.com', '327-8822', '', '703-1868'), ('54', 'Rochelle', 'Cummins', 'f', '4', '3.9', 'R2Kirk2@msn.com', '', '', ''), ('55', 'Dave', 'Massee', 'm', '3.5', '3.8', 'massfit@boisetennis.com', '', '', ''), ('56', 'Mike', 'Kirby', 'm', '4.5', '4.6', 'michael.kirby@wellsfargo.com', '', '', ''), ('57', 'Lori', 'Kirby', 'f', '3', '3.1', '', '', '', ''), ('58', 'Bill', 'Sharp', 'm', '4', '4', 'billsharp@boisebuilding.com', '323-2759', '484-0456', ''), ('59', 'Gina', 'Sharp', 'f', '4.5', '4.5', 'gina.sharp@hp.com', '323-2759', '859-5316', ''), ('60', 'Pratap', 'Murali', 'm', '4', '4', 'pratap.murali@gmail.com', '', '', ''), ('61', 'Marcia', 'McChristal', 'f', '4', '4.1', '', '', '', ''), ('62', 'Tyler', 'Holtz', 'm', '3.5', '3.6', '', '', '', ''), ('63', 'Tyler', 'Holtz', 'f', '3.5', '3.7', '', '', '', ''), ('64', 'Michelle', 'Phillips', 'f', '4.5', '4.5', '', '', '', ''), ('65', 'Mark', 'Phillips', 'm', '4', '4.15', '', '', '', ''), ('66', 'Avi', 'Basu', 'm', '4', '4.15', '', '', '', ''), ('67', 'Geri', 'Hyatt', 'f', '4', '4.05', '', '', '', ''), ('68', 'Mike', 'Buckingham', 'm', '4.5', '4.6', '', '', '', ''), ('69', 'Donna', 'Buckingham', 'f', '4.5', '4.2', '', '', '', ''), ('70', 'Nan', 'Jacobsen', 'f', '4', '4.2', '', '', '', ''), ('71', 'Mark', 'Jacobsen', 'm', '4', '4.2', '', '', '', ''), ('72', 'Heather', 'Paddock', 'f', '4', '4', '', '', '', ''), ('73', 'Mark', 'Smith', 'm', '4', '4.4', '', '', '', '');
COMMIT;

-- ----------------------------
--  Table structure for `schedule`
-- ----------------------------
DROP TABLE IF EXISTS `schedule`;
CREATE TABLE `schedule` (
  `schedid` int(16) NOT NULL AUTO_INCREMENT,
  `matchid` int(8) NOT NULL,
  `pid` int(8) NOT NULL,
  `sub` tinyint(1) NOT NULL DEFAULT '0',
  `season` varchar(12) NOT NULL DEFAULT '2008 fall',
  PRIMARY KEY (`schedid`),
  UNIQUE KEY `match_players` (`schedid`,`matchid`,`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=7068 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `season_players`
-- ----------------------------
DROP TABLE IF EXISTS `season_players`;
CREATE TABLE `season_players` (
  `pid` int(8) NOT NULL,
  `season` varchar(12) NOT NULL,
  `blockmember` tinyint(1) NOT NULL,
  `sid` smallint(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `seasons`
-- ----------------------------
DROP TABLE IF EXISTS `seasons`;
CREATE TABLE `seasons` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `season` varchar(20) NOT NULL,
  `courts` int(11) NOT NULL,
  `firstcourt` int(11) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `slots`
-- ----------------------------
DROP TABLE IF EXISTS `slots`;
CREATE TABLE `slots` (
  `SLOTID` int(16) NOT NULL AUTO_INCREMENT,
  `matchid` int(8) NOT NULL,
  `setnum` int(8) NOT NULL,
  `court` varchar(12) NOT NULL,
  `pid` int(16) NOT NULL,
  `position` varchar(12) NOT NULL,
  `combokey` varchar(15) NOT NULL,
  PRIMARY KEY (`SLOTID`),
  UNIQUE KEY `slotindex` (`matchid`,`setnum`,`court`,`pid`),
  KEY `combokey` (`combokey`)
) ENGINE=InnoDB AUTO_INCREMENT=10585 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `teams`
-- ----------------------------
DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
  `team_id` int(16) NOT NULL AUTO_INCREMENT,
  `ta_pa` int(16) NOT NULL,
  `ta_pb` int(11) NOT NULL,
  `ta_ntrp` float NOT NULL,
  `ta_untrp` float NOT NULL,
  `tb_pa` int(11) NOT NULL,
  `tb_pb` int(11) NOT NULL,
  `tb_ntrp` float NOT NULL,
  `tb_untrp` float NOT NULL,
  `season` varchar(12) NOT NULL DEFAULT '2008 fall',
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `tmp_couples`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_couples`;
CREATE TABLE `tmp_couples` (
  `cid` int(16) NOT NULL AUTO_INCREMENT,
  `m_pid` int(16) DEFAULT NULL,
  `m_name` varchar(60) DEFAULT NULL,
  `m_ntrp` float DEFAULT NULL,
  `m_untrp` float DEFAULT NULL,
  `f_pid` int(8) DEFAULT NULL,
  `f_name` varchar(60) DEFAULT NULL,
  `f_ntrp` float DEFAULT NULL,
  `f_untrp` float DEFAULT NULL,
  `c_ntrp` float DEFAULT NULL,
  `c_untrp` float DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `tmp_players`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_players`;
CREATE TABLE `tmp_players` (
  `pid` int(8) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(8) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(32) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `users`
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('1', 'kutenai', '46730ce4707e8302dc1dc1bd7f3eb575'), ('2', 'ednh', 'a5944c0b4cae8984a2c6095c84426f36'), ('3', 'fntennis', 'c4cbf6c9371a6e0232632aae111e6b60');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
