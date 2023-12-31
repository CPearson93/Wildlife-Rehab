-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wildlife_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `wildlife_schema` ;

-- -----------------------------------------------------
-- Schema wildlife_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wildlife_schema` DEFAULT CHARACTER SET utf8 ;
USE `wildlife_schema` ;

-- -----------------------------------------------------
-- Table `wildlife_schema`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wildlife_schema`.`users` ;

CREATE TABLE IF NOT EXISTS `wildlife_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(255) NULL,
  `lastName` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `createdAt` DATETIME NULL DEFAULT NOW(),
  `updateAt` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wildlife_schema`.`animals`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `wildlife_schema`.`animals` ;

CREATE TABLE IF NOT EXISTS `wildlife_schema`.`animals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickName` VARCHAR(255) NULL,
  `species` VARCHAR(255) NULL,
  `locationFound` VARCHAR(255) NULL,
  `injury` VARCHAR(255) NULL,
  `createdAt` DATETIME NULL DEFAULT NOW(),
  `updatedAt` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_animals_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_animals_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `wildlife_schema`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
