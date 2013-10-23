SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

CREATE TABLE IF NOT EXISTS `dim_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `did` int(11),
  `cid` int(10) NOT NULL,
  `tid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `did` (`did`),
  KEY `tid` (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `dim_jobrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `dim_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `time_interval` enum('DAILY','MONTHLY','YEARLY','') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `fact_employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gender` enum('MALE','FEMALE','UNDEFINED','') NOT NULL,
  `did` int(11) NOT NULL,
  `jid` int(10) NOT NULL,
  `tid` int(11) NOT NULL,
  `cid` int(10) NOT NULL,
  `salary` double NOT NULL,
  `manager` tinyint(1) NOT NULL,
  `age` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `did` (`did`),
  KEY `jid` (`jid`),
  KEY `tid` (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

ALTER TABLE `dim_department`
  ADD CONSTRAINT `dim_department_ibfk_2` FOREIGN KEY (`tid`) REFERENCES `dim_time` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `dim_department_ibfk_1` FOREIGN KEY (`did`) REFERENCES `dim_department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `fact_employee`
  ADD CONSTRAINT `fact_employee_ibfk_3` FOREIGN KEY (`tid`) REFERENCES `dim_time` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fact_employee_ibfk_1` FOREIGN KEY (`did`) REFERENCES `dim_department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fact_employee_ibfk_2` FOREIGN KEY (`jid`) REFERENCES `dim_jobrole` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
