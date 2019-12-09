--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  `url` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
INSERT INTO `menu` VALUES (1,'General',NULL,NULL),(2,'Sub menu',1,NULL);
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(36) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `question` varchar(128) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
INSERT INTO `questions` VALUES (1,'hello','test','How are you','2019-12-09 11:46:57');
UNLOCK TABLES;