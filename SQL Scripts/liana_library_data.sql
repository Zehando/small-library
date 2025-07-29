-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: lianas_library
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES ('978-0061120084','Biography of a Leader','Doris','Goodwin','History House',2005,'Biography'),('978-0132350884','Science Fiction Odyssey','Arthur','Clarke','Galaxy Press',1968,'Science Fiction'),('978-0307277671','Self-Help Guide','Stephen','Covey','Success Books',1989,'Self-Help'),('978-0321765723','The Great Adventure','John','Doe','Adventure Books Inc.',2020,'Adventure'),('978-0345339685','The Art of Cooking','Julia','Child','Gourmet Guides',1961,'Cookbook'),('978-0451524935','Fantasy Realm','J.R.R.','Tolkien','Mythic Tales',1954,'Fantasy'),('978-0590353403','Children\'s ABC','Dr.','Seuss','Kids Books Ltd.',1990,'Children\'s'),('978-0743273565','Poetry Collection','Maya','Angelou','Verse Publishers',1978,'Poetry'),('978-0743273566','Historical Echoes','Emily','Bronte','Timeless Classics',1847,'Historical Fiction'),('978-1234567890','Mystery of the Old House','Jane','Smith','Mystery Publishers',2018,'Mystery');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,1,'978-0321765723','2024-01-01','2024-01-15'),(2,2,'978-1234567890','2024-01-05','2024-01-20'),(3,3,'978-0132350884','2024-01-10','2025-07-25'),(4,4,'978-0743273565','2024-01-12','2025-07-28'),(5,1,'978-0451524935','2024-02-05','2025-07-25'),(6,7,'978-0307277671','2025-07-25','2025-07-28'),(7,4,'978-0590353403','2025-07-25',NULL),(8,13,'978-0451524935','2025-07-27',NULL);
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (1,'Alice','Smith','2023-01-15','123 Oak Ave, Anytown, USA','555-111-2222','alice.smith@example.com','facebook.com/alices','Email','active'),(2,'Bob','Johnson','2023-02-20','456 Pine St, Anytown, USA','555-333-4444','bob.j@example.com','twitter.com/bobj','Mobile','active'),(3,'Charlie','Brown','2023-03-10','789 Elm Rd, Anytown, USA','555-555-6666','charlie.b@example.com','instagram.com/charlieb','Social Media','active'),(4,'Diana','Prince','2023-04-05','101 Maple Ln, Anytown, USA','555-777-8888','diana.p@example.com','linkedin.com/dianap','Email','active'),(5,'Eve','Davis','2023-05-12','202 Birch Blvd, Anytown, USA','555-999-0000','eve.d@example.com','facebook.com/eved','Address','inactive'),(6,'Frank','White','2023-06-01','303 Cedar Ct, Anytown, USA','555-123-4567','frank.w@example.com','twitter.com/frankw','Mobile','active'),(7,'Grace','Taylor','2023-07-08','404 Spruce Dr, Anytown, USA','555-234-5678','grace.t@example.com','instagram.com/gracet','Email','active'),(8,'Henry','Miller','2023-08-19','505 Willow Way, Anytown, USA','555-345-6789','henry.m@example.com','linkedin.com/henrym','Social Media','suspended'),(9,'Ivy','Moore','2023-09-25','606 Poplar Pl, Anytown, USA','555-456-7890','ivy.m@example.com','facebook.com/ivym','Email','active'),(10,'Jack','Hall','2023-10-30','707 Aspen Apt, Anytown, USA','555-567-8901','jack.h@example.com','twitter.com/jackh','Mobile','active'),(11,'Eve','Adams','2022-05-05','202 Birch Ct, Anytown, CA 90210','555-1005','eve.a@example.com','@eveadams','Email','active'),(12,'Ivy','King','2022-09-01','606 Poplar Pl, Anytown, CA 90210','555-1009','ivy.k@example.com','@ivyking','Address','active'),(13,'Jack','Green','2022-10-10','707 Ash Ct, Anytown, CA 90210','555-1010','jack.g@example.com','@jackgreen','Social Media','active'),(14,'Karen','Hall','2022-11-15','808 Fir Ave, Anytown, CA 90210','555-1011','karen.h@example.com','@karenhall','Email','active'),(15,'Liam','Baker','2022-12-01','909 Walnut St, Anytown, CA 90210','555-1012','liam.b@example.com','@liambaker','Mobile','active'),(16,'Mia','Wright','2023-01-05','111 Cherry Ln, Anytown, CA 90210','555-1013','mia.w@example.com','@miawright','Email','active'),(17,'Noah','Scott','2023-02-14','222 Peach Rd, Anytown, CA 90210','555-1014','noah.s@example.com','@noahscott','Mobile','active'),(18,'Olivia','Rivera','2023-03-20','333 Plum Dr, Anytown, CA 90210','555-1015','olivia.r@example.com','@oliviarivera','Address','active'),(20,'Quinn','Lewis','2023-05-09','555 Berry Ct, Anytown, CA 90210','555-1017','quinn.l@example.com','@quinnlewis','Email','active'),(23,'Tina','Nelson','2023-08-30','888 Date Ave, Anytown, CA 90210','555-1020','tina.n@example.com','@tinanelson','Mobile','active'),(24,'Ursula','Carter','2023-09-05','999 Olive St, Anytown, CA 90210','555-1021','ursula.c@example.com','@ursulacarter','Address','active'),(25,'Victor','Mitchell','2023-10-11','123 Lemon Ln, Anytown, CA 90210','555-1022','victor.m@example.com','@victormitchell','Social Media','active'),(26,'Wendy','Perez','2023-11-19','456 Lime Rd, Anytown, CA 90210','555-1023','wendy.p@example.com','@wendyperez','Email','active'),(27,'Xavier','Roberts','2023-12-25','789 Orange Dr, Anytown, CA 90210','555-1024','xavier.r@example.com','@xavierroberts','Mobile','active'),(28,'Yara','Turner','2024-01-01','101 Grapefruit Blvd, Anytown, CA 90210','555-1025','yara.t@example.com','@yaraturner','Email','active'),(29,'Zack','Phillips','2024-02-08','202 Kiwi Ct, Anytown, CA 90210','555-1026','zack.p@example.com','@zackphillips','Mobile','active'),(30,'Anna','Campbell','2024-03-14','303 Mango Way, Anytown, CA 90210','555-1027','anna.c@example.com','@annacampbell','Address','active'),(31,'Ben','Parker','2024-04-21','404 Papaya Pl, Anytown, CA 90210','555-1028','ben.p@example.com','@benparker','Social Media','active'),(32,'Chloe','Evans','2024-05-03','505 Guava Ave, Anytown, CA 90210','555-1029','chloe.e@example.com','@chloeevans','Email','active'),(33,'David','Edwards','2024-06-10','606 Lychee St, Anytown, CA 90210','555-1030','david.e@example.com','@davidedwards','Mobile','active'),(34,'Ella','Collins','2024-07-17','707 Dragonfruit Ln, Anytown, CA 90210','555-1031','ella.c@example.com','@ellacollins','Email','active'),(35,'Finn','Stewart','2024-08-24','808 Rambutan Rd, Anytown, CA 90210','555-1032','finn.s@example.com','@finnstewart','Mobile','active'),(36,'Gia','Sanchez','2024-09-01','909 Starfruit Dr, Anytown, CA 90210','555-1033','gia.s@example.com','@giasanchez','Address','active'),(37,'Hugh','Morris','2024-10-08','111 Passionfruit Blvd, Anytown, CA 90210','555-1034','hugh.m@example.com','@hughmorris','Social Media','active'),(38,'Isla','Rogers','2024-11-15','222 Persimmon Ct, Anytown, CA 90210','555-1035','isla.r@example.com','@islarogers','Email','active'),(39,'Jake','Reed','2024-12-22','333 Pomegranate Way, Anytown, CA 90210','555-1036','jake.r@example.com','@jakereed','Mobile','active'),(40,'Kira','Cook','2025-01-01','444 Fig Tree Pl, Anytown, CA 90210','555-1037','kira.c@example.com','@kiracook','Email','active'),(41,'Leo','Morgan','2025-02-07','555 Date Palm Ave, Anytown, CA 90210','555-1038','leo.m@example.com','@leomorgan','Mobile','active'),(42,'Maya','Bell','2025-03-14','666 Apricot St, Anytown, CA 90210','555-1039','maya.b@example.com','@mayabell','Address','active'),(43,'Nora','Murphy','2025-04-21','777 Nectarine Ln, Anytown, CA 90210','555-1040','nora.m@example.com','@noramurphy','Social Media','active'),(44,'Oscar','Bailey','2025-05-03','888 Cherry Blossom Rd, Anytown, CA 90210','555-1041','oscar.b@example.com','@oscarbailey','Email','active'),(45,'Penny','Cooper','2025-06-10','999 Peach Tree Dr, Anytown, CA 90210','555-1042','penny.c@example.com','@pennycooper','Mobile','active'),(46,'Quinn','Howard','2025-07-17','123 Apple Blvd, Anytown, CA 90210','555-1043','quinn.h@example.com','@quinnhoward','Email','active'),(47,'Ryan','Ward','2025-07-20','456 Pear Ct, Anytown, CA 90210','555-1044','ryan.w@example.com','@ryanward','Mobile','active'),(48,'Sophia','Torres','2025-07-21','789 Orange Grove Way, Anytown, CA 90210','555-1045','sophia.t@example.com','@sophiatorres','Address','active'),(49,'Tom','Ramirez','2025-07-22','101 Lemon Zest Pl, Anytown, CA 90210','555-1046','tom.r@example.com','@tomramirez','Social Media','active'),(50,'Uma','Gonzales','2025-07-23','202 Lime Twist Ave, Anytown, CA 90210','555-1047','uma.g@example.com','@umagonzales','Email','active'),(51,'Vance','Price','2025-07-24','303 Grape Vine St, Anytown, CA 90210','555-1048','vance.p@example.com','@vanceprice','Mobile','active'),(52,'Will','Foster','2025-07-24','404 Berry Patch Ln, Anytown, CA 90210','555-1049','will.f@example.com','@willfoster','Email','active'),(53,'Zara','Ross','2025-07-24','505 Melon Field Rd, Anytown, CA 90210','555-1050','zara.r@example.com','@zaraross','Mobile','active'),(54,'Peter','Clark','2023-04-01','444 Grape Blvd, Anytown, CA 90210','555-1016','peter.c@example.com','@peterclark','Social Media','active'),(55,'Rachel','Young','2023-06-17','666 Melon Way, Anytown, CA 90210','555-1018','rachel.y@example.com','@rachelyoung','Mobile','active'),(56,'Sam','Harris','2023-07-22','777 Fig Pl, Anytown, CA 90210','555-1019','sam.h@example.com','@samharris','Email','active');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$1Ur/pndXtFWcorUxBEEmFe45Y1oV97NXMhSrN.ztPt65lfxKXDATm','admin'),(2,'liana','$2b$12$.EP5yAKQe3XRuWopqYjJveEqGoQ5LnYqzXJ6FA05hz10kb0B5ADb6','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-28 14:17:03
