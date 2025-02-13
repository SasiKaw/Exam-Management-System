SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `exammanagementsystem` DEFAULT CHARACTER SET utf8;
USE `exammanagementsystem`;

-- -----------------------------------------------------
-- Table `programs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `programs` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Level` int NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `batches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `batches` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Programs_ID` int NOT NULL,
  `Current_Level` varchar(45) NOT NULL DEFAULT '1',
  `is_active` tinyint NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Batches_Programs1`
    FOREIGN KEY (`Programs_ID`)
    REFERENCES `programs` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `semesters`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semesters` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Start_date` date NOT NULL,
  `End_date` date NOT NULL,
  `Status` tinyint NULL DEFAULT 1,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `subjects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `subjects` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Code` varchar(45) NOT NULL,
  `Total_credit` int,
  `Theory_credit` int,
  `Practical_credit` int,
  `Level` int NOT NULL,
  `Programs_ID` int NOT NULL,
  `CA` int NOT NULL,
  `FE` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Subjects_Programs1`
    FOREIGN KEY (`Programs_ID`)
    REFERENCES `programs` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `courses` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Semesters_ID` int NOT NULL,
  `Subjects_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Courses_Semesters1`
    FOREIGN KEY (`Semesters_ID`)
    REFERENCES `semesters` (`ID`),
  CONSTRAINT `fk_Courses_Subjects1`
    FOREIGN KEY (`Subjects_ID`)
    REFERENCES `subjects` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `repeat_enrollment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `repeat_enrollment` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `attemp_no` int NOT NULL,
  `assessment_type` VARCHAR(10) NOT NULL,
  `students_ID` int NOT NULL,
  `courses_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_repeat_enrollment_students`
    FOREIGN KEY (`students_ID`)
    REFERENCES `students` (`ID`),
  CONSTRAINT `fk_repeat_enrollment_courses1`
    FOREIGN KEY (`courses_ID`)
    REFERENCES `courses` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `courses_batches`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `courses_batches` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Courses_ID` int NOT NULL,
  `Batches_ID` int NOT NULL,
  `status` tinyint  DEFAULT 0,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Courses_Batches_Courses1`
    FOREIGN KEY (`Courses_ID`)
    REFERENCES `courses` (`ID`),
  CONSTRAINT `fk_Courses_Batches_Batches1`
    FOREIGN KEY (`Batches_ID`)
    REFERENCES `batches` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `students` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Index_No` varchar(45),
  `Name` varchar(100) NOT NULL,
  `auth_user_id` int NOT NULL,
  `batches_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_students_batches1`
    FOREIGN KEY (`batches_ID`)
    REFERENCES `batches` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `criterias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `criterias` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nature` enum('In class','Quiz','Essay','MCQ') NOT NULL,
  `Type` enum('CA','FE') NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Weights` int NOT NULL,
  `Courses_ID` int NOT NULL,
  `Max_mark` int NULL DEFAULT 0,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Criterias_Courses1`
    FOREIGN KEY (`Courses_ID`)
    REFERENCES `courses` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `ca_sechedule`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ca_sechedule` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Start_date` DATE NOT NULL,
  `criterias_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_CA_Sechedule_criterias1`
    FOREIGN KEY (`criterias_ID`)
    REFERENCES `criterias` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `students_criterias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `students_criterias` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Students_ID` int NOT NULL,
  `Criterias_ID` int NOT NULL,
  `Mark` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `fk_Students_Criterias_Students1`
    FOREIGN KEY (`Students_ID`)
    REFERENCES `students` (`ID`),
  CONSTRAINT `fk_Students_Criterias_Criterias1`
    FOREIGN KEY (`Criterias_ID`)
    REFERENCES `criterias` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `results` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Grade` varchar(20),
  `S_grade` varchar(45),
  `Courses_ID` int NOT NULL,
  `Students_ID` int NOT NULL,
  `Parent_ID` int,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Results_Courses1`
    FOREIGN KEY (`Courses_ID`)
    REFERENCES `courses` (`ID`),
  CONSTRAINT `fk_Results_Students1`
    FOREIGN KEY (`Students_ID`)
    REFERENCES `students` (`ID`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `courses_student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `courses_student` (
  `Enroll_Id` int NOT NULL AUTO_INCREMENT,
  `Marks` decimal(10,0) NOT NULL,
  `Students_ID` int NOT NULL,
  `Courses_ID` int NOT NULL,
  `Level` int NULL,
  `Attemp` int NULL,
  PRIMARY KEY (`Enroll_Id`),
  CONSTRAINT `fk_Students_Courses_Students`
    FOREIGN KEY (`Students_ID`)
    REFERENCES `students` (`ID`),
  CONSTRAINT `fk_Students_Courses_Courses1`
    FOREIGN KEY (`Courses_ID`)
    REFERENCES `courses` (`ID`)
) ENGINE=InnoDB;

-- Add Lecturers table
CREATE TABLE IF NOT EXISTS `lecturers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `auth_user_id` int NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_lecturers_auth_user1` 
    FOREIGN KEY (`auth_user_id`) 
    REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB;

-- Add Courses Lecturer table
CREATE TABLE IF NOT EXISTS `courses_lecturer` (
  `Id` varchar(45) NOT NULL,
  `Lectures_ID` int NOT NULL,
  `Courses_ID` int NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `fk_Lectures_has_Courses_Lectures1`
    FOREIGN KEY (`Lectures_ID`)
    REFERENCES `lecturers` (`ID`),
  CONSTRAINT `fk_Lectures_has_Courses_Courses1`
    FOREIGN KEY (`Courses_ID`)
    REFERENCES `courses` (`ID`)
) ENGINE=InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;