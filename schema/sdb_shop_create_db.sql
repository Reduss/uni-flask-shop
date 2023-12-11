-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sdb_shop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sdb_shop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sdb_shop` ;
USE `sdb_shop` ;

-- -----------------------------------------------------
-- Table `sdb_shop`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `phone_num` VARCHAR(13) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sdb_shop`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sdb_shop`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `price` DOUBLE NOT NULL,
  `category_id` INT NOT NULL,
  `amount_in_stock` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `category_id_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `sdb_shop`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sdb_shop`.`order_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`order_status` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sdb_shop`.`customer_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`customer_order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `status_id` INT NOT NULL,
  `order_date` DATETIME NOT NULL,
  `total_price` DOUBLE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `customer_id_idx` (`customer_id` ASC) VISIBLE,
  INDEX `status_id_idx` (`status_id` ASC) VISIBLE,
  CONSTRAINT `customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `sdb_shop`.`customer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `status_id`
    FOREIGN KEY (`status_id`)
    REFERENCES `sdb_shop`.`order_status` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sdb_shop`.`order_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdb_shop`.`order_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `amount` INT NOT NULL,
  `price` DOUBLE NULL,
  PRIMARY KEY (`id`),
  INDEX `produt_id_idx` (`product_id` ASC) VISIBLE,
  INDEX `customer_order_id_idx` (`customer_order_id` ASC) VISIBLE,
  CONSTRAINT `produt_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `sdb_shop`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer_order_id`
    FOREIGN KEY (`customer_order_id`)
    REFERENCES `sdb_shop`.`customer_order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
