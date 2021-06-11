ALTER TABLE `fasthealth`.`patients`
ADD COLUMN `gender` VARCHAR(20) NOT NULL AFTER `userid`,
ADD COLUMN `age` INT NOT NULL AFTER `gender`,
ADD COLUMN `nricno` VARCHAR(25) NOT NULL AFTER `age`,
ADD COLUMN `contactno` VARCHAR(25) NOT NULL AFTER `nricno`,
ADD COLUMN `address` VARCHAR(255) NOT NULL AFTER `usercol`,
ADD COLUMN `email` VARCHAR(100) NOT NULL AFTER `address`,
ADD COLUMN `dob` DATETIME NULL AFTER `email`,
CHANGE COLUMN `patientname` `patientname` VARCHAR(100) NOT NULL ;