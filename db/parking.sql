/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - parking
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`parking` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `parking`;

/*Table structure for table `addarea` */

DROP TABLE IF EXISTS `addarea`;

CREATE TABLE `addarea` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `arname` varchar(30) NOT NULL,
  `arplace` varchar(30) NOT NULL,
  `desc` varchar(150) NOT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `addarea` */

insert  into `addarea`(`aid`,`arname`,`arplace`,`desc`,`latitude`,`longitude`) values 
(1,'Kasavu Kendra','Thazhekkod','17/53, Mavoor Rd\r\nMavoor Road Junction, Opposite National Hospital, Tazhekkod\r\nKozhikode, Kerala 673001\r\nIndia','11.259019635245838','75.781529545784'),
(2,'Distric court','Mananchira','Court Rd\r\nMananchira\r\nKozhikode, Kerala 673032\r\nIndia','11.251898543522012','75.77552407979965'),
(3,'Ashoka hospital','KOZHIKODE','134, Kozhikode - Palakkad Hwy\r\nPolpaya Mana, Tazhekkod\r\nKozhikode, Kerala 673004\r\nIndia','11.257835867890503','75.78059077262878'),
(4,'KSRTC','KOZHIKODE',' near kozhikode ksrtc stand Mavoor road calicut','11.259367768933968','75.78298442456916');

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `bookid` int(10) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `entime` datetime NOT NULL,
  `extime` datetime NOT NULL,
  `sid` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `vehno` varchar(30) DEFAULT NULL,
  `slot` int(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`bookid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`bookid`,`uid`,`entime`,`extime`,`sid`,`status`,`vehno`,`slot`,`name`) values 
(1,17,'2022-06-26 16:30:00','2022-06-26 18:30:00',43,'booked','KL12K9886',8,'AMAL'),
(2,17,'2022-06-27 00:30:00','2022-06-27 01:30:00',39,'booked','KL57A9886',4,'ADIL'),
(3,17,'2022-06-26 04:30:00','2022-06-26 06:31:00',39,'booked','KL12K9886',4,'jilson'),
(4,17,'2022-06-30 00:54:00','2022-06-30 02:54:00',1,'booked','KL12A8762',1,'Manu'),
(5,17,'0000-00-00 00:00:00','2022-06-30 17:00:00',7,'booked','KL11X9852',3,'Ajay'),
(6,17,'2022-06-26 18:00:00','2022-06-26 19:00:00',1,'booked','KL11AB2532',1,'Luthfab'),
(7,17,'2022-06-30 17:05:00','2022-06-30 19:05:00',38,'booked','KL12L9988',3,'abu'),
(8,16,'2022-06-26 18:00:00','2022-06-26 20:29:00',39,'booked','KL12K9886',4,'Jilson'),
(9,16,'2022-06-26 18:00:00','2022-06-26 20:29:00',39,'booked','KL12K9886',4,'Jilson'),
(10,16,'2022-06-28 15:00:00','2022-06-28 16:00:00',7,'booked','KL12C2219',3,'anagha a'),
(11,16,'2022-06-28 16:00:00','2022-06-28 17:00:00',26,'booked','KL12K9886',1,'jilson');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(10) NOT NULL,
  `usertype` varchar(20) NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`lid`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'jilsonjil16@gmail.com','04-11-1998','manager'),
(3,'prasoonp@gmail.com','01-01-1999','manager'),
(4,'varun@gmail.com','28-02-1997','staff'),
(5,'manu@gmail.com','07-12-2018','staff'),
(6,'jj@jj.com','02-12-2018','staff'),
(7,'jilsonjil16@gmail.com','28-12-2018','staff'),
(8,'jilsonjil16@gmail.com','28-12-2018','staff'),
(9,'irshad@gmail.com','30-03-1998','staff'),
(10,'irshad@gmail.com','30-03-1998','staff'),
(11,'vyshak@gmail.com','13-08-1999','staff'),
(12,'jelvin@gmail.com','20-12-2018','staff'),
(13,'luthfan@gmail.com','05-08-1999','manager'),
(14,'sarthaj@gmail.com','02-06-1999','manager'),
(15,'lithin@gmail.com','02-01-1999','staff'),
(16,'varun@gmail.com','Varun@12','user'),
(17,'manu@gmail.com','Manu@123','user'),
(18,'Manu@gmail.com','Manu@1234','user');

/*Table structure for table `manager` */

DROP TABLE IF EXISTS `manager`;

CREATE TABLE `manager` (
  `pm_id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(20) DEFAULT NULL,
  `address` varchar(70) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `aid` int(10) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`pm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `manager` */

insert  into `manager`(`pm_id`,`fullname`,`address`,`gender`,`dob`,`mail`,`phone`,`photo`,`aid`,`status`) values 
(1,'JILSON JOSE','Cherumalayil house,Thariyode po','Male','1998-11-04','jilsonjil16@gmail.com',8075046628,'Jilson.jpg',2,'Active'),
(2,'Prasoon p','Thaj House','Male','1999-01-01','prasoonp@gmail.com',8590494466,'images_3.jpg',1,'Active'),
(3,'Luthfan','vengeri','Male','1999-08-05','luthfan@gmail.com',9048563211,'images.jpg',3,'Active'),
(4,'sarthaj roshan','karakkat house','Male','1999-06-02','sarthaj@gmail.com',9586995831,'images_4.jpg',4,'Active');

/*Table structure for table `registration` */

DROP TABLE IF EXISTS `registration`;

CREATE TABLE `registration` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `vno` varchar(12) NOT NULL,
  `phone` bigint(20) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `registration` */

insert  into `registration`(`uid`,`lid`,`name`,`email`,`vno`,`phone`) values 
(1,20,'jilson','jilson@gmail.com','vzbz',8590494466),
(2,16,'varun','varun@gmail.com','gsbsb',8590494466),
(3,17,'Manu','manu@gmail.com','kl12k9886',8590494466),
(4,18,'Manu','Manu@gmail.com','KL12K9886',8590494466);

/*Table structure for table `slot` */

DROP TABLE IF EXISTS `slot`;

CREATE TABLE `slot` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `aid` int(11) DEFAULT NULL,
  `slot_no` int(11) DEFAULT NULL,
  `floor` int(11) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=latin1;

/*Data for the table `slot` */

insert  into `slot`(`sid`,`aid`,`slot_no`,`floor`,`status`,`type`) values 
(1,2,1,1,'free','R'),
(2,2,2,1,'free','R'),
(5,2,1,2,'free','R'),
(6,2,2,2,'free','R'),
(7,2,3,2,'free','R'),
(8,2,4,2,'free','R'),
(9,2,5,2,'free','R'),
(10,2,6,2,'free','R'),
(11,2,7,2,'free','R'),
(12,2,8,2,'free','R'),
(13,2,9,2,'free','R'),
(14,2,10,2,'free','R'),
(15,3,1,1,'free','R'),
(16,3,2,1,'free','R'),
(17,3,3,1,'free','R'),
(18,3,4,1,'free','R'),
(19,3,5,1,'free','R'),
(20,3,1,1,'free','R'),
(21,3,2,1,'free','NR'),
(22,3,3,1,'free','NR'),
(23,3,4,1,'free','NR'),
(24,3,5,1,'Booked','NR'),
(25,3,6,1,'free','NR'),
(26,2,1,3,'free','R'),
(27,2,2,3,'free','R'),
(28,2,3,3,'free','R'),
(29,2,4,3,'free','R'),
(30,2,5,3,'free','R'),
(31,2,6,3,'free','R'),
(32,2,7,3,'free','R'),
(33,2,8,3,'free','R'),
(34,2,9,3,'free','R'),
(35,2,10,3,'free','R'),
(36,2,11,3,'free','R'),
(37,2,12,3,'free','R'),
(38,2,3,1,'free','R'),
(39,2,4,1,'free','R'),
(40,2,5,1,'free','R'),
(41,2,6,1,'free','R'),
(42,2,7,1,'free','R'),
(43,2,8,1,'free','R'),
(44,2,9,1,'free','R'),
(45,2,10,1,'free','R'),
(46,2,11,1,'free','R'),
(47,2,12,1,'free','R'),
(58,2,1,2,'free','NR'),
(59,2,2,2,'free','NR'),
(60,2,3,2,'free','NR'),
(61,2,4,2,'free','NR'),
(62,2,5,2,'free','NR'),
(63,2,6,2,'free','NR'),
(64,2,7,2,'free','NR'),
(65,2,8,2,'free','NR'),
(66,2,9,2,'free','NR'),
(67,2,10,2,'free','NR'),
(68,4,1,1,'free','R'),
(69,4,2,1,'free','R'),
(70,4,3,1,'free','R'),
(71,4,4,1,'free','R'),
(72,4,5,1,'free','R'),
(73,4,6,1,'free','R'),
(74,4,7,1,'free','R'),
(75,4,8,1,'free','R'),
(76,4,9,1,'free','R'),
(77,4,10,1,'free','R'),
(78,4,1,2,'free','R'),
(79,4,2,2,'free','R'),
(80,4,3,2,'free','R'),
(81,4,4,2,'free','R'),
(82,4,5,2,'free','R'),
(83,4,1,2,'free','NR'),
(84,4,2,2,'free','NR'),
(85,4,3,2,'free','NR'),
(86,4,4,2,'free','NR'),
(87,4,5,2,'free','NR'),
(88,4,6,2,'free','NR'),
(89,4,7,2,'free','NR'),
(90,4,8,2,'free','NR'),
(91,4,9,2,'free','NR'),
(92,4,10,2,'free','NR'),
(93,1,1,1,'free','R'),
(94,1,2,1,'free','R'),
(95,1,3,1,'free','R'),
(96,1,4,1,'free','R'),
(97,1,5,1,'free','R'),
(98,1,6,1,'free','R'),
(99,1,7,1,'free','R'),
(100,1,8,1,'free','R'),
(101,1,9,1,'free','R'),
(102,1,10,1,'free','R'),
(103,1,1,1,'free','NR'),
(104,1,2,1,'free','NR'),
(105,1,3,1,'free','NR'),
(106,1,4,1,'free','NR'),
(107,1,5,1,'free','NR');

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `address` varchar(30) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `photo` varchar(30) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `staff` */

insert  into `staff`(`sid`,`name`,`gender`,`address`,`dob`,`mail`,`phone`,`photo`,`status`) values 
(1,'Irshad','Male','Male','1998-03-30','irshad@gmail.com',8590494462,'images.jpg','Active'),
(2,'Vyshak','Male','Male','1999-08-13','vyshak@gmail.com',8956989567,'images_1.jpg','Inactive'),
(3,'Jelvin jaison','Male','Kurunnumkara house wayanad','2018-12-20','jelvin@gmail.com',9447541650,'images_3.jpg','Active'),
(4,'lithin krishna','Male','Valiya nirappil','1999-01-02','lithin@gmail.com',8590494466,'images_1.jpg','Active');

/*Table structure for table `vehicle` */

DROP TABLE IF EXISTS `vehicle`;

CREATE TABLE `vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookid` int(11) NOT NULL,
  `entry` datetime DEFAULT NULL,
  `exit` varchar(30) DEFAULT NULL,
  `sid` int(11) DEFAULT NULL,
  `vehno` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`,`bookid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `vehicle` */

insert  into `vehicle`(`id`,`bookid`,`entry`,`exit`,`sid`,`vehno`,`status`) values 
(1,11,'2022-06-23 15:33:37','null',3,'KL13AS0150','null'),
(2,11,'2022-06-23 15:35:08','null',3,'KL11BT1065','null'),
(4,11,'2022-06-27 12:21:43','null',3,'KL12A4456','null');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
