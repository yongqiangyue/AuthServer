SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for AppVersion
-- ----------------------------
DROP TABLE IF EXISTS `AppVersion`;
CREATE TABLE `AppVersion` (
`appName` varchar(255) CHARACTER SET utf8 NOT NULL,
`appVersion` varchar(255) CHARACTER SET utf8 NOT NULL,
PRIMARY KEY (`appName`)
);

-- ----------------------------
-- Table structure for HouseAddress
-- ----------------------------
DROP TABLE IF EXISTS `HouseAddress`;
CREATE TABLE `HouseAddress` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`addressJson` mediumblob NULL,
`tel` bigint(30) NOT NULL,
PRIMARY KEY (`id`)
);

-- ----------------------------
-- Table structure for User
-- ----------------------------

DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `Tel` bigint(30) NOT NULL,
  `Name` varchar(255) CHARACTER SET utf8,
  `Pwd` varchar(255) CHARACTER SET utf8 NOT NULL,
  `Email` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `SigKey` text CHARACTER SET utf8,
  `CreateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastLoginTime` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Tel`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



-- ----------------------------
-- Table structure for PPDevices
-- ----------------------------
DROP TABLE IF EXISTS `PPDevices`;
CREATE TABLE `PPDevices` (
  `PPDeviceID` varchar(255) CHARACTER SET utf8  NOT NULL,
  `IsUsed` bigint(30),
  PRIMARY KEY (`PPDeviceID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for NASDevices
-- ----------------------------
DROP TABLE IF EXISTS `NASDevices`;
CREATE TABLE `NASDevices` (
  `NasId` bigint(30) NOT NULL,
  `IP` bigint(10),
  `MAC` varchar(255),
  PRIMARY KEY (`NasId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



-- ----------------------------
-- Table structure for PShare
-- ----------------------------
DROP TABLE IF EXISTS `PShare`;
CREATE TABLE `PShare` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `NasId` bigint(30) NOT NULL,
  `ShareId` int(11) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Pwd` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `Type` int(11) DEFAULT NULL,
  `ShareWith` text CHARACTER SET utf8 DEFAULT NULL,
  `ShareWithHash` varchar(255) DEFAULT NULL,
  `Notes` text CHARACTER SET utf8 DEFAULT NULL,
  `Tel` bigint(30) DEFAULT NULL,
  `CreateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `HEAT` int(11) DEFAULT '0',
  `Thumbnail` mediumblob DEFAULT NULL,
  `expiration` timestamp NULL DEFAULT NULL,
  `expirationType` int(11) DEFAULT '1',
  `accessTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  CONSTRAINT `NasId_PShare_FK` FOREIGN KEY (`NasId`) REFERENCES `NASDevices` (`NasId`),
  CONSTRAINT `Tel_PShare_FK` FOREIGN KEY (`Tel`) REFERENCES `User` (`Tel`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for UserNAS
-- ----------------------------
DROP TABLE IF EXISTS `UserNAS`;
CREATE TABLE `UserNAS` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Tel` bigint(30) NOT NULL,
  `NasId` varchar(255) NOT NULL,
  `IsAdmin` tinyint(1) DEFAULT FALSE,
  PRIMARY KEY (`Id`),
  KEY `Tel_UserNAS_index` (`Tel`) USING BTREE,
  CONSTRAINT `Tel_UserNAS_FK` FOREIGN KEY (`Tel`) REFERENCES `User` (`Tel`),
  CONSTRAINT `NasId_UserNAS_FK` FOREIGN KEY (`NasId`) REFERENCES `NASDevices` (`NasId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for UserSession
-- ----------------------------
DROP TABLE IF EXISTS `UserSession`;
CREATE TABLE `UserSession` (
  `Tel` bigint(30) NOT NULL,
  `RandomCode` int(10) NOT NULL,
  `CreateTime` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Tel`),
  CONSTRAINT `Tel_UserSession_FK` FOREIGN KEY (`Tel`) REFERENCES `User` (`Tel`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

