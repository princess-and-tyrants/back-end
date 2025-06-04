-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: mbtid
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cardcase`
--

DROP TABLE IF EXISTS `cardcase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cardcase` (
  `cardcase_id` varchar(50) NOT NULL COMMENT 'Primary Key (UUID)',
  `owner_user_id` varchar(50) NOT NULL COMMENT '명함 보관자 (Owner)',
  `collected_user_id` varchar(50) NOT NULL COMMENT '명함 소유자 (Collected)',
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일',
  `modified_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
  `is_deleted` varchar(1) NOT NULL DEFAULT 'N' COMMENT '삭제 여부 (''N'': 활성, ''Y'': 삭제됨)',
  PRIMARY KEY (`cardcase_id`),
  KEY `fk_owner_user` (`owner_user_id`),
  KEY `fk_collected_user` (`collected_user_id`),
  CONSTRAINT `fk_collected_user` FOREIGN KEY (`collected_user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_owner_user` FOREIGN KEY (`owner_user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='명함 보관함 테이블';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cardcase`
--

LOCK TABLES `cardcase` WRITE;
/*!40000 ALTER TABLE `cardcase` DISABLE KEYS */;
/*!40000 ALTER TABLE `cardcase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(50) NOT NULL COMMENT 'UUID',
  `id` varchar(50) NOT NULL COMMENT '사용자 ID, 고유 값',
  `mbti_ei_score` int NOT NULL COMMENT 'MBTI 1번째 (E,I) [0(100)~100(0)]',
  `mbti_sn_score` int NOT NULL COMMENT 'MBTI 2번째 (S,N) [0(100)~100(0)]',
  `mbti_tf_score` int NOT NULL COMMENT 'MBTI 3번째 (T,F) [0(100)~100(0)]',
  `mbti_pj_score` int NOT NULL COMMENT 'MBTI 4번째 (P,J) [0(100)~100(0)]',
  `nickname` varchar(50) NOT NULL COMMENT '닉네임',
  `password` varchar(255) NOT NULL COMMENT '비밀번호 (암호화된 해시 사용)',
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일',
  `modified_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
  `is_deleted` varchar(1) NOT NULL DEFAULT 'N' COMMENT '삭제 여부 (''N'': 활성, ''Y'': 삭제됨)',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `unique_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='사용자 테이블';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('02d2a7ce-75c9-4059-aa16-8994da2f7ef3','admin2',100,0,100,0,'admin2','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-06-04 00:01:26',NULL,'N'),('1b64fb7f-b0b6-4c15-8ea8-ffceaa9f948a','admin',100,0,100,0,'admin','$2b$12$DVpawvHdH5JY657yVmUXZuMlwBSL1OrGYpvBB15r2UqCEmxGtl63i','2025-06-04 00:01:04',NULL,'N'),('550e8400-e29b-41d4-a716-446655440000','user1',70,60,80,50,'Nickname1','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-01-01 10:00:00','2025-06-04 00:01:37','N'),('550e8400-e29b-41d4-a716-446655440001','user2',40,50,30,90,'Nickname2','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-01-02 11:00:00','2025-06-04 00:01:37','Y'),('550e8400-e29b-41d4-a716-446655440002','user3',90,20,70,40,'Nickname3','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-01-02 12:00:00','2025-06-04 00:01:37','N'),('550e8400-e29b-41d4-a716-446655440003','user4',30,40,50,60,'Nickname4','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-01-03 13:00:00','2025-06-04 00:01:37','N'),('550e8400-e29b-41d4-a716-446655440004','user5',50,70,40,80,'Nickname5','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-01-04 14:00:00','2025-06-04 00:01:37','Y'),('550e8400-e29b-41d4-a716-446655440005','iuholic83',45,40,30,15,'string1','$2b$12$PlOMLJVCS0IZ2KK0Z6uO1.SMXA3x5MCmSnqlmertnyQ7FSIsXjBaa','2025-06-03 23:52:32','2025-06-04 00:42:21','N');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vote` (
  `vote_id` varchar(50) NOT NULL COMMENT '투표 고유 ID (PK)',
  `link_id` varchar(50) NOT NULL COMMENT '징검다리 테이블(vote_link)의 ID (FK)',
  `voting_user_id` varchar(50) NOT NULL COMMENT '투표를 한 유저 ID (user 테이블의 user_id를 참조)',
  `first_mbti_element` varchar(1) NOT NULL COMMENT 'MBTI 첫 번째 요소 (E/I)',
  `second_mbti_element` varchar(1) NOT NULL COMMENT 'MBTI 두 번째 요소 (S/N)',
  `third_mbti_element` varchar(1) NOT NULL COMMENT 'MBTI 세 번째 요소 (T/F)',
  `forth_mbti_element` varchar(1) NOT NULL COMMENT 'MBTI 네 번째 요소 (P/J)',
  `comment` text COMMENT '투표 관련 코멘트',
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일',
  `modified_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
  `is_deleted` varchar(1) NOT NULL DEFAULT 'N' COMMENT '삭제 여부 (''N'': 활성, ''Y'': 삭제됨)',
  `incognito` varchar(1) NOT NULL COMMENT '가명',
  PRIMARY KEY (`vote_id`),
  UNIQUE KEY `vote_unique` (`link_id`,`voting_user_id`),
  KEY `voting_user_id` (`voting_user_id`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`link_id`) REFERENCES `vote_link` (`link_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vote_ibfk_2` FOREIGN KEY (`voting_user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='투표 테이블';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote_link`
--

DROP TABLE IF EXISTS `vote_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vote_link` (
  `link_id` varchar(50) NOT NULL COMMENT 'UUID (PK)',
  `target_user_id` varchar(50) NOT NULL COMMENT '투표 대상 유저 ID (user 테이블의 user_id를 참조)',
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일',
  `modified_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일',
  `is_deleted` varchar(1) NOT NULL DEFAULT 'N' COMMENT '삭제 여부 (''N'': 활성, ''Y'': 삭제됨)',
  PRIMARY KEY (`link_id`),
  UNIQUE KEY `vote_link_unique` (`target_user_id`),
  CONSTRAINT `vote_link_ibfk_1` FOREIGN KEY (`target_user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='투표 징검다리 테이블';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote_link`
--

LOCK TABLES `vote_link` WRITE;
/*!40000 ALTER TABLE `vote_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mbtid'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-05  1:24:05
