-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema medserver
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema medserver
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `medserver` DEFAULT CHARACTER SET utf8 ;
USE `medserver` ;

-- -----------------------------------------------------
-- Table `medserver`.`areas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medserver`.`areas` (
  `id` INT NOT NULL,
  `area_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medserver`.`doctors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medserver`.`doctors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `mail` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `card` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `area_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_doctors_areas1_idx` (`area_id` ASC) VISIBLE,
  CONSTRAINT `fk_doctors_areas1`
    FOREIGN KEY (`area_id`)
    REFERENCES `medserver`.`areas` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medserver`.`patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medserver`.`patients` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `mail` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `dx` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medserver`.`notes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medserver`.`notes` (
  `id` INT NOT NULL,
  `descirption` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medserver`.`sessions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medserver`.`sessions` (
  `id` INT NOT NULL,
  `date` DATE NULL,
  `hour` TIME NULL,
  `amount` INT NULL,
  `doctor_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `note_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sessions_doctors_idx` (`doctor_id` ASC) VISIBLE,
  INDEX `fk_sessions_patients1_idx` (`patient_id` ASC) VISIBLE,
  INDEX `fk_sessions_comment1_idx` (`note_id` ASC) VISIBLE,
  CONSTRAINT `fk_sessions_doctors`
    FOREIGN KEY (`doctor_id`)
    REFERENCES `medserver`.`doctors` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sessions_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `medserver`.`patients` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sessions_comment1`
    FOREIGN KEY (`note_id`)
    REFERENCES `medserver`.`notes` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
