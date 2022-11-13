-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema medcenter
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema medcenter
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `medcenter` DEFAULT CHARACTER SET utf8 ;
USE `medcenter` ;

-- -----------------------------------------------------
-- Table `medcenter`.`areas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`areas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `area_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medcenter`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `mail` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medcenter`.`doctors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`doctors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `card` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `area_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_doctors_areas1_idx` (`area_id` ASC) VISIBLE,
  INDEX `fk_doctors_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_doctors_areas1`
    FOREIGN KEY (`area_id`)
    REFERENCES `medcenter`.`areas` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_doctors_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `medcenter`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medcenter`.`patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`patients` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `birthday` DATE NULL,
  `dx` VARCHAR(45) NULL,
  `amount` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_patients_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_patients_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `medcenter`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medcenter`.`notes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`notes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `medcenter`.`sessions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `medcenter`.`sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `hour` TIME NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `doctor_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `note_id` INT NOT NULL,
  `area_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sessions_doctors_idx` (`doctor_id` ASC) VISIBLE,
  INDEX `fk_sessions_patients1_idx` (`patient_id` ASC) VISIBLE,
  INDEX `fk_sessions_comment1_idx` (`note_id` ASC) VISIBLE,
  INDEX `fk_sessions_areas1_idx` (`area_id` ASC) VISIBLE,
  CONSTRAINT `fk_sessions_doctors`
    FOREIGN KEY (`doctor_id`)
    REFERENCES `medcenter`.`doctors` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sessions_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `medcenter`.`patients` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sessions_comment1`
    FOREIGN KEY (`note_id`)
    REFERENCES `medcenter`.`notes` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_sessions_areas1`
    FOREIGN KEY (`area_id`)
    REFERENCES `medcenter`.`areas` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
